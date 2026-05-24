# Rocks System — Design Spec

## Problem

Parallel CC sessions across workspaces (home-lab, oneonme, and others) ship a lot of work each day. The "big rocks" — outcome-themed initiatives that span multiple tickets, sometimes across workspaces, often ill-fit for Linear's taxonomy — get lost in the firehose. JM ends the day uncertain whether the things he actually meant to land got landed.

Examples of rocks (not tickets, not projects):
- "Ship the next iteration of onboarding to TestFlight for QA"
- "Wrap up any in-flight dot-me work so we can onboard Claude Cowork beta testers"

## Out of Scope

- Linear taxonomy (Initiatives, Projects, Epics) — wrong fit for daily outcome themes
- Per-session writes to the rocks file (single-writer principle; idempotent re-eval only)
- Replacing or modifying `/jm-daily-recap` — keeps current behavior, separate concern

## File Format

Path: `~/.me/rocks/YYYY-MM-DD.md`

```markdown
---
date: 2026-05-18
---

# Rocks

## Rock 1: <one-line outcome statement>
- Done when: <objective condition>
- Linear: <optional, comma-sep JM-N / OOM-N refs covering this rock>
- Status: <eval output: untouched | progressed | done | blocked>
- Related: <git/PR/Linear refs from eval>

## Rock 2: ...

## Carryover Notes
- <freeform notes from previous days that didn't ship>
```

Frontmatter enables future querying. Plain Markdown so JM can read and edit directly.

### Linear linkage (optional, not required)

The `Linear:` line is a soft pointer. A rock may have:
- **Zero tickets** — themes like "Finish onboarding" or "Wrap dot-me for beta testers" routinely span work that never gets ticketed. Don't fabricate tickets to satisfy the field; omit the line.
- **Partial coverage** — some sub-work ticketed, some not. List what exists; don't gate the rock on full coverage.
- **Full coverage** — every meaningful chunk maps to a JM-N / OOM-N. Common for engineering-heavy rocks.

The eval pass uses `Linear:` refs as additional signal sources when present (cross-references ticket state transitions), but absence of the field never downgrades status. Rocks remain primary; tickets are bookkeeping.

### Promotion: rock → Linear Project

When a rock carries forward 3+ days *and* has 2+ Linear refs, it's structurally a Project, not a daily theme. Suggest at carryover time (`/jm-rocks-new` § 2 guidance): "This rock has carried 4 days with refs JM-201, JM-205, JM-208 — consider promoting to a Linear Project so the issues nest under shipped scope, and let the rock become a daily pointer to the Project."

This is a *prompt*, not an enforcement. Some rocks legitimately carry without ticket gravity (research, ops drift, life work).

## Components

### 1. SessionStart hook (global)

Location: `~/.claude/settings.json` hooks block.

- On every CC session start, reads `~/.me/rocks/YYYY-MM-DD.md` if it exists
- Injects rock titles + done-conditions into the session's context
- Silent no-op when file is missing
- Cost: ~200 tokens per session

Purpose: every session knows the rocks, so Claude can narrate "this commit lands part of Rock 2" in user-facing text without each session having to write to the rocks file.

### 2. `/jm-standup` (morning skill)

Location: `~/.claude/commands/jm-standup.md` (chezmoi-managed at `~/.local/share/chezmoi/dot_claude/commands/jm-standup.md`)

Behavior:
- Reads yesterday's rocks from the dashboard `/api/rocks` mirror (falls back to local file walk if unreachable)
- Surfaces rocks with status != done as carryover candidates
- Surfaces promotion candidates: rocks carrying 3+ days with 2+ Linear refs are flagged as Linear Project candidates per the guidance above (prompt only, never auto-promoted)
- Pulls cross-workspace active work via Linear + GitHub MCPs (In Progress + In Review for `@me`, open PRs, recent git) as suggestion list
- Prompts JM to confirm, edit, add
- Writes today's file AND POSTs to dashboard `/api/rocks` (file + dashboard mirror; Claude is the single writer)
- On dashboard failure: file write succeeds, payload buffered to `~/.claude/scratch/rocks-pending/<date>.json` for `/jm-wrap` retry

Replaces the unbuilt `/jm-rocks-new` stub. Initial eval pass moves to `/jm-wrap` (per § 4 below) so morning ritual stays fast.

### 3. `/jm-rocks` (anytime status skill)

Location: `~/.claude/commands/jm-rocks.md`

Behavior:
- Reads today's rocks file
- Calls shared eval lib
- Prints status per rock to chat: `Rock 1: done via PR #41, JM-203. Rock 2: progressed (commit abc123). Rock 3: untouched.`
- Idempotently rewrites the status section in the rocks file using atomic-replace semantics (write a temp file in the same directory, fsync, then rename over the original). Last-writer-wins with no partial/interleaved markdown.

Naming note: chose `/jm-rocks` (status is the high-frequency verb) over `/jm-rocks-status`. Asymmetric with `/jm-rocks-new` but matches actual usage frequency.

### 4. `/jm-wrap` extension

Location: `~/.claude/commands/jm-wrap.md` (existing, chezmoi-managed)

Add step at end of wrap flow:
- Calls shared eval lib
- Surfaces this-session's contribution to each rock in wrap output
- Idempotently rewrites status section in rocks file with atomic-replace semantics (see § 3)

Tradeoff: wrap gets ~1-2 minutes slower from the LLM eval pass. Acceptable cost; consider `--no-rocks` flag if it becomes annoying.

### 5. Shared eval lib

Location: `~/.claude/lib/rocks-eval.sh` (or `.py` if cleaner; decide during build)

Contract:
- Inputs: rocks file path, day scope (default today)
- Activity sources:
  - Git log across home-lab + oneonme repos for the day
  - PR activity via `gh search prs --author thebestmensch --updated ">=YYYY-MM-DD"` (quote the comparator to prevent shell redirection)
  - Linear ticket state transitions for the day (Linear MCP)
  - Optional: CC session transcript scanning under `~/.claude/projects/*/` for narrated rock references
- LLM judgment pass: for each rock, classify as `done` / `progressed` / `blocked` / `untouched` and cite specific work
- Output: structured per-rock status; optionally rewrites the status section in the rocks file via atomic-replace (temp file + fsync + rename)
- Idempotent — multiple callers safe; last-writer-wins is the intended semantic. Atomic replace ensures no partial/interleaved file writes under concurrent callers.

LLM model: default `sonnet` for cost, escalate to `opus` if judgment quality is poor.

## Cross-Workspace Assumptions

- `~/.me/rocks/` is workspace-agnostic by virtue of `~/.me/` already being a portable repo loaded by every CC session
- Eval lib must read both `~/Documents/local/jm-home-lab/` and `~/Documents/local/oneonme/` (and any future workspaces) for git activity
- Linear MCP is available in any workspace where rocks skills run
- `/jm-wrap` is global; runs in any workspace

## Failure Modes

| Failure | Behavior |
|---|---|
| Skip morning ritual | No rocks file today; SessionStart inject is no-op; `/jm-rocks` reports "no rocks set" |
| LLM mis-attributes work | JM edits rocks file directly; next eval pass picks up corrections |
| Two simultaneous evals (e.g. `/jm-wrap` in session A + `/jm-rocks` in session B) | Last-writer-wins; activity sources unchanged between runs; conflict is harmless |
| Eval lib slow | `--no-rocks` flag on `/jm-wrap`; `/jm-rocks` runs only on explicit invocation |

## Build Order (post-compact)

1. Create `~/.me/rocks/` directory and commit this `SPEC.md` (feature branch + PR in `~/.me/` repo)
2. Build `~/.claude/lib/rocks-eval.sh` first — everything else depends on it (chezmoi feature branch + PR)
3. Build `/jm-rocks-new` and `/jm-rocks` commands — same chezmoi PR
4. SessionStart hook in `~/.claude/settings.json` — same chezmoi PR
5. `/jm-wrap` extension — separate chezmoi PR if scope grows; same PR otherwise
6. Smoke test: write a real rocks file, run `/jm-rocks`, check eval against actual day's activity

## Open Questions for Build Phase

- Eval LLM model: `sonnet` default, escalate to `opus` if quality is poor
- Session transcript scanning depth: probably last 24h of transcripts across all projects; revisit if signal is noisy
- `/jm-rocks-new` should auto-detect "stale rocks file from previous day" and prompt to roll forward — yes
- Should the eval lib be Bash or Python? Bash for shell composition; Python if LLM call shape or JSON handling gets ugly. Decide during build.
