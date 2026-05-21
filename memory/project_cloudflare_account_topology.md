---
name: cloudflare-account-topology
description: Two Cloudflare accounts (personal + work) — personal `d1deb1b79d3e9047ff9a132a22c84ae6` is free plan, hosts personal-site DNS only (jamesmensch.com, thespenschs.com); work `608361cd8e347f99d5a46b1d52c89bce` is paid plan, hosts oneonme.com + the entire OOM MCP Worker fleet (oom-mcp, oom-design-mcp, oom-scrape-mcp) with Browser Rendering.
metadata:
  type: project
---

JM has two Cloudflare accounts. Despite both being James@*.com accounts on the same dashboard login, they have different account_ids, different plans, different responsibilities, and different vendor isolation per [[workspace-topology]].

## Topology

| Account | account_id | Plan | Hosts | 1P item |
|---|---|---|---|---|
| **Personal** | `d1deb1b79d3e9047ff9a132a22c84ae6` | Free | DNS for `jamesmensch.com`, `thespenschs.com`; personal site Workers | `op://homelab/machine_cloudflare` (jm SA) |
| **Work (OOM)** | `608361cd8e347f99d5a46b1d52c89bce` | Paid | `oneonme.com` DNS + all OOM MCP Workers + Browser Rendering | `op://machine/machine_cloudflare` (oneonme SA) |

**Workers subdomain on work account:** `oneonme.workers.dev`. So OOM Workers land at `oom-mcp.oneonme.workers.dev`, `oom-scrape-mcp.oneonme.workers.dev`, etc.

## OOM Worker fleet (work CF account)

All three Workers share the same OAUTH_KV namespace `f7258e006af5453e952b3bec79609a27` and the same OOM-GCP OAuth client (`machine_oom_mcp_google_oauth`) — see [[oom-mcp-shared-auth-pattern]] (write when relevant). Sharing is safe because all enforce the same `@oneonme.com` domain allowlist; the shared KV gives SSO-style UX across the fleet.

| Worker | URL | Purpose |
|---|---|---|
| `oom-mcp` | `https://oom-mcp.oneonme.workers.dev` | Postgres read-only gate |
| `oom-design-mcp` | `https://oom-design-mcp.oneonme.workers.dev` | Design language brand kit |
| `oom-scrape-mcp` | `https://oom-scrape-mcp.oneonme.workers.dev` | Menu scraping via CF Browser Rendering (OOM-53) |

## How to apply

- **Deploying a new OOM Worker:** target work CF (`608361cd...`). Pull token via `op-oneonme` wrapper from 1P `machine_cloudflare`. Set `CLOUDFLARE_ACCOUNT_ID` explicitly per [[wrangler-account-id-caching]] when crossing accounts in the same session.
- **Deploying anything that uses Browser Rendering:** must be on work CF — personal CF caps Browser Rendering at 5 (free-plan quota).
- **DNS or personal-site Worker:** personal CF. Don't put OOM things there.
- **Cross-pollination IS expected for INFRA, not for CREDENTIALS.** The OOM-scrape Worker is callable from JM's personal home-lab CC sessions (it's just a URL), but the Worker itself runs on OOM CF, billed to OOM, auth'd via OOM GCP. The principle: credentials match the workspace the *service* belongs to, not where the *caller* runs.
- **CF API token scopes** on work account need (minimum): Workers Scripts:Edit, Workers KV Storage:Edit, Browser Rendering:Edit, Account Settings:Read. A token with only basic identity scope will pass `wrangler whoami` but fail every account-scoped operation — see [[wrangler-account-id-caching]] for the diagnostic.

**Validated 2026-05-21 on OOM-53 deploy:** initially deployed scrape-mcp pointing at personal-CF OAuth client (residual from oom-mcp scaffolding), then migrated to OOM-GCP `MCP Server` client when JM flagged the workspace-affinity mismatch. New 1P item `machine_oom_mcp_google_oauth` (work `machine` vault) is now canonical for the OOM Worker fleet's Google OAuth. Personal CF OAuth client + its 1P entry are pending deletion once the migration is verified end-to-end (oom-mcp + oom-design-mcp also need rotation to the work-OAuth client — see [[oom-mcp-oauth-migration-pending]] when filed).

Related: [[workspace-topology]], [[op-account-topology]], [[wrangler-account-id-caching]].
