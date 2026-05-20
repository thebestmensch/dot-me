---
name: op-account-topology
description: "1Password CLI + keychain account topology — `my` shorthand = JM personal (`james@jamesmensch.com`); `oneonme` shorthand = OneOnMe NEW (`james@oneonme.com`, uuid `5BQ6ZWDMKVC4VKSRYIVGSBJ5UU`). Deprecated OneOnMe org (`Q7VTNZCOC5A7NJKX6WERMHAKBM`) forgotten 2026-05-19. Keychain SA token items: `op-token-personal` → JM (vault: `homelab`); `op-token-oneonme-machine` → OneOnMe NEW (vaults: `dev`, `machine`)."
metadata:
  node_type: memory
  type: project
---

`op account list` topology after the 2026-05-19 cleanup:

| Shorthand | UUID (user) | Email | Account name |
|---|---|---|---|
| `my` | `GZQJMQIB5NF63ARX5AYI77V224` | james@jamesmensch.com | The Spensch's (JM personal) |
| `oneonme` | `5BQ6ZWDMKVC4VKSRYIVGSBJ5UU` | james@oneonme.com | OneOnMe NEW |

The DEPRECATED OneOnMe org (user uuid `Q7VTNZCOC5A7NJKX6WERMHAKBM`, same email `james@oneonme.com`) was forgotten via `op account forget` on 2026-05-19. Two `james@oneonme.com` accounts coexisted because email reuse across orgs is allowed; the deprecated one was the original, NEW is canonical. Do not re-add the deprecated UUID.

## Keychain service-account tokens

- `op-token-personal` — JM SA. Vault grants: `homelab` (uuid `25bndylky2hajvvlnysbush5ky`). Headless reads for JM/home-lab infra.
- `op-token-oneonme-machine` — OneOnMe NEW SA. Vault grants: `dev` (`ck23jbvlflzvs4rnpkamvyxm3u`), `machine` (`w4jvhkibxgkwtiqzwxo7rhs64m`). Headless reads for OOM infra. The `machine` vault is the SA-target vault; new OOM machine/agent creds go here.
- A separate (in-vault) SA token lives at `op://machine/machine_linear_agent_mcp/credential` — that's the linear-agent container's SA, bootstrapped via `op inject` from a Mac with the `oneonme` shorthand registered. Not stored locally in Keychain — pulled from 1P at .env-build time.

## OneOnMe NEW vault structure

```
lsyszglamhgnxwnr3a4gy73n3a    Private
64j6j5irk3ifgmfnx4yifpnydy    admin
ck23jbvlflzvs4rnpkamvyxm3u    dev
w4jvhkibxgkwtiqzwxo7rhs64m    machine
kpvljljtzp4go6bfr7qn7qrwsri   Shared
```

**No `oneonme`-named vault in NEW.** The deprecated org had a vault literally named `oneonme`; NEW reorganized into the five above. All `op://oneonme/...` refs in repos must rewrite to `op://machine/...` (or whichever NEW vault holds the item).

## How to apply

- New machine/agent credentials → `op://machine/<item>/<field>` in NEW.
- JM home-lab creds → `op://homelab/<item>/<field>` in JM personal.
- `op-personal` wrapper (in `~/.zshrc`) ensures bare-`op` calls use JM SA; `op-oneonme` wrapper ensures OOM SA. Never run bare `op` if the workspace differs from the ambient `OP_SERVICE_ACCOUNT_TOKEN` — it'll silently hit the wrong account (see [[reference_op_cli_quirks]] for the SA-token-overrides-`--account` gotcha).
- When adding a new OOM credential consumer: verify the item lives in `machine` vault (or grant the SA token access to a different vault) before referencing it.
- This memory is distinct from [[project_oom_account_naming]] which covers Anthropic Max billing accounts (`personal`/`oom` labels), NOT 1Password accounts.
