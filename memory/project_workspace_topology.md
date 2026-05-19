---
name: workspace-topology
description: "Two workspaces (jm/personal + oom/oneonme), each with own Sentry org, 1Password vault, Linear team. Workspace creds shared across all projects within. Slash-command prefix (jm-*, oom-*) maps 1:1 to workspace."
metadata: 
  node_type: memory
  type: project
  originSessionId: 09717e22-dea9-457b-a70a-3a826cac9113
---

JM's work splits into **two workspaces**, each a self-contained namespace for credentials, tools, and slash commands:

- **jm / personal**: projects include `jm-home-lab`, `dot-me`, `personal-site`, chezmoi config repo. Workspace creds: jm Sentry org, jm 1Password vault (`james@jamesmensch.com`), jm Linear team.
- **oom / oneonme**: projects include `oneonme-platform` and any other OneOnMe repos. Workspace creds: oom Sentry org, oom 1Password vault (`james@oneonme.com`), oom Linear team.

**Workspace creds are shared across all projects within the workspace.** When `/jm-audit-sentry` runs in any jm-workspace project, it uses jm Sentry org. When `/oom-linear-new-ticket` runs, it uses oom Linear team. Never cross.

**Slash-command prefix = workspace tag.** `jm-*` commands assume jm-workspace creds; `oom-*` assume oom-workspace. Parity drift across the boundary is enforced by [[feedback_jm_oom_parity_surfaces]] — if a jm-* command exists for a workspace-level concern, the oom-* sibling should too (unless the underlying tool is workspace-exclusive).

**Why:** Identity isolation (preventing OneOnMe creds from leaking into personal Sentry, etc.) and parity-discipline for cross-workspace concerns (Linear flows, Sentry audits) where both workspaces have the same shape of need.

**How to apply:**
- "Why doesn't `/jm-X` exist in personal-site/dot-me?" → expected answer: chezmoi `dot_claude/commands/` is the workspace-level surface for jm-*. If it's not there, either it should be lifted or it's legitimately repo-pinned (Task Agent runbook, per-project deploy script, etc.).
- Lifting a `jm-*` command to chezmoi global = making it workspace-available across all jm projects. Same for `oom-*` on the oneonme side.
- When auditing a command for portability, check: does it call workspace-shared infra (Linear MCP, Sentry MCP, 1Password) or project-specific infra (`tickets new -p home-lab`, `heroku deploy`, repo-local services/)? Former = lift candidate, latter = legitimate pin.
- Related: [[project_oom_account_naming]] (account-level cred mapping), [[workspace-pattern]] (tmux session arrangement — orthogonal to workspace topology).
