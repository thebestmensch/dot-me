# Rocks System — Design Spec

> **Status:** reference design layered on top of dot-me. The rocks system is a per-user productivity layer that uses dot-me's well-known `~/.me/` path as its storage anchor. It is not part of the dot-me core spec (`SPEC.md`); consumers and dot-me users are not required to implement or adopt it. See [Open question: scope](#open-question-scope-of-this-spec-in-the-oss-repo).

## Problem

Parallel agent sessions across workspaces (multiple repos, organizations, projects) ship a lot of work each day. The "big rocks" — outcome-themed initiatives that span multiple tickets, sometimes across workspaces, often ill-fit for an issue tracker's taxonomy — get lost in the firehose. Users end the day uncertain whether the things they actually meant to land got landed.

Examples of rocks (not tickets, not projects):
- "Ship the next iteration of onboarding to TestFlight for QA"
- "Wrap up any in-flight platform work so we can onboard beta testers"

## Out of Scope

- Issue-tracker taxonomy (Initiatives, Projects, Epics) — wrong fit for daily outcome themes
- Per-session writes to the rocks file (single-writer principle; idempotent re-eval only)
- Replacing or modifying any existing daily-recap command — keeps current behavior, separate concern

## File Format

Path: `<rocks-dir>/YYYY-MM-DD.md` (recommended: `~/.me/rocks/YYYY-MM-DD.md` for users who already have a dot-me directory)

```markdown
---
date: 2026-05-18
---

# Rocks

## Rock 1: <one-line outcome statement>
- Done when: <objective condition>
- Tickets: <optional, comma-sep issue refs covering this rock>
- Status: <eval output: untouched | progressed | done | blocked>
- Related: <git/PR/issue refs from eval>

## Rock 2: ...

## Carryover Notes
- <freeform notes from previous days that didn't ship>
```

Frontmatter enables future querying. Plain Markdown so the user can read and edit directly.

### Issue-tracker linkage (optional, not required)

The `Tickets:` line is a soft pointer. A rock may have:
- **Zero tickets** — themes like "Finish onboarding" or "Wrap platform work for beta testers" routinely span work that never gets ticketed. Don't fabricate tickets to satisfy the field; omit the line.
- **Partial coverage** — some sub-work ticketed, some not. List what exists; don't gate the rock on full coverage.
- **Full coverage** — every meaningful chunk maps to an issue ref. Common for engineering-heavy rocks.

The eval pass uses ticket refs as additional signal sources when present (cross-references state transitions), but absence of the field never downgrades status. Rocks remain primary; tickets are bookkeeping.

### Promotion: rock → tracker Project

When a rock carries forward 3+ days *and* has 2+ ticket refs, it's structurally a Project, not a daily theme. Suggest at carryover time (`<workspace>-rocks-new` § 2 guidance): "This rock has carried 4 days with refs ABC-201, ABC-205, ABC-208 — consider promoting to a tracker Project so the issues nest under shipped scope, and let the rock become a daily pointer to the Project."

This is a *prompt*, not an enforcement. Some rocks legitimately carry without ticket gravity (research, ops drift, life work).

## Components

> **Naming convention.** The command names below use `<workspace>-` as a placeholder prefix (e.g. `<workspace>-rocks`, `<workspace>-wrap`). Consumers pick a prefix that matches their host environment — a per-user prefix, a project name, or no prefix at all. Names are illustrative, not normative.

### 1. SessionStart hook (global)

Location: the host agent runtime's SessionStart hook surface (e.g. `~/.claude/settings.json` hooks block for Claude Code).

- On every session start, reads `<rocks-dir>/YYYY-MM-DD.md` if it exists
- Injects rock titles + done-conditions into the session's context
- Silent no-op when file is missing
- Cost: ~200 tokens per session

Purpose: every session knows the rocks, so the agent can narrate "this commit lands part of Rock 2" in user-facing text without each session having to write to the rocks file.

### 2. `<workspace>-rocks-new` (morning skill)

Location: a slash command in the host agent's command surface (e.g. `~/.claude/commands/` for Claude Code).

Behavior:
- Finds most recent `<rocks-dir>/*.md` (yesterday or earlier)
- Surfaces rocks with status != done as carryover candidates
- Surfaces promotion candidates: rocks carrying 3+ days with 2+ ticket refs are flagged as tracker Project candidates per the guidance above (prompt only, never auto-promoted)
- Optional pre-fill: scans the issue tracker for `In Progress` issues + open PRs across configured workspaces for rock-shaped candidates
- Prompts the user to confirm, edit, add
- Writes today's file
- Calls eval lib once, prints initial status

### 3. `<workspace>-rocks` (anytime status skill)

Location: a slash command in the host agent's command surface.

Behavior:
- Reads today's rocks file
- Calls shared eval lib
- Prints status per rock to chat: `Rock 1: done via PR #41, ABC-203. Rock 2: progressed (commit abc123). Rock 3: untouched.`
- Idempotently rewrites the status section in the rocks file using atomic-replace semantics (write a temp file in the same directory, fsync, then rename over the original). Last-writer-wins with no partial/interleaved markdown.

Naming note: `<workspace>-rocks` (status is the high-frequency verb) is preferred over `<workspace>-rocks-status`. Asymmetric with `<workspace>-rocks-new` but matches actual usage frequency.

### 4. `<workspace>-wrap` extension

Location: an end-of-session wrap command in the host agent's command surface (if one exists).

Add step at end of wrap flow:
- Calls shared eval lib
- Surfaces this-session's contribution to each rock in wrap output
- Idempotently rewrites status section in rocks file with atomic-replace semantics (see § 3)

Tradeoff: wrap gets ~1-2 minutes slower from the LLM eval pass. Acceptable cost; consider `--no-rocks` flag if it becomes annoying.

### 5. Shared eval lib

Location: a shared script in the host agent's lib directory (e.g. `~/.claude/lib/rocks-eval.sh`). Bash or Python; choose what reads cleanest.

Contract:
- Inputs: rocks file path, day scope (default today)
- Activity sources:
  - Git log across configured workspace repos for the day
  - PR activity via `gh search prs --author <username> --updated ">=YYYY-MM-DD"` (quote the comparator to prevent shell redirection)
  - Issue-tracker state transitions for the day (via the tracker's API / MCP)
  - Optional: agent session transcript scanning for narrated rock references
- LLM judgment pass: for each rock, classify as `done` / `progressed` / `blocked` / `untouched` and cite specific work
- Output: structured per-rock status; optionally rewrites the status section in the rocks file via atomic-replace (temp file + fsync + rename)
- Idempotent — multiple callers safe; last-writer-wins is the intended semantic. Atomic replace ensures no partial/interleaved file writes under concurrent callers.

LLM model: default to a cost-efficient tier (e.g. Sonnet-class); escalate if judgment quality is poor.

## Cross-Workspace Assumptions

- `<rocks-dir>/` is workspace-agnostic. If layered on dot-me, `~/.me/rocks/` rides along with the already-portable `~/.me/` directory loaded by every session.
- Eval lib must read every configured workspace repo for git activity. The list of workspaces is consumer configuration, not part of this spec.
- Issue-tracker access is available in any workspace where rocks skills run.
- The wrap extension is global; it runs in any workspace.

## Failure Modes

| Failure | Behavior |
|---|---|
| Skip morning ritual | No rocks file today; SessionStart inject is no-op; `<workspace>-rocks` reports "no rocks set" |
| LLM mis-attributes work | User edits rocks file directly; next eval pass picks up corrections |
| Two simultaneous evals (e.g. `<workspace>-wrap` in session A + `<workspace>-rocks` in session B) | Last-writer-wins; activity sources unchanged between runs; conflict is harmless |
| Eval lib slow | `--no-rocks` flag on the wrap command; rocks-status command runs only on explicit invocation |

## Build Order (reference sequence)

1. Create `<rocks-dir>/` and commit this `SPEC.md` (feature branch + PR in whatever repo hosts the user's personal context)
2. Build the shared eval lib first — everything else depends on it
3. Build the `rocks-new` and `rocks` commands — same PR
4. SessionStart hook — same PR
5. Wrap-command extension — separate PR if scope grows; same PR otherwise
6. Smoke test: write a real rocks file, run the status command, check eval against actual day's activity

## Open Questions

- Eval LLM model: cost-efficient default, escalate if quality is poor
- Session transcript scanning depth: typically last 24h across all projects; revisit if signal is noisy
- The morning command should auto-detect "stale rocks file from previous day" and prompt to roll forward
- Eval lib in Bash or Python? Bash for shell composition; Python if the LLM call shape or JSON handling gets ugly. Decide during build.

## Open question: scope of this spec in the OSS repo

This document specifies a productivity layer that *uses* dot-me's storage convention; it is not part of the core dot-me format. Three possible homes for it in this repository:

1. **Keep in `rocks/SPEC.md` at repo root** — implies the rocks system is a first-class part of dot-me. Risks confusing installers who only want the identity/voice/preferences load contract.
2. **Move to `examples/rocks-system/SPEC.md`** — frames it as one example of what can be built on top of `~/.me/`. Lower-prominence, signals "reference design, not required."
3. **Remove from this repo entirely** — host the rocks design in the user's personal infrastructure repo, link from the dot-me CHANGELOG/feedback if a third party asks for prior art.

Defer to dot-me v0.4 planning. Until that decision lands, this file stays here in scrubbed (plugin-generic) form.
