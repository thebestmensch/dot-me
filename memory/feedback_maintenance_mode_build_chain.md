---
name: maintenance-mode-build-chain
description: "Static-site generator in maintenance mode is NOT adoption-safe just because static HTML doesn't rot — plugins/MD-extensions/search-JS/build-chain do"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 32e01533-c45e-4f8a-bfef-17928a59897e
---

When evaluating a static-site generator (or any output-static tool) that has entered maintenance mode, the "files survive, output is HTML, what could go wrong" intuition is too generous. The output doesn't rot but the build chain does.

**What rots in a maintenance-mode SSG:**
- Third-party plugins lose their reason to keep up w/ ecosystem drift (Python/Markdown versions, theme APIs, search backends)
- Markdown extensions and admonition syntax tied to specific parser versions
- Frontmatter/nav/sidebar schemas baked into the framework — exit cost lives here, not in `.md` source
- Search index JS bundles tied to specific framework releases
- Container/deploy paths assume specific tooling versions

**Why:** Observed 2026-05-16. Triangulation on adopting MkDocs Material today. Naive read: "static HTML, who cares about maintenance mode." Codex non-overlap finding: lock-in lives in the build chain (MDX/admonition syntax, plugin semantics, nav schema), not in source files. Devils-advocate found a 2-month-old llms.txt plugin in the rec — pinning that w/ a sunsetting framework forces vendoring + manual patches across multiple repos within 12 months.

**How to apply:** When recommending a maintenance-mode tool, the rec must explicitly enumerate what gets pinned (framework version, plugin versions, Python/Node deps) AND state a vendoring plan (copy plugin source into repo). If the rec is silent on those, the rec is wrong by omission. Connects to [[high-stakes-triangulation]] — this is the kind of failure mode adversarial passes surface that single-pass research misses. Also connects to the Watchtower lesson (pin tags, avoid sunsetting tools knowingly).
