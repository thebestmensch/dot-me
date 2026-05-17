---
name: oss-post-discipline
description: Outbound posts to external OSS repos under @thebestmensch must run through /jm-oss-post (template fetch + /jm-voice --pro pass). Memory alone failed; enforced by oss-post-gate.sh hook.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b845a7f2-95e8-4d39-abd3-0b1541e15bb0
---

When posting issues, PRs, or comments to external repos (anything outside own-orgs: thebestmensch, OneOnMe, Otterplan, threatcare, noahjs) as `@thebestmensch`, use `/jm-oss-post`. It (1) fetches and conforms to the repo's `.github/ISSUE_TEMPLATE/*` or `PULL_REQUEST_TEMPLATE.md`, (2) pipes the body through `/jm-voice --pro`, and (3) searches for duplicates.

**Why:** On 2026-05-17 I filed `anthropics/claude-code#60063` with raw `gh issue create` — no template check (the repo has a `feature_request.yml` form with required Problem / Solution / Priority / Category sections that I skipped) and no voice pass (em-dashes throughout, AI-shape padding). The memory rule [[voice-for-outgoing]] says "always invoke `/jm-voice` when drafting any text sent as James" but it didn't fire because I bypassed it. Memory rule alone wasn't enough.

**How to apply:** `/jm-oss-post issue|pr|comment <owner/repo-or-url>`. The `oss-post-gate.sh` PreToolUse hook blocks raw `gh issue/pr create|edit|comment` against external repos unless `/tmp/cc-gates/$SESSION_ID/oss-post-ok` exists (skill writes it on success). Own-org repos bypass the gate. Bypass mechanism for mechanical retries: write a reason to the marker path; "skipping voice" is not a valid reason.

See also [[voice-for-outgoing]] (the broader voice rule), [[voice-register-routing]] (`--pro` routing), [[chezmoi-pr-workflow]] (how the skill + hook got deployed).
