---
name: wrap-default-execute-mechanical
description: "/jm-wrap should execute mechanical cross-repo deferreds inline when user is live + parallel-CC contention is absent, not surface as Blocking + dump shell one-liners."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 09717e22-dea9-457b-a70a-3a826cac9113
---

When `/jm-wrap` encounters deferreds that are (a) mechanical — file deletions, well-understood git ops, no design decisions; (b) cross-repo but obviously scoped; and (c) the user is live in the session with no other CC sessions running — **execute inline**. Don't dump shell one-liners under the Blocking section and call it "user action required."

**Why:** Validated 2026-05-19 (this session) wrap on the PR #38 lift. 6 file deletions sat uncommitted in jm-home-lab + oneonme-platform `main`/`staging` working trees — shadowed-by-chezmoi files that were the direct continuation of the merged PR's work. First wrap pass classified them as non-trivial "needs PR review = ticket it" and surfaced as ❌ Blocking with one-liner commands for the user to run after `/clear`. User redirected: "go ahead and handle whatevers lying around. we have no other sessions working right now." Correct path was execute inline — the deletions were obvious, the chezmoi globals were already verified present, the work was the natural finish to the session's merged PR.

**How to apply:**
- Wrap's "Trivial — execute now" criteria (safe / reversible / in scope / no user decision) take precedence over heuristic shortcuts like "cross-repo = ticket" or "needs CR review = ticket." Mechanical follow-ups to this session's own merged PR are exactly the case the inline path exists for.
- Treat "cross-repo" as a friction multiplier, not a triviality blocker. If the work needs 2 worktrees + 2 PRs but each PR is a single mechanical commit, that's still trivial — just two-step trivial.
- Treat "needs CR review" similarly. Every PR needs CR review; that's not what makes work non-trivial. What makes it non-trivial is whether the work itself involves judgment beyond the wrap session's existing context.
- Reserve Blocking + dump-commands posture for: (a) work that needs user input the wrap doesn't have, (b) work the user might not want done at all, (c) work that's irreversible enough that auto-execution is risky.
- Parallel-CC check: confirm no other sessions before executing cross-repo work. The [[feedback_parallel_cc_single_writer]] rule still holds; just ask once at the wrap step or check the session list.
