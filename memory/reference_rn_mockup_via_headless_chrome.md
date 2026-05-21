---
name: rn-mockup-via-headless-chrome
description: "React Native visual preview without a sim — HTML mockup using real assets + brand tokens, rendered via Google Chrome --headless --screenshot, then copied to macOS clipboard as PNG via osascript so the user can drag-drop into a PR comment."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f37b83a6-7000-4955-b332-20bb21c6dec2
---

When a background CC session needs to produce a visual preview of a React Native screen but the sim isn't installed or the dev client isn't running, build an HTML mockup using:

- the real asset files (PNG / SVG from `mobile-app/assets/`) referenced by relative path
- Google Fonts CDN for Inter (matches the app)
- exact brand tokens copied as CSS custom properties from `mobile-app/theme/tokens.ts`
- exact spacing values (4px grid) and font sizes from the design philosophy

Render via headless Chrome (Chrome is installed at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` on JM's box; no `chrome`/`chromium` binary in PATH):

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --hide-scrollbars --no-sandbox \
  --window-size=460,940 --virtual-time-budget=2000 \
  --screenshot=mockup.png \
  file://$PWD/mockup.html
```

(`--virtual-time-budget=2000` is required so Google Fonts + image loads complete before capture; without it the screenshot fires immediately and text renders in a fallback font.)

To put the PNG on the macOS clipboard so the user can paste it directly into a GitHub PR comment (CLI can't upload assets to github.com):

```bash
osascript -e 'set the clipboard to (read (POSIX file "/abs/path/to/mockup.png") as «class PNGf»)'
```

The `«class PNGf»` (note the angled « » brackets, not chevrons) is the AppleScript type code for PNG clipboard data. `pbcopy` only handles text and can't be used for binary clipboard.

**Limitations:**
- Mockup is approximate, not a real-device screenshot. Composition + typography fidelity is good; native widgets (status bar, keyboard, native back chevron) are emoji/svg stand-ins.
- Use only when the goal is design-direction review, not pixel-perfect QA. For pixel QA the dev-client build + sim is still required.
- Validated 2026-05-20 on OOM-120 terminal state preview; JM drag-dropped the result into PR #126.

**Files to write under:** `.qa/` in the project root (already gitignored in workspace settings), so `rm -rf .qa/` cleans the session.
