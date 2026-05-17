---
name: ghostty-macos-menu-keybind-intercept
description: "On macOS, Ghostty default keybinds tied to menu items (Edit > Undo, etc.) fire before user keybind overrides — must `unbind` first, then rebind"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 48cf01b3-eb3c-4159-b5cd-373fbe84add1
---

On macOS, any Ghostty default keybind wired into the main menu fires **before** Ghostty's keybind layer processes user overrides. AppKit/macOS handles menu activation itself, so a config entry like `keybind = super+shift+t=text:\x01T` silently has no effect when there's also a default `super+shift+t=undo` in the Edit menu.

Symptom: keybind looks correct in `ghostty +list-keybinds` (user binding wins), but pressing the chord triggers the menu action (Undo, etc.) instead of the user's text/action.

**Fix:** unbind the menu binding first, then rebind:

```
keybind = super+shift+t=unbind
keybind = super+shift+t=text:\x01T
```

Ghostty docs explicitly call this out: "On macOS, bindings in the main menu will trigger before any remapping is done. To workaround this, you should unbind the menu items and rebind them using your desired modifier."

Known affected defaults (Ghostty 1.3.1, may grow):

- `super+shift+t=undo` (Edit > Undo)
- `super+shift+z=redo` (Edit > Redo)
- `super+q=quit`
- Other Edit-menu / tab-management defaults

Watch for this whenever Ghostty upgrades and a previously-working keybind goes silent — diff `ghostty +list-keybinds --default` against your config for new menu-backed defaults.
