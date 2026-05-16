---
name: gh-search-user-flags
description: "gh search issues/prs doesn't honor `involves:@me` / `author:@me` query tokens; must use explicit --involves / --author / --review-requested flags with username"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6665ff01-ca39-43cc-b250-262f23cd1453
---

`gh search issues "is:open involves:@me"` returns `[]` silently — the `@me` alias works on github.com web UI and REST API, but `gh search` CLI parses these as literal query terms and returns no matches. Empty result with no warning.

Working form: pass username explicitly via dedicated flags.

```bash
gh search issues --involves thebestmensch --state open --limit 100
gh search prs --review-requested thebestmensch --state open --limit 50
gh search prs --author thebestmensch --state open --limit 50
gh search issues --mentions thebestmensch --state open --limit 50
```

The notifications API (`gh api notifications`) is unrelated — it ignores user filters entirely and just returns the authenticated user's unread thread subscriptions.

**How to apply:** when wiring any GitHub-wide "what needs my attention" automation (skills, scripts, n8n nodes), use the dedicated flags and pass the username string. Don't bring `@me` syntax over from REST/web-UI usage. Validated 2026-05-16 building `/jm-oss-inbox`: in-query `involves:@me` returned `[]`, `--involves thebestmensch` returned 100+ results from same auth context.
