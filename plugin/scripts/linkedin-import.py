#!/usr/bin/env python3
"""linkedin-import.py — ingest a LinkedIn data export into ~/.me/identity.yaml.

Maps a LinkedIn export (Full tier preferred — see "Tiers" below) onto the
EXISTING dot-me identity schema:

    Profile.csv   -> location.city, website, social_profiles[], headline (gap-fill)
    Positions.csv -> work[] (current roles) + past_work[] (ended roles, with
                     start / end / summary)
    Education.csv -> education[]  (new in spec v0.5)

Design rules (SPEC + JM-254 acceptance criteria):
  - Reuse, don't reinvent. work[]/past_work[] already exist (v0.3); Positions
    maps onto them rather than a parallel work-history file.
  - Non-destructive. Curated scalar fields (headline, website, blurb) are
    gap-filled only — a non-empty existing value is never overwritten without
    --force. LinkedIn fills holes, it does not flatten your curation.
  - Idempotent. work/past_work/education merge BY KEY (org+role / institution+
    degree). Re-running with a fresher export updates matched entries in place
    and preserves manual-only sub-fields (e.g. a hand-written `mission`); it does
    not append duplicates.
  - Comment-preserving. Round-trips identity.yaml via ruamel.yaml so the file's
    hand-written comments and field order survive the write.
  - Tier-aware. A Basic export (no Positions.csv / Education.csv) is handled
    gracefully: it imports what it can and reports, per section, what a Full
    export would add.

Usage:
    uv run --with ruamel.yaml python linkedin-import.py <export.zip|export-dir> [opts]

Options:
    --identity PATH   target identity.yaml (default: $DOT_ME_DIR/identity.yaml
                      or ~/.me/identity.yaml)
    --dry-run         print the merged identity.yaml to stdout, write nothing
    --force           allow overwriting non-empty curated scalar fields
    --no-integrity    skip the .integrity refresh after writing

Exit codes: 0 ok, 2 usage error, 1 runtime error.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path

try:
    from ruamel.yaml import YAML
except ImportError:
    sys.stderr.write(
        "error: ruamel.yaml is required. Run via: uv run --with ruamel.yaml python linkedin-import.py ...\n"
    )
    sys.exit(1)

# Files the importer reads, by basename (LinkedIn nests some under subdirs).
PROFILE = "Profile.csv"
POSITIONS = "Positions.csv"
EDUCATION = "Education.csv"

# Identity scalar fields the importer may gap-fill from Profile.csv.
_SCALAR_GAPFILL = ("headline", "website")


def _yaml() -> YAML:
    y = YAML()
    y.preserve_quotes = True
    y.width = 4096  # don't wrap long scalars (blurb, summaries)
    y.indent(mapping=2, sequence=2, offset=0)
    return y


def _find(root: Path, basename: str) -> Path | None:
    """LinkedIn nests files inconsistently; match by basename anywhere under root."""
    if (root / basename).is_file():
        return root / basename
    hits = [p for p in root.rglob(basename) if p.is_file()]
    return hits[0] if hits else None


def _read_csv(path: Path) -> list[dict[str, str]]:
    # LinkedIn exports are UTF-8 (sometimes with BOM). Header keys vary in case
    # across export vintages, so callers normalise via _col().
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [dict(row) for row in csv.DictReader(fh)]


def _col(row: dict[str, str], *names: str) -> str:
    """Case/space-insensitive column lookup; returns the first match, stripped."""
    norm = {re.sub(r"\s+", " ", k).strip().lower(): v for k, v in row.items()}
    for name in names:
        v = norm.get(name.lower())
        if v is not None and v.strip():
            return v.strip()
    return ""


def _year(s: str) -> str | None:
    """Extract a 4-digit year from LinkedIn's many date shapes ('Jan 2018', '2018', '2018-03')."""
    m = re.search(r"\b(19|20)\d{2}\b", s or "")
    return m.group(0) if m else None


def _truncate(s: str, limit: int = 160) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    if len(s) <= limit:
        return s
    return s[: limit - 1].rstrip() + "…"


# --- parsing ----------------------------------------------------------------


def parse_profile(root: Path) -> tuple[dict, list[str]]:
    """Returns (fields, notes). fields keys: city, website, headline, social_profiles."""
    notes: list[str] = []
    path = _find(root, PROFILE)
    if not path:
        return {}, ["Profile.csv not found — skipped name/location/headline import."]
    rows = _read_csv(path)
    if not rows:
        return {}, ["Profile.csv was empty."]
    row = rows[0]
    out: dict = {}

    geo = _col(row, "Geo Location", "Location")
    if geo:
        # "Austin, Texas, United States" -> city "Austin"
        out["city"] = geo.split(",")[0].strip()

    headline = _col(row, "Headline")
    if headline:
        out["headline"] = headline

    profiles: list[dict] = []
    websites = _col(row, "Websites")
    # LinkedIn packs websites as e.g. "[OTHER:https://a.com],[BLOG:https://b.com]"
    urls = re.findall(r"https?://[^\],\s]+", websites)
    if urls:
        out["website"] = urls[0]
        for u in urls[1:]:
            profiles.append({"network": "Website", "url": u})
    twitter = _col(row, "Twitter Handles", "Twitter Handle")
    if twitter:
        handle = twitter.lstrip("@").strip()
        profiles.append({"network": "Twitter", "url": f"https://twitter.com/{handle}"})
    if profiles:
        out["social_profiles"] = profiles
    return out, notes


def parse_positions(root: Path) -> tuple[list[dict], list[dict], list[str]]:
    """Returns (current_work, past_work, notes)."""
    path = _find(root, POSITIONS)
    if not path:
        return [], [], [
            "Positions.csv not found — work history NOT imported. "
            "It is Full-export-only; request a Full export for job chronology."
        ]
    current: list[dict] = []
    past: list[dict] = []
    for row in _read_csv(path):
        org = _col(row, "Company Name", "Company")
        role = _col(row, "Title", "Position Title")
        if not org and not role:
            continue
        started = _year(_col(row, "Started On", "Start Date"))
        finished_raw = _col(row, "Finished On", "End Date")
        desc = _truncate(_col(row, "Description"))
        if not finished_raw:  # still in the role
            entry: dict[str, object] = {"role": role, "org": org}
            current.append({k: v for k, v in entry.items() if v})
        else:
            entry = {"role": role, "org": org}
            if started:
                entry["start"] = int(started)
            end_year = _year(finished_raw)
            if end_year:
                entry["end"] = int(end_year)
            if desc:
                entry["summary"] = desc
            past.append({k: v for k, v in entry.items() if v not in (None, "")})
    return current, past, []


def parse_education(root: Path) -> tuple[list[dict], list[str]]:
    path = _find(root, EDUCATION)
    if not path:
        return [], [
            "Education.csv not found — education NOT imported (Full-export-only)."
        ]
    out: list[dict] = []
    for row in _read_csv(path):
        institution = _col(row, "School Name", "School")
        if not institution:
            continue
        entry: dict = {"institution": institution}
        degree = _col(row, "Degree Name", "Degree")
        if degree:
            entry["degree"] = degree
        area = _col(row, "Field Of Study", "Notes")
        if area and area != degree:
            entry["area"] = area
        start = _year(_col(row, "Start Date"))
        end = _year(_col(row, "End Date"))
        if start:
            entry["start"] = int(start)
        if end:
            entry["end"] = int(end)
        out.append(entry)
    return out, []


# --- merge ------------------------------------------------------------------


def _entry_key(e: dict, fields: tuple[str, ...]) -> tuple:
    return tuple(str(e.get(f, "")).strip().lower() for f in fields)


def merge_list(existing: list, incoming: list, base_key: tuple[str, ...]) -> tuple[list, int, int, list]:
    """Merge incoming entries into existing BY KEY.

    - Matched entry: update incoming's fields, preserve existing-only sub-fields
      (e.g. a hand-written `mission`).
    - Unmatched incoming: appended.
    - Unmatched existing (manual entries LinkedIn lacks): preserved as-is.

    The key is normally `base_key` (org+role), which lets the common case — a
    curated startless entry enriched by LinkedIn's dates — merge cleanly. But
    when `base_key` is AMBIGUOUS in the incoming set (the same org+role appears
    more than once: two distinct stints at the same company/title), the key
    ESCALATES to `base_key + (start,)` for that group, so the distinct stints stay
    distinct instead of collapsing into one row. Ambiguous groups are reported so
    the caller can warn.

    Returns (merged, n_updated, n_added, ambiguous_groups). Idempotent: a second
    run with the same incoming set produces an identical list (escalated entries
    re-match by start year).
    """
    from collections import Counter

    existing = list(existing or [])
    base_counts = Counter(_entry_key(e, base_key) for e in incoming)
    ambiguous = {k for k, c in base_counts.items() if c > 1}

    def keyfor(e: dict) -> tuple:
        bk = _entry_key(e, base_key)
        return bk + (str(e.get("start", "")),) if bk in ambiguous else bk

    by_key: dict[tuple, int] = {}
    for i, e in enumerate(existing):
        if isinstance(e, dict):
            by_key.setdefault(keyfor(e), i)
    updated = added = 0
    for inc in incoming:
        k = keyfor(inc)
        if k in by_key:
            target = existing[by_key[k]]
            for field, val in inc.items():
                target[field] = val  # incoming wins on shared fields; manual-only fields untouched
            updated += 1
        else:
            existing.append(inc)
            by_key[k] = len(existing) - 1
            added += 1
    return existing, updated, added, sorted(" / ".join(k) for k in ambiguous)


def apply_import(identity: dict, profile: dict, current: list, past: list,
                 education: list, force: bool) -> list[str]:
    """Mutate `identity` in place. Returns a list of human-readable change lines."""
    changes: list[str] = []

    # Scalars: gap-fill only (curated values preserved unless --force).
    for field in _SCALAR_GAPFILL:
        val = profile.get(field)
        if not val:
            continue
        cur = identity.get(field)
        if cur and not force:
            changes.append(f"  kept {field} (curated; --force to overwrite): {cur!r}")
        elif cur != val:
            identity[field] = val
            changes.append(f"  set {field} = {val!r}")

    # location.city (nested; never invents a location block without a timezone).
    if profile.get("city"):
        loc = identity.get("location")
        if isinstance(loc, dict):
            if not loc.get("city") or force:
                if loc.get("city") != profile["city"]:
                    loc["city"] = profile["city"]
                    changes.append(f"  set location.city = {profile['city']!r}")
        else:
            changes.append(
                f"  skipped location.city ({profile['city']!r}): no location block "
                "(needs a timezone first per SPEC §5.1)"
            )

    # social_profiles: add networks not already present (by network name).
    if profile.get("social_profiles"):
        sp = identity.setdefault("social_profiles", [])
        have = {str(p.get("network", "")).lower() for p in sp if isinstance(p, dict)}
        for prof in profile["social_profiles"]:
            if prof["network"].lower() not in have:
                sp.append(prof)
                have.add(prof["network"].lower())
                changes.append(f"  added social_profile: {prof['network']} -> {prof['url']}")

    # Lists: merge by key.
    def _merge(field: str, incoming: list, base_key: tuple[str, ...], label: str) -> None:
        merged, u, a, ambiguous = merge_list(identity.get(field, []), incoming, base_key)
        identity[field] = merged
        changes.append(f"  {field}[]: {u} updated, {a} added{label}")
        for group in ambiguous:
            changes.append(
                f"    ⚠ multiple stints for '{group}' — kept distinct by start year; review chronology"
            )

    if current:
        _merge("work", current, ("org", "role"), " (current roles)")
    if past:
        _merge("past_work", past, ("org", "role"), "")
    if education:
        _merge("education", education, ("institution", "degree"), "")

    return changes


# --- integrity --------------------------------------------------------------

def refresh_integrity(me_dir: Path) -> None:
    """Update ONLY identity.yaml's baseline hash; preserve every other file's line.

    The importer writes identity.yaml and nothing else, so it must re-baseline
    only identity.yaml. Rehashing the whole set would silently bless any
    pre-existing tamper drift on voice.md / preferences.yaml / working-style.yaml
    / voice.compact.md — the SessionStart integrity warning would stop firing for
    an unrelated file. Updating one line keeps every other file's drift evidence
    intact.
    """
    integrity = me_dir / ".integrity"
    if not integrity.exists():
        return  # producer hasn't opted into integrity; nothing to refresh
    identity = me_dir / "identity.yaml"
    if not identity.is_file():
        return
    new_hash = hashlib.sha256(identity.read_bytes()).hexdigest()
    out: list[str] = []
    replaced = False
    for line in integrity.read_text().splitlines(keepends=True):
        parts = line.split()
        if len(parts) == 2 and parts[1] == "identity.yaml":
            out.append(f"{new_hash}  identity.yaml\n")
            replaced = True
        else:
            out.append(line)  # untouched files (incl. any drift) preserved verbatim
    if not replaced:
        out.append(f"{new_hash}  identity.yaml\n")
    integrity.write_text("".join(out))


# --- main -------------------------------------------------------------------


def run(args: argparse.Namespace) -> int:
    src = Path(args.export).expanduser()
    if not src.exists():
        sys.stderr.write(f"error: export path not found: {src}\n")
        return 2

    me_dir = Path(
        args.identity or os.environ.get("DOT_ME_DIR", str(Path.home() / ".me"))
    ).expanduser()
    identity_path = me_dir if me_dir.suffix == ".yaml" else me_dir / "identity.yaml"
    me_dir = identity_path.parent
    if not identity_path.is_file():
        sys.stderr.write(f"error: identity.yaml not found at {identity_path}\n")
        return 2

    with tempfile.TemporaryDirectory() as td:
        if src.is_file() and zipfile.is_zipfile(src):
            with zipfile.ZipFile(src) as zf:
                zf.extractall(td)
            root = Path(td)
        elif src.is_dir():
            root = src
        else:
            sys.stderr.write(f"error: {src} is neither a zip nor a directory\n")
            return 2

        profile, n1 = parse_profile(root)
        current, past, n2 = parse_positions(root)
        education, n3 = parse_education(root)

    tier = "Full" if (current or past or education) else "Basic"
    notes = n1 + n2 + n3

    yaml = _yaml()
    with identity_path.open("r", encoding="utf-8") as fh:
        identity = yaml.load(fh)
    if identity is None:
        sys.stderr.write("error: identity.yaml is empty or unparseable\n")
        return 1

    changes = apply_import(identity, profile, current, past, education, args.force)

    sys.stderr.write(f"LinkedIn export tier detected: {tier}\n")
    for note in notes:
        sys.stderr.write(f"note: {note}\n")
    if changes:
        sys.stderr.write("changes:\n" + "\n".join(changes) + "\n")
    else:
        sys.stderr.write("no changes (nothing new to import).\n")

    if args.dry_run:
        sys.stderr.write("\n[dry-run] merged identity.yaml below; nothing written.\n")
        yaml.dump(identity, sys.stdout)
        return 0

    # Atomic write (write-then-rename per SPEC §7 update invariants).
    buf = io.StringIO()
    yaml.dump(identity, buf)
    tmp = identity_path.with_suffix(identity_path.suffix + ".tmp")
    tmp.write_text(buf.getvalue(), encoding="utf-8")
    tmp.replace(identity_path)

    if not args.no_integrity:
        refresh_integrity(me_dir)
        sys.stderr.write("refreshed .integrity baseline.\n")

    sys.stderr.write(f"wrote {identity_path}\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Import a LinkedIn export into ~/.me/identity.yaml")
    p.add_argument("export", help="path to the LinkedIn export .zip or its unzipped directory")
    p.add_argument("--identity", help="target identity.yaml (default: $DOT_ME_DIR/identity.yaml or ~/.me/identity.yaml)")
    p.add_argument("--dry-run", action="store_true", help="print merged result, write nothing")
    p.add_argument("--force", action="store_true", help="overwrite non-empty curated scalar fields")
    p.add_argument("--no-integrity", action="store_true", help="skip .integrity refresh")
    args = p.parse_args(argv)
    try:
        return run(args)
    except Exception as exc:  # noqa: BLE001 — top-level guard, surface cleanly
        sys.stderr.write(f"error: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
