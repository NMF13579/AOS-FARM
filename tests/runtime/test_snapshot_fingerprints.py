import pytest
from aos.runtime.snapshot_fingerprints import (
    fingerprint_repository_identity,
    fingerprint_pr_anchor,
    fingerprint_commit_set,
    fingerprint_required_checks,
    fingerprint_review_threads,
    fingerprint_effective_reviews,
    fingerprint_blocking_reviews,
    fingerprint_required_policy,
    fingerprint_rulesets,
    fingerprint_protected_paths
)

def test_same_semantic_input_same_fingerprint():
    in1 = {"a": 1, "b": "c"}
    in2 = {"b": "c", "a": 1}
    assert fingerprint_repository_identity(in1) == fingerprint_repository_identity(in2)

def test_dictionary_key_ordering():
    in1 = {"x": 1, "a": 2}
    in2 = {"a": 2, "x": 1}
    assert fingerprint_pr_anchor(in1) == fingerprint_pr_anchor(in2)

def test_commit_ordering_normalization():
    in1 = [{"sha": "b"}, {"sha": "a"}]
    in2 = [{"sha": "a"}, {"sha": "b"}]
    assert fingerprint_commit_set(in1) == fingerprint_commit_set(in2)

def test_commit_set_change():
    in1 = [{"sha": "a"}]
    in2 = [{"sha": "b"}]
    assert fingerprint_commit_set(in1) != fingerprint_commit_set(in2)

def test_required_check_change():
    in1 = [{"name": "check1", "status": "pass"}]
    in2 = [{"name": "check2", "status": "pass"}]
    assert fingerprint_required_checks(in1) != fingerprint_required_checks(in2)

def test_thread_resolution_change():
    in1 = [{"id": "1", "resolved": True}]
    in2 = [{"id": "1", "resolved": False}]
    assert fingerprint_review_threads(in1) != fingerprint_review_threads(in2)

def test_effective_review_change():
    in1 = [{"user": "A", "state": "APPROVED"}]
    in2 = [{"user": "A", "state": "CHANGES_REQUESTED"}]
    assert fingerprint_effective_reviews(in1) != fingerprint_effective_reviews(in2)

def test_blocking_review_change():
    in1 = [{"id": 1, "blocking": True}]
    in2 = [{"id": 1, "blocking": False}]
    assert fingerprint_blocking_reviews(in1) != fingerprint_blocking_reviews(in2)

def test_ruleset_change():
    in1 = [{"id": 1, "enforcement": "active"}]
    in2 = [{"id": 1, "enforcement": "disabled"}]
    assert fingerprint_rulesets(in1) != fingerprint_rulesets(in2)

def test_protected_path_change():
    in1 = {"paths": ["a", "b"]}
    in2 = {"paths": ["a", "c"]}
    assert fingerprint_protected_paths(in1) != fingerprint_protected_paths(in2)

def test_timestamp_metadata_stripped():
    in1 = {"data": 1, "created_at": "2023-01-01"}
    in2 = {"data": 1, "created_at": "2023-01-02"}
    assert fingerprint_repository_identity(in1) == fingerprint_repository_identity(in2)

def test_api_source_metadata_stripped():
    in1 = {"data": 1, "url": "http://a"}
    in2 = {"data": 1, "url": "http://b"}
    assert fingerprint_repository_identity(in1) == fingerprint_repository_identity(in2)

def test_float_rejected():
    with pytest.raises(ValueError, match="Float is rejected"):
        fingerprint_repository_identity({"data": 1.0})

def test_bool_not_accepted_as_integer():
    assert fingerprint_repository_identity({"data": True}) != fingerprint_repository_identity({"data": 1})

def test_local_absolute_path_rejected():
    with pytest.raises(ValueError, match="Local absolute path is rejected where prohibited."):
        fingerprint_repository_identity({"path": "/etc/passwd"})

def test_result_format():
    res = fingerprint_repository_identity({"data": 1})
    assert res.startswith("sha256:")
    assert len(res) == 7 + 64
    assert res[7:].islower()
    assert res[7:].isalnum()
