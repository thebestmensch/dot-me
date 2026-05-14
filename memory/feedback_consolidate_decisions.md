---
name: consolidate-decisions
description: "Under broad autonomy (\"continue\", autonomous mode, \"you decide\"), make reasonable calls inline rather than surfacing 3+ decision-points per turn; reserve fan-out for genuine ambiguity or irreversible scope"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 77e64a9b-48d4-481f-a5cc-0d3ab544bf99
---

When JM grants broad autonomy ("continue on", "you decide", "no need to review", or an autonomous-mode flag in the session prompt), consolidate routine decisions inline rather than fanning out 3-4 forks per turn for him to resolve.

**Why:** JM's typical response under broad authorization is one-letter or one-word ("A", "yep", "continue", "PR"). Surfacing 3-4 decision-points back to him wastes the round-trip and reads as wanting permission for routine calls. Validated 2026-05-14 in the dot-me OSS session: every turn that ended with "options 1/2/3, you pick" forks got a terse single answer back, never the multi-decision response the fan-out invited.

**How to apply:**
- Default: make the call inline, name the choice in one line ("Picking X because Y"), and continue.
- Reserve fan-out for: (a) genuinely irreversible scope decisions outside the granted authorization, (b) name-collision-level branches where the wrong pick is 10x more expensive than a round-trip, (c) JM's own taste calls that mechanical reasoning can't resolve (visual design, positioning headline, naming).
- After one fan-out per turn, stop. If a second decision genuinely needs JM, pick a default and flag it as "going with X unless you redirect" — keep momentum, don't stall.

Related: [[autonomous-loop-default]] (loop-end discipline), [[no-uber-for-x-positioning]] (the taste-call exception)
