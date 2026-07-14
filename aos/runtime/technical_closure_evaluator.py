from aos.runtime.technical_closure_contracts import (
    ContractError,
    attach_result_digest,
    compute_evaluation_input_digest,
    compute_subject_digest,
    input_payload_digest,
    normalize_closure_input,
)


PRIORITY = {
    "REQUIRED_BINDING_MISMATCH": 2,
    "TECHNICAL_FAIL": 3,
    "TECHNICAL_UNKNOWN": 4,
    "REQUIRED_NOT_RUN": 5,
    "BOUND_SAFETY_TRIGGER": 6,
    "VALID_REAUDIT_REQUEST_REFERENCE": 7,
    "REQUIRED_HUMAN_AUTHORIZATION_DECISION": 8,
    "TECHNICALLY_CLOSED": 9,
}


def _sorted_reason_codes(items):
    return [code for _priority, code in sorted(items, key=lambda item: (item[0], item[1]))]


def _base_flags():
    return {
        "continue_allowed": False,
        "broad_reaudit_started": False,
        "approval_granted": False,
        "execution_authorized": False,
        "commit_authorized": False,
        "push_authorized": False,
        "integration_authorized": False,
        "release_authorized": False,
        "operation_started": False,
        "background_action_started": False,
        "schedule_created": False,
        "lifecycle_mutated": False,
        "next_stage_started": False,
    }


def _contract_error_response(error):
    result = {
        "response_kind": "CONTRACT_ERROR",
        "schema_version": 1,
        "task_id": error.task_id,
        "subject_digest": None,
        "evaluation_input_digest": None,
        "input_payload_digest": input_payload_digest(error.input_payload),
        "result_digest": "",
        "technical_status": "FAIL",
        "control_status": "BLOCKED",
        "closure_status": "CLOSURE_CORRECTION_REQUIRED",
        "reason_codes": sorted(error.reason_codes),
        "next_required_action": "HUMAN_CORRECTION_DECISION",
        "broad_reaudit_may_be_proposed": False,
        **_base_flags(),
    }
    return attach_result_digest(result)


def _collect_binding_mismatches(payload, subject_digest):
    reasons = []
    required_results = payload["required_results"]
    if required_results["validation"]["subject_digest"] != subject_digest:
        reasons.append((PRIORITY["REQUIRED_BINDING_MISMATCH"], "VALIDATION_SUBJECT_DIGEST_MISMATCH"))
    if required_results["evidence"]["subject_digest"] != subject_digest:
        reasons.append((PRIORITY["REQUIRED_BINDING_MISMATCH"], "EVIDENCE_SUBJECT_DIGEST_MISMATCH"))
    if payload["requirements"]["merge_authorization_required"]:
        merge_subject = required_results["merge_authorization"]["subject_digest"]
        if merge_subject != subject_digest:
            reasons.append((PRIORITY["REQUIRED_BINDING_MISMATCH"], "MERGE_AUTHORIZATION_SUBJECT_DIGEST_MISMATCH"))
    if payload["requirements"]["integration_result_required"]:
        integration_subject = required_results["integration"]["subject_digest"]
        if integration_subject != subject_digest:
            reasons.append((PRIORITY["REQUIRED_BINDING_MISMATCH"], "INTEGRATION_SUBJECT_DIGEST_MISMATCH"))
    for trigger in payload["review_triggers"]["safety_triggers"]:
        if trigger["subject_digest"] != subject_digest:
            reasons.append((PRIORITY["REQUIRED_BINDING_MISMATCH"], "SAFETY_TRIGGER_SUBJECT_DIGEST_MISMATCH"))
    return reasons


def _required_statuses(payload):
    statuses = [
        (
            "VALIDATION",
            payload["required_results"]["validation"]["technical_status"],
            payload["required_results"]["validation"]["reason_codes"],
        ),
        (
            "EVIDENCE",
            payload["required_results"]["evidence"]["technical_status"],
            payload["required_results"]["evidence"]["reason_codes"],
        ),
    ]
    if payload["requirements"]["merge_authorization_required"]:
        statuses.append(
            (
                "MERGE_AUTHORIZATION",
                payload["required_results"]["merge_authorization"]["verification_status"],
                payload["required_results"]["merge_authorization"]["reason_codes"],
            )
        )
    if payload["requirements"]["integration_result_required"]:
        statuses.append(
            (
                "INTEGRATION",
                payload["required_results"]["integration"]["observed_status"],
                payload["required_results"]["integration"]["reason_codes"],
            )
        )
    return statuses


def _collect_status_reasons(payload, status, priority_name):
    priority = PRIORITY[priority_name]
    reasons = []
    for section, observed_status, reason_codes in _required_statuses(payload):
        if observed_status == status:
            if reason_codes:
                reasons.extend((priority, code) for code in reason_codes)
            else:
                reasons.append((priority, f"{section}_{status}"))
    return reasons


def _binding_summary(previous_binding, subject_digest, evaluation_input_digest):
    if not previous_binding["present"]:
        return False, False, []
    stale = []
    binding_changed = previous_binding["subject_digest"] != subject_digest
    evaluation_input_changed = previous_binding["evaluation_input_digest"] != evaluation_input_digest
    if binding_changed:
        stale.append("SUBJECT_DIGEST_CHANGED")
    if evaluation_input_changed:
        stale.append("EVALUATION_INPUT_DIGEST_CHANGED")
    return binding_changed, evaluation_input_changed, stale


def evaluate_technical_closure(payload):
    try:
        normalized = normalize_closure_input(payload)
    except ContractError as error:
        return _contract_error_response(error)

    task_id = normalized["subject"]["task_id"]
    subject_digest = compute_subject_digest(normalized["subject"])
    evaluation_input_digest = compute_evaluation_input_digest(normalized)
    previous_binding = normalized["previous_result_binding"]
    binding_changed, evaluation_input_changed, stale_inputs = _binding_summary(
        previous_binding,
        subject_digest,
        evaluation_input_digest,
    )

    reason_items = []
    broad_reaudit = False
    required_human_decision = normalized["authorization_frontier"]["required_human_decision"]

    binding_reasons = _collect_binding_mismatches(normalized, subject_digest)
    if binding_reasons:
        reason_items.extend(binding_reasons)
        technical_status = "FAIL"
        control_status = "BLOCKED"
        closure_status = "CLOSURE_CORRECTION_REQUIRED"
        next_required_action = "HUMAN_CORRECTION_DECISION"
        broad_reaudit = True
    else:
        fail_reasons = _collect_status_reasons(normalized, "FAIL", "TECHNICAL_FAIL")
        unknown_reasons = _collect_status_reasons(normalized, "UNKNOWN", "TECHNICAL_UNKNOWN")
        not_run_reasons = _collect_status_reasons(normalized, "NOT_RUN", "REQUIRED_NOT_RUN")
        if fail_reasons:
            reason_items.extend(fail_reasons)
            technical_status = "FAIL"
            control_status = "BLOCKED"
            closure_status = "CLOSURE_CORRECTION_REQUIRED"
            next_required_action = "HUMAN_CORRECTION_DECISION"
        elif unknown_reasons:
            reason_items.extend(unknown_reasons)
            technical_status = "UNKNOWN"
            control_status = "UNKNOWN_BLOCKED"
            closure_status = "CLOSURE_OPEN"
            next_required_action = "HUMAN_RESOLVE_UNKNOWN"
        elif not_run_reasons:
            reason_items.extend(not_run_reasons)
            technical_status = "NOT_RUN"
            control_status = "BLOCKED"
            closure_status = "CLOSURE_OPEN"
            next_required_action = "HUMAN_VALIDATION_DECISION"
        elif normalized["review_triggers"]["safety_triggers"]:
            reason_items.extend(
                (PRIORITY["BOUND_SAFETY_TRIGGER"], trigger["trigger_code"])
                for trigger in normalized["review_triggers"]["safety_triggers"]
            )
            technical_status = "PASS"
            control_status = "HUMAN_REVIEW_REQUIRED"
            closure_status = "CLOSURE_HUMAN_DECISION_REQUIRED"
            next_required_action = "HUMAN_VALIDATION_DECISION"
            broad_reaudit = True
        elif normalized["review_triggers"]["reaudit_request_reference"]["present"]:
            reason_items.append((PRIORITY["VALID_REAUDIT_REQUEST_REFERENCE"], "VALID_REAUDIT_REQUEST_REFERENCE"))
            technical_status = "PASS"
            control_status = "HUMAN_REVIEW_REQUIRED"
            closure_status = "CLOSURE_HUMAN_DECISION_REQUIRED"
            next_required_action = "HUMAN_VALIDATION_DECISION"
            broad_reaudit = True
        elif required_human_decision != "NONE":
            reason_items.append((PRIORITY["REQUIRED_HUMAN_AUTHORIZATION_DECISION"], required_human_decision))
            technical_status = "PASS"
            control_status = "HUMAN_REVIEW_REQUIRED"
            closure_status = "CLOSURE_HUMAN_DECISION_REQUIRED"
            next_required_action = required_human_decision
        else:
            reason_items.append((PRIORITY["TECHNICALLY_CLOSED"], "TECHNICALLY_CLOSED"))
            technical_status = "PASS"
            control_status = "HUMAN_REVIEW_REQUIRED"
            closure_status = "CLOSURE_TECHNICALLY_CLOSED"
            next_required_action = "HUMAN_RESULT_REVIEW"

    reopened = (
        previous_binding["present"]
        and previous_binding["closure_status"] == "CLOSURE_TECHNICALLY_CLOSED"
        and closure_status != "CLOSURE_TECHNICALLY_CLOSED"
    )
    result = {
        "response_kind": "TECHNICAL_CLOSURE_RESULT",
        "schema_version": 1,
        "task_id": task_id,
        "subject_digest": subject_digest,
        "evaluation_input_digest": evaluation_input_digest,
        "result_digest": "",
        "technical_status": technical_status,
        "control_status": control_status,
        "closure_status": closure_status,
        "binding_changed": binding_changed,
        "evaluation_input_changed": evaluation_input_changed,
        "reopened": reopened,
        "stale_inputs": stale_inputs,
        "reason_codes": _sorted_reason_codes(reason_items),
        "required_human_decision": required_human_decision,
        "next_required_action": next_required_action,
        "broad_reaudit_may_be_proposed": broad_reaudit,
        **_base_flags(),
    }
    return attach_result_digest(result)
