---
name: ruff-format-drive-by-churn
description: "Don't run `ruff format <whole_file>` after a few targeted edits inside a legacy-unformatted file — it reflows hundreds of unrelated lines and obscures the diff"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4aa78910-77ee-4e55-9493-ffce77b18920
---

Manual `ruff format <path>` formats the **entire** file, not just edited regions. On a tests file with lots of legacy unformatted content, this can produce a 700-line reformat diff for 6 lines of intent.

**Why:** Validated on OOM-34 (api/gifts/tests.py, 2026-05-17). After 6 targeted edits totaling ~150 lines, calling `ruff format` to clean up trailing-comma / quote-style inconsistencies in *my own additions* also rewrote ~700 lines of pre-existing code. Result: 712/-9 diff for a fix that should have been ~200 net additions. Had to `git checkout HEAD -- <file>`, re-apply targeted edits, skip the format step. Same trap on api/gifts/utils.py (155-line diff for ~120 lines of intent because the formatter collapsed multi-line function calls elsewhere).

**How to apply:**
- For files with substantive legacy unformatted content: do NOT manually invoke `ruff format <file>` after targeted edits. Let pre-commit / CI handle format-on-save scoped to actually-changed lines (or accept that the format pass is a separate concern).
- For new files or whole-file rewrites: `ruff format` is fine — there's nothing to churn.
- If pre-existing format inconsistency *blocks* a lint check on your changes, scope the fix narrowly: `ruff format --diff <file>` first to inspect what would change, then either accept it as a follow-up PR or revert + apply targeted edits without the format pass.
- The "every changed line should trace to the request" discipline applies to format passes too. Code-review reviewers waste time wading through reflow churn.

Related: [[no-emdashes]] is also a stylistic-discipline rule the formatter doesn't enforce.
