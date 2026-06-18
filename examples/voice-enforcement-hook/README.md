# Voice-enforcement hook (Claude Code)

Reference consumer-side enforcement example for the v0.4 default-voice-exposure
contract (SPEC.md §6.1, §6.4). Optional. The spec does not require it.

## What it's for

The v0.4 load contract is **compact-always, full-lazy**:

- `voice.compact.md` always-loads (~2 KB) — the floor, so no session starts at zero voice.
- the full `voice.md` is the *deep* load — fired for real prose work.

This hook is the backstop for that second load. Instead of relying on the agent to
notice a task is prose-shaped and fire a voice skill, a `UserPromptSubmit` hook scans
the prompt for prose-generation intent (`draft`, `bio`, `rewrite`, `email`, `post`,
`changelog`, ...) and injects the full `voice.md` into that turn's context.

Floor (compact) + ceiling (this hook) means: every session has *some* voice, and any
turn that's actually about writing gets the *full* voice — without the agent having to
remember to ask for it.

## The §6.3 boundary (why this is allowed)

SPEC.md §6.3 forbids consumers from adding a **model-callable surface** that returns
`~/.me/` content as a tool result — that's the prompt-injection exfiltration vector.

This hook does not do that. It writes `voice.md` to stdout, and Claude Code adds that
stdout to the turn's instruction context. That's **harness-side context assembly**, the
same tier as session-start loading. The model never calls a `get_user_voice()` tool;
the harness pulls the file. The distinction the spec draws is *who pulls the content* —
the harness (allowed) vs. the model deciding to call a fetch tool (forbidden). A hook
that instead exposed an MCP resource or a tool returning voice.md would cross the line.

## Install

User-global. Drop the script somewhere stable (e.g. `~/.me/hooks/`) and register it:

```bash
mkdir -p ~/.me/hooks
cp voice-enforcement.sh ~/.me/hooks/
chmod +x ~/.me/hooks/voice-enforcement.sh
```

`~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "~/.me/hooks/voice-enforcement.sh" } ] }
    ]
  }
}
```

Per-project installs work the same way via `.claude/settings.json`.

## Behavior

| Prompt | Result |
|--------|--------|
| contains a prose trigger (`draft a bio`, `rewrite this email`) | full `voice.md` injected into the turn |
| no trigger (`fix the auth bug`) | silent no-op, exit 0, zero output |
| `voice.md` missing | silent no-op (the compact floor still applies) |

Tuning: edit the `TRIGGERS` list in the script. Over-matching just loads `voice.md` on a
turn that didn't strictly need it (cheap); under-matching reverts to the compact-only
floor (still safe). Override the voice path with `DOTME_VOICE_FILE` for testing.

## Portability

`UserPromptSubmit`-into-context is a Claude Code mechanism. Other consumers implement the
same *pattern* differently (Codex/Gemini have their own pre-turn hooks; some have none).
The portable layer is the always-loaded `voice.compact.md` floor — every consumer can
load a 2 KB file at startup. This hook is the Claude-Code-specific ceiling on top.
