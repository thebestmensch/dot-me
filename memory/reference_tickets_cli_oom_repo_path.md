---
name: tickets-cli-oom-repo-path
description: "The `tickets` CLI defaults OOM `_OOM_REPO_PATH` to `/Users/jm/Documents/local/oneonme`, but the actual repo lives at `oneonme-platform`. Set `ONEONME_REPO_PATH` env var when invoking `tickets work OOM-N` or any OOM-prefixed subcommand from outside the repo, or the CLI errors with \"Configured repo path for OOM ... is not a git repo.\""
metadata: 
  node_type: memory
  type: reference
  originSessionId: c814f6bd-79ec-4db9-b122-ced8b06f5ea7
---

The `tickets` CLI (`/Users/jm/Documents/local/jm-home-lab/services/tickets/tickets/config.py`) declares:

```python
_OOM_REPO_PATH = Path(os.environ.get("ONEONME_REPO_PATH", "/Users/jm/Documents/local/oneonme"))
```

The default points at the legacy repo location. The current repo lives at `/Users/jm/Documents/local/oneonme-platform`. Without the override the CLI bails immediately:

```
Error: Configured repo path for OOM (/Users/jm/Documents/local/oneonme) is not a git repo. Check tickets/config.py.
```

**Workarounds (in order of preference):**

1. Set `ONEONME_REPO_PATH` in the invocation:
   ```bash
   zsh -ic 'export ONEONME_REPO_PATH=/Users/jm/Documents/local/oneonme-platform && op-linear-oom && tickets work OOM-N --yes --bg'
   ```
2. Export it in `~/.zshrc` (or chezmoi-managed equivalent) once and forget — the cleaner long-term fix.
3. Patch the default in `config.py` to `oneonme-platform` and PR it back into jm-home-lab.

**Related:** the `op-linear-oom` zsh function must load before `tickets` (loads `LINEAR_API_KEY_OOM` from 1Password); chpwd-based routing won't fire when CC's Bash tool spawns a fresh shell, so always `zsh -ic 'op-linear-oom && tickets ...'`.

Validated 2026-05-20 launching OOM-115 agent run.
