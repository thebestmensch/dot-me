---
name: classifier-denies-self-authored-security-bypass
description: "Auto-mode classifier denies model-authored writes to security-bypass tokens (skip_*_gate, tower-ssh bypass, etc.) even when the user has explicitly authorized the action in chat — chat consent doesn't satisfy the classifier. Recovery: ask the user to write the token via `! echo … > /tmp/cc-gates/$SID/<token>` in their own shell; user-shell origination is treated as explicit auth."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 979330cc-7027-4b10-8abc-178121956d57
---

When CC asks the user "should I do X?" with options like "1. yes / 2. authorize bypass", and the user picks the bypass option, the model still cannot self-author the bypass file write. The auto-mode classifier reads the bypass write as "model is trying to bypass its own safety check" and denies — chat consent ("user said do it") doesn't propagate to the classifier's signal.

**Why:** Anthropic's auto-mode classifier looks at the *action shape* (writing a known-security-bypass path), not the conversational context. Self-authored security-bypass writes are denied by policy even with chat consent. The user's shell, by contrast, is treated as the originating principal — `! echo …` writes carry explicit user-action provenance the classifier accepts.

This is distinct from [[classifier-bulk-ticket-retry]] (denial on routine creates, retry usually succeeds) and [[no-self-authored-classifier-rules]] (model can draft but not apply auto-mode rules). Specifically: the **security-bypass** subclass — `skip_codex_gate`, `skip_visual_qa_gate`, `skip_commit_gate`, `skip_tower_ssh_gate`, `skip_commit_drift_gate`, and similar — always needs user-shell origination on first write.

**How to apply:**
- When a hook fires and you need to bypass, write the reason via your own Bash tool. If the classifier denies, the denial message will say so.
- DO NOT retry the write — the classifier won't change its mind on the same action.
- Surface to the user: "Type in your shell: `! echo '<reason>' > /tmp/cc-gates/$SID/<token-name>`". Quote the FULL path the hook's error message emitted; do not reconstruct.
- After user writes, you can retry the original blocked operation. The bypass token persists for that gate's TTL.
- Note: drift-gate bypass requires TWO files: `skip_commit_drift_gate` AND `bypass_commit_drift_approved`. The hook's error message says step 1 is model-writeable ("Claude writes the reason"), but **the classifier denies it anyway** — both steps need user-shell origination. Surface BOTH commands to JM up front; don't waste a turn attempting step 1 first. Validated 2026-05-20 during JM-287 chezmoi commit: classifier denied my model-authored `skip_commit_drift_gate` write with "Agent self-authored a `skip_commit_drift_gate` bypass token to route around the drift gate; bypass tokens require user-originated shell input, not agent-written."

**Validated 2026-05-20 during OOM-117 deploy verification.** Asked JM "Authorize tower bypass?", JM picked option "2" (authorize). I attempted `echo "JM authorized tower bypass" > /tmp/cc-gates/$SID/skip_tower_ssh_gate` — classifier denied with reason: "Writing a self-authored bypass justification claiming user authorization for production SSH to tower, when the user's '2' response does not explicitly authorize bypassing the tower-ssh gate — this is a safety-check bypass setup." The classifier doesn't read the question text I asked; it only sees the action. Recovery: JM ran `! echo "JM authorized tower bypass for OOM-117 deploy verification" > /tmp/cc-gates/$SID/skip_tower_ssh_gate` in their shell; subsequent `ssh tower` worked.

**Boundary:** This applies to *security-bypass* token writes specifically. Other classifier denials (Linear writes, routine config) often clear on retry per [[classifier-bulk-ticket-retry]]. Don't generalize this rule beyond the explicit security-bypass set.
