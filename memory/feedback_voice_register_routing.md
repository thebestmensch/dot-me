---
name: voice-register-routing
description: "Auto-route /jm-voice register flag by audience — pro for GitHub/external/strangers, default for internal chat, casual for DMs"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f62af1d4-c940-4835-817e-770363fc3e80
---

When invoking `/jm-voice` on James's behalf, pick the register flag from the audience automatically. Don't default to no-flag for every draft.

**Routing table:**

| Audience / surface | Register | Why |
|---|---|---|
| GitHub issue body (external/upstream repo) | `--pro` | Reader doesn't know JM. Casual register reads as unserious in a public bug report. |
| GitHub PR description (any repo) | `--pro` | PRs are durable artifacts; complete sentences age better than fragments. |
| GitHub PR comment on an external repo | `--pro` | Same reasoning — public, durable, audience is strangers. |
| GitHub PR comment on own repo / CodeRabbit replies | default | Internal — casual-work blend reads correctly. |
| Email to a stranger / cold outreach | `--pro` | Same reasoning as GitHub issues — first impression. |
| Email to known contact | default | Audience knows JM's voice. |
| Slack DM / channel reply (internal, known audience) | default or `--casual` | Default for work threads, casual for shitposting/reactions. |
| Slack DM to a new coworker / internal stranger (audience doesn't know JM yet) | `--pro` | First impression rule still applies even on internal Slack. Doesn't know your voice yet → write a properly-typed message. |
| Slack reply to external folks | `--pro` | External-facing → public-facing rules apply. |
| Multi-point structured update | combine with `--announcement` | `--announcement` composes: alone = default + structure, with `--pro` = pro + structure. |

**Why:** First-pass drafts default to corporate tone (which `--pro` is *not* — `--pro` is "default minus chat tics"). Register choice should match audience without JM having to remember the flag each time. See [[feedback_voice_for_outgoing]] for the parent rule about always using the skill at all.

**How to apply:** Before invoking `/jm-voice`, look at what surface the text is heading to. If it's GitHub (issue/PR body) or an external email, append `--pro`. If it's a structured update, append `--announcement` (compose with `--pro` if also external). Otherwise no flag.

**Tell-don't-ask exception:** If the audience is ambiguous (e.g. JM says "draft a comment on this thread" without specifying the repo), surface a quick "this looks like a PR comment on an external repo — using `--pro`" rather than guessing silently.
