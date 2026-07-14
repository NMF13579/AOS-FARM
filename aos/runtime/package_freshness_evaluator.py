import copy
from typing import Dict, Any

FORBIDDEN_FIELDS = {
    "timestamp",
    "local_path",
    "raw_error",
    "pagination_cursor",
    "verification_result",
    "human_preview",
    "approval",
    "execution_authorization"
}

def evaluate_package_freshness(
    package_id: str,
    package_decision_state: Dict[str, Any],
    current_stabilized_live_state: Dict[str, Any],
    selected_merge_method: str
) -> Dict[str, Any]:

    if not isinstance(package_id, str) or not package_id.startswith("sha256:"):
        return _unknown_res(package_id, ["PACKAGE_ID_INVALID"], set(), set())

    for f in FORBIDDEN_FIELDS:
        if f in package_decision_state:
            return _unknown_res(package_id, ["UNKNOWN_PACKAGE_STATE_FIELD"], set(), set())

    ds = package_decision_state
    ls = current_stabilized_live_state

    col = ls.get("collection_completeness", {})
    if col.get("commits_complete") is False or col.get("pagination_complete") is False:
        return _unknown_res(package_id, ["FRESHNESS_STATE_INCOMPLETE"], set(), set())

    if "commits" not in ls or "pull_request" not in ls:
        return _unknown_res(package_id, ["FRESHNESS_STATE_INCOMPLETE"], set(), set())

    reasons = set()
    changed_fields = set()
    unknown_fields = set()

    def add_reason(reason: str, field: str):
        if reason:
            reasons.add(reason)
        changed_fields.add(field)

    def add_unknown(reason: str, field: str):
        if reason:
            reasons.add(reason)
        unknown_fields.add(field)

    # 1. Repository identity
    r1 = ds.get("repository_identity")
    r2 = ls.get("repository_identity")
    # Handle both string and dictionary for backwards compatibility
    r1_val = r1.get("id") if isinstance(r1, dict) else r1
    r2_val = r2.get("id") if isinstance(r2, dict) else r2
    if r1_val != r2_val:
        add_reason("REPOSITORY_IDENTITY_CHANGED", "repository_identity")

    # 2. PR
    p1 = ds.get("pull_request", {})
    p2 = ls.get("pull_request", {})
    if p1.get("repository_id") != p2.get("repository_id") or p1.get("number") != p2.get("number"):
        add_reason("PULL_REQUEST_IDENTITY_CHANGED", "pull_request")

    # 3. Base/Head OID
    if p1.get("base_oid") != p2.get("base_oid"):
        add_reason("BASE_OID_CHANGED", "pull_request")
    if p1.get("head_oid") != p2.get("head_oid"):
        add_reason("HEAD_OID_CHANGED", "pull_request")

    # 4. Commit set
    c1 = ds.get("commits", {})
    c2 = ls.get("commits", {})
    if c1 != c2:
        add_reason("COMMIT_SET_CHANGED", "commits")

    # 5. Changed paths
    cp1 = sorted(ds.get("changed_paths", {}).get("items", []))
    cp2 = sorted(ls.get("changed_paths", {}).get("items", []))
    if cp1 != cp2:
        add_reason("CHANGED_PATHS_CHANGED", "changed_paths")

    # 6. Protected path result
    pp1 = ds.get("protected_path_result", {})
    pp2 = ls.get("protected_path_result", {})
    if pp1 != pp2:
        add_reason("PROTECTED_PATH_RESULT_CHANGED", "protected_path_result")

    # 7. Required checks
    chk1 = {c["name"]: c for c in ds.get("required_checks", {}).get("items", [])}
    chk2 = {c["name"]: c for c in ls.get("required_checks", {}).get("items", [])}
    if chk1 != chk2:
        add_reason("REQUIRED_CHECK_STATE_CHANGED", "required_checks")

    # 8. Required approvals
    pol1 = ds.get("required_review_policy", {})
    pol2 = ls.get("required_review_policy", {})
    if pol1 != pol2:
        add_reason("REQUIRED_APPROVAL_STATE_CHANGED", "required_review_policy")

    # 9. Effective reviews
    rev1 = ds.get("reviews", {})
    rev2 = ls.get("reviews", {})
    if rev1 != rev2:
        add_reason("REVIEW_STATE_CHANGED", "reviews")

    # 10. Review threads
    th1 = ds.get("review_threads", {})
    th2 = ls.get("review_threads", {})
    if th1 != th2:
        add_reason("REVIEW_THREAD_STATE_CHANGED", "review_threads")

    # 11. Codeowner state
    co1 = ds.get("codeowner_state", {})
    co2 = ls.get("codeowner_state", {})
    if co1 != co2:
        add_reason("REVIEW_STATE_CHANGED", "codeowner_state")

    # 12. Rulesets
    rs1 = ds.get("rulesets", {})
    rs2 = ls.get("rulesets", {})
    if rs1 != rs2:
        add_reason("RULESET_STATE_CHANGED", "rulesets")
        if rs2.get("unsupported_type"):
            add_unknown("UNSUPPORTED_REQUIRED_POLICY", "rulesets")

    # 13. Branch protection
    bp1 = ds.get("branch_protection", {})
    bp2 = ls.get("branch_protection", {})
    if bp1 != bp2:
        add_reason("BRANCH_PROTECTION_STATE_CHANGED", "branch_protection")
        if bp2.get("unsupported_type"):
            add_unknown("UNSUPPORTED_REQUIRED_POLICY", "branch_protection")

    # 14. Merge queue
    mq1 = ds.get("merge_queue", {})
    mq2 = ls.get("merge_queue", {})
    if mq1 != mq2:
        add_reason("MERGE_QUEUE_STATE_CHANGED", "merge_queue")

    # 15. Required deployments
    dp1 = ds.get("required_deployments", {})
    dp2 = ls.get("required_deployments", {})
    if dp1 != dp2:
        add_reason("DEPLOYMENT_STATE_CHANGED", "required_deployments")

    # 16. Allowed merge methods
    allowed = bp2.get("allowed_merge_methods")
    if allowed is not None and selected_merge_method not in allowed:
        add_reason("MERGE_METHOD_NO_LONGER_ALLOWED", "branch_protection")

    # 17. Collection completeness
    cc1 = ds.get("collection_completeness", {})
    cc2 = ls.get("collection_completeness", {})
    if cc1 != cc2:
        add_reason("COLLECTION_COMPLETENESS_CHANGED", "collection_completeness")

    if not reasons and ds != ls:
        for k in set(ds.keys()) | set(ls.keys()):
            if ds.get(k) != ls.get(k):
                add_reason("AUTHORIZATION_PACKAGE_STALE", k)

    if unknown_fields:
        return _unknown_res(package_id, reasons, changed_fields, unknown_fields)

    if reasons or changed_fields:
        reasons.add("AUTHORIZATION_PACKAGE_STALE")
        return _fail_res(package_id, reasons, changed_fields)

    return {
        "schema_version": 1,
        "package_id": package_id,
        "technical_status": "PASS",
        "integrity_status": "NOT_RUN",
        "freshness_status": "PASS",
        "control_status": "HUMAN_REVIEW_REQUIRED",
        "changed_fields": [],
        "unknown_fields": [],
        "reason_codes": [],
        "approval_granted": False,
        "execution_authorized": False,
        "github_remote_mutation_performed": False,
        "protected_operation_performed": False
    }

def _unknown_res(package_id, reasons, changed, unknown):
    return {
        "schema_version": 1,
        "package_id": package_id,
        "technical_status": "UNKNOWN",
        "integrity_status": "NOT_RUN",
        "freshness_status": "UNKNOWN",
        "control_status": "UNKNOWN_BLOCKED",
        "changed_fields": sorted(list(changed)),
        "unknown_fields": sorted(list(unknown)),
        "reason_codes": sorted(list(reasons)),
        "approval_granted": False,
        "execution_authorized": False,
        "github_remote_mutation_performed": False,
        "protected_operation_performed": False
    }

def _fail_res(package_id, reasons, changed):
    return {
        "schema_version": 1,
        "package_id": package_id,
        "technical_status": "FAIL",
        "integrity_status": "NOT_RUN",
        "freshness_status": "FAIL",
        "control_status": "BLOCKED",
        "changed_fields": sorted(list(changed)),
        "unknown_fields": [],
        "reason_codes": sorted(list(reasons)),
        "approval_granted": False,
        "execution_authorized": False,
        "github_remote_mutation_performed": False,
        "protected_operation_performed": False
    }
