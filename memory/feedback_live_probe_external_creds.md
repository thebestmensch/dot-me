---
name: live-probe-external-creds
description: "When designing a fix around external credential systems (1Password, AWS IAM, GCP roles, Stripe keys), run live probes BEFORE settling on a fix shape — assumed scope drifts silently from documented/template scope."
metadata:
  node_type: memory
  type: feedback
---

When designing a fix around an external credential system, run **live probes** against the actual current state before settling on the fix shape. Assumed scope (from templates, .env files, code comments, memory notes) drifts silently from real scope.

**Why:** Credential systems' state isn't authoritatively visible from inside the repo — it's stored in the credential platform (1P vault grants, IAM policies, OAuth client configs). Templates and .env.template files capture the AUTHOR'S intent at write time, not current reality. A `op://oneonme/...` reference in a template doesn't mean a vault named `oneonme` exists today. The fix you'd design for the assumed state could be wrong in surprising ways.

Validated 2026-05-19 (workspace-restructure audit):
- Drafted a `op-oneonme` shell wrapper assuming the OOM SA token had read access to the `oneonme` vault, because `services/linear-agent/.env.template` referenced `op://oneonme/...`.
- User prompted "are you assuming the op flows work or did you verify?"
- Ran `OP_SERVICE_ACCOUNT_TOKEN=<oom-token> op vault list` → only `dev` + `machine` vaults granted, no `oneonme`.
- Further probe: `OP_SERVICE_ACCOUNT_TOKEN= op vault list --account oneonme` → revealed NEW org has no `oneonme` vault AT ALL; deprecated org did. All `op://oneonme/...` refs are stale and need rewriting to `op://machine/...`.
- The fix shape changed dramatically: from "make the wrapper work with the existing refs" to "the refs themselves are broken, sweep them."

**How to apply:**

- When the fix involves a credential system, BEFORE writing fix code: list every consumer (grep `op://`, `aws_iam_role`, `gcp_service_account`, `STRIPE_SECRET_KEY`, etc.), then live-probe each one's actual access.
- For 1Password specifically: `OP_SERVICE_ACCOUNT_TOKEN=<token> op vault list` for SA scope; `OP_SERVICE_ACCOUNT_TOKEN= op --account <shorthand> vault list` for app-account scope (see [[reference_op_cli_quirks]] for why the unset is required).
- Probe with `>/dev/null 2>&1; echo $?` to check existence without dumping credential contents — the auto-mode classifier rejects credential echoes.
- If the probe shows the assumed state is wrong: STOP and re-scope the plan. Don't paper over the gap.
- Related: [[feedback_verify_scheduled_handoff_path]] (grep beat_schedule before asserting handoff path), [[feedback_corpus_research_specificity]] (broad survey underestimates), [[feedback_flip_condition_is_a_tell]] (when reasoning says "if X then drop entire plan," X is usually the actual state).
