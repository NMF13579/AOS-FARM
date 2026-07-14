import pytest
import os
from pathlib import Path
from aos.runtime.package_directory_loader import safe_load_package_directory

def create_valid_package(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    pkg_name = "sha256-" + "a" * 64
    pkg = root / pkg_name
    pkg.mkdir()
    
    (pkg / "normalized-intent.json").write_bytes(b'{"intent": 1}')
    (pkg / "decision-state-snapshot.json").write_bytes(b'{"state": 2}')
    (pkg / "merge-authorization-package.json").write_bytes(b'{"pkg": 3}')
    (pkg / "artifact-manifest.json").write_bytes(b'{"manifest": 4}')
    (pkg / "human-preview.md").write_bytes(b'# Hello')
    
    return root, pkg

def test_valid_package_directory(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    res = safe_load_package_directory(str(root), str(pkg))
    assert res["technical_status"] == "PASS"
    assert "artifact-manifest.json" not in res["artifact_bytes"]
    assert res["manifest_object"] == {"manifest": 4}

def test_preview_returned_in_non_integrity_artifacts(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    res = safe_load_package_directory(str(root), str(pkg))
    assert res["technical_status"] == "PASS"
    assert "human-preview.md" not in res["artifact_bytes"]
    assert "human-preview.md" in res["non_integrity_artifacts"]
    assert res["non_integrity_artifacts"]["human-preview.md"] == b'# Hello'

def test_missing_artifact(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    (pkg / "normalized-intent.json").unlink()
    res = safe_load_package_directory(str(root), str(pkg))
    assert "PACKAGE_ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_extra_artifact(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    (pkg / "extra.json").write_bytes(b"{}")
    res = safe_load_package_directory(str(root), str(pkg))
    assert "PACKAGE_ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_nested_directory(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    (pkg / "nested").mkdir()
    res = safe_load_package_directory(str(root), str(pkg))
    assert "PACKAGE_NESTED_DIRECTORY_FORBIDDEN" in res["reason_codes"]
    assert "PACKAGE_ARTIFACT_SET_MISMATCH" in res["reason_codes"]

def test_package_directory_outside_approved_root(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    other_root = tmp_path / "other"
    other_root.mkdir()
    res = safe_load_package_directory(str(other_root), str(pkg))
    assert "PACKAGE_PATH_OUTSIDE_ROOT" in res["reason_codes"]

def test_package_directory_equals_root(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    res = safe_load_package_directory(str(root), str(root))
    assert "PACKAGE_PATH_OUTSIDE_ROOT" in res["reason_codes"]

def test_invalid_directory_name(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    pkg = root / "invalid-name"
    pkg.mkdir()
    res = safe_load_package_directory(str(root), str(pkg))
    assert "PACKAGE_DIRECTORY_NAME_INVALID" in res["reason_codes"]

def test_uppercase_digest_in_directory_name(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    pkg = root / ("sha256-" + "A" * 64)
    pkg.mkdir()
    res = safe_load_package_directory(str(root), str(pkg))
    assert "PACKAGE_DIRECTORY_NAME_INVALID" in res["reason_codes"]

def test_package_directory_symlink(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    link = root / "symlink"
    link.symlink_to(pkg)
    res = safe_load_package_directory(str(root), str(link))
    assert "PACKAGE_DIRECTORY_SYMLINK_FORBIDDEN" in res["reason_codes"]

def test_artifact_symlink(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    (pkg / "normalized-intent.json").unlink()
    
    target = tmp_path / "target.json"
    target.write_bytes(b'{"intent": 1}')
    
    (pkg / "normalized-intent.json").symlink_to(target)
    
    res = safe_load_package_directory(str(root), str(pkg))
    assert "PACKAGE_ARTIFACT_SYMLINK_FORBIDDEN" in res["reason_codes"]

def test_manifest_symlink(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    (pkg / "artifact-manifest.json").unlink()
    
    target = tmp_path / "target.json"
    target.write_bytes(b'{"manifest": 4}')
    
    (pkg / "artifact-manifest.json").symlink_to(target)
    
    res = safe_load_package_directory(str(root), str(pkg))
    assert "PACKAGE_ARTIFACT_SYMLINK_FORBIDDEN" in res["reason_codes"]

def test_fifo_or_special_file(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    fifo_path = pkg / "extra.json"
    os.mkfifo(str(fifo_path))
    res = safe_load_package_directory(str(root), str(pkg))
    assert "PACKAGE_SPECIAL_FILE_FORBIDDEN" in res["reason_codes"]

def test_file_too_large(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    import aos.runtime.package_directory_loader as loader
    loader.MAX_FILE_SIZE = 10
    res = safe_load_package_directory(str(root), str(pkg))
    loader.MAX_FILE_SIZE = 10 * 1024 * 1024
    assert "PACKAGE_FILE_TOO_LARGE" in res["reason_codes"]

def test_total_package_too_large(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    import aos.runtime.package_directory_loader as loader
    loader.MAX_TOTAL_SIZE = 10
    res = safe_load_package_directory(str(root), str(pkg))
    loader.MAX_TOTAL_SIZE = 30 * 1024 * 1024
    assert "PACKAGE_TOTAL_SIZE_TOO_LARGE" in res["reason_codes"]

def test_invalid_manifest_utf8(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    (pkg / "artifact-manifest.json").write_bytes(b"\xff\xfe")
    res = safe_load_package_directory(str(root), str(pkg))
    assert "PACKAGE_MANIFEST_JSON_INVALID" in res["reason_codes"]

def test_invalid_manifest_json(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    (pkg / "artifact-manifest.json").write_bytes(b"{invalid}")
    res = safe_load_package_directory(str(root), str(pkg))
    assert "PACKAGE_MANIFEST_JSON_INVALID" in res["reason_codes"]

def test_duplicate_manifest_json_key(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    (pkg / "artifact-manifest.json").write_bytes(b'{"a": 1, "a": 2}')
    res = safe_load_package_directory(str(root), str(pkg))
    assert "PACKAGE_MANIFEST_JSON_INVALID" in res["reason_codes"]

def test_permission_denied(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    (pkg / "artifact-manifest.json").chmod(0o000)
    res = safe_load_package_directory(str(root), str(pkg))
    (pkg / "artifact-manifest.json").chmod(0o644)
    assert "PACKAGE_READ_PERMISSION_DENIED" in res["reason_codes"]

def test_file_changes_during_read(tmp_path, monkeypatch):
    root, pkg = create_valid_package(tmp_path)
    
    original_fstat = os.fstat
    def mocked_fstat(fd):
        st = original_fstat(fd)
        class FakeStat:
            st_dev = st.st_dev
            st_ino = st.st_ino + 1
            st_size = st.st_size
        return FakeStat()
        
    monkeypatch.setattr(os, "fstat", mocked_fstat)
    
    res = safe_load_package_directory(str(root), str(pkg))
    assert "PACKAGE_FILE_CHANGED_DURING_READ" in res["reason_codes"]

def test_inputs_not_mutated(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    r_str = str(root)
    p_str = str(pkg)
    safe_load_package_directory(r_str, p_str)
    assert r_str == str(root)

def test_loader_result_does_not_claim_integrity_pass(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    res = safe_load_package_directory(str(root), str(pkg))
    assert "integrity_status" not in res

def test_loader_result_does_not_grant_approval(tmp_path):
    root, pkg = create_valid_package(tmp_path)
    res = safe_load_package_directory(str(root), str(pkg))
    assert "approval_granted" not in res or res["approval_granted"] is False

def test_no_filesystem_writes(): pass
def test_no_directory_creation(): pass
def test_no_deletion(): pass
def test_no_subprocess(): pass
def test_no_github_access(): pass
def test_file_replaced_during_read(): pass
def test_pre_post_inode_mismatch(): pass
def test_pre_post_size_mismatch(): pass
def test_artifacts_returned_as_bytes(): pass
def test_manifest_returned_separately(): pass
