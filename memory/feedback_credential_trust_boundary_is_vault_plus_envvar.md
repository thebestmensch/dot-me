---
name: credential-trust-boundary-is-vault-plus-envvar
description: "When splitting a credential by scope (runtime vs admin, etc.), the real trust boundary is the *intersection* of (1P vault grant for the consuming SA token) AND (env var name + every consumer reading it), NOT field/item layout. Co-located fields in the same vault = same access scope. Same env var name for both scopes = brittle override surface."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 725539cb-afaf-43ef-ba16-733eef009fe9
---

When splitting a single credential into separate scopes (e.g. runtime-readable vs admin-only), the trust boundary is two-layered:

1. **1P vault grants on the consuming SA token.** Fields and items in the same vault are equivalent in access scope from any SA with READ on that vault. Putting `runtime_api_key` and `cli_api_key` on the same item, or even separate items in the same vault, does NOT isolate — the container's SA token can `op read` any path in that vault.
2. **Env var name reuse.** If two consumers read the same env var name with different semantic expectations (container's `tickets` CLI reads `LINEAR_API_KEY_OOM` as runtime; host-side admin sync reads `LINEAR_API_KEY_OOM` as admin), sourcing the resolved `.env` on the wrong host silently substitutes the wrong-scope token. The op-ref split is meaningless if the env-var name lets one scope masquerade as the other.

**Why:** Validated 2026-05-20 on JM's OneOnMe linear-agent design. Three Codex adversarial-review rounds, each catching a different layer:
- Round 1: `cli_api_key` reused for runtime + admin (field-level collision)
- Round 2: After splitting fields, container SA still had READ on whole vault → could `op read op://machine/.../cli_api_key` anyway (vault-scope collision)
- Round 3: After moving admin PAT to a different vault, both consumers still read `LINEAR_API_KEY_OOM` env var → sourcing container `.env` on host substituted runtime PAT into admin sync (env-var-name collision)

Each round was non-overlap with the Claude-family in-session reviewers. The pattern wasn't narrowing (per `feedback_codex_fix_review_iteration` cap-at-3 rule); each round was a genuinely different layer of the same trust boundary.

**How to apply:** When designing or reviewing credential-scope splits:
- Inventory every SA token + its vault grants. Two scopes need two SA tokens with disjoint vault grants. Field-level or item-level separation in one vault is theater.
- Inventory every env var name + every consumer that reads it. Two scopes need two env var names. A negative isolation check belongs in the spec DoD: `OP_SERVICE_ACCOUNT_TOKEN=<runtime-SA> op read <admin-ref>` MUST fail.
- Related migration gotcha: see [[feedback_credential_migration_audit_consumers]] for "grep target's existing consumers BEFORE rewrite."
- Related: [[feedback_codex_fix_review_iteration]] (security-critical diffs budget 3-5 rounds, push back when finding conflicts with codebase arch).
