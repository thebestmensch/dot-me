---
name: voice-doc-reconciliation
description: When adding a new style rule to ~/.me/memory/, immediately audit voice.md and preferences.yaml for contradictions and fix them in the same PR.
metadata:
  type: feedback
---

When a new style/voice rule lands in `~/.me/memory/feedback_*.md`, audit `~/.me/voice.md` and `~/.me/preferences.yaml` for contradictions in the same session, and fix them in the same PR as the rollout.

**Why:** `voice.md` is the generation guide for [[voice-for-outgoing]]. If the memory rule says "no em dashes" but voice.md still tells `/jm-voice` em dashes are fine in pro register, the rule loses every time `/jm-voice` runs. Same trap for preferences.yaml structured fields. Discovered 2026-05-16 on the no-em-dashes rollout: caught only by spot-checking the agent's flagged rewrites; voice.md was teaching the opposite of the new rule with empirical backing (5 historical GitHub issues). Without the reconciliation, the next `/jm-voice` pass would have re-introduced em dashes despite the freshly committed rule.

**How to apply:**
- After writing `feedback_<style>.md`, grep `voice.md` and `preferences.yaml` for the topic (em-dash, exclamation, contraction, etc.)
- If voice.md asserts the opposite, rewrite the relevant lines AND any format-matrix rows AND any "pro structural traits" lists
- Preserve historical-pattern context as caveat ("empirically true in pre-2026 samples, but the rule changed")
- Quoted source material with the old pattern stays verbatim (don't rewrite other people's text)
- Roll the voice/preferences updates into the same PR as the OSS scrub so reviewers see the policy and the doc together

Related: [[no-emdashes]], [[voice-for-outgoing]], [[voice-register-routing]].
