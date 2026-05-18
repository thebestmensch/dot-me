---
name: worktree-aware-activity-scan
description: Scripts scanning git activity across N repos must enumerate worktrees per repo via `git worktree list --porcelain` and dedupe commits by hash; a single canonical path per repo misses feature-branch commits in linked worktrees
metadata:
  node_type: memory
  type: feedback
---

When writing a tool that scans git activity (`git log`, `git diff`, commit walks) across multiple repos, do NOT hardcode a single canonical path per repo. JM's workflow keeps feature work in linked worktrees (`~/.claude/worktrees/*`, `~/.local/share/chezmoi-*`, `~/.me/.claude/worktrees/*`, etc.), and `git -C <main-worktree> log` only sees commits reachable from that worktree's HEAD — feature-branch commits on linked worktrees are invisible. Enumerate all worktrees per repo via `git worktree list --porcelain`, iterate `git log` in each, and dedupe by commit hash across the union.

**Why:** Validated 2026-05-18 on `rocks-eval.sh` Codex adversarial-review (cross-provider, job `review-mpbezu8z-s622ib`). The eval lib's whole purpose is to surface activity for rock-status judgment in the parallel-worktree workflow. Original implementation hardcoded canonical paths (`~/Documents/local/jm-home-lab`, `~/.local/share/chezmoi`, `~/.me`, etc.) — commits made on `feat/rocks-system` in `~/.local/share/chezmoi-rocks/` and on `worktree-precompact-memory` in `~/.me/.claude/worktrees/precompact-memory/` were entirely invisible. A session could ship its rock's work and `/jm-rocks` would still report it as `untouched`. Codex graded MEDIUM (0.9 confidence): "exactly the parallel-worktree workflow this feature targets." Smoke test post-fix surfaced previously-invisible commits from `precompact-memory` and `oom-71-persona-phase-0` worktrees.

The fix pattern (bash 3 compatible, runs on macOS):

```bash
SEEN_FILE=$(mktemp -t scan-seen.XXXXXX)
trap 'rm -f "$SEEN_FILE"' EXIT

for repo in "${REPOS[@]}"; do
  [[ -e "$repo/.git" ]] || continue   # .git can be file (linked) or dir (main)
  worktrees=$(git -C "$repo" worktree list --porcelain 2>/dev/null \
    | awk '/^worktree / {print $2}')
  [[ -z "$worktrees" ]] && worktrees="$repo"

  while IFS= read -r wt; do
    [[ -z "$wt" || ! -d "$wt" ]] && continue
    while IFS= read -r entry; do
      hash="${entry%% *}"
      grep -qxF "$hash" "$SEEN_FILE" 2>/dev/null && continue
      echo "$hash" >> "$SEEN_FILE"
      # ... use $entry ...
    done < <(git -C "$wt" log --since=... --pretty=format:'%h %s' 2>/dev/null)
  done <<< "$worktrees"
done
```

**How to apply:**
- Writing a tool that loops over canonical repo paths and runs `git log`/`git diff`/`git rev-list` in each → enumerate worktrees first, scan each, dedupe
- Reference impl: `~/.claude/lib/rocks-eval.sh` (post-fix), "Git activity" section
- Test: does the tool see commits on a feature branch whose worktree lives outside the canonical repo path? If no, it has this bug
- `.git` membership: use `[[ -e "$repo/.git" ]]` not `[[ -d ... ]]` — linked worktrees have `.git` as a file, not a directory
- Don't reach for bash 4 associative arrays for dedupe — macOS default bash is 3. Tempfile + `grep -qxF` against an accumulating seen-file works portably

Related: [[feedback_parallel_cc_single_writer]] (same workflow assumption), [[feedback_jm_oom_parity_surfaces]] (similar "scan across N similar things" failure mode)
