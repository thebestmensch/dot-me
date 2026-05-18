---
name: linkedin-export-tiers
description: "LinkedIn data export has two tiers — Basic (~250KB, instant) and Full (24hr wait, much larger). Basic LACKS Positions.csv / Education.csv / Projects.csv / Certifications.csv. Ad_Targeting.csv (in Basic) carries aggregated career info but NOT explicit job date ranges. Default to requesting Full when chronology matters."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 355b2c93-b128-4fa4-badd-7c14719f940f
---

LinkedIn data exports are tiered. Both are requested from `linkedin.com/mypreferences/d/download-my-data`. The user picks tier at request time.

## Basic export

- **Size**: ~250KB (varies by user)
- **Wait**: instant, ZIP ready within seconds
- **Use case**: quick sanity check; non-employment-history needs

**Files included (verified 2026-05-18 on James's export):**

| File | Carries |
|---|---|
| `Profile.csv` | Single-row name, headline, current location, summary, industry, postal code, twitter handle, website. **No employment history.** |
| `Skills.csv` | Listed skills, no endorsement counts |
| `Endorsement_Received_Info.csv` | Per-skill endorsement metadata |
| `Honors.csv` | Self-reported honors/awards |
| `Recommendations_Received.csv` | Full text + author + author title + author company + date |
| `Recommendations_Given.csv` | Same shape, outbound |
| `Ad_Targeting.csv` | **The goldmine.** Aggregated career profile: Company Names (past employers), Company Follower of, Education (school + degree + year), Years of Experience bucket, Job Seniorities, Job Titles, Member Schools. NO explicit date ranges. |
| `Connections.csv` | First-name + last-name + email (if visible) + connected-on date |
| `Articles/Articles/*.html` | Long-form posts authored by user, each with publish date in filename or frontmatter |
| `Email Addresses.csv` | All emails associated with account |
| `Jobs/Job Applications.csv` | Applications made via LinkedIn Easy Apply |
| `Rich_Media.csv` | Uploaded media attachments |
| `Registration.csv` | Account registration date + IP |

## Full export

- **Size**: 5-50MB (varies; James's not yet validated)
- **Wait**: ~24 hours (LinkedIn emails when ready)
- **Use case**: any task needing explicit job-date chronology, education-by-year, certifications, projects, courses, languages, patents, organizations

**Additional files (per LinkedIn's public archive docs):**

- `Positions.csv` — past + current jobs with explicit start/end dates, titles, companies, descriptions, locations
- `Education.csv` — schools with explicit start/end years, degrees, fields of study, activities
- `Projects.csv` — listed projects with dates + collaborators
- `Certifications.csv` — licenses + certifications with issuers + dates
- `Courses.csv` — listed coursework
- `Languages.csv` — languages + proficiency
- `Patents.csv` — patents authored
- `Organizations.csv` — listed affiliations
- `Volunteering.csv` — volunteer history with dates
- `Messages.csv` — full InMail / messaging history
- `Activity feed` JSON exports of likes / comments / shares

## Critical gap to know

**Basic does NOT carry explicit job dates.** `Ad_Targeting.csv`'s "Company Names" column is an unordered list of all past employers — no tenures, no sequence guaranteed. To infer chronology from Basic alone, cross-reference:

1. Article publish dates (`Articles/Articles/*.html` filenames + body datelines)
2. LinkedIn account creation date (`Registration.csv` — proxies "professional career started ≤ this date")
3. Education year (`Ad_Targeting.csv` "Member Schools" — proxies "career started ~here")
4. User's own statements in chat

This is brittle. Default to requesting Full when chronology matters.

## What no LinkedIn tier carries

- **Other social handles** (Instagram, Bluesky, personal site URLs not on LinkedIn profile)
- **Family/relationship info** (partner, kids, etc. — LinkedIn doesn't store this)
- **Income or compensation**
- **Manager / org-chart context** for past roles
- **Performance reviews / internal documents** from prior employers

These have to come from other sources (user statements, separate exports from other platforms, dot-me identity fields).

## How to apply

- **Default**: if the task is "fill in James's work history" or "draft a bio that needs chronology" → request **Full** export. 24hr wait is acceptable for high-stakes content.
- **Basic is fine for**: voice samples (use Articles/), endorsement context, connection-graph queries, quick "what skills are listed" lookups.
- When given a Basic export and asked for chronology: state the gap explicitly, infer what you can from article dates + user statements, then ask the user to do a Full request as followup if precision matters.
- Annotate JM-254 (the LinkedIn import automation ticket) to require Full as the supported input + carve out fields for personal handles (IG, Bluesky, etc.) since LinkedIn doesn't carry them.

## Validated

2026-05-18 on James's Basic export. `Profile.csv` had no positions field. `Ad_Targeting.csv` had every past employer (Google, Yonder/New Knowledge, Tembo, Libra APIs, Zoomer, Open Austin) plus education (Villanova CS 2013) plus 12+ years experience bucket — none of which I'd seen on first surface-scan. Chronology with explicit dates was NOT recoverable from Basic; James had to confirm "Google in between each" verbally because `Positions.csv` is Full-only.

Related: [[feedback_exhaustive_archive_scan]] (the meta-rule about full-inventory-before-asking on opaque archives; this reference is the LinkedIn-specific instance).
