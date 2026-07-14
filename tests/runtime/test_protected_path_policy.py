import pytest
import os
import json
from aos.runtime.protected_path_policy import load_protected_path_policy, PolicyLoadError, normalize_path

def test_valid_policy(tmp_path):
    f = tmp_path / "policy.json"
    f.write_text('{"schema_version": 1, "protected_paths": ["a.md", "b/"]}')
    paths = load_protected_path_policy(str(f))
    assert paths == ["a.md", "b/"]

def test_missing_policy():
    with pytest.raises(PolicyLoadError, match="Policy file is missing"):
        load_protected_path_policy("nonexistent.json")

def test_malformed_json(tmp_path):
    f = tmp_path / "policy.json"
    f.write_text('{ bad json')
    with pytest.raises(PolicyLoadError, match="Policy file is malformed"):
        load_protected_path_policy(str(f))

def test_unknown_schema(tmp_path):
    f = tmp_path / "policy.json"
    f.write_text('{"schema_version": 2, "protected_paths": []}')
    with pytest.raises(PolicyLoadError, match="Unsupported schema version"):
        load_protected_path_policy(str(f))

def test_absolute_path():
    with pytest.raises(PolicyLoadError, match="Absolute paths are rejected"):
        normalize_path("/etc/passwd")

def test_traversal():
    with pytest.raises(PolicyLoadError, match="Path traversal is rejected"):
        normalize_path("../foo")
    with pytest.raises(PolicyLoadError, match="Path traversal is rejected"):
        normalize_path("foo/../bar")
    with pytest.raises(PolicyLoadError, match="Path traversal is rejected"):
        normalize_path("foo/..")
    with pytest.raises(PolicyLoadError, match="Path traversal is rejected"):
        normalize_path(".")

def test_duplicate_normalized_path(tmp_path):
    f = tmp_path / "policy.json"
    f.write_text('{"schema_version": 1, "protected_paths": ["a/", "a//"]}')
    with pytest.raises(PolicyLoadError, match="Duplicate path after normalization"):
        load_protected_path_policy(str(f))

def test_backslash_normalization():
    assert normalize_path("foo\\\\bar") == "foo/bar"

def test_empty_entry():
    with pytest.raises(PolicyLoadError, match="Empty path is not allowed"):
        normalize_path("")

def test_additional_property(tmp_path):
    f = tmp_path / "policy.json"
    f.write_text('{"schema_version": 1, "protected_paths": [], "extra": 1}')
    with pytest.raises(PolicyLoadError, match="Additional property not allowed"):
        load_protected_path_policy(str(f))
