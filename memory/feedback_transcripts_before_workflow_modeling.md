---
name: transcripts-before-workflow-modeling
description: "When asked to visualize/document user's actual workflow, sample transcripts BEFORE drafting from rules or memory; rules describe intent, transcripts show practice"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 38807a38-c8a4-49e8-9c7c-6fd2c00e3d0d
---

When asked to visualize, document, or otherwise model "how the user actually works" — sample recent transcripts in `~/.claude/projects/*/` first. Extract slash-command frequencies, session-start patterns, session-end patterns. Only then draft the artifact.

**Why:** Rules and memory describe intent and standing instructions; transcripts show actual practice. They diverge. Validated 2026-05-16 building a Claude Code workflow visualization: drafted v1+v2 from `~/.claude/rules/` and memory, prominently featured `/jm-catchup`, `/jm-linear-promote-tbd`, `/deploy` as workflow anchors. User pushback: "we don't do jm-catchup either really — can you read some transcripts of past conversations to make this more real?" Explore-on-transcripts pass returned zero uses of those three commands across recent sessions; actual top commands were `/jm-precompact`, `/jm-wrap`, `/compact`, `/jm-pr`. Should've been turn-1 recon, not turn-8 recovery.

**How to apply:** First creative artifact about user's behavior (workflow viz, onboarding doc, "how I work" summary, retrospectives, agent prompts that describe user patterns) → dispatch `Explore` on `~/.claude/projects/-Users-jm-*/` JSONL files → extract actual user-typed commands and session shapes → reconcile against rules/memory. If transcripts contradict rules, transcripts win for the description; flag the contradiction so the user can decide whether rules or practice is the source of truth. See [[user-pivot-is-scope-reduction]] for the adjacent failure (extending the wrong surface mid-implementation).
