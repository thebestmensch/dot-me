#!/usr/bin/env bash
#
# dot-me voice-enforcement hook (Claude Code UserPromptSubmit) — reference example.
#
# Backstop for the §6.1 "compact-always, full-lazy" load contract. voice.compact.md
# always-loads the floor; this hook detects prose-generation intent in the prompt and
# injects the FULL voice.md for that turn, so deep prose work (bios, blog drafts,
# register-specific output) gets the rich profile without the agent having to notice
# and fire a load itself.
#
# §6.3 boundary (this is the whole point): the hook INJECTS voice.md into the
# instruction context via stdout — harness-side context assembly, the same tier as
# session-start loading. It does NOT add a model-callable surface that returns ~/.me/
# content as a tool result. That distinction is what keeps this compliant: the harness
# pulls the content, not the model deciding to call a fetch tool.
#
# Install (user-global, ~/.claude/settings.json):
#   "hooks": {
#     "UserPromptSubmit": [
#       { "hooks": [ { "type": "command",
#                      "command": "~/.me/hooks/voice-enforcement.sh" } ] }
#     ]
#   }
# Drop this file at the referenced path (chmod +x), or point the command at wherever
# you keep it. Per-project installs work too (.claude/settings.json).
#
# Behavior: no prose trigger -> silent no-op (exit 0, no output). voice.md missing ->
# silent no-op. Match -> voice.md printed to stdout, which Claude Code adds to the
# turn's context.

set -euo pipefail

VOICE_FILE="${DOTME_VOICE_FILE:-$HOME/.me/voice.md}"

# Prose-generation intent triggers. Tune to taste; over-matching just loads voice.md
# on a turn that didn't strictly need it (cheap), under-matching reverts to the
# compact-only floor (still safe). Word-boundary matched, case-insensitive.
TRIGGERS='draft|bio|blurb|rewrite|reword|rephrase|tagline|headline|copy|caption|email|reply|respond|post|tweet|thread|blog|write[ -]?up|write me|ghostwrite|in my voice|sound like me|announcement|changelog|release notes'

# Pull the user prompt out of the hook's stdin JSON. Prefer jq; fall back to a
# permissive grep so the hook still fires without jq installed.
payload="$(cat)"
if command -v jq >/dev/null 2>&1; then
  prompt="$(printf '%s' "$payload" | jq -r '.prompt // empty')"
else
  prompt="$payload"
fi

[ -n "$prompt" ] || exit 0
printf '%s' "$prompt" | grep -qiE "(^|[^[:alnum:]_])(${TRIGGERS})([^[:alnum:]_]|$)" || exit 0
[ -f "$VOICE_FILE" ] || exit 0

# Match. Inject the full voice profile for this turn.
printf '%s\n\n' "[dot-me] Prose-generation intent detected. The user's full voice profile is loaded below; apply it to any user-facing text you generate this turn. On conflict, this file overrides the always-loaded voice.compact.md."
cat "$VOICE_FILE"
exit 0
