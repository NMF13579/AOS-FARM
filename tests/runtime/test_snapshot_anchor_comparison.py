import pytest
from aos.runtime.snapshot_anchor_comparison import compare_anchors, REQUIRED_FIELDS

def get_valid_anchor():
    return {
        "repository_identity": "owner/repo",
        "base_oid": "12345",
        "head_oid": "67890",
        "pr_state": "open",
        "draft_state": False,
        "commit_set_fingerprint": "sha256:a",
        "required_policy_fingerprint": "sha256:b",
        "required_checks_fingerprint": "sha256:c",
        "review_threads_fingerprint": "sha256:d",
        "effective_reviews_fingerprint": "sha256:e",
        "blocking_reviews_fingerprint": "sha256:f",
        "rulesets_fingerprint": "sha256:g",
        "protected_paths_fingerprint": "sha256:h"
    }

def test_identical_anchors_stable():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    res = compare_anchors(a1, a2)
    assert res["stable"] is True
    assert res["technical_status"] == "PASS"
    assert res["reason_code"] is None
    assert res["changed_fields"] == []

def test_base_oid_changed():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["base_oid"] = "999"
    res = compare_anchors(a1, a2)
    assert res["stable"] is False
    assert res["technical_status"] == "FAIL"
    assert res["reason_code"] == "SNAPSHOT_ANCHOR_CHANGED"
    assert res["changed_fields"] == ["base_oid"]

def test_head_oid_changed():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["head_oid"] = "000"
    res = compare_anchors(a1, a2)
    assert "head_oid" in res["changed_fields"]
    assert res["stable"] is False

def test_pr_state_changed():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["pr_state"] = "closed"
    res = compare_anchors(a1, a2)
    assert "pr_state" in res["changed_fields"]

def test_draft_state_changed():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["draft_state"] = True
    res = compare_anchors(a1, a2)
    assert "draft_state" in res["changed_fields"]

def test_commit_fingerprint_changed():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["commit_set_fingerprint"] = "sha256:changed"
    res = compare_anchors(a1, a2)
    assert "commit_set_fingerprint" in res["changed_fields"]

def test_required_policy_fingerprint_changed():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["required_policy_fingerprint"] = "x"
    res = compare_anchors(a1, a2)
    assert "required_policy_fingerprint" in res["changed_fields"]

def test_required_checks_fingerprint_changed():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["required_checks_fingerprint"] = "x"
    res = compare_anchors(a1, a2)
    assert "required_checks_fingerprint" in res["changed_fields"]

def test_review_thread_fingerprint_changed():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["review_threads_fingerprint"] = "x"
    res = compare_anchors(a1, a2)
    assert "review_threads_fingerprint" in res["changed_fields"]

def test_effective_reviews_fingerprint_changed():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["effective_reviews_fingerprint"] = "x"
    res = compare_anchors(a1, a2)
    assert "effective_reviews_fingerprint" in res["changed_fields"]

def test_blocking_reviews_fingerprint_changed():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["blocking_reviews_fingerprint"] = "x"
    res = compare_anchors(a1, a2)
    assert "blocking_reviews_fingerprint" in res["changed_fields"]

def test_ruleset_fingerprint_changed():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["rulesets_fingerprint"] = "x"
    res = compare_anchors(a1, a2)
    assert "rulesets_fingerprint" in res["changed_fields"]

def test_protected_paths_fingerprint_changed():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["protected_paths_fingerprint"] = "x"
    res = compare_anchors(a1, a2)
    assert "protected_paths_fingerprint" in res["changed_fields"]

def test_multiple_changes_return_sorted_field_list():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["base_oid"] = "x"
    a2["head_oid"] = "y"
    a2["pr_state"] = "z"
    res = compare_anchors(a1, a2)
    assert res["changed_fields"] == sorted(["base_oid", "head_oid", "pr_state"])

def test_missing_field_unknown():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    del a2["base_oid"]
    res = compare_anchors(a1, a2)
    assert res["stable"] is False
    assert res["technical_status"] == "UNKNOWN"
    assert res["reason_code"] == "SNAPSHOT_ANCHOR_INCOMPLETE"
    assert res["missing_fields"] == ["base_oid"]

def test_unknown_field_schema_mismatch():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["extra"] = "value"
    res = compare_anchors(a1, a2)
    assert res["stable"] is False
    assert res["technical_status"] == "FAIL"
    assert res["reason_code"] == "SNAPSHOT_ANCHOR_SCHEMA_MISMATCH"
    assert res["unexpected_fields"] == ["extra"]

def test_timestamp_metadata_rejected():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2["created_at"] = "123"
    res = compare_anchors(a1, a2)
    assert res["stable"] is False
    assert res["reason_code"] == "SNAPSHOT_ANCHOR_SCHEMA_MISMATCH"

def test_input_objects_are_not_mutated():
    a1 = get_valid_anchor()
    a2 = get_valid_anchor()
    a2_copy = get_valid_anchor()
    compare_anchors(a1, a2)
    assert a2 == a2_copy
