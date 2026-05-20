---
name: partial-state-grep-adjacent-branches
description: "Half-done directory layouts / config / restructures often look abandoned but are actually in-progress with adjacent un-merged branches encoding the destination state. Before declaring 'partial = abandoned,' grep un-merged branches in adjacent config repos for assumptions matching the partial state."
metadata:
  node_type: memory
  type: feedback
---

Half-done directory layouts, config rewrites, or restructures often look abandoned but are actually in-progress — with adjacent un-merged branches in sibling config repos already encoding the destination state. Before declaring "partial = abandoned," grep un-merged branches for assumptions that match the partial state.

**Why:** A restructure usually touches multiple repos in lockstep — main repo + chezmoi + memory + ticket tracking. If the chezmoi side gets pushed to a branch and not merged while the main-repo side waits, the working tree looks like a "stalled" partial migration when it's actually mid-flight on a sibling branch. Treating it as abandoned and re-doing it from scratch wastes the in-flight work, OR worse: re-does it slightly differently and creates merge conflicts with the un-merged work.

Validated 2026-05-19 (workspace-restructure session):
- `~/Documents/local/jm/` and `~/Documents/local/oneonme/` directories existed with partial content (scratch repos + some siblings but not the main repos `jm-home-lab`, `oneonme-platform`).
- Original framing: "partial state, maybe abandoned prior attempt with un-surfaced reasons."
- Devils-advocate ran `rg` against chezmoi un-merged worktrees and found `~/.local/share/chezmoi/.claude/worktrees/drop-oom-linear-groom/dot_config/starship.toml` AND the `dark-theme` worktree already mapped `Documents/local/oneonme` + `Documents/local/jm` as workspace labels. Main chezmoi branch (`master`) still referenced the OLD paths in `executable_dot_zshrc.tmpl`.
- Verdict: the partial state was the load-bearing in-progress restructure. Adjacent chezmoi work assumed the new layout; the main-repo moves just hadn't caught up yet. NOT abandoned.

**How to apply:**

- When inspecting a directory that looks half-migrated: list un-merged branches in adjacent config/memory/dotfiles repos with `git branch -a --no-merged` and `git worktree list`.
- For each un-merged branch, grep for the partial-state's path patterns. If any branch references the destination paths, the migration is mid-flight, not abandoned.
- For OneOnMe + JM workflow specifically, the adjacent config repo is `~/.local/share/chezmoi/` (executable_dot_zshrc.tmpl, starship.toml, slash commands). For memory, it's `~/.me/` (rocks files, memory entries). Grep both before assuming abandonment.
- If the partial state IS mid-flight: don't re-do it from scratch. Inventory the un-merged work, coordinate the merges + remaining steps as one plan.
- Related: [[feedback_worktree_aware_activity_scan]] (worktree enumeration catches activity invisible to single-canonical-path scans), [[feedback_jm_oom_parity_surfaces]] (parity drift across siblings).
