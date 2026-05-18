---
name: corpus-research-specificity
description: "When broad-pattern research (e.g. \"22 founder bios\") only partially fits the user's specific profile, dispatch a SECOND targeted pass on the matching subset (e.g. \"ex-Google founders with multiple ventures\"). Extrapolating from the broad corpus to the user's narrow case produces confidently-wrong general advice."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 355b2c93-b128-4fa4-badd-7c14719f940f
---

Broad-corpus research is the right shape for *frame-setting* (what are the common bio archetypes? what's the structural range?). It's the wrong shape for *positioning the user's specific case*. The user is not the median of the corpus; they're a specific data point with a specific shape, and the corpus's general patterns may not apply to their narrow intersection.

The failure mode: do one broad research pass (e.g. "study 22 successful CTO/founder bios"), then try to answer narrow positioning questions ("where does ex-Google fit in a repeat-founder's bio?") by extrapolating from the broad data. The extrapolation feels analytical but is unanchored — the corpus didn't filter for the user's specific intersection.

**Why:** Validated 2026-05-18 during James's bio. First research-agent pass gathered 22 successful founder/CTO bios across the broad space (Charity Majors, Patrick McKenzie, DHH, Will Larson, etc.). Returned 4 archetypes + general patterns. I then tried to answer "where does Google sit in a repeat-founder's bio?" by extrapolating from the corpus. James pushed back: *"can you google around for other folks that have worked at both bic co's like google and also have successfuly cofounded startups?"* — directly requesting the targeted second pass.

The second research-agent pass on ~12 ex-big-tech-+-founder trajectories (Bret Taylor, Rosenstein, Systrom, Williams, D'Angelo, Butterfield, Koomen, Fadell, Krieger, Thrun, Singleton, Lior Ron, Mauskopf) returned specific findings the broad corpus could never have surfaced: "sentence-1 placement of ex-big-tech credential is anti-pattern," "ex-Google is third-party language," "colon-list-with-Google is anti-pattern." None of those would have come from extrapolating the broad 22-bio set.

**How to apply:**

- For positioning / framing tasks involving the user's specific profile, structure the research as **two passes**, not one:
  1. **Broad pass**: archetypes, structural range, general taste rules.
  2. **Targeted pass**: explicit corpus restricted to the user's specific intersection. Name the intersection precisely (e.g. "ex-Google IC turned multi-time founder", "Y Combinator alum who built developer tools", "AI researcher who left to start an enterprise startup").
- Don't try to answer narrow positioning questions from broad corpus data. Surface the limitation: "the 22-bio corpus is broad — to answer where ex-Google sits in YOUR bio, I should do a targeted pass on ex-big-tech founders."
- If the user asks the targeted question and you only have broad data, that's the trigger to dispatch the second pass, not to extrapolate.
- For pure-archetype questions ("what shapes exist?"), broad is fine. For positioning-the-user questions ("where do I fit?"), broad is insufficient.

**Heuristic for "is the broad pass enough?":** if you can articulate the user's specific intersection (ex-Google + repeat founder, OR ex-Slack engineer + first-time founder, OR data scientist + B2B SaaS founder) and the corpus didn't filter on it, you need a targeted second pass before positioning.

**Anti-pattern:** confidently citing the broad corpus as the source of a narrow positioning recommendation. The corpus is your source for the SHAPE OF THE QUESTION, not the SHAPE OF THE ANSWER for this specific user.

Related: [[feedback_landscape_scan_before_bulk_creative]] (competitor scan discipline — same "broad-then-targeted" shape applied to creative output rather than research input).
