---
name: two-layer-tool-evaluation
description: "When evaluating dev tools/frameworks, split \"AI consumption layer\" from \"human authoring/browse layer\" — different optimal answers per layer"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 32e01533-c45e-4f8a-bfef-17928a59897e
---

When recommending tools for documentation, component catalogs, knowledge bases, or anything that serves both humans and AI, split the decision into two layers and answer separately:

- **AI-consumption layer** — Claude reads files. Wants raw, indexed, predictable. Almost never needs a framework. `llms.txt` + raw `.md` + auto-imports is usually enough.
- **Human authoring / browse layer** — wants nav, search, cross-link, generation, visual catalog. Often benefits from a framework (MkDocs Material, Obsidian, etc.).

These layers have different optimal answers. A framework can own the human side without touching the AI side (files stay MD on disk).

**Why:** Conflating them produces too-dismissive first answers. Observed 2026-05-16: dismissed framework adoption for "docs-for-AI" pattern by saying "Claude reads files, no framework needed." User pushed back ("are you positive we don't want a framework?"). Correct framing is two-layer — AI side stays dumb, human side may want MkDocs Material / Obsidian / similar. The "no framework" answer was right for one layer and wrong for the other; presenting it as a single answer was the mistake.

**How to apply:** Before any "should we adopt X framework" recommendation, ask: who's the consumer of each layer? If both humans and AI consume the same content, name both answers separately. When recommending against a tool, also explicitly state the conditions under which the recommendation flips — don't leave the alternative undefended. See [[high-stakes-triangulation]] for the dispatch protocol when the decision is also lock-in-shaped.
