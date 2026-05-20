---
name: codex-inline-return-no-marker
description: "Codex adversarial-review on small diffs returns synchronously (no job id) and DOES NOT update the codex-stop-gate's `codex_dispatched` marker; commit gate still fires"
metadata:
  node_type: memory
  type: feedback
---

**Rule:** When `~/.claude/codex-dispatch.sh adversarial-review` returns a verdict inline (the wrapper output prints `ERROR: dispatch did not return a job id` and the full result JSON), Codex actually ran and the review is complete — but the `codex-stop-gate.sh` marker file (e.g. `/tmp/cc-gates/$SID/code_review_dispatched` for the codex path) is NOT written. The next `git commit` will still fire the gate complaining "no Codex cross-provider diff review landing in context."

**Why:** The wrapper expects an async background dispatch returning a job id that it polls; the inline-return path bypasses the marker-write step. Empirically validated 2026-05-20 on OOM-94 (115-line diff, ~30s synchronous return, verdict `approve` 0 findings) and OOM-93 (250-line diff, synchronous return on each of 3 rounds). The gate fires regardless of whether the review actually succeeded.

**How to apply:**
- If the wrapper prints the inline-return ERROR but the JSON shows `codex.status: 0` and a real `verdict` field — the review landed; treat it as complete.
- Bypass via `skip_codex_gate` with concrete evidence: paste the verdict + finding count + summary text into the bypass reason. This survives the classifier's "self-authoring bypass" check because the evidence is verifiable from chat.
- Re-running the wrapper does NOT fix the marker (the next inline return will also skip the marker write). Don't loop-drain attempting to "make the marker stick."
- The per-commit mtime race ([[drift-gate-tokens-per-commit]]) still applies: first commit attempt after a fresh `skip_codex_gate` typically fails because the gate's augmenter bumps `edited_files` mtime past the bypass; refresh + retry once.
- Related: [[stop-hook-bypass-prereq-invocation]] (Skill-invocation prereq), [[visual-qa-gate-session-cascade]] (parallel pattern for visual-qa cascade).
