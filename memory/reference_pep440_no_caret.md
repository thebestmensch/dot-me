---
name: pep440-no-caret
description: "Caret (`^`) is Poetry/Cargo syntax, NOT valid PEP 440 / PEP 508. uv and pip use `~=` (compatible-release), `>=X,<Y` (bounded ranges), or exact `==`."
metadata:
  node_type: memory
  type: reference
  originSessionId: 4838f494-2343-41e7-914d-e8e0b29801f3
---

The caret operator (`^1.2.3`) is Poetry and Cargo syntax. It is NOT part of PEP 440 (version specifiers) or PEP 508 (dependency specification). uv- and pip-managed projects must use one of:

- **Compatible release**: `~=1.2.3` (allows `>=1.2.3, <1.3.0`), or `~=1.2` (allows `>=1.2, <2.0`). Closest analog to Poetry's `^`
- **Bounded range**: `>=1.2.3,<2.0.0` (explicit, recommended when you want to pin upper bound)
- **Exact**: `==1.2.3`

```toml
# pyproject.toml (correct for uv/pip)
[project]
dependencies = [
  "requests~=2.31",        # >=2.31, <3.0
  "django>=5.2,<6.0",      # explicit upper bound
  "pydantic==2.9.2",       # exact pin
]
```

**Sourced 2026-05-18** from CodeRabbit finding on oneonme-claude-plugins R4, with citations to PEP 440 §6 and uv project documentation.

**How to apply:**
- Writing version constraints in any `pyproject.toml`, `requirements.txt`, or PEP-621 metadata for a uv- or pip-managed project: never use `^`
- Proposing version-pin language in CodeRabbit `.coderabbit.yaml` rules or custom_checks: use `~=` or bounded ranges, not `^`
- Poetry-managed projects keep `^`. The distinction is per-tool, not per-language
- When porting from a Poetry `pyproject.toml`, translate `^X.Y.Z` to `>=X.Y.Z,<(X+1).0.0`

Related: [[dependabot-uv-ecosystem]].
