---
name: explicit-verb-over-flag
description: Prefer dedicated slash command over flag/mode toggle when the variant has its own muscle-memory verb
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0d3a3ce3-443f-4646-9f43-c3c2d35d6eb5
---

When proposing a new variant of an existing slash command, default to a dedicated command (e.g. `/jm-precompact`), not a flag on the parent (e.g. `/jm-retro --pre-compact`) — even at the cost of some duplication.

**Why:** JM said directly: "the flag is too implicit". Slash commands are muscle-memory triggers; a flag hides the variant inside the parent's help and demands the user remember both the parent name and the modifier. A dedicated verb is one keystroke pattern, discoverable in the command list, with its own description line.

**How to apply:**
- New variant of a `/jm-*` command → propose dedicated command as default, mention flag-on-parent only as a runner-up
- Reduce duplication via cross-reference inside the body ("Follow `/jm-retro` § N"), not by hiding the variant behind a parent flag
- Exception: variants that are genuinely tiny modifier knobs with no distinct workflow shape (e.g. `--dry-run`, `--verbose`) stay as flags

Related: [[chezmoi-pr-workflow]] for the PR-not-direct-commit pattern when shipping these.
