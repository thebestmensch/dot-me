---
name: no-emdashes
description: "Avoid em dashes (—) in written output. Reads as AI-generated in 2026. Use comma, parens, period, or rewrite. No semicolons (banned identity-wide per voice.md)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f5325c59-e29d-4684-8e96-4b99a7eef608
---

Don't use em dashes (—) in any written output: docs, READMEs, commit messages, PR bodies, code comments, user-facing copy, chat responses.

**Why:** Em dashes have become a strong tell for AI-generated text in 2026. Even when grammatically clean, they make prose sound LLM-flavored. James wants outgoing writing to read as human-authored.

**How to apply:**
- Replace with comma, parentheses, period, or rewrite the sentence. Semicolons are NOT a valid replacement (banned identity-wide per `voice.md`)
- En dashes (–) for ranges are fine (e.g. "pages 4–7", "2024–2026")
- Hyphens (-) in compound words are fine
- Quoted source material stays verbatim (don't rewrite other people's text)
- Applies to all `.me`/[[no-uber-for-x-positioning]]-style OSS surfaces, personal writing via [[voice-for-outgoing]], and ad-hoc chat

Related: [[voice-for-outgoing]], [[voice-register-routing]].
