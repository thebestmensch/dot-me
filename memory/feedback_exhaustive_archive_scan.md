---
name: exhaustive-archive-scan
description: "When ingesting an opaque archive (LinkedIn export ZIP, Slack dump, takeout bundle, mbox), do a FULL inventory pass before declaring data-missing. Files with non-obvious names (Ad_Targeting.csv, Endorsement_Received_Info.csv) often carry the goldmine; surface-skim hits the famous files and asks the user for what's already in the archive."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 355b2c93-b128-4fa4-badd-7c14719f940f
---

When the user hands over an opaque archive (multi-file ZIP, takeout bundle, exported dataset), the failure mode is "scan the file names you recognize, skip the ones you don't, declare gaps based on the recognized subset."

The recognized files are usually the famous ones (Profile.csv, Contacts.csv). The non-obvious files are where the actual goldmine lives — aggregated targeting CSVs, endorsement metadata, indexed activity logs. Asking the user for data that's already in those files is the exact "James shouldn't have to tell me his work history" failure mode.

**Why:** Validated 2026-05-18 during James's bio draft. He requested his LinkedIn Basic export. Initial scan read `Profile.csv` (no positions field), `Skills.csv`, `Honors.csv`, `Recommendations_Received.csv` — concluded "no employment history, ask user." User pushed back: *"you have my linkedin, why cnant you use that?"* Re-scan caught `Ad_Targeting.csv`, which contained: every past employer (Google, Yonder/New Knowledge, Tembo, Libra APIs, etc.), education (Villanova CS 2013), years of experience (12+), past job titles, and Companies Followed (Magnifai et al.). Every employment question I'd been about to ask was answered there.

Then later in the same session: again asked James about chronology (when was Google between which gigs). He flagged: *"you shouldnt have to ask me about the chonology — you have my linkedin info."* Partial: chronology with exact dates lives in Full-export `Positions.csv`, not Basic. But the SHAPE of "ask before exhausting the data" was the same recurring bug.

**How to apply:**

- **Step 1 on any opaque archive ingest**: `ls -lah <dir>/` for inventory, `wc -l <each-csv>` for size, brief read of the FIRST FEW LINES of every file — including the ones with cryptic names — before forming a plan.
- For ZIPs from large platforms (LinkedIn, Twitter/X, Slack, Google Takeout): assume there's a "summary" or "aggregated" file with a non-obvious name carrying the cross-cuts. LinkedIn's is `Ad_Targeting.csv`. Slack's is `users.json`. Twitter's is `account.js`. Find it before asking gap questions.
- Note tier limits explicitly: LinkedIn Basic ≠ Full (see [[reference_linkedin_export_tiers]]). If a tier doesn't carry a field, state that — don't ask the user to provide what no tier of their data export contains.
- **Gap declaration discipline**: before "I don't have X, can you tell me?", run a grep across the archive for the field name AND its likely synonyms (`employer | company | position | role | tenure`). If the grep is silent, then ask.

**Anti-pattern:** scanning 3-4 files, declaring "data missing," asking the user, then getting pushback. Recovery is fine (re-scan, find the missed file). But each instance burns trust. James's reaction was rightly *"this is the second time, fix the pattern."*

**Adjacent:** opaque archives often include format-spec or schema files (`README.md`, `data-key.csv`, `manifest.json`) that list every field across every file. Read those first if present — they make the inventory pass trivial.

Related: [[reference_linkedin_export_tiers]] (LinkedIn Basic vs Full file inventories), [[feedback_landscape_scan_before_bulk_creative]] (broad-survey discipline; this rule is the data-input analog of that creative-output rule).
