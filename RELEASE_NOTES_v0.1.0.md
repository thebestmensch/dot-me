# dot-me v0.1.0

Initial public release of the dot-me reference implementation.

## What is dot-me

> a name tag at the door for AI tools.

Three files at `~/.me/` (`identity.yaml`, `voice.md`, `preferences.yaml`) that AI tools load at session start so they know who the user is, how they sound, and what they like. Lightweight, filesystem-first, opt-in.

## What ships in v0.1.0

- **The v0.1 format spec.** Schema + load contract + precedence rules. See [the spec](https://github.com/thebestmensch/home-lab/blob/main/docs/superpowers/specs/2026-05-05-personal-context-design.md).
- **Reference content.** The maintainer's own `identity.yaml` + `voice.md` + `preferences.yaml` as a worked example.
- **Templates** under `examples/` — a fictional Sam Patel persona demonstrating each schema.
- **The `/me` consumer plugin** under `plugin/` — bundles a `/me` umbrella slash command (`scan` / `add` / `show` / `edit` / `check` / `init` subcommands) and a `SessionStart` integrity hook.
- **Public-repo hygiene** — LICENSE (MIT), SECURITY.md (threat model + disclosure), CONTRIBUTING.md (additive-only schema policy), GitHub issue templates.

## Audience

Wave 1: friends the maintainer will hand-hold for first-wave adoption. Wave 2 (strangers) is deferred to v0.2.

## Out of scope (deferred to v0.2 / v1)

- Cross-session sweep for `/me` scan
- Encrypted vault for `family` / `inner_circle` free-text notes
- Conformance test suite for downstream consumers
- MCP-resource exposure (conflicts with spec §6.3 read-at-startup rule)
- Cursor / Codex / other-vendor consumer plugins
- Stranger-adopter onboarding flow

## Feedback

`feedback.md` is the input stream for v0.2. PRs against `feedback.md` are welcomed without ceremony.

## License

MIT. See [LICENSE](LICENSE).
