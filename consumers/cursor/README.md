# dot-me: Cursor consumer

Native integration for [Cursor](https://cursor.com). Pipes your `~/.me/` content into Cursor's two rule surfaces; pick whichever fits your workflow.

## TL;DR

```bash
# clone dot-me into your home directory first
git clone git@github.com:thebestmensch/dot-me.git ~/.me

# global personal context (paste once into Cursor Settings)
bash ~/.me/consumers/cursor/install.sh

# OR: per-repo file that re-syncs on every install
bash ~/.me/consumers/cursor/install.sh --project /path/to/repo
```

Curl-bash one-liner (assumes `~/.me/` already cloned):

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/thebestmensch/dot-me/main/consumers/cursor/install.sh)
```

## Two modes, two tradeoffs

Cursor has two rule surfaces. Neither is a clean "files-on-disk syncs to global context" loop the way Codex CLI's `~/.codex/AGENTS.md` is, so this installer ships both; pick which limitation you'd rather live with.

### Default: User Rules (paste once)

The installer renders the dot-me block to stdout, pipes it through `pbcopy` on macOS when your terminal is interactive, and prints paste instructions:

```bash
bash ~/.me/consumers/cursor/install.sh
# (block is now on your clipboard)
# 1. Cursor → Settings → Rules → User Rules
# 2. Paste
# 3. Save
```

User Rules apply globally across every Cursor chat. The catch: Cursor stores User Rules only in Settings; there's no filesystem path it reads. **Editing `~/.me/identity.yaml` requires re-running the installer and re-pasting**, because Cursor has nothing to watch.

Use this mode when:

- The same context should apply everywhere you use Cursor
- You're OK re-pasting on the rare occasions you edit `~/.me/`

### `--project <dir>`: Project Rule (file-on-disk)

```bash
bash ~/.me/consumers/cursor/install.sh --project ~/code/my-repo
```

Writes `~/code/my-repo/.cursor/rules/dot-me.mdc` with `alwaysApply: true`. Cursor reads `.cursor/rules/*.mdc` from disk at session start, so re-running the installer refreshes the rule with no paste step.

When the target is a git worktree, the installer:

1. **Refuses to overwrite a tracked `dot-me.mdc`.** If the file is already part of the repo (e.g. shared team rules use the same filename), the install errors out. `--force-tracked` overrides if you know what you're doing.
2. **Auto-adds the file to `.git/info/exclude`.** Local-only ignore (does not touch the repo's `.gitignore`). Prevents `git add -A` from accidentally staging personal context into a shared repo.
3. **Warns visibly** that the file contains personal identity/preferences and should not be committed.

Use this mode when:

- A specific repo benefits from your personal context (e.g. a project where you do user-facing writing)
- You want dot-me edits to flow through without paste friction

Caveat: it's per-repo. You'd add it to each repo where you want the context. Many users will want **both**: User Rules for the everyday case, plus `--project` for one or two repos that do heavy writing.

## Modes

```bash
bash ~/.me/consumers/cursor/install.sh --minimal       # identity only (~1.5 KB)
bash ~/.me/consumers/cursor/install.sh                 # identity + preferences (default, ~3 KB)
bash ~/.me/consumers/cursor/install.sh --with-voice    # identity + preferences + voice (~17 KB)
```

`--with-voice` is heaviest; only worth it if you do significant writing through Cursor. For most cases, the standard default is enough.

## Other flags

```bash
bash ~/.me/consumers/cursor/install.sh --dry-run                       # preview, no clipboard / no write
bash ~/.me/consumers/cursor/install.sh --project <dir> --dry-run       # preview project file content
bash ~/.me/consumers/cursor/install.sh --project <dir> --uninstall     # remove the project file + any .bak
bash ~/.me/consumers/cursor/install.sh --project <dir> --force-tracked # allow overwrite when dot-me.mdc is git-tracked
bash ~/.me/consumers/cursor/install.sh --uninstall                     # prints Cursor Settings instructions for User Rules
```

User Rules can't be removed by a script; Cursor doesn't expose them as a file. The `--uninstall` (no `--project`) flag prints the Settings UI steps so you can clear it manually.

Project-mode uninstall removes both `dot-me.mdc` and any leftover `dot-me.mdc.bak`; leaving the `.bak` behind would defeat the privacy point of uninstalling.

## How loading works

Cursor reads User Rules and `.cursor/rules/*.mdc` once per session at startup. Neither surface is retrievable by the model mid-session; they're folded into the system-tier instructions. This matches dot-me [SPEC §6.2](../../SPEC.md) (system-tier) and [§6.3](../../SPEC.md) (read at session start). This consumer adds no new dot-me-scoped tool surface; there's no `read_user_identity` skill or MCP resource the model can call mid-session.

**Filesystem reality.** Like the Codex consumer, the inlined content lives on disk somewhere (`~/.me/identity.yaml`, plus a copy in `.cursor/rules/dot-me.mdc` if you use project mode). A generic filesystem tool (a `Read` tool, a shell) could re-read those files mid-session if a malicious project's prompt asks it to. The same exposure exists for `~/.me/` itself. SPEC §6.3 explicitly does not require the filesystem to be unreachable; it bans *new dot-me-scoped* surfaces, which this consumer doesn't add. Generic filesystem-tool exfiltration is a property of the user's tool-permission setup, addressed by sandboxing.

## Environment variables

```bash
DOT_ME_DIR=/path/to/your/me bash ~/.me/consumers/cursor/install.sh    # custom dot-me location
```

Default: `DOT_ME_DIR=~/.me`.

## Schema version handling

The installer reads `spec_version` from `identity.yaml` (per [SPEC §5.5](../../SPEC.md)):

- **Missing** → warn, assume `"0.3"`, proceed
- **Matches a known additive version** (`"0.1"`, `"0.2"`, or `"0.3"`) → proceed silently
- **Unknown / future** → refuse with an upgrade message

## Refreshing after edits to `~/.me/`

**User Rules mode:** re-run the installer, re-paste into Cursor Settings.

**Project mode:** re-run with the same `--project <dir>`. The `.mdc` file is replaced (previous version backed up to `dot-me.mdc.bak`). Cursor picks up the new content on the next session.

## Why no `@`-import?

Cursor supports `@filename` *inside* a rule body to pull file context into a specific chat (useful for "include this code file in my next message"). It's not the same as Codex's missing chain-level `@<path>` import. Cursor's User Rules surface has no filesystem-aware include directive at all. The only path to land `~/.me/` content in the global chain is to inline the text and re-paste on change. Project Rules have a filesystem path but no cross-file `@` chaining either, one `.mdc` per rule.

If Cursor ships a user-level filesystem rules directory (`~/.cursor/rules/`) or a chain-level `@`-import in a future release, this installer will switch to that path.
