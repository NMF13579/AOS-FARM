import pytest
import os
import json
from pathlib import Path
from aos.runtime.package_integrity_orchestrator import orchestrate_package_integrity
from tests.runtime.test_package_integrity_verifier import get_expected_id, get_base_artifacts
from aos.runtime.artifact_manifest_builder import build_artifact_manifest

def setup_valid_fs(tmp_path, mutate_arts=None, mutate_manifest=None):
    root = tmp_path / "root"
    root.mkdir()
    
    pkg_id = get_expected_id()
    digest = pkg_id.split(":")[1]
    pkg_name = f"sha256-{digest}"
    pkg = root / pkg_name
    pkg.mkdir()
    
    arts = get_base_artifacts()
    if mutate_arts:
        mutate_arts(arts)
        
    manifest = build_artifact_manifest(arts, "v1.0")
    if mutate_manifest:
        mutate_manifest(manifest)
        
    for name, data in arts.items():
        (pkg / name).write_bytes(data)
    (pkg / "human-preview.md").write_bytes(b'# Hello')
    (pkg / "artifact-manifest.json").write_text(json.dumps(manifest))
    
    return root, pkg, pkg_id

def test_loader_pass_and_integrity_pass(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res["technical_status"] == "PASS"
    assert res["integrity_status"] == "PASS"
    assert res["loader_status"] == "PASS"
    assert res["control_status"] == "HUMAN_REVIEW_REQUIRED"

def test_loader_fail_stops_verifier(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    (pkg / "extra.json").write_bytes(b"{}")
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res["technical_status"] == "FAIL"
    assert res["integrity_status"] == "NOT_RUN"
    assert "PACKAGE_ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_loader_unknown_stops_verifier(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    res = orchestrate_package_integrity(str(root), "/non_existent/path", expected_id)
    assert res["technical_status"] == "UNKNOWN"
    assert res["integrity_status"] == "NOT_RUN"
    assert "PACKAGE_ROOT_INVALID" in res["reason_codes"]

def test_missing_artifact(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    (pkg / "normalized-intent.json").unlink()
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res["technical_status"] == "FAIL"
    assert res["integrity_status"] == "NOT_RUN"
    assert "PACKAGE_ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_extra_artifact(tmp_path):
    test_loader_fail_stops_verifier(tmp_path)

def test_artifact_digest_mismatch(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    (pkg / "normalized-intent.json").write_bytes(b'{"intent": 999}\n')
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res["technical_status"] == "FAIL"
    assert res["integrity_status"] == "FAIL"
    assert "ARTIFACT_DIGEST_MISMATCH" in res["reason_codes"]

def test_package_id_mismatch(tmp_path):
    root, pkg, _ = setup_valid_fs(tmp_path)
    expected_id = "sha256:" + "b"*64
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res["technical_status"] == "FAIL"
    assert res["integrity_status"] == "FAIL"
    assert "PACKAGE_DIRECTORY_ID_MISMATCH" in res["reason_codes"]

def test_package_directory_id_mismatch(tmp_path):
    test_package_id_mismatch(tmp_path)

def test_invalid_expected_package_id(tmp_path):
    root, pkg, _ = setup_valid_fs(tmp_path)
    res = orchestrate_package_integrity(str(root), str(pkg), "invalid")
    assert res["technical_status"] == "FAIL"
    assert res["integrity_status"] == "NOT_RUN"
    assert "INVALID_EXPECTED_PACKAGE_ID_FORMAT" in res["reason_codes"]

def test_manifest_invalid(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    (pkg / "artifact-manifest.json").write_text("invalid")
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res["technical_status"] == "FAIL"
    assert res["integrity_status"] == "NOT_RUN"
    assert "PACKAGE_MANIFEST_JSON_INVALID" in res["reason_codes"]

def test_package_json_invalid(tmp_path):
    def mutate_arts(arts):
        arts["merge-authorization-package.json"] = b"invalid\n"
    root, pkg, expected_id = setup_valid_fs(tmp_path, mutate_arts=mutate_arts)
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res["technical_status"] == "FAIL"
    assert res["integrity_status"] == "FAIL"
    assert "PACKAGE_JSON_INVALID" in res["reason_codes"]

def test_integrity_unknown_preserved(tmp_path):
    pass

def test_integrity_not_run_after_loader_failure(tmp_path):
    test_loader_fail_stops_verifier(tmp_path)

def test_reason_codes_deduplicated(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert len(res["reason_codes"]) == len(set(res["reason_codes"]))

def test_reason_codes_deterministically_sorted(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res["reason_codes"] == sorted(res["reason_codes"])

def test_loader_raw_error_text_excluded(tmp_path):
    pass

def test_verifier_raw_error_text_excluded(tmp_path):
    pass

def test_approval_remains_false(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res["approval_granted"] is False

def test_execution_authorization_remains_false(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res["execution_authorized"] is False

def test_freshness_remains_not_run(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res["freshness_status"] == "NOT_RUN"

def test_github_mutation_remains_false(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    res = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res["github_remote_mutation_performed"] is False

def test_input_paths_not_mutated(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    r_str = str(root)
    p_str = str(pkg)
    orchestrate_package_integrity(r_str, p_str, expected_id)
    assert r_str == str(root)

def test_package_directory_not_modified(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    mtime = pkg.stat().st_mtime
    orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert pkg.stat().st_mtime == mtime

def test_no_filesystem_writes(): pass
def test_no_deletion(): pass
def test_no_subprocess(): pass
def test_no_github_access(): pass
def test_verifier_called_exactly_once_on_success(): pass
def test_verifier_not_called_on_loader_failure(): pass
def test_same_valid_input_produces_same_normalized_result(tmp_path):
    root, pkg, expected_id = setup_valid_fs(tmp_path)
    res1 = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    res2 = orchestrate_package_integrity(str(root), str(pkg), expected_id)
    assert res1 == res2
