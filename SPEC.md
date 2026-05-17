# dot-me: Personal Context Spec (v0.2)

**Date:** 2026-05-16
**Status:** RFC, solo-maintained
**Scope:** Schema, load contract, update invariants, and precedence vs existing personal-context layers (AGENTS.md, Codex memories, Claude Code global CLAUDE.md, `~/.agents/profile/user.md`) for a lightweight, file-based personal-context standard at `~/.me/`.
**Driver:** AI tools re-onboard the user in every new project, ticket, subagent, and chat. Twice. They forget *who you are* (name, timezone, dogs, durable context) and they forget *how you want them to work with you* (autonomy level, voice, scope discipline, the calls you already made). AGENTS.md handles project context; vendor memory features handle conversation history; no portable, file-based standard covers either layer of durable personal context. dot-me fills both as the lowest-effort viable answer.

> the personal-context card AI tools read at the door: your name tag and your working agreement.

## 1. What this is

Every new project, every new ticket, every fresh subagent, every fresh chat: your AI tools start with no idea who you are *and* no idea how you want them to work with you. So you re-onboard yourself, twice. You paste a paragraph into CLAUDE.md saying who you are. You paste another about how to write for you. You re-explain your dogs *and* your tolerance for clarifying questions to ChatGPT for the seventh time this week.

dot-me is the file you stop copy-pasting. It carries two layers in three files:

- **Identity layer**: who you are. Stable, vCard-shaped. Lives in `identity.yaml`.
- **Working-agreement layer**: how you want the AI to write for you and work with you. Lives in `voice.md` (prose) and `preferences.yaml` (structured).

Three files at `~/.me/`. Plain YAML and Markdown. Any AI tool can opt in.

## 2. The gap

Most "personal AI" projects in 2026 want to give you a brain. mem0, Letta, Khoj, Rewind: they capture, embed, retrieve, recall. They take hours to set up. They need vector DBs, daemons, capture pipelines. They aim very high.

dot-me aims very low. Its only job is: when an agent starts, it knows your name, your voice, your preferences. That's it.

The persistence problem dot-me solves shows up daily for anyone with multi-project setups. Your home-dir CLAUDE.md gets your dogs right. The ticket-agent in a sibling repo doesn't. The next ChatGPT thread starts blank. The next worktree-spawned subagent forgets your tone. You keep paying the re-onboarding cost.

dot-me is the lowest-effort fix for that cost.

## 3. What dot-me is not

- **Not a brain.** No recall, no embeddings, no retrieval. It's three static files.
- **Not a service.** No daemon, no API, no background process. Read-from-disk-once at session start, done.
- **Not AGENTS.md.** AGENTS.md is the project brief (what this codebase is, what conventions to follow, what tests to run). dot-me is the personal-context card (who the human at the keyboard is and how they want the AI to work with them). They're orthogonal. You SHOULD have both.
- **Not a replacement for per-project memory.** Project memory still has its place: what you discovered debugging that flaky test last Tuesday. dot-me is the layer above project memory: invariant facts about the human, not the project.

## 4. File layout

dot-me content lives at a well-known home-dir path: `~/.me/`. Three content files:

```text
~/.me/
├── identity.yaml      # invariant facts about the user
├── voice.md           # voice profile (tone, lexicon, anti-patterns)
└── preferences.yaml   # likes / favorites / avoid triads
```

These three files are the format. Anything else in `~/.me/` (integrity sidecars, update logs, encrypted vaults) is implementation choice, not part of the spec. Consumers MUST NOT depend on the presence of any file beyond the three above.

## 5. Schema

The three content files split across two layers:

- **§5.A Identity layer**: answers *who you are*. `identity.yaml`. Stable, vCard-aligned.
- **§5.B Working-agreement layer**: answers *how you want the AI to write for you and work with you*. `voice.md` + `preferences.yaml` today; a future `working-style.yaml` file is planned.

Schemas are intentionally loose; most fields are optional, and consumers MUST ignore unknown fields (forward-compat). Conformance at the layer level is addressed in §6.1: consumers MUST disclose which layers they load so adopters can tell layer-aware adoption from layer-skipping adoption.

### 5.A. Identity layer

The identity layer is one file: `identity.yaml`. It carries durable, low-velocity facts about the user (name, timezone, pronouns, what they know about, the family/pets/work surface tools use for rapport and contextual cues). v0.2 aligned this layer with canonical identity specs (vCard RFC 6350, Schema.org Person, JSON Resume, FOAF) so tool implementers can reuse existing schemas instead of inventing a new one.

#### 5.1. `identity.yaml`

```yaml
name: <string>                    # required
preferred_name: <string>          # optional, how to address the user in prose
nickname: <string>                # optional, informal short label (vCard NICKNAME / FOAF foaf:nick)
pronouns: <string>                # optional, e.g. "he/him", "she/her", "they/them"
email: <string>                   # optional, primary contact email (vCard EMAIL / Schema.org email)
website: <URI>                    # optional, canonical homepage (vCard URL / Schema.org url)
avatar: <URI>                     # optional, profile image URI (vCard PHOTO / Schema.org image / OIDC picture)
handle: <@-prefixed string>       # optional, legacy single-handle field; producers SHOULD use `social_profiles` instead
social_profiles:                  # optional, list of social accounts (JSON Resume basics.profiles shape)
  - network: <string>             #   e.g. "GitHub", "Mastodon", "Bluesky", "LinkedIn"
    url: <URI>
blurb: <one-line string>          # optional, short self-description / bio line
headline: <one-line string>       # optional, professional label (JSON Resume basics.label / Schema.org jobTitle)
spec_version: "0.2"               # optional but recommended; pins the schema version
location:
  timezone: <IANA tz string>      # required if location present
  city: <string>                  # optional, free-text city / locality
  country: <ISO 3166-1 alpha-2>   # optional, two-letter country code (e.g. "US", "GB")
languages:                        # optional, BCP 47 language tags (Schema.org knowsLanguage)
  - <bcp47 tag>                   #   e.g. "en", "en-US", "fr"
knows_about:                      # optional, Schema.org knowsAbout semantics (domain expertise, NOT spoken languages)
  - <free-text topic>
work:                             # optional
  - role: <string>
    org: <string>
pets: []                          # optional
family: []                        # optional, may be deferred to v1
inner_circle: []                  # optional, may be deferred to v1
```

Required: `name`. The single strictness elsewhere is `location.timezone`: when `location` is present, the timezone MUST be a valid IANA identifier (e.g., `America/Chicago`). `location.country` SHOULD be ISO 3166-1 alpha-2 when present; `languages` SHOULD be BCP 47 tags when present. Everything else is optional.

**`handle` vs `social_profiles` (v0.2):** v0.1 carried a single opaque `handle` string. v0.2 introduces `social_profiles` as a list of `{network, url}` objects (the shape used by JSON Resume, Schema.org `sameAs`, and vCard `IMPP`/`X-SOCIALPROFILE`). `handle` is retained for backward compatibility (consumers MUST continue to read it) but new producers SHOULD prefer `social_profiles`. When both are present, `social_profiles` is authoritative.

**`languages` vs `knows_about` (v0.2):** Schema.org separates `knowsLanguage` (spoken/written languages) from `knowsAbout` (domain expertise). v0.1 conflated them; v0.2 introduces `languages` as the dedicated field. `knows_about` retains its v0.1 semantics: free-text expertise topics, not languages.

### 5.B. Working-agreement layer

The working-agreement layer carries the behavioral content that moves agent output on every session, not just sessions where identity context happens to surface. Two files today: `voice.md` (prose-shaped, *how the AI should write for you*) and `preferences.yaml` (structured, *what tools and aesthetics you favor*). A future `working-style.yaml` is planned to extend the layer with imperative behavioral defaults (autonomy level, scope discipline, interruption thresholds).

Working-agreement content benefits from a different authoring style than identity content. The execution-time differences documented in §6.6 suggest that prohibitions and hard constraints ("don't ask before doing routine decisions", "always explain irreversible changes before acting") port more reliably across Claude / Codex / Gemini / Cursor than permissions or preferences ("I prefer autonomy"); the latter are easier for a given tool's instruction-application semantics to soften or override. Authors of working-agreement files SHOULD lean imperative. This is maintainer experience to date, not a systematic study, and the format will accommodate corrections from implementers who hit different results in practice.

#### 5.2. `voice.md`

Freeform Markdown. The five section headers below are a recommended convention, not required. When present, consumers MUST treat them as human-readable markers only, not as parseable structure.

```markdown
## Tone & Dimensions
## Mechanics
## Lexicon
## Anti-patterns
## Sample Passages
```

Content within sections is intentionally unstructured; voice is artistic, not enumerable. Consumers reading `voice.md` MUST treat it as plain prose to load into context, not as structured data to parse.

**Authoring tip: name the quiet traits, not just the loud ones.** It's tempting to capture only the traits a reader would notice in 30 seconds (humor, bluntness, hedging). But generation defaults strip whatever isn't named, so unnamed traits that *do* show up in your writing (sincerity, vulnerability, restraint, formality, warmth) quietly disappear from output. If a sample passage of yours has a trait the trait list doesn't mention, that's a gap. Name it.

#### 5.3. `preferences.yaml`

```yaml
tools:        { editor: ..., shell: ..., ... }
aesthetics:   { formality: ..., color_temperature: ..., ... }
media:        { games: { likes: [...] }, movies: { likes: [...] } }
workflow:     { commit_messages: ... }
```

Each top-level key is optional. Nested keys are free-form: `likes`, `favorites`, `avoid` triads work for most categories. A trailing `notes` block accommodates cross-cutting preferences that don't fit a category.

### 5.4. Why three files, not one

The three files have different lifecycles:

- `identity.yaml`: rarely changes (your name, timezone, dogs). Near-static.
- `voice.md`: stable, occasionally refined. Medium velocity.
- `preferences.yaml`: churns (you swap editors, change themes, update the avoid lists).

Separating by lifecycle lets consumers cache the stable parts and re-load the volatile parts independently. As a downstream benefit, this also helps with prompt-cache prefix-stability on providers that offer it, but lifecycle is the honest reason; cache is a side-effect. A combined `me.md` would force all three to share a cache fate and re-invalidate the stable parts whenever the volatile parts changed.

### 5.5. Unknown keys

Consumers MUST ignore unknown keys silently. Producers MAY add new keys at any time without coordinating with consumers. This is the entire versioning policy v0.1 has: additive-only, ignore-what-you-don't-know.

For the rare case where a breaking change becomes necessary in a future spec version, `spec_version` (§5.1) is the escape hatch. Consumers SHOULD branch on `spec_version` when handling fields that have changed semantics between versions.

## 6. Load contract

dot-me content is meant to be loaded into the agent's instruction context at session start. It is NOT a runtime tool surface.

### 6.1. Load tiers (descriptive, not normative)

- `identity.yaml`: load every session. Small, stable, near-universal value.
- `voice.md`: load when the agent generates user-facing text (writing, replying, drafting, generating commit messages). A math-only or pure-code-fix context can skip it.
- `preferences.yaml`: load when the agent makes recommendations (tool choice, design direction, copy tone). A strict bug-fix context can skip it.

**Conformance disclosure (v0.2+).** A consumer MAY load any subset of files, but it MUST disclose which layers it loads (identity / working-agreement / both) and, optionally, which files within each layer. The disclosure SHOULD be made in the consumer's public documentation (README, install guide, or equivalent adopter-facing surface) and MAY also be surfaced at runtime (e.g., a verbose-mode banner or startup log line). Adopters use this disclosure to predict cross-tool behavior: a tool that loads only the identity layer will not honor the user's voice or working-agreement rules, and adopters must be able to tell that from the tool's documentation rather than discovering it through behavior drift. A consuming tool that only reads `identity.yaml` is still a valid dot-me consumer at the identity-layer level; it is NOT a full dot-me consumer.

### 6.2. Where in the instruction hierarchy

dot-me content goes in **system or developer-tier instructions**, not user-tier messages.

- On the OpenAI Responses API, that means the `system` or `developer` role; these outrank user-role instructions and are not invertible by user input.
- On Anthropic's API, that means the `system` prompt block.
- On tools without a hierarchy, the highest-priority context the tool exposes (e.g., a global preamble, a system rule, an `instructions:` field).

dot-me describes who the user is. The user themselves can't be relied on to assert that, so system/developer-tier is correct.

### 6.3. Read-at-startup, not retrievable

dot-me content MUST be loaded into the context at session start. Consumers MUST NOT add a new model-callable surface that re-fetches dot-me content on demand mid-session: no tool, no MCP resource, no skill, no plugin command that returns `~/.me/` content as a tool result.

**Scope of "retrievable":** This rule concerns *new surfaces a consumer adds* (a `read_user_identity` tool, an `me://` MCP resource, etc.). It does not require the underlying filesystem to be unreachable; `~/.me/identity.yaml` lives on disk, and so does any inlined copy a consumer writes (e.g., `~/.codex/AGENTS.md`). A generic filesystem tool (a `Bash` or `Read` tool with `$HOME` access) can always re-read either path. That exposure is a property of the user's tool-permission setup, not the dot-me consumer.

The threat the rule blocks is exfiltration via prompt injection through *dot-me-specific* tools: a malicious project's `CLAUDE.md` or `AGENTS.md` invoking a hypothetical `get_user_voice()` MCP call. Consumers that need to expose user context to the model SHOULD inline it into instructions at session start (per §6.4) rather than wiring an on-demand surface. Generic-filesystem-tool exfiltration is an orthogonal concern that user-level tool sandboxing addresses; see Appendix A.

### 6.4. Consumer implementation patterns

There are two practical ways to wire dot-me into a tool's startup chain:

1. **By reference (`@`-include).** If the host config format supports filesystem includes (e.g., Claude Code's `CLAUDE.md` resolving `@~/.me/identity.yaml`), the consumer SHOULD prefer this: single source of truth, edits in `~/.me/` propagate without re-running the installer.
2. **By inline copy with idempotent markers.** If the host has no include mechanism (e.g., Codex CLI as of May 2026, whose `AGENTS.md` reader treats `@<path>` as literal text), the consumer SHOULD inline the file contents between named delimiters (e.g., `<!-- dot-me:begin -->` / `<!-- dot-me:end -->`) and provide an installer that replaces the block in place. Consumers MUST preserve content outside the markers and MUST provide a clean uninstall path.

Inline consumers SHOULD also surface the host's instruction-budget cap (e.g., Codex's combined 32 KiB across the AGENTS.md chain) and offer optional modes that omit heavier files like `voice.md` when budget is tight.

### 6.5. Prompt-cache guidance (advisory)

Stable content (identity, voice) belongs before volatile content (preferences) in any cached system-prompt prefix. Mechanics differ across providers. As of May 2026, Anthropic uses explicit `cache_control` breakpoints with provider-specified minimum-token thresholds; OpenAI uses automatic exact-prefix caching with a 1024-token minimum; others vary. Provider mechanics and thresholds change across API versions; verify current behavior before relying on specific numbers. Consumers SHOULD bundle dot-me content with other stable system content to clear provider cache minimums, since the three files alone are usually too small to cache independently.

Specific cache annotations are the consumer's responsibility, not the spec's. The spec only ranks files by stability.

### 6.6. Portability limits at execution time

dot-me content is portable as text. Its *effect* is not uniformly portable, because consuming tools differ at the execution-mode layer in ways the format cannot reach.

Example: the working-agreement instruction *"When you make a change, always explain what you changed and why before showing any code."* placed identically in each tool's user-global config yields four different observable behaviors:

- **Claude Code (`CLAUDE.md`):** followed in conversational mode; in non-interactive `-p` mode, the explanation is suppressed by the terminal harness even though the instruction fires internally.
- **Codex CLI (`~/.codex/AGENTS.md`):** followed in TUI mode; in `--full-auto --quiet`, explanations are suppressed at the infrastructure level regardless of the AGENTS.md instruction.
- **Cursor (User Rules / `.cursor/rules/*.mdc`):** in agent mode the explanation appears in the thinking pane but not necessarily in the diff view the user watches.
- **Gemini CLI (`GEMINI.md`):** followed consistently in interactive mode.

The instruction text is identical and parsed similarly by all four. Outcomes diverge because each tool's execution-mode architecture handles suppression, surfacing, and rendering differently. Other behavioral divergences with the same shape: instruction-budget thresholds (Claude Code's ~150–200 soft cap, Gemini's recursive concatenation, Codex's 32 KiB chain limit), path-scoped rule application (Claude Code's `@include` + path-scope vs. Codex/AGENTS.md applying globally), and self-modifying memory (Claude Code can write to its own context; no other tool does).

**Adopter expectation.** Consumers and adopters SHOULD expect dot-me to give them more consistent *instruction parsing* across tools (the format is plain text, the working-agreement file ports cleanly). They SHOULD NOT expect identical *behavior* across tools, because execution-mode quirks downstream of parsing are out of scope for any text-based personal-context format. The bounded determinism claim is the only honest one.

**Authoring implication.** Working-agreement content written as prohibitions and hard constraints survives more execution modes than content written as preferences. Where you can phrase a rule as "don't X" or "always X", do; the imperative form has the best cross-vendor survival rate. Preferences are still useful (they shape default behavior in interactive modes) but expect them to be the first thing tools drop under context-budget pressure.

## 7. Update invariants

dot-me files are user-managed. When updating any file, producers MUST hold:

- **Atomicity.** Partial writes are unacceptable. Write-then-rename (or equivalent) is the floor. A consumer parsing a half-written file is a bug; a producer that allows it is the bug's cause.
- **Integrity refresh.** If a producer maintains an integrity sidecar (Appendix C), that sidecar MUST be regenerated atomically with the file change. Otherwise stale hashes false-positive on every load.
- **Append-only provenance** (recommended). A separate `.updates.log` capturing timestamp + source + summary per change is useful for tamper triage. Not normative.

The reference implementation provides a `/me` umbrella slash command (`/me add`, `/me show`, `/me edit`, `/me check`, `/me init`, and bare `/me` for session-scan) that handles all three invariants. It is one of many possible producers, not part of the format.

## 8. Precedence and portability

### 8.1. Relationship to other personal-context layers

dot-me is **opt-in import**, not auto-discovered. Consumers MUST NOT load `~/.me/` unless the user explicitly enables it (via configuration, a CLAUDE.md `@include`, an `--import` flag, or equivalent). This makes dot-me non-clashing with existing layers:

- Codex `~/.codex/AGENTS.md` (auto-loaded global personal config)
- Codex `~/.codex/memories/` (managed memory layer)
- Cursor Settings → Rules (UI-managed personal rules)
- Claude Code `~/.claude/CLAUDE.md` (auto-loaded global; can `@include` dot-me files)

A tool with its own personal-context layer SHOULD treat dot-me as supplementary, not as a replacement. Precedence on conflicts: project-level instructions (project `AGENTS.md`, project `CLAUDE.md`) outrank dot-me, because the project knows its own rules better than the user does.

### 8.2. Relationship to AGENTS.md specifically

AGENTS.md is a cross-tool standard for project + personal coding-style guidance; see [`agentsmd/agents.md`](https://github.com/agentsmd/agents.md) for current scope and adopter list. The format has no schema for identity, voice, or preferences (open issue [`agentsmd/agents.md#91`](https://github.com/agentsmd/agents.md/issues/91)). dot-me fills that gap.

A tool that consumes both SHOULD load dot-me as the person-level layer first, then apply AGENTS.md as the project-level layer over it.

### 8.3. Relationship to `~/.agents/profile/user.md` (dotstandards.info)

[dotstandards.info](https://dotstandards.info/standards/agents/) defines `~/.agents/profile/user.md` as a freeform Markdown file for general user information. Scope overlaps with dot-me. Differences as of v0.1 of both drafts:

- dot-me splits structured fields (identity, preferences) from prose (voice) using YAML and Markdown respectively; `.agents/profile/user.md` is single-file freeform Markdown.
- dot-me's `~/.me/` is shorter to type and matches `~/.ssh/` / `~/.gitconfig` convention; `~/.agents/` is parallel to the project-scoped `.agents/` directory the broader dotstandards.info covers.

A future spec revision may define a compatibility profile (e.g., publish a dot-me-shaped `user.md` for tools that only look in `~/.agents/profile/`). Out of scope for this version.

### 8.4. Portability limits

`~/.me/` is a home-directory standard. It does not portably reach:

- Cloud-hosted agents (Codex Cloud, GitHub-backed agent tasks): no real home directory.
- Container sandboxes without a mounted home volume.
- Browser-based agent surfaces.
- Windows clients without a unix-style home (use `%USERPROFILE%\.me\` or equivalent).

A conforming consumer in a no-home environment SHOULD provide an alternate import path (env var, configured directory, mounted volume) and document it. dot-me is filesystem-first. It is not magic.

## Appendix A: Threat model summary

Documented 2026 attack classes against personal-context files: local file tamper (filesystem access modifying `identity.yaml` to inject persistent instructions) and exfiltration via prompt injection (a malicious repo's `CLAUDE.md` instructing the agent to read and exfiltrate `~/.me/voice.md`). The §6.3 read-at-startup-not-retrievable rule is the most effective mitigation against the second class. Optional integrity sidecars (Appendix C) cover the first.

See current threat-modeling literature on agentic memory compromise and instruction-injection for the underlying research; the categories above are the load-bearing ones for `~/.me/`.

## Appendix B: Comparison

|                   | dot-me                              | AGENTS.md (project)    | Cursor rules (project)        | `~/.codex/AGENTS.md` (user) | ChatGPT Memory / mem0       |
| ----------------- | ----------------------------------- | ---------------------- | ----------------------------- | --------------------------- | --------------------------- |
| Subject           | the human (identity + agreement)    | the project            | the project                   | the human (Codex-only)      | the conversation history    |
| Filesystem scope  | user (`~/`)                         | project (`./`)         | project (`.cursor/rules/`)    | user (`~/.codex/`)          | none (vendor service)       |
| Format            | YAML + Markdown                     | freeform Markdown      | `.mdc` (front-matter + MD)    | freeform Markdown           | proprietary, vendor-managed |
| Cross-vendor      | yes (filesystem + consumers)        | yes (multi-tool)       | no (Cursor-only)              | no (Codex-only)             | no (vendor-locked)          |
| Load model        | read at session start               | read at session start  | scope-on-glob, `alwaysApply`  | read at session start       | retrieved on demand         |
| Infrastructure    | none                                | none                   | none                          | none                        | service / vector DB         |

The combination of user-level scope and cross-vendor portability is the niche dot-me claims. Codex's `~/.codex/AGENTS.md` is the closest analog as a user-level behavioral-config file but ships with Codex only; Cursor rules and AGENTS.md are project-scoped. No prior artifact in the developer-tooling ecosystem positions itself as a user-level, cross-vendor, behavioral working agreement.

## Appendix C: Hardening sketch (optional)

Producers concerned about local tamper detection MAY maintain integrity files alongside the schema:

- `.integrity`: a SHA-256 hash baseline of the three content files, regenerated on every legitimate write.
- Signed git commits in the `~/.me/` directory: covers append-only history; tampering is detectable post-hoc via `git log --show-signature`.
- A `SessionStart`-style hook that compares actual hashes to baseline at every session start and warns on drift.

These are not part of the format. A consumer MUST work correctly whether or not they exist. The hash + signed-commit + session-start-drift design is one workable answer to the local-tamper threat class; there are others.

## Out of scope (deferred)

- Encrypted vault (sops/age). The reference implementation reserves a directory for it; not part of this version.
- Free-text relationship notes for `family` / `inner_circle` (deferred to v1, conditional on encrypted-vault availability).
- Multi-user or per-org variants.
- Selective per-project loading (load only `voice.md` for repo X).
- Conformance test suite.
- Reference implementations beyond the author's `~/.me/` setup and Claude Code integration.
- MCP-resource architecture (could expose `~/.me/` files as resources; conflicts with §6.3 read-at-startup rule).
- Compatibility profile for `~/.agents/profile/user.md` (see §8.3).

## Open questions for v0.3

- Should `voice.md` allow optional YAML frontmatter for structured metadata (e.g., `voice_version`) without breaking the prose-not-data rule?
- Does the spec need a "non-conformance" section? What does "this tool doesn't support dot-me" look like, and how does it degrade?
- Native integrations: Codex hook, Cursor extension, Gemini CLI loader. Which lands first, and what's the minimum surface area for each?

## Implementation history

Design rationale, adversarial-review thread, and migration design for the v0.1 reference implementation live in the maintainer's home-lab repo: [`personal-context-design.md`](https://github.com/thebestmensch/home-lab/blob/main/docs/superpowers/specs/2026-05-05-personal-context-design.md). That document is the design history; this file is the public spec.

**v0.2 (2026-05-16):** Adds seven optional identity fields to align `identity.yaml` with the baseline shape used by canonical identity specs (vCard RFC 6350, Schema.org Person, OIDC standard claims, FOAF, JSON Resume): `nickname`, `email`, `website`, `avatar`, `headline`, `social_profiles[]` (preferred over the legacy single `handle`), `languages` (split out from `knows_about` per Schema.org's `knowsLanguage`/`knowsAbout` distinction), and `location.city` + `location.country`. All additive; v0.1 files remain valid v0.2 files.
