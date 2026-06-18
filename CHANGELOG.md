# Changelog

All notable changes to the dot-me spec land here. Individual release notes carry the full rationale; this file is the index.

The spec is additive-only by policy ([CONTRIBUTING.md](CONTRIBUTING.md) §Schema evolution policy). Every release listed here is a strict superset of the previous one: existing `~/.me/` content stays valid across version bumps.

## Releases

- **[v0.4.0](RELEASE_NOTES_v0.4.0.md)** (2026-06-18): `voice.compact.md` optional derived companion — a ~30-line always-loaded extract of `voice.md` that fixes the silent-failure gap where conditional voice loading leaves prose tasks defaulting to model house style. Sets the default voice exposure (§6.1: compact-always, full-lazy); documents a §6.3-compliant prompt-trigger enforcement hook as the optional backstop. Additive: existing `~/.me/` content stays valid; producers that skip the compact file stay conformant.
- **[v0.3.0](RELEASE_NOTES_v0.3.0.md)** (2026-05-18): `past_work[]` sibling block (narrows `work[]` to current-only); `inner_circle[].handles` optional social-handle map; consumer installers treat missing `spec_version` as legacy `"0.1"`.
- **[v0.2.0](RELEASE_NOTES_v0.2.0.md)** (2026-05-16 / 2026-05-17): Seven optional `identity.yaml` fields (`nickname`, `email`, `website`, `avatar`, `headline`, `social_profiles[]`, `languages`, plus nested `location.city` / `location.country`) aligning to vCard / Schema.org / OIDC / FOAF / JSON Resume baselines; `working-style.yaml` added as the fourth content file (imperative behavioral defaults).
- **[v0.1.0](RELEASE_NOTES_v0.1.0.md)**: initial public draft. Three content files (`identity.yaml`, `voice.md`, `preferences.yaml`), the `~/.me/` filesystem convention, load-at-session-start contract, threat model.

## Pre-release history

Design rationale and adversarial-review thread for v0.1 live in the maintainer's home-lab repo: [`personal-context-design.md`](https://github.com/thebestmensch/home-lab/blob/main/docs/superpowers/specs/2026-05-05-personal-context-design.md).
