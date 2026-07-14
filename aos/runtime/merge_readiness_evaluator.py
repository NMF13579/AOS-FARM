from typing import Dict, Any
from aos.runtime.merge_readiness_contracts import evaluate_readiness_gates
import copy

def _gate(name: str, status: str, req: bool = True) -> Dict[str, Any]:
    return {
        "name": name,
        "status": status,
        "required_for_operation": req,
        "reason_code": None,
        "evidence_reference": ""
    }

def evaluate_stabilized_snapshot(
    stabilized_snapshot: Dict[str, Any],
    intent: Dict[str, Any],
    protected_path_policy: Dict[str, Any]
) -> Dict[str, Any]:
    # Ensure inputs are not mutated
    snapshot = copy.deepcopy(stabilized_snapshot)
    
    pr = snapshot.get("pull_request", {})
    completeness = snapshot.get("collection_completeness", {})
    
    gates = []
    
    # 4.1 PR state
    state = pr.get("state")
    if state == "OPEN":
        gates.append(_gate("pr_open", "PASS"))
    elif state is None:
        gates.append(_gate("pr_open", "UNKNOWN"))
    else:
        gates.append(_gate("pr_open", "FAIL"))
        
    draft = pr.get("is_draft")
    if draft is False:
        gates.append(_gate("pr_not_draft", "PASS"))
    elif draft is True:
        gates.append(_gate("pr_not_draft", "FAIL"))
    else:
        gates.append(_gate("pr_not_draft", "UNKNOWN"))
        
    # 4.2 Repositories
    repo = snapshot.get("repository_identity")
    intent_repo = intent.get("repository")
    if not repo or not intent_repo:
        gates.append(_gate("repository_identity_matches", "UNKNOWN"))
    elif repo == intent_repo:
        gates.append(_gate("repository_identity_matches", "PASS"))
    else:
        gates.append(_gate("repository_identity_matches", "FAIL"))
        
    base_repo = pr.get("base_repository_identity")
    if base_repo:
        gates.append(_gate("base_repository_identity_known", "PASS"))
    else:
        gates.append(_gate("base_repository_identity_known", "UNKNOWN"))
        
    head_repo = pr.get("head_repository_identity")
    if head_repo:
        gates.append(_gate("head_repository_identity_known", "PASS"))
    else:
        gates.append(_gate("head_repository_identity_known", "UNKNOWN"))
        
    # OIDs
    head_oid = pr.get("head_oid")
    expected_head = intent.get("expected_head_oid")
    if expected_head:
        if not head_oid:
            gates.append(_gate("head_oid_matches", "UNKNOWN"))
        elif head_oid == expected_head:
            gates.append(_gate("head_oid_matches", "PASS"))
        else:
            gates.append(_gate("head_oid_matches", "FAIL"))
    else:
        gates.append(_gate("head_oid_matches", "NOT_APPLICABLE", req=False))
        
    base_oid = pr.get("base_oid")
    expected_base = intent.get("expected_base_oid")
    if expected_base:
        if not base_oid:
            gates.append(_gate("base_oid_matches", "UNKNOWN"))
        elif base_oid == expected_base:
            gates.append(_gate("base_oid_matches", "PASS"))
        else:
            gates.append(_gate("base_oid_matches", "FAIL"))
    else:
        gates.append(_gate("base_oid_matches", "NOT_APPLICABLE", req=False))
        
    # 4.3 Commits
    commits_data = snapshot.get("commits", {})
    if not completeness.get("commits_complete"):
        gates.append(_gate("commit_set_complete", "UNKNOWN"))
    elif commits_data.get("truncated") or commits_data.get("duplicate"):
        gates.append(_gate("commit_set_complete", "UNKNOWN"))
    elif not commits_data.get("items"):
        gates.append(_gate("commit_set_complete", "UNKNOWN"))
    else:
        gates.append(_gate("commit_set_complete", "PASS"))
        
    if completeness.get("pagination_complete"):
        gates.append(_gate("pagination_complete", "PASS"))
    else:
        gates.append(_gate("pagination_complete", "UNKNOWN"))
        
    # 4.4 Required checks
    checks = snapshot.get("required_checks", {})
    if not head_oid or checks.get("policy_unknown"):
        gates.append(_gate("required_checks_for_exact_head", "UNKNOWN"))
    else:
        check_status = "PASS"
        for check in checks.get("items", []):
            if check.get("head_oid") != head_oid:
                continue
            c_state = check.get("state")
            if c_state in ("PENDING", "MISSING", "FAILURE", "FAIL"):
                check_status = "FAIL"
                break
        gates.append(_gate("required_checks_for_exact_head", check_status))
        
    # 4.5 Reviews
    policy = snapshot.get("required_review_policy", {})
    reviews = snapshot.get("reviews", {})
    if policy.get("unknown") or reviews.get("unresolved_state"):
        gates.append(_gate("required_approvals_satisfied", "UNKNOWN"))
    else:
        req_count = policy.get("required_approvals", 0)
        actual_count = reviews.get("approval_count", 0)
        if actual_count >= req_count:
            gates.append(_gate("required_approvals_satisfied", "PASS"))
        else:
            gates.append(_gate("required_approvals_satisfied", "FAIL"))
            
    blocking = reviews.get("blocking_count")
    if blocking is None:
        gates.append(_gate("blocking_reviews_zero", "UNKNOWN"))
    elif blocking > 0:
        gates.append(_gate("blocking_reviews_zero", "FAIL"))
    else:
        gates.append(_gate("blocking_reviews_zero", "PASS"))
        
    # 4.6 Codeowners
    co = snapshot.get("codeowner_state", {})
    if co.get("unknown") or not co:
        gates.append(_gate("codeowner_requirements_satisfied", "UNKNOWN"))
    elif co.get("satisfied"):
        gates.append(_gate("codeowner_requirements_satisfied", "PASS"))
    elif co.get("unsatisfied"):
        gates.append(_gate("codeowner_requirements_satisfied", "FAIL"))
    else:
        gates.append(_gate("codeowner_requirements_satisfied", "UNKNOWN"))
        
    # 4.7 Threads
    threads = snapshot.get("review_threads", {})
    if threads.get("incomplete") or threads.get("unavailable"):
        gates.append(_gate("unresolved_review_threads_zero", "UNKNOWN"))
    else:
        unresolved = threads.get("unresolved_count")
        if unresolved is None:
            gates.append(_gate("unresolved_review_threads_zero", "UNKNOWN"))
        elif unresolved > 0:
            gates.append(_gate("unresolved_review_threads_zero", "FAIL"))
        else:
            gates.append(_gate("unresolved_review_threads_zero", "PASS"))
            
    if policy.get("unknown"):
        gates.append(_gate("conversation_resolution_policy_satisfied", "UNKNOWN"))
    elif policy.get("conversation_resolution_required"):
        unres = threads.get("unresolved_count")
        if unres is None:
            gates.append(_gate("conversation_resolution_policy_satisfied", "UNKNOWN"))
        elif unres > 0:
            gates.append(_gate("conversation_resolution_policy_satisfied", "FAIL"))
        else:
            gates.append(_gate("conversation_resolution_policy_satisfied", "PASS"))
    else:
        gates.append(_gate("conversation_resolution_policy_satisfied", "NOT_APPLICABLE", req=False))
        
    # 4.9 Deployments
    deps = snapshot.get("required_deployments", {})
    if deps.get("unknown"):
        gates.append(_gate("required_deployments_satisfied", "UNKNOWN"))
    elif deps.get("required"):
        if deps.get("satisfied"):
            gates.append(_gate("required_deployments_satisfied", "PASS"))
        else:
            gates.append(_gate("required_deployments_satisfied", "FAIL"))
    else:
        gates.append(_gate("required_deployments_satisfied", "NOT_APPLICABLE", req=False))
        
    # 4.9 Merge Queue
    mq = snapshot.get("merge_queue", {})
    if mq.get("unknown"):
        gates.append(_gate("merge_queue_requirement_supported", "UNKNOWN"))
    elif mq.get("required"):
        if mq.get("supported"):
            gates.append(_gate("merge_queue_requirement_supported", "PASS"))
        else:
            gates.append(_gate("merge_queue_requirement_supported", "FAIL"))
    else:
        gates.append(_gate("merge_queue_requirement_supported", "NOT_APPLICABLE", req=False))
        
    # Merge method
    method = intent.get("merge_method")
    bp = snapshot.get("branch_protection", {})
    allowed_methods = bp.get("allowed_merge_methods")
    if not method or allowed_methods is None:
        gates.append(_gate("merge_method_allowed", "UNKNOWN"))
    elif method in allowed_methods:
        gates.append(_gate("merge_method_allowed", "PASS"))
    else:
        gates.append(_gate("merge_method_allowed", "FAIL"))
        
    # 4.8 Rulesets and policy
    rulesets = snapshot.get("rulesets", {})
    if rulesets.get("unknown_policy") or bp.get("unknown_policy"):
        gates.append(_gate("required_ruleset_state_known", "UNKNOWN"))
    else:
        status_ruleset = "PASS"
        if rulesets.get("policy_violation") or bp.get("policy_violation"):
            status_ruleset = "FAIL"
        gates.append(_gate("required_ruleset_state_known", status_ruleset))
        
    if rulesets.get("unsupported_type") or bp.get("unsupported_type"):
        gates.append(_gate("all_required_policy_types_supported", "UNKNOWN"))
    else:
        gates.append(_gate("all_required_policy_types_supported", "PASS"))
        
    # 4.10 Protected paths
    pol = protected_path_policy.get("normalized_paths")
    changed = snapshot.get("changed_paths", {})
    if pol is None or changed.get("incomplete"):
        gates.append(_gate("protected_paths_changed_zero", "UNKNOWN"))
    else:
        items = changed.get("items", [])
        protected_changed = sum(1 for p in items if p in pol)
        if protected_changed > 0:
            gates.append(_gate("protected_paths_changed_zero", "FAIL"))
        else:
            gates.append(_gate("protected_paths_changed_zero", "PASS"))

    return evaluate_readiness_gates(gates)
