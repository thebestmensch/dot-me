---
name: port-surfaces-sibling-bugs
description: When copying scaffold verbatim from a sibling service (OAuth Worker, cookie module, auth handler), Codex review on the new copy can surface real bugs in the original. Fix in the same PR or open a tracking ticket — don't ship the bug aware-and-silent.
metadata:
  type: feedback
---

When porting / cloning a scaffold from a sibling service (sibling Worker, sibling repo, sibling auth module), the adversarial review on the *new* copy will sometimes find bugs that have been silently live in the *original*. The review on the copy is often the first time anyone has read those exact lines critically, even though they've been deployed for months.

**Why:** Scaffolds copied verbatim look like "already-reviewed code" to maintainers. When the original shipped, it may have been reviewed lightly, by a different reviewer, or in a different context. The new copy triggers a fresh adversarial pass on the same code, but the reviewer is reviewing it as new — they don't know it's a copy, so they don't grade on a curve. Real bugs surface.

This is the same pedagogy as generalization-as-audit (porting code into a generalized plugin/template exposes assumptions baked in by workspace context) but at the *runtime-correctness* layer, not the *prose-clarity* layer.

**Validated 2026-05-21 on OOM-53 scrape-mcp scaffold:**

- `scrape-mcp/src/cookies.ts` was copied verbatim from `oom-mcp/src/cookies.ts` (production OneOnMe Postgres MCP Worker, live for months).
- Codex pass 4 on scrape-mcp flagged the HMAC-sign function: `btoa(JSON.stringify({...name: 'José'}))` throws `InvalidCharacterError` because `btoa` requires a Latin-1 string but the JSON payload contains UTF-8 bytes (curly apostrophes, accents, CJK, emoji).
- This same bug is live in `oom-mcp` production today — any user with a non-ASCII Google profile name has a broken sign-in callback. We just hadn't noticed.
- Fixed in the new Worker with `TextEncoder` → bytes → base64url. Folded into the cross-Worker tracking ticket (OOM-127) so the prod Worker gets the same fix.

**How to apply:**

1. When Codex (or any reviewer) flags a finding in code you ported verbatim from a sibling, **check the sibling first**. Run the same grep, check git history. If the bug is there too, the finding is more important, not less.
2. Two paths, ordered:
   - **Same-PR backfix** (default): patch the original in the same PR if the sibling lives in the same repo and the fix is small. Two-commit PR; the second commit fixes the original.
   - **Tracking ticket** (sibling lives in a different repo, or fix needs coordinated deploy across services): open a ticket with concrete acceptance criteria + reference to the Codex finding. Don't ship "we know it's there" silently — that's the lazy path that lets the bug rot in production.
3. NEVER ship "fix the new copy, leave the original broken, no ticket". That's silent decay of production while the polished port ships.
4. The PR body / commit message should explicitly call out the sibling bug + tracking artifact. Reviewers should not have to discover this in the diff comments.

**Skip-when:** the sibling is genuinely retired / on its way out (already has a replace-with-new-thing ticket). Then the fix goes on the migration path, not on the dying sibling.

Related: [[no-security-theater]], [[jm-oom-parity-surfaces]].
