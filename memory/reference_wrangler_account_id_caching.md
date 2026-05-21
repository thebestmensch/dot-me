---
name: wrangler-account-id-caching
description: Wrangler caches the first-resolved CF account_id locally and uses it across subsequent calls even when CLOUDFLARE_API_TOKEN switches to a different account's token; explicitly set CLOUDFLARE_ACCOUNT_ID env var when crossing CF accounts.
metadata:
  type: reference
---

Wrangler (v4.93+) caches the first CF account it resolves and continues hitting that account's API endpoints even when `CLOUDFLARE_API_TOKEN` is swapped to a token belonging to a *different* CF account. Symptom: `wrangler whoami` correctly shows the new account, but `wrangler kv namespace list` (or any account-scoped call) hits the OLD account_id and fails with `Authentication error [code: 10000]`.

The 10000 is misleading — the token IS valid for ITS account, but wrangler is sending the request to the *wrong account's* URL path (e.g. `/accounts/<wrong_id>/storage/kv/namespaces`). The token isn't authorized for that other account, so CF returns auth error.

**Fix:** explicitly set `CLOUDFLARE_ACCOUNT_ID` env var to override wrangler's cached choice:

```bash
CLOUDFLARE_API_TOKEN=$WORK_TOKEN \
CLOUDFLARE_ACCOUNT_ID=608361cd8e347f99d5a46b1d52c89bce \
  bunx wrangler kv namespace list
```

**Diagnostic trick:** when wrangler returns 10000 but the same token works in raw curl against the same endpoint, run with `WRANGLER_LOG=debug WRANGLER_LOG_SANITIZE=false` and grep for `URL:` in the log. If the URL contains an unexpected account_id, that's the cache poisoning.

**How the cache gets seeded:** wrangler stores account info in `~/Library/Preferences/.wrangler/` (macOS) after the first successful `wrangler whoami` or `wrangler login`. Subsequent invocations prefer the cached value when no explicit env var is set, even when the token changes underneath.

**When this matters:** any workflow that touches multiple CF accounts (personal + work split, multi-tenant deploys, agency setups). For OneOnMe specifically: work CF `608361cd8e347f99d5a46b1d52c89bce` (paid plan, hosts oom-mcp / oom-design-mcp / oom-scrape-mcp) vs personal CF `d1deb1b79d3e9047ff9a132a22c84ae6` (free, jamesmensch.com DNS). See [[cloudflare-account-topology]].

**Validated 2026-05-21 on OOM-53 scrape-mcp deploy:** token swap from personal → work passed `whoami` but `kv namespace list` 10000'd because cached personal account_id was still the path target. Explicit `CLOUDFLARE_ACCOUNT_ID` env override fixed it. Same gotcha would have wasted ~10min if the wrangler debug log hadn't surfaced the URL mismatch.

Related: [[op-cli-quirks]] (same shape of env-var-override gotcha for `op` CLI).
