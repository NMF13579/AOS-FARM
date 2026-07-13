import json

from aos.runtime.simple_control_planning import bind_payload, risk_at_least, validate_analysis_package


VALIDATION_STATUSES = {"PASS", "FAIL", "NOT_RUN", "UNKNOWN"}
ALLOWED_BUNDLE_FIELDS = {
    "bundle_version",
    "task_id",
    "user_intent",
    "analysis_package",
    "scope_proposal",
    "scope_confirmation",
    "risk_profile_assignment",
    "execution_authorization",
    "repository_observation",
    "lifecycle",
}
FORBIDDEN_READY_STATES = {
    "CONTROL_READY_FOR_EXECUTION",
    "CONTROL_EXECUTING",
    "CONTROL_CHANGES_PREPARED",
    "CONTROL_READY_TO_COMMIT",
    "CONTROL_COMMITTED",
    "CONTROL_PUSHED",
    "CONTROL_INTEGRATED",
}
MAX_BUNDLE_JSON_BYTES = 65536


class StatusError(Exception):
    pass


def _add_check(checks, name, status, message):
    checks.append({"name": name, "status": status, "message": message})


def _proposal_binding(proposal):
    payload = json.loads(json.dumps(proposal))
    payload.pop("proposal_binding", None)
    return bind_payload(payload)


def _base_result(bundle):
    return {
        "validation_version": 1,
        "task_id": bundle.get("task_id"),
        "validation_status": "PASS",
        "checks": [],
        "unknowns": [],
        "blockers": [],
        "warnings": [],
        "evidence_status": "NOT_RUN",
        "approval_status": "NOT_PROVIDED",
        "execution_authorized": False,
        "derived_control_state": "CONTROL_BLOCKED",
        "analysis_status": "NOT_RUN",
        "lifecycle": {
            "status": bundle.get("lifecycle", {}).get("status", "UNKNOWN") if isinstance(bundle.get("lifecycle"), dict) else "UNKNOWN",
            "mutated": False,
        },
        "control": {"state": "CONTROL_BLOCKED"},
        "non_grants": ["approval", "execution", "commit", "push", "integration", "merge", "release", "lifecycle_mutation"],
    }


def _finalize(result, state=None):
    if state:
        result["derived_control_state"] = state
    if result["derived_control_state"] in FORBIDDEN_READY_STATES:
        result["derived_control_state"] = "CONTROL_BLOCKED"
        result["blockers"].append("681.5 cannot derive execution or Git write states")
    if result["blockers"] and result["validation_status"] == "PASS":
        result["validation_status"] = "FAIL"
    if result["unknowns"] and result["validation_status"] == "PASS":
        result["validation_status"] = "UNKNOWN"
    result["control"] = {"state": result["derived_control_state"]}
    return result


def _fail(result, check_name, message, state="CONTROL_BLOCKED"):
    _add_check(result["checks"], check_name, "FAIL", message)
    result["blockers"].append(message)
    result["validation_status"] = "FAIL"
    return _finalize(result, state)


def _unknown(result, check_name, message):
    _add_check(result["checks"], check_name, "UNKNOWN", message)
    result["unknowns"].append(message)
    result["validation_status"] = "UNKNOWN"
    return _finalize(result, "CONTROL_UNKNOWN_BLOCKED")


def validate_bundle(bundle):
    if not isinstance(bundle, dict):
        raise StatusError("validation bundle must be an object")
    if len(json.dumps(bundle, ensure_ascii=False).encode("utf-8")) > MAX_BUNDLE_JSON_BYTES:
        result = _base_result({"task_id": None})
        return _fail(result, "Bundle Size", "INPUT_SIZE_LIMIT_EXCEEDED")
    unknown_fields = sorted(set(bundle) - ALLOWED_BUNDLE_FIELDS)
    result = _base_result(bundle)
    if unknown_fields:
        return _fail(result, "Bundle Fields", "unknown top-level fields: " + ", ".join(unknown_fields))
    if bundle.get("bundle_version") != 1:
        return _fail(result, "Bundle Version", "bundle_version must be 1")
    intent = bundle.get("user_intent")
    if not isinstance(intent, dict):
        raise StatusError("user_intent is required")
    if bundle.get("execution_authorization") is not None:
        return _fail(result, "Execution Authorization", "execution authorization is not implemented in AOS-FARM.681.5")
    if intent.get("task_id") and intent.get("task_id") != bundle.get("task_id"):
        return _fail(result, "Task Binding", "user intent task_id does not match bundle task_id")
    _add_check(result["checks"], "User Intent", "PASS", "user intent present and bound")

    analysis = bundle.get("analysis_package")
    if analysis is None:
        _add_check(result["checks"], "Analysis Package", "NOT_RUN", "analysis package absent")
        result["analysis_status"] = "NOT_RUN"
        return _finalize(result, "CONTROL_ANALYZING")
    if not isinstance(analysis, dict):
        return _fail(result, "Analysis Package", "analysis_package must be object or null")
    try:
        validate_analysis_package(intent, analysis, analysis.get("repository_binding"))
    except Exception as exc:
        return _fail(result, "Analysis Package", str(exc))
    _add_check(result["checks"], "Analysis Package", "PASS", "analysis package contract valid")
    result["analysis_status"] = "PASS"

    proposal = bundle.get("scope_proposal")
    if proposal is None:
        _add_check(result["checks"], "Scope Proposal", "NOT_RUN", "scope proposal absent")
        return _finalize(result, "CONTROL_ANALYZED")
    if not isinstance(proposal, dict):
        return _fail(result, "Scope Proposal", "scope_proposal must be object or null")
    if proposal.get("intent_binding") != bind_payload(intent):
        return _fail(result, "Proposal Intent Binding", "proposal intent binding mismatch")
    if proposal.get("analysis_binding") != bind_payload(analysis):
        return _fail(result, "Proposal Analysis Binding", "proposal analysis binding mismatch")
    if proposal.get("repository_baseline_binding") != analysis.get("repository_binding"):
        return _fail(result, "Proposal Repository Binding", "proposal repository binding mismatch")
    if proposal.get("proposal_binding") != _proposal_binding(proposal):
        return _fail(result, "Proposal Binding", "proposal binding mismatch")
    if proposal.get("blockers"):
        result["blockers"].extend(proposal["blockers"])
        _add_check(result["checks"], "Proposal Blockers", "FAIL", "proposal contains blockers")
        return _finalize(result, "CONTROL_BLOCKED")
    if any(item.get("included") for item in proposal.get("optional_improvements", []) if isinstance(item, dict)):
        result["warnings"].append("optional improvements are included")
    _add_check(result["checks"], "Scope Proposal", "PASS", "proposal binding and completeness valid")

    confirmation = bundle.get("scope_confirmation")
    if confirmation is None:
        _add_check(result["checks"], "Scope Confirmation", "NOT_RUN", "scope confirmation absent")
        return _finalize(result, "CONTROL_SCOPE_CONFIRMATION_REQUIRED")
    if not isinstance(confirmation, dict):
        return _fail(result, "Scope Confirmation", "scope_confirmation must be object or null")
    if confirmation.get("proposal_binding") != proposal.get("proposal_binding"):
        return _fail(result, "Scope Confirmation Binding", "scope confirmation proposal binding mismatch")
    if confirmation.get("proposal_version") != proposal.get("proposal_version"):
        return _fail(result, "Scope Confirmation Version", "scope confirmation proposal version mismatch")
    if not confirmation.get("actor_reference"):
        return _fail(result, "Scope Confirmation Actor", "scope confirmation actor missing")
    _add_check(result["checks"], "Scope Confirmation", "PASS", "scope confirmation candidate bound")

    risk_minimum = proposal.get("risk_recommendation", {}).get("minimum", "UNKNOWN")
    if risk_minimum == "UNKNOWN":
        return _unknown(result, "Risk Profile Minimum", "Risk Profile minimum is UNKNOWN")
    risk = bundle.get("risk_profile_assignment")
    if risk is None:
        _add_check(result["checks"], "Risk Profile Assignment", "NOT_RUN", "Risk Profile assignment absent")
        return _finalize(result, "CONTROL_RISK_SELECTION_REQUIRED")
    if not isinstance(risk, dict):
        return _fail(result, "Risk Profile Assignment", "risk_profile_assignment must be object or null")
    if risk.get("proposal_binding") != proposal.get("proposal_binding"):
        return _fail(result, "Risk Profile Binding", "Risk Profile assignment proposal binding mismatch")
    if risk.get("minimum_Risk_Profile") != risk_minimum:
        return _fail(result, "Risk Profile Minimum", "Risk Profile minimum mismatch")
    selected = risk.get("selected_Risk_Profile")
    if not risk_at_least(selected, risk_minimum):
        return _fail(result, "Risk Profile Selection", "selected Risk Profile is below minimum")
    if not risk.get("actor_reference") or str(risk.get("actor_reference")).lower().startswith("agent"):
        return _fail(result, "Risk Profile Actor", "local human actor is required")
    _add_check(result["checks"], "Risk Profile Assignment", "PASS", "Risk Profile assignment candidate bound")
    return _finalize(result, "CONTROL_EXECUTION_AUTHORIZATION_REQUIRED")


def status_card(validation_result, locale="en"):
    state = validation_result["derived_control_state"]
    labels = {
        "CONTROL_ANALYZING": {"en": "Analysis not run", "ru": "Анализ не выполнен"},
        "CONTROL_ANALYZED": {"en": "Analysis ready", "ru": "Анализ готов"},
        "CONTROL_SCOPE_CONFIRMATION_REQUIRED": {"en": "Scope confirmation required", "ru": "Требуется подтверждение scope"},
        "CONTROL_RISK_SELECTION_REQUIRED": {"en": "Risk Profile selection required", "ru": "Требуется выбор Risk Profile"},
        "CONTROL_EXECUTION_AUTHORIZATION_REQUIRED": {"en": "Execution authorization required", "ru": "Требуется отдельное разрешение execution"},
        "CONTROL_BLOCKED": {"en": "Blocked", "ru": "Заблокировано"},
        "CONTROL_UNKNOWN_BLOCKED": {"en": "Unknown blocked", "ru": "UNKNOWN заблокировал продолжение"},
    }
    return {
        "kind": "status",
        "task_id": validation_result.get("task_id"),
        "lifecycle": validation_result.get("lifecycle", {"status": "UNKNOWN", "mutated": False}),
        "control_state": state,
        "control_state_label": labels.get(state, {}).get(locale, labels.get(state, {}).get("en", state)),
        "documentation_route": _detail_value(validation_result, "documentation_route") or "UNKNOWN",
        "proposal_version": _detail_value(validation_result, "proposal_version"),
        "scope_confirmation_status": _check_status(validation_result, "Scope Confirmation"),
        "risk_profile_minimum": _detail_value(validation_result, "minimum_Risk_Profile"),
        "selected_Risk_Profile": _detail_value(validation_result, "selected_Risk_Profile"),
        "validation_status": validation_result["validation_status"],
        "evidence_status": validation_result["evidence_status"],
        "approval_status": validation_result["approval_status"],
        "execution_authorized": False,
        "unknown_count": len(validation_result["unknowns"]),
        "blocker_count": len(validation_result["blockers"]),
        "next_recommended_command": next_step(validation_result)["recommended_command"],
        "non_grants": validation_result["non_grants"],
        "status_is_source_of_truth": False,
    }


def _find_check(result, name):
    for check in result.get("checks", []):
        if check["name"] == name:
            return check["status"]
    return "NOT_RUN"


def _check_status(result, name):
    return _find_check(result, name)


def _detail_value(result, key):
    return result.get("details", {}).get(key)


def next_step(validation_result):
    state = validation_result["derived_control_state"]
    mapping = {
        "CONTROL_ANALYZING": ("ANALYZE", True, None),
        "CONTROL_ANALYZED": ("PLAN", True, None),
        "CONTROL_SCOPE_CONFIRMATION_REQUIRED": ("ACCEPT_SCOPE", True, None),
        "CONTROL_RISK_SELECTION_REQUIRED": ("SELECT_RISK", True, None),
        "CONTROL_EXECUTION_AUTHORIZATION_REQUIRED": ("EXECUTE", False, "RUNTIME_NOT_IMPLEMENTED"),
    }
    if state == "CONTROL_BLOCKED":
        return {
            "kind": "next",
            "recommended_command": "HUMAN_REVIEW",
            "available": False,
            "reason_code": "CONTROL_BLOCKED",
            "operation_started": False,
            "blockers": validation_result.get("blockers", []),
            "non_grants": validation_result["non_grants"],
        }
    if state == "CONTROL_UNKNOWN_BLOCKED":
        return {
            "kind": "next",
            "recommended_command": "HUMAN_REVIEW",
            "available": False,
            "reason_code": "CONTROL_UNKNOWN_BLOCKED",
            "operation_started": False,
            "unknowns": validation_result.get("unknowns", []),
            "non_grants": validation_result["non_grants"],
        }
    command, available, reason = mapping.get(state, ("HUMAN_REVIEW", False, "UNKNOWN_STATE"))
    return {
        "kind": "next",
        "recommended_command": command,
        "available": available,
        "reason_code": reason,
        "operation_started": False,
        "non_grants": validation_result["non_grants"],
    }


def show_details(bundle, validation_result):
    proposal = bundle.get("scope_proposal") or {}
    confirmation = bundle.get("scope_confirmation") or {}
    risk = bundle.get("risk_profile_assignment") or {}
    analysis = bundle.get("analysis_package") or {}
    return {
        "kind": "details",
        "schema_versions": {"bundle": bundle.get("bundle_version"), "validation": validation_result.get("validation_version")},
        "task_id": bundle.get("task_id"),
        "intent_binding": bind_payload(bundle["user_intent"]) if isinstance(bundle.get("user_intent"), dict) else None,
        "analysis_binding": bind_payload(analysis) if analysis else None,
        "repository_baseline_binding": proposal.get("repository_baseline_binding") or analysis.get("repository_binding"),
        "proposal_id": proposal.get("proposal_id"),
        "proposal_version": proposal.get("proposal_version"),
        "proposal_binding": proposal.get("proposal_binding"),
        "confirmation_binding": confirmation.get("proposal_binding"),
        "minimum_Risk_Profile": risk.get("minimum_Risk_Profile") or proposal.get("risk_recommendation", {}).get("minimum"),
        "selected_Risk_Profile": risk.get("selected_Risk_Profile"),
        "actor_reference": confirmation.get("actor_reference") or risk.get("actor_reference"),
        "authentication_level": confirmation.get("authentication_level") or risk.get("authentication_level"),
        "checks": validation_result.get("checks", []),
        "unknowns": validation_result.get("unknowns", []),
        "not_run": [check for check in validation_result.get("checks", []) if check.get("status") == "NOT_RUN"],
        "blockers": validation_result.get("blockers", []),
        "non_grants": validation_result.get("non_grants", []),
        "derived_control_state": validation_result.get("derived_control_state"),
        "command_availability": next_step(validation_result),
    }


def validation_result_with_details(bundle):
    result = validate_bundle(bundle)
    proposal = bundle.get("scope_proposal") or {}
    risk = bundle.get("risk_profile_assignment") or {}
    analysis = bundle.get("analysis_package") or {}
    result["details"] = {
        "documentation_route": proposal.get("documentation_route") or analysis.get("documentation_route"),
        "proposal_version": proposal.get("proposal_version"),
        "minimum_Risk_Profile": risk.get("minimum_Risk_Profile") or proposal.get("risk_recommendation", {}).get("minimum"),
        "selected_Risk_Profile": risk.get("selected_Risk_Profile"),
    }
    return result
