#!/usr/bin/env bash
# SessionStart integrity check for ~/.me/.
# Compares actual file hashes against baseline in ~/.me/.integrity.
# Drift = something wrote to ~/.me/ outside /me (any subcommand) or `git pull`.
set -euo pipefail

ME_DIR="$HOME/.me"
[[ -d "$ME_DIR" ]] || exit 0          # graceful no-op if ~/.me/ doesn't exist (new machine)

INTEGRITY="$ME_DIR/.integrity"
[[ -f "$INTEGRITY" ]] || exit 0       # graceful no-op on first run

drifted=()
while read -r expected file; do
  [[ -z "${expected:-}" || -z "${file:-}" ]] && continue   # skip blank lines
  [[ "$expected" == \#* ]] && continue                      # skip comments
  if [[ ! -f "$ME_DIR/$file" ]]; then
    drifted+=("$file (missing)")
    continue
  fi
  actual=$(shasum -a 256 "$ME_DIR/$file" 2>/dev/null | awk '{print $1}' || true)
  [[ "$actual" == "$expected" ]] || drifted+=("$file")
done < "$INTEGRITY"

if (( ${#drifted[@]} > 0 )); then
  echo "WARN: ~/.me/ integrity drift detected: ${drifted[*]}" >&2
  echo "Files modified outside /me (any subcommand) or git pull. Inspect ~/.me/ before relying on context." >&2
fi
