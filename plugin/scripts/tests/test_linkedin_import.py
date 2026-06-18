"""Tests for plugin/scripts/linkedin-import.py.

Run from repo root:
    uv run --with ruamel.yaml --with pytest pytest plugin/scripts/tests/ -v

The module filename is hyphenated, so it's loaded via importlib (per the
hyphenated-script convention). Fixtures under tests/fixtures/ stand in for a
real LinkedIn export, which is unavailable in CI and 24h-gated to obtain.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from ruamel.yaml import YAML

SCRIPTS = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load_module():
    spec = importlib.util.spec_from_file_location("linkedin_import", SCRIPTS / "linkedin-import.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


li = _load_module()


# --- parsing ----------------------------------------------------------------


def test_parse_profile_maps_to_existing_fields():
    fields, notes = li.parse_profile(FIXTURES / "full-export")
    assert fields["city"] == "Portland"          # parsed from "Portland, Oregon, United States"
    assert fields["headline"] == "Engineer & Writer"
    assert fields["website"] == "https://samrivera.example.com"
    assert any(p["network"] == "Twitter" and "samplehandle" in p["url"] for p in fields["social_profiles"])
    assert notes == []


def test_parse_positions_splits_current_and_past():
    current, past, notes = li.parse_positions(FIXTURES / "full-export")
    assert [c["org"] for c in current] == ["Globex"]      # Finished On empty -> current
    assert current[0]["role"] == "Principal Engineer"
    orgs = {p["org"] for p in past}
    assert orgs == {"Initech", "Hooli"}
    initech = next(p for p in past if p["org"] == "Initech")
    assert initech["start"] == 2018 and initech["end"] == 2022
    assert isinstance(initech["start"], int)
    assert initech["summary"].startswith("Built internal tooling")


def test_parse_education():
    edu, notes = li.parse_education(FIXTURES / "full-export")
    assert edu == [{"institution": "Reed College", "degree": "BA",
                    "area": "Computer Science", "start": 2011, "end": 2015}]


def test_basic_export_reports_missing_full_only_files():
    current, past, notes = li.parse_positions(FIXTURES / "basic-export")
    assert current == [] and past == []
    assert any("Full-export-only" in n for n in notes)
    edu, edu_notes = li.parse_education(FIXTURES / "basic-export")
    assert edu == [] and any("Full-export-only" in n for n in edu_notes)


# --- merge semantics --------------------------------------------------------


def test_merge_preserves_manual_fields_and_is_idempotent():
    existing = [{"role": "Senior Engineer", "org": "Initech", "mission": "kept by hand"}]
    incoming = [{"role": "Senior Engineer", "org": "Initech", "start": 2018, "end": 2022,
                 "summary": "from linkedin"}]
    merged, updated, added, ambiguous = li.merge_list(existing, incoming, ("org", "role"))
    assert updated == 1 and added == 0 and ambiguous == []
    assert len(merged) == 1
    entry = merged[0]
    assert entry["mission"] == "kept by hand"     # manual-only field survives
    assert entry["start"] == 2018 and entry["summary"] == "from linkedin"
    # second run with same incoming must not grow or change the result
    merged2, u2, a2, _ = li.merge_list(merged, incoming, ("org", "role"))
    assert a2 == 0 and len(merged2) == 1


def test_gapfill_keeps_curated_scalar_without_force():
    identity = {"headline": "Curated Headline"}
    changes = li.apply_import(identity, {"headline": "LinkedIn Headline"}, [], [], [], force=False)
    assert identity["headline"] == "Curated Headline"     # not clobbered
    assert any("kept headline" in c for c in changes)


def test_gapfill_overwrites_with_force():
    identity = {"headline": "Curated Headline"}
    li.apply_import(identity, {"headline": "LinkedIn Headline"}, [], [], [], force=True)
    assert identity["headline"] == "LinkedIn Headline"


def test_city_skipped_when_no_location_block():
    identity = {}
    changes = li.apply_import(identity, {"city": "Portland"}, [], [], [], force=False)
    assert "location" not in identity
    assert any("skipped location.city" in c for c in changes)


# --- end-to-end -------------------------------------------------------------


def _write_identity(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "identity.yaml"
    p.write_text(body)
    return p


def test_end_to_end_full_import_and_idempotency(tmp_path):
    identity_path = _write_identity(tmp_path, (
        "name: Sam Rivera\n"
        'headline: "Curated"\n'
        'spec_version: "0.5"\n'
        "location:\n"
        "  timezone: America/Los_Angeles\n"
        "work:\n"
        "  - role: Principal Engineer\n"
        "    org: Globex\n"
        "past_work:\n"
        "  - role: Senior Engineer\n"
        "    org: Initech\n"
        "    mission: handcrafted\n"
    ))
    args = li.argparse.Namespace(export=str(FIXTURES / "full-export"), identity=str(identity_path),
                                 dry_run=False, force=False, no_integrity=True)
    assert li.run(args) == 0

    yaml = YAML()
    d = yaml.load(identity_path.read_text())
    assert d["headline"] == "Curated"                              # gap-fill respected curation
    assert d["location"]["city"] == "Portland"
    initech = next(e for e in d["past_work"] if e["org"] == "Initech")
    assert initech["mission"] == "handcrafted"                     # manual field survived
    assert initech["end"] == 2022
    assert any(e["org"] == "Hooli" for e in d["past_work"])        # new past role added
    assert d["education"][0]["institution"] == "Reed College"
    counts = (len(d["work"]), len(d["past_work"]), len(d["education"]))

    # idempotency: a second run produces identical counts (no append-grow)
    assert li.run(args) == 0
    d2 = yaml.load(identity_path.read_text())
    assert (len(d2["work"]), len(d2["past_work"]), len(d2["education"])) == counts


def test_dry_run_writes_nothing(tmp_path, capsys):
    body = (
        "name: Sam Rivera\n"
        'spec_version: "0.5"\n'
        "location:\n"
        "  timezone: America/Los_Angeles\n"
    )
    identity_path = _write_identity(tmp_path, body)
    args = li.argparse.Namespace(export=str(FIXTURES / "full-export"), identity=str(identity_path),
                                 dry_run=True, force=False, no_integrity=True)
    assert li.run(args) == 0
    assert identity_path.read_text() == body          # unchanged on disk
    out = capsys.readouterr().out
    assert "education" in out and "Reed College" in out   # merged result printed to stdout


# --- regression: Codex adversarial review (JM-254) --------------------------


def test_duplicate_org_role_stints_kept_distinct():
    """Two distinct tenures at the same company+title must NOT collapse into one."""
    incoming = [
        {"role": "Engineer", "org": "Hooli", "start": 2010, "end": 2012, "summary": "first stint"},
        {"role": "Engineer", "org": "Hooli", "start": 2015, "end": 2018, "summary": "second stint"},
    ]
    merged, updated, added, ambiguous = li.merge_list([], incoming, ("org", "role"))
    assert len(merged) == 2 and added == 2        # not collapsed
    assert ambiguous                              # flagged for the user
    assert sorted(e["start"] for e in merged) == [2010, 2015]
    # idempotent: re-running the same ambiguous set does not grow the list
    merged2, _, a2, _ = li.merge_list(merged, incoming, ("org", "role"))
    assert a2 == 0 and len(merged2) == 2


def test_integrity_refresh_preserves_other_files_drift(tmp_path):
    """Refreshing after an identity-only write must NOT bless drift on other files."""
    import hashlib
    (tmp_path / "identity.yaml").write_text("name: X\n")
    drifted = "0" * 64  # stand-in for a tampered voice.md whose baseline must stay
    (tmp_path / ".integrity").write_text(
        f"{drifted}  voice.md\n"
        f"{'1' * 64}  identity.yaml\n"
    )
    li.refresh_integrity(tmp_path)
    by_file = {ln.split()[1]: ln.split()[0] for ln in (tmp_path / ".integrity").read_text().splitlines()}
    assert by_file["voice.md"] == drifted         # drift evidence preserved -> warning still fires
    assert by_file["identity.yaml"] == hashlib.sha256((tmp_path / "identity.yaml").read_bytes()).hexdigest()
