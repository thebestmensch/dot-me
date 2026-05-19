---
name: rtk-caches-stat-output
description: "RTK (Rust Token Killer) proxies `stat` and may return cached/stale output when debugging file mtimes. Use `/usr/bin/stat` directly for live mtime reads during bypass-gate mtime-race debugging."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 01923e80-8511-4ca8-8163-54930ec8ceb1
---

When debugging cc-gates bypass-mtime races (codex-stop-gate, drift-gate, etc.), `stat -f '%m %N' <file>` can return stale data because RTK's hook-based command rewriting proxies the stat call.

**Symptom:** Touch a bypass file, run `stat -f '%m %N' /tmp/cc-gates/$SID/skip_codex_gate` — output shows the OLD mtime. Touch again, still old. Conclude touch is broken; it isn't.

**Recovery:** Bypass RTK by using the absolute path: `/usr/bin/stat -f '%m %Sm %N' <file>`. That reads the live filesystem mtime.

**How to apply:**
- Debugging any cc-gates mtime race: `/usr/bin/stat -f '%m %Sm %N'` for ground truth
- Don't conclude "touch isn't working" without a direct stat call
- Same caution applies to other read-only commands RTK rewrites; for stat-class operations, the live-fs read is the authoritative source

Validated 2026-05-19 during `/jm-pr` on OneOnMe PR #103: bypass commit attempts failing despite `touch`. RTK-proxied `stat` showed mtime frozen across multiple touches; `/usr/bin/stat` showed mtime updating correctly. The actual issue was that failed `git commit` (gate-blocked) unstages files — needed `git add` again before retry, not a mtime fix.

Related: [[drift-gate-tokens-per-commit]], codex-dispatch.md gap #9.
