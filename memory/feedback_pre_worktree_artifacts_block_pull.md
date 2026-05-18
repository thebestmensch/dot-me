---
name: pre-worktree-artifacts-block-pull
description: Files written to the shared-checkout path before EnterWorktree fires can survive as untracked duplicates and block `git pull` post-merge with "would be overwritten by merge"; rm-if-identical is the fix
metadata:
  node_type: memory
  type: feedback
---

When a CC session writes a new file at the shared-checkout path *before* `EnterWorktree` is called (because the bg-isolation guard hadn't fired yet, or the session started outside a worktree), the file stays as an untracked artifact in the main working tree. The worktree picks up a fresh copy, the worktree's PR merges normally, and *then* `git pull` in the main worktree aborts with "The following untracked working tree files would be overwritten by merge / Please move or remove them before you merge." The artifacts are identical to what the merge wants to add; the local copies just predate the merge commit.

Diagnostic + fix:
1. `git status --short` to find the untracked paths git is complaining about
2. For each one: `diff <main-path> <worktree-path-or-merge-commit-content>` — if identical, `rm` is safe (the merge will recreate the file with identical content)
3. If NOT identical, surface to user — never silently discard
4. After the rm, `git pull --ff-only` proceeds cleanly

**Why:** Validated 2026-05-18 on the rocks-system session. `/jm-precompact` created `~/.me/rocks/SPEC.md` at the shared-checkout path before the bg-isolation guard tripped on the second Write. EnterWorktree then created `~/.me/.claude/worktrees/precompact-memory/`, into which the spec was duplicated. The worktree's PR (thebestmensch/dot-me#30) merged. Post-merge `git -C ~/.me pull --ff-only` aborted with the "would be overwritten" error. The original shared-checkout `rocks/SPEC.md` was the blocker, identical in content to what the merge brought in. `rm` + retry resolved it cleanly.

**How to apply:**
- Add to `/jm-wrap` § 4 (Repo clean-state check) mental model: after merging a PR for a worktree branch, the main worktree's pull will block on untracked files at any path the PR introduced if the same path was scratch-written at the shared checkout earlier
- Detection: `git status --short` shows `??` lines for paths that match (or contain) files introduced by the just-merged PR
- Fix is rm-if-identical (verify via diff), not stash or commit
- Prevention: when a session starts outside a worktree and writes files that will eventually live at a tracked path, either commit them immediately at the shared checkout OR clean them up before EnterWorktree creates the duplicate
- This is a sibling failure mode to codex-dispatch gap #3 ("edits in sibling repo return no diff") — both stem from "the path you edited isn't the path the merge sees"

Related: [[feedback_parallel_cc_single_writer]] (also a "where does this artifact actually live" pitfall)
