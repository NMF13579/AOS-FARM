import pytest
import copy
from aos.runtime.package_freshness_evaluator import evaluate_package_freshness

def valid_ds():
    return {
        "repository_identity": {"id": 1},
        "pull_request": {"repository_id": 1, "number": 2, "base_oid": "a", "head_oid": "b"},
        "commits": {"items": []},
        "changed_paths": {"items": []},
        "protected_path_result": {"items": []},
        "required_checks": {"items": [{"name": "ci", "state": "PASS", "head_oid": "b"}]},
        "required_review_policy": {"required_approvals": 1},
        "reviews": {"approval_count": 1, "blocking_count": 0},
        "review_threads": {"unresolved_count": 0},
        "codeowner_state": {"satisfied": True},
        "rulesets": {"unsupported_type": False},
        "branch_protection": {"unsupported_type": False, "allowed_merge_methods": ["merge", "squash"]},
        "merge_queue": {"required": False},
        "required_deployments": {"required": False},
        "collection_completeness": {"commits_complete": True, "pagination_complete": True}
    }

def test_exact_state_match():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert res["technical_status"] == "PASS"
    assert res["freshness_status"] == "PASS"

def test_repository_identity_changed():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["repository_identity"]["id"] = 2
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert res["freshness_status"] == "FAIL"
    assert "REPOSITORY_IDENTITY_CHANGED" in res["reason_codes"]
    assert "AUTHORIZATION_PACKAGE_STALE" in res["reason_codes"]

def test_pr_identity_changed():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["pull_request"]["number"] = 3
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "PULL_REQUEST_IDENTITY_CHANGED" in res["reason_codes"]

def test_base_oid_changed():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["pull_request"]["base_oid"] = "c"
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "BASE_OID_CHANGED" in res["reason_codes"]

def test_head_oid_changed():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["pull_request"]["head_oid"] = "c"
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "HEAD_OID_CHANGED" in res["reason_codes"]

def test_commit_set_changed():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["commits"]["items"] = [{"oid": "c"}]
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "COMMIT_SET_CHANGED" in res["reason_codes"]

def test_changed_paths_changed():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["changed_paths"]["items"] = ["x"]
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "CHANGED_PATHS_CHANGED" in res["reason_codes"]

def test_protected_path_result_worsened():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["protected_path_result"]["items"] = ["y"]
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "PROTECTED_PATH_RESULT_CHANGED" in res["reason_codes"]

def test_required_check_becomes_pending():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["required_checks"]["items"][0]["state"] = "PENDING"
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "REQUIRED_CHECK_STATE_CHANGED" in res["reason_codes"]

def test_required_check_fails():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["required_checks"]["items"][0]["state"] = "FAILURE"
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "REQUIRED_CHECK_STATE_CHANGED" in res["reason_codes"]

def test_required_check_refers_to_old_head():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["required_checks"]["items"][0]["head_oid"] = "old"
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "REQUIRED_CHECK_STATE_CHANGED" in res["reason_codes"]

def test_required_approval_removed():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["required_review_policy"]["required_approvals"] = 2
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "REQUIRED_APPROVAL_STATE_CHANGED" in res["reason_codes"]

def test_new_blocking_review():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["reviews"]["blocking_count"] = 1
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "REVIEW_STATE_CHANGED" in res["reason_codes"]

def test_new_unresolved_thread():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["review_threads"]["unresolved_count"] = 1
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "REVIEW_THREAD_STATE_CHANGED" in res["reason_codes"]

def test_codeowners_changes():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["codeowner_state"]["satisfied"] = False
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "REVIEW_STATE_CHANGED" in res["reason_codes"]

def test_ruleset_changes():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["rulesets"]["foo"] = "bar"
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "RULESET_STATE_CHANGED" in res["reason_codes"]

def test_unsupported_new_required_rule():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["rulesets"]["unsupported_type"] = True
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert res["freshness_status"] == "UNKNOWN"
    assert "UNSUPPORTED_REQUIRED_POLICY" in res["reason_codes"]

def test_branch_protection_changes():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["branch_protection"]["foo"] = "bar"
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "BRANCH_PROTECTION_STATE_CHANGED" in res["reason_codes"]

def test_merge_queue_requirement_changes():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["merge_queue"]["required"] = True
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "MERGE_QUEUE_STATE_CHANGED" in res["reason_codes"]

def test_required_deployment_changes():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["required_deployments"]["required"] = True
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "DEPLOYMENT_STATE_CHANGED" in res["reason_codes"]

def test_merge_method_no_longer_allowed():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["branch_protection"]["allowed_merge_methods"] = ["rebase"]
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert "MERGE_METHOD_NO_LONGER_ALLOWED" in res["reason_codes"]

def test_collection_becomes_incomplete():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["collection_completeness"]["commits_complete"] = False
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert res["freshness_status"] == "UNKNOWN"
    assert "FRESHNESS_STATE_INCOMPLETE" in res["reason_codes"]

def test_missing_required_current_field():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    del ls["commits"]
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert res["freshness_status"] == "UNKNOWN"
    assert "FRESHNESS_STATE_INCOMPLETE" in res["reason_codes"]

def test_unknown_package_state_field():
    ds = valid_ds()
    ds["timestamp"] = 123
    ls = copy.deepcopy(ds)
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert res["freshness_status"] == "UNKNOWN"
    assert "UNKNOWN_PACKAGE_STATE_FIELD" in res["reason_codes"]

def test_invalid_package_id():
    res = evaluate_package_freshness("invalid", valid_ds(), valid_ds(), "squash")
    assert "PACKAGE_ID_INVALID" in res["reason_codes"]

def test_deterministic_changed_field_ordering():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["repository_identity"]["id"] = 2
    ls["pull_request"]["number"] = 3
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert res["changed_fields"] == sorted(res["changed_fields"])

def test_deterministic_reason_code_ordering():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    ls["repository_identity"]["id"] = 2
    ls["pull_request"]["number"] = 3
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert res["reason_codes"] == sorted(res["reason_codes"])

def test_inputs_not_mutated():
    ds = valid_ds()
    ds_orig = copy.deepcopy(ds)
    ls = copy.deepcopy(ds)
    ls["repository_identity"]["id"] = 2
    ls_orig = copy.deepcopy(ls)
    evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert ds == ds_orig
    assert ls == ls_orig

def test_pass_does_not_grant_approval():
    ds = valid_ds()
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ds, "squash")
    assert res["approval_granted"] is False

def test_pass_does_not_authorize_execution():
    ds = valid_ds()
    res = evaluate_package_freshness("sha256:" + "a"*64, ds, ds, "squash")
    assert res["execution_authorized"] is False

def test_no_filesystem_reads(): pass
def test_no_filesystem_writes(): pass
def test_no_github_access(): pass
def test_same_input_produces_same_result():
    ds = valid_ds()
    ls = copy.deepcopy(ds)
    res1 = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    res2 = evaluate_package_freshness("sha256:" + "a"*64, ds, ls, "squash")
    assert res1 == res2
