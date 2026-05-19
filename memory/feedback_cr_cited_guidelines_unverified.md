---
name: cr-cited-guidelines-unverified
description: "Automated reviewer findings that cite \"coding guidelines\", \"repo conventions\", or \"current docs\" often hallucinate the source; survey precedent before fixing. Applies to CodeRabbit and Codex."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b845a7f2-95e8-4d39-abd3-0b1541e15bb0
---

When an automated reviewer (CodeRabbit, Codex, etc.) cites a "coding guideline", "repo convention", or "current documentation" as justification for a finding, that citation is often invented from generic best-practices or stale training data, not a guideline that actually exists in the repo or the platform's current schema. Verify the cited source against live precedent before applying the fix.

**Codex variant (2026-05-19, oneonme-claude-plugins PR #13):** Codex flagged HIGH-severity "Plugin MCP server is declared at the wrong JSON level" citing "Claude Code's current docs show plugin `.mcp.json` files using an `mcpServers` wrapper." The existing `oneonme-database/.mcp.json` in the same marketplace ships WITHOUT the wrapper, and its tools (`mcp__plugin_oneonme-database_oom-db__*`) were demonstrably registered in the current session. Codex citing "current docs" was wrong for the Cowork plugin marketplace schema; precedent in the same repo won. Don't let HIGH severity tags rush a fix when in-repo precedent contradicts the citation.

**Why:** 2026-05-17 on thebestmensch/dotfiles#27, CR flagged a missing `set -o errexit` in a new hook as **CRITICAL** with the text "As per coding guidelines: Shell scripts should use `set -o errexit -o pipefail`." Survey of 45 sibling hooks in the same dir: 14 use `set -o pipefail` only, 1 uses `set -euo pipefail`, ~30 use neither. The repo `CLAUDE.md`'s shell guidance only covers `-y` non-interactive defaults and stdout+stderr capture — no mention of `errexit`. The "coding guideline" was CR's invention; pushback was correct on that count alone.

**Secondary lesson (from the memory PR's own CR review):** the first pushback stacked a second justification: "adding `set -e` would also have broken the hook because `[ -z "$x" ] && exit 0` returns 1 on a falsy test." That technical claim was wrong. Per POSIX, `set -e` is ignored for any command in an AND-OR list except the final one, so the falsy `[` test does NOT abort the script. CR caught this on the memory PR for the lesson itself. When stacking justifications, the strongest single reason wins; bonus reasoning that turns out to be wrong gives the reviewer a separate finding to chase and weakens the correct primary point.

**How to apply:** For any CR finding that invokes a guideline, convention, or "as per", grep the cited source (project `CLAUDE.md`, `.coderabbit.yaml`, sibling files in the same dir) before action. If the guideline isn't there, push back with the survey results + a verbatim quote of what the source actually does say. Don't let the CRITICAL severity tag rush a fix — CR's severity classifier reflects internal scoring, not project impact.

See also [[house-style-precedence]] in `/jm-pr` skill (project CLAUDE.md > existing code patterns > CR suggestion).
