import copy
from typing import Dict, Any

def _check_contradictions(res: Dict[str, Any], is_integrity: bool = False, is_freshness: bool = False) -> bool:
    tech = res.get("technical_status")
    ctrl = res.get("control_status")
    
    if res.get("approval_granted") is True:
        return True
    if res.get("execution_authorized") is True:
        return True
        
    if tech == "PASS" and ctrl != "HUMAN_REVIEW_REQUIRED":
        return True
    if tech == "FAIL" and ctrl != "BLOCKED":
        return True
    if tech == "UNKNOWN" and ctrl != "UNKNOWN_BLOCKED":
        return True
        
    if is_integrity:
        i_stat = res.get("integrity_status")
        if tech == "PASS" and i_stat != "PASS":
            return True
        if i_stat == "FAIL" and tech != "FAIL":
            return True
    
    if is_freshness:
        f_stat = res.get("freshness_status")
        if tech == "PASS" and f_stat != "PASS":
            return True
        if f_stat == "FAIL" and tech != "FAIL":
            return True

    return False

def build_unified_verification_result(
    package_id: str,
    integrity_result: Dict[str, Any],
    freshness_result: Dict[str, Any]
) -> Dict[str, Any]:

    if not isinstance(package_id, str) or not package_id.startswith("sha256:"):
        return _fail_res(package_id, ["VERIFICATION_RESULT_CONTRACT_VIOLATION"])

    id_i = integrity_result.get("package_id")
    id_f = freshness_result.get("package_id")
    if id_i != package_id or id_f != package_id:
        return _fail_res(package_id, ["VERIFICATION_PACKAGE_ID_MISMATCH"])

    if _check_contradictions(integrity_result, is_integrity=True) or \
       _check_contradictions(freshness_result, is_freshness=True):
        return _fail_res(package_id, ["VERIFICATION_RESULT_CONTRACT_VIOLATION"])

    tech_i = integrity_result.get("technical_status", "NOT_RUN")
    tech_f = freshness_result.get("technical_status", "NOT_RUN")
    stat_i = integrity_result.get("integrity_status", "NOT_RUN")
    stat_f = freshness_result.get("freshness_status", "NOT_RUN")
    
    reasons_i = integrity_result.get("reason_codes", [])
    reasons_f = freshness_result.get("reason_codes", [])
    
    all_reasons = set(reasons_i) | set(reasons_f)
    
    has_fail = False
    has_unknown = False
    has_not_run = False
    
    if tech_i == "FAIL" or tech_f == "FAIL" or stat_i == "FAIL" or stat_f == "FAIL":
        has_fail = True
    if tech_i == "UNKNOWN" or tech_f == "UNKNOWN" or stat_i == "UNKNOWN" or stat_f == "UNKNOWN":
        has_unknown = True
    if stat_i == "NOT_RUN" or stat_f == "NOT_RUN":
        has_not_run = True

    if stat_i == "FAIL":
        all_reasons.add("INTEGRITY_VERIFICATION_FAILED")
    elif stat_i == "UNKNOWN":
        all_reasons.add("INTEGRITY_VERIFICATION_UNKNOWN")
        
    if stat_f == "FAIL":
        all_reasons.add("FRESHNESS_VERIFICATION_FAILED")
    elif stat_f == "UNKNOWN":
        all_reasons.add("FRESHNESS_VERIFICATION_UNKNOWN")

    if has_not_run:
        all_reasons.add("REQUIRED_VERIFICATION_NOT_RUN")

    if has_fail:
        final_tech = "FAIL"
        final_ctrl = "BLOCKED"
    elif has_unknown or has_not_run:
        final_tech = "UNKNOWN"
        final_ctrl = "UNKNOWN_BLOCKED"
    else:
        final_tech = "PASS"
        final_ctrl = "HUMAN_REVIEW_REQUIRED"

    changed = set(freshness_result.get("changed_fields", []))
    unknown = set(freshness_result.get("unknown_fields", []))
    
    return {
        "schema_version": 1,
        "package_id": package_id,
        "technical_status": final_tech,
        "integrity_status": stat_i,
        "freshness_status": stat_f,
        "control_status": final_ctrl,
        "integrity_reason_codes": sorted(list(set(reasons_i))),
        "freshness_reason_codes": sorted(list(set(reasons_f))),
        "reason_codes": sorted(list(all_reasons)),
        "changed_fields": sorted(list(changed)),
        "unknown_fields": sorted(list(unknown)),
        "approval_granted": False,
        "execution_authorized": False,
        "github_remote_mutation_performed": False,
        "protected_operation_performed": False
    }

def _fail_res(package_id: str, reasons: list) -> Dict[str, Any]:
    return {
        "schema_version": 1,
        "package_id": package_id,
        "technical_status": "FAIL",
        "integrity_status": "NOT_RUN",
        "freshness_status": "NOT_RUN",
        "control_status": "BLOCKED",
        "integrity_reason_codes": [],
        "freshness_reason_codes": [],
        "reason_codes": sorted(list(set(reasons))),
        "changed_fields": [],
        "unknown_fields": [],
        "approval_granted": False,
        "execution_authorized": False,
        "github_remote_mutation_performed": False,
        "protected_operation_performed": False
    }
