# dot-me — Personal Context Spec (v0.1)

**Date:** 2026-05-05
**Status:** RFC, solo-maintained
**Scope:** Schema, load contract, update invariants, and precedence vs existing personal-context layers (AGENTS.md, Codex memories, Claude Code global CLAUDE.md, `~/.agents/profile/user.md`) for a lightweight, file-based personal-context standard at `~/.me/`.
**Driver:** AI tools re-onboard the user in every new project, ticket, subagent, and chat. There is no portable, file-based standard for "who is the human at the keyboard" — AGENTS.md handles project context, vendor memory features handle conversation history, neither covers durable personal identity. dot-me fills that gap as the lowest-effort viable answer.

> a name tag at the door for AI tools.

## 1. What this is

Every new project, every new ticket, every fresh subagent, every fresh chat — your AI tools start with no idea who you are. So you re-onboard yourself. You paste a paragraph into CLAUDE.md. You copy three lines about your tone into a new repo. You re-explain your dogs to ChatGPT for the seventh time this week.

dot-me is the file you stop copy-pasting.

Three files at `~/.me/`. Plain YAML and Markdown. Any AI tool can opt in.

## 2. The gap

Most "personal AI" projects in 2026 want to give you a brain. mem0, Letta, Khoj, Rewind — they capture, embed, retrieve, recall. They take hours to set up. They need vector DBs, daemons, capture pipelines. They aim very high.

dot-me aims very low. Its only job is: when an agent starts, it knows your name, your voice, your preferences. That's it.

The persistence problem dot-me solves shows up daily for anyone with multi-project setups. Your home-dir CLAUDE.md gets your dogs right. The ticket-agent in a sibling repo doesn't. The next ChatGPT thread starts blank. The next worktree-spawned subagent forgets your tone. You keep paying the re-onboarding cost.

dot-me is the lowest-effort fix for that cost.

## 3. What dot-me is not

- **Not a brain.** No recall, no embeddings, no retrieval. It's three static files.
- **Not a service.** No daemon, no API, no background process. Read-from-disk-once at session start, done.
- **Not AGENTS.md.** AGENTS.md is the project brief — what this codebase is, what conventions to follow, what tests to run. dot-me is the name tag — who is the human at the keyboard. They're orthogonal. You SHOULD have both.
- **Not a replacement for per-project memory.** Project memory still has its place — what you discovered debugging that flaky test last Tuesday. dot-me is the layer above project memory: invariant facts about the human, not the project.

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

Each file has a defined shape. Schemas are intentionally loose — most fields are optional, and consumers MUST ignore unknown fields (forward-compat).

### 5.1. `identity.yaml`

```yaml
name: <string>                    # required
preferred_name: <string>          # optional
pronouns: <string>                # optional, e.g. "he/him", "she/her", "they/them"
handle: <@-prefixed string>       # optional, primary social handle (e.g. "@thebestmensch")
blurb: <one-line string>          # optional, short self-description / bio line
spec_version: "0.1"               # optional but recommended; pins the schema version
location:
  timezone: <IANA tz string>      # required if location present
knows_about:                      # optional, schema.org/knowsAbout semantics
  - <free-text topic>
work:                             # optional
  - role: <string>
    org: <string>
pets: []                          # optional
family: []                        # optional, may be deferred to v1
inner_circle: []                  # optional, may be deferred to v1
```

Required: `name`. The single strictness elsewhere is `location.timezone` — when `location` is present, the timezone MUST be a valid IANA identifier (e.g., `America/Chicago`). Everything else is optional.

### 5.2. `voice.md`

Freeform Markdown. The five section headers below are a recommended convention, not required. When present, consumers MUST treat them as human-readable markers only — not as parseable structure.

```markdown
## Tone & Dimensions
## Mechanics
## Lexicon
## Anti-patterns
## Sample Passages
```

Content within sections is intentionally unstructured — voice is artistic, not enumerable. Consumers reading `voice.md` MUST treat it as plain prose to load into context, not as structured data to parse.

### 5.3. `preferences.yaml`

```yaml
tools:        { editor: ..., shell: ..., ... }
aesthetics:   { formality: ..., color_temperature: ..., ... }
media:        { games: { likes: [...] }, movies: { likes: [...] } }
workflow:     { commit_messages: ... }
```

Each top-level key is optional. Nested keys are free-form: `likes`, `favorites`, `avoid` triads work for most categories. A trailing `notes` block accommodates cross-cutting preferences that don't fit a category.

### 5.4. Why three files, not one

The three files have different lifecycles:

- `identity.yaml` — rarely changes (your name, timezone, dogs). Near-static.
- `voice.md` — stable, occasionally refined. Medium velocity.
- `preferences.yaml` — churns (you swap editors, change themes, update the avoid lists).

Separating by lifecycle lets consumers cache the stable parts and re-load the volatile parts independently. As a downstream benefit, this also helps with prompt-cache prefix-stability on providers that offer it — but lifecycle is the honest reason; cache is a side-effect. A combined `me.md` would force all three to share a cache fate and re-invalidate the stable parts whenever the volatile parts changed.

### 5.5. Unknown keys

Consumers MUST ignore unknown keys silently. Producers MAY add new keys at any time without coordinating with consumers. This is the entire versioning policy v0.1 has — additive-only, ignore-what-you-don't-know.

For the rare case where a breaking change becomes necessary in a future spec version, `spec_version` (§5.1) is the escape hatch. Consumers SHOULD branch on `spec_version` when handling fields that have changed semantics between versions.

## 6. Load contract

dot-me content is meant to be loaded into the agent's instruction context at session start. It is NOT a runtime tool surface.

### 6.1. Load tiers (descriptive, not normative)

- `identity.yaml` — load every session. Small, stable, near-universal value.
- `voice.md` — load when the agent generates user-facing text (writing, replying, drafting, generating commit messages). A math-only or pure-code-fix context can skip it.
- `preferences.yaml` — load when the agent makes recommendations (tool choice, design direction, copy tone). A strict bug-fix context can skip it.

A consuming tool that only reads `identity.yaml` is still a valid consumer. Tool builders are encouraged to document which files they load.

### 6.2. Where in the instruction hierarchy

dot-me content goes in **system or developer-tier instructions**, not user-tier messages.

- On the OpenAI Responses API, that means the `system` or `developer` role — these outrank user-role instructions and are not invertible by user input.
- On Anthropic's API, that means the `system` prompt block.
- On tools without a hierarchy, the highest-priority context the tool exposes (e.g., a global preamble, a system rule, an `instructions:` field).

dot-me describes who the user is. The user themselves can't be relied on to assert that — system/developer-tier is correct.

### 6.3. Read-at-startup, not retrievable

dot-me content MUST be loaded into the context at session start. It MUST NOT be exposed as model-callable retrievable content (a tool, an MCP resource, a filesystem path the agent has standing permission to read on demand) after startup.

The threat is exfiltration via prompt injection — a malicious project's `CLAUDE.md` or `AGENTS.md` instructing the agent to read and exfiltrate `~/.me/voice.md`. Read-at-startup-not-retrievable is the single most effective mitigation. See Appendix A.

### 6.4. Prompt-cache guidance (advisory)

Stable content (identity, voice) belongs before volatile content (preferences) in any cached system-prompt prefix. Mechanics differ across providers — as of May 2026, Anthropic uses explicit `cache_control` breakpoints with provider-specified minimum-token thresholds; OpenAI uses automatic exact-prefix caching with a 1024-token minimum; others vary. Provider mechanics and thresholds change across API versions — verify current behavior before relying on specific numbers. Consumers SHOULD bundle dot-me content with other stable system content to clear provider cache minimums, since the three files alone are usually too small to cache independently.

Specific cache annotations are the consumer's responsibility, not the spec's. The spec only ranks files by stability.

## 7. Update invariants

dot-me files are user-managed. When updating any file, producers MUST hold:

- **Atomicity.** Partial writes are unacceptable. Write-then-rename (or equivalent) is the floor. A consumer parsing a half-written file is a bug; a producer that allows it is the bug's cause.
- **Integrity refresh.** If a producer maintains an integrity sidecar (Appendix C), that sidecar MUST be regenerated atomically with the file change. Otherwise stale hashes false-positive on every load.
- **Append-only provenance** (recommended). A separate `.updates.log` capturing timestamp + source + summary per change is useful for tamper triage. Not normative.

The reference implementation provides a `/me` umbrella slash command (`/me add`, `/me show`, `/me edit`, `/me check`, `/me init`, and bare `/me` for session-scan) that handles all three invariants. It is one of many possible producers — not part of the format.

## 8. Precedence and portability

### 8.1. Relationship to other personal-context layers

dot-me is **opt-in import**, not auto-discovered. Consumers MUST NOT load `~/.me/` unless the user explicitly enables it (via configuration, a CLAUDE.md `@include`, an `--import` flag, or equivalent). This makes dot-me non-clashing with existing layers:

- Codex `~/.codex/AGENTS.md` (auto-loaded global personal config)
- Codex `~/.codex/memories/` (managed memory layer)
- Cursor Settings → Rules (UI-managed personal rules)
- Claude Code `~/.claude/CLAUDE.md` (auto-loaded global; can `@include` dot-me files)

A tool with its own personal-context layer SHOULD treat dot-me as supplementary, not as a replacement. Precedence on conflicts: project-level instructions (project `AGENTS.md`, project `CLAUDE.md`) outrank dot-me, because the project knows its own rules better than the user does.

### 8.2. Relationship to AGENTS.md specifically

AGENTS.md is a cross-tool standard for project + personal coding-style guidance — see [`agentsmd/agents.md`](https://github.com/agentsmd/agents.md) for current scope and adopter list. The format has no schema for identity, voice, or preferences (open issue [`agentsmd/agents.md#91`](https://github.com/agentsmd/agents.md/issues/91)). dot-me fills that gap.

A tool that consumes both SHOULD load dot-me as the person-level layer first, then apply AGENTS.md as the project-level layer over it.

### 8.3. Relationship to `~/.agents/profile/user.md` (dotstandards.info)

[dotstandards.info](https://dotstandards.info/standards/agents/) defines `~/.agents/profile/user.md` as a freeform Markdown file for general user information. Scope overlaps with dot-me. Differences as of v0.1 of both drafts:

- dot-me splits structured fields (identity, preferences) from prose (voice) using YAML and Markdown respectively; `.agents/profile/user.md` is single-file freeform Markdown.
- dot-me's `~/.me/` is shorter to type and matches `~/.ssh/` / `~/.gitconfig` convention; `~/.agents/` is parallel to the project-scoped `.agents/` directory the broader dotstandards.info covers.

A future spec revision may define a compatibility profile (e.g., publish a dot-me-shaped `user.md` for tools that only look in `~/.agents/profile/`). Out of scope for v0.1.

### 8.4. Portability limits

`~/.me/` is a home-directory standard. It does not portably reach:

- Cloud-hosted agents (Codex Cloud, GitHub-backed agent tasks) — no real home directory.
- Container sandboxes without a mounted home volume.
- Browser-based agent surfaces.
- Windows clients without a unix-style home (use `%USERPROFILE%\.me\` or equivalent).

A conforming consumer in a no-home environment SHOULD provide an alternate import path (env var, configured directory, mounted volume) and document it. dot-me is filesystem-first. It is not magic.

## Appendix A — Threat model summary

Documented 2026 attack classes against personal-context files: local file tamper (filesystem access modifying `identity.yaml` to inject persistent instructions) and exfiltration via prompt injection (a malicious repo's `CLAUDE.md` instructing the agent to read and exfiltrate `~/.me/voice.md`). The §6.3 read-at-startup-not-retrievable rule is the most effective mitigation against the second class. Optional integrity sidecars (Appendix C) cover the first.

See current threat-modeling literature on agentic memory compromise and instruction-injection for the underlying research; the categories above are the load-bearing ones for `~/.me/`.

## Appendix B — Comparison

|                   | dot-me                  | AGENTS.md              | ChatGPT Memory / mem0       |
| ----------------- | ----------------------- | ---------------------- | --------------------------- |
| Subject           | the human               | the project            | the conversation history    |
| Filesystem scope  | user (`~/`)             | project (`./`)         | none (vendor service)       |
| Format            | YAML + Markdown         | freeform Markdown      | proprietary, vendor-managed |
| Portability       | filesystem              | filesystem (in-repo)   | locked to vendor            |
| Load model        | read at session start   | read at session start  | retrieved on demand         |
| Infrastructure   | none                    | none                   | service / vector DB         |

## Appendix C — Hardening sketch (optional)

Producers concerned about local tamper detection MAY maintain integrity files alongside the schema:

- `.integrity` — a SHA-256 hash baseline of the three content files, regenerated on every legitimate write.
- Signed git commits in the `~/.me/` directory — covers append-only history; tampering is detectable post-hoc via `git log --show-signature`.
- A `SessionStart`-style hook that compares actual hashes to baseline at every session start and warns on drift.

These are not part of the format. A consumer MUST work correctly whether or not they exist. The hash + signed-commit + session-start-drift design is one workable answer to the local-tamper threat class — there are others.

## Out of scope (deferred)

- Encrypted vault (sops/age). The reference implementation reserves a directory for it; not part of v0.1.
- Free-text relationship notes for `family` / `inner_circle` (deferred to v1, conditional on encrypted-vault availability).
- Multi-user or per-org variants.
- Selective per-project loading (load only `voice.md` for repo X).
- Conformance test suite.
- Reference implementations beyond the author's `~/.me/` setup and Claude Code integration.
- MCP-resource architecture (could expose `~/.me/` files as resources; conflicts with §6.3 read-at-startup rule for v0.1).
- Compatibility profile for `~/.agents/profile/user.md` (see §8.3).

## Open questions for v0.2

- Should `voice.md` allow optional YAML frontmatter for structured metadata (e.g., `voice_version`) without breaking the prose-not-data rule?
- Does the spec need a "non-conformance" section — what does "this tool doesn't support dot-me" look like, and how does it degrade?
- Native integrations: Codex hook, Cursor extension, Gemini CLI loader. Which lands first, and what's the minimum surface area for each?

## Implementation history

Design rationale, adversarial-review thread, and migration design for the v0.1 reference implementation live in the maintainer's home-lab repo: [`personal-context-design.md`](https://github.com/thebestmensch/home-lab/blob/main/docs/superpowers/specs/2026-05-05-personal-context-design.md). That document is the design history; this file is the public spec.
