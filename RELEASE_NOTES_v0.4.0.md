# dot-me v0.4.0

Strictly-additive release that closes a silent-failure gap in the load contract: **conditional voice loading leaves prose tasks blind.** No field renamed or removed, no `spec_version`-gated semantic change — every v0.3 (and earlier) `~/.me/` is a valid v0.4 setup unchanged.

The change is one optional derived companion file (`voice.compact.md`) plus the load-contract and integrity-baseline rules around it, motivated by real friction the maintainer hit running v0.3 daily: a quick "rewrite this bio" inside a coding session got every fact and zero voice signal, because nothing had loaded `voice.md`. The draft read corporate. Nothing errored.

## The gap

`voice.md` is rich (often 10-20 KB). §6.1 loads it *conditionally* — only when the agent expects to generate user-facing text. That conditional load fails silently when:

1. The task isn't obviously prose at the prompt level (a "pick a tagline" request is a copy decision wearing a config-pick costume).
2. The agent skips the cue under context-budget pressure (long session, parallel work, post-compaction resume).
3. The consumer has no skill-discovery semantics to fire an on-demand load at all.

In every case the agent has the user's full identity and no voice, so the first draft defaults to model house style: corporate, em-dash-heavy, "It's worth noting that...". There's no signal the miss happened — the output just isn't the user's voice.

## What's new

- **`voice.compact.md`** (§4, §5.2.1): an optional, producer-generated, ~30-line extract of `voice.md` carrying the top-tier signal — the identity-invariant rules (no em-dashes, no semicolons, no corporate phrases, connective-driven flow) and the loudest AI-speak tells to strip. It is **derived, not a fifth core file**: same status as the integrity sidecar (implementation choice). On any conflict the full `voice.md` wins.
- **Default voice exposure** (§6.1): the recommended posture is now **compact-always, full-lazy**. Always-load `voice.compact.md` (like `identity.yaml`) so the floor is never "zero voice" for ~2 KB; reserve the full `voice.md` for the deep load on real prose work. A consumer that can do reliable conditional loading MAY skip the always-load, but the floor is the safer default and the two compose.
- **Enforcement-hook pattern** (§6.4): an optional, §6.3-compliant prompt-trigger pattern for consumers wanting belt-and-suspenders — a runtime hook that detects prose intent (`draft`, `bio`, `rewrite`, `email`, ...) and injects the full `voice.md` for that turn. Hard boundary restated: the hook MUST inject into the instruction context (harness-side assembly), MUST NOT expose a new model-callable fetch surface (the §6.3 exfiltration vector). A reference Claude Code `UserPromptSubmit` hook ships in [`examples/voice-enforcement-hook/`](examples/voice-enforcement-hook/).
- **Integrity baseline** (Appendix C): `voice.compact.md` joins the `.integrity` hash set when present, because an always-loaded file is the same tamper surface as `identity.yaml` — leaving it unbaselined would be a blind spot.

## Compatibility

**Strictly additive. Every v0.3 / v0.2 / v0.1 `~/.me/` is a valid v0.4 setup unchanged.** No field renamed or removed; no `spec_version`-gated semantic narrowing (unlike v0.3's `work[]`).

- A producer that never generates `voice.compact.md` stays fully conformant — it just doesn't get the default-exposure benefit, exactly as today.
- A consumer that never loads `voice.compact.md` stays fully conformant — it falls back to the prior conditional-`voice.md` behavior.
- Consumers MUST work correctly whether or not the companion exists (§4, §6.1). This is the same "MUST NOT depend on files beyond the four core" rule the integrity sidecar already lives under.

No consumer is required to branch on `spec_version` for this release. The companion is detect-and-use-if-present.

## Why a separate file, not voice.md frontmatter or a fifth core file

Considered both. Rejected:

- **A fifth core file** would break "these four files are the format" (§4) and the additive-superset guarantee that makes version bumps safe. The companion is derived from an existing core file, so it belongs in the same "implementation choice" tier as `.integrity`, not in the format's spine.
- **YAML frontmatter on `voice.md`** (the open §5.2 question) is orthogonal: frontmatter is metadata *about* the file, not a separately-loadable lightweight payload. The whole point of the compact file is to load ~2 KB without loading the ~20 KB parent; frontmatter doesn't give you that.
- **Always-loading the full `voice.md`** solves the silent failure but at ~20 KB every session for a signal most sessions don't use. The compact extract is the cost-proportionate answer.

The one real cost of a derived file is drift: a stale compact file silently ships outdated voice. v0.4 accepts manual sync (kept current by the `/me` producer by convention) and defers automated generation to v0.5 (see open questions). The drift risk is bounded because the full `voice.md` is authoritative on conflict.

## Open questions for v0.5

- Should the spec mandate (or reference-implement) automated `voice.compact.md` generation from `voice.md`, rather than the v0.4 hand-maintained-by-convention approach? A stale compact file is the one structural risk this design carries.
- Should `voice.md` allow optional YAML frontmatter (e.g., `voice_version`) — which would also give the compact extract a derivation-provenance anchor?
- Does the spec need a "non-conformance" section (carried from v0.4 open questions)?
- `education[]` / `honors[]` / `certifications[]` on `identity.yaml` (carried).

## License

MIT. See [LICENSE](LICENSE).
