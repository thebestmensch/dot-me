---
name: workspace-pattern
description: "JM works in the `agents` tmux session using Claude Agents project selector (e.g. @oneonme-platform, @jm-home-lab), not in the legacy `jm` / `oom` tmux session panes directly. The dedicated workspace panes are stale leftovers."
metadata: 
  node_type: memory
  type: project
  originSessionId: b82194bd-8b0d-4625-b3c0-ecd853f88d75
---

JM runs both OneOnMe and home-lab work from the **`agents` tmux session** via the Claude Agents UI project selector (`@oneonme-platform`, `@jm-home-lab`, etc.), not from the legacy per-workspace `jm` and `oom` tmux session panes. Those panes still exist but go unused.

**Why:** Single-pane multi-project flow is faster than session-switching. The launcher pane in `agents` is where active work happens; sub-chats spawn from there.

**How to apply:**
- When debugging tmux / HUD state: the `agents` window is the load-bearing one. `jm` / `oom` panes may be cold or broken in ways JM doesn't notice.
- Don't suggest "open it in your oom pane" unless work is project-scoped enough to warrant the dedicated session.
- HUD row 1 daemon-mode fallback (in [[workspace-layout]] / visor-hud.sh) is the primary path for `agents` — `jm` / `oom` panes use the ctx-mark hook path.
- Validated 2026-05-17: oom pane Claude wouldn't launch (post-Ghostty-update keychain ACL strip on `op-token-*` items), but JM hadn't noticed because all real work moved to `agents` session weeks prior.
