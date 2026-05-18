---
name: dependabot-uv-ecosystem
description: "GitHub Dependabot has a dedicated `uv` ecosystem; `pip` doesn't regenerate `uv.lock` cleanly for uv-managed projects"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4838f494-2343-41e7-914d-e8e0b29801f3
---

Dependabot's `package-ecosystem` for uv-managed Python projects is `"uv"`, NOT `"pip"`. The `pip` updater documents `requirements.txt` and PEP-621 `pyproject.toml` support but does not regenerate the uv lockfile, so dependency PRs from the pip updater leave CI on a stale `uv.lock`.

Use `package-ecosystem: "uv"` whenever the project ships a `uv.lock`. The Dependabot `uv` ecosystem is documented in `dependabot-core/uv/` and supported on GitHub Cloud.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "uv"   # not "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

Verified 2026-05-18 via official docs (`/dependabot/dependabot-core` on context7). Caught a MEDIUM Codex finding on OOM-70 plugins-repo scaffold.

How to apply: writing any new `.github/dependabot.yml` for a Python project → `ls` for `uv.lock` first; if present, use `uv`; if only `requirements.txt`, use `pip`; if `poetry.lock`, use `pip` (poetry still goes through the pip updater) or check the latest Dependabot docs since this is evolving.
