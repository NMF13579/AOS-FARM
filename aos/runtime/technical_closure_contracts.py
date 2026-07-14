import copy
import hashlib
import re
from typing import Any

from aos.runtime.canonical_serialization import canonicalize_validated_json


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_OID_RE = re.compile(r"^[0-9a-f]{40}$")

TECHNICAL_STATUSES = {"PASS", "FAIL", "UNKNOWN", "NOT_RUN"}
CLOSURE_STATUSES = {
    "CLOSURE_OPEN",
    "CLOSURE_CORRECTION_REQUIRED",
    "CLOSURE_HUMAN_DECISION_REQUIRED",
    "CLOSURE_TECHNICALLY_CLOSED",
}
REQUIRED_HUMAN_DECISIONS = {
    "NONE",
    "HUMAN_EXECUTION_DECISION",
    "HUMAN_COMMIT_DECISION",
    "HUMAN_PUSH_DECISION",
    "HUMAN_INTEGRATION_DECISION",
    "HUMAN_RESULT_REVIEW",
}
NEXT_REQUIRED_ACTIONS = {
    "HUMAN_CORRECTION_DECISION",
    "HUMAN_RESOLVE_UNKNOWN",
    "HUMAN_VALIDATION_DECISION",
    "HUMAN_EXECUTION_DECISION",
    "HUMAN_COMMIT_DECISION",
    "HUMAN_PUSH_DECISION",
    "HUMAN_INTEGRATION_DECISION",
    "HUMAN_RESULT_REVIEW",
    "NO_FURTHER_AUTOMATIC_ACTION",
}
FORBIDDEN_AUTHORITY_FIELDS = {
    "approval_granted",
    "execution_authorized",
    "commit_authorized",
    "push_authorized",
    "integration_authorized",
    "release_authorized",
    "operation_started",
    "background_action_started",
    "lifecycle_mutated",
    "next_stage_started",
}
PREVIOUS_BINDING_DIGEST_KEYS = (
    "subject_digest",
    "evaluation_input_digest",
    "result_digest",
    "closure_status",
)


class ContractError(ValueError):
    def __init__(self, reason_codes, task_id=None, input_payload=None):
        self.reason_codes = sorted(set(reason_codes))
        self.task_id = task_id
        self.input_payload = input_payload
        super().__init__(", ".join(self.reason_codes))


def _fail(code, task_id=None, input_payload=None):
    raise ContractError([code], task_id=task_id, input_payload=input_payload)


def _check_json_domain(value, path="$", task_id=None, input_payload=None):
    if isinstance(value, float):
        _fail("FLOAT_NOT_ALLOWED", task_id, input_payload)
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                _fail("NON_STRING_OBJECT_KEY", task_id, input_payload)
            _check_json_domain(item, f"{path}.{key}", task_id, input_payload)
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _check_json_domain(item, f"{path}[{index}]", task_id, input_payload)


def _check_forbidden_fields(value, task_id=None, input_payload=None):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in FORBIDDEN_AUTHORITY_FIELDS:
                _fail("FORBIDDEN_AUTHORITY_FIELD", task_id, input_payload)
            _check_forbidden_fields(item, task_id, input_payload)
    elif isinstance(value, list):
        for item in value:
            _check_forbidden_fields(item, task_id, input_payload)


def _require_fields(obj, fields, task_id=None, input_payload=None):
    if not isinstance(obj, dict):
        _fail("OBJECT_REQUIRED", task_id, input_payload)
    missing = sorted(set(fields) - set(obj.keys()))
    if missing:
        _fail("MISSING_REQUIRED_FIELD", task_id, input_payload)
    unknown = sorted(set(obj.keys()) - set(fields))
    if unknown:
        _fail("UNKNOWN_FIELD", task_id, input_payload)


def _expect_str(value, code, task_id=None, input_payload=None, allow_empty=False):
    if not isinstance(value, str):
        _fail(code, task_id, input_payload)
    if not allow_empty and value == "":
        _fail(code, task_id, input_payload)
    return value


def _expect_nullable_str(value, code, task_id=None, input_payload=None):
    if value is None:
        return None
    return _expect_str(value, code, task_id, input_payload, allow_empty=False)


def _expect_int(value, expected, task_id=None, input_payload=None):
    if isinstance(value, bool):
        _fail("BOOL_AS_INT", task_id, input_payload)
    if not isinstance(value, int):
        _fail("INTEGER_REQUIRED", task_id, input_payload)
    if value != expected:
        _fail("UNSUPPORTED_SCHEMA_VERSION", task_id, input_payload)
    return value


def _expect_bool(value, task_id=None, input_payload=None):
    if not isinstance(value, bool):
        _fail("BOOLEAN_REQUIRED", task_id, input_payload)
    return value


def _expect_sha(value, code="INVALID_SHA256", task_id=None, input_payload=None, nullable=False):
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        _fail(code, task_id, input_payload)
    return value


def _expect_oid(value, task_id=None, input_payload=None):
    if value is None:
        return None
    if not isinstance(value, str) or not GIT_OID_RE.fullmatch(value):
        _fail("INVALID_GIT_OID", task_id, input_payload)
    return value


def _expect_enum(value, allowed, code, task_id=None, input_payload=None):
    if not isinstance(value, str) or value not in allowed:
        _fail(code, task_id, input_payload)
    return value


def _validate_reason_codes(value, task_id=None, input_payload=None):
    if not isinstance(value, list):
        _fail("REASON_CODES_LIST_REQUIRED", task_id, input_payload)
    seen = set()
    result = []
    for item in value:
        code = _expect_str(item, "INVALID_REASON_CODE", task_id, input_payload)
        if code in seen:
            _fail("DUPLICATE_REASON_CODE", task_id, input_payload)
        seen.add(code)
        result.append(code)
    return sorted(result)


def _digest_payload(payload: Any) -> str:
    return hashlib.sha256(canonicalize_validated_json(payload)).hexdigest()


def compute_subject_digest(subject: dict) -> str:
    normalized_subject = _normalize_subject(
        subject,
        task_id=subject.get("task_id") if isinstance(subject, dict) else None,
        input_payload=subject,
    )
    projection = {
        "schema_version": normalized_subject["schema_version"],
        "task_id": normalized_subject["task_id"],
        "scope_digest": normalized_subject["scope_digest"],
        "candidate_oid": normalized_subject["candidate_oid"],
        "required_artifacts": normalized_subject["required_artifacts"],
        "integration_target": normalized_subject["integration_target"],
    }
    return _digest_payload(projection)


def compute_evaluation_input_digest(payload: dict) -> str:
    normalized = normalize_closure_input(payload)
    projection = {
        "subject": normalized["subject"],
        "requirements": normalized["requirements"],
        "required_results": normalized["required_results"],
        "authorization_frontier": normalized["authorization_frontier"],
        "review_triggers": normalized["review_triggers"],
    }
    return _digest_payload(projection)


def compute_result_digest(result: dict) -> str:
    projection = copy.deepcopy(result)
    projection.pop("result_digest", None)
    return _digest_payload(projection)


def attach_result_digest(result: dict) -> dict:
    normalized = copy.deepcopy(result)
    normalized["result_digest"] = compute_result_digest(normalized)
    return normalized


def _normalize_subject(subject, task_id=None, input_payload=None):
    _require_fields(
        subject,
        {
            "schema_version",
            "task_id",
            "scope_digest",
            "candidate_oid",
            "required_artifacts",
            "integration_target",
        },
        task_id,
        input_payload,
    )
    artifacts = subject["required_artifacts"]
    if not isinstance(artifacts, list):
        _fail("REQUIRED_ARTIFACTS_LIST_REQUIRED", task_id, input_payload)
    normalized_artifacts = []
    artifact_ids = set()
    for artifact in artifacts:
        _require_fields(artifact, {"artifact_type", "artifact_id", "artifact_digest"}, task_id, input_payload)
        artifact_type = _expect_str(artifact["artifact_type"], "INVALID_ARTIFACT_TYPE", task_id, input_payload)
        artifact_id = _expect_str(artifact["artifact_id"], "INVALID_ARTIFACT_ID", task_id, input_payload)
        identity = (artifact_type, artifact_id)
        if identity in artifact_ids:
            _fail("DUPLICATE_ARTIFACT", task_id, input_payload)
        artifact_ids.add(identity)
        normalized_artifacts.append(
            {
                "artifact_type": artifact_type,
                "artifact_id": artifact_id,
                "artifact_digest": _expect_sha(artifact["artifact_digest"], task_id=task_id, input_payload=input_payload),
            }
        )
    normalized_artifacts.sort(key=lambda item: (item["artifact_type"], item["artifact_id"], item["artifact_digest"]))

    target = subject["integration_target"]
    _require_fields(target, {"repository", "base_ref", "candidate_ref"}, task_id, input_payload)
    return {
        "schema_version": _expect_int(subject["schema_version"], 1, task_id, input_payload),
        "task_id": _expect_str(subject["task_id"], "INVALID_TASK_ID", task_id, input_payload),
        "scope_digest": _expect_sha(subject["scope_digest"], task_id=task_id, input_payload=input_payload),
        "candidate_oid": _expect_oid(subject["candidate_oid"], task_id, input_payload),
        "required_artifacts": normalized_artifacts,
        "integration_target": {
            "repository": _expect_nullable_str(target["repository"], "INVALID_REPOSITORY", task_id, input_payload),
            "base_ref": _expect_nullable_str(target["base_ref"], "INVALID_BASE_REF", task_id, input_payload),
            "candidate_ref": _expect_nullable_str(target["candidate_ref"], "INVALID_CANDIDATE_REF", task_id, input_payload),
        },
    }


def _normalize_requirements(requirements, task_id=None, input_payload=None):
    _require_fields(
        requirements,
        {
            "validation_required",
            "evidence_required",
            "merge_authorization_required",
            "integration_result_required",
        },
        task_id,
        input_payload,
    )
    return {key: _expect_bool(requirements[key], task_id, input_payload) for key in requirements}


def _normalize_validation_result(result, task_id=None, input_payload=None):
    _require_fields(result, {"technical_status", "subject_digest", "result_digest", "reason_codes"}, task_id, input_payload)
    return {
        "technical_status": _expect_enum(result["technical_status"], TECHNICAL_STATUSES, "INVALID_TECHNICAL_STATUS", task_id, input_payload),
        "subject_digest": _expect_sha(result["subject_digest"], task_id=task_id, input_payload=input_payload),
        "result_digest": _expect_sha(result["result_digest"], task_id=task_id, input_payload=input_payload, nullable=True),
        "reason_codes": _validate_reason_codes(result["reason_codes"], task_id, input_payload),
    }


def _normalize_evidence_result(result, task_id=None, input_payload=None):
    _require_fields(result, {"technical_status", "subject_digest", "evidence_digest", "reason_codes"}, task_id, input_payload)
    return {
        "technical_status": _expect_enum(result["technical_status"], TECHNICAL_STATUSES, "INVALID_TECHNICAL_STATUS", task_id, input_payload),
        "subject_digest": _expect_sha(result["subject_digest"], task_id=task_id, input_payload=input_payload),
        "evidence_digest": _expect_sha(result["evidence_digest"], task_id=task_id, input_payload=input_payload, nullable=True),
        "reason_codes": _validate_reason_codes(result["reason_codes"], task_id, input_payload),
    }


def _normalize_merge_authorization(result, task_id=None, input_payload=None):
    _require_fields(result, {"package_id", "subject_digest", "verification_status", "result_digest", "reason_codes"}, task_id, input_payload)
    return {
        "package_id": _expect_nullable_str(result["package_id"], "INVALID_PACKAGE_ID", task_id, input_payload),
        "subject_digest": _expect_sha(result["subject_digest"], task_id=task_id, input_payload=input_payload, nullable=True),
        "verification_status": _expect_enum(result["verification_status"], TECHNICAL_STATUSES, "INVALID_VERIFICATION_STATUS", task_id, input_payload),
        "result_digest": _expect_sha(result["result_digest"], task_id=task_id, input_payload=input_payload, nullable=True),
        "reason_codes": _validate_reason_codes(result["reason_codes"], task_id, input_payload),
    }


def _normalize_integration(result, task_id=None, input_payload=None):
    _require_fields(result, {"subject_digest", "observed_status", "result_digest", "reason_codes"}, task_id, input_payload)
    return {
        "subject_digest": _expect_sha(result["subject_digest"], task_id=task_id, input_payload=input_payload, nullable=True),
        "observed_status": _expect_enum(result["observed_status"], TECHNICAL_STATUSES, "INVALID_OBSERVED_STATUS", task_id, input_payload),
        "result_digest": _expect_sha(result["result_digest"], task_id=task_id, input_payload=input_payload, nullable=True),
        "reason_codes": _validate_reason_codes(result["reason_codes"], task_id, input_payload),
    }


def _normalize_required_results(results, requirements, task_id=None, input_payload=None):
    _require_fields(results, {"validation", "evidence", "merge_authorization", "integration"}, task_id, input_payload)
    normalized = {
        "validation": _normalize_validation_result(results["validation"], task_id, input_payload),
        "evidence": _normalize_evidence_result(results["evidence"], task_id, input_payload),
        "merge_authorization": _normalize_merge_authorization(results["merge_authorization"], task_id, input_payload),
        "integration": _normalize_integration(results["integration"], task_id, input_payload),
    }
    if requirements["merge_authorization_required"] is False and normalized["merge_authorization"] != {
        "package_id": None,
        "subject_digest": None,
        "verification_status": "NOT_RUN",
        "result_digest": None,
        "reason_codes": [],
    }:
        _fail("MERGE_AUTHORIZATION_REQUIRED_FALSE_INCONSISTENT", task_id, input_payload)
    if requirements["integration_result_required"] is False and normalized["integration"] != {
        "subject_digest": None,
        "observed_status": "NOT_RUN",
        "result_digest": None,
        "reason_codes": [],
    }:
        _fail("INTEGRATION_RESULT_REQUIRED_FALSE_INCONSISTENT", task_id, input_payload)
    return normalized


def _normalize_authorization_frontier(frontier, task_id=None, input_payload=None):
    _require_fields(frontier, {"required_human_decision"}, task_id, input_payload)
    return {
        "required_human_decision": _expect_enum(
            frontier["required_human_decision"],
            REQUIRED_HUMAN_DECISIONS,
            "INVALID_REQUIRED_HUMAN_DECISION",
            task_id,
            input_payload,
        )
    }


def _normalize_review_triggers(triggers, task_id=None, input_payload=None):
    _require_fields(triggers, {"reaudit_request_reference", "safety_triggers"}, task_id, input_payload)
    reference = triggers["reaudit_request_reference"]
    _require_fields(reference, {"present", "witness_id", "witness_digest"}, task_id, input_payload)
    present = _expect_bool(reference["present"], task_id, input_payload)
    witness_id = _expect_nullable_str(reference["witness_id"], "INVALID_WITNESS_ID", task_id, input_payload)
    witness_digest = _expect_sha(reference["witness_digest"], task_id=task_id, input_payload=input_payload, nullable=True)
    if present and (witness_id is None or witness_digest is None):
        _fail("REAUDIT_REFERENCE_INCOMPLETE", task_id, input_payload)
    if not present and (witness_id is not None or witness_digest is not None):
        _fail("REAUDIT_REFERENCE_PRESENT_FALSE_INCONSISTENT", task_id, input_payload)

    safety = triggers["safety_triggers"]
    if not isinstance(safety, list):
        _fail("SAFETY_TRIGGERS_LIST_REQUIRED", task_id, input_payload)
    normalized_safety = []
    seen = set()
    for trigger in safety:
        _require_fields(trigger, {"trigger_code", "subject_digest", "evidence_digest"}, task_id, input_payload)
        item = {
            "trigger_code": _expect_str(trigger["trigger_code"], "INVALID_TRIGGER_CODE", task_id, input_payload),
            "subject_digest": _expect_sha(trigger["subject_digest"], task_id=task_id, input_payload=input_payload),
            "evidence_digest": _expect_sha(trigger["evidence_digest"], task_id=task_id, input_payload=input_payload),
        }
        identity = (item["trigger_code"], item["subject_digest"], item["evidence_digest"])
        if identity in seen:
            _fail("DUPLICATE_SAFETY_TRIGGER", task_id, input_payload)
        seen.add(identity)
        normalized_safety.append(item)
    normalized_safety.sort(
        key=lambda item: (
            item["trigger_code"],
            item["subject_digest"],
            item["evidence_digest"],
        )
    )
    return {
        "reaudit_request_reference": {
            "present": present,
            "witness_id": witness_id,
            "witness_digest": witness_digest,
        },
        "safety_triggers": normalized_safety,
    }


def _normalize_previous_binding(binding, task_id=None, input_payload=None):
    _require_fields(
        binding,
        {"present", *PREVIOUS_BINDING_DIGEST_KEYS},
        task_id,
        input_payload,
    )
    present = _expect_bool(binding["present"], task_id, input_payload)
    normalized = {
        "present": present,
        "subject_digest": _expect_sha(
            binding["subject_digest"],
            task_id=task_id,
            input_payload=input_payload,
            nullable=True,
        ),
        "evaluation_input_digest": _expect_sha(
            binding["evaluation_input_digest"],
            task_id=task_id,
            input_payload=input_payload,
            nullable=True,
        ),
        "result_digest": _expect_sha(
            binding["result_digest"],
            task_id=task_id,
            input_payload=input_payload,
            nullable=True,
        ),
        "closure_status": None,
    }
    closure_status = binding["closure_status"]
    if closure_status is not None:
        normalized["closure_status"] = _expect_enum(closure_status, CLOSURE_STATUSES, "INVALID_CLOSURE_STATUS", task_id, input_payload)
    if not present and any(normalized[key] is not None for key in PREVIOUS_BINDING_DIGEST_KEYS):
        _fail("PREVIOUS_BINDING_PRESENT_FALSE_INCONSISTENT", task_id, input_payload)
    if present and any(normalized[key] is None for key in PREVIOUS_BINDING_DIGEST_KEYS):
        _fail("PREVIOUS_BINDING_INCOMPLETE", task_id, input_payload)
    return normalized


def normalize_closure_input(payload: dict) -> dict:
    task_id = None
    if isinstance(payload, dict):
        subject_payload = payload.get("subject")
        if isinstance(subject_payload, dict):
            task_id = subject_payload.get("task_id")
    _check_json_domain(payload, task_id=task_id, input_payload=payload)
    _check_forbidden_fields(payload, task_id=task_id, input_payload=payload)
    _require_fields(
        payload,
        {
            "schema_version",
            "subject",
            "requirements",
            "required_results",
            "authorization_frontier",
            "review_triggers",
            "previous_result_binding",
        },
        task_id,
        payload,
    )
    normalized = {
        "schema_version": _expect_int(payload["schema_version"], 1, task_id, payload),
        "subject": _normalize_subject(payload["subject"], task_id, payload),
    }
    normalized["requirements"] = _normalize_requirements(payload["requirements"], task_id, payload)
    normalized["required_results"] = _normalize_required_results(
        payload["required_results"],
        normalized["requirements"],
        task_id,
        payload,
    )
    normalized["authorization_frontier"] = _normalize_authorization_frontier(payload["authorization_frontier"], task_id, payload)
    normalized["review_triggers"] = _normalize_review_triggers(
        payload["review_triggers"],
        task_id=task_id,
        input_payload=payload,
    )
    normalized["previous_result_binding"] = _normalize_previous_binding(payload["previous_result_binding"], task_id, payload)
    return normalized


def terminal_stop_result() -> dict:
    result = {
        "response_kind": "TERMINAL_COMMAND_RESULT",
        "schema_version": 1,
        "command": "STOP",
        "result_digest": "",
        "terminal": True,
        "next_required_action": "NO_FURTHER_AUTOMATIC_ACTION",
        "continue_allowed": False,
        "closure_result_mutated": False,
        "approval_granted": False,
        "execution_authorized": False,
        "commit_authorized": False,
        "push_authorized": False,
        "integration_authorized": False,
        "release_authorized": False,
        "operation_started": False,
        "background_action_started": False,
        "broad_reaudit_started": False,
        "schedule_created": False,
        "lifecycle_mutated": False,
        "next_stage_started": False,
    }
    return attach_result_digest(result)


def input_payload_digest(payload):
    try:
        return _digest_payload(payload)
    except Exception:
        return None
