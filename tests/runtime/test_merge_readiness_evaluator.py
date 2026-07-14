import pytest
import copy
from aos.runtime.merge_readiness_evaluator import evaluate_stabilized_snapshot

def get_base_snapshot():
    return {
        "repository_identity": "owner/repo",
        "pull_request": {
            "state": "OPEN",
            "is_draft": False,
            "base_repository_identity": "owner/repo",
            "head_repository_identity": "owner/repo",
            "head_oid": "123",
            "base_oid": "abc"
        },
        "commits": {
            "items": [{"oid": "123"}]
        },
        "collection_completeness": {
            "commits_complete": True,
            "pagination_complete": True
        },
        "required_checks": {
            "items": [
                {"head_oid": "123", "state": "SUCCESS"}
            ]
        },
        "reviews": {
            "approval_count": 1,
            "blocking_count": 0
        },
        "required_review_policy": {
            "required_approvals": 1,
            "conversation_resolution_required": True
        },
        "codeowner_state": {
            "satisfied": True
        },
        "review_threads": {
            "unresolved_count": 0
        },
        "rulesets": {},
        "branch_protection": {
            "allowed_merge_methods": ["SQUASH"]
        },
        "merge_queue": {},
        "required_deployments": {},
        "changed_paths": {
            "items": ["README.md"]
        }
    }

def get_base_intent():
    return {
        "repository": "owner/repo",
        "expected_head_oid": "123",
        "merge_method": "SQUASH"
    }

def get_base_policy():
    return {
        "normalized_paths": ["protected/file.py"]
    }

def test_fully_ready():
    res = evaluate_stabilized_snapshot(get_base_snapshot(), get_base_intent(), get_base_policy())
    assert res["technical_status"] == "PASS"
    assert res["all_required_gates_passed"] is True

def test_pr_closed():
    snap = get_base_snapshot()
    snap["pull_request"]["state"] = "CLOSED"
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_pr_draft():
    snap = get_base_snapshot()
    snap["pull_request"]["is_draft"] = True
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_repository_mismatch():
    intent = get_base_intent()
    intent["repository"] = "other/repo"
    res = evaluate_stabilized_snapshot(get_base_snapshot(), intent, get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_missing_base_identity():
    snap = get_base_snapshot()
    del snap["pull_request"]["base_repository_identity"]
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "UNKNOWN"

def test_missing_head_identity():
    snap = get_base_snapshot()
    del snap["pull_request"]["head_repository_identity"]
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "UNKNOWN"

def test_head_oid_mismatch():
    intent = get_base_intent()
    intent["expected_head_oid"] = "999"
    res = evaluate_stabilized_snapshot(get_base_snapshot(), intent, get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_incomplete_commits():
    snap = get_base_snapshot()
    snap["collection_completeness"]["commits_complete"] = False
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "UNKNOWN"

def test_old_head_check_ignored():
    snap = get_base_snapshot()
    snap["required_checks"]["items"] = [{"head_oid": "old", "state": "FAILURE"}, {"head_oid": "123", "state": "SUCCESS"}]
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "PASS"

def test_missing_required_check():
    snap = get_base_snapshot()
    snap["required_checks"]["items"] = [{"head_oid": "123", "state": "MISSING"}]
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_pending_required_check():
    snap = get_base_snapshot()
    snap["required_checks"]["items"] = [{"head_oid": "123", "state": "PENDING"}]
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_failing_required_check():
    snap = get_base_snapshot()
    snap["required_checks"]["items"] = [{"head_oid": "123", "state": "FAILURE"}]
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_required_approvals_missing():
    snap = get_base_snapshot()
    snap["reviews"]["approval_count"] = 0
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_blocking_review_present():
    snap = get_base_snapshot()
    snap["reviews"]["blocking_count"] = 1
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_unresolved_thread_present():
    snap = get_base_snapshot()
    snap["review_threads"]["unresolved_count"] = 1
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_codeowners_unknown():
    snap = get_base_snapshot()
    snap["codeowner_state"]["unknown"] = True
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "UNKNOWN"

def test_ruleset_unknown():
    snap = get_base_snapshot()
    snap["rulesets"]["unknown_policy"] = True
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "UNKNOWN"

def test_unsupported_required_policy():
    snap = get_base_snapshot()
    snap["rulesets"]["unsupported_type"] = True
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "UNKNOWN"

def test_merge_queue_required_and_unsupported():
    snap = get_base_snapshot()
    snap["merge_queue"] = {"required": True, "supported": False}
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_deployment_required_and_failing():
    snap = get_base_snapshot()
    snap["required_deployments"] = {"required": True, "satisfied": False}
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_protected_path_changed():
    snap = get_base_snapshot()
    snap["changed_paths"]["items"] = ["protected/file.py"]
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "FAIL"

def test_changed_paths_incomplete():
    snap = get_base_snapshot()
    snap["changed_paths"]["incomplete"] = True
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "UNKNOWN"

def test_pagination_incomplete():
    snap = get_base_snapshot()
    snap["collection_completeness"]["pagination_complete"] = False
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["technical_status"] == "UNKNOWN"

def test_required_unknown_blocked():
    snap = get_base_snapshot()
    del snap["pull_request"]["base_repository_identity"]
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["control_status"] == "UNKNOWN_BLOCKED"

def test_required_fail_blocked():
    snap = get_base_snapshot()
    snap["pull_request"]["state"] = "CLOSED"
    res = evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert res["control_status"] == "BLOCKED"

def test_all_required_pass_human_review_required():
    res = evaluate_stabilized_snapshot(get_base_snapshot(), get_base_intent(), get_base_policy())
    assert res["control_status"] == "HUMAN_REVIEW_REQUIRED"

def test_pass_does_not_set_approval():
    res = evaluate_stabilized_snapshot(get_base_snapshot(), get_base_intent(), get_base_policy())
    assert res["approval_granted"] is False

def test_input_snapshot_not_mutated():
    snap = get_base_snapshot()
    snap_copy = copy.deepcopy(snap)
    evaluate_stabilized_snapshot(snap, get_base_intent(), get_base_policy())
    assert snap == snap_copy
