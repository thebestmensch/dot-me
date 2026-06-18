# dot-me plugin

The reference consumer plugin for [dot-me](https://github.com/thebestmensch/dot-me). Bundles the `/me` slash command, the `me-integrity.sh` SessionStart hook, and the auto-load wiring needed to read `~/.me/identity.yaml` into every session.

## What it ships

| Component | Path | Surface |
|---|---|---|
| `/me` umbrella command (scan / add / show / edit / check / init) | `commands/me.md` | Claude Code + Cowork |
| `me-integrity.sh` SessionStart hook | `hooks/scripts/me-integrity.sh` | **Claude Code only** (Cowork hook bug, see below) |
| Plugin manifest | `.claude-plugin/plugin.json` | Both |

## Install: Claude Code

```bash
/plugin marketplace add thebestmensch/dot-me
/plugin install dot-me@dot-me
```

(The marketplace + plugin live in the same repo. Once added, the marketplace is named `dot-me` and ships the `dot-me` plugin; hence the `dot-me@dot-me` syntax.)

After install:

1. Run `/me init` to seed `~/.me/` from `examples/` (skips if `~/.me/` already exists)
2. Verify with `/me check`; `integrity baseline intact` means you're set up
3. Edit the seeded files: `/me edit identity` (or voice / preferences) to replace the Sam Patel templates with your own content
4. Use `/me add "<fact>"` to record facts mid-session, or bare `/me` to scan the current session for vCard-shape candidates

The `me-integrity.sh` hook fires on SessionStart and warns when `~/.me/` files drift from the `.integrity` baseline; your tamper-detection signal for filesystem-tampering attacks.

## Install: Claude Cowork

Skill / command surface works the same. **The SessionStart hook does NOT fire** because of an open Cowork plugin-hook bug ([`anthropics/claude-code#16288`](https://github.com/anthropics/claude-code/issues/16288), still open as of June 2026; the Cowork VM spawns `claude --setting-sources user` which excludes plugin-scoped hooks).

For Cowork's missing auto-load + missing integrity hook, paste the contents of `~/.me/identity.yaml` into **Settings → Cowork → Global Instructions** after running `/me init`. Re-paste when the file changes. The `/me show identity` command renders the current content for easy copying.

When the upstream bug is fixed, this plugin's hook will start firing automatically with no install changes needed.

## Auto-load contract

On Claude Code, `~/.me/identity.yaml` is loaded at session start by the `@~/.me/identity.yaml` import line that `/me init` writes into `~/.claude/CLAUDE.md` (only on first-run). The `me-integrity.sh` SessionStart hook is a separate concern: it verifies the `.integrity` baseline and warns on tamper drift — it does not itself load file content into context.

The plugin is **opt-in**: nothing reads `~/.me/` until you explicitly install it, run `/me init`, and edit the seeded content.

## Uninstall

```bash
/plugin uninstall dot-me
```

Removes the slash command and hook. Does NOT touch `~/.me/`; your personal content is preserved. To reverse the install entirely:

```bash
/plugin uninstall dot-me
rm -rf ~/.me                       # only if you don't want the content
# manually remove the `@~/.me/identity.yaml` line from ~/.claude/CLAUDE.md
```

## Spec

This plugin is one implementation of the format. The format itself is the contract; see [`SPEC.md`](../SPEC.md) in the parent dot-me repo.

## License

[MIT](../LICENSE). Same as the parent dot-me repo.
