# ADR 0001 — Default voice exposure: compact-always, full-lazy

**Status:** Accepted (v0.4.0, 2026-06-18)
**Ticket:** JM-251
**Supersedes:** the implicit v0.1–v0.3 contract where voice loading was conditional-only.

## Context

dot-me's load contract (§6.1) auto-loads `identity.yaml` every session and loads
`voice.md` *conditionally* — only when the agent expects to generate user-facing text.
That conditional load fails silently in three cases:

1. The task isn't obviously prose at the prompt level ("pick a tagline" is a copy
   decision wearing a config-pick costume).
2. The agent skips the cue under context-budget pressure (long session, parallel work,
   post-compaction resume).
3. The consumer has no skill-discovery semantics to fire an on-demand load.

In every case the agent has the user's full identity and zero voice signal, so the first
draft defaults to model house style (corporate, em-dash-heavy, "It's worth noting
that..."). Nothing surfaces the miss — the output just isn't the user's voice. Validated
2026-05-17 (a bio-rewrite session where the agent never loaded voice and the user had to
re-anchor mid-task).

The root cause is the spec, not any one implementation: conditional loading assumes the
agent *notices* it needs voice, and that assumption breaks under the conditions above.

## Decision

Adopt **compact-always, full-lazy** as the default voice exposure, implemented as two
composable layers:

1. **`voice.compact.md`** (spec layer, all consumers): an optional ~30-line derived
   extract of `voice.md` carrying the identity-invariant rules and loudest AI-speak
   tells. Always-loaded (like `identity.yaml`) for ~2 KB, so the floor is never "zero
   voice." Derived companion, not a fifth core file — same status as `.integrity`.
2. **Prompt-trigger enforcement hook** (consumer layer, Claude Code reference): a
   `UserPromptSubmit` hook that injects the *full* `voice.md` when it detects
   prose-generation intent. The ceiling on top of the floor.

The full `voice.md` stays the deep load — fired for real prose work, not every session.

## Alternatives considered

- **Auto-load full `voice.md` every session.** Solves the silent failure but costs ~20 KB
  per session for a signal most sessions don't use. Rejected as cost-disproportionate.
- **A fifth core content file.** Would break "these four files are the format" (§4) and
  the additive-superset guarantee. The companion is derived from an existing core file,
  so it belongs in the implementation-choice tier, not the format's spine.
- **YAML frontmatter on `voice.md`.** Orthogonal — frontmatter is metadata about the
  file, not a separately-loadable lightweight payload. Doesn't give you "load 2 KB
  without loading 20 KB." Left as an open v0.5 question.
- **Hook-only, no spec change.** Cheapest to ship but non-portable: each consumer needs
  its own hook, and non-CC consumers stay blind. Rejected as the *sole* answer; kept as
  the optional ceiling.

## §6.3 compliance (load-bearing)

The enforcement hook MUST inject voice content into the instruction context (harness-side
assembly, the same tier as session-start loading). It MUST NOT satisfy the trigger by
exposing a new model-callable surface returning `~/.me/` content as a tool result — that
is the exact exfiltration vector §6.3 prohibits. The distinction is *who pulls the
content*: the harness (allowed) vs. the model deciding to call a fetch tool (forbidden).
The reference hook prints to stdout, which Claude Code folds into context — compliant.

## Consequences

- **Positive:** prose tasks get a voice floor on every session, portably (any consumer
  can load a 2 KB file at startup). The expensive full load is reserved for when it's
  actually needed. The enforcement hook gives Claude Code a belt-and-suspenders ceiling.
- **Cost — drift:** a derived file can go stale, silently shipping outdated voice signal.
  Bounded by: (a) the full `voice.md` is authoritative on conflict; (b) the `/me`
  producer keeps the compact in sync by convention. Automated generation is deferred to
  v0.5 (tracked in SPEC.md open questions) precisely because drift is the one structural
  risk this design carries.
- **Integrity:** the always-loaded compact file joins the `.integrity` baseline — an
  always-loaded file is the same tamper surface as `identity.yaml`.
- **Conformance:** strictly additive. Producers that skip the compact file and consumers
  that don't load it both stay fully conformant.
