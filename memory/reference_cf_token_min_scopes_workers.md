---
name: cf-token-min-scopes-workers
description: Minimum Cloudflare API token scopes to deploy a Workers + KV + Browser Rendering app — Workers Scripts:Edit, Workers KV Storage:Edit, Browser Rendering:Edit, Account Settings:Read. A token with only basic identity scope passes wrangler whoami but fails every account-scoped operation with confusing 10000 errors.
metadata:
  type: reference
---

Minimum CF API token scopes for a typical Worker deploy stack:

| Scope | Why |
|---|---|
| **Account → Workers Scripts: Edit** | `wrangler deploy`, `wrangler tail` |
| **Account → Workers KV Storage: Edit** | `wrangler kv namespace create/list/delete`, `wrangler secret put` (secrets are stored in KV under the hood) |
| **Account → Workers R2 Storage: Edit** | (optional) if Worker uses R2 |
| **Account → Browser Rendering: Edit** | calls to `/accounts/{id}/browser-rendering/*` (e.g. `oom-scrape-mcp` CF browser-rendering REST) |
| **Account → Account Settings: Read** | `wrangler whoami`, account-detail enumeration |

**Resource scope:** "Specific account → \<your account name\>" (NOT "Include all accounts" — that template is for multi-account agency tokens and Cloudflare sometimes drops account-level scopes when you save with "All accounts" selected).

**Diagnostic for "I added scopes but it's still 10000":**

1. `curl -H "Authorization: Bearer $TOKEN" https://api.cloudflare.com/client/v4/accounts/$ACCT/tokens/verify` — must return `success: true`.
2. Then probe each scope's actual endpoint directly:
   - Workers Scripts → `GET /accounts/$ACCT/workers/scripts`
   - KV → `GET /accounts/$ACCT/storage/kv/namespaces`
   - Browser Rendering → `POST /accounts/$ACCT/browser-rendering/content` with `{"url":"https://example.com"}`
   - Subdomain → `GET /accounts/$ACCT/workers/subdomain`
3. Whichever endpoint returns 10000 names the missing scope. Re-edit the token, save with explicit "Specific account" resource scope, re-probe.

**Common silent failures:**
- Token saved with "All accounts" resource scope drops account-level permissions when scope dropdown defaults reset.
- "Browser Rendering" appears under TWO permission groups (Account-level + Zone-level); pick the Account-level one for Worker deploys.
- "Read" on a permission is NOT enough for `wrangler deploy` (writes), but IS enough for listing. Mixing read-only sub-scopes will partially work and confuse the operator.

**Token format check:** OneOnMe uses Account API Tokens prefixed `cfat_` (53 char). The `verify` endpoint `/accounts/{id}/tokens/verify` is for account-scoped tokens; `/user/tokens/verify` is for user-scoped tokens. Hitting the wrong verify endpoint returns "Invalid API Token" even when the token is fine — confusing but harmless.

**Validated 2026-05-21 on OOM-53 scrape-mcp deploy:** initial token (personal CF) only had basic identity scope — `whoami` worked, `kv namespace list` 10000'd. JM rotated scopes on the work-CF token, re-probe confirmed all 4 Worker-relevant endpoints succeeded. Final scopes on token id `c9bb34d3b8da680e5f135d6f1dc260e9` (work CF account `608361cd8e347f99d5a46b1d52c89bce`).

Related: [[wrangler-account-id-caching]], [[cloudflare-account-topology]].
