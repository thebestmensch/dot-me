---
name: codex-resolution-drift-verify
description: "Codex findings about transitive-dep resolution drift (singleton splits, peer-dep conflicts) describe a *direction of risk*, not necessarily current state — verify actual install layout before reverting wholesale"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5b0ab023-7db0-4994-9078-1c755e40bf61
---

When Codex flags a HIGH-severity finding about resolution drift — singleton splits, peer-dep version mismatches, "package X and Y will end up at different versions" — the finding is often **directionally correct but state-uncertain**. The reviewer reads manifests and lockfile entries; it doesn't always inspect the actual `node_modules` / venv layout that ships.

**Why:** On 2026-05-19 (PR #108 dep bumps), Codex returned HIGH on `@react-navigation/*` bumps splitting the singleton vs expo-router 6.0.23's internal pins. The fix-as-instructed was to revert the three nav bumps. Investigation found that with both root manifest and expo-router's internal manifest at `^7.x`, npm/bun semver deduplication actually produced one installed copy (7.1.28) in the immediate state. The finding was right about *future drift* (bumping root past `^7.x` would split), wrong about *current breakage*. Reverting was still the right call — the dedup is fragile and would split on the next registry update — but the verification step matters for sizing the fix.

**How to apply:**

1. When Codex returns a HIGH resolution-drift finding, run the actual install (`bun install` / `uv sync`) and inspect:
   - `node_modules/<pkg>/package.json` vs `node_modules/<host-pkg>/node_modules/<pkg>/package.json`
   - For Python: `uv tree --depth 2 <pkg>` to see effective resolved versions
2. If only one copy is installed today, the dep-graph math is dedup'd at this snapshot. The risk is forward-looking, not current-state.
3. Still fix it, but the framing changes: "preventing future drift" not "currently broken." Commit message should reflect that — overstating "broken now" makes the diff harder to land.
4. If you can't verify (no `node_modules`, fresh worktree), state the assumption explicitly in the commit message rather than asserting current breakage.

**Don't:**
- Dismiss the finding as false-positive because the install happens to dedup right now. Drift is real.
- Re-dispatch Codex to "ask if it really meant current state vs future drift" — that's loop-drain per [[codex_dispatch]].

Related: [[reference_uv_prerelease_block]] (another uv/bun gotcha), `~/.claude/rules/codex-dispatch.md` (codex protocol).
