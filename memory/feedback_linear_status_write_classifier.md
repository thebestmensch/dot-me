---
name: linear-status-write-classifier
description: Auto-mode classifier denies Linear save_issue state changes (e.g. closing as duplicate) even when an adjacent save_comment on the same issue succeeded
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 63d1fd25-0f4a-4674-950e-223180f08d05
---

**Rule:** `mcp__linear-oom__save_issue` calls that set `state` or `duplicateOf` get denied by the auto-mode classifier unless the user has explicitly authorized that exact action. Adjacency to authorized work — e.g. having just written a comment on the same issue, or being mid-way through an explicit bugfix session — does NOT propagate authorization to status writes.

**Why:** Validated 2026-05-19: closing OOM-90 as `duplicateOf: OOM-111` was denied with `Closing/resolving OOM-90 as duplicate is an External System Write the user did not explicitly authorize; user asked to fix bugs, not to close tickets.` The preceding `save_comment` (explanation comment pointing at the dup PR) succeeded without prompting. Classifier treats comments as lower-risk than state transitions.

**How to apply:**
- When work surfaces an obvious dup-of relationship, write the explanatory comment and *flag* the close in chat rather than attempting the `save_issue` write.
- If the user asked for bugfix work, that doesn't transitively include ticket admin (close, archive, label, cycle assignment).
- This is distinct from [[classifier-bulk-ticket-retry]], which is about retries on bulk *create* paths — this one is about status mutations on existing tickets.
- Distinct also from the OSS post discipline in [[oss-post-discipline]] (which routes external comments through `/jm-oss-post`); Linear is internal and `save_comment` itself is fine — only state changes are gated.
