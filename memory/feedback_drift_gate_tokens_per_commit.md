---
name: drift-gate-tokens-per-commit
description: "`commit-on-drifted-branch-guard.sh` bypass tokens (`skip_commit_drift_gate` + `bypass_commit_drift_approved`) are consumed per-commit. Multi-round CR fixes on a drifted branch require re-priming both tokens each commit, and the first attempt after a fresh prime typically fails (race). Second attempt succeeds."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4838f494-2343-41e7-914d-e8e0b29801f3
---

The `commit-on-drifted-branch-guard.sh` bypass is single-shot per commit, not per-session.

**Why:** OOM-70 plugins PR #8 needed 5 CodeRabbit rounds. Each round, JM had to re-approve the bypass in their shell before CC could commit the fix. First commit attempt after fresh approval consistently failed (mtime race between gate evaluating tokens and the fresh `echo > skip_commit_drift_gate` write). Second attempt right after consistently passed. Same pattern as the codex pre-commit-gate mtime race documented in `codex-dispatch.md` gap #9.

**How to apply:**
- When starting a multi-round CR loop on a drifted branch (primary checkout NOT on a `jm/`- or `james/`-prefixed canonical branch): plan for re-priming the bypass once per CR round
- Each round: tell JM the inline path the gate emits (`/tmp/cc-gates/$SID/skip_commit_drift_gate` AND `…/bypass_commit_drift_approved`), wait for approval, then attempt commit
- Expect the first commit attempt to fail with "results have not been retrieved" or stale-mtime style errors. Refresh both tokens (`echo '<reason>' >` each) and re-attempt immediately
- Don't pre-augment `edited_files` or fabricate token writes. The auto-mode classifier (correctly) flags that as a safety-check bypass
- Bare token rule: "first attempt fails after fresh bypass, touch bypass + retry once" (same shape as codex gap #9)

Related: [[chezmoi-pr-workflow]], [[parallel-cc-single-writer]], [[enforce-via-hook-when-memory-fails]].
