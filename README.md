# dot-me

Portable user-context consumed by AI tools. Single source of truth for "who is this user, how do they sound, what do they like" — replaces fragmented `user_*.md` files scattered across per-project Claude Code memory dirs.

This repo is private. Treat its contents as personal data.

## Layout

| File | Purpose | Auto-loaded? |
|---|---|---|
| `identity.yaml` | Invariant facts: name, location, dogs, family, work | Yes — `@~/.me/identity.yaml` in `~/.claude/CLAUDE.md` |
| `voice.md` | Voice profile (hybrid: dimensions + lexicon + anti-patterns + sample passages) | Lazy — loaded by `/jm-voice` |
| `preferences.yaml` | likes / favorites / avoid triads (media, food, tools, aesthetics) | Lazy — loaded on demand |
| `memory/` | Auto-memory writes from every Claude Code project (via `autoMemoryDirectory`) | Selective by project |
| `.integrity` | SHA-256 hashes of `@include`d files; baseline for tamper detection | — |
| `.updates.log` | Append-only provenance: timestamp, source, file, summary | — |

## Integrity model

`~/.me/` files are treated as authoritative by Claude. Cisco's published persistent-memory compromise of Claude Code (2026) and Snyk's ToxicSkills study confirm `~/.claude/`-style files are an active attack surface. Three mitigations:

1. **SessionStart integrity hook** (`~/.claude/hooks/me-integrity.sh`) — compares actual file hashes to baseline in `.integrity`; warns if anything was modified outside the protocol.
2. **Signed git commits** — `git log --show-signature` makes tampering detectable post-hoc.
3. **`/me-add` pre-write lint** — rejects writes containing prompt-injection markers (`ignore`, `disregard`, `system prompt`, `override`, `forget previous`).

`.integrity` is regenerated only on legitimate writes (`/me-add`) or post-`git pull`. Drift detected by the SessionStart hook = something else wrote to the dir.

## Update flow

```
User-invariant fact discovered in session
  ├─→ /jm-retro (session end)        — §2 routing dispatches to /me-add
  ├─→ /me-add "<fact>" (mid-session)  — direct dispatch
  └─→ Auto-memory                     — autoMemoryDirectory routes writes here
```

`/me-add` write protocol (9 steps): read+hash → classify → prune → diff-preview → user-confirm → re-hash check → write → log → signed commit + push → `.integrity` regen.

## Setup on a fresh machine

```bash
git clone git@github.com:thebestmensch/dot-me.git ~/.me
git -C ~/.me config commit.gpgsign true
git -C ~/.me config user.signingkey <your-gpg-key-id>
# chezmoi-managed ~/.claude/CLAUDE.md and settings.json wire the rest
chezmoi apply
```

## Spec

Design rationale, adversarial-review history, and v0/v1 delineation: home-lab `docs/superpowers/specs/2026-05-05-personal-context-design.md`.
