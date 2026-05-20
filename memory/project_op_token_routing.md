---
name: op-token-routing
description: "Workspace-aware OP_SERVICE_ACCOUNT_TOKEN routing via zsh chpwd hook. Path prefix selects JM personal vs OneOnMe NEW SA token. Fail-closed on lookup miss. Scripts crossing vaults must use op-personal / op-oneonme wrappers explicitly, not rely on ambient token."
metadata: 
  node_type: memory
  type: project
  originSessionId: 725539cb-afaf-43ef-ba16-733eef009fe9
---

`~/.zshrc` (chezmoi-managed `executable_dot_zshrc.tmpl`) installs a chpwd hook that sets `OP_SERVICE_ACCOUNT_TOKEN` based on `$PWD` path prefix:

| Path prefix | Token routed |
|---|---|
| `~/Documents/local/jm/*` | `op-token-personal` (JM SA, vault: `homelab`) |
| `~/Documents/local/oneonme/*` | `op-token-oneonme-machine` (OOM NEW SA, vaults: `dev`, `machine`) |
| (interim) `~/Documents/local/oneonme-platform/*`, `~/Documents/local/oneonme-claude-plugins/*` | same as oneonme |
| anywhere else | `op-token-personal` (default) |

**Fail-closed semantics** (Codex I3): on keychain lookup miss for the selected workspace's SA, `unset OP_SERVICE_ACCOUNT_TOKEN` rather than silently preserve prior workspace's token. Prior workspace token leaking forward is exactly the pollution class the routing fixes; hidden behind a hook would be worse than the original bug.

## Why

Before the hook: `~/.zshrc` unconditionally exported JM SA at every shell start. Any `op read` inside an OOM workspace dir silently hit JM's `homelab` vault. Bug surfaced 2026-05-19 when `op vault list --account oneonme` returned JM's vault — `OP_SERVICE_ACCOUNT_TOKEN` takes priority over `--account` (see [[reference_op_cli_quirks]]).

After the hook: shells started in workspace-A then `cd`-d to workspace-B re-route to B's SA. Interactive `op read` from inside the correct workspace dir hits the correct vault.

## How to apply

- **chpwd hook is defense-in-depth for interactive shells.** MCP processes (Stripe, Mixpanel via `.mcp.json`), Linear-agent containers running `claude -p`, and `~/.claude/hooks/` scripts all inherit env at *spawn time*, not on each `cd`. Long-lived processes don't pick up workspace-aware routing.
- **Scripts that need a specific account must use explicit wrappers.** Either `op-personal …` / `op-oneonme …` (both defined in `~/.zshrc`) or set `OP_SERVICE_ACCOUNT_TOKEN` inline. Never rely on ambient routing inside a script — calling-shell state isn't a stable contract.
- **Cross-vault reads inside an OOM workspace dir use the homelab vault explicitly.** `admin/agents/menu-discovery/.env.template` references `op://homelab/*/...` from inside oneonme-platform. After routing flips, run `op-personal op inject -i .env.template -o .env` instead of bare `op inject` (which would resolve as the OOM SA and fail with "no vault access"). Same pattern for any future cross-workspace consumer.
- **`mobile-app/scripts/sentryToken.ts:47-72`** is the canonical defensive pattern: it `delete env.OP_SERVICE_ACCOUNT_TOKEN` then calls `op read --account "$OP_ACCOUNT"` to force the desktop-app integration path. Worth re-reading before designing any new credential consumer in OOM workspace.

## Related memory

- [[project_op_account_topology]] — UUIDs, keychain item names, vault grants per SA
- [[reference_op_cli_quirks]] — `OP_SERVICE_ACCOUNT_TOKEN` overrides `--account`, signin requires `eval $(...)`
- [[feedback_live_probe_external_creds]] — verify credential systems live before fix-design
