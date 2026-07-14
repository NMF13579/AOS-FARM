import os
import pytest
import json
import uuid
import hashlib
from unittest.mock import patch
from pathlib import Path

from aos.runtime.package_publisher import atomic_publish_package
from aos.runtime.package_identity import generate_package_identity

def _valid_package():
    pkg_core = {"schema_version": 1}
    identity = generate_package_identity(pkg_core)
    pkg_id = identity["package_id"]

    b = {
        "normalized-intent.json": b'{"a":1}',
        "decision-state-snapshot.json": b'{"b":2}',
        "merge-authorization-package.json": json.dumps({
            "schema_version": 1,
            "package_id": pkg_id,
            "package_core": pkg_core
        }, separators=(',', ':')).encode('utf-8'),
        "human-preview.md": b'# Hello'
    }

    manifest = {
        "schema_version": 1,
        "type": "merge_authorization_manifest",
        "artifacts": []
    }
    for k, v in b.items():
        if k == "human-preview.md":
            continue
        manifest["artifacts"].append({
            "relative_path": k,
            "byte_length": len(v),
            "sha256": hashlib.sha256(v).hexdigest(),
            "terminal_lf": v.endswith(b"\n")
        })

    return pkg_id, b, manifest

def test_valid_atomic_publish(tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    pkg_id, b, manifest = _valid_package()
    res = atomic_publish_package(str(root), pkg_id, b, manifest)

    assert res["technical_status"] == "PASS", res
    assert res["integrity_status"] == "PASS"
    assert res["published"] is True
    digest = pkg_id.split(":")[1]
    assert res["package_directory"] == f"sha256-{digest}"

    final_dir = root / res["package_directory"]
    assert final_dir.is_dir()
    assert (final_dir / "normalized-intent.json").read_bytes() == b["normalized-intent.json"]

def test_existing_final_directory_blocks(tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    pkg_id, b, manifest = _valid_package()
    digest = pkg_id.split(":")[1]
    final_dir = root / f"sha256-{digest}"
    final_dir.mkdir()

    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["technical_status"] == "FAIL"
    assert "PACKAGE_ALREADY_EXISTS" in res["reason_codes"]
    assert res["published"] is False

def test_modified_preview_does_not_affect_integrity(tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    pkg_id, b, manifest = _valid_package()
    b["human-preview.md"] = b"# Modified"
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["technical_status"] == "PASS"
    assert res["integrity_status"] == "PASS"

def test_modified_integrity_bound_artifact_fails_integrity(tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    pkg_id, b, manifest = _valid_package()
    b["normalized-intent.json"] = b'{"a": 2}' # Modified
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["technical_status"] == "FAIL"
    assert "PACKAGE_STAGING_INTEGRITY_FAILED" in res["reason_codes"]

def test_package_root_symlink_rejected(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    sym_root = tmp_path / "sym_root"
    os.symlink(root, sym_root)

    pkg_id, b, manifest = _valid_package()
    res = atomic_publish_package(str(sym_root), pkg_id, b, manifest)
    assert res["technical_status"] == "FAIL"
    assert "PACKAGE_ROOT_SYMLINK_FORBIDDEN" in res["reason_codes"]

def test_invalid_package_id_rejected(tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    _, b, manifest = _valid_package()
    res = atomic_publish_package(str(root), "sha256:invalid", b, manifest)
    assert res["technical_status"] == "FAIL"
    assert "PACKAGE_ID_INVALID" in res["reason_codes"]

def test_missing_artifact_rejected(tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    pkg_id, b, manifest = _valid_package()
    del b["human-preview.md"]
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["technical_status"] == "FAIL"
    assert "PACKAGE_ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_extra_artifact_rejected(tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    pkg_id, b, manifest = _valid_package()
    b["extra.json"] = b'{}'
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["technical_status"] == "FAIL"
    assert "PACKAGE_ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_nested_artifact_path_rejected(tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    pkg_id, b, manifest = _valid_package()
    b["nested/human-preview.md"] = b.pop("human-preview.md")
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["technical_status"] == "FAIL"
    assert "PACKAGE_ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_integrity_failure_blocks_rename(tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    pkg_id, b, manifest = _valid_package()
    manifest["artifacts"][0]["sha256"] = "bad"
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["technical_status"] == "FAIL"
    assert "PACKAGE_STAGING_INTEGRITY_FAILED" in res["reason_codes"]

    digest = pkg_id.split(":")[1]
    final_dir = root / f"sha256-{digest}"
    assert not final_dir.exists()

    assert list(root.iterdir()) == []

@patch("os.rename")
def test_rename_failure(mock_rename, tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    mock_rename.side_effect = OSError("fake error")

    pkg_id, b, manifest = _valid_package()
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["technical_status"] == "FAIL"
    assert "PACKAGE_ATOMIC_RENAME_FAILED" in res["reason_codes"]

    assert list(root.iterdir()) == []

@patch("os.rename")
def test_cross_filesystem_simulation_blocked(mock_rename, tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    err = OSError("cross device")
    err.errno = 18
    mock_rename.side_effect = err

    pkg_id, b, manifest = _valid_package()
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["technical_status"] == "FAIL"
    assert "PACKAGE_ATOMIC_RENAME_FAILED" in res["reason_codes"]

def test_no_github_access(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    pkg_id, b, manifest = _valid_package()
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["github_remote_mutation_performed"] is False

def test_approval_remains_false(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    pkg_id, b, manifest = _valid_package()
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["approval_granted"] is False

def test_execution_authorization_remains_false(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    pkg_id, b, manifest = _valid_package()
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["execution_authorized"] is False

def test_freshness_remains_not_run(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    pkg_id, b, manifest = _valid_package()
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["freshness_status"] == "NOT_RUN"

@patch("pathlib.Path.unlink")
def test_cleanup_failure_reported(mock_unlink, tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    mock_unlink.side_effect = Exception("unlink failed")

    pkg_id, b, manifest = _valid_package()
    res = atomic_publish_package(str(root), pkg_id, b, {"bad": 1})
    assert res["technical_status"] == "FAIL"
    assert "STAGING_CLEANUP_FAILED" in res["reason_codes"]
    assert "PACKAGE_STAGING_INTEGRITY_FAILED" in res["reason_codes"]

def test_write_failure_before_completion(tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    pkg_id, b, manifest = _valid_package()
    b["human-preview.md"] = 123
    res = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res["technical_status"] == "FAIL"
    assert "PACKAGE_ARTIFACT_WRITE_FAILED" in res["reason_codes"]
    assert list(root.iterdir()) == []

def test_same_package_cannot_be_published_twice(tmp_path):
    root = tmp_path / "root"
    root.mkdir()

    pkg_id, b, manifest = _valid_package()
    res1 = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res1["technical_status"] == "PASS"

    res2 = atomic_publish_package(str(root), pkg_id, b, manifest)
    assert res2["technical_status"] == "FAIL"
    assert "PACKAGE_ALREADY_EXISTS" in res2["reason_codes"]
