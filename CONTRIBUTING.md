# Contributing

`dot-me` is a small format spec plus one maintainer's lived-in example. Two kinds of contribution welcome:

- **Spec clarifications** — sections that are ambiguous, edge cases the spec doesn't cover, contradictions between the README and the linked design doc
- **Consumer-tool integration notes** — you're building a tool that loads `~/.me/` and you've hit something the spec doesn't help you with

**Not a fit:**

- PRs against `identity.yaml`, `voice.md`, `preferences.yaml`, or anything in `memory/` — these are the maintainer's personal content, included as a worked example. Forks are encouraged; PRs into this repo's content are closed without review.
- Scope expansions ("you should add a field for X") — file an issue using the consumer-tool-integration template first so we can discuss whether the addition belongs in the spec, in consumer tools, or in a v1.

## Schema evolution policy

The spec is **additive-only**. Producers MAY add new top-level keys; consumers MUST ignore unknown keys. This is the contract that lets the spec evolve without breaking every consumer tool downstream.

- ✅ Adding `dietary` under a future v0.2 — consumers that don't know about it keep working
- ❌ Renaming `preferred_name` → `nickname` — every existing consumer breaks
- ❌ Tightening a previously-loose field to require a stricter shape — existing user content becomes invalid

When proposing additions: state the user-context need, give an example field shape, name a consumer tool that would actually use it.

## How to file an issue

Pick the template that fits:

- **Spec clarification** — "Section X says Y but doesn't cover Z"
- **Consumer-tool integration** — "I'm building [tool] and I can't tell how to handle [edge case]"

For security issues: see [SECURITY.md](SECURITY.md) — please email, don't open a public issue.

## Local development

There's nothing to build. The "tooling" is `git`, a text editor, and consumer tools that read these files. To propose spec changes, edit [`SPEC.md`](SPEC.md) in this repo. Design history and adversarial-review thread for v0.1 live in the maintainer's home-lab repo (linked from `SPEC.md`).

## Code of conduct

Be normal. Slow, calm responses; ambiguity is fine; "I don't know" is fine. Bad-faith engagement (drive-by demands, demands for unpaid work, scope-expansion via fait-accompli PRs) gets a single response and then a lock.
