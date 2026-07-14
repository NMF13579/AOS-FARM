import pytest
from aos.runtime.merge_readiness_contracts import evaluate_readiness_gates, REQUIRED_GATES

def _valid_gates():
    gates = []
    for g in REQUIRED_GATES:
        gates.append({
            "name": g,
            "status": "PASS",
            "required_for_operation": True,
            "reason_code": None,
            "evidence_reference": "ref"
        })
    return gates

def test_all_required_pass():
    res = evaluate_readiness_gates(_valid_gates())
    assert res["technical_status"] == "PASS"
    assert res["control_status"] == "HUMAN_REVIEW_REQUIRED"
    assert res["all_required_gates_passed"] is True
    assert res["approval_granted"] is False
    assert res["execution_authorized"] is False

def test_one_required_fail():
    gates = _valid_gates()
    gates[0]["status"] = "FAIL"
    gates[0]["reason_code"] = "SOME_ERROR"
    res = evaluate_readiness_gates(gates)
    assert res["technical_status"] == "FAIL"
    assert res["control_status"] == "BLOCKED"
    assert "SOME_ERROR" in res["reason_codes"]

def test_multiple_required_fail():
    gates = _valid_gates()
    gates[0]["status"] = "FAIL"
    gates[0]["reason_code"] = "ERROR_A"
    gates[1]["status"] = "FAIL"
    gates[1]["reason_code"] = "ERROR_B"
    res = evaluate_readiness_gates(gates)
    assert res["technical_status"] == "FAIL"
    assert res["control_status"] == "BLOCKED"
    assert res["reason_codes"] == sorted(["ERROR_A", "ERROR_B"])

def test_one_required_unknown():
    gates = _valid_gates()
    gates[0]["status"] = "UNKNOWN"
    res = evaluate_readiness_gates(gates)
    assert res["technical_status"] == "UNKNOWN"
    assert res["control_status"] == "UNKNOWN_BLOCKED"

def test_fail_and_unknown_together():
    gates = _valid_gates()
    gates[0]["status"] = "FAIL"
    gates[1]["status"] = "UNKNOWN"
    res = evaluate_readiness_gates(gates)
    assert res["technical_status"] == "FAIL"
    assert res["control_status"] == "BLOCKED"

def test_missing_required_gate():
    gates = _valid_gates()
    gates.pop()
    res = evaluate_readiness_gates(gates)
    assert res["technical_status"] == "UNKNOWN"
    assert res["control_status"] == "UNKNOWN_BLOCKED"
    assert "MISSING_REQUIRED_GATE" in res["reason_codes"]

def test_extra_unknown_gate():
    gates = _valid_gates()
    gates.append({"name": "magic_gate", "status": "PASS", "required_for_operation": False})
    with pytest.raises(ValueError, match="Unknown gate"):
        evaluate_readiness_gates(gates)

def test_optional_not_applicable():
    gates = _valid_gates()
    gates[0]["status"] = "NOT_APPLICABLE"
    gates[0]["required_for_operation"] = False
    res = evaluate_readiness_gates(gates)
    assert res["technical_status"] == "PASS"

def test_required_not_applicable_rejected():
    gates = _valid_gates()
    gates[0]["status"] = "NOT_APPLICABLE"
    gates[0]["required_for_operation"] = True
    with pytest.raises(ValueError, match="is required but marked NOT_APPLICABLE"):
        evaluate_readiness_gates(gates)

def test_deterministic_gate_ordering():
    gates1 = _valid_gates()
    gates2 = _valid_gates()
    gates2.reverse()
    res1 = evaluate_readiness_gates(gates1)
    res2 = evaluate_readiness_gates(gates2)
    assert [g["name"] for g in res1["gates"]] == [g["name"] for g in res2["gates"]]

def test_deterministic_reason_code_ordering():
    gates = _valid_gates()
    gates[0]["status"] = "FAIL"
    gates[0]["reason_code"] = "Z_ERROR"
    gates[1]["status"] = "FAIL"
    gates[1]["reason_code"] = "A_ERROR"
    res = evaluate_readiness_gates(gates)
    assert res["reason_codes"] == ["A_ERROR", "Z_ERROR"]

def test_pass_does_not_set_approval():
    res = evaluate_readiness_gates(_valid_gates())
    assert res["approval_granted"] is False

def test_pass_does_not_set_execution_authorization():
    res = evaluate_readiness_gates(_valid_gates())
    assert res["execution_authorized"] is False

def test_false_cannot_substitute_unknown():
    gates = _valid_gates()
    gates[0]["status"] = False
    with pytest.raises(ValueError, match="Invalid status"):
        evaluate_readiness_gates(gates)

def test_bool_as_int_rejected_where_relevant():
    gates = _valid_gates()
    gates[0]["required_for_operation"] = 1
    with pytest.raises(ValueError, match="must be a strict boolean"):
        evaluate_readiness_gates(gates)

def test_input_object_not_mutated():
    import copy
    gates = _valid_gates()
    original = copy.deepcopy(gates)
    evaluate_readiness_gates(gates)
    assert gates == original
