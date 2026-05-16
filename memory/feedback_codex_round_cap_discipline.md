---
name: codex-round-cap-discipline
description: "When Codex flags the same conceptual issue across 2+ rounds of adversarial-review, bypass with documented reasoning instead of scope-expanding to fix it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 194dfa54-8491-431c-a79a-022c2ba6303f
---

When Codex adversarial-review surfaces the **same conceptual concern** across 2+ rounds (e.g. "shared identity space," "missing ownership marker"), that's the signal to **bypass with documented reasoning**, not iterate further.

**Why:** Validated 2026-05-15 on OneOnMe B2B partner gifting Phase 4 pivot. Codex ran 4 rounds on a tiny 12-line signal:
- Round 1: 3 findings (CTA URL routing, no backfill, no DB constraint) — fixed 2, deferred 1.
- Round 2: 2 findings (migration overwrite/rollback-delete, raw=True side effects) — fixed both.
- Round 3: 1 finding (shared identity space with admin-authored campaigns) — same theme as deferred round-1 #3, recommended explicit FK.
- Round 4: 1 finding (failed CTA marks welcome seen without retry) — pre-existing behavior of the original component, not introduced by the edit.

I almost added a cross-app OneToOneField + new migration + signal rewrite to satisfy round 3 — until the `PreToolUse:Edit hook` checkpoint at edit #10 forced a pause. Realized: user's pivot was scope REDUCTION ("just hook into existing"), Codex was pushing scope EXPANSION, and the "fix" would have added more model surface than the pivot eliminated.

Recognition triggers:
- Same conceptual issue restated across rounds with different recommendations (FK → marker → ownership) — concern is design-level, not iterable
- Fix would touch model schema / require migration for a tiny feature edit
- The recommended fix existed as an option in round 1 and was already deferred — Codex just isn't moving on

**How to apply:** After round 2 on the same theme, write a bypass naming:
1. Why the concern is real in principle
2. Why practical risk is acceptable for this diff (e.g. brand-new app, no operator data, single-writer surface)
3. The right long-term fix as a follow-up

Trust the `Edit #N` hook checkpoint when it fires — it's catching exactly this drift. Re-read the goal, not the latest review.

Related: [[feedback_user_pivot_is_scope_reduction]]
