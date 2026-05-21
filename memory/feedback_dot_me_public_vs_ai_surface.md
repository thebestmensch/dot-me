---
name: dot-me-public-vs-ai-surface
description: "identity.yaml blurb is canonical for AI consumers but isn't automatically safe to lift onto crawler-indexable public pages — surface the privacy tradeoff before copying"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8bcb96e-b145-4d69-abc7-a355d5641a54
---

When copying the `~/.me/identity.yaml` blurb verbatim onto a public crawler-indexable surface (jamesmensch.com homepage, public bio cards, OSS profile pages), pause and surface the privacy tradeoff to JM before changing. The dot-me blurb mentions Sarah by name and the three dogs by name (Bean, Gia, Ruthie); that's appropriate context for AI agents but creates social-engineering / account-recovery / correlation surface when indexed by search.

**Why:** Validated 2026-05-21 on the personal-site round-2 polish. JM said "check dot-me, i believe its up to date there" → I copied the full blurb verbatim onto the homepage bio. Codex adversarial-review caught it: "Public bio now exposes household member and pet names." JM chose the strip-names-keep-family-mention variant when surfaced. The "dot-me is up to date" signal answers "is this content current?" not "is this content safe for a public page?" — two different questions.

**How to apply:**
- Public homepage / OSS README / crawler-indexable bio: strip partner name + pet names, keep role narrative and city. Default phrasing: "with my partner and three dogs" not "with Sarah and our three dogs: Bean, Gia, and Ruthie."
- dot-me identity.yaml itself stays unchanged — it remains canonical for AI consumers.
- Ask before lifting verbatim. Don't assume "dot-me is current" = "dot-me is publish-safe."

Related: [[feedback_landscape_scan_before_bulk_creative]] for the broader pattern of pre-flight checks on public-facing content; [[user_role]] and `~/.me/identity.yaml` for the canonical AI-consumer blurb.
