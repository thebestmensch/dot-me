---
name: oss-launch-checklist
description: "Discipline checklist for JM-owned OSS launches — positioning, sequencing, validation, and pre-flight checks distilled from the dot-me v0.1 launch work"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 77e64a9b-48d4-481f-a5cc-0d3ab544bf99
---

When prepping any JM-owned OSS project for public launch (HN Show, Reddit, Twitter), run this checklist before scheduling the launch. Each item exists because skipping it has either burned dot-me's first launch attempt or has a documented failure-mode in adjacent projects (Prettier, AGENTS.md, devcontainer.json post-mortems).

**Why:** OSS launches are single-use top-of-funnel events. HN Show in particular is roughly one shot per project — the comment thread is durable and "thin launch" tags the repo in search for months. Discipline before launch is cheap; relaunching after a thin launch is expensive.

**How to apply:** Treat this as a gate before any external-facing launch action (HN post, Show HN, public tweet thread, dev.to post, paid promotion). If any item fails, defer the launch. None of these items needs to be done by me alone — research-agent, devils-advocate, tone-qa, and code-review cover most of them.

### Positioning

- Pitch defines problem and solution in plain self-contained terms; no "X for Y" framing in the elevator pitch (body comparisons are fine — see [[no-uber-for-x-positioning]])
- Reader's implicit competitor questions are answered inside the pitch's properties, not by naming competitors
- Comparison tables in README body are *truthful* — every column maps to a real differentiator; no row hides a hidden distinction (e.g. project-scoped vs user-scoped)
- Pitch read aloud has acceptable rhythm; JM-voice cadence matches `voice.md`

### Credibility floor

- v0.1 has at least two independent consumers, not just the author's reference plugin — "spec with one consumer" is the credibility-theater failure mode
- If positioning as a "standard" or "spec," there is a paper-shaped SPEC.md in the repo itself (not just a design doc in a sibling repo)
- Schema has a `schema_version` field from day 1; "additive-only" promise has a documented escape hatch for v2 breaks
- No naming collisions on npm, pypi, GitHub (verify directly, don't assume)

### Competitor scan

- Prior-art scan includes draft-stage standards, not just shipped ones — peers at v0.1 are competitors too (dot-me missed dotstandards.info initially)
- Where a competing draft exists, the README answers "why not just use that" inside the solution shape, without naming it head-to-head
- For each named competitor in the README's comparison table, the comparison is accurate enough to survive a hostile reader

### Cross-tool support

- Cross-tool install instructions cover only tools you've *actually tested*; tools you haven't tested are marked "contributions welcome," not silently included
- Demo asset (asciinema/screencast) shows the cross-tool story, not single-tool — single-tool demos undersell a multi-tool standard

### First-follower seeding

- 5-10 specific people identified by name who would publicly endorse before launch
- Outreach to those people happens *before* the HN clock starts, not after
- If <5 high-confidence names exist, the Prettier-style big-bang launch is not viable — switch to drip launch (Twitter/Bluesky over 2-4 weeks)

### Pre-flight validation

- HN war-game: top 5 hostile comments imagined, README/pitch answers each
- Cold-reader test: 2-3 humans who haven't seen the project read the pitch and can say back what it does
- Voice-fit check: pitch matches JM voice (run `tone-qa` or general-purpose against `voice.md`)
- HN title: 5+ candidates written, top 2 ranked; title carries 80% of click-through

### Launch venue selection

- Wrong venues: `r/programming` (low AI-tooling density), generic dev subreddits where the framing won't land
- Right venues (for AI-tooling-config niche): HN Show, `r/ClaudeAI`, `r/cursor`, Bluesky AI-tooling community, dev.to AI tags
- Timing: Tue/Wed AM US Central for HN; weekday for Reddit; threads on Twitter/Bluesky right after HN post submits

### Post-launch

- Issue tracker has 5-8 seeded issues so visitors don't see an empty Issues tab
- GitHub Discussions enabled, one thread seeded ("what fields are you adding that aren't in the spec?")
- Repository topics, homepage URL, description all populated — discoverability gaps cost nothing to close

### Anti-patterns

- Don't burn HN Show on v0.1 with one consumer; wait for v0.2 with two
- Don't lobby a foundation/governance body (Linux Foundation, AAIF) before the project has independent traction — reads as fragmenting an ecosystem they just unified
- Don't add schema fields before ≥5 outside adopters hit the gap — pre-emptive field bloat is the slow-death failure mode
- Don't ship "lite" cross-tool docs that haven't been verified — first hostile commenter who tries them becomes the top reply

Related: [[no-uber-for-x-positioning]], [[project_personal_context_repo]]
