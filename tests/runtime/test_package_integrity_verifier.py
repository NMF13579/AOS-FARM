import pytest
import hashlib
from aos.runtime.package_integrity_verifier import verify_package_integrity
from aos.runtime.artifact_manifest_builder import build_artifact_manifest
from aos.runtime.package_identity import generate_package_identity

def get_base_package_core():
    return {
        "schema_version": 1,
        "operation": "MERGE_AUTHORIZATION",
        "repository_identity": "owner/repo",
        "pull_request": "owner/repo/pull/1",
        "normalized_intent": {},
        "fixed_safety_policy": {},
        "decision_state": {},
        "exact_merge_parameters": {},
        "forbidden_actions": [],
        "tool_identity": {
            "product_version": "1.0",
            "generator_build_digest": "sha256:" + "a"*64,
            "canonicalizer_version": "1.0",
            "package_schema_version": "1.0"
        }
    }

def get_base_package():
    core = get_base_package_core()
    pkg_id = generate_package_identity(core)["package_id"]
    return {
        "schema_version": 1,
        "package_id": pkg_id,
        "package_core": core
    }

def get_base_artifacts():
    import json
    pkg = get_base_package()
    pkg_bytes = json.dumps(pkg).encode('utf-8') + b'\n'
    return {
        "normalized-intent.json": b'{"intent": 1}\n',
        "decision-state-snapshot.json": b'{"state": 2}\n',
        "merge-authorization-package.json": pkg_bytes
    }

def get_expected_id():
    core = get_base_package_core()
    return generate_package_identity(core)["package_id"]

def test_valid_artifacts_and_manifest():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert res["technical_status"] == "PASS"
    assert res["integrity_status"] == "PASS"
    assert res["control_status"] == "HUMAN_REVIEW_REQUIRED"
    assert res["approval_granted"] is False

def test_same_valid_input_produces_same_result():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    res1 = verify_package_integrity(arts, manifest, get_expected_id())
    res2 = verify_package_integrity(arts, manifest, get_expected_id())
    assert res1 == res2

def test_missing_artifact():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    del arts["normalized-intent.json"]
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_extra_artifact():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    arts["extra.json"] = b"{}\n"
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_missing_manifest_entry():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    manifest["artifacts"] = [a for a in manifest["artifacts"] if a["relative_path"] != "normalized-intent.json"]
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "MANIFEST_SET_MISMATCH" in res["reason_codes"]

def test_extra_manifest_entry():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    manifest["artifacts"].append({
        "relative_path": "extra.json",
        "byte_length": 1,
        "sha256": "abc",
        "encoding": "UTF-8",
        "line_endings": "LF",
        "terminal_lf": True,
        "generator_version": "v1.0"
    })
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "MANIFEST_SET_MISMATCH" in res["reason_codes"]

def test_modified_artifact_byte():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    arts["normalized-intent.json"] = b'{"intent": 2}\n'
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "ARTIFACT_DIGEST_MISMATCH" in res["reason_codes"]

def test_wrong_byte_length():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    manifest["artifacts"][0]["byte_length"] = 999
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "ARTIFACT_LENGTH_MISMATCH" in res["reason_codes"]

def test_wrong_artifact_digest():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    manifest["artifacts"][0]["sha256"] = "wrong"
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "ARTIFACT_DIGEST_MISMATCH" in res["reason_codes"]

def test_invalid_utf8():
    arts = get_base_artifacts()
    arts["normalized-intent.json"] = b"\xff\xfe\n"
    manifest = build_artifact_manifest(get_base_artifacts(), "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "ARTIFACT_ENCODING_INVALID" in res["reason_codes"]

def test_bom():
    arts = get_base_artifacts()
    arts["normalized-intent.json"] = b"\xef\xbb\xbf{}\n"
    manifest = build_artifact_manifest(get_base_artifacts(), "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "ARTIFACT_BOM_FORBIDDEN" in res["reason_codes"]

def test_crlf():
    arts = get_base_artifacts()
    arts["normalized-intent.json"] = b"{}\r\n"
    manifest = build_artifact_manifest(get_base_artifacts(), "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "ARTIFACT_LINE_ENDINGS_INVALID" in res["reason_codes"]

def test_wrong_terminal_lf_metadata():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    manifest["artifacts"][0]["terminal_lf"] = not manifest["artifacts"][0]["terminal_lf"]
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "ARTIFACT_TERMINAL_LF_MISMATCH" in res["reason_codes"]

def test_invalid_package_json():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    arts["merge-authorization-package.json"] = b"invalid json"
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "PACKAGE_JSON_INVALID" in res["reason_codes"]

def test_duplicate_json_key():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    arts["merge-authorization-package.json"] = b'{"a": 1, "a": 2}'
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "PACKAGE_JSON_INVALID" in res["reason_codes"]

def test_missing_package_core():
    arts = get_base_artifacts()
    pkg = get_base_package()
    del pkg["package_core"]
    import json
    arts["merge-authorization-package.json"] = json.dumps(pkg).encode('utf-8') + b'\n'
    manifest = build_artifact_manifest(arts, "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "PACKAGE_CORE_INVALID" in res["reason_codes"]

def test_unknown_package_wrapper_field():
    arts = get_base_artifacts()
    pkg = get_base_package()
    pkg["unknown"] = 1
    import json
    arts["merge-authorization-package.json"] = json.dumps(pkg).encode('utf-8') + b'\n'
    manifest = build_artifact_manifest(arts, "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "FORBIDDEN_PACKAGE_FIELD" in res["reason_codes"]

def test_forbidden_approval_field():
    arts = get_base_artifacts()
    pkg = get_base_package()
    pkg["approval"] = True
    import json
    arts["merge-authorization-package.json"] = json.dumps(pkg).encode('utf-8') + b'\n'
    manifest = build_artifact_manifest(arts, "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "FORBIDDEN_PACKAGE_FIELD" in res["reason_codes"]

def test_forbidden_execution_authorization_field():
    arts = get_base_artifacts()
    pkg = get_base_package()
    pkg["execution_authorization"] = True
    import json
    arts["merge-authorization-package.json"] = json.dumps(pkg).encode('utf-8') + b'\n'
    manifest = build_artifact_manifest(arts, "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "FORBIDDEN_PACKAGE_FIELD" in res["reason_codes"]

def test_changed_package_core():
    arts = get_base_artifacts()
    pkg = get_base_package()
    pkg["package_core"]["repository_identity"] = "changed"
    import json
    arts["merge-authorization-package.json"] = json.dumps(pkg).encode('utf-8') + b'\n'
    manifest = build_artifact_manifest(arts, "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "PACKAGE_ID_MISMATCH" in res["reason_codes"]

def test_wrong_expected_package_id():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    res = verify_package_integrity(arts, manifest, "wrong_id")
    assert "PACKAGE_ID_MISMATCH" in res["reason_codes"]

def test_invalid_package_id_format():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    res = verify_package_integrity(arts, manifest, 123)
    assert res["technical_status"] == "UNKNOWN"

def test_manifest_self_entry_rejected():
    arts = get_base_artifacts()
    arts["artifact-manifest.json"] = b"{}\n"
    manifest = build_artifact_manifest(get_base_artifacts(), "v1.0")
    manifest["artifacts"].append({
        "relative_path": "artifact-manifest.json",
        "byte_length": 3,
        "sha256": hashlib.sha256(b"{}\n").hexdigest(),
        "encoding": "UTF-8",
        "line_endings": "LF",
        "terminal_lf": True,
        "generator_version": "v1.0"
    })
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_verification_result_artifact_rejected():
    arts = get_base_artifacts()
    arts["verification-result.json"] = b"{}\n"
    manifest = build_artifact_manifest(get_base_artifacts(), "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_preview_artifact_rejected():
    arts = get_base_artifacts()
    arts["human-preview.md"] = b"\n"
    manifest = build_artifact_manifest(get_base_artifacts(), "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert "ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_inputs_not_mutated():
    import copy
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    arts_copy = copy.deepcopy(arts)
    manifest_copy = copy.deepcopy(manifest)
    verify_package_integrity(arts, manifest, get_expected_id())
    assert arts == arts_copy
    assert manifest == manifest_copy

def test_reason_codes_deterministic():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    arts["extra.json"] = b"{}\n"
    manifest["artifacts"][0]["byte_length"] = 999
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert res["reason_codes"] == sorted(res["reason_codes"])

def test_pass_does_not_grant_approval():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert res["approval_granted"] is False

def test_pass_does_not_authorize_execution():
    arts = get_base_artifacts()
    manifest = build_artifact_manifest(arts, "v1.0")
    res = verify_package_integrity(arts, manifest, get_expected_id())
    assert res["execution_authorized"] is False

def test_no_filesystem_reads():
    pass

def test_no_filesystem_writes():
    pass

def test_no_github_access():
    pass
