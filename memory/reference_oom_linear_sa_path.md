---
name: oom-linear-sa-path
description: Path to fetch OneOnMe Linear API key from background CC session via macOS Keychain SA token
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0222f6f7-3400-480c-b0ec-f0e954e7a2e3
---

OneOnMe Linear API key is reachable from any non-interactive CC session on this Mac via the `oneonme-machine` 1Password service-account token stored in macOS Keychain. The active `OP_SERVICE_ACCOUNT_TOKEN` env var only grants `homelab` vault on the `oneonme` 1P account; the `machine` vault (where the Linear key lives) requires the separate `oneonme-machine` SA token.

Recipe:

```bash
TOK=$(security find-generic-password -s op-token-oneonme-machine -a "$USER" -w)
KEY=$(OP_SERVICE_ACCOUNT_TOKEN="$TOK" op read 'op://machine/machine_linear_oneonme/cli_api_key')
# now use $KEY as Linear `Authorization` header (no `Bearer` prefix)
```

Verified workspace via `viewer { organization { urlKey } }` → `oneonme`.

Same pattern works for OneOnMe Sentry token (`op://machine/machine_sentry/api_key`). The interactive shell wraps both as `op-linear-oom` and `op-sentry-oom` functions in `~/.zshrc` (lines 65, 70-73), but those are zsh functions not available from CC's bash tool — use the recipe above directly.

Don't confuse with `op://homelab/machine_linear/cli_api_key` — that's the JM personal workspace key (org `thebestmensch`), reachable via the default SA token.
