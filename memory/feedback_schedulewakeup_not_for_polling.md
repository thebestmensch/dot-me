---
name: schedulewakeup-not-for-polling
description: "ScheduleWakeup is /loop-dynamic-mode only; using it as a generic poll-after-N-seconds primitive (CI watch, deploy wait) is rejected by the harness. Use `timeout N bash -c 'until <check>; do sleep S; done'` with `run_in_background:true` instead."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 01923e80-8511-4ca8-8163-54930ec8ceb1
---

`ScheduleWakeup` is documented as a `/loop`-only tool: it accepts a `prompt` that must be either a real `/loop` input or the `<<autonomous-loop-dynamic>>` sentinel, and the runtime rejects anything else as a misuse pattern. It is NOT a generic "ping me in N seconds" primitive.

**Why:** During `/jm-pr` on PR #103 (OneOnMe Berkeley retry), needed to wait for CI + CR re-review (~2 min) after pushing. Reached for `ScheduleWakeup({delaySeconds: 120, prompt: "/jm-pr 103"})` — runtime rejected with explicit pointer to `feedback_afk_no_prompts.md` and `feedback_bg_loop_predicate_ceiling.md`: "ScheduleWakeup is /loop-dynamic-mode ONLY".

**How to apply:**
- Watching CI checks, deploy completions, remote queues, or any external state with no harness notification: use `timeout 600 bash -c 'until <predicate>; do sleep 20; done'` with `run_in_background: true`. The harness fires a completion notification when the bg job exits (predicate true OR timeout hit).
- **Verify the predicate in foreground FIRST** before dispatching the bg loop. An unmatched predicate produces an infinite-spin shell that the auto-notification never fires on. One bash call with the bare check, expect exit 0, then dispatch.
- **Bound with `timeout`** so a broken predicate fails loud, not silent. `gh pr checks 103 --watch` is a built-in alternative for the specific GH-PR case.
- ScheduleWakeup's actual use case: a `/loop` session where you want to self-pace iterations of a recurring task; the `prompt` parameter passes the verbatim `/loop` input back through.

Related: [[parallel-cc-single-writer]], [[bg-loop-predicate-ceiling]] (referenced by harness rejection text).
