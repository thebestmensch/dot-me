---
name: codex-companion-per-cwd-state
description: codex-companion.mjs's job state is keyed per-cwd-repo. `status` and `result` invoked from outside the dispatching cwd show "No jobs recorded yet" even when jobs are actively running. Always cd into the dispatching repo/worktree before any companion subcommand.
metadata:
  type: reference
---

The Codex companion CLI (`node $HOME/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs`) stores its job-tracker state per-cwd-resolved git-repo. Specifically, state lives under `$HOME/.claude/plugins/data/codex-openai-codex/state/<repo-slug>/` where `<repo-slug>` is derived from the cwd's git common-dir.

**Symptom of cwd mismatch:**

- You dispatch a Codex review from inside `/path/to/repo/.claude/worktrees/foo/` via `~/.claude/codex-dispatch.sh`.
- Dispatch script's pre-flight log writes (you see "Starting adversarial-review (background)..." in the bg-job output).
- Later, you run `node …/codex-companion.mjs status` from a different cwd (the main repo, a sibling worktree, or `~/.me/.claude/worktrees/precompact-memory`).
- Status reports "No jobs recorded yet." **The jobs are real and running — the wrong cwd is reading the wrong state directory.**

This wastes investigation cycles: empty `status` looks identical to "dispatch failed and exited silently", so you start debugging the dispatch script when nothing is wrong.

**How to apply:**

1. ALWAYS `cd` into the exact cwd where the dispatch happened before running `status`, `result`, or `cancel`. The worktree path matters — `cd`ing to the main repo when the dispatch ran in a linked worktree shows empty state.
2. If you're not sure which cwd dispatched, list `$HOME/.claude/plugins/data/codex-openai-codex/state/` — each subdirectory is one repo-slug with its own `jobs/` directory. Recent subdirs reveal where dispatches actually ran.
3. The dispatch script (`codex-dispatch.sh`) does inherit cwd properly when called normally. The trap is the *follow-up* `status` / `result` invocation getting run from a different shell or after the cwd changed.
4. CC's `Bash` tool resets cwd after every command (`Shell cwd was reset to <home-of-job>`), so chaining `cd repo && node companion status` in a single Bash call is correct; running `cd repo` alone and then a separate `node companion status` will read the wrong state.

**Validated 2026-05-21 on OOM-53 scrape-mcp scaffold:** dispatched adversarial-review from `/Users/jm/Documents/local/oneonme-platform/.claude/worktrees/scrape-mcp`, then checked status from cwd `/Users/jm/.me/.claude/worktrees/precompact-memory` → "No jobs recorded yet" while 4 jobs were running. Re-running with `cd <worktree>` in the same Bash call surfaced all 4 jobs immediately.

Related: [[claude-plugin-update-noop]], [[gh-pr-merge-delete-branch-worktree]].
