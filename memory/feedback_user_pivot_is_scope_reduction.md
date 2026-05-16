---
name: user-pivot-is-scope-reduction
description: "When user points to existing infrastructure mid-implementation (\"we already have X — why not hook into that?\"), interpret as scope reduction and USE the existing surface, not extend it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 194dfa54-8491-431c-a79a-022c2ba6303f
---

When user interrupts implementation with "we already have X — why not hook into that?", the request is **always scope reduction**, never extension.

**Why:** Validated 2026-05-15 on OneOnMe B2B partner gifting. Mid-Phase-4 (building a new welcome sheet endpoint + mobile component), user said: "we already have a welcome sheet that changes based on appsflyer links — why not hook into that?"

Investigation confirmed the existing `SignupCampaign` + `useFirstLoginAnnouncement` + `WelcomeAnnouncementSheet` pipeline could deliver partner-branded welcomes via the existing AppsFlyer install attribution (the SMS landing already emits `campaign=partner_{slug}`). The right pivot was:
- Revert the new endpoint
- Add a 30-line Partner→SignupCampaign sync signal
- Zero new mobile component, zero new endpoint

Anti-pattern I almost fell into: Codex pushed back with "but the existing surface needs an explicit ownership marker FK to be safe" — I almost added a OneToOneField + migration + signal rewrite, EXPANDING scope to make the integration "robust." That would have been more model surface than the original plan eliminated.

**How to apply:**
- "We already have X" = STOP adding new surface; use X with minimal glue
- The glue should be subordinate to X, not vice versa (don't restructure X to accommodate the new use case)
- If Codex / a reviewer demands hardening of X to support the new use, that's out-of-scope for the pivot — document and defer
- The user's signal is "I want LESS code from you, not more"

Related: [[feedback_codex_round_cap_discipline]]
