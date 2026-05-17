---
name: jm-oom-parity-surfaces
description: "Tools that ship in parallel JM/OOM pairs (setup_{jm,oom}_*, op-*-{jm,oom} helpers, agent profiles) drift silently — when editing one, audit the sibling in the same PR"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b59ead49-7cfe-45eb-9b61-39053ef15c75
---

Several home-lab tooling surfaces ship as parallel JM/OOM pairs:

- `services/tickets/scripts/setup_{jm,oom}_linear.py` — Linear team/view/label setup
- `~/.zshrc` `op-{linear,sentry,...}-{jm,oom}` 1Password helper pairs
- `services/tickets/tickets/config.py` `PROJECTS["JM"|"OOM"]` ProjectConfig entries
- `.claude/agent-profiles/code.yaml` (oneonme) and equivalent home-lab profile
- `/jm-*` vs `/oom-*` slash command pairs (e.g. `jm-linear-groom` / `oom-linear-groom`)

**Rule:** when editing one half, grep for the sibling and update it in the same PR. If the change is structural (new view, new state, new label, new env var), add a brief cross-org parity comment to BOTH files pointing at each other.

**Why:** validated 2026-05-17 — `setup_oneonme_linear.py` defined the legacy `A1/B1-B4/C1-C4/All Awaiting Review` view scheme. JM workspace adopted a new `0·`/`1·`/`A·` scheme; OOM's canonical views were manually authored to match, but the setup script never got the port. Result: 11 orphan views in OOM Linear that kept being re-created on every script run, parked alongside the canonical ones with no descriptions. Cleanup required script rewrite + 11 customViewDelete mutations + config.py review_view_url update.

**How to apply:** before merging an edit to any `*_jm_*` or `*_oom_*` file in `jm-home-lab/services/tickets/`, `jm-home-lab/services/*/`, or sibling slash-command files in `~/.local/share/chezmoi/`, run `rg -l '<basename-with-other-org>'` and inspect for parallel drift. If the surface doesn't logically need a sibling (genuinely org-specific), say so in the commit message so the absence is explicit.

**Long-term:** extract shared scheme into a module when the same data structure (e.g. REQUIRED_VIEWS list) ships in both scripts. See [[project_oom_account_naming]] for the account/credential side of the same parity concern.
