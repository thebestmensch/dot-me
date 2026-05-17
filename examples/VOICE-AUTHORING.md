# Voice Authoring Guide

> Why write a voice profile? Because your voice is how you want the AI to write FOR you, the language part of your working agreement.

`voice.md` is the highest-leverage file in `~/.me/`. A strong `voice.md` visibly changes every paragraph the agent generates on your behalf; a weak one is invisible. The delta between a weak and strong `voice.md` is larger than the delta between having and not having `identity.yaml`.

This guide walks you through six introspection questions, each with a worked answer-to-file mapping. Run through them in order; the questions build on each other. By the end you should have a `voice.md` that produces noticeably different output than the default "I'm direct and don't like hedging" baseline most first drafts converge on.

A note before starting: write in the language you actually write in. `voice.md` is plain prose loaded into context, not parsed structure. If you write primarily in Japanese, Spanish, or Welsh, write the profile in that language. The schema doesn't assume English (see `aki-tanaka/` for a mixed-language example).

---

## Question 1: What are the *quiet* traits in your writing?

**Why it matters.** It's tempting to capture only the traits a reader would notice in the first 30 seconds: humor, bluntness, hedging. But generation defaults strip whatever isn't named, so unnamed traits that *do* show up in your writing (sincerity, vulnerability, restraint, formality, warmth) quietly disappear from output. This is the highest-ROI insight in the entire spec (SPEC §5.2), and it's the one most often missed.

**How to find them.** Read three things you've recently written: a Slack message to a coworker, a short essay or post, a personal text to a friend. For each, list the traits a stranger would describe back to you. Then list the traits that are *present but unstated*: the warmth threading through a critique, the dry undercut at the end of a sincere paragraph, the patience or impatience in how you walk through an explanation.

**Mapping to file structure.** Quiet traits go under `## Tone & Dimensions` alongside loud ones, each with a one-line rule plus a DO/DON'T pair. The DO/DON'T format forces concreteness; abstract rules ("I'm warm") generate generic output.

**Example.**
```markdown
**Warm but unsentimental**
- DO: "Glad this is finally landing. The cover treatment really earns its space."
- DON'T: "I'm so thrilled to share this with you!"
```

The trait "warm" is loud. "Unsentimental" is the quiet pair. Naming both stops the agent from defaulting to performative warmth.

---

## Question 2: What words and phrases are *yours*?

**Why it matters.** Vocabulary is identity-shaped. The agent will reach for safe, AI-shaped phrasing ("delve into," "leverage," "in today's fast-paced world") unless your lexicon is named. A six-word list of phrases you actually use beats a paragraph describing "a casual, modern voice."

**How to find them.** Pull up your recent writing again. Note: words you use that most people don't, phrases you reach for repeatedly, intensifiers and qualifiers that recur ("genuinely," "fairly," "a bit," "actually"). Also note words you *avoid*: corporate phrases, particular cliches, register-mismatched words.

**Mapping to file structure.** Goes under `## Lexicon`. Two lists: "Use" and "Avoid". Short.

**Example.**
```markdown
## Lexicon

Use: actually, genuinely, the thing is, fair enough, sharp, lands, earns

Avoid: leverage, delve, robust, in today's, ecosystem, journey, unlock
```

---

## Question 3: What are your mechanical tics?

**Why it matters.** Punctuation and sentence rhythm carry voice even when word choice doesn't. AI-generated prose tends toward em-dashes, parallel three-item lists, and balanced subordinate clauses. Your real writing probably has specific rhythm quirks: short sentences for emphasis, parenthetical asides, semicolons over commas, no em-dashes, fragments. Naming them lets the agent reproduce the cadence.

**How to find them.** Look at your last five paragraphs. Are sentences mostly short, mostly long, or mixed? Where do you put emphasis: italics, caps, bold, asides, a one-word sentence? How do you handle lists: comma-separated in-line, bulleted, three with "and"? Any punctuation marks you use a lot or actively avoid?

**Mapping to file structure.** Goes under `## Mechanics`. Bulleted, one rule per line.

**Example.**
```markdown
## Mechanics

- No em dashes. Use commas, semicolons, parens, or rewrite. Em dashes read as AI-generated.
- Fragments fine for emphasis. "Not a bug. A feature."
- Lists prefer comma-separated in prose over bullets, unless three or more items.
- One-clause sentences for the punchline at the end of a paragraph.
```

---

## Question 4: What patterns make you *flinch* when you read them?

**Why it matters.** Naming anti-patterns is as load-bearing as naming positive traits. The agent has strong defaults toward certain shapes (hedging, throat-clearing, "I'd be happy to help"). A positive rule says "be direct"; an anti-pattern says "never write 'I'd be happy to help'." The anti-pattern is more enforceable because it names the specific failure mode rather than a vague aspiration.

**How to find them.** Read AI-generated text in your voice (ask any chatbot to write something as you, given a paragraph sample). Mark every sentence that makes you cringe. Categorize: hedging? performative enthusiasm? throat-clearing? meta-commentary? Each cringe is an anti-pattern candidate.

**Mapping to file structure.** Goes under `## Anti-patterns`. One bullet per pattern, with the specific phrasing called out where possible.

**Example.**
```markdown
## Anti-patterns

- No "I'd be happy to help" / "Great question!" / "Sure, here's..." openings.
- No throat-clearing ("It's worth noting that...", "One thing to consider..."). Just say the thing.
- No three-item parallel lists when two would do. The third item is usually filler.
- No "in today's [adjective] world" framings.
```

---

## Question 5: Where does your voice *shift*?

**Why it matters.** Most people have at least two registers: one for colleagues, one for friends, sometimes a third for public writing. A single flat voice profile produces uniformly-pitched output; naming the shifts lets the agent match the audience.

**How to find them.** Ask yourself: do you write differently in Slack vs. email? In a code review vs. a launch announcement? Talking to your boss vs. a peer? Note the axes that shift: formality, hedging, jokes, emoji, length.

**Mapping to file structure.** Goes under `## Register`. A short paragraph or two on what shifts and when. This is one of the few prose-shaped sections; bullets break the nuance.

**Example.**
```markdown
## Register

Default mode: friendly-direct. Drops to plain-direct in code review (no warmth padding, the work is the work). Shifts up to slightly-warm for product announcements where the team's energy is the message.

Slack vs. async writing: Slack is short, fragmentary, comma-spliced. Async writing (PR descriptions, design docs) is composed sentences and uses semicolons.
```

---

## Question 6: Can you produce *sample passages*?

**Why it matters.** This is the single highest-leverage section in the file. Concrete examples beat prose descriptions because the agent can pattern-match. A paragraph describing "warm but unsentimental" is generative ambiguity; a paragraph *demonstrating* it is calibration.

Sample passages also catch what introspection misses. If a sample you write has a trait the trait list doesn't mention, that's a gap; name it (back to Question 1).

**How to write them.** Three to five passages of 50 to 150 words each. Pick scenarios that span your registers (a PR description, an announcement, a sympathy note, a critique, a debrief). Write them as if you were writing them for real. Don't sanitize or fancy them up.

**Mapping to file structure.** Goes under `## Sample Passages`. Each passage gets a one-line scenario label, then the passage.

**Example.**
```markdown
## Sample Passages

**Announcing a launch in a team channel:**

Bookshelf 2.0 is live. Series cache rebuild took longer than it should have (Calibre split-brain, fixable, fixed now), but the cover treatment is sharp and the empty states finally feel like the rest of the app. Cheryl carried this one. Worth a read of the migration PR if you're curious how the dual-source schema landed.

**Pushing back on a design proposal:**

The two-column layout is fine but I think we're solving the wrong problem. The complaint wasn't "I can't find the action button," it was "I don't know what state I'm in." Adding a column doesn't address that. What if we tried a state pill at the top instead?
```

---

## A worked example, end-to-end

Suppose you ran through the questions above and your answers were:

1. **Quiet traits:** I'm dry but sincere. Most rules I write capture the dryness but lose the sincerity. I also have an aversion to overclaiming.
2. **Lexicon:** Use "genuinely," "the thing is," "fair," "sharp." Avoid "leverage," "robust," anything with "journey."
3. **Mechanics:** No em dashes. Short sentences for emphasis. Parentheticals for asides, not commas.
4. **Anti-patterns:** "I'd be happy to help." "It's worth noting." Three-item lists where two would do.
5. **Register shifts:** Slack is fragmentary; PR descriptions are composed. Critique drops warmth.
6. **Sample passage:** "Bookshelf 2.0 is live. Series cache rebuild took longer than it should have (Calibre split-brain, fixable, fixed now), but the cover treatment is sharp and the empty states finally feel like the rest of the app. Worth a read of the migration PR if you're curious how the dual-source schema landed."

The resulting `voice.md` excerpt:

```markdown
## Tone & Dimensions

**Dry but sincere**
- DO: "Worth a read of the migration PR if you're curious how the dual-source schema landed."
- DON'T: "This is going to be such an exciting change for the whole team!"

**No overclaiming**
- DO: "Cover treatment is sharp and the empty states finally feel like the rest of the app."
- DON'T: "We've built something truly transformative."

## Mechanics

- No em dashes. Use commas, semicolons, parens, or rewrite.
- Short sentences for emphasis.
- Parentheticals for asides; commas for in-line continuation.

## Lexicon

Use: genuinely, the thing is, fair, sharp, lands, earns
Avoid: leverage, robust, journey, ecosystem, in today's

## Anti-patterns

- No "I'd be happy to help" / "Great question!" openings.
- No "it's worth noting" throat-clearing.
- No three-item parallel lists when two would do.

## Register

Default mode: dry-direct in async writing, fragmentary in Slack. Drops warmth for critique. Composed sentences in PR descriptions and design docs; semicolons appear there but not in Slack.
```

That excerpt produces visibly different output than the generic "I'm direct and don't like hedging" baseline, because:

- "Dry but sincere" names a *quiet* second trait that would otherwise vanish (most first drafts capture only "dry").
- The DO/DON'T pairs anchor the trait in specific phrasings, not abstractions.
- The lexicon list short-circuits the agent's reach for AI-shaped vocabulary.
- The anti-patterns name specific failure modes the agent will otherwise produce by default.

---

## Iterating

Your first `voice.md` won't be right. Generate something with it, read the output, mark where the voice slipped. Each slip is either: a trait you didn't name, an anti-pattern you didn't list, or a register the file doesn't cover. Add it. Re-test.

The file is meant to grow. `maya-okonkwo/voice.md` is what a v0.1 looks like; `sam-patel/voice.md` is what a fully-populated version looks like. Most authors land somewhere between the two after three or four iterations.

---

## See also

- [`SPEC.md §5.2`](../SPEC.md): the canonical `voice.md` schema and section conventions
- [`sam-patel/voice.md`](sam-patel/voice.md): fully-populated reference
- [`maya-okonkwo/voice.md`](maya-okonkwo/voice.md): sparse v0.1 starting point
- [`aki-tanaka/voice.md`](aki-tanaka/voice.md): non-English worked example
- [`marcus-webb/voice.md`](marcus-webb/voice.md): non-engineer worked example
