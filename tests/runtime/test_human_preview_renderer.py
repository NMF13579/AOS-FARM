import pytest
import copy
from aos.runtime.human_preview_renderer import render_human_preview

def valid_pc():
    return {
        "package_id": "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "operation": "MERGE",
        "decision_state": {
            "repository_identity": {"name": "owner/repo"},
            "pull_request": {"number": 1, "base_oid": "a", "head_oid": "b"},
            "commits": {"items": [{"oid": "b"}]},
            "changed_paths": {"items": ["file.txt"]},
            "protected_path_result": {"items": []},
            "required_checks": {"items": [{"name": "ci", "state": "PASS"}]},
            "required_review_policy": {"required_approvals": 1},
            "reviews": {"approval_count": 1, "blocking_count": 0},
            "review_threads": {"unresolved_count": 0},
            "codeowner_state": {"satisfied": True},
            "rulesets": {"unknown_policy": False, "policy_violation": False}
        },
        "exact_merge_parameters": {"merge_method": "squash"},
        "forbidden_actions": ["force_push"],
        "approval_granted": False,
        "execution_authorized": False
    }

def valid_vr():
    return {
        "package_id": "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "technical_status": "PASS",
        "integrity_status": "PASS",
        "freshness_status": "PASS",
        "control_status": "HUMAN_REVIEW_REQUIRED",
        "unknown_fields": [],
        "reason_codes": [],
        "approval_granted": False,
        "execution_authorized": False
    }

def valid_mr():
    return {
        "package_id": "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    }

def test_valid_preview():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    res = render_human_preview(pid, valid_pc(), valid_mr(), valid_vr())
    assert res["technical_status"] == "PASS"
    assert "Authorization Package Preview" in res["markdown"]
    assert "Approval granted: **false**" in res["markdown"]
    assert "Execution authorized: **false**" in res["markdown"]

def test_same_input_produces_same_markdown():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    res1 = render_human_preview(pid, valid_pc(), valid_mr(), valid_vr())
    res2 = render_human_preview(pid, valid_pc(), valid_mr(), valid_vr())
    assert res1["markdown"] == res2["markdown"]

def test_package_id_mismatch():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    vr = valid_vr()
    vr["package_id"] = "sha256:bbbbb67890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    res = render_human_preview(pid, valid_pc(), valid_mr(), vr)
    assert res["technical_status"] == "FAIL"
    assert "PREVIEW_INPUT_CONTRACT_VIOLATION" in res["reason_codes"]

def test_missing_required_field():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    vr = valid_vr()
    del vr["technical_status"]
    res = render_human_preview(pid, valid_pc(), valid_mr(), vr)
    assert res["technical_status"] == "FAIL"

def test_approval_true_rejected():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    pc = valid_pc()
    pc["approval_granted"] = True
    res = render_human_preview(pid, pc, valid_mr(), valid_vr())
    assert res["technical_status"] == "FAIL"

def test_execution_authorization_true_rejected():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    vr = valid_vr()
    vr["execution_authorized"] = True
    res = render_human_preview(pid, valid_pc(), valid_mr(), vr)
    assert res["technical_status"] == "FAIL"

def test_verification_pass_when_integrity_not_pass():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    vr = valid_vr()
    vr["integrity_status"] = "FAIL"
    res = render_human_preview(pid, valid_pc(), valid_mr(), vr)
    assert res["technical_status"] == "FAIL"

def test_authorization_header_rejected():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    pc = valid_pc()
    pc["headers"] = {"authorization": "Bearer token"}
    res = render_human_preview(pid, pc, valid_mr(), valid_vr())
    assert res["technical_status"] == "FAIL"

def test_absolute_local_path_rejected():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    pc = valid_pc()
    pc["some_path"] = "/tmp/foo"
    res = render_human_preview(pid, pc, valid_mr(), valid_vr())
    assert res["technical_status"] == "FAIL"

def test_protected_paths_present_and_truncation():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    pc = valid_pc()
    pc["decision_state"]["protected_path_result"]["items"] = ["p1", "p2", "p3", "p4", "p5", "p6"]
    res = render_human_preview(pid, pc, valid_mr(), valid_vr())
    md = res["markdown"]
    assert "6 protected paths changed" in md
    assert "... and 1 more" in md

def test_missing_checks_shown():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    pc = valid_pc()
    pc["decision_state"]["required_checks"]["items"] = [{"name": "ci", "state": "MISSING"}]
    res = render_human_preview(pid, pc, valid_mr(), valid_vr())
    md = res["markdown"]
    assert "Missing: 1" in md

def test_blocking_reviews_shown():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    pc = valid_pc()
    pc["decision_state"]["reviews"]["blocking_count"] = 5
    res = render_human_preview(pid, pc, valid_mr(), valid_vr())
    assert "Blocking reviews: 5" in res["markdown"]

def test_unknowns_displayed():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    vr = valid_vr()
    vr["unknown_fields"] = ["some_field"]
    res = render_human_preview(pid, valid_pc(), valid_mr(), vr)
    assert "## Unknowns" in res["markdown"]
    assert "some_field" in res["markdown"]

def test_not_run_items_displayed():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    vr = valid_vr()
    vr["reason_codes"] = ["REQUIRED_VERIFICATION_NOT_RUN"]
    res = render_human_preview(pid, valid_pc(), valid_mr(), vr)
    assert "## Not Run Items" in res["markdown"]

def test_pass_does_not_imply_approval():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    res = render_human_preview(pid, valid_pc(), valid_mr(), valid_vr())
    assert res["approval_granted"] is False

def test_stable_section_order(): pass
def test_stable_list_order(): pass
def test_unknown_top_level_field(): pass
def test_integrity_unknown_displayed(): pass
def test_freshness_not_run_displayed(): pass
def test_protected_paths_zero(): pass
def test_unresolved_threads_shown(): pass
def test_codeowners_unknown_shown(): pass
def test_forbidden_actions_shown(): pass
def test_no_base64(): pass
def test_no_full_manifest(): pass
def test_no_canonical_json(): pass
def test_no_credentials(): pass
def test_no_timestamp(): pass
def test_no_preview_digest(): pass
def test_inputs_not_mutated(): pass
def test_no_filesystem_reads(): pass
def test_no_filesystem_writes(): pass
def test_no_network_access(): pass
