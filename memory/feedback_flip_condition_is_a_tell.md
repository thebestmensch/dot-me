---
name: flip-condition-is-a-tell
description: "When a recommendation says \"if X then drop entire rec,\" X is usually the right default — promote flip-conditions to primary"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 32e01533-c45e-4f8a-bfef-17928a59897e
---

When drafting (or reading) a recommendation that ends "...but if [condition] turns out to be true, skip this entire plan and do [simpler thing] instead" — the [condition] is almost always the actual state, and the [simpler thing] is the actual right answer. The framing is the rec author's own subconscious surfacing the truth they don't want to ship.

**Signals to watch for in own output:**
- "If pain is single-repo not cross-repo, drop the framework and use [X]"
- "If the user already covers this via [existing ticket], skip step 2"
- "If [tool] reaches stable by [date], migrate; otherwise stay on [simpler]"

Each of these is the rec author admitting the lighter path is plausibly correct. The burden of proof was implicitly inverted — heavier rec presented as default, lighter as fallback. Correct framing flips it: lighter is default, heavier requires evidence that the flip-condition is false.

**Why:** Observed 2026-05-16. Initial rec was "adopt MkDocs Material today w/ Zensical Plan B; flip to Dashboard `/docs` route if cross-repo pain isn't real." Devils-advocate caught it: "the rec author already knows the cross-repo framing might be wrong — they flip the burden of proof. The default should be the Dashboard catalog, with MkDocs as the upgrade IF cross-repo aggregation proves load-bearing." Both Codex and devils-advocate converged on RECONSIDER. The flip-condition was the right answer all along.

**How to apply:** Before shipping any recommendation w/ a stated flip-condition, re-read it w/ the burden of proof inverted. Ask: "If I had to defend the heavier path against this flip-condition, what evidence would I need?" If the answer is "none I have today," the lighter path is the actual rec. See [[high-stakes-triangulation]] for the dispatch protocol that surfaces this pattern.
