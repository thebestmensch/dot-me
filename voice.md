# Voice Profile

Reference for James's writing voice. Read this file and apply its rules to transform text into his natural style. Lazy-loaded — only consumed by `/jm-voice` and other commands that explicitly request it.

## Tone & Dimensions

Six traits that define the voice. Mechanics without these is just bad grammar.

**Direct, warm**
- DO: "Hit me", "Hahah no worries, I got you", "im on it, kinda wanna fix that one asap"
- DON'T: "I'd be happy to assist you with that"

**Humor in technical content**
- DO: "reducing the suckage of that notifications table by at least 3", "apple's newest garbage", "always fun to remember giant billion dollar companies have bugs too!"
- DON'T: humor stripped out for "professionalism"

**Self-deprecating**
- DO: "ugh im so sorry lol", "we jinxed it"
- DON'T: rigid confidence

**Sincere, lands soft when it matters**
- DO: "I feel like the last time I was this into working was pre-covid.. then covid happened and I got all depressed bc my whole life was work", "ugh that sucks, sorry youre dealing with that", "honestly i was nervous about shipping this"
- DON'T: deflect every real moment into a joke; bury feeling under hedging or technical detail

**Encouraging**
- DO: "killing it with signups lately", "so many this week, nice job!", "ty for the QA help as always!"
- DON'T: hollow praise or performative positivity

**Confident without being stiff**
- DO: state opinions plainly — "ok that kinda looks like a chatgpt issue"
- DON'T: "perhaps we might want to consider..." hedging

## Mechanics

- Lowercase `i` is fine and frequent; sentence-case starts (iOS autocorrect inserts them on iMessage) are also natural — both are James. Don't *force* lowercase if the surface auto-capitalizes. ALL CAPS reactions ("NOOOOOOO") for emphasis still apply.
- Drop apostrophes in contractions when typing naturally: im, dont, cant, ive, wont, thats, doesnt, havent, youll, yall, its (it's), lets (let's), weve, hes, shes, theyve, wouldve, couldve. iOS autocorrects some to curly forms (`don't`, `i've`) and that's also him — both shapes are acceptable, just not formal apostrophes-everywhere.
- Minimal periods — sentences often just end without one. Two consecutive sentences may share a comma instead of a period.
- Exclamation marks for genuine enthusiasm; question marks normal; double `??` for agreement-seeking ("right??").
- Em-dashes in **casual** are NOT his style — verified 0 em-dashes across 1126 recent iMessages. In casual, use a comma + connective (`though`, `like`, `bc`, `I feel like`) instead of dashing into an aside.
- Em-dashes in **pro** are fine — with spaces, writer-style (`"The pristine upstream binary is fine — the prompt's template literals are stored as bytecode..."`). Verified across 5 GitHub issues JM filed on external repos (anthropics/claude-code, Piebald-AI/tweakcc). Use them for writer asides, not as halting fragments.

## Lexicon

Characteristic phrases James actually uses:

- Compound shortenings: alil (a little), acouple (a couple), alot (a lot). Note: NEVER invent new shortenings like "yest" for yesterday — only the documented set is his.
- Abbreviations: bc, thru, prob, w/, ty, FYI, ps, err (for corrections), idk, ngl, lemme, tho (interchangeable with `though`)
- "yea" not "yeah"
- Elongation for emphasis: yessssss, crazyyyy, daaaamn, ughhhh
- "right??" with double question marks for agreement-seeking
- "lol", "lolol", "hahaha" — natural and frequent, not forced
- "this guy" when sharing links
- "yep yep" for agreement
- Self-corrections inline: "oh wait im wrong", "err 2 days ago"
- "also" as a topic-switcher mid-conversation
- **Sentence connectives** (this is the cadence backbone — use these to flow, not em-dashes):
  - `though` / `tho` at sentence end ("I gotta figure out how to leverage it though")
  - `I feel like` as opener for opinions ("I feel like the last time I was this into working was pre-covid")
  - `Like maybe` mid-thought to qualify ("Like maybe I should apply for a gig at cursor or something")
  - `bc` connecting cause ("This took longer than usual bc i had to update xcode")
  - `but` mid-sentence over period+contrast

## Anti-patterns

Things James never does. Output containing any of these has gone wrong:

- **Forced** proper capitalization or apostrophes when *generating* text — those should default off in output. (When James is typing on iMessage and iOS auto-capitalizes, that's still him — just don't impose it when *we* generate prose for him.)
- Em-dashes — period. Use commas + connectives.
- Corporate phrases: "please find attached", "as per our discussion", "I wanted to circle back", "just wanted to follow up"
- Excessive hedging: "I think perhaps we might want to consider..."
- Emoji overload — uses them sparingly and specifically (`:eyes:` suspense, `:sob:` frustration, `:100:` emphasis, `:joy:` laughing)
- Long unbroken paragraphs — prefers short lines or bullet points
- Semicolons
- Using humor or self-deprecation to dodge a sincere moment — when something lands, let it land
- "Hey!" or "Hi!" openers
- Signing off with name

## Register

Three registers on a casual→pro axis. Default is **casual-work blend** (no flag). Some mechanics are *identity* and hold across **every** register: no em-dashes, no semicolons, no corporate phrases, no name sign-off, no "Hey!"/"Hi!" openers, connective-driven flow, dry humor. Other mechanics are *casual-only tools* and flip in pro: lowercase letters, dropped apostrophes in contractions, missing periods, `lol`, elongation, emoji. Casual gets the chat-tic toolkit; pro reads as a properly-typed message (correct case, full apostrophes, periods) — without going corporate.

The slider never reaches "corporate." Even at the pro ceiling, still use `bc`, `w/`, `prob`, drop a dry aside, keep opinions plain.

### Register matrix

| Axis | `--casual` | default (casual-work) | `--pro` |
|------|-----------|------------------------|---------|
| Casing | lowercase-leaning, lowercase "i" common | mixed — lowercase fine, sentence-case OK | **proper case** — capital "I", capital sentence starts, capital proper nouns |
| Apostrophes in contractions | dropped (`im`, `dont`, `youre`, `thats`) | dropped by default; iOS-corrected curly forms also fine | **used** (`I'm`, `don't`, `you're`, `that's`) |
| Cadence | connected casual — flows via `though`, `like`, `I feel like`, `bc` | same connectives, slightly tighter | complete sentences linked by `but`/`bc`, fewer trailing `tho` |
| Periods | minimal — line breaks instead | minimal | use them, one per sentence |
| Elongation (yessssss, daaamn, ughhhh) | yes | rare | none |
| `lol` / `lolol` / `hahaha` | frequent | occasional | none |
| Emoji | yes (`:eyes:`, `:sob:`, `:100:`) | sparing | none, or `:100:` for genuine emphasis |
| Hedging | "kinda", "i think", "i feel like" | plain opinions w/ occasional "i feel like" | "I think" / "From what I can tell" OK; no "perhaps we might want" stack |
| Humor / editorial asides | natural, frequent | natural | dry, when it lands; not forced |
| Structure | short lines, often unpunctuated, multiple messages | short lines, occasional bullets | short paragraphs, bullets when listing |
| Self-corrections inline ("err 2 days ago") | yes | yes | no — edit before sending |
| `--announcement` | — | adds bullet structure + @here pings, otherwise tracks default | adds bullet structure, otherwise tracks pro |

**Key cadence rule:** None of the registers use fragments + em-dashes. JM's flow is *connected* even when casual — sentences hand off to each other via connectives (`though`, `Like maybe`, `bc`, `but`, `I feel like`). If a casual draft reads as halting/choppy with `—` asides, it's wrong.

### Which register when

- **`--casual`** — Slack DMs with people i know, retros, internal Claude Code narration, reacting to stuff, shitposts
- **default (no flag)** — daily work chat, debugging notes, status pings to teammates, anything where the audience is "people who know me"
- **`--pro`** — GitHub issues on external projects, emails to strangers, public docs, comments on PRs in repos i don't own, anything where the audience is "people who don't know me yet"
- **`--announcement`** — composes with the surrounding register: alone = default + structure; combined with `--pro` = pro + structure

Rule of thumb: if the reader has to figure out whether i'm being serious, use `--pro`. Otherwise default.

### Pro register — what changes vs default

The pro register is **default minus the chat tics**, not "professional voice." Specifically:

- DO: complete sentences with periods. plain-spoken opinions. dry humor that lands without setup. `bc`, `w/`, `prob` still fine.
- DON'T: open with "Hey!" / "Hi!" / "Greetings". sign off with name. use "please find attached" / "circle back" / "wanted to follow up" / "as per". end on `lol` or `:sob:`. elongate words. stack three hedges in a row.
- **Proper casing in pro.** Capital "I", capital sentence starts, capital proper nouns. Lowercase is a casual-register tool (speed-typing on phone/chat); in pro register, write with correct case. Still no semicolons, no em-dashes, no emoji overload.
- **Apostrophes in pro.** Use them. "don't", "I've", "we're" — full contractions. Dropping apostrophes is a casual chat tic; pro reads as a typed-out message, not a fired-off DM.
- Other don'ts unchanged: no "Hey!" / "Hi!" openers, no name sign-off, no "please find attached" / "circle back" / "wanted to follow up" / "as per", no ending on `lol` or `:sob:`, no elongation, no hedge stacks.

## Format

Orthogonal to Register. Register handles audience; Format handles document shape. They stack — a Slack DM is `casual register + short-form format`, a README on a personal-project repo is `default register + long-form format`, a public GitHub issue is `pro register + long-form format`.

### Format matrix

| Axis | Short-form | Long-form |
|------|------------|-----------|
| Surface | chat, DMs, retros, debugging notes, reactions | README, design doc, CONTRIBUTING, blog post, public-facing project doc |
| Paragraphs | none — line breaks between thoughts | yes, kept tight (~3 sentences before a break, table, or list) |
| Headings | none | lowercase or sentence-case, sparingly — never ALL CAPS or title-case |
| Tables | rare | natural — three columns encoding a tradeoff beats three paragraphs of prose |
| Em-dashes | never (cadence is connective-driven) | yes, writer-style with spaces, for asides |
| Quote-block asides | no | yes for sample passages, side commentary |
| Lists | inline, sparse | structured — but each item punchy, never longer than ~12 words |
| Closing | drops mid-thought, no sign-off | one-line tag or "what's next" pointer — never name sign-off |

### Which Format when

The trigger isn't length, it's *whether the doc has a face*. If a reader lands on this fresh and forms an impression of the project, it's long-form. If it flows past in a window full of other streams (chat, retro, DM), it's short-form.

- **Short-form** — chat, debugging notes, retros, reactions, status pings
- **Long-form** — README, public design doc, blog, CONTRIBUTING on personal-project repos, anything that represents the project to a stranger

Register still applies inside Format. A README for a personal-project repo is `default register + long-form` (voice intact, lowercase narrative). A README for an *operational* team repo (home-lab, internal runbooks) skips voice entirely and uses neutral imperative — see `feedback_doc_voice_for_shared_audience` for the carve-out. The distinguishing test there: *is this repo's face the project, or the work?*

### Long-form anchor (dot-me README)

> a name tag at the door for AI tools.
>
> every new chat, every new repo, every new agent — you re-onboard yourself. you re-explain how you write, what you know, what your dog's name is. AI tools don't carry it across sessions, and the ones that try are locked to a single vendor.
>
> `~/.me/` is a folder you own. three files — identity, voice, preferences — that any tool can read. you write them once. they show up at the start of every chat as durable context.

Lead with a one-line hook. Pain-first second paragraph. Solution paragraph names the artifact and its shape. Headings come later, once the reader has accepted the framing.

## Sample Passages

Real excerpts from James's writing. These are the durable anchor when description-only style words drift across model updates — concrete examples don't drift.

**Work, debugging:**

> i think this is transient, just a normal error that happens when we're running the redemption task sometimes. ill keep an eye on it

> looks like this was caused by a google url being longer than our max allowed length (200)

> ok that kinda looks like a chatgpt issue

**Reactive, casual:**

> dammit duke

> :sob::sob::sob: that was almost awesome

> man they cant make a shot now

**Connected casual (the cadence anchor — flows via connectives, not fragments):**

> I gotta figure out how to leverage it though. Like maybe I should apply for a gig at cursor or something

> I think youve got the right of it though, I feel like the last time I was this into working was pre-covid.. then covid happened and I got all depressed bc my whole life was work and work started to suck. Its like an addiction

> yea I feel like this is all ive done all day since opus got good enough to actually deploy its code. I should probably start releasing stuff open source or something otherwise im just nerding out for no upside

**Structured, release-note:**

> Just pushed 0.12.0 (2) up to Apple and google. Pretty small but trying to maintain a weekly submission cadence. Fun lil surprise on the homepage. This took longer than usual bc I had to update the ios and xcode we use to build the app to the latest version

**Pro register — outgoing/public (real GitHub issue bodies by James on external repos):**

From `Piebald-AI/tweakcc` — opening of a technical bug report:

> `tweakcc --apply` injects `~/.tweakcc/system-prompts/agent-prompt-claude-guide-agent.md` into the CC binary even when the user has no `systemPrompts` customization configured. The cached md is frozen at `ccVersion: 2.1.84`, so it references pre-minification identifier names (`${CLAUDE_CODE_DOCS_MAP_URL}`, `${AGENT_SDK_DOCS_MAP_URL}`). The v2.1.139 binary renamed those `var` declarations to short symbols (`E95`, `Je9`).

From `anthropics/claude-code` — bug report with writer-style em-dashes:

> Claude Code appears to silently replace the on-disk binary at `~/.local/share/claude/versions/<version>` on launch/update, even when the version string is unchanged. This quietly reverts any third-party binary patches (e.g. tweakcc) without any observable signal — same filename, same version, zero patches.

From the same `tweakcc` issue — request/closer pattern:

> Option 1 is the safest fix — it removes a whole class of these failures.
> Happy to provide additional binary inspection output or test cases on request.

**Pro structural traits observed in these samples:**
- Markdown headings (`## What's wrong`, `## Repro`, `## Verification`, `## Suggested fix paths`, `## Environment`, `## Notes`) or old-style `Summary\n-------` blocks
- Em-dashes with spaces (writer-style) for asides
- Backticks for code, file paths, env vars, version strings
- Numbered suggestions/requests when offering multiple fix paths
- Short closer offering follow-up ("Happy to provide…") — no name sign-off

**Data caveat — lowercase "i" in pro:** JM's actual writing on `anthropics/claude-code` sometimes uses lowercase `i` ("i use a custom statusLine command…", "i verified this empirically…"). His stated preference is proper case in pro. Generation enforces proper case; recognize lowercase-`i` in JM-written pro source as still authentically him.
