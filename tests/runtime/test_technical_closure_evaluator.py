import copy
import json

import pytest

from aos.runtime.technical_closure_contracts import (
    compute_evaluation_input_digest,
    compute_subject_digest,
    normalize_closure_input,
)
from aos.runtime.technical_closure_evaluator import evaluate_technical_closure

from tests.runtime.test_technical_closure_contracts import bound_input, valid_input


def prepared_input():
    payload = bound_input()
    subject_digest = compute_subject_digest(payload["subject"])
    payload["required_results"]["validation"]["subject_digest"] = subject_digest
    payload["required_results"]["evidence"]["subject_digest"] = subject_digest
    payload["required_results"]["integration"]["subject_digest"] = subject_digest
    return normalize_closure_input(payload)


def evaluate(payload):
    return evaluate_technical_closure(payload)


def test_valid_integration_pass_is_technically_closed_and_deterministic():
    payload = prepared_input()
    first = evaluate(payload)
    second = evaluate(copy.deepcopy(payload))
    assert first == second
    assert first["response_kind"] == "TECHNICAL_CLOSURE_RESULT"
    assert first["technical_status"] == "PASS"
    assert first["control_status"] == "HUMAN_REVIEW_REQUIRED"
    assert first["closure_status"] == "CLOSURE_TECHNICALLY_CLOSED"
    assert first["next_required_action"] == "HUMAN_RESULT_REVIEW"
    assert first["continue_allowed"] is False
    assert first["approval_granted"] is False
    assert first["operation_started"] is False
    assert len(first["subject_digest"]) == 64
    assert len(first["evaluation_input_digest"]) == 64
    assert len(first["result_digest"]) == 64


def test_contract_error_has_no_fake_subject_digest():
    payload = valid_input()
    payload["subject"]["scope_digest"] = "bad"
    result = evaluate(payload)
    assert result["response_kind"] == "CONTRACT_ERROR"
    assert result["technical_status"] == "FAIL"
    assert result["control_status"] == "BLOCKED"
    assert result["subject_digest"] is None
    assert result["next_required_action"] == "HUMAN_CORRECTION_DECISION"


@pytest.mark.parametrize(
    "section,status_field,status,next_action,technical,control,closure",
    [
        ("validation", "technical_status", "FAIL", "HUMAN_CORRECTION_DECISION", "FAIL", "BLOCKED", "CLOSURE_CORRECTION_REQUIRED"),
        ("evidence", "technical_status", "UNKNOWN", "HUMAN_RESOLVE_UNKNOWN", "UNKNOWN", "UNKNOWN_BLOCKED", "CLOSURE_OPEN"),
        ("validation", "technical_status", "NOT_RUN", "HUMAN_VALIDATION_DECISION", "NOT_RUN", "BLOCKED", "CLOSURE_OPEN"),
    ],
)
def test_evaluation_priority_for_fail_unknown_and_not_run(section, status_field, status, next_action, technical, control, closure):
    payload = prepared_input()
    payload["required_results"][section][status_field] = status
    payload["required_results"][section]["reason_codes"] = [f"{section.upper()}_{status}"]
    result = evaluate(payload)
    assert result["technical_status"] == technical
    assert result["control_status"] == control
    assert result["closure_status"] == closure
    assert result["next_required_action"] == next_action


def test_binding_mismatch_precedes_technical_pass_and_proposes_reaudit():
    payload = prepared_input()
    payload["required_results"]["evidence"]["subject_digest"] = "1" * 64
    result = evaluate(payload)
    assert result["technical_status"] == "FAIL"
    assert result["next_required_action"] == "HUMAN_CORRECTION_DECISION"
    assert result["broad_reaudit_may_be_proposed"] is True
    assert "EVIDENCE_SUBJECT_DIGEST_MISMATCH" in result["reason_codes"]


def test_human_decision_frontier_returns_exact_one_action():
    payload = prepared_input()
    payload["authorization_frontier"]["required_human_decision"] = "HUMAN_PUSH_DECISION"
    result = evaluate(payload)
    assert result["technical_status"] == "PASS"
    assert result["closure_status"] == "CLOSURE_HUMAN_DECISION_REQUIRED"
    assert result["required_human_decision"] == "HUMAN_PUSH_DECISION"
    assert result["next_required_action"] == "HUMAN_PUSH_DECISION"


def test_safety_trigger_and_reaudit_reference_do_not_start_broad_audit():
    payload = prepared_input()
    subject_digest = compute_subject_digest(payload["subject"])
    payload["review_triggers"]["safety_triggers"] = [
        {"trigger_code": "OUT_OF_SCOPE_DELETION", "subject_digest": subject_digest, "evidence_digest": "b" * 64}
    ]
    result = evaluate(payload)
    assert result["next_required_action"] == "HUMAN_VALIDATION_DECISION"
    assert result["broad_reaudit_may_be_proposed"] is True
    assert result["broad_reaudit_started"] is False

    payload = prepared_input()
    payload["review_triggers"]["reaudit_request_reference"] = {
        "present": True,
        "witness_id": "witness-1",
        "witness_digest": "c" * 64,
    }
    result = evaluate(payload)
    assert result["next_required_action"] == "HUMAN_VALIDATION_DECISION"
    assert result["broad_reaudit_started"] is False


def test_previous_result_binding_detects_changed_input_and_reopen():
    payload = prepared_input()
    closed = evaluate(payload)
    payload["previous_result_binding"] = {
        "present": True,
        "subject_digest": closed["subject_digest"],
        "evaluation_input_digest": closed["evaluation_input_digest"],
        "result_digest": closed["result_digest"],
        "closure_status": "CLOSURE_TECHNICALLY_CLOSED",
    }
    payload["required_results"]["integration"]["observed_status"] = "UNKNOWN"
    result = evaluate(payload)
    assert result["binding_changed"] is False
    assert result["evaluation_input_changed"] is True
    assert result["reopened"] is True


def test_aos_farm_683_fixture_replay_cases():
    payload = prepared_input()
    subject_digest = compute_subject_digest(payload["subject"])

    deletion = copy.deepcopy(payload)
    deletion["required_results"]["validation"]["technical_status"] = "FAIL"
    deletion["required_results"]["validation"]["reason_codes"] = ["OUT_OF_SCOPE_DELETION"]
    assert evaluate(deletion)["next_required_action"] == "HUMAN_CORRECTION_DECISION"

    commit_ready = copy.deepcopy(payload)
    commit_ready["requirements"]["integration_result_required"] = False
    commit_ready["required_results"]["integration"] = {
        "subject_digest": None,
        "observed_status": "NOT_RUN",
        "result_digest": None,
        "reason_codes": [],
    }
    commit_ready["authorization_frontier"]["required_human_decision"] = "HUMAN_PUSH_DECISION"
    assert evaluate(commit_ready)["next_required_action"] == "HUMAN_PUSH_DECISION"

    pushed = copy.deepcopy(payload)
    pushed["requirements"]["integration_result_required"] = False
    pushed["required_results"]["integration"] = {
        "subject_digest": None,
        "observed_status": "NOT_RUN",
        "result_digest": None,
        "reason_codes": [],
    }
    pushed["authorization_frontier"]["required_human_decision"] = "HUMAN_INTEGRATION_DECISION"
    assert evaluate(pushed)["next_required_action"] == "HUMAN_INTEGRATION_DECISION"

    integrated = evaluate(payload)
    assert integrated["closure_status"] == "CLOSURE_TECHNICALLY_CLOSED"
    assert integrated["next_required_action"] == "HUMAN_RESULT_REVIEW"
    assert evaluate(copy.deepcopy(payload)) == integrated


def test_evaluator_blocks_side_effect_primitives(monkeypatch, tmp_path):
    import builtins
    import os
    import pathlib
    import socket
    import subprocess
    import tempfile

    def forbidden(*_args, **_kwargs):
        raise AssertionError("side effect attempted")

    monkeypatch.setattr(subprocess, "run", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    monkeypatch.setattr(os, "system", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(tempfile, "TemporaryDirectory", forbidden)
    monkeypatch.setattr(pathlib.Path, "write_text", forbidden)
    monkeypatch.setattr(pathlib.Path, "write_bytes", forbidden)
    monkeypatch.setattr(pathlib.Path, "mkdir", forbidden)
    original_open = builtins.open

    def guarded_open(file, mode="r", *args, **kwargs):
        if any(flag in mode for flag in ("w", "a", "x", "+")):
            raise AssertionError("write open attempted")
        return original_open(file, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", guarded_open)
    result = evaluate(prepared_input())
    assert result["technical_status"] == "PASS"
