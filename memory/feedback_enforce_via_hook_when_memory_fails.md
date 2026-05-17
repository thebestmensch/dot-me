---
name: enforce-via-hook-when-memory-fails
description: When a memory rule fails to fire and a high-cost mistake ships under the rule's nose, the right next step is a PreToolUse/Stop hook that enforces the rule, not a sharper memory note.
metadata:
  type: feedback
---

A memory rule that *exists* and *should* have applied but *didn't fire* is a signal that the workflow has a bypass path. Sharper wording in the memory file won't close it — the next slip will take the same path. The fix is a hook that catches the bypass.

**Why:** On 2026-05-17 the memory rule [[voice-for-outgoing]] said "always invoke `/jm-voice` when drafting any text sent as James." It was loaded into context, I had read it that session, and I still filed `anthropics/claude-code#60063` with raw `gh issue create` — no voice pass, no template check. The rule was clear, I just bypassed it. Adding "no really, always do this" to the memory file would not have caught the next bypass. What did: a PreToolUse hook (`oss-post-gate.sh`) that blocks raw `gh issue/pr create|edit|comment` against external repos unless a scoped marker is written by the sanctioned skill ([[oss-post-discipline]]).

**How to apply:** When a session retro surfaces "this memory rule should have prevented X and didn't," do not respond by rewording the memory. Instead:

1. Identify the bypass path (what tool call slipped past the rule).
2. Find or build the matching hook event (PreToolUse on Bash for shell commands, on Edit/Write for files, etc.).
3. Define the marker mechanism: what state must exist for the gate to pass, who writes it, when it's consumed.
4. Pair the hook with a skill that's the happy path (writes the marker, does the work properly).
5. Keep the memory entry as the *why* (so the rule is portable across machines + sessions where the hook isn't loaded), but understand the hook is the load-bearing enforcement.

Tactical corollary: if I find myself writing "be more careful about X" as a memory entry, that's almost always the wrong shape. "Be more careful" doesn't survive context pressure or session restarts. A hook does.

See also [[voice-for-outgoing]], [[oss-post-discipline]], [[chezmoi-pr-workflow]] (workflow rule that *is* paired with a hook today).
