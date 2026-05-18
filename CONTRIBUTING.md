# Contributing

`dot-me` is a small format spec plus one maintainer's lived-in example. Two kinds of contribution welcome:

- **Spec clarifications**: sections that are ambiguous, edge cases the spec doesn't cover, contradictions between the README and the linked design doc
- **Consumer-tool integration notes**: you're building a tool that loads `~/.me/` and you've hit something the spec doesn't help you with

**Not a fit:**

- PRs against `identity.yaml`, `voice.md`, `preferences.yaml`, `working-style.yaml`, or anything in `memory/`. These are the maintainer's personal content, included as a worked example. Forks are encouraged; PRs into this repo's content are closed without review.
- Scope expansions ("you should add a field for X"). File an issue using the consumer-tool-integration template first so we can discuss whether the addition belongs in the spec, in consumer tools, or in a v1.

## Schema evolution policy

The spec is **additive-only at the file level**: every v0.N `identity.yaml` is a valid v0.(N+1) file unchanged. Producers MAY add new top-level keys; consumers MUST ignore unknown keys. v0.1 → v0.2 → v0.3 all preserve this; see [CHANGELOG.md](CHANGELOG.md) for the per-release diff.

The one wrinkle to know: v0.3 narrows the *semantic* of the existing `work[]` field (current-only under `spec_version: "0.3"`; mixed under earlier versions). Field-level compatibility holds (no key removed or renamed), but consumers MUST branch on `spec_version` to handle `work[]` without silently dropping historical roles. Future schema changes that can't be expressed additively will use the same escape hatch.

- ✅ Adding `dietary` under a future v0.4: consumers that don't know about it keep working (per §5.6 unknown-key rule)
- ❌ Renaming `preferred_name` → `display_name`: every existing consumer that reads `preferred_name` breaks
- ❌ Tightening a previously-loose field to require a stricter shape: existing user content becomes invalid

When a schema change can't be additive, the escape hatch is `spec_version`: bump the spec version, document the breaking change in the release notes, and have consumers branch on `spec_version` per §5.6.

When proposing additions: state the user-context need, give an example field shape, name a consumer tool that would actually use it.

## How to file an issue

Pick the template that fits:

- **Spec clarification**: "Section X says Y but doesn't cover Z"
- **Consumer-tool integration**: "I'm building [tool] and I can't tell how to handle [edge case]"

For security issues: see [SECURITY.md](SECURITY.md). Please email, don't open a public issue.

## Local development

There's nothing to build. The "tooling" is `git`, a text editor, and consumer tools that read these files. To propose spec changes, edit [`SPEC.md`](SPEC.md) in this repo. Design history and adversarial-review thread for v0.1 live in the maintainer's home-lab repo (linked from `SPEC.md`).

## Code of conduct

Be normal. Slow, calm responses; ambiguity is fine; "I don't know" is fine. Bad-faith engagement (drive-by demands, demands for unpaid work, scope-expansion via fait-accompli PRs) gets a single response and then a lock.
