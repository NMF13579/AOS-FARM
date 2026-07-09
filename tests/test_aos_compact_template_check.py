import json
import subprocess
import pytest
from pathlib import Path

SCRIPT_PATH = "aos/scripts/aos_compact_template_check.py"

def test_help_exits_0():
    result = subprocess.run(["python3", SCRIPT_PATH, "--help"], capture_output=True)
    assert result.returncode == 0

def test_json_shape_and_safety_flags():
    result = subprocess.run(["python3", SCRIPT_PATH, "--json", "--target", "tests/fixtures/compact_template_check/valid_compact_template.md"], capture_output=True, text=True)
    assert result.returncode == 0
    data = json.loads(result.stdout)

    # Required top-level keys
    required_keys = [
        "final_status", "target_path", "checks", "failures", "warnings",
        "blocked_reasons", "unknown_reasons", "advisory_only", "approval_granted",
        "execution_authorized", "commit_authorized", "push_authorized",
        "merge_authorized", "release_authorized"
    ]
    for key in required_keys:
        assert key in data

    # Safety flags must be explicitly false
    assert data["advisory_only"] is True
    assert data["approval_granted"] is False
    assert data["execution_authorized"] is False
    assert data["commit_authorized"] is False
    assert data["push_authorized"] is False
    assert data["merge_authorized"] is False
    assert data["release_authorized"] is False

    # Every check must have required fields
    for check in data["checks"]:
        assert "name" in check
        assert "status" in check
        assert "severity" in check
        assert "message" in check
        assert "evidence" in check

def test_valid_fixture_returns_pass():
    result = subprocess.run(["python3", SCRIPT_PATH, "--json", "--target", "tests/fixtures/compact_template_check/valid_compact_template.md"], capture_output=True, text=True)
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["final_status"] == "PASS"

def test_missing_required_section_returns_fail():
    result = subprocess.run(["python3", SCRIPT_PATH, "--json", "--target", "tests/fixtures/compact_template_check/missing_sections.md"], capture_output=True, text=True)
    assert result.returncode != 0
    data = json.loads(result.stdout)
    assert data["final_status"] == "FAIL"

def test_explicit_approval_wording_returns_blocked():
    result = subprocess.run(["python3", SCRIPT_PATH, "--json", "--target", "tests/fixtures/compact_template_check/explicit_approval.md"], capture_output=True, text=True)
    assert result.returncode != 0
    data = json.loads(result.stdout)
    assert data["final_status"] == "BLOCKED"

def test_boundary_and_source_of_truth_violations():
    result = subprocess.run(["python3", SCRIPT_PATH, "--json", "--target", "tests/fixtures/compact_template_check/boundary_and_source_of_truth_violations.md"], capture_output=True, text=True)
    assert result.returncode != 0
    data = json.loads(result.stdout)
    assert data["final_status"] == "BLOCKED"

    # Assert both reasons separately
    has_commit_push_blocked = any(c["name"] == "Same-Block Commit+Push" and c["status"] == "BLOCKED" for c in data["checks"])
    has_sot_blocked = any(c["name"] == "Source of Truth Claim" and c["status"] == "BLOCKED" for c in data["checks"])

    assert has_commit_push_blocked, "Same-block commit+push violation not detected"
    assert has_sot_blocked, "Source of Truth authority claim not detected"

def test_traversal_target_rejected(tmp_path):
    result = subprocess.run(["python3", SCRIPT_PATH, "--json", "--target", "../outside.md"], capture_output=True, text=True)
    assert result.returncode != 0
    data = json.loads(result.stdout)
    assert data["final_status"] == "BLOCKED"
    assert "outside repository root" in data["failures"][0]

def test_absolute_path_outside_repo_rejected(tmp_path):
    outside_file = tmp_path / "outside.md"
    outside_file.write_text("dummy content")
    result = subprocess.run(["python3", SCRIPT_PATH, "--json", "--target", str(outside_file)], capture_output=True, text=True)
    assert result.returncode != 0
    data = json.loads(result.stdout)
    assert data["final_status"] == "BLOCKED"
    assert "outside repository root" in data["failures"][0]

def setup_fake_repo(tmp_path):
    (tmp_path / "00_AOS_Core_Control.md").touch()
    (tmp_path / "01_AOS_Assembly_Pipelines_and_Build_Roadmap.md").touch()
    (tmp_path / "02_AOS_Governance_Control_Module_and_Safety_Rules.md").touch()
    (tmp_path / "aos").mkdir()
    return tmp_path

def test_ambiguous_forbidden_wording_human_review_required(tmp_path):
    setup_fake_repo(tmp_path)
    valid_content = Path("tests/fixtures/compact_template_check/valid_compact_template.md").read_text()
    ambiguous_file = tmp_path / "ambiguous.md"
    # "no human review needed" is forbidden but not in the explicitly BLOCKED list (like "READY_FOR_EXECUTION")
    ambiguous_file.write_text(valid_content + "\nno human review needed\n")

    script_abs = Path(SCRIPT_PATH).resolve()
    result = subprocess.run(["python3", str(script_abs), "--json", "--target", str(ambiguous_file)], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode != 0
    data = json.loads(result.stdout)
    assert data["final_status"] == "HUMAN_REVIEW_REQUIRED"
    assert any(c["status"] == "HUMAN_REVIEW_REQUIRED" and "no human review needed" in c["name"] for c in data["checks"])

def test_unsafe_findings_not_downgraded_under_pass(tmp_path):
    setup_fake_repo(tmp_path)
    valid_content = Path("tests/fixtures/compact_template_check/valid_compact_template.md").read_text()
    mixed_file = tmp_path / "mixed.md"
    mixed_file.write_text(valid_content + "\nREADY_FOR_EXECUTION\n")

    script_abs = Path(SCRIPT_PATH).resolve()
    result = subprocess.run(["python3", str(script_abs), "--json", "--target", str(mixed_file)], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode != 0
    data = json.loads(result.stdout)

    # Must be BLOCKED, not PASS with a warning
    assert data["final_status"] == "BLOCKED"
    assert "READY_FOR_EXECUTION" in str(data["blocked_reasons"])
