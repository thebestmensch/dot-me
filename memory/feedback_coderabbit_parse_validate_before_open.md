---
name: coderabbit-parse-validate-before-open
description: "Validate `.coderabbit.yaml` against CodeRabbit's schema before opening any PR that modifies it. `yaml.safe_load` only proves the file parses. CR silently rejects schema-invalid configs and applies defaults, leaving all custom rules inert."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4838f494-2343-41e7-914d-e8e0b29801f3
---

Before opening any PR that adds or modifies `.coderabbit.yaml`, validate against CodeRabbit's schema, not just YAML grammar.

**Why:** OOM-70 R1 had a 66-character `custom_check.name` (CR's schema cap is 50). YAML parsed fine via `uv run --with pyyaml python -c "yaml.safe_load(open('.coderabbit.yaml'))"`, but CR silently rejected the entire config on the PR. Defaults applied, every custom rule went inert. Cost ~30 min and a full CR ping-pong round before the cap surfaced.

**How to apply:**
- Run the validator at `https://docs.coderabbit.ai/configuration/yaml-validator` (or equivalent CR-hosted schema check) before pushing the branch
- `yaml.safe_load` is necessary but not sufficient. It confirms grammar, not schema conformance
- CR failures are silent by design in some PR states (no `/coderabbit configuration` summary comment on schema-invalid configs), so absence of CR config-feedback is NOT proof the config landed
- After merge, spot-check by reading a fresh CR review on a subsequent PR and confirming the custom rules fire (cite-back behavior)
- Applies to any repo with `.coderabbit.yaml` at root: oneonme-platform, oneonme-claude-plugins, dot-me, home-lab

Related: [[cr-cited-guidelines-unverified]], [[chezmoi-pr-workflow]].
