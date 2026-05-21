---
name: no-security-theater
description: When a security mitigation Codex (or any reviewer) catches as bypassable, the right move is rip + document + ticket — NOT a quick patch that keeps the broken mitigation in place. Half-broken security feature is worse than no feature.
metadata:
  type: feedback
---

When a reviewer (Codex, security audit, manual review) catches a security mitigation as bypassable or incomplete, do NOT default to patching the half-broken thing. The default move is:

1. **Rip the mitigation.** Remove the broken code path entirely.
2. **Document the gap** in a code comment at the site where the mitigation was. Future readers need to see WHY the obvious-looking mitigation isn't there.
3. **Ticket the proper fix** with concrete acceptance criteria.
4. **Keep the audit log / forensic trail** if one existed. That's the actual defense until the proper fix lands.

**Why:** A half-broken security feature is worse than no feature. It creates false confidence ("we have a consent gate" / "we have rate limiting" / "we have CSRF protection"), it survives via copy-paste into other places, and the next reviewer flags it as "looks like it's solved already" rather than "this is missing." The "looks like it's protected but isn't" surface is the worst kind of security debt because nobody knows to add the right thing.

Patching a half-broken security feature into a working one in the same PR usually means writing 50-100 lines of nonce/state-binding/POST-only/CSRF-resistance code on top of a Worker that hasn't been deployed once. Each new line is an opportunity for another Codex round to surface another bypass. Compound risk on cost-paid territory.

**Validated 2026-05-21 on OOM-53 scrape-mcp scaffold:**

- Codex round 1 + 2 caught DCR (dynamic client registration) trust gap.
- I added an `approve=1` consent interstitial as the mitigation (~50 lines).
- Codex round 3 caught the consent gate as bypassable (attacker can include `approve=1` in the URL stashed verbatim as Google `state`; survives the round trip; grant auto-issues without fresh confirmation).
- Correct call (after user choice): rip the consent interstitial, restore the gap-acknowledgment comment, file Linear ticket (OOM-127) for the proper fix that's coordinated across both Workers (`oom-mcp` has the same gap in production).
- Incorrect call: build the 80-line nonce/POST/state-binding flow on top of the bypassable code; trigger Codex round 4, 5, 6 each on net-new security-sensitive code; risk shipping a worse second-order bug.

**How to apply:**

1. When a reviewer catches a security mitigation as bypassable, ask: "is the fix one line (e.g., tighten a validator) or 50+ lines (e.g., add nonce flow, CSRF token, full session-state-binding)?"
2. One-line tighten: do it.
3. 50+ line full primitive: rip + ticket. Don't ship the half-state.
4. Always preserve the audit log / forensic trail. That's the meaningful defense.
5. When ripping, the code comment at the site should name the failure mode the reviewer found, not just "see ticket". Future maintainers need enough context to understand why the obvious-looking mitigation got reverted, not added.
6. If the same gap is live in a sibling Worker / service / repo, the ticket spans BOTH — design the fix once, deploy identically. Two ad-hoc fixes diverge.

**Skip-when:** the mitigation is itself the deliverable (e.g., PR explicitly says "add consent gate") rather than an incidental piece of a larger feature. Then the rip/ticket flow means killing the PR, not just trimming a feature.

Related: [[codex-fix-review-iteration]], [[port-surfaces-sibling-bugs]], [[user-pushback-on-bypass-means-dispatch]].
