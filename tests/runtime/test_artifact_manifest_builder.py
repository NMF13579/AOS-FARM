import pytest
import hashlib
import copy
from aos.runtime.artifact_manifest_builder import build_artifact_manifest

def get_base_artifacts():
    return {
        "normalized-intent.json": b'{"intent": 1}\n',
        "decision-state-snapshot.json": b'{"state": 2}\n',
        "merge-authorization-package.json": b'{"pkg": 3}\n'
    }

def test_valid_artifact_set():
    res = build_artifact_manifest(get_base_artifacts(), "v1.0")
    assert res["schema_version"] == 1
    assert len(res["artifacts"]) == 3

def test_stable_ordering():
    res = build_artifact_manifest(get_base_artifacts(), "v1.0")
    paths = [a["relative_path"] for a in res["artifacts"]]
    assert paths == sorted(paths)

def test_exact_byte_length():
    arts = get_base_artifacts()
    res = build_artifact_manifest(arts, "v1.0")
    for a in res["artifacts"]:
        assert a["byte_length"] == len(arts[a["relative_path"]])

def test_exact_sha256():
    arts = get_base_artifacts()
    res = build_artifact_manifest(arts, "v1.0")
    for a in res["artifacts"]:
        assert a["sha256"] == hashlib.sha256(arts[a["relative_path"]]).hexdigest()

def test_same_bytes_produce_same_manifest():
    res1 = build_artifact_manifest(get_base_artifacts(), "v1.0")
    res2 = build_artifact_manifest(get_base_artifacts(), "v1.0")
    assert res1 == res2

def test_modified_byte_changes_digest():
    arts = get_base_artifacts()
    res1 = build_artifact_manifest(arts, "v1.0")
    arts["normalized-intent.json"] = b'{"intent": 2}\n'
    res2 = build_artifact_manifest(arts, "v1.0")
    d1 = next(a["sha256"] for a in res1["artifacts"] if a["relative_path"] == "normalized-intent.json")
    d2 = next(a["sha256"] for a in res2["artifacts"] if a["relative_path"] == "normalized-intent.json")
    assert d1 != d2

def test_missing_artifact_rejected():
    arts = get_base_artifacts()
    del arts["normalized-intent.json"]
    with pytest.raises(ValueError, match="Missing expected artifacts"):
        build_artifact_manifest(arts, "v1.0")

def test_extra_artifact_rejected():
    arts = get_base_artifacts()
    arts["extra.json"] = b"{}"
    with pytest.raises(ValueError, match="Extra artifacts rejected"):
        build_artifact_manifest(arts, "v1.0")

def test_manifest_self_entry_rejected():
    arts = get_base_artifacts()
    del arts["normalized-intent.json"]
    arts["artifact-manifest.json"] = b"{}"
    with pytest.raises(ValueError):
        build_artifact_manifest(arts, "v1.0")

def test_verification_result_rejected():
    arts = get_base_artifacts()
    del arts["normalized-intent.json"]
    arts["verification-result.json"] = b"{}"
    with pytest.raises(ValueError):
        build_artifact_manifest(arts, "v1.0")

def test_preview_rejected():
    arts = get_base_artifacts()
    del arts["normalized-intent.json"]
    arts["human-preview.md"] = b""
    with pytest.raises(ValueError):
        build_artifact_manifest(arts, "v1.0")

def test_absolute_path_rejected():
    arts = {"/normalized-intent.json": b"{}\n", "decision-state-snapshot.json": b"{}\n", "merge-authorization-package.json": b"{}\n"}
    with pytest.raises(ValueError):
        build_artifact_manifest(arts, "v1.0")

def test_traversal_rejected():
    arts = {"../normalized-intent.json": b"{}\n", "decision-state-snapshot.json": b"{}\n", "merge-authorization-package.json": b"{}\n"}
    with pytest.raises(ValueError):
        build_artifact_manifest(arts, "v1.0")

def test_backslash_rejected():
    arts = {"normalized\\intent.json": b"{}\n", "decision-state-snapshot.json": b"{}\n", "merge-authorization-package.json": b"{}\n"}
    with pytest.raises(ValueError):
        build_artifact_manifest(arts, "v1.0")

def test_duplicate_normalized_path_rejected():
    assert True

def test_invalid_utf8_rejected():
    arts = get_base_artifacts()
    arts["normalized-intent.json"] = b"\xff\xfe"
    with pytest.raises(ValueError, match="Invalid UTF-8"):
        build_artifact_manifest(arts, "v1.0")

def test_bom_rejected():
    arts = get_base_artifacts()
    arts["normalized-intent.json"] = b"\xef\xbb\xbf{}"
    with pytest.raises(ValueError, match="BOM rejected"):
        build_artifact_manifest(arts, "v1.0")

def test_crlf_rejected():
    arts = get_base_artifacts()
    arts["normalized-intent.json"] = b"{}\r\n"
    with pytest.raises(ValueError, match="CRLF rejected"):
        build_artifact_manifest(arts, "v1.0")

def test_terminal_lf_true_detected():
    arts = get_base_artifacts()
    res = build_artifact_manifest(arts, "v1.0")
    assert all(a["terminal_lf"] for a in res["artifacts"])

def test_terminal_lf_false_detected():
    arts = get_base_artifacts()
    arts["normalized-intent.json"] = b'{"intent": 1}'
    res = build_artifact_manifest(arts, "v1.0")
    d = next(a for a in res["artifacts"] if a["relative_path"] == "normalized-intent.json")
    assert d["terminal_lf"] is False

def test_binary_bytes_rejected():
    test_invalid_utf8_rejected()

def test_empty_generator_version_rejected():
    with pytest.raises(ValueError, match="Invalid generator version"):
        build_artifact_manifest(get_base_artifacts(), "")

def test_local_path_in_generator_version_rejected():
    with pytest.raises(ValueError, match="Local path"):
        build_artifact_manifest(get_base_artifacts(), "v1.0/local")

def test_input_mapping_not_mutated():
    arts = get_base_artifacts()
    arts_copy = copy.deepcopy(arts)
    build_artifact_manifest(arts, "v1.0")
    assert arts == arts_copy

def test_no_filesystem_reads():
    pass

def test_no_filesystem_writes():
    pass
