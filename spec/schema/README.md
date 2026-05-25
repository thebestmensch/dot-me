# dot-me JSON Schemas

Machine-readable schemas for the structured dot-me files. Tracks `SPEC.md` §5.A and §5.3.

> **Read this first.** These schemas enforce *structural shape*. The single non-`name` strict invariant in SPEC §5.1 — `location.timezone` MUST be a valid IANA identifier — is not enforced by JSON Schema alone, because most validators (including Python `jsonschema` by default) treat `format` as annotation-only. The bundled `validate-examples.py` layers a `zoneinfo.available_timezones()` check on top. If you wire either schema into your own validator without that extra check, you will silently pass typos like `America/Not_A_Zone`. Either pass an explicit format checker that knows IANA zones, or run the supplied validator instead of (or in addition to) a generic one.

| File                       | Covers                              | Spec section |
| -------------------------- | ----------------------------------- | ------------ |
| `identity.schema.json`     | `~/.me/identity.yaml`               | §5.A / §5.1  |
| `preferences.schema.json`  | `~/.me/preferences.yaml`            | §5.3         |

Out of scope:

- `voice.md` — intentionally unstructured prose (SPEC §5.2). Not a schema target.
- `working-style.yaml` — schema deferred. The §5.4 dimensions are descriptive section markers, not enforceable structure; the value is in the imperative rule strings inside, which a schema can't validate. May land in a future revision if implementers ask for it.

## What the schemas enforce

- **`name`** is the only required field in `identity.yaml` (SPEC §5.1).
- When `location` is present, `location.timezone` is required (§5.1). The schema combines a structural regex with `format: iana-time-zone` as a hint to validators that support tzdata lookup. **Real IANA-zone validation is executable** — the bundled `validate-examples.py` checks against `zoneinfo.available_timezones()` because most generic JSON Schema validators (including Python's `jsonschema`) treat `format` as annotation-only by default. Consumers wiring this schema into their own validator should pass an explicit format checker or layer a zoneinfo check on top.
- `past_work[].start` and `.end` accept four-digit year as string or integer; `end` also accepts the literal `"present"`.
- `handle` MUST start with `@` when present.
- `additionalProperties: true` is set on every object so that the §5.6 forward-compat rule ("consumers MUST tolerate unknown keys") holds at the schema layer too. The schemas describe the contract, not the universe.

**SHOULD-level fields stay unconstrained at the schema layer.** SPEC §5.1 marks `location.country` as SHOULD be ISO 3166-1 alpha-2 and `languages[]` SHOULD be BCP 47. The schema documents both with descriptions but does not pattern-enforce them — install-time validation would otherwise harden SHOULD-level guidance into rejection, breaking dot-me's loose/additive compatibility promise for files that predate the schema. If future spec revisions promote either to MUST, the schema and SPEC.md change together.

`preferences.yaml` has no required fields. The schema documents the conventional top-level buckets (`tools`, `aesthetics`, `media`, `workflow`, `notes`) but leaves nested shape free-form, which matches SPEC §5.3.

## Validate your own files

The schemas are standard JSON Schema 2020-12, so any conforming validator works. Two paths:

```bash
# from a clone of this repo:
uv run --with jsonschema --with pyyaml python spec/schema/validate-examples.py

# against your own ~/.me/identity.yaml with check-jsonschema (pip):
pipx run check-jsonschema --schemafile spec/schema/identity.schema.json ~/.me/identity.yaml
```

The bundled `validate-examples.py` walks every `examples/<persona>/*.yaml` and reports per-file pass/fail. It MUST stay green; run it whenever the schemas or examples change. (CI gating is open as a future improvement once the repo grows a workflow file.)

## Stability

These schemas track the spec at the same version. When SPEC.md bumps from v0.3 → v0.4, both schemas and `validate-examples.py` are updated in the same PR. Schemas remain additive-only / forward-compatible: existing valid files stay valid across spec bumps, matching the dot-me forward-compat promise.
