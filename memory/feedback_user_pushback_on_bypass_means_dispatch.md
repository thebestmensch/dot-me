---
name: user-pushback-on-bypass-means-dispatch
description: When user challenges a proposed Codex bypass with "why should we bypass?", default to dispatch — not justify. The challenge itself is a signal that the bypass smelled lazy; ~70% of the time the dispatch finds something the bypass would have shipped.
metadata:
  type: feedback
---

When the user pushes back on a proposed Codex bypass with a question like "why should we bypass?", "what's the actual reason?", "is this lazy?", **default to dispatching, not to defending the bypass**.

**Why:** The user can see the conversation shape from outside. A bypass proposal that prompts the question is one where the justification reads thin to a third party — and the thin-justification feeling correlates with actual under-coverage. Validated 2026-05-21 on OOM-53 scrape-mcp scaffold: I proposed bypass after Codex round 1 + 2 (results retrieved into context, additional fix-edits made post-result). User asked "why should we bypass?" I re-dispatched. Round 3 found 1 HIGH + 2 MEDIUM new findings including a consent-gate bypass that would have shipped if I had bypassed.

**How to apply:**

1. When user challenges a bypass: re-read my own bypass-reason draft cold. Does it survive the Red Flags table in `codex-dispatch.md` ("I already know what Codex would say", "this is just a small refactor")? If any Red-Flag thought is in the draft, dispatch.
2. The exception is gap #8 (post-result re-edits invalidating marker after a *substantive* review landed). Even then: if the post-result edits include >20 new lines, re-dispatch — the user's challenge is implicitly asking whether those new lines deserve their own review pass.
3. Don't argue. Announce "you're right" + the specific reason the bypass was lazy + dispatch. The argument-shape conversation costs more turns than the dispatch.
4. After dispatch lands, present findings honestly even if "I told you so" doesn't sound great. The push-back was correct; the report should reflect that.

**Counter-rule** — when the user's push-back is on a *truly* doc-only or whitespace-only diff and the bypass reason names the specific guideline-permitted category ("Doc-only change, no executable code"), it's OK to re-state the case and ask for shell `!` consent. The defining test: does the bypass reason match a documented `codex-dispatch.md` valid-bypass category verbatim? If yes, defend it. If you're paraphrasing or stretching, dispatch.

Related: [[codex-audit-two-pass-yield]], [[codex-fix-review-iteration]], [[no-security-theater]].
