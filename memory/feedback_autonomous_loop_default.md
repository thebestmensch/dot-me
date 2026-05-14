---
name: autonomous-loop-default
description: "When designing routine-loop workflows (PR ping-pong, session cleanup, batch processing), default to full autonomy including the irreversible end action — escalate only on named ambiguity triggers, not by default at each step."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7f41bc92-bb53-4732-9687-6748e6ed8711
---

When designing routine-loop workflows for JM (PR ping-pong, session cleanup, batch processing, anything with a clear convergence condition), default to **full autonomy including the irreversible end action**. Don't hand back at the last step unless there's genuine ambiguity.

**Why:** JM is hands-off on routine work. The whole point of a workflow command is to remove user-in-the-loop friction; stopping at the obvious-next-mechanical-step ("ready to merge — you click the button") defeats the purpose. Validated 2026-05-14: drafted `/jm-pr` with "stop at merge boundary" guardrail by default; JM corrected to fully autonomous including `gh pr merge --delete-branch`.

**How to apply:**
- Identify the convergence condition (PR green + all comments resolved; clean tree + no background procs).
- Identify the obvious-next-action when conditions are met (merge, delete branch, clear stash).
- Identify the genuine ambiguity points (contentious review, ambiguous conflict, missing approval, repeat-finding loop) — these are escalation triggers, not default hand-back points.
- Make escalation triggers explicit and enumerable. Lazy escalation criteria ("when stuck") either fire constantly or never; named triggers make the autonomy boundary auditable.
- Hard limits still hold: never force-push, never self-approve, never bypass codex-stop-gate, never act on human review comments autonomously.

Related: [[voice-for-outgoing]] — same shape; JM owns the output, the workflow doesn't ask for sign-off at each step.
