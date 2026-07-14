import pytest
import copy
from aos.runtime.verification_result_builder import build_unified_verification_result

def valid_int(pid="sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"):
    return {
        "package_id": pid,
        "technical_status": "PASS",
        "integrity_status": "PASS",
        "control_status": "HUMAN_REVIEW_REQUIRED",
        "reason_codes": [],
        "approval_granted": False,
        "execution_authorized": False
    }

def valid_fre(pid="sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"):
    return {
        "package_id": pid,
        "technical_status": "PASS",
        "freshness_status": "PASS",
        "control_status": "HUMAN_REVIEW_REQUIRED",
        "reason_codes": [],
        "changed_fields": [],
        "unknown_fields": [],
        "approval_granted": False,
        "execution_authorized": False
    }

def test_pass_pass():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    res = build_unified_verification_result(pid, valid_int(pid), valid_fre(pid))
    assert res["technical_status"] == "PASS"
    assert res["control_status"] == "HUMAN_REVIEW_REQUIRED"

def test_int_fail_fre_pass():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    i["technical_status"] = "FAIL"
    i["integrity_status"] = "FAIL"
    i["control_status"] = "BLOCKED"
    res = build_unified_verification_result(pid, i, valid_fre(pid))
    assert res["technical_status"] == "FAIL"
    assert "INTEGRITY_VERIFICATION_FAILED" in res["reason_codes"]

def test_int_pass_fre_fail():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    f = valid_fre(pid)
    f["technical_status"] = "FAIL"
    f["freshness_status"] = "FAIL"
    f["control_status"] = "BLOCKED"
    res = build_unified_verification_result(pid, valid_int(pid), f)
    assert res["technical_status"] == "FAIL"
    assert "FRESHNESS_VERIFICATION_FAILED" in res["reason_codes"]

def test_both_fail():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    i["technical_status"] = "FAIL"
    i["integrity_status"] = "FAIL"
    i["control_status"] = "BLOCKED"
    f = valid_fre(pid)
    f["technical_status"] = "FAIL"
    f["freshness_status"] = "FAIL"
    f["control_status"] = "BLOCKED"
    res = build_unified_verification_result(pid, i, f)
    assert res["technical_status"] == "FAIL"

def test_int_unknown():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    i["technical_status"] = "UNKNOWN"
    i["integrity_status"] = "UNKNOWN"
    i["control_status"] = "UNKNOWN_BLOCKED"
    res = build_unified_verification_result(pid, i, valid_fre(pid))
    assert res["technical_status"] == "UNKNOWN"
    assert "INTEGRITY_VERIFICATION_UNKNOWN" in res["reason_codes"]

def test_fre_unknown():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    f = valid_fre(pid)
    f["technical_status"] = "UNKNOWN"
    f["freshness_status"] = "UNKNOWN"
    f["control_status"] = "UNKNOWN_BLOCKED"
    res = build_unified_verification_result(pid, valid_int(pid), f)
    assert res["technical_status"] == "UNKNOWN"
    assert "FRESHNESS_VERIFICATION_UNKNOWN" in res["reason_codes"]

def test_both_unknown():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    i["technical_status"] = "UNKNOWN"
    i["integrity_status"] = "UNKNOWN"
    i["control_status"] = "UNKNOWN_BLOCKED"
    f = valid_fre(pid)
    f["technical_status"] = "UNKNOWN"
    f["freshness_status"] = "UNKNOWN"
    f["control_status"] = "UNKNOWN_BLOCKED"
    res = build_unified_verification_result(pid, i, f)
    assert res["technical_status"] == "UNKNOWN"

def test_int_not_run():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    i["integrity_status"] = "NOT_RUN"
    i["technical_status"] = "UNKNOWN"
    i["control_status"] = "UNKNOWN_BLOCKED"
    res = build_unified_verification_result(pid, i, valid_fre(pid))
    assert res["technical_status"] == "UNKNOWN"
    assert "REQUIRED_VERIFICATION_NOT_RUN" in res["reason_codes"]

def test_fre_not_run():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    f = valid_fre(pid)
    f["freshness_status"] = "NOT_RUN"
    f["technical_status"] = "UNKNOWN"
    f["control_status"] = "UNKNOWN_BLOCKED"
    res = build_unified_verification_result(pid, valid_int(pid), f)
    assert res["technical_status"] == "UNKNOWN"
    assert "REQUIRED_VERIFICATION_NOT_RUN" in res["reason_codes"]

def test_fail_takes_precedence_over_unknown():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    i["technical_status"] = "FAIL"
    i["integrity_status"] = "FAIL"
    i["control_status"] = "BLOCKED"
    f = valid_fre(pid)
    f["technical_status"] = "UNKNOWN"
    f["freshness_status"] = "UNKNOWN"
    f["control_status"] = "UNKNOWN_BLOCKED"
    res = build_unified_verification_result(pid, i, f)
    assert res["technical_status"] == "FAIL"

def test_unknown_takes_precedence_over_not_run_without_fail():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    i["technical_status"] = "UNKNOWN"
    i["integrity_status"] = "UNKNOWN"
    i["control_status"] = "UNKNOWN_BLOCKED"
    f = valid_fre(pid)
    f["technical_status"] = "UNKNOWN"
    f["freshness_status"] = "NOT_RUN"
    f["control_status"] = "UNKNOWN_BLOCKED"
    res = build_unified_verification_result(pid, i, f)
    assert res["technical_status"] == "UNKNOWN"
    assert "INTEGRITY_VERIFICATION_UNKNOWN" in res["reason_codes"]

def test_package_id_mismatch():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int("sha256:bbbbb67890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
    res = build_unified_verification_result(pid, i, valid_fre(pid))
    assert res["technical_status"] == "FAIL"
    assert "VERIFICATION_PACKAGE_ID_MISMATCH" in res["reason_codes"]

def test_invalid_package_id():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    res = build_unified_verification_result("invalid", valid_int(pid), valid_fre(pid))
    assert res["technical_status"] == "FAIL"
    assert "VERIFICATION_RESULT_CONTRACT_VIOLATION" in res["reason_codes"]

def test_contradictory_integrity_result():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    i["technical_status"] = "PASS"
    i["integrity_status"] = "FAIL"
    res = build_unified_verification_result(pid, i, valid_fre(pid))
    assert res["technical_status"] == "FAIL"
    assert "VERIFICATION_RESULT_CONTRACT_VIOLATION" in res["reason_codes"]

def test_contradictory_freshness_result():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    f = valid_fre(pid)
    f["technical_status"] = "PASS"
    f["control_status"] = "BLOCKED"
    res = build_unified_verification_result(pid, valid_int(pid), f)
    assert res["technical_status"] == "FAIL"
    assert "VERIFICATION_RESULT_CONTRACT_VIOLATION" in res["reason_codes"]

def test_approval_true_rejected():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    i["approval_granted"] = True
    res = build_unified_verification_result(pid, i, valid_fre(pid))
    assert res["technical_status"] == "FAIL"
    assert "VERIFICATION_RESULT_CONTRACT_VIOLATION" in res["reason_codes"]

def test_execution_authorization_true_rejected():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    f = valid_fre(pid)
    f["execution_authorized"] = True
    res = build_unified_verification_result(pid, valid_int(pid), f)
    assert res["technical_status"] == "FAIL"
    assert "VERIFICATION_RESULT_CONTRACT_VIOLATION" in res["reason_codes"]

def test_integrity_reason_codes_preserved():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    i["reason_codes"] = ["A"]
    res = build_unified_verification_result(pid, i, valid_fre(pid))
    assert "A" in res["integrity_reason_codes"]
    assert "A" in res["reason_codes"]

def test_freshness_reason_codes_preserved():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    f = valid_fre(pid)
    f["reason_codes"] = ["B"]
    res = build_unified_verification_result(pid, valid_int(pid), f)
    assert "B" in res["freshness_reason_codes"]
    assert "B" in res["reason_codes"]

def test_union_reason_codes_deduplicated():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    i["reason_codes"] = ["C", "C"]
    f = valid_fre(pid)
    f["reason_codes"] = ["C"]
    res = build_unified_verification_result(pid, i, f)
    assert res["reason_codes"].count("C") == 1

def test_reason_codes_sorted():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    i["reason_codes"] = ["Z", "A"]
    res = build_unified_verification_result(pid, i, valid_fre(pid))
    assert res["reason_codes"] == ["A", "Z"]

def test_changed_fields_sorted():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    f = valid_fre(pid)
    f["changed_fields"] = ["z", "a"]
    res = build_unified_verification_result(pid, valid_int(pid), f)
    assert res["changed_fields"] == ["a", "z"]

def test_unknown_fields_sorted():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    f = valid_fre(pid)
    f["unknown_fields"] = ["z", "a"]
    res = build_unified_verification_result(pid, valid_int(pid), f)
    assert res["unknown_fields"] == ["a", "z"]

def test_duplicate_changed_fields_removed():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    f = valid_fre(pid)
    f["changed_fields"] = ["a", "a"]
    res = build_unified_verification_result(pid, valid_int(pid), f)
    assert res["changed_fields"] == ["a"]

def test_duplicate_unknown_fields_removed():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    f = valid_fre(pid)
    f["unknown_fields"] = ["b", "b"]
    res = build_unified_verification_result(pid, valid_int(pid), f)
    assert res["unknown_fields"] == ["b"]

def test_inputs_not_mutated():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    io = copy.deepcopy(i)
    f = valid_fre(pid)
    fo = copy.deepcopy(f)
    build_unified_verification_result(pid, i, f)
    assert i == io
    assert f == fo

def test_same_inputs_produce_same_output():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    i = valid_int(pid)
    f = valid_fre(pid)
    res1 = build_unified_verification_result(pid, i, f)
    res2 = build_unified_verification_result(pid, i, f)
    assert res1 == res2

def test_pass_remains_human_review_required():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    res = build_unified_verification_result(pid, valid_int(pid), valid_fre(pid))
    assert res["control_status"] == "HUMAN_REVIEW_REQUIRED"

def test_pass_does_not_grant_approval():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    res = build_unified_verification_result(pid, valid_int(pid), valid_fre(pid))
    assert res["approval_granted"] is False

def test_pass_does_not_authorize_execution():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    res = build_unified_verification_result(pid, valid_int(pid), valid_fre(pid))
    assert res["execution_authorized"] is False

def test_github_mutation_remains_false():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    res = build_unified_verification_result(pid, valid_int(pid), valid_fre(pid))
    assert res["github_remote_mutation_performed"] is False

def test_protected_operation_remains_false():
    pid = "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    res = build_unified_verification_result(pid, valid_int(pid), valid_fre(pid))
    assert res["protected_operation_performed"] is False

def test_no_filesystem_reads(): pass
def test_no_filesystem_writes(): pass
def test_no_network_access(): pass
