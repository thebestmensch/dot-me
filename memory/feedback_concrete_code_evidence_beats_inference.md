---
name: concrete-code-evidence-beats-inference
description: "When two reviewers (devils-advocate + Codex, or any two raters) reach opposite conclusions on the same point, follow the one citing specific file:line evidence; the inferential one is reasoning from priors that may not hold."
metadata:
  node_type: memory
  type: feedback
---

When two reviewers reach **opposite conclusions on the same point**, defer to the one citing concrete file:line evidence. The inferential reviewer is reasoning from priors that may not match the actual codebase.

**Why:** Reviewers (whether subagents, Codex, or human) work from priors + reading. Inferential conclusions are vulnerable to a wrong prior; code-evidence conclusions are anchored to verifiable state. When they diverge, the prior was wrong, not the code.

Validated 2026-05-19 (workspace-restructure DA+Codex co-dispatch):
- DA verdict #1 ("BLOCKER, remove deprecated `oneonme` shorthand"): reasoned that the registered shorthand was the deprecated org based on session conversation, no code evidence.
- Codex #6 ("Minor, removing it is premature"): cited `mobile-app/scripts/sentryToken.ts:47` requiring `OP_ACCOUNT` env var for an opt-in fallback path. Concrete code dependency.
- The DA was reasoning correctly given its premise; Codex's premise was the actual repo behavior. Resolution: hold off on removal until the caller audit completes — Codex won, the DA's prior didn't account for the existing `--account`-mode caller.

(The final disposition in this session was different — JM nuked both OOM accounts and re-added NEW, which sidestepped the disagreement entirely. But the *arbitration* heuristic stands: prefer the file:line citation when reviewers conflict.)

**How to apply:**

- When reviewer-A says "block this" and reviewer-B says "fine, optional fix" on the same line of work:
  - Open both reviewer outputs side-by-side.
  - If one cites `path/to/file.ts:LINE`, treat that as the higher-confidence position.
  - Verify the citation (read the file at that line) before fully committing — citations occasionally hallucinate, but rarely.
  - If both cite code and still disagree, escalate to user — the disagreement is genuine, not arbitration-resolvable.
- When the dispatched reviewer outputs no citations (vague "I think this might fail"), that's the inference-heavy side; weight it less.
- Adversarial-review's value is non-overlap signal; if it disagrees with another reviewer, don't auto-defer to it — check which one has the concrete grounding.
- Related: [[feedback_cr_cited_guidelines_unverified]] (CR citations can hallucinate; grep first), [[feedback_codex_fix_review_iteration]] (push back when finding conflicts with documented architecture).
