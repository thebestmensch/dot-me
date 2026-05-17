---
name: cr-non-overlap-after-codex
description: "CodeRabbit catches ordering/coverage bugs after Codex approves — treat 'codex green' as one signal, not the final word, on classification or branch-ordering logic"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 765d0c02-5615-419b-8373-98a59b271a2b
---

When Codex returns `approve` on a diff that contains classification logic (exception mapping, status-code routing, error-bucketing), don't treat it as final. CodeRabbit consistently catches branch-ordering and coverage-gap bugs Codex misses on the same diff.

**Why:** Validated 2026-05-17 on jm-sentry PR #89:
- Round 1: Codex adversarial flagged one classification bug (LinearError → 400 for upstream outages). Fixed via new LinearUpstreamError. Codex approved.
- Round 2: CR caught that the new `status >= 500` branch ran AFTER the generic `errors[]` branch — so a Linear 500 with a GraphQL errors body STILL fell through to LinearError → 400. Same conceptual bug Codex thought was fixed.
- Round 3: CR caught that the round-2 fix's test fixture (`{"data": None}`) didn't exercise the bug class — would have stayed green even with the ordering bug.

CR's value here is multi-round iteration on the same surface. Codex does one pass. The pattern: Codex finds the obvious case, CR finds the variant the obvious case shadowed.

**How to apply:** On any PR touching exception classification or status-mapping logic, expect 2-3 CR rounds even when Codex approves round 1. Don't ship before CR re-reviews after each push. Reply substantively to CR comments (push-back when wrong, fix-and-acknowledge when right) — don't auto-accept; the third round in #89 was a real bug, not a nit. See [[no-cr-sycophancy]] for the inverse failure mode.
