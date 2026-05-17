# dot-me v0.2.0

Schema-additive release. Closes the "homebrewed shape" gap between dot-me `identity.yaml` and the canonical identity specs (vCard RFC 6350, Schema.org Person, OIDC standard claims, FOAF, JSON Resume) by promoting seven baseline fields that every comparable spec carries.

## What's new

Seven optional fields added to `identity.yaml` (§5.1):

- **`nickname`**: informal short label (vCard `NICKNAME` / FOAF `foaf:nick`). Distinct from `preferred_name`.
- **`email`**: primary contact email (vCard `EMAIL` / Schema.org `email` / OIDC `email` / FOAF `foaf:mbox` / JSON Resume `basics.email`). Universal across all five canonical specs.
- **`website`**: canonical homepage URI (vCard `URL` / Schema.org `url` / FOAF `foaf:homepage` / JSON Resume `basics.url`).
- **`avatar`**: profile image URI (vCard `PHOTO` / Schema.org `image` / OIDC `picture` / FOAF `foaf:depiction` / JSON Resume `basics.image`). Optional and not load-bearing for text-mode consumers, but present here for shape parity with the canonical specs and future multimodal use.
- **`headline`**: one-line professional label, distinct from `work[]` and `blurb` (JSON Resume `basics.label` / Schema.org `jobTitle`).
- **`social_profiles[]`**: list of `{network, url}` objects (JSON Resume shape / Schema.org `sameAs` semantics / vCard `IMPP` + `X-SOCIALPROFILE`). Replaces the single opaque `handle` for new producers; `handle` is retained for backward compatibility (when both are present, `social_profiles` is authoritative).
- **`languages`**: BCP 47 language tags for spoken/written languages (Schema.org `knowsLanguage`). v0.1 conflated spoken languages and domain expertise under `knows_about`; v0.2 splits them per Schema.org's distinction.

Plus two nested additions:

- **`location.city`** and **`location.country`**: locality and ISO 3166-1 alpha-2 country code, paired with the existing `timezone`. Aligns with how vCard, Schema.org, JSON Resume, and OIDC group location facts.

## Compatibility

v0.2 is **strictly additive**. Every v0.1 `identity.yaml` is a valid v0.2 file unchanged. Consumers built against v0.1 continue to work; they ignore the new optional fields per §5.5 (unknown-key rule). New consumers SHOULD branch on `spec_version` when treating `handle` / `social_profiles` as equivalent.

## Why these fields

Each of the seven fields appears in at least three of the five canonical identity specs surveyed:

| Field | vCard | Schema.org | OIDC | FOAF | JSON Resume |
|---|---|---|---|---|---|
| `email` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `nickname` | ✓ | - | ✓ | ✓ | (implied) |
| `website` | ✓ | ✓ | - | ✓ | ✓ |
| `avatar` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `social_profiles[]` | ✓ | ✓ | - | ✓ | ✓ |
| `languages` | ✓ | ✓ | ✓ | - | ✓ |
| `headline` | - | ✓ | - | ✓ | ✓ |
| `location.city` / `country` | ✓ | ✓ | ✓ | - | ✓ |

The goal is making dot-me feel "obviously the right baseline shape" to anyone reviewing the spec, not homebrewed.

## What did NOT make the cut

Fields present in canonical specs but deliberately omitted from v0.2:

- **`gender`**: `pronouns` already covers the AI-use-case more usefully ("they/them" is unambiguous; "non-binary" is not). Three specs carry both as independent fields, but for a name-tag, `pronouns` alone is sufficient.
- **`birthdate`**: present in four specs but no obvious name-tag value. May surface in v0.3 if a use case emerges.

## Open questions for v0.3

- `voice.md` optional YAML frontmatter (`voice_version`, etc.)
- Non-conformance section ("this tool doesn't support dot-me", what does that look like?)
- Native integrations: Codex hook, Cursor extension, Gemini CLI loader (minimum surface area for each)

## License

MIT. See [LICENSE](LICENSE).
