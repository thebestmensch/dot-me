---
name: format-clarify-on-visualization
description: "When user asks to visualize/diagram and the medium is ambiguous, offer a one-line format choice up front instead of picking a reasonable default"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 38807a38-c8a4-49e8-9c7c-6fd2c00e3d0d
---

When user asks to "visualize", "create a diagram", "show me X" and the medium is not specified — offer a one-line format proposal before drafting. Don't pick a reasonable default silently.

**Why:** Visualizations are taste artifacts where the medium matters as much as the content. Mermaid, SVG flowchart, HTML page, card grid, slide deck, Figma diagram all serve "visualize my workflow" — picking the wrong one wastes a full iteration. Validated 2026-05-16: asked to "visualize Claude development workflow", defaulted to card-grid swimlane layout. User correction: "I was thinking more of a flow chart". Required a full rewrite. The "reasonable default" framing from the global execution guide applies to execution mechanics (running commands, reading files), not to creative-artifact taste calls.

**How to apply:** First creative-artifact ask in a session where the user hasn't specified a medium — open with one line: "going [chosen format] unless you'd prefer [alternative]". Make it cheap to redirect. Single-format defaults are appropriate when the deliverable is constrained (e.g. "add a diagram to this README" → mermaid is the right pick because the host doc is markdown). See [[explicit-verb-over-flag]] for the related principle that ambiguity in creative surfaces wants explicit signaling over implicit defaults.
