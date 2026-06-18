# dot-me v0.5.0

Strictly-additive release: one optional `identity.yaml` block (`education[]`) plus a reference producer subcommand (`/me linkedin-import`) that populates work history from a LinkedIn export. No field renamed or removed; every v0.4 (and earlier) `~/.me/` is a valid v0.5 setup unchanged.

Motivated by a recurring chore: building a bio or "about me" output that references work history meant manually downloading a LinkedIn export, unzipping it, and pasting rows into chat — and none of that parsing survived the session. v0.5 makes the import durable and one-shot.

## What's new

- **`education[]`** (§5.1): optional schooling history on `identity.yaml`, mirroring JSON Resume's `education[]` shape (`institution`, `degree`, `area`, `start`, `end`). This is the sibling block v0.3 explicitly deferred ("`education[]` / `honors[]` / `certifications[]` — worth a separate proposal"). Low-velocity historical facts a bio draws on, alongside `work[]` + `past_work[]`.
- **`/me linkedin-import <export.zip>`** (reference producer, `plugin/scripts/linkedin-import.py`): parses a LinkedIn data export and merges it into `~/.me/identity.yaml`. A producer convenience, **not** part of the format.

## Design: reuse the schema, don't fork it

The importer maps a LinkedIn export onto the **existing** identity fields rather than inventing parallel ones:

| LinkedIn source | dot-me destination | Notes |
|---|---|---|
| `Profile.csv` → Geo Location | `location.city` | gap-fill |
| `Profile.csv` → Websites | `website` + `social_profiles[]` | first URL is `website` |
| `Profile.csv` → Twitter / Headline | `social_profiles[]` / `headline` | headline gap-filled |
| `Positions.csv` (current) | `work[]` | role still open (no end date) |
| `Positions.csv` (ended) | `past_work[]` | with `start` / `end` / `summary` |
| `Education.csv` | `education[]` | new in v0.5 |

The original JM-254 proposal floated a parallel `work-history.yaml` file. It was written the same day `past_work[]` (v0.3) landed, which supersedes the need — `Positions.csv` maps onto `work[]` / `past_work[]` directly, so v0.5 adds no new file and only the one genuinely-missing field (`education[]`).

## Importer behavior

- **Non-destructive.** Curated scalars (`headline`, `website`) are gap-filled only — a non-empty existing value is kept unless you pass `--force`. `work` / `past_work` / `education` merge BY KEY (org+role / institution+degree): matched entries take LinkedIn's dates/summary but keep manual-only sub-fields like a hand-written `mission`. Manual entries LinkedIn lacks are preserved.
- **Idempotent.** Re-running with a fresher export updates in place; it does not append duplicates.
- **Comment-preserving.** Round-trips `identity.yaml` via ruamel.yaml, so hand-written comments and field order survive.
- **Tier-aware.** A Basic export (instant, `Profile.csv` only) imports location/website/headline and reports, per section, that `Positions.csv` / `Education.csv` are Full-export-only (~24h to request). It never fabricates chronology from a Basic export.
- **Dry-run-first.** `/me linkedin-import` runs `--dry-run` and shows the diff before any write. The write is atomic (write-then-rename, SPEC §7) and refreshes `~/.me/.integrity`.

## Compatibility

**Strictly additive.** No `spec_version`-gated semantic change. `education[]` is optional and unknown-keys-tolerated per §5.6; a consumer that ignores it stays conformant. The importer is a reference-plugin tool — producers on other consumers are unaffected. The shipped installers (codex/cursor/gemini) accept `spec_version: "0.5"` (a 0.5 identity is structurally a superset of 0.4).

## Open questions for v0.6

- `honors[]` / `certifications[]` on `identity.yaml`, mirroring `education[]` — file if a consumer surfaces a use case (LinkedIn's `Certifications.csv` would map cleanly).
- Other-source imports (GitHub profile, Twitter export) — separate tickets if there's appetite.
- Automated `voice.compact.md` generation (carried from v0.4).

## License

MIT. See [LICENSE](LICENSE).
