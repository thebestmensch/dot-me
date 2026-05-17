# Security Policy

## Threat model

`dot-me` defines a file format consumed by AI tools as authoritative user-context. The two attack classes that shape the v0.1 spec:

1. **Local file tamper**: an attacker with filesystem access modifies `identity.yaml` / `voice.md` / `preferences.yaml` to inject persistent instructions into every future AI session.
2. **Exfiltration via prompt injection**: a malicious project's `CLAUDE.md`, `AGENTS.md`, or similar instructs the agent to read and exfiltrate `~/.me/voice.md` (or another file) to a third party.

The spec's primary mitigation for class (2) is the **read-at-startup, not retrievable** rule: consumers SHOULD load `~/.me/` files once at session start and MUST NOT expose them as tools the agent can re-read mid-session. Class (1) is mitigated by optional integrity tooling (`.integrity` hash baselines + signed git commits + a SessionStart drift check); these are not part of the format and consumers MUST work correctly whether or not they exist.

Full threat-model section: see [`personal-context-design.md` §Appendix A](https://github.com/thebestmensch/home-lab/blob/main/docs/superpowers/specs/2026-05-05-personal-context-design.md#appendix-a--threat-model-summary).

## Reporting a vulnerability

If you find a vulnerability in the **spec itself** (a loading pattern, schema convention, or hardening recommendation that creates exploitable behavior across consumer tools), email **james@jamesmensch.com**.

Please include:
- The spec section or convention involved
- The attack class (which threat above, or a new one)
- A concrete consumer-tool scenario that exhibits the issue
- Suggested mitigation if you have one

I'll acknowledge within 7 days. Coordinated disclosure preferred for issues that affect multiple consumer tools.

## What's out of scope

- Vulnerabilities in **specific consumer tools** that load `dot-me` files (Claude Code, future Claude Cowork plugin, third-party agents). Report those to the tool's vendor.
- Vulnerabilities in **a user's personal `~/.me/` content** (e.g. weak GPG key, world-readable filesystem permissions). The spec recommends practices; enforcement is the user's responsibility.
- Issues with the example content in this repo (the maintainer's `identity.yaml` etc.). These are illustrative, not normative.

## Disclosure history

None yet. This file will be updated as findings land.
