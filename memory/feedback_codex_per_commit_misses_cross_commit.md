---
name: codex-per-commit-misses-cross-commit
description: Codex dispatches per-incremental-commit only review the delta of that commit; cross-commit interactions emerge only when dispatched against the full PR diff (vs base branch). Re-dispatch on full diff before declaring done.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f37b83a6-7000-4955-b332-20bb21c6dec2
---

When a PR lands as a sequence of commits (initial implementation + reviewer-fix follow-ups), each per-commit codex dispatch only reads `git diff` of the working tree at that moment. New issues introduced by the *interaction* between commits — a race the initial commit had AND that the reviewer-fix didn't address, or a side-effect (TipGuidanceSheet popping over a new branch) that the original implementation forgot to suppress — are invisible to any per-commit pass and emerge only when codex sees the full PR delta.

**Why:** Validated 2026-05-20 on OOM-120. Initial codex pass found 1 HIGH (cardLoadFailed branch erroneously included transient errors), I fixed it, committed, declared done. JM pushed back on the bypass; I dispatched codex with `--base HEAD~2 --scope branch` (= full PR diff vs the prior staging commit). That pass found 3 NEW findings the initial dispatch missed entirely: a cold-entry race (HIGH), TipGuidanceSheet popping over the terminal state (MED), and `router.back()` looping back into the stale redeem page (MED). None of those involved the cardLoadFailed code path — they were interactions between the new render branch and pre-existing side effects.

**How to apply:**
- For multi-commit PRs: after the final fix-up commit on the branch, dispatch codex one more time with `--base <merge-base> --scope branch` (or `--base origin/staging`) to catch cross-commit interactions before declaring the PR ready.
- The default `~/.claude/codex-dispatch.sh` wrapper resolves to working-tree diff, which is per-commit scope. For PR-level review, fall back to the raw companion: `node $HOME/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs adversarial-review --base origin/<base-branch> --scope branch`.
- "I already ran codex on the previous commit" is the Red Flag — that pass didn't see the surrounding context.
- Bypass discipline should defer to "did we run codex on the full PR diff" not "did we run codex on each edit." [[codex-per-diff-vs-per-commit]]

Related: see `~/.claude/rules/codex-dispatch.md` gap discussion; this is the inverse of "loop-drain" — single full-PR pass at the end is high-signal, mid-stream repeated per-edit passes are low-signal.
