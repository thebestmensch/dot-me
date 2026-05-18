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

## What to read

Best-effort. Skip any file that doesn't exist or fails to parse.

- `~/.me/identity.yaml` — name, preferred_name, pronouns, handle, location,
  knows_about, work, past_work, pets, inner_circle, family
- `~/.me/preferences.yaml` — tools, aesthetics (formality, color_temperature,
  current_theme, design_principles), media
- `~/.me/working-style.yaml` — behavioral rule groups (top-level keys only,
  for the tally row)
- `~/.me/voice.md` — first non-empty heading or one-line tagline if present;
  optional, only used for the footer
- `~/.me/memory/` — count files by prefix: `feedback_*.md`, `reference_*.md`,
  `project_*.md`, `user_*.md`. Each `.md` minus `MEMORY.md` and `.gitkeep`

Use a quick `ls | wc -l` style scan for the memory tallies. Don't read the
memory file contents.

## Layout

Single contiguous block, 72 columns wide, Unicode box-drawing characters.
Frame with `╔═╗ ║ ╠═╣ ╚═╝`. Section dividers use `╠═══ LABEL ═══...═╣`.
Inside content uses two-space left padding from `║`.

Render sections in this order, **skipping any section whose data is empty**:

1. **Header band** — preferred name (or name) in ALL CAPS, pronouns right-
   aligned on same line. Handle on next line. Blank line. Location: city/region
   from blurb if present, otherwise just timezone. (`identity.yaml` doesn't
   have a city field; pull it from the blurb if regex-obvious, otherwise show
   only the timezone.)
2. **NOW** — `work[]` as `◆  <role>  <org-or-project>` aligned.
3. **THEN** — `past_work[]` as `·  <role>  <org>  <summary-or-mission>` with
   role/org column-aligned.
4. **KNOWS** — one `knows_about` item per line, no bullet.
5. **PACK** — `pets[]` as `<name>  <species>  <breed>` column-aligned. Only
   shown if `pets` is non-empty.
6. **INNER CIRCLE** — `inner_circle[]` as `<name>  <role>`. Skip handles.
7. **STACK** — selected `preferences.tools` keys: editor, shell (combine with
   shell_plugin_manager and prompt if present, e.g. `zsh + zinit + starship`),
   terminal_mac or terminal_windows, multiplexer, dotfiles, runtime_manager.
   Two columns: label (left, 10 chars) + value.
8. **AESTHETIC** — `aesthetics.design_principles` joined with `  ·  `, then a
   line `theme: <current_theme>` if present. Skip if both absent.
9. **MEMORY** — bar chart. Each non-zero category is one row:
   `<label-padded-9>  <bar>  <count>`
   where `<bar>` is `█` repeated proportionally so the longest bar fits in
   ~40 columns. Floor the scale by the largest count: bar_len =
   round(count / max_count * 40), minimum 1 if count > 0. Label set:
   `feedback`, `reference`, `project`, `user` (in that order). If all four
   are zero, skip the section entirely.

End with the closing `╚═══...═══╝`.

## Field quirks

- YAML flow lists like `org: [redacted]` parse as `["redacted"]`. Render
  scalar-or-single-element-list fields as a plain string (`redacted`).
- For AESTHETIC, if a `design_principles` entry is longer than ~25 chars,
  drop it from the joined line so the row doesn't truncate. (Long
  principles belong in notes, not the card.)
- Strip parenthetical detail from `tools.*` values before rendering
  (e.g. `zinit (turbo-mode lazy loading)` → `zinit`).

## Width discipline

Every line between `║ ... ║` is exactly 72 chars wide including the borders.
Pad the interior with trailing spaces. Truncate any single field with `…` if
it would overflow (rare — most identity fields are short). Re-measure after
emitting; if any line is off by one, fix it before printing.

## Characters

- Box drawing: `╔ ╗ ╚ ╝ ║ ═ ╠ ╣ ┌ ┐ └ ┘ │ ─ ├ ┤`
- Bullets / separators: `◆  ·  ·  ·`
- Bar fill: `█` (U+2588)
- No em dashes. Use `·` for inline separators, `+` for compound stack
  entries (`zsh + zinit`), parentheses for parentheticals.
- No emoji. Box-drawing and `█` only.

## Color (optional)

If `NO_COLOR` is unset and stdout is a TTY, you may wrap the frame and
section labels in dim warm ANSI (e.g. `\033[38;5;180m` for the frame,
`\033[38;5;215m` for section labels, `\033[0m` to reset). Skip color
otherwise. Default to no color when in doubt — the unstyled card should
be the primary form.

## Example shape (with sample data)

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   JAMES                                                    he/him    ║
║   @thebestmensch                                                     ║
║                                                                      ║
║   Austin, TX  ·  America/Chicago                                     ║
║                                                                      ║
╠═══ NOW ══════════════════════════════════════════════════════════════╣
║                                                                      ║
║   ◆  Founder       [redacted]                                        ║
║   ◆  Maintainer    home-lab                                          ║
║                                                                      ║
╠═══ THEN ═════════════════════════════════════════════════════════════╣
║                                                                      ║
║   ·  Cofounder           Magnifai       Public-agency data work      ║
║   ·  Product + frontend  New Knowledge  Fighting disinformation      ║
║   ·  Engineer            Google                                      ║
║                                                                      ║
╠═══ KNOWS ════════════════════════════════════════════════════════════╣
║                                                                      ║
║   home automation and home labs                                      ║
║   mobile development                                                 ║
║   AI tooling and agent systems                                       ║
║   data infrastructure                                                ║
║                                                                      ║
╠═══ PACK ═════════════════════════════════════════════════════════════╣
║                                                                      ║
║   Bean    dog   Mini Australian Shepherd / Blue Heeler mix           ║
║   Gia     dog   Husky                                                ║
║   Ruthie  dog   Alaskan Klee Kai                                     ║
║                                                                      ║
╠═══ INNER CIRCLE ═════════════════════════════════════════════════════╣
║                                                                      ║
║   Rachel  cofounder + CEO, OneOnMe                                   ║
║   Sarah   partner                                                    ║
║                                                                      ║
╠═══ STACK ════════════════════════════════════════════════════════════╣
║                                                                      ║
║   editor     Claude Code                                             ║
║   shell      zsh + zinit + starship                                  ║
║   terminal   Ghostty + tmux                                          ║
║   dotfiles   chezmoi                                                 ║
║   runtime    mise                                                    ║
║                                                                      ║
╠═══ AESTHETIC ════════════════════════════════════════════════════════╣
║                                                                      ║
║   calm  ·  minimal  ·  cohesive  ·  whisper-quiet over busy          ║
║   theme: SpenschSuite Light                                          ║
║                                                                      ║
╠═══ MEMORY ═══════════════════════════════════════════════════════════╣
║                                                                      ║
║   feedback   ████████████████████████████████████████  34            ║
║   reference  ██████                                     5            ║
║   project    ███                                        2            ║
║   user       ██                                         1            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

The example is illustrative — render from the actual file contents at
invocation time, do not echo this static block.

## Rules

- Read-only. Never write, edit, or move anything under `~/.me/`.
- One card per invocation. No follow-up commentary unless the user asks.
- If `~/.me/` is empty / unbootstrapped, print a one-line card pointing
  at `/me init` instead of an empty frame.
- If the user passes an argument like `me-card --no-color`, honor it.
