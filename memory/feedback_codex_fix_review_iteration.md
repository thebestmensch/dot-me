---
name: codex-fix-review-iteration
description: Codex review on a security-critical fix can run 3–5+ rounds, each surfacing a new bypass class. Cap when findings repeat OR shift to documented-architecture conflicts. Push back with doc citation, don't auto-refactor.
metadata:
  type: feedback
---

When fixing a Codex-found security issue, dispatching adversarial-review on the FIX diff frequently reveals a *next* bypass class the original fix didn't anticipate. Each round genuinely advances; the bypasses aren't repeats. Plan for it.

**Why:** Validated 2026-05-19 on OOM-85 (GPT SQL allowlist). 5 rounds, each found a new bypass:
1. Quoted-ident regex (`\w+` missed `"users_user"`)
2. Comment-stripping regex ate string-literal contents (`SELECT '--' AS x ... FROM users_user`)
3. Comma-join after JOIN (`JOIN _scope s ON ..., users_user u`)
4. Comma-join in derived table / CTE-nested
5. (Re-raised round-2-class concern about row-comparison ON predicates — turned out already handled, locked in with regression test)

Same pattern in lighter form across OOM-86 (3 rounds) and OOM-102 (3 rounds). Most security-critical surfaces with non-trivial parsing/state will go ≥3 rounds.

**How to apply:**
- For security-critical fix diffs (SQL allowlist, auth/refresh, payment idempotency, webhook signature, etc.), budget 3–5 Codex adversarial-review rounds up front. Don't get discouraged after round 2.
- Each round: read the finding, verify empirically (test or repro), then either fold in or push back. Iterate.
- **Stop condition is NOT a fixed round count.** Stop when findings start repeating, OR when the next finding conflicts with a documented existing architecture decision (see push-back rule below), OR when the recommendation is genuine scope-creep (response-interceptor stamping when ticket is about refresh writes, etc.).

**Push-back-on-documented-architecture sub-rule:** When Codex flags a HIGH that conflicts with a documented architecture decision IN THE CODEBASE (not just personal preference), bypass with the doc citation, do NOT refactor away. Examples from this session:
- OOM-86/87 stale-LOAD_STARTED recovery: `api/gifts/berkeley.py:30-39` documents "non-idempotent POSTs intentionally use no timeout because timed-out-but-processed diverges Berkeley/local state; reconciliation tracked separately." Auto-reclaim by timestamp would reintroduce the very double-load risk the doc explicitly chose to accept stuck rows over.
- OOM-102 response-interceptor stamping: explicit code comment marks this as "tracked as separate hardening item."

In both cases the right move was: bypass with doc citation + commit/PR-body note that the finding is real and tracked separately. Re-dispatching to satisfy Codex is loop-drain — verdict won't change because the architecture won't change in this PR's scope.

Related: [[codex-audit-two-pass-yield]] (audit-time yield, different surface than fix-time iteration).
