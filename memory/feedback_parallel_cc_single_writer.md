---
name: parallel-cc-single-writer
description: Features touching shared state across N concurrent CC sessions need a single-writer pattern OR idempotent re-evaluation; never N writers appending to a shared file
metadata:
  node_type: memory
  type: feedback
---

When designing a feature that involves multiple concurrent CC sessions (parallel agents, multiple workspaces, sibling sessions) touching the same persistent artifact, never let N sessions each write/append to the artifact directly. Two safe patterns: (1) **single-writer**: one canonical skill rewrites the artifact, all others read-only; (2) **idempotent re-evaluation**: every writer re-derives the full artifact state from external sources (git, Linear, transcripts) and overwrites — last-writer-wins is safe because the source of truth is the activity, not the file.

**Why:** Validated 2026-05-18 during rocks-system design. Initial sketch had each parallel CC session annotating the day's rocks file with "this session contributed X to Rock 2." Surfaced two failure modes: (a) write conflicts when sessions ran concurrently, (b) false-positive attribution where session A thinks commit abc is Rock 1, session B disagrees, both append, file becomes inconsistent narrative. Resolved by: SessionStart hook injects rocks read-only into every session's context (claude can narrate in chat but never writes); `/jm-rocks` and `/jm-wrap` both call the same idempotent eval lib that re-derives rock status from full day's git/PR/Linear activity — last-writer-wins is safe because each writer reads the same external sources.

**How to apply:**
- New feature spec mentions "this skill updates [file] as we work" + "multiple sessions can be running" → single-writer or idempotent-re-eval required
- Per-session writes with append semantics are the failure mode to refuse
- For status-tracking artifacts (rocks, daily logs, progress files): default to idempotent re-eval — the file is a cache of external truth, not the truth itself
- For artifacts where state genuinely originates in a session (decisions, transcripts): single-writer with a clear handoff (only `/jm-wrap` writes wrap notes, etc.)
- Inject-don't-mutate is fine for SessionStart hooks (read-only fan-out is safe)
