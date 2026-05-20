---
name: op-cli-quirks
description: "1Password CLI gotchas — `OP_SERVICE_ACCOUNT_TOKEN` silently overrides `--account` (so code calling `op --account X` must `unset OP_SERVICE_ACCOUNT_TOKEN` first); `op signin` output must be `eval`-ed; `op account add` registers but doesn't create a session — `eval $(op signin --account X)` required. SA tokens are read-only on vault grants by default — write ops fail with generic 'Couldn't update the item.' Use interactive `eval $(op signin)` for one-off writes. `op inject` errors on bare `op://` in input files (including in comments)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 725539cb-afaf-43ef-ba16-733eef009fe9
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

## 4. SA tokens are read-only on vault grants by default

A 1P service-account token's vault grants confer **read** by default. `op item edit`, `op item create`, `op item delete` under an SA token fail with a generic and unhelpful error: `[ERROR] ... Couldn't update the item.` — no mention of permissions.

To grant write: 1P admin → Settings → Developer → Infrastructure Secrets Management → edit the SA → toggle write on the specific vault. (Cannot be done via CLI.)

**Workaround for one-off writes without granting permanent write:** drop to interactive user auth. `unset OP_SERVICE_ACCOUNT_TOKEN; eval $(op signin --account X); op item edit ...`. The user account writes; SA stays read-only.

**Live demo (2026-05-20):** `op item edit machine_linear_oneonme --vault machine --account oneonme "credential=$(...)"` with SA token in env → "Couldn't update the item." After `unset OP_SERVICE_ACCOUNT_TOKEN; eval $(op signin --account oneonme)` (Touch ID), same command succeeded.

## 5. Vault-level admin ops (rename, create) are SA-blocked

Service-account tokens have **vault-level read/write grants only** — vault-level admin ops (`op vault edit --name`, `op vault create`, `op vault delete`) require user-account auth with admin/owner privileges. SA returns `(403) Forbidden: You aren't authorized to access this resource.` Distinct from #4 (item-level write block) — even granting the SA write on the vault won't help; rename is a different permission class.

**Recovery:** user-shell session required. `OP_SERVICE_ACCOUNT_TOKEN= eval $(op signin --account my); op vault edit homelab --name machine` (Touch ID fires). Or do it in the 1P desktop app (right-click vault → Rename). Cannot be triggered from CC's Bash tool — Touch ID needs interactive TTY; `op signin` without TTY returns "operation not supported by device".

**Live verified 2026-05-20** on JM-287 during attempt to rename `homelab` → `machine`.

## 6. Post-rename multi-account `--vault` collision

After JM-287 (2026-05-20), the vault name `machine` exists in **both** `my` (JM personal, JM-287 cutover) **and** `oneonme` (OneOnMe NEW, OOM-117). Any `op item get`/`op read` call against `--vault machine` without `--account` pin resolves against whichever account's session/SA token the shell happens to have active — silently wrong, no warning.

**Defensive pattern:** always pin `--account` alongside `--vault machine`. The chezmoi `zshrc.tmpl` helpers already do this via the SA-token routing layer (`op-personal`/`op-oneonme`/`op-oneonme-host` wrappers). Setup scripts and preflight checks must also pin — Codex flagged this as P2 in chezmoi `bin/setup-linear-agent` during JM-287 review; fixed by adding `--account my` to the preflight `op item get machine_linear --vault machine`.

## 7. `op inject` errors on bare `op://` in input

`op inject` scans the input file for any occurrence of `op://...` and tries to resolve it — including inside comments. A bare literal `op://` (e.g. in documentation text describing the schema) trips it with:

```
[ERROR] invalid secret reference 'op://': too few '/': secret references should have at least vault, item and field specified
```

The whole `op inject` invocation fails before reaching the real refs. Common in `.env.template` files that have an inline comment like `# inject silently writes literal \`op://\` strings into .env`.

**Fix:** rewrite the comment to avoid the bare token. "literal references", "unresolved references", "the \`op:\` scheme" all work. Don't try to escape — `op inject` ignores common escape conventions (it doesn't parse shell or markdown syntax, just regex-scans for `op://`).

**Live verified 2026-05-20** on `services/linear-agent/.env.template` in oneonme-platform.

## How to apply

- Before debugging "why is `op --account X` returning the wrong account's data," check `env | grep OP_SERVICE_ACCOUNT_TOKEN`.
- Before adding new code paths that mix SA-token and `--account`-mode auth in the same shell session, plan the unset boundary.
- After `op account add ...`, follow immediately with `eval $(op signin --account ...)` or the next probe will look broken.
- For write operations on a vault where you only have an SA: use interactive signin, don't try to grant write to the SA just for a one-off (or do, then revoke).
- For `.env.template` files driving `op inject`: lint inputs for bare `op://` substrings — failing fast at template-author time beats failing late during deploy.
- For vault-level admin ops (rename/create/delete): never attempt from CC — Touch ID needs interactive TTY; surface the `op vault edit ...` command for JM to run in his shell, or do via the 1P desktop app.
- For any new code/script touching `--vault machine`: always pin `--account my` or `--account oneonme` — the name collision is silent.
- Related: [[project_op_account_topology]] for which accounts/UUIDs exist.
