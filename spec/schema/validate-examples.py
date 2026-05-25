#!/usr/bin/env python3
"""Validate every examples/*/identity.yaml and examples/*/preferences.yaml
against the published JSON Schemas.

Run from repo root:
    uv run --with jsonschema --with pyyaml python spec/schema/validate-examples.py

Exits non-zero on any validation failure. Used in CI per SPEC §5 acceptance
criteria: schemas MUST validate every shipped example cleanly.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from zoneinfo import available_timezones

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_DIR = REPO_ROOT / "spec" / "schema"
EXAMPLES_DIR = REPO_ROOT / "examples"

PAIRS = [
    ("identity.yaml", SCHEMA_DIR / "identity.schema.json"),
    ("preferences.yaml", SCHEMA_DIR / "preferences.schema.json"),
]

# SPEC §5.1: location.timezone, when present, MUST be a valid IANA identifier.
# This is the only strict invariant in the identity layer beyond the required
# `name`. JSON Schema's `format: iana-time-zone` is annotation-only in most
# validators (python-jsonschema does not enforce `format` without an explicit
# FormatChecker), so the bundled validator does the executable check here.
_IANA_TIMEZONES = available_timezones()


def load_validator(schema_path: Path) -> Draft202012Validator:
    schema = json.loads(schema_path.read_text())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def check_identity_timezone(data: dict) -> list[str]:
    """SPEC §5.1 MUST: location.timezone must be a real IANA zone."""
    location = data.get("location") if isinstance(data, dict) else None
    if not isinstance(location, dict):
        return []
    tz = location.get("timezone")
    if tz is None:
        return []
    if not isinstance(tz, str):
        return [f"location/timezone :: expected string, got {type(tz).__name__}"]
    if tz not in _IANA_TIMEZONES:
        return [f"location/timezone :: '{tz}' is not a recognised IANA timezone (zoneinfo.available_timezones)"]
    return []


def main() -> int:
    validators = {name: load_validator(path) for name, path in PAIRS}
    failures: list[str] = []
    checked = 0

    example_dirs = sorted(d for d in EXAMPLES_DIR.iterdir() if d.is_dir())
    if not example_dirs:
        print(f"ERROR: no example directories under {EXAMPLES_DIR}", file=sys.stderr)
        return 2

    for example_dir in example_dirs:
        for filename, validator in validators.items():
            target = example_dir / filename
            if not target.exists():
                continue
            checked += 1
            data = yaml.safe_load(target.read_text())
            if data is None:
                data = {}
            errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
            file_failed = False
            if errors:
                file_failed = True
                for err in errors:
                    path = "/".join(str(p) for p in err.absolute_path) or "(root)"
                    failures.append(f"{target.relative_to(REPO_ROOT)} :: {path} :: {err.message}")
            if filename == "identity.yaml":
                for msg in check_identity_timezone(data):
                    file_failed = True
                    failures.append(f"{target.relative_to(REPO_ROOT)} :: {msg}")
            if not file_failed:
                print(f"ok   {target.relative_to(REPO_ROOT)}")

    if failures:
        print(f"\n{len(failures)} validation error(s) across {checked} file(s):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print(f"\nall {checked} example file(s) validate cleanly against the schemas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
