---
name: codex-oscillating-findings
description: "Codex returning HIGH on round N then HIGH on round N+1 advocating the OPPOSITE direction (same surface, same diff iteration) is taste-territory, not narrowing. Defer to ticket's stated architectural decision, push back, document in PR body."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: dc9af289-989b-4082-972d-43f53d57bce8
---

Codex adversarial-review HIGH on round N followed by HIGH on round N+1 with a recommendation that *reverses* round N's recommendation = oscillation, not narrowing. Don't apply round N+1's fix just because it's the most recent verdict. Both directions are defensible; the trade-off space has no objectively correct answer, which is exactly why the LLM swings.

**Why:** Validated 2026-05-21 on OOM-124 (`_card_has_real_transactions`). Round 1 HIGH: "don't require `merchant_name` — risks false-reverse of legitimately spent gifts on partial Berkeley payloads." Adopted (dropped merchant_name requirement, transaction_type exclusion only). Round 2 on the revised diff: HIGH "do require merchant/MCC — unknown types reopen the OOM-34 false-flip mode." Same file, same lines, opposite recommendation. The trade-off is asymmetric — under-reversal vs over-flip — and the ticket's own Major Architectural Decisions section had already called `merchant_name` *optional*, deliberately leaving the call to the implementer. Either direction ships defensible code; whichever round you happen to stop on becomes the shipped version. That's a tell.

**How to apply:**
- When round N+1's `title` or `recommendation` reverses round N's on the same file/function, **stop iterating**. Treat as taste-territory equivalent to the `codex-dispatch.md` narrowing-edge-case 2-round cap.
- Defer to the ticket's stated architectural decisions or the user's prior call. The human picked one direction deliberately; oscillating Codex output isn't new information.
- Surface the contradiction in the PR body (own `## What I made up` item) and the Linear completion comment — name both rounds' verdicts, name the direction chosen, name the asymmetry rationale. The human reviewer resolves it, not the agent.
- Do NOT re-dispatch a third round on the same diff hoping for a tie-breaker. The verdict won't converge — it'll either oscillate again or land on whichever direction Codex's sampling happens to favour, which is noise.
- Different from [[codex-fix-review-iteration]] (3-5 rounds finding *new* bypass classes — each round advances). Different from `codex-dispatch.md` narrowing-edge-case (round N+1 narrower than round N — diminishing real risk). Oscillation is a sibling tell, not a subtype of either.

Related: [[codex-fix-review-iteration]], `codex-dispatch.md` narrowing-edge-case section.
