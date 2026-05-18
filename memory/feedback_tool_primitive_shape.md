---
name: tool-primitive-shape
description: When user suggests a known tool/system for a new problem, identify the tool's primitive vs the problem's primitive before designing within it; mismatches indicate the tool is wrong-shaped
metadata:
  node_type: memory
  type: feedback
---

When the user proposes a familiar tool (Linear, GitHub, n8n, Notion, etc.) as the home for a new concept, do not immediately design within that tool's taxonomy. First identify the tool's primitive (ticket, project, issue, document, workflow) and compare to the problem's primitive (theme, intent, outcome, fact, fuzzy state). If the primitives don't match shape, the tool is wrong-shaped for the problem.

**Why:** Validated 2026-05-18 on the rocks-tracking system design. User opened with "perhaps we start using epics in Linear that I set every morning to keep track of [big tasks]?" My first response leaned into Linear-shaped solutions (labels, projects). User then surfaced concrete rocks: "ship the next iteration of onboarding to TestFlight for QA" and "wrap up any in-flight dot-me work so we can onboard Claude Cowork beta testers." Those are outcome themes spanning N tickets across workspaces, possibly with no clean ticket bag at all. Linear's primitive is a ticket; the rock primitive is an outcome statement with a done-condition. Wrong shape. Right answer was a scratch file in `~/.me/rocks/` evaluated semantically by an LLM pass, no Linear primitive involved.

**How to apply:**
- Whenever user says "let's use X for Y," articulate (in chat or in head) the primitive of X and the primitive of Y in one phrase each
- If they match: design within X
- If they don't: surface the mismatch before designing. "Linear's primitive is a ticket; what you're describing is an outcome theme that may span multiple tickets and not map cleanly to any of them." Then propose a tool whose primitive matches
- Default to the lightest-weight matching primitive (file > Linear doc > Linear project > Linear initiative)
- Watch for the failure mode: forcing the problem's shape to fit the tool's taxonomy ("we'll just make a daily Linear project") is the smell that you should have changed tools instead

Related: [[feedback_user_pivot_is_scope_reduction]]
