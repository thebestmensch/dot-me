---
name: permissions-automode-schema
description: "`permissions.autoMode.{allow,soft_deny,hard_deny,environment}` arrays let user add prose rules that steer the auto-mode classifier; `$defaults` sentinel inherits built-ins"
metadata: 
  node_type: memory
  type: reference
  originSessionId: d621c5e0-55ea-47c4-9999-23ff3ca9c00c
---

`~/.claude/settings.json → permissions.autoMode` accepts four optional string arrays — same structure as the classifier's built-in prompt sections:

- `allow`: rules describing what counts as routine, not credential/security exploration
- `soft_deny`: destructive/irreversible actions user intent can clear
- `hard_deny`: security boundaries user intent does NOT clear
- `environment`: facts about the user's setup the classifier should know

Each array accepts the literal sentinel `"$defaults"` to inherit the built-in rules at that position. Without `$defaults`, the user-authored entries REPLACE the built-ins for that section — usually not what you want.

**Example shape** (do not apply via the model — see [[feedback_no_self_authored_classifier_rules]]):

```json
"permissions": {
  "autoMode": {
    "allow": [
      "$defaults",
      "<user-authored prose>"
    ]
  }
}
```

**When to surface a diff:**
- Classifier blocks documented workflow that should be routine (e.g. dual-org 1Password SA token reads).
- Classifier blocks repeatedly across sessions for the same legit pattern — signal that the rule belongs in the user's permanent classifier config.

**When NOT to surface:**
- One-off block where user intent expressed in a follow-up message will clear it.
- Block that the user agrees is correct on inspection.

Discovered 2026-05-19 during OOM-deploy-notif-summary (settings.json schema dump via `update-config` skill).
