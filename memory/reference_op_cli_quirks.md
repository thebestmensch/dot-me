---
name: op-cli-quirks
description: "1Password CLI gotchas — `OP_SERVICE_ACCOUNT_TOKEN` silently overrides `--account` (so code calling `op --account X` must `unset OP_SERVICE_ACCOUNT_TOKEN` first); `op signin` output must be `eval`-ed; `op account add` registers but doesn't create a session — `op signin --account X` then `eval $(op signin --account X)` required."
metadata:
  node_type: memory
  type: reference
---

Three behaviors of the `op` CLI that bite if not known. All verified live on 1P CLI v3.14.3 (2026-05-19).

## 1. `OP_SERVICE_ACCOUNT_TOKEN` silently overrides `--account`

When `OP_SERVICE_ACCOUNT_TOKEN` is set in the env AND `--account <shorthand>` is passed on the command line, the SA token wins and `--account` is **silently dropped** (no error, no warning). Subsequent `op read`/`op vault list`/`op item get` operations hit the SA token's account+scope, NOT the `--account` shorthand.

**Live demo (2026-05-19):** ran `op vault list --account oneonme` with JM SA token in env from `~/.zshrc`. Returned JM's `homelab` vault — `--account oneonme` was ignored.

**Defensive pattern:** code that calls `op --account X` MUST `unset OP_SERVICE_ACCOUNT_TOKEN` first. The canonical example lives at `mobile-app/scripts/sentryToken.ts:64`:

```ts
// The 1Password CLI treats OP_SERVICE_ACCOUNT_TOKEN as higher priority
// than --account, so a service-account token in the parent shell would
// hijack the lookup into SA mode and ignore OP_ACCOUNT entirely.
const opEnv = { ...env } as NodeJS.ProcessEnv;
delete opEnv.OP_SERVICE_ACCOUNT_TOKEN;
```

For one-shot shell commands: `OP_SERVICE_ACCOUNT_TOKEN= op --account oneonme ...` (leading prefix unsets just for this command).

## 2. `op signin` output must be `eval`-ed

Running `op signin --account X` directly prints shell-export commands to stdout — calling it without `eval` produces:

```
[ERROR] Output of 'op signin' is meant to be executed by your terminal.
Please run 'eval $(op signin)'.
You can use the '-f' flag to override this warning.
```

**Correct:** `eval $(op signin --account oneonme)` — populates `OP_SESSION_<account>` in current shell. Biometric prompt fires via desktop integration.

## 3. `op account add` ≠ session

Adding an account with `op account add` writes the shorthand+URL+account-key to `~/.config/op/config` but does NOT create a session token. Subsequent `op --account <new-shorthand>` calls fail with `could not find session token for account <shorthand>` until `eval $(op signin --account <new-shorthand>)` runs.

## How to apply

- Before debugging "why is `op --account X` returning the wrong account's data," check `env | grep OP_SERVICE_ACCOUNT_TOKEN`.
- Before adding new code paths that mix SA-token and `--account`-mode auth in the same shell session, plan the unset boundary.
- After `op account add ...`, follow immediately with `eval $(op signin --account ...)` or the next probe will look broken.
- Related: [[project_op_account_topology]] for which accounts/UUIDs exist.
