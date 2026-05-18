---
name: semgrep-ce-vs-platform-invocation
description: "Semgrep CLI invocation differs by whether you have an AppSec Platform token; `ci` mode is platform-only, `scan --config auto` is the CE invocation"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4838f494-2343-41e7-914d-e8e0b29801f3
---

Semgrep has two GitHub-Actions invocation shapes, and they are NOT interchangeable:

- **`semgrep ci`** — for orgs using Semgrep AppSec Platform. Rules + policies are configured in the cloud UI (semgrep.dev). Requires `SEMGREP_APP_TOKEN`. Does NOT accept `--config=auto` as a flag in this mode.
- **`semgrep scan --config auto`** — Community Edition. Pulls registry rules. No platform account needed. Works in a bare GitHub Actions job using the `semgrep/semgrep` container image.

Common drift: training-data examples and old README copy show `semgrep ci --config=auto` which used to work and no longer does. If you want CE without the platform, write `semgrep scan --config auto` and pair with `continue-on-error: true` for first-week comment-only posture.

Switch to `semgrep ci` only after provisioning `SEMGREP_APP_TOKEN` and tuning policies in the cloud UI.

Verified 2026-05-18 via official docs (`/semgrep/semgrep-docs` on context7). Caught a HIGH Codex finding on OOM-70 plugins-repo scaffold; reference [[oom-claude-plugins-review-tooling-scaffold]] PR if the symptom repeats.

How to apply: writing any new `semgrep.yml` workflow → choose `scan --config auto` unless an `SEMGREP_APP_TOKEN` already exists on the target org.
