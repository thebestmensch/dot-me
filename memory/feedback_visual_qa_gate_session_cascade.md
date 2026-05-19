---
name: visual-qa-gate-session-cascade
description: "A single UI .tsx/.css edit in any worktree fires the visual-qa stop-hook gate for ALL subsequent commits in the same session, including unrelated API/backend work"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 63d1fd25-0f4a-4674-950e-223180f08d05
---

**Rule:** In multi-fix CC sessions, sequence UI changes (`.tsx` in `components/`, `app/`, `ui/`) LAST — or split UI work into a separate session entirely. Once a UI file lands in `edited_files`, the visual-qa stop-hook gate (`~/.claude/hooks/visual-qa-stop-gate.sh`) blocks every subsequent commit attempt this session until cleared, even commits touching no UI.

**Why:** The session's `edited_files` tracker at `/tmp/cc-gates/$SESSION_ID/edited_files` is path-accumulating across worktrees, not commit-scoped. Validated 2026-05-19 on OOM-105 (FriendRequestsSheet.tsx restructure): blocked OOM-88 (pure API), OOM-93, OOM-94 from committing in the same session despite those diffs touching zero UI. Background sessions can't run `/visual-qa` (no sim, no screenshots), so once the cascade triggers in bg, every remaining fix is gated behind a user-approved bypass.

**How to apply:**
- When planning a multi-fix bg session, queue UI fixes LAST after API-only fixes have shipped.
- If a UI fix is the only one possible and others remain, expect the cascade — surface it up front rather than mid-session.
- The `skip_visual_qa_gate` bypass requires `/visual-qa` or `/code-review` skill invocation as a prereq (see [[stop-hook-bypass-prereq-invocation]]), then user approval via `bypass_approved`.
- Save uncommitted work as `git diff > .claude/<ticket>-<slug>.patch` so user can `git apply` after bypass.
