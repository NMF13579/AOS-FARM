import copy
import json
from pathlib import Path

import pytest

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise RuntimeError("JSON_SCHEMA_VALIDATOR_UNAVAILABLE") from exc

from aos.runtime.canonical_serialization import canonicalize_validated_json
from aos.runtime.technical_closure_contracts import (
    ContractError,
    compute_result_digest,
    compute_subject_digest,
    compute_evaluation_input_digest,
    normalize_closure_input,
    terminal_stop_result,
)


HEX = "a" * 64
OID = "9efd4d47f30a3cc00ac5a9314375dcc027e1cc58"
SCHEMA_PATH = Path("aos/schemas/technical-closure-input.schema.json")
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA)


def valid_input():
    return {
        "schema_version": 1,
        "subject": {
            "schema_version": 1,
            "task_id": "AOS-FARM.684.1.5",
            "scope_digest": HEX,
            "candidate_oid": OID,
            "required_artifacts": [
                {"artifact_type": "evidence", "artifact_id": "b", "artifact_digest": "b" * 64},
                {"artifact_type": "evidence", "artifact_id": "a", "artifact_digest": "c" * 64},
            ],
            "integration_target": {
                "repository": "NMF13579/AOS-FARM",
                "base_ref": "dev",
                "candidate_ref": "build/aos-farm-684-technical-closure",
            },
        },
        "requirements": {
            "validation_required": True,
            "evidence_required": True,
            "merge_authorization_required": False,
            "integration_result_required": True,
        },
        "required_results": {
            "validation": {
                "technical_status": "PASS",
                "subject_digest": HEX,
                "result_digest": "d" * 64,
                "reason_codes": [],
            },
            "evidence": {
                "technical_status": "PASS",
                "subject_digest": HEX,
                "evidence_digest": "e" * 64,
                "reason_codes": [],
            },
            "merge_authorization": {
                "package_id": None,
                "subject_digest": None,
                "verification_status": "NOT_RUN",
                "result_digest": None,
                "reason_codes": [],
            },
            "integration": {
                "subject_digest": HEX,
                "observed_status": "PASS",
                "result_digest": "f" * 64,
                "reason_codes": [],
            },
        },
        "authorization_frontier": {"required_human_decision": "NONE"},
        "review_triggers": {
            "reaudit_request_reference": {
                "present": False,
                "witness_id": None,
                "witness_digest": None,
            },
            "safety_triggers": [],
        },
        "previous_result_binding": {
            "present": False,
            "subject_digest": None,
            "evaluation_input_digest": None,
            "result_digest": None,
            "closure_status": None,
        },
    }


def bound_input():
    payload = valid_input()
    normalized = normalize_closure_input(payload)
    subject_digest = compute_subject_digest(normalized["subject"])
    normalized["required_results"]["validation"]["subject_digest"] = subject_digest
    normalized["required_results"]["evidence"]["subject_digest"] = subject_digest
    normalized["required_results"]["integration"]["subject_digest"] = subject_digest
    return normalize_closure_input(normalized)


def _schema_errors(payload):
    return sorted(
        VALIDATOR.iter_errors(payload),
        key=lambda error: (
            tuple(error.absolute_path),
            error.message,
        ),
    )


def _exact_empty_array_schema(schema):
    return schema.get("type") == "array" and schema.get("maxItems") == 0


def _top_level_conditional_count(schema):
    return sum(1 for item in schema.get("allOf", []) if isinstance(item, dict) and "if" in item and "then" in item)


def _has_required_false_condition(schema, requirement_name, result_name, exact_definition):
    for item in schema.get("allOf", []):
        if not isinstance(item, dict):
            continue
        requirement = (
            item.get("if", {})
            .get("properties", {})
            .get("requirements", {})
            .get("properties", {})
            .get(requirement_name, {})
        )
        result_ref = (
            item.get("then", {})
            .get("properties", {})
            .get("required_results", {})
            .get("properties", {})
            .get(result_name, {})
            .get("$ref")
        )
        if requirement.get("const") is False and result_ref == f"#/$defs/{exact_definition}":
            return True
    return False


def _runtime_accepts(payload):
    try:
        normalize_closure_input(payload)
    except ContractError as exc:
        return False, exc.reason_codes
    return True, []


def test_normalizes_artifacts_and_computes_non_circular_digests():
    payload = bound_input()
    assert [item["artifact_id"] for item in payload["subject"]["required_artifacts"]] == ["a", "b"]

    subject_digest = compute_subject_digest(payload["subject"])
    evaluation_digest = compute_evaluation_input_digest(payload)
    payload["previous_result_binding"] = {
        "present": True,
        "subject_digest": subject_digest,
        "evaluation_input_digest": "1" * 64,
        "result_digest": "2" * 64,
        "closure_status": "CLOSURE_TECHNICALLY_CLOSED",
    }
    assert compute_subject_digest(payload["subject"]) == subject_digest
    assert compute_evaluation_input_digest(payload) == evaluation_digest

    result = {
        "response_kind": "TECHNICAL_CLOSURE_RESULT",
        "schema_version": 1,
        "task_id": "AOS-FARM.684.1.5",
        "result_digest": "0" * 64,
        "reason_codes": [],
    }
    digest = compute_result_digest(result)
    mutated = dict(result)
    mutated["result_digest"] = "1" * 64
    assert compute_result_digest(mutated) == digest


@pytest.mark.parametrize(
    "mutate, fragment",
    [
        (lambda p: p.update({"unknown": True}), "UNKNOWN_FIELD"),
        (lambda p: p["subject"].update({"unknown": True}), "UNKNOWN_FIELD"),
        (lambda p: p.update({"schema_version": True}), "BOOL_AS_INT"),
        (lambda p: p["subject"].update({"scope_digest": "bad"}), "INVALID_SHA256"),
        (lambda p: p["subject"].update({"candidate_oid": "bad"}), "INVALID_GIT_OID"),
        (lambda p: p["subject"]["required_artifacts"].append(copy.deepcopy(p["subject"]["required_artifacts"][0])), "DUPLICATE_ARTIFACT"),
        (lambda p: p["required_results"]["validation"]["reason_codes"].extend(["A", "A"]), "DUPLICATE_REASON_CODE"),
        (lambda p: p.update({"approval_granted": False}), "FORBIDDEN_AUTHORITY_FIELD"),
    ],
)
def test_contract_rejects_strict_invalid_inputs(mutate, fragment):
    payload = valid_input()
    mutate(payload)
    with pytest.raises(ContractError) as exc:
        normalize_closure_input(payload)
    assert fragment in exc.value.reason_codes


def test_contract_rejects_float_and_non_string_mapping_key():
    payload = valid_input()
    payload["subject"]["scope_digest"] = 1.2
    with pytest.raises(ContractError) as exc:
        normalize_closure_input(payload)
    assert "FLOAT_NOT_ALLOWED" in exc.value.reason_codes

    payload = valid_input()
    payload["subject"]["required_artifacts"][0][1] = "bad"
    with pytest.raises(ContractError) as exc:
        normalize_closure_input(payload)
    assert "NON_STRING_OBJECT_KEY" in exc.value.reason_codes


def test_required_false_consistency_is_enforced():
    payload = valid_input()
    payload["required_results"]["merge_authorization"]["verification_status"] = "PASS"
    with pytest.raises(ContractError) as exc:
        normalize_closure_input(payload)
    assert "MERGE_AUTHORIZATION_REQUIRED_FALSE_INCONSISTENT" in exc.value.reason_codes

    payload = valid_input()
    payload["requirements"]["integration_result_required"] = False
    payload["required_results"]["integration"]["observed_status"] = "PASS"
    with pytest.raises(ContractError) as exc:
        normalize_closure_input(payload)
    assert "INTEGRATION_RESULT_REQUIRED_FALSE_INCONSISTENT" in exc.value.reason_codes


def schema_runtime_case_matrix():
    subject_digest = compute_subject_digest(bound_input()["subject"])
    evaluation_digest = compute_evaluation_input_digest(bound_input())

    def merge_not_required(field, value):
        payload = valid_input()
        payload["required_results"]["merge_authorization"][field] = value
        return payload

    def integration_not_required(field, value):
        payload = valid_input()
        payload["requirements"]["integration_result_required"] = False
        payload["required_results"]["integration"] = {
            "subject_digest": None,
            "observed_status": "NOT_RUN",
            "result_digest": None,
            "reason_codes": [],
        }
        payload["required_results"]["integration"][field] = value
        return payload

    def previous_false(field, value):
        payload = valid_input()
        payload["previous_result_binding"][field] = value
        return payload

    def previous_true():
        payload = bound_input()
        payload["previous_result_binding"] = {
            "present": True,
            "subject_digest": subject_digest,
            "evaluation_input_digest": evaluation_digest,
            "result_digest": "6" * 64,
            "closure_status": "CLOSURE_TECHNICALLY_CLOSED",
        }
        return payload

    def previous_true_field(field, value):
        payload = previous_true()
        payload["previous_result_binding"][field] = value
        return payload

    def reaudit_false(field, value):
        payload = valid_input()
        payload["review_triggers"]["reaudit_request_reference"][field] = value
        return payload

    def reaudit_true():
        payload = valid_input()
        payload["review_triggers"]["reaudit_request_reference"] = {
            "present": True,
            "witness_id": "witness",
            "witness_digest": "7" * 64,
        }
        return payload

    def reaudit_true_field(field, value):
        payload = reaudit_true()
        payload["review_triggers"]["reaudit_request_reference"][field] = value
        return payload

    def with_unknown(container_name):
        payload = valid_input()
        containers = {
            "root": payload,
            "subject": payload["subject"],
            "requirements": payload["requirements"],
            "required_results": payload["required_results"],
            "authorization_frontier": payload["authorization_frontier"],
            "review_triggers": payload["review_triggers"],
            "previous_result_binding": payload["previous_result_binding"],
        }
        containers[container_name]["unexpected"] = True
        return payload

    def authority_field(field, nested=False):
        payload = valid_input()
        if nested:
            payload["subject"][field] = False
        else:
            payload[field] = False
        return payload

    def exact_duplicate_artifact():
        payload = valid_input()
        payload["subject"]["required_artifacts"].append(copy.deepcopy(payload["subject"]["required_artifacts"][0]))
        return payload

    def composite_duplicate_artifact():
        payload = valid_input()
        payload["subject"]["required_artifacts"].append(
            {
                "artifact_type": payload["subject"]["required_artifacts"][0]["artifact_type"],
                "artifact_id": payload["subject"]["required_artifacts"][0]["artifact_id"],
                "artifact_digest": "8" * 64,
            }
        )
        return payload

    cases = [
        ("valid_baseline_input", bound_input(), True, True, None, "FULL"),
        ("merge_required_false_package_id", merge_not_required("package_id", "pkg"), False, False, "MERGE_AUTHORIZATION_REQUIRED_FALSE_INCONSISTENT", "FULL"),
        ("merge_required_false_subject_digest", merge_not_required("subject_digest", "1" * 64), False, False, "MERGE_AUTHORIZATION_REQUIRED_FALSE_INCONSISTENT", "FULL"),
        ("merge_required_false_status", merge_not_required("verification_status", "PASS"), False, False, "MERGE_AUTHORIZATION_REQUIRED_FALSE_INCONSISTENT", "FULL"),
        ("merge_required_false_result_digest", merge_not_required("result_digest", "2" * 64), False, False, "MERGE_AUTHORIZATION_REQUIRED_FALSE_INCONSISTENT", "FULL"),
        ("merge_required_false_reason_codes", merge_not_required("reason_codes", ["MERGE_NOT_RUN"]), False, False, "MERGE_AUTHORIZATION_REQUIRED_FALSE_INCONSISTENT", "FULL"),
        ("integration_required_false_subject_digest", integration_not_required("subject_digest", "3" * 64), False, False, "INTEGRATION_RESULT_REQUIRED_FALSE_INCONSISTENT", "FULL"),
        ("integration_required_false_status", integration_not_required("observed_status", "PASS"), False, False, "INTEGRATION_RESULT_REQUIRED_FALSE_INCONSISTENT", "FULL"),
        ("integration_required_false_result_digest", integration_not_required("result_digest", "4" * 64), False, False, "INTEGRATION_RESULT_REQUIRED_FALSE_INCONSISTENT", "FULL"),
        ("integration_required_false_reason_codes", integration_not_required("reason_codes", ["INTEGRATION_NOT_RUN"]), False, False, "INTEGRATION_RESULT_REQUIRED_FALSE_INCONSISTENT", "FULL"),
        ("previous_false_subject_digest", previous_false("subject_digest", "5" * 64), False, False, "PREVIOUS_BINDING_PRESENT_FALSE_INCONSISTENT", "FULL"),
        ("previous_false_evaluation_input_digest", previous_false("evaluation_input_digest", "5" * 64), False, False, "PREVIOUS_BINDING_PRESENT_FALSE_INCONSISTENT", "FULL"),
        ("previous_false_result_digest", previous_false("result_digest", "5" * 64), False, False, "PREVIOUS_BINDING_PRESENT_FALSE_INCONSISTENT", "FULL"),
        ("previous_false_closure_status", previous_false("closure_status", "CLOSURE_OPEN"), False, False, "PREVIOUS_BINDING_PRESENT_FALSE_INCONSISTENT", "FULL"),
        ("previous_true_valid", previous_true(), True, True, None, "FULL"),
        ("previous_true_subject_digest_null", previous_true_field("subject_digest", None), False, False, "PREVIOUS_BINDING_INCOMPLETE", "FULL"),
        ("previous_true_evaluation_input_digest_null", previous_true_field("evaluation_input_digest", None), False, False, "PREVIOUS_BINDING_INCOMPLETE", "FULL"),
        ("previous_true_result_digest_null", previous_true_field("result_digest", None), False, False, "PREVIOUS_BINDING_INCOMPLETE", "FULL"),
        ("previous_true_closure_status_null", previous_true_field("closure_status", None), False, False, "PREVIOUS_BINDING_INCOMPLETE", "FULL"),
        ("previous_true_subject_digest_invalid", previous_true_field("subject_digest", "bad"), False, False, "INVALID_SHA256", "FULL"),
        ("previous_true_evaluation_input_digest_invalid", previous_true_field("evaluation_input_digest", "bad"), False, False, "INVALID_SHA256", "FULL"),
        ("previous_true_result_digest_invalid", previous_true_field("result_digest", "bad"), False, False, "INVALID_SHA256", "FULL"),
        ("previous_true_closure_status_invalid", previous_true_field("closure_status", "BAD"), False, False, "INVALID_CLOSURE_STATUS", "FULL"),
        ("reaudit_false_witness_id", reaudit_false("witness_id", "witness"), False, False, "REAUDIT_REFERENCE_PRESENT_FALSE_INCONSISTENT", "FULL"),
        ("reaudit_false_witness_digest", reaudit_false("witness_digest", "7" * 64), False, False, "REAUDIT_REFERENCE_PRESENT_FALSE_INCONSISTENT", "FULL"),
        ("reaudit_true_valid", reaudit_true(), True, True, None, "FULL"),
        ("reaudit_true_witness_id_null", reaudit_true_field("witness_id", None), False, False, "REAUDIT_REFERENCE_INCOMPLETE", "FULL"),
        ("reaudit_true_witness_id_empty", reaudit_true_field("witness_id", ""), False, False, "INVALID_WITNESS_ID", "FULL"),
        ("reaudit_true_witness_digest_null", reaudit_true_field("witness_digest", None), False, False, "REAUDIT_REFERENCE_INCOMPLETE", "FULL"),
        ("reaudit_true_witness_digest_invalid", reaudit_true_field("witness_digest", "bad"), False, False, "INVALID_SHA256", "FULL"),
        ("unknown_field_root", with_unknown("root"), False, False, "UNKNOWN_FIELD", "FULL"),
        ("unknown_field_subject", with_unknown("subject"), False, False, "UNKNOWN_FIELD", "FULL"),
        ("unknown_field_requirements", with_unknown("requirements"), False, False, "UNKNOWN_FIELD", "FULL"),
        ("unknown_field_required_results", with_unknown("required_results"), False, False, "UNKNOWN_FIELD", "FULL"),
        ("unknown_field_authorization_frontier", with_unknown("authorization_frontier"), False, False, "UNKNOWN_FIELD", "FULL"),
        ("unknown_field_review_triggers", with_unknown("review_triggers"), False, False, "UNKNOWN_FIELD", "FULL"),
        ("unknown_field_previous_result_binding", with_unknown("previous_result_binding"), False, False, "UNKNOWN_FIELD", "FULL"),
    ]

    for field in [
        "approval_granted",
        "execution_authorized",
        "commit_authorized",
        "push_authorized",
        "integration_authorized",
        "release_authorized",
        "lifecycle_mutated",
        "next_stage_started",
    ]:
        cases.append((f"authority_field_root_{field}", authority_field(field), False, False, "FORBIDDEN_AUTHORITY_FIELD", "FULL"))
        cases.append((f"authority_field_nested_{field}", authority_field(field, nested=True), False, False, "FORBIDDEN_AUTHORITY_FIELD", "FULL"))

    cases.append(("exact_duplicate_artifact_object", exact_duplicate_artifact(), False, False, "DUPLICATE_ARTIFACT", "FULL"))
    cases.append(("composite_duplicate_artifact_identity", composite_duplicate_artifact(), True, False, "DUPLICATE_ARTIFACT", "RUNTIME_ONLY_COMPOSITE_UNIQUENESS"))
    return cases


@pytest.mark.parametrize(
    "case,payload,schema_expected,runtime_expected,reason_code,expressibility",
    schema_runtime_case_matrix(),
)
def test_input_schema_matches_runtime_for_expressible_contracts(case, payload, schema_expected, runtime_expected, reason_code, expressibility):
    schema_errors = _schema_errors(payload)
    schema_accepts = not schema_errors
    runtime_accepts, reason_codes = _runtime_accepts(payload)

    assert schema_accepts is schema_expected, (case, [error.message for error in schema_errors])
    assert runtime_accepts is runtime_expected, case
    if reason_code is not None:
        assert reason_code in reason_codes, case
    if expressibility == "RUNTIME_ONLY_COMPOSITE_UNIQUENESS":
        assert schema_accepts is True
        assert runtime_accepts is False


def test_schema_declares_exact_required_false_and_binding_conditionals():
    schema = SCHEMA
    assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    assert _top_level_conditional_count(schema) >= 2
    assert _has_required_false_condition(schema, "merge_authorization_required", "merge_authorization", "merge_authorization_not_required")
    assert _has_required_false_condition(schema, "integration_result_required", "integration", "integration_not_required")

    merge = schema["$defs"]["merge_authorization_not_required"]["properties"]
    assert merge["package_id"]["const"] is None
    assert merge["subject_digest"]["const"] is None
    assert merge["verification_status"]["const"] == "NOT_RUN"
    assert merge["result_digest"]["const"] is None
    assert _exact_empty_array_schema(merge["reason_codes"])

    integration = schema["$defs"]["integration_not_required"]["properties"]
    assert integration["subject_digest"]["const"] is None
    assert integration["observed_status"]["const"] == "NOT_RUN"
    assert integration["result_digest"]["const"] is None
    assert _exact_empty_array_schema(integration["reason_codes"])

    assert len(schema["$defs"]["previous_result_binding"].get("allOf", [])) >= 2
    assert len(schema["$defs"]["reaudit_request_reference"].get("allOf", [])) >= 2
    artifacts = schema["$defs"]["subject"]["properties"]["required_artifacts"]
    assert artifacts["uniqueItems"] is True
    assert "runtime-only" in artifacts["$comment"]


def test_reaudit_and_safety_trigger_contracts_require_binding():
    payload = valid_input()
    payload["review_triggers"]["reaudit_request_reference"] = {
        "present": True,
        "witness_id": None,
        "witness_digest": "a" * 64,
    }
    with pytest.raises(ContractError) as exc:
        normalize_closure_input(payload)
    assert "REAUDIT_REFERENCE_INCOMPLETE" in exc.value.reason_codes

    payload = bound_input()
    subject_digest = compute_subject_digest(payload["subject"])
    payload["review_triggers"]["safety_triggers"] = [
        {"trigger_code": "A", "subject_digest": subject_digest, "evidence_digest": "b" * 64},
        {"trigger_code": "A", "subject_digest": subject_digest, "evidence_digest": "b" * 64},
    ]
    with pytest.raises(ContractError) as exc:
        normalize_closure_input(payload)
    assert "DUPLICATE_SAFETY_TRIGGER" in exc.value.reason_codes


def test_stale_safety_trigger_subject_digest_is_not_contract_error():
    payload = bound_input()
    payload["review_triggers"]["safety_triggers"] = [
        {"trigger_code": "A", "subject_digest": "b" * 64, "evidence_digest": "c" * 64}
    ]
    normalized = normalize_closure_input(payload)
    assert normalized["review_triggers"]["safety_triggers"][0]["subject_digest"] == "b" * 64


def test_invalid_safety_trigger_digest_remains_contract_error():
    payload = bound_input()
    payload["review_triggers"]["safety_triggers"] = [
        {"trigger_code": "A", "subject_digest": "bad", "evidence_digest": "c" * 64}
    ]
    with pytest.raises(ContractError) as exc:
        normalize_closure_input(payload)
    assert "INVALID_SHA256" in exc.value.reason_codes


def test_stop_terminal_result_is_separate_and_digest_bound():
    result = terminal_stop_result()
    assert result["response_kind"] == "TERMINAL_COMMAND_RESULT"
    assert result["command"] == "STOP"
    assert "technical_status" not in result
    assert result["continue_allowed"] is False
    assert result["approval_granted"] is False
    digest = result["result_digest"]
    assert len(digest) == 64
    assert compute_result_digest(result) == digest
    canonicalize_validated_json(result)
