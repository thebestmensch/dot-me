---
name: gh-pr-merge-delete-branch-worktree
description: "`gh pr merge --delete-branch` from a linked worktree fails when the primary checkout holds the default branch; merge succeeds but local branch-cleanup step errors. Workaround: omit `--delete-branch`, delete remote ref via REST API."
metadata:
  node_type: memory
  type: reference
  originSessionId: 09717e22-dea9-457b-a70a-3a826cac9113
---

`gh pr merge <N> --squash --delete-branch` invoked from inside a linked worktree (e.g. `.claude/worktrees/<slug>`) errors with `fatal: 'main' is already used by worktree at '<primary>'` when the primary checkout has the default branch checked out. The merge itself completes server-side (verifiable via `gh pr view <N> --json state` returning `MERGED`); the failure happens during gh's local branch-cleanup step.

**Workaround:** re-invoke `gh pr merge <N> --squash` without `--delete-branch` (idempotent: returns "already merged" on the second call), then delete the remote ref via the REST API:

```bash
gh api -X DELETE repos/<owner>/<repo>/git/refs/heads/<branch>
```

Validated 2026-05-19 on thebestmensch/dotfiles#38 merge from `.claude/worktrees/lift-jm-oom-commands`. The branch was deleted on the remote and the merge landed cleanly; only gh's local cleanup step needed the API substitute. The local branch in the worktree can be cleaned up afterward via `git worktree remove` + `git branch -d` from the primary checkout root (see [[chezmoi-pr-workflow]] for the worktree convention this lives inside).

Don't try `gh pr merge --delete-branch` again after the API delete — gh will succeed at the merge step (already merged) but still fail at the local-branch step.
