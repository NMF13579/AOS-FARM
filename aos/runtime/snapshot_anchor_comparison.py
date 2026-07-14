from typing import Dict, Any

REQUIRED_FIELDS = {
    "repository_identity",
    "base_oid",
    "head_oid",
    "pr_state",
    "draft_state",
    "commit_set_fingerprint",
    "required_policy_fingerprint",
    "required_checks_fingerprint",
    "review_threads_fingerprint",
    "effective_reviews_fingerprint",
    "blocking_reviews_fingerprint",
    "rulesets_fingerprint",
    "protected_paths_fingerprint"
}

def compare_anchors(first_anchor: Dict[str, Any], revalidation_anchor: Dict[str, Any]) -> Dict[str, Any]:
    first_missing = REQUIRED_FIELDS - set(first_anchor.keys())
    reval_missing = REQUIRED_FIELDS - set(revalidation_anchor.keys())
    missing_fields = sorted(list(first_missing | reval_missing))
    
    if missing_fields:
        return {
            "stable": False,
            "changed_fields": [],
            "missing_fields": missing_fields,
            "unexpected_fields": [],
            "technical_status": "UNKNOWN",
            "reason_code": "SNAPSHOT_ANCHOR_INCOMPLETE"
        }
        
    first_unexpected = set(first_anchor.keys()) - REQUIRED_FIELDS
    reval_unexpected = set(revalidation_anchor.keys()) - REQUIRED_FIELDS
    unexpected_fields = sorted(list(first_unexpected | reval_unexpected))
    
    if unexpected_fields:
        return {
            "stable": False,
            "changed_fields": [],
            "missing_fields": [],
            "unexpected_fields": unexpected_fields,
            "technical_status": "FAIL",
            "reason_code": "SNAPSHOT_ANCHOR_SCHEMA_MISMATCH"
        }
        
    changed_fields = []
    for field in REQUIRED_FIELDS:
        if first_anchor[field] != revalidation_anchor[field]:
            changed_fields.append(field)
            
    if changed_fields:
        return {
            "stable": False,
            "changed_fields": sorted(changed_fields),
            "missing_fields": [],
            "unexpected_fields": [],
            "technical_status": "FAIL",
            "reason_code": "SNAPSHOT_ANCHOR_CHANGED"
        }
        
    return {
        "stable": True,
        "changed_fields": [],
        "missing_fields": [],
        "unexpected_fields": [],
        "technical_status": "PASS",
        "reason_code": None
    }
