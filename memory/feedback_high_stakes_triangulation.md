---
name: high-stakes-triangulation
description: "For lock-in / \"stuck with this\" decisions, dispatch research-agent + devils-advocate + Codex cross-provider + raw repo metrics in parallel; converge on signals before recommending"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 32e01533-c45e-4f8a-bfef-17928a59897e
---

On high-stakes lock-in decisions (framework choice, architecture pivot, vendor commit, anything user describes as "we'll be stuck with this for awhile"), don't ship a single-pass research-agent answer. Triangulate:

1. **research-agent** — gather options w/ explicit constraints + current state (last 6-12 months)
2. **devils-advocate** — challenge the leading recommendation, attack vectors listed explicitly
3. **codex:codex-rescue** (read-only diagnose) — cross-provider second opinion (Claude blind spots ≠ GPT-5 blind spots)
4. **Raw data** via Bash — GitHub repo metrics (stars, contributors, last commit, releases, `archived` flag), npm downloads, license. Vibes about maintainer health are not evidence.

Dispatch in parallel where possible (same message, multiple tool calls). Synthesize at the end. If 3+ signals agree → high confidence. If divergent → name the disagreement and what would resolve it.

**Why:** Single-pass research-agent ships confident-but-wrong recommendations under lock-in pressure. Observed 2026-05-16: home-lab component-library decision. First-pass research recommended Astro + storybook-astro. Triangulation surfaced bus-factor-1 on storybook-astro (28★, 2 contributors, no releases), hand-waved 6× auth-middleware port to TypeScript, and the meta-observation that "Claude reads files, not Storybook UIs" → final verdict was RECONSIDER. Without the adversarial pass, the wrong answer ships.

**How to apply:** Trigger phrases — "are you positive", "are you sure", "we'll be stuck with this", "big decision", "lock-in", "use all the tools", "make sure it's the right one". Also self-fire when about to recommend a framework, vendor SaaS, schema migration, or anything that's expensive to reverse. See [[two-layer-tool-evaluation]] for the framing rule that prevents the most common first-pass error.

Skill draft tracked in JM-196.
