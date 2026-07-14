from typing import Dict, Any, List
import copy

REQUIRED_GATES = {
    "pr_open", "pr_not_draft", "repository_identity_matches",
    "base_repository_identity_known", "head_repository_identity_known",
    "base_oid_matches", "head_oid_matches", "commit_set_complete",
    "required_checks_for_exact_head", "required_approvals_satisfied",
    "codeowner_requirements_satisfied", "unresolved_review_threads_zero",
    "blocking_reviews_zero", "conversation_resolution_policy_satisfied",
    "required_deployments_satisfied", "merge_queue_requirement_supported",
    "merge_method_allowed", "required_ruleset_state_known",
    "all_required_policy_types_supported", "pagination_complete",
    "protected_paths_changed_zero"
}

ALLOWED_STATUSES = {"PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE"}

def evaluate_readiness_gates(gates: List[Dict[str, Any]]) -> Dict[str, Any]:
    gates_input = copy.deepcopy(gates)
    
    provided_names = set()
    has_unknown = False
    has_fail = False
    reason_codes = set()
    
    gates_input.sort(key=lambda g: str(g.get("name", "")))
    
    for g in gates_input:
        name = g.get("name")
        status = g.get("status")
        required = g.get("required_for_operation")
        reason = g.get("reason_code")
        
        if name not in REQUIRED_GATES:
            raise ValueError(f"Unknown gate: {name}")
            
        if name in provided_names:
            raise ValueError(f"Duplicate gate: {name}")
            
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status: {status}")
            
        if type(required) is not bool:
            raise ValueError("required_for_operation must be a strict boolean")
            
        if status == "NOT_APPLICABLE" and required is True:
            raise ValueError(f"Gate {name} is required but marked NOT_APPLICABLE")
            
        provided_names.add(name)
        
        if required:
            if status == "FAIL":
                has_fail = True
            elif status == "UNKNOWN":
                has_unknown = True
                
        if reason:
            reason_codes.add(reason)
            
    missing = REQUIRED_GATES - provided_names
    if missing:
        has_unknown = True
        reason_codes.add("MISSING_REQUIRED_GATE")
        
    technical_status = "PASS"
    control_status = "HUMAN_REVIEW_REQUIRED"
    all_required_passed = True
    
    if has_fail:
        technical_status = "FAIL"
        control_status = "BLOCKED"
        all_required_passed = False
    elif has_unknown:
        technical_status = "UNKNOWN"
        control_status = "UNKNOWN_BLOCKED"
        all_required_passed = False
        
    return {
        "technical_status": technical_status,
        "control_status": control_status,
        "all_required_gates_passed": all_required_passed,
        "approval_granted": False,
        "execution_authorized": False,
        "reason_codes": sorted(list(reason_codes)),
        "gates": gates_input
    }
