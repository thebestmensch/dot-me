---
name: verify-scheduled-handoff-path
description: "When designing a fix that delegates work to \"the other path,\" verify the other path actually runs on the scheduled/automatic surface — don't trust function names or \"this exists, it'll get called\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4aa78910-77ee-4e55-9493-ffce77b18920
---

If a fix says "balance-only check is OK because the transaction-sync function will pick up the slack on the next cron pass," verify the transaction-sync function is **actually scheduled**. Grep `beat_schedule` / `CELERY_BEAT_SCHEDULE` / equivalent. A function that only runs from admin actions or tests cannot rescue a regression in the scheduled path.

**Why:** OOM-34 (2026-05-17). My initial fix gated `reconcile_gift_redemption_status` on `redemption_card.transaction_count > 0`. ADR docstring confidently asserted "real redemptions will flip via `fetch_and_store_card_transactions` on its next sync." Codex adversarial review verified the claim by grepping callers and found `fetch_and_store_card_transactions` is *only* triggered from `gifts/admin.py` (manual button) and tests — never from beat schedule. So the local `transaction_count` snapshot would stay stale forever, and the gate would suppress real redemptions indefinitely. Caught pre-merge by Codex; would have shipped silent revenue-state bug otherwise.

**How to apply:**
- Before writing "the other path will handle it" in an ADR or design note: open `api/celery.py` (or your equivalent beat-schedule config) and grep for the function name. If it's not there, your handoff is hypothetical.
- Also grep `gh_actions` / `cron` / `crontab` / scheduled-task config for non-Celery surfaces.
- Don't trust function-name semantics. `fetch_and_store_card_transactions` sounds like a thing that runs regularly; it doesn't in this codebase.
- Same investigation applies before writing a one-time data-fix command that selects candidates by a snapshot field — if the field is unreliable, the reversal is destructive. Confirm the field is authoritative or pull live source-of-truth per row.
- The "Verify before claiming done" rule in CLAUDE.md is the umbrella; this is the specific sharper failure mode it doesn't name. Adversarial review catches it; "I'm sure the other path runs" is the rationalization to reject.

Related: [[flip-condition-is-a-tell]] — when a fix says "if X then drop entire rec," X is usually the actual state; same shape applies to handoff assertions.
