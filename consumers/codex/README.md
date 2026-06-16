# dot-me: Codex CLI consumer

Native integration for [Codex CLI](https://github.com/openai/codex). Inlines your `~/.me/` content into `~/.codex/AGENTS.md` so every Codex session starts with the right user context (no copy-paste, no drift).

## Install

```bash
# clone (or fork) dot-me into your home directory first
git clone https://github.com/thebestmensch/dot-me.git ~/.me

# install the Codex consumer
bash ~/.me/consumers/codex/install.sh
```

Or run straight from the repo without cloning:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/thebestmensch/dot-me/main/consumers/codex/install.sh)
```

(curl-bash assumes `~/.me/` already exists. If not, clone first.)

The installer:

1. Reads `~/.me/identity.yaml` (and `preferences.yaml` by default)
2. Writes the content between `<!-- dot-me:begin -->` / `<!-- dot-me:end -->` markers in `~/.codex/AGENTS.md`
3. Preserves anything outside the markers; your existing global Codex instructions are untouched
4. Backs up the previous file to `~/.codex/AGENTS.md.bak`

Re-running the installer replaces the block in place. Idempotent.

## Modes

```bash
bash ~/.me/consumers/codex/install.sh --minimal       # identity only (~1.5 KB)
bash ~/.me/consumers/codex/install.sh                 # identity + preferences (default, ~3 KB)
bash ~/.me/consumers/codex/install.sh --with-voice    # identity + preferences + voice (~17 KB)
```

**Why voice is opt-in:** Codex caps the combined instruction chain (global + repo + cwd `AGENTS.md` files) at ~32 KiB. `voice.md` is the heaviest file in dot-me; including it leaves less budget for project-level `AGENTS.md` content. The installer warns when the projected total exceeds 24 KiB.

If you want voice context only when generating user-facing text, you can keep it out of the global chain and paste it into project-level `AGENTS.md` for repos where you do writing/correspondence.

## Other flags

```bash
bash ~/.me/consumers/codex/install.sh --dry-run     # preview the block, write nothing
bash ~/.me/consumers/codex/install.sh --uninstall   # strip the dot-me block, restore AGENTS.md
```

`--uninstall` works even if `~/.me/` is missing or has a spec version this installer doesn't recognize; uninstall always has a clean exit path.

## How loading works

Codex reads `~/.codex/AGENTS.md` once per session at startup and folds it into the system-tier instruction chain. This matches dot-me [SPEC §6.2](../../SPEC.md) (system-tier) and [§6.3](../../SPEC.md) (read at session start). This consumer adds no new tool surface scoped to dot-me content; there is no `read_user_identity` skill or MCP resource that the model can call mid-session.

**The filesystem reality.** Codex needs the content on disk to load it, so an installed dot-me block lives at the well-known path `~/.codex/AGENTS.md`. A generic filesystem tool the model has access to (a `Bash` tool, a `Read` tool) could re-read that file mid-session if a malicious project's prompt asks it to. The same exposure exists for `~/.me/` itself. SPEC §6.3 explicitly does not require the filesystem to be unreachable; it bans *new dot-me-scoped* surfaces, which this consumer doesn't add. Generic filesystem-tool exfiltration is a property of the user's tool-permission setup, addressed by sandboxing, not by dot-me.

**Tradeoff with `--with-voice`.** Voice content concentrates writing patterns and sample passages at one well-known path, raising the value of a filesystem-tool exfil. Default mode (identity + preferences) keeps that surface narrower. If you only need voice for tasks that generate user-facing text, consider keeping voice paste-in at the project level for those repos rather than inlining globally.

## Why inline instead of `@`-import

Claude Code's `CLAUDE.md` supports `@<path>` imports; you can write `@~/.me/identity.yaml` and the file is loaded by reference. **Codex doesn't have this.** As of May 2026, Codex CLI's `AGENTS.md` reader treats `@<path>` lines as literal text. The only native path is to inline the content.

If Codex adds `@`-imports in a future release, this installer will switch to writing a single `@~/.me/identity.yaml` line in the block (smaller footprint, automatic content refresh on edit).

## Environment variables

```bash
DOT_ME_DIR=/path/to/your/me bash ~/.me/consumers/codex/install.sh   # custom dot-me location
CODEX_HOME=/path/to/codex   bash ~/.me/consumers/codex/install.sh   # custom Codex config dir
```

Defaults: `DOT_ME_DIR=~/.me`, `CODEX_HOME=~/.codex` (or `$CODEX_HOME` if set per [Codex docs](https://developers.openai.com/codex/guides/agents-md)).

## Schema version handling

The installer reads `spec_version` from `identity.yaml` (per [SPEC §5.5](../../SPEC.md)):

- **Missing** → warn, treat as legacy `"0.1"` (mixed `work[]` semantics per SPEC §5.A), proceed
- **Matches a known additive version** (`"0.1"`, `"0.2"`, or `"0.3"`) → proceed silently
- **Unknown / future** → refuse with an upgrade message; rerun after upgrading the installer

This lets the spec evolve breaking changes via `spec_version` bumps without silently corrupting older consumer integrations.

## Refreshing after edits to `~/.me/`

Codex AGENTS.md is loaded at session start, not retrievable mid-session. After editing `~/.me/identity.yaml`:

```bash
bash ~/.me/consumers/codex/install.sh   # regenerate the block
# then start a new Codex session
```

A future iteration may add a SessionStart-equivalent hook if Codex ships one.

## Uninstall

```bash
bash ~/.me/consumers/codex/install.sh --uninstall
```

Strips the marked block. Anything outside the markers is preserved. A backup lands at `~/.codex/AGENTS.md.bak`.

To fully reverse:

```bash
bash ~/.me/consumers/codex/install.sh --uninstall
rm -rf ~/.me   # only if you don't want the content
```
