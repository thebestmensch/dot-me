---
name: credential-migration-audit-consumers
description: "When migrating or consolidating 1Password (or any credential-store) references — rename, vault move, field merge — grep ALL existing consumers of BOTH source AND target refs before changing pointers. What looks like a clean field collapse can silently fold trust boundaries: a target ref already in use at one scope (e.g. admin full-API) silently expands to a new caller's scope (e.g. agent runtime read-only) and widens blast radius."
metadata:
  node_type: memory
  type: feedback
---

When migrating credential references (rename items, move vaults, collapse fields), the diff that *looks* purely mechanical (`s|op://oldvault/A/credential|op://newvault/B/cli_api_key|g`) can encode a real security regression.

**The pattern that bites:**

1. Source ref (`op://oldvault/A/credential`) was scope-X (e.g. read-only runtime).
2. Target ref (`op://newvault/B/cli_api_key`) is *already in use* by some other consumer at scope-Y (e.g. full-API admin sync).
3. Mechanical migration collapses one ref onto the other.
4. The original scope-X consumer (e.g. an agent container running with `bypassPermissions`) now reads scope-Y's higher-privilege token.

**Why:** Cross-provider non-overlap signal is exactly this — Claude-family reviewers infer-from-pattern (item name matches, field name matches → safe collapse) and miss the consumer-graph implication; Codex's GPT-5.x training catches "wait, who else reads this exact ref?" Validated 2026-05-20 on JM oneonme-platform Stage B migration: rewrote `op://oneonme/oom_linear_api_key/credential` → `op://machine/machine_linear_oneonme/cli_api_key` because the unified item already existed with both fields. Codex HIGH-flagged that `admin/scripts/sync_oneonme_linear_to_homelab.py:110` already used `cli_api_key` as the *admin full-API token*, distinct from the agent runtime token. The collapse would have shipped an admin-scope key to a bypassPermissions container. Caught pre-commit by Codex adversarial-review on the diff.

**How to apply:**

- Before any credential-ref migration, run `grep -rn 'op://<target-vault>/<target-item>/<target-field>'` across **all** consuming repos and code (not just the file you're editing). Same for source ref.
- If target ref has ≥1 existing consumer, name what scope it gives them and compare to what scope the new caller needs. Mismatch = stop, restore separation or design a new item/field.
- The README/spec is your friend: per-OneOnMe convention, README tables document "runtime" vs "admin" scopes per credential. Re-read those rows after rewrite; if both rows now point at the same item, that's the regression.
- Default to **separate items per trust scope** (one item per scope, even if the underlying secret value can be the same) — gives 1P SA-token vault grants something to scope against. Conflation removes that lever.
- This applies to any credential store: 1P, AWS SSM, Vault, GCP Secret Manager, etc.

**Related memory:**

- [[reference_op_cli_quirks]] — 1P CLI behaviors
- [[project_op_account_topology]] — current vault/item topology
- [[feedback_concrete_code_evidence_beats_inference]] — Codex's file:line citation beat my pattern-inference
