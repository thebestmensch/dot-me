---
name: james-in-prose-not-jm
description: "Use \"James\" in memory bodies, descriptions, and frontmatter prose. \"JM\" is shorthand for command prefixes (jm-voice, jm-blog-publish), index labels, and tags — never the prose subject."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 355b2c93-b128-4fa4-badd-7c14719f940f
---

`identity.yaml::preferred_name: James`. Prose content referring to the user as the subject should call him "James," not "JM."

"JM" is a workspace shorthand with three valid uses:

- **Command prefix**: `/jm-voice`, `/jm-blog-publish`, `/jm-precompact`, `/jm-retro`, `/jm-commit`, etc.
- **Index/tag/category labels**: "JM workspace", "JM's home-lab repo", "JM project memory dir". These are scoping labels, not subjects.
- **Cross-account disambiguation**: `jm` vs `oom` accounts, sessions, configs. Lowercase, technical context.

"JM" is NOT valid as a prose subject. The following are bugs:

- ❌ "JM's partner"
- ❌ "JM is a cofounder"
- ❌ "JM prefers warm colors"
- ✓ "James's partner"
- ✓ "James is a cofounder"
- ✓ "James prefers warm colors"

**Why:** Caught 2026-05-18 mid-bio session while drafting memory entries for Sarah's handles + a feedback memory file. Draft descriptions read "Sarah is JM's partner" and "Sarah, JM's partner" — workspace-jargon shape rather than personal-context-data shape. The spec already encoded the right answer (`preferred_name: James`), so the bug was in the prose pipeline, not the data.

**How to apply:** before committing any memory write (body or frontmatter description), scan for "JM's" / "JM was" / "JM is" / "for JM" — if it's prose about the person, replace with "James." Leave command names (`/jm-voice`), file path conventions (memory file naming doesn't use jm prefix anyway), and tag labels alone.

**Adjacent rule:** the `oom` shorthand pairs with `jm` (workspace/account disambiguation) and follows the same scoping rule — lowercase for technical contexts, "OneOnMe" in prose. Existing memory `project_oom_account_naming.md` already uses both correctly; this rule generalizes the pattern to all user-as-subject prose.

Related: `~/.me/identity.yaml` (`preferred_name` field is the source of truth), [[user_favorite_color]] (other prose memory that should follow this convention).
