---
name: pre-commit-gate-bypass-loop
description: "When codex-pre-commit-gate fights bypass mtime repeatedly, dispatch a real adversarial-review instead of touching markers — small diffs run inline and satisfy the gate cleanly via `result` fetch"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 765d0c02-5615-419b-8373-98a59b271a2b
---

When `codex-pre-commit-gate.sh` keeps blocking even after `touch skip_codex_gate`, stop fighting the mtime race and dispatch the real review.

**Why:** The gate's augmenter bumps `edited_files` mtime on every commit attempt, so freshly-touched bypass markers go stale instantly (gap #9 in codex-dispatch.md). After 2-3 touch-retry cycles you're loop-draining for no signal. Meanwhile `node …/codex-companion.mjs adversarial-review --background` on a small diff (< 50 lines) returns synchronously in ~20s with a verdict, and `codex-companion.mjs result` fetches it into context — gate auto-clears via the `codex_diff_handled` marker the companion writes itself. Cleaner, faster, and produces real signal you can cite if CR follow-ups land. Validated 2026-05-17 on jm-sentry session: 4 failed bypass-retry cycles vs one ~20s real dispatch.

**How to apply:** First gate block on a small CR-followup diff → dispatch `adversarial-review --background` immediately. Don't try `touch skip_codex_gate` more than once. Only fall back to bypass writes when (a) the companion is genuinely unavailable, or (b) the diff is the same conceptual issue codex already reviewed in this session (per [[codex-round-cap-discipline]]).

Related: [[codex-round-cap-discipline]], [[codex-dispatch-before-commit]].
