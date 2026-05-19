---
name: uv-prerelease-transitive-block
description: uv refuses to resolve when a dep pulls a pre-release transitive (e.g. mixpanel 5.1.0 → json-logic==0.7.0a0). Symptom + workaround.
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5b0ab023-7db0-4994-9078-1c755e40bf61
---

## Symptom

`uv lock` fails with:

```
× No solution found when resolving dependencies for split (markers: ...):
  Because there is no version of <transitive>==X.Y.Za0 and <direct>==A.B.C
  depends on <transitive>==X.Y.Za0, we can conclude that <direct>==A.B.C cannot be used.
  ...
  hint: `<transitive>` was requested with a pre-release marker (e.g.,
  <transitive>==X.Y.Za0), but pre-releases weren't enabled (try:
  `--prerelease=allow`)
```

Validated 2026-05-19 on `mixpanel==5.1.0`, which depends on `json-logic==0.7.0a0` (alpha). The mixpanel direct floor `>=5.1.0` was unsatisfiable in `uv lock` until reverted to `>=4.11.1`.

## Why this happens

PyPI semantics: a release that lists a pre-release transitive as a hard `==` requirement effectively requires `--prerelease=allow` at the resolver. uv refuses by default. pip + poetry do the same.

## How to recognize during package audit

Run `uv lock` against the bumped manifest in a scratch worktree. If it errors with the "pre-release marker" hint, the safe-patches PR can't include this dep. Either:

1. Hold the floor at the previous version, file a ticket pointing to the next patch release (`5.1.1` typically un-pre-releases the transitive).
2. Pin `<transitive>` explicitly in `tool.uv.constraint-dependencies` to a release version — this is the heavyweight fix and only worth it if the bump is required.
3. Add `--prerelease=allow` to `uv lock` invocations — DON'T do this lightly; opens the whole resolver to pre-releases globally.

Default to option 1. The cost of waiting one patch release is almost always lower than the cost of explaining option 2 to a reviewer.

## Detection check for audits

Tools like `/oom-package-audit` should call this out as a discrete bucket: "uv-blocked due to transitive pre-release," distinct from "safe" and "coordinated." It's neither — it's blocked by the resolver until the upstream cuts a clean release.
