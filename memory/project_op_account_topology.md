---
name: op-account-topology
description: "1Password CLI + keychain account topology — `my` shorthand = JM personal (`james@jamesmensch.com`); `oneonme` shorthand = OneOnMe NEW (`james@oneonme.com`, uuid `5BQ6ZWDMKVC4VKSRYIVGSBJ5UU`). Deprecated OneOnMe org (`Q7VTNZCOC5A7NJKX6WERMHAKBM`) forgotten 2026-05-19. Keychain SA token items: `op-token-personal` → JM (vault: `homelab`); `op-token-oneonme-machine` → OneOnMe NEW (vaults: `dev`, `machine`); `op-token-oneonme-machine-host` → OneOnMe NEW (vault: `machine-host`, host-only admin PATs)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 979330cc-7027-4b10-8abc-178121956d57
---

`op account list` topology after the 2026-05-19 cleanup:

| Shorthand | UUID (user) | Email | Account name |
|---|---|---|---|
| `my` | `GZQJMQIB5NF63ARX5AYI77V224` | james@jamesmensch.com | The Spensch's (JM personal) |
| `oneonme` | `5BQ6ZWDMKVC4VKSRYIVGSBJ5UU` | james@oneonme.com | OneOnMe NEW |

The DEPRECATED OneOnMe org (user uuid `Q7VTNZCOC5A7NJKX6WERMHAKBM`, same email `james@oneonme.com`) was forgotten via `op account forget` on 2026-05-19. Two `james@oneonme.com` accounts coexisted because email reuse across orgs is allowed; the deprecated one was the original, NEW is canonical. Do not re-add the deprecated UUID.

## Keychain service-account tokens

- `op-token-personal` — JM SA. Vault grants: `homelab` (uuid `25bndylky2hajvvlnysbush5ky`). Headless reads for JM/home-lab infra.
- `op-token-oneonme-machine` — OneOnMe NEW SA. Vault grants: `dev` (`ck23jbvlflzvs4rnpkamvyxm3u`), `machine` (`w4jvhkibxgkwtiqzwxo7rhs64m`). Headless reads for OOM infra readable BOTH on host AND inside the linear-agent container. `machine` is where the runtime Linear PAT and other container-readable creds live.
- `op-token-oneonme-machine-host` — OneOnMe NEW SA, host-only. Vault grant: `machine-host` (`d65j7p23zh25mjq42lbqfq3yiq`) ONLY. Trust boundary: this vault holds the OneOnMe Linear ADMIN PAT (full scope) and any future host-only admin creds. The container's SA (`oneonme-machine`) is INTENTIONALLY NOT granted READ on `machine-host` — so a compromised linear-agent container running Claude with `bypassPermissions` cannot `op read` admin PATs. Established via OOM-117 (2026-05-20). See [[feedback_credential_trust_boundary_is_vault_plus_envvar]] — the vault-grant split IS the boundary; field-level splits in the same vault are theater.
- A separate (in-vault) SA token lives at `op://machine/machine_linear_agent_mcp/credential` — that's the linear-agent container's SA, bootstrapped via `op inject` from a Mac with the `oneonme` shorthand registered. Not stored locally in Keychain — pulled from 1P at .env-build time.

## OneOnMe NEW vault structure

```
lsyszglamhgnxwnr3a4gy73n3a    Private
ck23jbvlflzvs4rnpkamvyxm3u    dev
w4jvhkibxgkwtiqzwxo7rhs64m    machine
d65j7p23zh25mjq42lbqfq3yiq    machine-host
kpvljljtzp4go6bfr7qn7qrwsri   Shared
```

**No `oneonme`-named vault in NEW.** The deprecated org had a vault literally named `oneonme`; NEW reorganized into the above. All `op://oneonme/...` refs in repos must rewrite to `op://machine/...` (or whichever NEW vault holds the item).

**`machine-host` was added 2026-05-20 via OOM-117.** Pre-OOM-117 there was an `admin` vault (uuid `64j6j5irk3ifgmfnx4yifpnydy`) created by PR #124; OOM-117 renamed `admin` → `machine-host` to make the trust boundary self-documenting ("admin" was too generic across team contexts). If the `admin` uuid still appears in `op vault list`, the rename may not have been applied in 1P web UI — verify.

**Item naming convention (post-OOM-117):** `<vault>_<org>_<service>[_<scope>]`. Concrete items: `machine_oneonme_linear` in `machine` vault (fields `credential` = container SA token, `runtime_api_key` = limited-scope runtime PAT); `machine_oneonme_linear_admin` in `machine-host` vault (field `cli_api_key` = full-scope admin PAT).

## How to apply

- New machine/agent credentials → `op://machine/<item>/<field>` in NEW.
- JM home-lab creds → `op://homelab/<item>/<field>` in JM personal.
- `op-personal` wrapper (in `~/.zshrc`) ensures bare-`op` calls use JM SA; `op-oneonme` wrapper ensures OOM SA. Never run bare `op` if the workspace differs from the ambient `OP_SERVICE_ACCOUNT_TOKEN` — it'll silently hit the wrong account (see [[reference_op_cli_quirks]] for the SA-token-overrides-`--account` gotcha).
- When adding a new OOM credential consumer: verify the item lives in `machine` vault (or grant the SA token access to a different vault) before referencing it.
- This memory is distinct from [[project_oom_account_naming]] which covers Anthropic Max billing accounts (`personal`/`oom` labels), NOT 1Password accounts.
