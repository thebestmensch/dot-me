---
name: cte-pattern-for-single-statement-mcp
description: MCP Postgres tools that advertise "single statement only" can't run BEGIN; … COMMIT;. The atomic equivalent is a multi-CTE single statement (WITH ... RETURNING chains + CROSS JOIN to thread new IDs). Use this pattern in skills/runbooks targeting query-style MCP tools; don't author BEGIN/COMMIT prose that the tool can't execute.
metadata:
  type: feedback
---

When a skill, runbook, or agent prompt prescribes a multi-statement transaction (`BEGIN; INSERT ...; INSERT ...; COMMIT;`) for an MCP-backed Postgres tool, verify the tool actually supports multiple statements before shipping the prose. Tools like `mcp__plugin_oneonme-database_oom-db__query_database_rw` explicitly state "A single SQL statement to execute. Multiple statements are not supported." A `BEGIN; ... COMMIT;` prescription against such a tool either silently runs only the first statement or errors at parse — neither is the atomicity the skill author intended.

**Why:** Skills authored against a generic "Postgres can do transactions" mental model rot when the tool layer is single-statement. The skill's transaction guarantees become vapor; partial-write hazards re-appear under whatever loose error handling the tool exposes. Authors copy the BEGIN/COMMIT pattern from sibling docs (Django shell, psql examples) without verifying it works against the actual runtime, same failure mode as [[introspect-schema-before-authoring-sql-docs]] but at the tool-API layer, not the column-name layer.

**The atomic equivalent** is one statement built as a CTE chain:

```sql
WITH new_address AS (
  INSERT INTO address_address (...) VALUES (...) RETURNING id
),
new_extraction AS (
  INSERT INTO core_extractionrecord (...) VALUES (gen_random_uuid(), ...) RETURNING id
),
new_establishment AS (
  INSERT INTO establishments_establishment (...)
  SELECT gen_random_uuid(), ..., (SELECT id FROM new_address), (SELECT id FROM new_extraction), ...
  RETURNING id
),
new_menu AS (
  INSERT INTO menus_menu (...)
  SELECT gen_random_uuid(), (SELECT id FROM new_establishment), ...
  RETURNING id
),
item_data(name, price, category_id, ...) AS (VALUES (...), (...), ...),
new_items AS (
  INSERT INTO menus_menuitem (...)
  SELECT gen_random_uuid(), m.id, d.category_id, d.name, ...
  FROM item_data d CROSS JOIN new_menu m CROSS JOIN new_extraction e
  RETURNING id
)
SELECT (SELECT id FROM new_establishment) AS establishment_id, (SELECT COUNT(*) FROM new_items) AS items_inserted;
```

PostgreSQL guarantees a single statement is atomic — all CTE INSERTs commit together or none do. The `VALUES (...) AS data_table` + `CROSS JOIN` pattern keeps the SQL size linear in row count (each row is just its column tuple, not a full per-row `(gen_random_uuid(), (SELECT id FROM ...), '<uuid>'::uuid, ...)` boilerplate). ~150 rows fit in ~21KB of SQL.

**How to apply:**

1. Before writing a `BEGIN; ... COMMIT;` prescription in a skill or runbook that targets an MCP DB tool, read the tool's description. If it says "single statement only" (or equivalent), use the CTE chain instead.
2. Thread IDs forward via `(SELECT id FROM <previous_cte>)` in scalar position, or `CROSS JOIN <previous_cte>` when building multi-row INSERTs from a `VALUES`-based data table.
3. Generate the CTE programmatically when the row count is meaningful (>20 rows). Hand-typed VALUES lists are bug magnets at scale; a small Python builder in `$CLAUDE_JOB_DIR` is the right move.
4. Final `SELECT` should return the IDs and row-counts the verifier step (e.g., Step 7) will check.
5. Document the pattern in the skill itself — don't make the next caller re-derive it.

Validated 2026-05-21 on OOM-53 smoke test: SKILL.md prescribed `BEGIN; ... COMMIT;` for the venue write package, but `query_database_rw` is single-statement only. CTE chain shipped The Vandal (12 tabs + 141 items) atomically. Findings folded into OOM-125.

**Skip-when:** the MCP tool description explicitly supports multi-statement execution (e.g., a `psql_exec`-style passthrough), OR you're running the SQL via a non-MCP path (`psql`, Django shell, raw cursor in a management command). Then `BEGIN; ... COMMIT;` is fine.

Related: [[introspect-schema-before-authoring-sql-docs]] (sibling rule, column-name layer instead of tool-API layer).
