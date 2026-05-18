---
name: me-card
description: >
  Render the user's saved `~/.me/` context as a single ASCII-art infographic
  card. Use when the user asks to "show my info", "print my card", "render my
  profile", "me card", "ascii infographic of my dot-me", or invokes the
  `/me-card` shortcut. Read-only — never writes to `~/.me/`.
---

# me-card

Produce one stdout-friendly ASCII card that summarizes everything saved in
`~/.me/`. The output is the deliverable. No prose before or after.

The card is an **open-frame zine column** — single vertical rail down the
left, no top/right/bottom walls. Section breaks cut across the rail. The
brand mark `·me` sits at the top, a one-line signature at the bottom. Each
section uses its own glyph so the card scans by silhouette, not just text.

## What to read

Best-effort. Skip any file that doesn't exist or fails to parse.

- `~/.me/identity.yaml` — name, preferred_name, pronouns, handle, location,
  knows_about, work, past_work, pets, inner_circle, family
- `~/.me/preferences.yaml` — tools, aesthetics (formality, color_temperature,
  current_theme, design_principles), media
- `~/.me/working-style.yaml` — behavioral rule groups (not rendered, but
  counted for the footer total)
- `~/.me/voice.md` — first non-empty heading or one-line tagline if present;
  optional, only used for the footer
- `~/.me/memory/` — count files by prefix: `feedback_*.md`, `reference_*.md`,
  `project_*.md`, `user_*.md`. Each `.md` minus `MEMORY.md` and `.gitkeep`
- `~/.me/plugin/.claude-plugin/plugin.json` — `version` field for the
  spec/version stamp in the signature (fall back to identity.yaml
  `spec_version` if the plugin file is missing)

Use a quick `ls | wc -l` style scan for the memory tallies. Don't read the
memory file contents.

## Layout

Total column width: **68 chars** (rail + 2-space gutter + ≤64 chars content).

Lines start with `  ┃   ` (two leading spaces, rail, three-space gutter) and
then content. Blank lines between sections are `  ┃` (rail only). Never close
the right side — content trails off into whitespace, that's the design.

### Section glyph alphabet

Each section uses one glyph as its row marker (the column-2 character after
the gutter). Pick by section:

| Section       | Glyph | Use for                                |
|---------------|-------|----------------------------------------|
| location      | `◌`   | one row, in the header band             |
| now           | `●`   | each `work[]` row (filled dot = present)|
| then          | `○`   | each `past_work[]` row (open dot = past)|
| knows         | `✦`   | each `knows_about[]` row                |
| pack          | `◉`   | each `pets[]` row                       |
| inner circle  | `◈`   | each `inner_circle[]` row               |
| stack         | `▣`   | each tools row                          |
| aesthetic     | `◐`   | each principles/theme row               |
| memory        | (none — bar chart, see below)              |

The `now`/`then` filled-vs-open dot is intentional: a tiny temporal device
that reinforces the dot motif while encoding past/present at a glance.

### Order

Skip any section whose data is empty.

1. **Brand strip + header** — see template below.
2. **now** — `work[]` as `● <role-padded>  <org-or-project>`.
3. **then** — `past_work[]` as `○ <role-padded>  <org-padded>  <summary-or-mission>`.
4. **knows** — `knows_about[]`.
5. **pack** — `pets[]` as `◉ <name-padded>  <breed>` (skip species — it's
   almost always "dog" and adds no signal).
6. **inner circle** — `inner_circle[]` as `◈ <name-padded>  <role>`.
   Skip handles.
7. **stack** — selected `preferences.tools` keys, two cols (label 9, value):
   editor, shell (combine `shell + shell_plugin_manager + prompt`),
   terminal (combine `terminal_mac + multiplexer`), dotfiles, runtime.
8. **aesthetic** — `◐ <principles joined with " · ">` then
   `◐ theme: <current_theme split on first comma>`.
9. **memory** — bar chart, no row glyph.

### Section divider

Each section header is a single line — rail + thin tee + label, then dashes
to column 68:

```
  ┠──╴ <label> ─────────────────────────...
```

Use `┠` (thick-rail thin-tee) and `─` (thin dash) and `╴` (thin terminator
before the label) — this is what makes it look layered. The label is
lowercase.

### Brand sigil + header

```
  ┃
  ┃    o     ╭───╮
  ┃   /|\    │ · │   d o t  ·  m e
  ┃   / \    ╰───╯   portable user-context · v<plugin version>
  ┃
  ┃   <NAME-SPACED-CAPS>                                       <pronouns>
  ┃   <handle>
  ┃   ◌ <city> · <timezone>
  ┃
```

The header has two visual elements sitting side by side:

- A 3-line **stick figure** (`o` head, `/|\` body, `/ \` legs) on the left
  — the user's avatar/mascot, friendly and minimal. Occupies 3 chars wide.
- A 3-line **sigil** (rounded box containing a single centered middle-dot
  `·`) — visually echoes the `.me` filename, reads as a brand mark.

Right of the sigil sits the wordmark `d o t · m e` spelled in spaced caps
to match the name treatment below. Tagline + plugin version sit on the
sigil's third row, aligned with the wordmark.

Layout (column positions inside the rail's content area, where col 1 = first
char after the rail's 3-space gutter):

- Figure: col 2-4 (head `o` centered at col 2; body/legs spanning col 1-3,
  shifted right one for the head; concretely: ` o ` / `/|\` / `/ \`)
- Sigil: col 7-11 (5 chars: `╭───╮` / `│ · │` / `╰───╯`)
- Wordmark/tagline: col 15+ (sigil end + 3-space gutter)

The sigil block must be exactly 5 chars wide. The figure occupies a 3-char
column; if the name renders extremely long, the figure stays put and the
right-aligned tokens (pronouns, etc.) wrap or truncate first.

`NAME-SPACED-CAPS` = `preferred_name` (or `name`) uppercased with one space
between each letter — gives the name visual weight without needing a figlet
font. Right-align pronouns to column 68.

If the name renders wider than ~30 columns (long name), drop the
between-letter spacing and just use plain caps so it still fits.

### Memory bar chart

```
  ┠──╴ memory ───────────────────────────────────────...
  ┃
  ┃   feedback   ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  34
  ┃   reference  ▇▇▇▇▇▇                                     5
  ┃   project    ▇▇                                         2
  ┃   user       ▇                                          1
  ┃
```

- Bar char: `▇` (U+2587). Use `▇`, not `█` — slightly shorter, leaves
  airspace above the row and looks less heavy.
- Width budget: 40 cols max. `bar_len = max(1, round(count / max * 40))`
  when count > 0; empty row dropped.
- Right-align the count number to a fixed column so the digits line up.

### Footer brand strip

```
  ┃
  ┃   ──┤ <total-memories> entries ├──┤ .me v<spec> ├──┤ <today> ├──
  ┃   github.com/thebestmensch/dot-me
  ┃
```

Three labeled chips separated by `──┤ … ├──` (using `┤` and `├` to bracket
each chip). Repo URL on its own line below — quiet typographic signature,
no rail glyph in front, just indented to match content gutter.

`<total-memories>` = sum of all four memory category counts.
`<spec>` = `identity.spec_version` (e.g. `0.3`), or plugin version if
identity lacks it.
`<today>` = current date in `YYYY-MM-DD` via `date +%Y-%m-%d`
(America/Chicago timezone).
Repo URL: pull from `~/.me/plugin/.claude-plugin/plugin.json:repository`
if present, else fall back to `github.com/thebestmensch/dot-me`. Strip
the `https://` prefix.

## Field quirks

- YAML flow lists like `org: [redacted]` parse as `["redacted"]`. Render
  scalar-or-single-element-list fields as a plain string (`redacted`).
- For AESTHETIC, if a `design_principles` entry is longer than ~25 chars,
  drop it from the joined line so the row doesn't truncate.
- Strip parenthetical detail from `tools.*` values before rendering
  (e.g. `zinit (turbo-mode lazy loading)` → `zinit`).
- For `past_work[]`, if `summary` and `mission` are both absent, render the
  row without the trailing field.

## Width discipline

Lines have no right border, so the only hard rule is: don't let any single
content row exceed column 68. Truncate the longest field with `…` if needed.
The brand strip's right-aligned tokens (pronouns, version) must land with
their last character at or before column 68.

## Characters

- Rail + section breaks: `┃ ┠ ─ ╴ ┤ ├`
- Sigil box: `╭ ─ ╮ │ ╰ ╯`
- Section glyphs: `● ○ ✦ ◉ ◈ ▣ ◐ ◌`
- Bar fill: `▇` (U+2587)
- Brand wordmark: `d o t · m e` in the header, `.me` in the footer
- No em dashes anywhere. Use `·` for inline separators, `+` for compound
  stack entries (`zsh + zinit`), parentheses for parentheticals.
- No emoji.

## Color (default ON, warm palette, dark/light aware)

Color is **on by default**. Disable with `NO_COLOR` env var, when stdout is
not a TTY, or when the user passes `--no-color`. Palette is warm/muted —
matches the dot-me aesthetic (calm, minimal, never corporate blue).

### Dark/light mode detection

Resolve theme in this priority order, first hit wins:

1. **Explicit flag** — `--light` or `--dark` on the command line.
2. **Env override** — `ME_CARD_THEME=light` or `ME_CARD_THEME=dark`.
3. **macOS Appearance** — `defaults read -g AppleInterfaceStyle 2>/dev/null`.
   Returns `Dark` if the OS is in dark mode; exits non-zero / prints
   nothing in light mode. Run with a 200ms timeout — never let detection
   stall the render.
4. **`COLORFGBG` env var** — parse the second `;`-delimited field. Values
   `0,1,2,3,4,5,6,8` mean dark bg; anything else (typically `15` or `7`)
   means light bg.
5. **OSC 11 query** — write `\033]11;?\033\\` to the controlling TTY,
   read the reply with a 100ms timeout, parse `rgb:RRRR/GGGG/BBBB`. Compute
   luminance `(0.299·R + 0.587·G + 0.114·B) / 65535`. < 0.5 → dark, ≥ 0.5
   → light. Skip if inside tmux without `allow-passthrough on` (the query
   will hang or get echoed as garbage); detect tmux via `$TMUX` env var
   and bypass this step when set.
6. **Default** — `dark` (safest assumption; most terminals ship dark).

### 256-color palettes

Use `\033[38;5;<n>m` … `\033[0m`. Two palettes, keyed by detected theme:

| Element                          | Dark | Light | Color name              |
|----------------------------------|-----:|------:|-------------------------|
| Rail `┃`, section dividers       | 180  | 130   | warm tan / brown        |
| Section labels (between `╴ ╶`)   | 215  | 166   | warm ochre / rust       |
| Sigil box `╭─╮ │ ╰─╯`            | 138  |  95   | dusty rose / mauve      |
| Sigil interior dot `·`           | 139  |  97   | muted purple            |
| Wordmark `d o t · m e` + `.me`   | 215  | 166   | warm ochre / rust       |
| Tagline, version                 | 245  | 240   | warm gray (mid / dark)  |
| Header NAME (spaced caps)        | 223  |  94   | cream / dark brown      |
| Stick figure head `o`            | 215  | 166   | warm ochre / rust       |
| Stick figure body/legs `/|\ / \` | 180  | 130   | warm tan / brown        |
| Section glyphs `● ○ ✦ ◉ ◈ ▣ ◐ ◌`| 180  | 130   | warm tan / brown        |
| Memory bars `▇`                  | 215  | 166   | warm ochre / rust       |
| Footer chip brackets `┤ ├`       | 180  | 130   | warm tan / brown        |
| Footer chip text                 | 245  | 240   | warm gray               |
| Repo URL line                    | 244  | 242   | dim gray                |
| Everything else (content)        | default (terminal foreground)             |

The muted purple sigil dot is the one bright accent — single-pixel pop of
James's favorite color (per `~/.me/memory/user_favorite_color.md` when
present; for other users, just leave it as the same warm tan as the rest of
the sigil). Don't read the memory file at runtime; treat 139/97 as the
default sigil-dot color.

Plain (no-color) form must remain fully legible and structured on its own —
color is decoration, never load-bearing.

## Example shape (with sample data)

```
  ┃
  ┃    o     ╭───╮
  ┃   /|\    │ · │   d o t  ·  m e
  ┃   / \    ╰───╯   portable user-context · v0.1.1
  ┃
  ┃   J A M E S                                                   he/him
  ┃   @thebestmensch
  ┃   ◌ Austin · America/Chicago
  ┃
  ┠──╴ now ───────────────────────────────────────────────────────
  ┃
  ┃   ● Founder       redacted
  ┃   ● Maintainer    home-lab
  ┃
  ┠──╴ then ──────────────────────────────────────────────────────
  ┃
  ┃   ○ Cofounder                Magnifai       Public-agency data
  ┃   ○ Product + frontend lead  New Knowledge  Fighting disinfo
  ┃   ○ Engineer                 Google
  ┃
  ┠──╴ knows ─────────────────────────────────────────────────────
  ┃
  ┃   ✦ home automation and home labs
  ┃   ✦ mobile development
  ┃   ✦ AI tooling and agent systems
  ┃   ✦ data infrastructure
  ┃
  ┠──╴ pack ──────────────────────────────────────────────────────
  ┃
  ┃   ◉ Bean     Mini Australian Shepherd / Blue Heeler mix
  ┃   ◉ Gia      Husky
  ┃   ◉ Ruthie   Alaskan Klee Kai
  ┃
  ┠──╴ inner circle ──────────────────────────────────────────────
  ┃
  ┃   ◈ Rachel   cofounder + CEO, OneOnMe
  ┃   ◈ Sarah    partner
  ┃
  ┠──╴ stack ─────────────────────────────────────────────────────
  ┃
  ┃   ▣ editor    Claude Code
  ┃   ▣ shell     zsh + zinit + starship
  ┃   ▣ terminal  Ghostty + tmux
  ┃   ▣ dotfiles  chezmoi
  ┃   ▣ runtime   mise
  ┃
  ┠──╴ aesthetic ─────────────────────────────────────────────────
  ┃
  ┃   ◐ calm · minimal · cohesive
  ┃   ◐ theme: SpenschSuite Light
  ┃
  ┠──╴ memory ────────────────────────────────────────────────────
  ┃
  ┃   feedback   ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  34
  ┃   reference  ▇▇▇▇▇▇                                     5
  ┃   project    ▇▇                                         2
  ┃   user       ▇                                          1
  ┃
  ┃   ──┤ 42 entries ├──┤ .me v0.3 ├──┤ 2026-05-18 ├──
  ┃   github.com/thebestmensch/dot-me
  ┃
```

The example is illustrative — render from the actual file contents at
invocation time, do not echo this static block.

## Rules

- Read-only. Never write, edit, or move anything under `~/.me/`.
- One card per invocation. No follow-up commentary unless the user asks.
- If `~/.me/` is empty / unbootstrapped, print a one-line card pointing
  at `/me init` instead of an empty frame.
- If the user passes an argument like `me-card --no-color`, honor it.
