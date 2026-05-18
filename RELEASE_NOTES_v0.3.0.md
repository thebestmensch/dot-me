# dot-me v0.3.0

Field-additive release with one **semantic narrowing of an existing field** (`work[]`) gated behind `spec_version`. Two `identity.yaml` additions, both motivated by real friction the maintainer hit running v0.2 against Claude Code, Codex, Cursor, and Gemini CLI for several weeks: `work[]` was conflating current and past roles (different update cadences, different field needs), and `inner_circle[]` carried names + relationship labels but no way to surface a contact's social handles for the agent to recognise.

Consumers MUST branch on `spec_version` to handle the `work[]` change without silent data loss. See [Compatibility](#compatibility).

## What's new

Two additions to `identity.yaml` (§5.A):

- **`past_work[]`**: sibling block for historical roles. Narrows `work[]` to *current* roles only. Fields: `role`, `org`, optional `start` (four-digit year) / `end` (four-digit year or literal `"present"`; omit if unknown), `summary` (one-line scope), `mission` (stance-led one-liner, e.g. "fighting disinformation"). Consumers reading "what is this user doing now" can read `work[]` alone; consumers wanting a full career timeline read both.
- **`inner_circle[].handles`**: optional map of platform-key → bare handle on each `inner_circle` entry. Typed-recommended keys: `instagram`, `linkedin`, `bluesky`, `twitter`, `github`, `mastodon`, `website`, `email`. Lowercase platform names; bare handles (no leading `@`, no URL) for social platforms; full URI / address for `website` / `email`. Additional unknown keys tolerated per §5.6.

### Privacy note

`identity.yaml` is loaded into every session by every conforming consumer (§6.1). Adding handles for someone other than yourself means *their* public identifiers propagate to every agent context the file reaches: unrelated coding sessions, generated outputs, shared screenshots. Producers SHOULD: (a) include third-party handles only with consent; (b) keep the set minimal (one platform is usually enough); (c) prefer `website` (publicly chosen by the contact) over per-platform handles when both exist; (d) treat `family[]` as off-limits for handles until v1's encrypted-vault story lands. Full text: SPEC.md §5.A under `inner_circle[].handles (v0.3)`.

## Compatibility

**File-level: every v0.2 (and v0.1) `identity.yaml` is a valid v0.3 file unchanged.** No field is renamed or removed. `past_work[]` and `inner_circle[].handles` are both optional unknown-keys-tolerated additions per §5.6.

**Semantic-level: `work[]` narrows from "all roles, mixed" to "current roles only" *when `spec_version` is `"0.3"`*.** This is the one semantic change in v0.3 and the reason this release is not the unqualified "strictly additive" v0.2 was. Consumers MUST branch on `spec_version` to read both legacy and v0.3 files correctly:

| `spec_version` | `work[]` semantics | full career timeline requires |
|---|---|---|
| `"0.1"`, `"0.2"`, absent | mixed (current + past, v0.1 semantics) | reading `work[]` alone |
| `"0.3"` | current-only | reading `work[]` AND `past_work[]` |

**Concrete failure mode a v0.1 / v0.2 consumer hits if it doesn't branch on `spec_version`:** reading a new v0.3 producer's file silently returns *only current roles* under `work[]` and ignores the unknown `past_work[]` per the unknown-key rule. The consumer reports "user has 1 job" when the file actually describes a 20-year career. No error fires. SPEC §5.A makes the branching expectation explicit; this release notes file restates it because the silent-loss failure mode is the load-bearing risk for v0.1 / v0.2 consumers in the wild.

**Producer migration path.** Producers maintaining `spec_version: "0.2"` files MAY upgrade to `0.3` and migrate past roles into `past_work[]`, but are not required to migrate while staying on `0.2`. A file with `spec_version: "0.2"` MUST retain mixed `work[]` semantics until it is rebumped to `0.3`. There is no "auto-migrate" path; the producer flips the version bit when they're ready.

**Installer fallback for files with no `spec_version`:** the Codex / Cursor / Gemini consumer installers now treat a missing `spec_version` as legacy `"0.1"` (mixed `work[]` semantics) and surface a warning recommending the producer add `spec_version: "0.3"` to pin. Previous behaviour assumed the latest spec, which silently broke the `work[]` semantic for legacy files.

**Why ship the semantic change at all** (rather than adding a parallel `current_work[]` field to keep `work[]` semantics frozen)? Considered. Rejected because: (a) the JSON Resume / LinkedIn shape every adopter recognises uses `work[]` for the employment block, so freezing `work[]` to mean "everything" indefinitely fights the convention; (b) `spec_version`-gated semantic narrowing is exactly what `spec_version` exists for (SPEC §5.6 escape hatch), and using the escape hatch for one well-documented case is healthier than accumulating frozen field aliases over future versions; (c) the failure mode (silent omission of historical roles for unaware consumers) degrades to "still gets the current job," which is the most load-bearing facet for the always-loaded tier. None of those reasons cancel the obligation on consumers to branch; they explain why this release prefers a documented narrowing over a frozen field.

## Why these fields

Both arose from the maintainer's lived-in setup, then validated against the canonical identity specs surveyed for v0.2:

- **`past_work[]`** mirrors JSON Resume's `work[]` (employment history) and the LinkedIn "Experience" shape. Resume-shaped data has always carried `startDate`/`endDate`/`summary` because *historical employment is structurally different from a current job title*. v0.1 / v0.2 conflated them because v0.1 was scoped to "name tag" content, not career history. Splitting honours the difference and stops `work[]` from drifting into a partial resume.
- **`inner_circle[].handles`** has no direct analog in vCard / Schema.org / OIDC / FOAF / JSON Resume (those all model the *self*, not the self's contacts). The friction it solves is workflow-specific: when an agent helps the user draft a message to a contact, knowing the contact's preferred platform handle is the difference between "Sarah" and "send Sarah a draft DM on Instagram (`@spearsarah`)." That's the value the always-loaded tier is for.

## What did NOT make the cut

Fields considered but deferred:

- **`education[]` / `honors[]` / `certifications[]`** on `identity.yaml`, mirroring the `past_work[]` shape. Worth a separate v0.4 proposal once a consumer demonstrates value. Currently no `~/.me/` consumer surfaces education context, and the always-loaded tier shouldn't carry data nothing reads.
- **`family[].handles[]`** parity with `inner_circle[].handles`. Family entries currently have no schema beyond `name` + `relationship`; the privacy-warning calculus is heavier for family than for chosen-context contacts. Revisit once v1's encrypted-vault tier exists.
- **`birthdate`** (carried over from v0.2's "did not make the cut" list): still no obvious name-tag value, still deferred.

## Open questions for v0.4

- Should `voice.md` allow optional YAML frontmatter for structured metadata (e.g., `voice_version`) without breaking the prose-not-data rule?
- Does the spec need a "non-conformance" section? What does "this tool doesn't support dot-me" look like, and how does it degrade?
- `education[]` / `honors[]` / `certifications[]` on `identity.yaml`: file as a v0.4 proposal if a consumer surfaces a use case.
- `family[]` schema, including `handles` parity once encrypted-vault lands.
- Conformance test suite (carried from v0.2 deferred list).

## License

MIT. See [LICENSE](LICENSE).
