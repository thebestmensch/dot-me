---
name: rg-aliased-in-cc-shell
description: "Inside Claude Code Bash-tool sessions, `rg` is a shell function (not the ripgrep binary) defined by ~/.claude/shell-snapshots/snapshot-zsh-*.sh. It re-execs the user-active claude binary, so `rg --no-config 'pat' .` errors with `grep: unrecognized option '--no-config'`. Use plain `grep -r --exclude-dir=...` or `command rg` to bypass."
metadata:
  node_type: memory
  type: reference
---

When `rg --some-flag` errors with `grep: unrecognized option`, you're hitting the CC shell snapshot's `rg` function, not the ripgrep binary. The function re-execs `$CLAUDE_CODE_EXECPATH` (or `/Users/jm/.local/bin/claude`), which routes to a grep-shaped fallback when no ripgrep is available in the resolved env.

```
$ type rg
rg () { local _cc_bin="${CLAUDE_CODE_EXECPATH:-}"; ... }
```

The brew formula for ripgrep is installed at `/opt/homebrew/opt/ripgrep` but the binary at `/opt/homebrew/opt/ripgrep/bin/rg` doesn't exist (formula installed, binary missing — possibly relocated, possibly a half-broken install).

## How to apply

- `grep -r 'pat' . --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=.venv` is the cleanest portable bypass. Cap scope with subdirs (`for d in services/ admin/; do grep -r ... "$d"; done`) on big monorepos so it returns in seconds.
- `command rg ...` does NOT bypass — the shell function is `function rg () { ... }`, so `command` skips builtins but not functions. `\rg ...` (backslash quote) skips aliases but not functions either. Use `unset -f rg` first, or just use grep.
- For symbol-level lookups across the repo, spawning the Explore agent (or general-purpose with caveman:cavecrew-investigator) is usually faster than grep-in-Bash anyway. Use grep-in-Bash for "I know what file I'm looking for and need to confirm lines."

## Related

- [[reference_rtk_caches_stat_output]] — sibling case of CC shell environment masking standard CLI behavior; check `type <cmd>` when output seems wrong.
