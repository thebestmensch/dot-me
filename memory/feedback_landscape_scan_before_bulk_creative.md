---
name: landscape-scan-before-bulk-creative
description: "For bulk creative-artifact filing (tickets, post ideas, design proposals), run a two-pass landscape scan (broad survey + per-item competitor scan) BEFORE filing, not after. Broad survey alone underestimates saturation."
metadata:
  node_type: memory
  type: feedback
---

When the ask is to file multiple creative artifacts at once (e.g. "make N tickets for blog post ideas", "draft N design proposals", "list N feature pitches"), validate the angles BEFORE filing the artifacts, not after. Two passes, not one.

**Why:** Validated 2026-05-17 filing 10 blog-post tickets in personal-site project. Initial workflow:
1. Ran one broad landscape audit ("survey what's been written about Claude Code in 2026")
2. Filed 10 tickets based on that audit
3. User then asked "what can we do to make sure these are what we want?"
4. Ran a per-item competitor scan (1-2 targeted searches per angle) — discovered 4 angles had direct competitors the broad audit missed (openai/codex-plugin-cc for Codex stop gate, mvara-ai/precompact-hook for pre-compaction, multiple tmux-statusline projects, worktree posts already saturated by Anthropic)
5. None of the 10 tickets survived the second pass without significant reframing; canceled 2, merged 1, rewrote 7

The broad survey answers "is this topic saturated overall?" The per-item scan answers "has the specific claim already been published?" They're different questions with different answers. Skipping the per-item pass means filing artifacts based on a confidently-wrong premise.

**How to apply:** When asked to bulk-file creative artifacts:

1. **Don't file yet.** Treat the ask as "validate angles" not "produce tickets," even if the user said "file tickets."
2. **Run a broad landscape audit** to surface saturated regions and dead-topic lists.
3. **Run a per-item competitor scan** with 1-2 targeted searches per specific claim. Aim to find prior art that names the same thing or makes the same argument. Be brutal: KEEP / SHARPEN / MERGE / KILL per item.
4. **Optionally run a devil's advocate pass** for set-level risks (dupes between siblings, one-note register, security tells).
5. **Then file**, with each artifact carrying its prior-art links and differentiation notes baked into the description.

Skipping straight to filing is the lazy path, and the user will (correctly) ask for validation after. Pre-validation is 5-10 min of subagent work; post-validation costs the same plus an artifact-rewrite pass.

Exception: when the user explicitly says "just file these N specific things I'm dictating" — they've already done the validation. Don't second-guess.

Related: [[oss-launch-checklist]] (competitor scan as launch-discipline section), [[format-clarify-on-visualization]] (clarify-format-up-front pattern), [[transcripts-before-workflow-modeling]] (verify-premise-before-modeling pattern).
