import re
from typing import Dict, Any, List

def _contains_forbidden_content(obj: Any) -> bool:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() == "authorization" or k.lower() == "token" or k.lower() == "password":
                return True
            if _contains_forbidden_content(v):
                return True
    elif isinstance(obj, list):
        for item in obj:
            if _contains_forbidden_content(item):
                return True
    elif isinstance(obj, str):
        # Look for absolute local paths, rudimentary check
        # We don't want to block valid branch names like "foo/bar", but absolute paths like "/var" or "/usr"
        if obj.startswith("/Users/") or obj.startswith("/tmp/") or obj.startswith("/var/") or obj.startswith("/etc/"):
            return True
        if "authorization: " in obj.lower() or "bearer " in obj.lower():
            return True
    return False

def render_human_preview(
    package_id: str,
    package_core: Dict[str, Any],
    merge_readiness_result: Dict[str, Any],
    verification_result: Dict[str, Any]
) -> Dict[str, Any]:

    def _fail(reason: str) -> Dict[str, Any]:
        return {
            "schema_version": 1,
            "package_id": package_id,
            "markdown": None,
            "technical_status": "FAIL",
            "control_status": "BLOCKED",
            "reason_codes": [reason],
            "approval_granted": False,
            "execution_authorized": False
        }

    # 1. Package ID mismatch
    if package_core.get("package_id") and package_core.get("package_id") != package_id:
        return _fail("PREVIEW_INPUT_CONTRACT_VIOLATION")
    if merge_readiness_result.get("package_id") and merge_readiness_result.get("package_id") != package_id:
        return _fail("PREVIEW_INPUT_CONTRACT_VIOLATION")
    if verification_result.get("package_id") != package_id:
        return _fail("PREVIEW_INPUT_CONTRACT_VIOLATION")

    # 2. Top-level unknowns / missing
    # Actually, we should check if verification_result has required fields.
    if "technical_status" not in verification_result or "control_status" not in verification_result:
        return _fail("PREVIEW_INPUT_CONTRACT_VIOLATION")

    # 4 & 5. Approval/Execution granted
    if package_core.get("approval_granted") is True or verification_result.get("approval_granted") is True:
        return _fail("PREVIEW_INPUT_CONTRACT_VIOLATION")
    if package_core.get("execution_authorized") is True or verification_result.get("execution_authorized") is True:
        return _fail("PREVIEW_INPUT_CONTRACT_VIOLATION")

    # 6. Verification PASS when integrity/freshness is not PASS
    if verification_result.get("technical_status") == "PASS":
        if verification_result.get("integrity_status") != "PASS" or verification_result.get("freshness_status") != "PASS":
            return _fail("PREVIEW_INPUT_CONTRACT_VIOLATION")

    # 7 & 8. Forbidden content
    if _contains_forbidden_content(package_core) or _contains_forbidden_content(verification_result):
        return _fail("PREVIEW_INPUT_CONTRACT_VIOLATION")

    ds = package_core.get("decision_state", {})
    if not isinstance(ds, dict):
        return _fail("PREVIEW_INPUT_CONTRACT_VIOLATION")

    # Extract required fields for markdown
    try:
        operation = package_core.get("operation", "UNKNOWN")
        repo = ds.get("repository_identity", {}).get("name", "UNKNOWN")
        pr = ds.get("pull_request", {})
        pr_number = pr.get("number", "UNKNOWN")
        base_oid = pr.get("base_oid", "UNKNOWN")
        head_oid = pr.get("head_oid", "UNKNOWN")

        commits = ds.get("commits", {}).get("items", [])
        commit_count = len(commits)

        changed_paths = ds.get("changed_paths", {}).get("items", [])
        changed_file_count = len(changed_paths)

        protected_paths = ds.get("protected_path_result", {}).get("items", [])

        req_checks = ds.get("required_checks", {}).get("items", [])
        passed_c = sum(1 for c in req_checks if c.get("state") == "PASS")
        pending_c = sum(1 for c in req_checks if c.get("state") == "PENDING")
        failing_c = sum(1 for c in req_checks if c.get("state") in ("FAILURE", "FAIL", "ERROR"))
        missing_c = sum(1 for c in req_checks if c.get("state") == "MISSING")

        req_approvals = ds.get("required_review_policy", {}).get("required_approvals", "UNKNOWN")
        obs_approvals = ds.get("reviews", {}).get("approval_count", "UNKNOWN")
        blocking_reviews = ds.get("reviews", {}).get("blocking_count", "UNKNOWN")
        unres_threads = ds.get("review_threads", {}).get("unresolved_count", "UNKNOWN")

        co_state = ds.get("codeowner_state", {})
        co_status = "SATISFIED" if co_state.get("satisfied") else ("UNSATISFIED" if co_state.get("unsatisfied") else "UNKNOWN")

        merge_method = package_core.get("exact_merge_parameters", {}).get("merge_method", "UNKNOWN")

        rulesets = ds.get("rulesets", {})
        rs_status = "UNKNOWN" if rulesets.get("unknown_policy") else ("FAIL" if rulesets.get("policy_violation") else "PASS")

        forbidden = sorted(package_core.get("forbidden_actions", []))

        int_status = verification_result.get("integrity_status", "UNKNOWN")
        fre_status = verification_result.get("freshness_status", "UNKNOWN")
        tech_status = verification_result.get("technical_status", "UNKNOWN")
        ctrl_status = verification_result.get("control_status", "UNKNOWN")

        unknowns = sorted(verification_result.get("unknown_fields", []))
        not_run_items = "REQUIRED_VERIFICATION_NOT_RUN" in verification_result.get("reason_codes", [])
    except Exception:
        return _fail("PREVIEW_INPUT_CONTRACT_VIOLATION")

    # Build Markdown
    lines = []
    lines.append(f"# Authorization Package Preview")
    lines.append(f"**Package ID:** `{package_id}`")
    lines.append(f"**Operation:** {operation}")
    lines.append(f"**Repository:** {repo}")
    lines.append(f"**Pull Request:** #{pr_number}")
    lines.append(f"**Base OID:** `{base_oid}`")
    lines.append(f"**Head OID:** `{head_oid}`")
    lines.append("")

    lines.append(f"## Status")
    lines.append(f"- Technical status: **{tech_status}**")
    lines.append(f"- Integrity status: **{int_status}**")
    lines.append(f"- Freshness status: **{fre_status}**")
    lines.append(f"- Control status: **{ctrl_status}**")
    lines.append(f"- Approval granted: **false**")
    lines.append(f"- Execution authorized: **false**")
    lines.append("")

    lines.append(f"## Content Summary")
    lines.append(f"- Commits: {commit_count}")
    lines.append(f"- Changed files: {changed_file_count}")

    lines.append("")
    lines.append(f"### Protected Paths")
    if not protected_paths:
        lines.append("No protected paths changed.")
    else:
        lines.append(f"{len(protected_paths)} protected paths changed:")
        display_limit = 5
        for p in sorted(protected_paths)[:display_limit]:
            lines.append(f"- `{p}`")
        if len(protected_paths) > display_limit:
            lines.append(f"- ... and {len(protected_paths) - display_limit} more")

    lines.append("")
    lines.append(f"## Checks & Reviews")
    lines.append(f"- Required checks: {len(req_checks)} (Passed: {passed_c}, Pending: {pending_c}, Failing: {failing_c}, Missing: {missing_c})")
    lines.append(f"- Required approvals: {req_approvals}")
    lines.append(f"- Observed approvals: {obs_approvals}")
    lines.append(f"- Blocking reviews: {blocking_reviews}")
    lines.append(f"- Unresolved review threads: {unres_threads}")
    lines.append(f"- Codeowner status: {co_status}")
    lines.append(f"- Ruleset status: {rs_status}")
    lines.append("")

    lines.append(f"## Merge Parameters")
    lines.append(f"- Merge method: {merge_method}")
    lines.append("")

    lines.append(f"## Security Constraints")
    lines.append(f"Forbidden actions:")
    for f in forbidden:
        lines.append(f"- {f}")

    if unknowns:
        lines.append("")
        lines.append(f"## Unknowns")
        for u in unknowns:
            lines.append(f"- {u}")

    if not_run_items:
        lines.append("")
        lines.append(f"## Not Run Items")
        lines.append(f"- REQUIRED_VERIFICATION_NOT_RUN")

    return {
        "schema_version": 1,
        "package_id": package_id,
        "markdown": "\n".join(lines),
        "technical_status": "PASS",
        "control_status": "HUMAN_REVIEW_REQUIRED",
        "reason_codes": [],
        "approval_granted": False,
        "execution_authorized": False
    }
