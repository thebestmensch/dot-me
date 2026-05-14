---
name: no-uber-for-x-positioning
description: "For dot-me and other OSS projects JM owns, don't use \"X for Y\" framing or lean on other tools/standards as adoption shortcuts in positioning"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 77e64a9b-48d4-481f-a5cc-0d3ab544bf99
---

**Scope: the elevator pitch / headline / launch positioning.** Body-level comparison tables and "where it sits in the landscape" sections are fine and useful — readers want orientation. The rule is about the *pitch*, not the docs.

Don't position dot-me (or other JM-owned OSS work) in the headline/pitch as "PAM for AI identity," "the .editorconfig of personal context," "AGENTS.md for the human," etc.

**Why:** "X for Y" framing borrows authority from a thing many readers don't recognize, makes the project sound like it can't stand on its own, and ties the pitch to whether the audience knows the reference. PAM and BSD Auth aren't ubiquitous enough for the line to land cold. Even when the analogy is technically clean, the pitch should be self-contained.

**How to apply:**
- Elevator pitch defines the problem in plain terms ("AI tools start blank every time, you re-type yourself") and the solution in plain terms ("three files at ~/.me/ that tools read at startup"). No comparison verbs ("like X", "the Y of Z"), no borrowed brand authority.
- Naming properties that make it work (plain files, no cloud, no daemon) is fine — those are facts about dot-me, not comparisons.
- Comparison tables in README body or docs are *fine* — they orient readers placing dot-me in their mental map. Keep them. They just don't lead.
- Metaphors that describe behavior ("a name tag at the door") are fine — those aren't borrowing brand authority, they're describing function.

Related: [[project_personal_context_repo]]
