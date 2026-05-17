---
name: claude-plugin-update-noop-on-version-match
description: "`claude plugin update <name>` returns 'already at latest' when plugin.json version matches, even if marketplace HEAD commit drifted. Force refresh via uninstall + reinstall."
metadata: 
  node_type: memory
  type: reference
  originSessionId: b024ada5-627d-43fc-975e-be8ae3dc48cf
---

`claude plugin update <name>@<marketplace>` compares `plugin.json` version strings, not git commits. Plugins that keep a static version (e.g. `claude-hud` at `0.1.0`) while shipping fix commits will report "already at the latest version" and no-op, leaving the installed copy stale.

**Recovery:**
```
claude plugin uninstall <name>@<marketplace>
claude plugin install <name>@<marketplace>
```
Reinstall pulls fresh from the marketplace's current HEAD and records the new sha in `~/.claude/plugins/installed_plugins.json`.

**How to detect:** compare `gitCommitSha` in `installed_plugins.json` against the marketplace's `git rev-parse HEAD` (for git-source marketplaces) or the source repo's HEAD (for plugins whose marketplace just routes — e.g. claude-hud's marketplace entry has `source: "./"` and the source IS the marketplace repo). Don't trust the version field alone.

**Validated 2026-05-17:** claude-hud installed sha was `bfde7cf` (2026-04-07); marketplace HEAD was `6f7d073` (10 commits later, all version 0.1.0). `claude plugin update claude-hud@claude-hud` returned "already at the latest version (0.1.0)". `uninstall` + `install` bumped sha to `6f7d073`.

Pairs with `/jm-plugin-audit` §4 (Updates Available) — the audit surfaces the drift; this memory documents the workaround. See [[chezmoi-pr-workflow]] for the PR that added §4 to the skill.
