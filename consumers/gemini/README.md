# dot-me: Gemini CLI consumer

Native integration for [Gemini CLI](https://github.com/google-gemini/gemini-cli). Inlines your `~/.me/` content into `~/.gemini/GEMINI.md` so every Gemini session starts with the right user context (no copy-paste, no drift).

## Install

```bash
# clone (or fork) dot-me into your home directory first
git clone git@github.com:thebestmensch/dot-me.git ~/.me

# install the Gemini consumer
bash ~/.me/consumers/gemini/install.sh
```

Or run from the repo without cloning:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/thebestmensch/dot-me/main/consumers/gemini/install.sh)
```

The installer:

1. Reads `~/.me/identity.yaml` (and `preferences.yaml` by default)
2. Writes the content between `<!-- dot-me:begin -->` / `<!-- dot-me:end -->` markers in `~/.gemini/GEMINI.md`
3. Preserves anything outside the markers; your existing global Gemini instructions are untouched
4. Backs up the previous file to `~/.gemini/GEMINI.md.bak`

Re-running the installer replaces the block in place. Idempotent.

After install, verify:

```bash
gemini   # start a new session
# inside Gemini:
/memory show
```

You should see the dot-me content rendered in the loaded context.

## Modes

```bash
bash ~/.me/consumers/gemini/install.sh --minimal       # identity only (~1 KB)
bash ~/.me/consumers/gemini/install.sh                 # identity + preferences (default, ~2 KB)
bash ~/.me/consumers/gemini/install.sh --with-voice    # identity + preferences + voice (~17 KB)
```

`--with-voice` is opt-in because it concentrates writing patterns at one well-known path, raising the value of a filesystem-tool exfil. Default mode (identity + preferences) keeps that surface narrower.

## Other flags

```bash
bash ~/.me/consumers/gemini/install.sh --dry-run                  # preview the block, write nothing
bash ~/.me/consumers/gemini/install.sh --uninstall                # strip the dot-me block
bash ~/.me/consumers/gemini/install.sh --context-file MYFILE.md   # use a non-default context filename
```

`--context-file` exists because Gemini CLI extensions can override the default `GEMINI.md` filename via the `contextFileName` config key. If you've customized that, point the installer at the right file or the install will silently write to a file Gemini won't load.

## Why inline (not `@`-import)

Gemini's `GEMINI.md` *does* support `@<path>` imports, and using them would be the prettier path (edit `~/.me/`, no re-install needed). But two behaviors in [Memory Import Processor](https://www.geminicli.com/docs/cli/gemini-md) make it unsafe in practice:

1. **`validateImportPath` rejects absolute paths outside the GEMINI.md's project root.** `~/.me/` is a sibling of `~/.gemini/`, so `@~/.me/identity.yaml` is dropped silently as path traversal. A symlink under `~/.gemini/` works around this.
2. **The processor recursively scans imported content for `@`-tokens.** dot-me content uses `@`-strings in normal ways: `identity.yaml` carries `handle: "@thebestmensch"`, `voice.md` mentions `@here` Slack pings. Recursive scanning would treat those as nested imports and either fail loudly (best case) or pull unintended files (worst case).

Inline content sidesteps both. GEMINI.md's body is plain context; the processor only resolves `@`-imports at the top level. Fenced code blocks in the block keep the YAML/markdown content as literal text.

The price: a re-install after every edit to `~/.me/`, same UX as the Codex consumer.

Codex adversarial review caught both issues on 2026-05-14 before the first version shipped with naive `@`-imports.

## How loading works

Gemini CLI uses a three-tier hierarchical chain: global (`~/.gemini/GEMINI.md`), workspace (`GEMINI.md` files in configured workspace directories), and just-in-time (scans accessed file directories). The CLI concatenates the contents of all found files before sending them to the model.

The dot-me block lives at the **global** level so it applies to every Gemini session regardless of cwd. This matches dot-me [SPEC §6.2](../../SPEC.md) (system-tier) and [§6.3](../../SPEC.md) (read at session start). This consumer adds no new dot-me-scoped tool surface; there's no `read_user_identity` skill or MCP resource the model can call mid-session.

**Filesystem reality.** Like the Codex consumer, the inlined content lives on disk somewhere. A generic filesystem tool the model has access to could re-read `~/.gemini/GEMINI.md` (or `~/.me/` directly) mid-session if a malicious project's `GEMINI.md` asks it to. SPEC §6.3 explicitly does not require the filesystem to be unreachable; it bans *new dot-me-scoped* surfaces, which this consumer doesn't add. Generic filesystem-tool exfiltration is a property of the user's tool-permission setup, addressed by sandboxing.

## Environment variables

```bash
DOT_ME_DIR=/path/to/your/me bash ~/.me/consumers/gemini/install.sh        # custom dot-me location
GEMINI_CLI_HOME=/path/to/gemini bash ~/.me/consumers/gemini/install.sh    # custom Gemini config dir
```

Defaults: `DOT_ME_DIR=~/.me`, `GEMINI_CLI_HOME` honors Gemini CLI's own env var (falls back to `~/.gemini` when unset, same as Gemini itself).

## Schema version handling

The installer reads `spec_version` from `identity.yaml` (per [SPEC §5.5](../../SPEC.md)):

- **Missing** → warn, treat as legacy `"0.1"` (mixed `work[]` semantics per SPEC §5.A), proceed
- **Matches a known additive version** (`"0.1"`, `"0.2"`, or `"0.3"`) → proceed silently
- **Unknown / future** → refuse with an upgrade message

`--uninstall` always works regardless of `spec_version`.

## Refreshing after edits to `~/.me/`

`GEMINI.md` is loaded at session start, not retrievable mid-session. After editing `~/.me/identity.yaml`:

```bash
bash ~/.me/consumers/gemini/install.sh   # regenerate the inlined block
# then start a new Gemini session
```

## Legacy cleanup

If you ran an earlier dev build of this installer that created a symlink at `~/.gemini/dot-me/`, the current installer detects and removes it on both install and uninstall. No manual cleanup needed.

## Uninstall

```bash
bash ~/.me/consumers/gemini/install.sh --uninstall
```

Strips the markered block from `~/.gemini/GEMINI.md`, removes any legacy `~/.gemini/dot-me/` symlink. Anything outside the markers is preserved. A backup of the previous `GEMINI.md` lands at `~/.gemini/GEMINI.md.bak`.
