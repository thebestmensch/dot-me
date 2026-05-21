---
name: verify-plugin-runtime-claim
description: When a Claude Code plugin claims callable from a specific environment (Cowork, Claude Desktop, mobile), verify the plugin's actual deps work IN that environment before declaring done. Authoring on local CC and asserting Cowork compat from a less-restrictive environment is the failure mode. Same pedagogy as introspect-schema-before-authoring and live-probe-external-creds, applied to the runtime layer.
metadata:
  type: feedback
---

When a plugin's `plugin.json` description or marketplace entry asserts "callable from Cowork" (or Claude Desktop, or mobile, or any environment more restricted than local CC), audit the skill/command body for deps that environment can't satisfy. The asymmetry is dangerous: local CC has Bash, env vars, file IO, and every MCP a developer has installed; Cowork has WebFetch + WebSearch + Claude Code built-ins + whatever hosted MCPs the user has connected — NOT Bash, NOT env vars, NOT shell pipes.

**Why:** Plugin authors test on local CC and gut-check "should work in Cowork" without actually running the skill there. The failure mode lands on the user — they install the plugin in Cowork, hit a Tier-2 fallback that needs `curl | jq` and an API key from an env var, get a half-finished result with no error path. Worse: the plugin author iterates on the doc copy ("now Cowork-ready!") without changing the actual deps, propagating the false claim across versions.

This is the same failure pattern as [[introspect-schema-before-authoring-sql-docs]] (schema layer), [[cte-pattern-for-single-statement-mcp]] (tool-API layer), [[live-probe-external-creds]] (creds layer). Different surface, same pedagogy: verify the claim against the actual runtime, not against your local mental model.

**Cowork's known gaps** (as of 2026-05-21):
- No Bash tool — `curl`, `jq`, `pdftotext`, any pipe is unavailable
- No env vars exposed to the model (no `$OPENAI_API_KEY`, no `$CF_ACCOUNT_ID`)
- No local file system writes (Read/Write tools operate on uploaded files, not arbitrary paths)
- WebFetch and WebSearch work
- Hosted MCP plugins work (`oneonme-database` MCP is the canonical example — OAuth, server-side secrets)
- Claude Code built-ins (Read for uploads, Write to ephemeral, TaskCreate, etc.) work

**The hosted-MCP pattern** is the canonical workaround for capabilities Cowork can't natively provide:
- Wrap the Bash-requiring capability as an MCP tool hosted on a Cloudflare Worker (or equivalent)
- Bake secrets into the Worker's secret store, not into the client
- Use OAuth on the domain you trust (`@oneonme.com` Google sign-in for OneOnMe MCPs)
- Client just calls `mcp__plugin_<name>__<tool>` — no env vars, no Bash, no client-side keys

**How to apply:**

1. Before authoring any "callable from Cowork" claim in `plugin.json` or `marketplace.json` description, grep the skill/command body for `Bash`, `curl`, `\$[A-Z_]+`, `jq`, `pdftotext`, `process.env`. Each hit is a Cowork blocker until proven otherwise.
2. If you find blockers and want the Cowork claim to hold: either drop the claim, drop the dep path (often a fallback that's never load-bearing), or build a hosted MCP plugin to expose the capability server-side.
3. End-to-end test in Cowork before shipping: install the plugin, invoke the skill on a real input that exercises every documented fallback tier. "It works on my local CC" is not Cowork verification.
4. If the plugin description's Cowork claim is inherited from a sibling plugin (e.g. "same pattern as oneonme-database"), still audit — the sibling may have built the hosted-MCP shim while your plugin still uses raw `curl`.
5. Don't ship a "Cowork compat as v0.2" plan. Either it works in Cowork at v0.1 or the description doesn't claim it does. Half-claimed compat is worse than no claim — users install and hit the gap silently.

**Validated 2026-05-21 on OOM-53 follow-up:** PR #18 shipped `oneonme-menu-discovery` plugin v0.1.0 claiming "callable from Cowork, Claude Desktop, or local CC." Post-merge dep audit found Tier 2 (Cloudflare browser-rendering via `curl` + `$CF_ACCOUNT_ID`) and Tier 3 (PDF via `curl | pdftotext`) both Bash+env-var-dependent — neither works in Cowork. ~50% of venues with JS-rendered or PDF menus would have hit silent half-failure. Fix path: build a new `oneonme-scrape` hosted MCP plugin (CF Worker, OAuth `@oneonme.com`, secrets in Worker store) exposing `crawl_js_rendered(url)` and `pdf_to_text(url)` server-side; port skill Tier 2/3 prose to call the new MCP tools. Tracking as part of the rename PR (oneonme-menu-discovery → oneonme-menus).

**Skip-when:** the plugin is explicitly scoped to local-CC-only (`engineering` plugins requiring `cd` into a repo, dev-server commands, etc.). Don't claim Cowork compat on those; the audit is moot.

Related: [[cte-pattern-for-single-statement-mcp]] (tool-API-shape layer), [[introspect-schema-before-authoring-sql-docs]] (schema layer), [[live-probe-external-creds]] (creds layer).
