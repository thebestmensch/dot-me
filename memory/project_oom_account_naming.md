---
name: oom-account-naming
description: "Anthropic account labels in OneOnMe menu-discovery tooling — \"personal\" = james@jamesmensch.com (jm/James), \"oom\" = james@oneonme.com (work). Legacy tower files name the work account `fallback-jm` which is confusingly inverted."
metadata: 
  node_type: memory
  type: project
  originSessionId: 134de499-9946-4d8d-8345-6cb78fbd2ce9
---

In OneOnMe menu-discovery agent tooling, two Anthropic Max subscriptions are in rotation:

- **`personal`** → `james@jamesmensch.com` — James's personal email. James also calls this account "jm" because **JM = James's personal identity**.
- **`oom`** → `james@oneonme.com` — James's OneOnMe work email.

**Why:** Legacy tower credential files use the inverted convention — `.credentials-personal.json` for the personal account (correct) and `.credentials-fallback-jm.json` for the **work** account (mis-named "jm" — historically tagged that way because the JM handle lives at the oneonme.com domain in some contexts). The `/oneonme-engineering:menu-agent-auth` skill's account map echoes the legacy naming (`jm` = `james@oneonme.com`), which contradicts how James thinks about it.

**How to apply:** New tooling (the `just menu-agent-auth-*` recipes added 2026-05-17) uses `personal` / `oom` — clearer mapping. When James says "JM sub" or "jm account" he means his personal account (`james@jamesmensch.com`). When he says "OOM" or "work" he means `james@oneonme.com`. Do NOT inherit the legacy `fallback-jm` filename naming for any new credential slots — use `.credentials-oom.json` for the work account in fresh setups. Tower stays on legacy names until rebuilt (run.sh's account discovery reads filename prefixes; renaming requires syncing run.sh's classifier).
