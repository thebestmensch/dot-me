---
name: Consumer tool integration
about: You're building a tool that loads dot-me and the spec doesn't cover something you need
title: "[integration] "
labels: ["integration"]
assignees: []
---

## What you're building

What's the tool? AI agent, editor plugin, MCP server, CLI utility, dotfile manager, something else? Brief is fine.

## What you tried to load

Which file(s) — `identity.yaml`, `voice.md`, `preferences.yaml`, `memory/`, the integrity sidecars?

## Where you got stuck

What does the spec say (or not say)? What did you do as a workaround?

Examples that have come up:
- "The spec says read-at-startup but my tool is request-scoped — how should this map?"
- "I want to load only `voice.md`, not `identity.yaml` — is per-file loading supported?"
- "What's the recommended behavior when `~/.me/` doesn't exist?"
- "I need a field that doesn't exist in v0.1 — should I extend the spec or store it elsewhere?"

## What would help

- A spec section that addresses your case
- A reference-implementation pattern you could copy
- A "no, that's intentionally out of scope" answer (which is a valid outcome — see the v0.1 spec's out-of-scope list)

---

For ambiguities in already-covered sections, use *Spec clarification* instead.
For security issues, see [SECURITY.md](../../SECURITY.md) — please email, don't open a public issue.
