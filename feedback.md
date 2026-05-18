# Feedback

This file collects friction reports from beta-cohort adopters and consumer-tool builders. It's the input stream that shapes the next spec revision.

## How to leave feedback

- **Public** (preferred for spec / integration questions): file an issue using the *Spec clarification* or *Consumer tool integration* template. See [CONTRIBUTING.md](CONTRIBUTING.md).
- **Private** (security or personal-context concerns): email **james@jamesmensch.com**. See [SECURITY.md](SECURITY.md).
- **Anything else** (tone, sales pitch, "this confused me on first install", "wait, this is weird"): drop a one-paragraph note in this file via PR. PRs that just append to this file are welcomed without ceremony.

## What's most useful

Bias toward **concrete moments of friction**, not abstract critique:

- "I ran `/me init` on a fresh machine and got [error] because [reason]."
- "I tried to consume `~/.me/` from [tool X] and the spec was silent on [edge case Y]."
- "I read the README and didn't realize I needed [step Z]."
- "The Sam Patel template made me think this format is for [role], so I bounced."

One paragraph per item. Date + source not required.

## Live entries

### 2026-05-18, maintainer week-1 dogfood notes

After a week of using `~/.me/` as the only personal-context layer in front of Claude Code, Codex, and Gemini CLI, a few patterns showed up that shaped this round of tweaks. Logging here so adopters can see the friction shape rather than treating the format as finished.

- **`preferences.yaml` accumulates rules that aren't preferences.** Started with `commit_messages: Conventional Commits` and `recommendation_order: order by ROI` under a `workflow:` block. Both are imperative behavioral rules; they belong in `working-style.yaml`, not in the aesthetic-and-taste file. Moved them. If you find yourself writing "I prefer X" in preferences when you mean "do X", that's the signal it belongs one file over.
- **Universal reasoning patterns kept landing in `memory/` when they could be in `working-style.yaml`.** Flip-condition detection, two-layer tool evaluation, landscape-scan-before-bulk-creative: all started as private memory entries before getting promoted. Rule of thumb: if the rule applies to any user, not just James, it's working-style content; if it's contextual or high-cardinality ("when working on the home-lab dashboard, port 8050 is mapped to 8000 internally"), it stays in memory.
- **`voice.md` Format section needed a posture axis.** Mechanics (paragraph length, em-dashes, headings) didn't cover *what argument the page is making*. Added a "prescriptive over exploratory" subsection for long-form public writing, since readers landing on a post usually want the call made, not a survey.
- **Stale `spec_version` is a real footgun.** `identity.yaml` was pinned at `0.1` after v0.2 added seven fields, and `preferences.yaml` had no version at all. If you're building a consumer, the SPEC §5.1 escape-hatch advice (branch on `spec_version`) only works when the files actually carry one. Bumped both.
- **One thing the format does NOT yet solve cleanly:** when a tool reads `working-style.yaml` and `memory/` simultaneously, there's no precedence rule for conflict. In practice the imperative file should win, but the SPEC is silent. Flagging for the next revision rather than guessing now.

---

## Triage cadence

The maintainer reviews `feedback.md` entries before any spec revision. Themes that show up in multiple reports become candidate spec changes; single-report ideas land in the issue tracker for discussion.
