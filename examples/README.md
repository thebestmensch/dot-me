# Examples

Four fictional personas demonstrating the shape of `~/.me/`. Each subdir contains a complete `identity.yaml` + `voice.md` + `preferences.yaml` set you can copy-paste as a starting template, then edit to reflect yourself.

| Persona | Shape | Demonstrates |
|---|---|---|
| [`sam-patel/`](sam-patel/) | full, English | Senior writer at a tech company. Fully-populated schema — the "everything filled in" reference. |
| [`maya-okonkwo/`](maya-okonkwo/) | sparse, English | Early-career backend engineer eight months into her first job. Most optional fields absent — shows what a v0.1 `~/.me/` looks like before preferences accrete. |
| [`marcus-webb/`](marcus-webb/) | non-engineer, English | UK product manager. No `editor`/`shell`/`color_temperature` because they don't apply; tooling list reflects PM workflow (Obsidian, Linear, Notion). Shows the spec works for non-coding agentic work. |
| [`aki-tanaka/`](aki-tanaka/) | polyglot, mixed-language | Japanese frontend engineer in Kyoto. `voice.md` is in Japanese; `knows_about` stays English (keywords); `preferences.yaml` mixes both. Shows the schema doesn't assume English content. |

## Picking a starting template

- **Just starting?** Copy `maya-okonkwo/` and add what's missing for you.
- **Want to see what "fully populated" looks like?** Read `sam-patel/`.
- **Not a developer?** Read `marcus-webb/` for what to drop and what to add.
- **Writing primarily in a non-English language?** Read `aki-tanaka/` for how the schema handles mixed-language content.

All four personas are fictional — names, employers, locations, and details are invented. The content is illustrative, not a profile of any real person.

## How to use a template

```bash
mkdir -p ~/.me
cp examples/<persona>/* ~/.me/
# edit to reflect yourself, then install your consumer of choice — see ../README.md
```
