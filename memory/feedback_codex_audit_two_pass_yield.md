---
name: codex-audit-two-pass-yield
description: Cross-provider Codex audits return high-value Crit/Important findings on pass-2 with broadened narrow scope, even when pass-1 looked thorough. Budget for at least 2 passes when surface is non-trivial.
metadata:
  type: feedback
---

Codex audits via `codex:codex-rescue` are scope-bounded: the subagent reads the prompt literally and won't broaden on its own. A "thorough" pass-1 prompt often misses entire categories of bugs because the categories weren't named in the scope. Pass-2 with broadened-narrow scope (named-but-narrow categories that pass-1 didn't list) reliably surfaces new Crit-tier findings that pass-1 couldn't have caught.

**Why:** Validated 2026-05-19 on OneOnMe mobile audit. Pass-1 (deep-link / Stripe / hooks lifecycle) returned 4 Important + 2 Minor, zero Crits. Pass-2 (auth/JWT/SecureStore + Sentry mobile PII + permissions UX + gestures/worklets/FlatList) returned 2 NEW Crits (logout race, Sentry attachScreenshot PII), 3 Important, 2 Minor — Crit-tier findings pass-1 was structurally unable to surface because auth/Sentry weren't scoped in.

The same pattern held on the API side earlier in the session: pass-2 with broadened scope (partner gifts, Berkeley webhook, celery global config, admin chat, attribution webhooks, auth=None ingress inventory) returned 3 Crits + 8 Important + 4 Minor where pass-1 had returned a narrower set.

**How to apply:**
- For ANY cross-provider audit on a non-trivial surface (mobile app, API service, plugin runtime): plan for 2 dispatches up front. Pass-1 = "go broad on what the surface obviously does"; pass-2 = explicit named-but-narrow categories pass-1 didn't list.
- When designing pass-2, list specific category names: "auth/JWT/SecureStore", "Sentry PII", "permissions UX", "Reanimated worklets", "FlatList perf" — not "anything pass-1 missed." Codex won't broaden a vague scope.
- ALWAYS tell pass-2 explicitly what pass-1 already covered (with file:line refs) so it doesn't re-flag the same surfaces. Include this as a "Out of scope" block in the dispatch prompt.
- Pass-2 cost is ~$0.30 of Codex time; ROI on 2+ Crit-tier tickets is enormous. Don't skip it because pass-1 "looked thorough."

Related: [[codex-audit-dispatch-path]] (subagent vs wrapper routing — wrapper critiques the prompt, subagent executes the audit).
