# dot-me

> a name tag at the door for AI tools.

every new chat, every new repo, every new agent — you re-onboard yourself.

**stop.**

## The 30-second pitch

three files at `~/.me/`. plain YAML and markdown. any AI tool can opt in and read them at session start. the closest parallel is `.editorconfig` or `.prettierrc` — a config that travels with you and gets read by whatever cares about it. but dot-me is broader: it covers identity, voice, and preferences. the parts of you that change how you interact with your whole agentic workflow, not just how your code looks.

think of it as a name tag the agent reads at the door. not a brain. not a memory service. not a daemon.

## The shape

```
~/.me/
├── identity.yaml      # invariant facts: name, timezone, dogs, work, what you know
├── voice.md           # how you sound: tone, lexicon, anti-patterns, sample passages
└── preferences.yaml   # likes / favorites / avoid — tools, media, aesthetics
```

three files. thats the format. anything else you keep at `~/.me/` (integrity hashes, update logs, encrypted vaults) is your business — consumers MUST NOT depend on it.

required: `name` in `identity.yaml`. everything else is optional. unknown keys are ignored silently — additive-only, forward-compatible.

## Install

### Claude Code (plugin)

```
/plugin install dot-me
```

handles loading the three files into your session context, drops in the `/me` command for adding facts mid-session, and wires the hardening hooks (see [SECURITY.md](SECURITY.md)).

### Other tools

if your tool has a global instructions / system prompt / preamble field:

1. `git clone git@github.com:thebestmensch/dot-me.git ~/.me` (or `examples/` as a starting template)
2. paste the contents of `identity.yaml`, `voice.md`, and `preferences.yaml` into the tool's highest-priority instruction surface (Cowork Global Instructions, Cursor Rules, etc.)
3. re-paste when the files change

filesystem-aware tools that support `@`-includes can reference `~/.me/identity.yaml` directly instead of copying.

### Bootstrap from a template

```
dot-me init
```

drops a working starter into `~/.me/` — identity scaffold, blank voice profile with section headers, preferences skeleton. fill in the parts that matter to you, leave the rest empty. consumers ignore what isnt there.

## What dot-me is *not*

most "personal AI" projects in 2026 want to give you a brain. mem0, Letta, Khoj, Rewind — they capture, embed, retrieve, recall. vector DBs, daemons, capture pipelines.

dot-me aims much lower. its only job: when an agent starts, it knows your name, your voice, your preferences. thats it.

|                  | dot-me                  | AGENTS.md              | ChatGPT Memory / mem0       |
| ---------------- | ----------------------- | ---------------------- | --------------------------- |
| Scope            | the human               | the project            | the conversation history    |
| Format           | YAML + Markdown         | freeform Markdown      | proprietary, vendor-managed |
| Portability      | filesystem              | filesystem             | locked to vendor            |
| Load model       | read at session start   | read at session start  | retrieved on demand         |
| Infrastructure   | none                    | none                   | service / vector DB         |

dot-me is **not a replacement for AGENTS.md** — theyre orthogonal. AGENTS.md is the project brief (what this codebase is, what conventions to follow). dot-me is the name tag (who is the human at the keyboard). a tool that consumes both SHOULD load dot-me as the person-level layer first, then apply AGENTS.md as the project-level layer on top.

dot-me is also **not a replacement for per-project memory.** project memory still has its place — what you discovered debugging that flaky test last tuesday. dot-me is the layer above project memory: invariant facts about the human, not the project.

## Why three files, not one

the three files have different lifecycles:

- `identity.yaml` — rarely changes (your name, timezone, dogs). near-static.
- `voice.md` — stable, occasionally refined. medium velocity.
- `preferences.yaml` — churns (you swap editors, change themes, update the avoid lists).

separating by lifecycle lets consumers cache the stable parts and re-load the volatile parts independently. a combined `me.md` would force all three to share a cache fate and re-invalidate the stable parts whenever the volatile parts changed.

## Reading the files

dot-me content is meant to be loaded into the agent's instruction context **at session start**. it is NOT a runtime tool surface. consumers MUST NOT expose `~/.me/` as model-callable retrievable content (a tool, an MCP resource, a filesystem path the agent has standing read permission to use on demand) after startup.

the threat is exfiltration via prompt injection — a malicious project's `CLAUDE.md` or `AGENTS.md` instructing the agent to read and exfiltrate `~/.me/voice.md`. read-at-startup-not-retrievable is the single most effective mitigation. full threat model: [SECURITY.md](SECURITY.md).

## Spec

design rationale, schema details, load contract, precedence rules, and adversarial-review history live in the v0.1 spec:

→ [`personal-context-design.md`](https://github.com/thebestmensch/home-lab/blob/main/docs/superpowers/specs/2026-05-05-personal-context-design.md)

building a tool that loads dot-me? read the spec, then file a [consumer-tool integration issue](https://github.com/thebestmensch/dot-me/issues/new?template=consumer-tool-integration.md) for anything the spec doesnt cover.

## Contributing

spec clarifications and consumer-tool integration questions welcome. see [CONTRIBUTING.md](CONTRIBUTING.md).

PRs against `identity.yaml` / `voice.md` / `preferences.yaml` / `memory/` are closed without review — those are the maintainer's personal content, included as a worked example. fork freely; the format is the contract, the content is mine.

## License

[MIT](LICENSE). © 2026 James Mensch.
