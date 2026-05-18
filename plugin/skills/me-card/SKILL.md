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
  ┃   ╭───╮
  ┃   │ · │   d o t  ·  m e
  ┃   ╰───╯   portable user-context · v<plugin version>
  ┃
  ┃   <NAME-SPACED-CAPS>                                       <pronouns>
  ┃   <handle>
  ┃   ◌ <city> · <timezone>
  ┃
```

The **sigil** is a 3-line rounded box containing a single centered middle-dot
(`·`) — visually echoes the `.me` filename, reads as a brand mark, anchors
the top of the card. Right of the sigil sits the wordmark `d o t · m e`
spelled in spaced caps to match the name treatment below. Tagline +
plugin version sit on the sigil's third row, aligned with the wordmark.

The sigil block must be exactly 5 chars wide (`╭───╮ / │ · │ / ╰───╯`) and
the wordmark/tagline indent to align with the right edge of the sigil + 3
spaces of gutter.

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

## Color (default ON, warm palette)

Color is **on by default**. Disable with `NO_COLOR` env var, when stdout is
not a TTY, or when the user passes `--no-color`. Palette is warm/muted —
matches the dot-me aesthetic (calm, minimal, never corporate blue).

256-color ANSI codes (use `\033[38;5;<n>m` … `\033[0m`):

| Element                          | Code | Color           |
|----------------------------------|-----:|-----------------|
| Rail `┃`, section dividers       | 180  | warm tan        |
| Section labels (between `╴ ╶`)   | 215  | warm ochre      |
| Sigil box `╭─╮ │ ╰─╯`            | 138  | dusty rose      |
| Sigil interior dot `·`           | 139  | muted purple    |
| Wordmark `d o t · m e` + `.me`   | 215  | warm ochre      |
| Tagline, version                 | 245  | warm gray       |
| Header NAME (spaced caps)        | 223  | cream           |
| Section glyphs `● ○ ✦ ◉ ◈ ▣ ◐ ◌`| 180  | warm tan        |
| Memory bars `▇`                  | 215  | warm ochre      |
| Footer chip brackets `┤ ├`       | 180  | warm tan        |
| Footer chip text                 | 245  | warm gray       |
| Repo URL line                    | 244  | dimmer gray     |
| Everything else (content)        | default (terminal foreground) |

The muted purple sigil dot is the one bright accent — single-pixel pop of
James's favorite color (per `~/.me/memory/user_favorite_color.md` when
present; for other users, just leave it as the same warm tan as the rest of
the sigil). Don't read the memory file at runtime; treat 139 as the default
sigil-dot color.

Plain (no-color) form must remain fully legible and structured on its own —
color is decoration, never load-bearing.

## Example shape (with sample data)

```
  ┃
  ┃   ╭───╮
  ┃   │ · │   d o t  ·  m e
  ┃   ╰───╯   portable user-context · v0.1.1
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
