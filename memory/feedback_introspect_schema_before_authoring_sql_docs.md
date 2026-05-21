---
name: Live-introspect schema before authoring SQL in skills/runbooks
description: Skills, runbooks, and agent prompts that ship SQL with literal column names rot silently — the doc keeps referencing columns that don't exist. Introspect the live schema while authoring, not as cleanup after a reviewer flags it.
metadata:
  type: feedback
---

When authoring SQL inside a skill, runbook, or agent prompt that **another agent or session will execute**, live-introspect the schema before shipping the column names. Don't trust training-data column names or names copy-pasted from a sibling doc.

**Why:** SQL embedded in docs rots without a compiler to catch it. The doc keeps referencing `e.website`, `e.phone`, `aa.formatted_address` because that's what training-data Django apps tend to use, but the actual schema has `e.url`, `e.phone_number`, `aa.formatted`. A future agent executing the SQL at production write-time gets a runtime error — and may not catch it before a partial-write orphan lands. Sibling runbooks (like the agent's existing `prompt.md`) often carry the same drift, so imitating them propagates the bug instead of fixing it.

Validated 2026-05-21 on OOM-53 `add-venue-menu` skill: drafted SQL by adapting the autonomous menu agent's `prompt.md`, which inherited `e.phone`, `e.website`, `aa.formatted_address` from somewhere. Codex round-1 review didn't catch the column names (they looked plausible). The 5-edit checkpoint hook fired with "verify you're not drifting into assumption-based changes" — only then did I run `mcp__plugin_oneonme-database_oom-db__schema_introspect` and confirm the actual columns are `e.url`, `e.phone_number`, `aa.formatted`. The agent's `prompt.md` works in production only because Django ORM maps fields at the framework layer; raw SQL in the skill has no such safety net.

**How to apply:**

When the diff includes literal column names inside SQL inside a skill / runbook / agent prompt:

1. Pause before declaring done.
2. Introspect every table the SQL touches (Postgres MCP `schema_introspect`, `\d <table>`, `DESCRIBE`, etc.).
3. Verify each column name in the doc exists in the schema.
4. While you're there, list the NOT NULL columns with no default — raw `INSERT` statements that omit those fail at runtime. ORM-driven prompts elide them because Django/Rails auto-fills; raw-SQL docs need them explicit.
5. If you find drift, fix the doc AND check whether the sibling source (e.g., `prompt.md`) carries the same drift — per [[feedback_codex_port_disposition]], backport in the same session or file a follow-up ticket.

**Skip-when:** SQL you're executing yourself ad-hoc in this session. The cost-benefit only flips when other actors will read + execute the SQL later. Doc-shipped SQL is the load-bearing case.

**Skip-when (negative example):** Don't introspect every column on every read query. The rule is for the **authored output**, not exploratory work.
