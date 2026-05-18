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
| now           | `▸`   | each `work[]` row                       |
| then          | `·`   | each `past_work[]` row                  |
| knows         | `✦`   | each `knows_about[]` row                |
| pack          | `◉`   | each `pets[]` row                       |
| inner circle  | `◈`   | each `inner_circle[]` row               |
| stack         | `▣`   | each tools row                          |
| aesthetic     | `◐`   | each principles/theme row               |
| memory        | (none — bar chart, see below)              |

### Order

Skip any section whose data is empty.

1. **Brand strip + header** — see template below.
2. **now** — `work[]` as `▸ <role-padded>  <org-or-project>`.
3. **then** — `past_work[]` as `· <role-padded>  <org-padded>  <summary-or-mission>`.
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

### Brand strip + header

```
  ┃
  ┃   · m e                                          v<plugin version>
  ┃
  ┃   <NAME-SPACED-CAPS>                                       <pronouns>
  ┃   <handle>
  ┃   ◌ <city> · <timezone>
  ┃
```

`NAME-SPACED-CAPS` = `preferred_name` (or `name`) uppercased with one space
between each letter — gives the name visual weight without needing a figlet
font. Right-align pronouns to column 68. Right-align the version to column 68.

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

### Footer signature

```
  ┃
  ┃   ─── <total-memories> total · dot-me v<spec> · <today YYYY-MM-DD> ───
  ┃
```

`<total-memories>` = sum of all four memory category counts.
`<spec>` = `identity.spec_version` (e.g. `0.3`), or plugin version if
identity lacks it.
`<today>` = current date in America/Chicago.

Use `date +%Y-%m-%d` for the date stamp. Surround the line with `─── ... ───`
(three dashes each side, single spaces).

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

- Rail + section breaks: `┃ ┠ ─ ╴`
- Section glyphs: `▸ · ✦ ◉ ◈ ▣ ◐ ◌`
- Bar fill: `▇` (U+2587)
- Brand mark: `·me` (middle dot, lowercase m, lowercase e), with the
  spaced-name treatment turning it into `· m e` in the header
- No em dashes anywhere. Use `·` for inline separators, `+` for compound
  stack entries (`zsh + zinit`), parentheses for parentheticals.
- No emoji.

## Color (optional)

If `NO_COLOR` is unset and stdout is a TTY, you may dim the rail and
section labels with warm ANSI (e.g. `\033[38;5;180m` for the rail and
dividers, `\033[38;5;215m` for section labels, `\033[0m` reset). Content
stays in the default terminal color. Skip color when in doubt.

## Example shape (with sample data)

```
  ┃
  ┃   · m e                                                       v0.1.1
  ┃
  ┃   J A M E S                                                   he/him
  ┃   @thebestmensch
  ┃   ◌ Austin · America/Chicago
  ┃
  ┠──╴ now ───────────────────────────────────────────────────────
  ┃
  ┃   ▸ Founder       redacted
  ┃   ▸ Maintainer    home-lab
  ┃
  ┠──╴ then ──────────────────────────────────────────────────────
  ┃
  ┃   · Cofounder                Magnifai       Public-agency data
  ┃   · Product + frontend lead  New Knowledge  Fighting disinfo
  ┃   · Engineer                 Google
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
  ┃   ─── 42 total · dot-me v0.3 · 2026-05-18 ───
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
