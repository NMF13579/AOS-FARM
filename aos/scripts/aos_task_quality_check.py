import sys
import json
import argparse
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from aos.scripts.aos_semantic_guard import collect_semantic_guard_violations

def check_task_quality(package_path):
    result = {
        "package": package_path,
        "status": "TASK_QUALITY_FUNCTIONAL_INTENT_BLOCKED",
        "warnings": [],
        "blocked_reasons": [],
        "approval_granted": False,
        "commit_authorized": False,
        "push_authorized": False,
        "merge_authorized": False,
        "release_authorized": False,
        "schema_required_fields_present": False,
        "functional_intent_present": False,
        "functional_intent_valid": False,
        "verification_status": None,
        "verification_method": None,
        "declared_purpose_present": False,
        "forbidden_behaviors_present": False,
        "human_review_required": False
    }

    if not os.path.exists(package_path):
        result["blocked_reasons"].append(f"Package file not found: {package_path}")
        return result

    try:
        with open(package_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        result["blocked_reasons"].append(f"Invalid JSON: {str(e)}")
        return result

    if not isinstance(data, dict):
        result["blocked_reasons"].append("Root element must be a JSON object")
        return result

    semantic_violations = collect_semantic_guard_violations(data)
    if semantic_violations:
        result["blocked_reasons"].extend(semantic_violations)

    result["schema_required_fields_present"] = True

    if data.get("non_authority_boundary", {}).get("task_quality_pass_is_not_human_result_acceptance") is False:
        result["blocked_reasons"].append("non_authority_boundary.task_quality_pass_is_not_human_result_acceptance must not be false")

    if data.get("human_review_required") is False:
        result["blocked_reasons"].append("human_review_required must not be false")
    else:
        result["human_review_required"] = data.get("human_review_required", False)

    functional_intent = data.get("functional_intent")
    if functional_intent:
        result["functional_intent_present"] = True
        if not isinstance(functional_intent, dict):
            result["blocked_reasons"].append("functional_intent must be an object")
        else:
            declared_purpose = functional_intent.get("declared_purpose")
            if not declared_purpose:
                result["blocked_reasons"].append("functional_intent.declared_purpose is empty or missing")
            else:
                result["declared_purpose_present"] = True

            forbidden_behaviors = functional_intent.get("forbidden_behaviors", [])
            if not forbidden_behaviors:
                result["warnings"].append("functional_intent.forbidden_behaviors is empty")
            else:
                result["forbidden_behaviors_present"] = True

            v_status = functional_intent.get("verification_status")
            if v_status:
                result["verification_status"] = v_status
                if v_status == "NOT_RUN":
                    result["blocked_reasons"].append("functional_intent.verification_status is NOT_RUN")

            v_method = functional_intent.get("verification_method")
            if v_method:
                result["verification_method"] = v_method

            if v_method == "not_verified" and v_status == "VERIFIED":
                result["blocked_reasons"].append("functional_intent.verification_method not_verified cannot produce verification_status VERIFIED")

            if result["declared_purpose_present"]:
                result["functional_intent_valid"] = True
    else:
        result["warnings"].append("functional_intent is missing (optional but recommended)")

    # evidence check just in case
    evidence = data.get("evidence", [])
    if isinstance(evidence, list):
        has_verified = False
        has_not_verified = False

        for ev in evidence:
            st = ev.get("status")
            if st == "VERIFIED":
                has_verified = True
            elif st == "NOT_RUN":
                result["blocked_reasons"].append(f"Evidence {ev.get('criterion_id')} is NOT_RUN")
            elif st == "not_verified":
                has_not_verified = True

        if has_not_verified and has_verified:
            result["blocked_reasons"].append("Mixed VERIFIED and not_verified states found in evidence; this is blocked.")

    if result["blocked_reasons"]:
        result["status"] = "TASK_QUALITY_FUNCTIONAL_INTENT_BLOCKED"
        result["message"] = "Validation failed."
    else:
        if result["functional_intent_present"]:
            result["status"] = "TASK_QUALITY_FUNCTIONAL_INTENT_REPORTED_HUMAN_REVIEW_REQUIRED"
        else:
            result["status"] = "FUNCTIONAL_INTENT_MISSING_HUMAN_REVIEW_REQUIRED"
        result["message"] = "Validator check passed. Commit, push, merge, release, or approval are NOT authorized by this script. Explicit human execution authorization and review is still required."

    return result

def check_forbidden_evidence_mapping(mapping_path):
    result = {
        "mapping": mapping_path,
        "status": "FORBIDDEN_EVIDENCE_MAPPING_BLOCKED",
        "blocked_reasons": [],
        "approval_granted": False,
        "commit_authorized": False,
        "push_authorized": False,
        "merge_authorized": False,
        "release_authorized": False,
        "human_review_required": True
    }

    if not os.path.exists(mapping_path):
        result["blocked_reasons"].append(f"Mapping file not found: {mapping_path}")
        return result

    try:
        with open(mapping_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        result["status"] = "FORBIDDEN_EVIDENCE_MAPPING_SCHEMA_INVALID"
        result["blocked_reasons"].append(f"Invalid JSON: {str(e)}")
        return result

    if not isinstance(data, dict):
        result["status"] = "FORBIDDEN_EVIDENCE_MAPPING_SCHEMA_INVALID"
        result["blocked_reasons"].append("Root element must be a JSON object")
        return result

    if not data.get("schema_version"):
        result["blocked_reasons"].append("schema_version missing")
    if not data.get("task_id"):
        result["blocked_reasons"].append("task_id missing")
    if not data.get("related_quality_package"):
        result["blocked_reasons"].append("related_quality_package missing")

    mappings = data.get("forbidden_behavior_evidence_mappings")
    if mappings is None:
        result["blocked_reasons"].append("forbidden_behavior_evidence_mappings missing")
    elif not isinstance(mappings, list):
        result["blocked_reasons"].append("forbidden_behavior_evidence_mappings must be an array")
    elif len(mappings) == 0:
        result["blocked_reasons"].append("forbidden_behavior_evidence_mappings is empty")
    else:
        for m in mappings:
            if not isinstance(m, dict):
                result["blocked_reasons"].append("mapping item must be an object")
                continue
            if not m.get("evidence_items"):
                result["blocked_reasons"].append("evidence_items missing or empty in mapping")
            v_status = m.get("verification_status")
            if not v_status:
                result["blocked_reasons"].append("verification_status missing in mapping")
            elif v_status == "NOT_RUN":
                result["blocked_reasons"].append("verification_status NOT_RUN is explicit but blocked from PASS")
            elif v_status == "UNKNOWN":
                if not m.get("human_review_required"):
                    result["blocked_reasons"].append("UNKNOWN requires human_review_required true")

    if not data.get("approval_boundary"):
        result["blocked_reasons"].append("approval_boundary missing")

    final_status = data.get("final_status")
    if final_status == "APPROVED":
        result["blocked_reasons"].append("final_status cannot be APPROVED")

    for f in ["approval_granted", "commit_authorized", "push_authorized", "merge_authorized", "release_authorized"]:
        if data.get(f) is True:
            result["blocked_reasons"].append(f"{f} cannot be true")

    if result["blocked_reasons"]:
        if any("UNKNOWN" in r for r in result["blocked_reasons"]):
            result["status"] = "FORBIDDEN_EVIDENCE_MAPPING_UNKNOWN_BLOCKED"
        elif result["status"] != "FORBIDDEN_EVIDENCE_MAPPING_SCHEMA_INVALID":
             result["status"] = "FORBIDDEN_EVIDENCE_MAPPING_BLOCKED"
    else:
        result["status"] = "FORBIDDEN_EVIDENCE_MAPPING_VALID_HUMAN_REVIEW_REQUIRED"

    return result


def check_result_acceptance(result_path):
    """Validate a Task Execution Result Acceptance Package.

    Checks structural and binary facts only.
    Does NOT check semantic correctness, implementation quality,
    or whether the result is sufficient for approval.
    Human Review is always required.
    """
    result = {
        "result": result_path,
        "status": "RESULT_ACCEPTANCE_BLOCKED",
        "blocked_reasons": [],
        "approval_granted": False,
        "commit_authorized": False,
        "push_authorized": False,
        "merge_authorized": False,
        "release_authorized": False,
        "human_review_required": True
    }

    if not os.path.exists(result_path):
        result["blocked_reasons"].append(f"Result file not found: {result_path}")
        result["status"] = "RESULT_ACCEPTANCE_SCHEMA_INVALID"
        return result

    try:
        with open(result_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        result["status"] = "RESULT_ACCEPTANCE_SCHEMA_INVALID"
        result["blocked_reasons"].append(f"Invalid JSON: {str(e)}")
        return result

    if not isinstance(data, dict):
        result["status"] = "RESULT_ACCEPTANCE_SCHEMA_INVALID"
        result["blocked_reasons"].append("Root element must be a JSON object")
        return result

    semantic_violations = collect_semantic_guard_violations(data)
    if semantic_violations:
        result["blocked_reasons"].extend(semantic_violations)
        result["status"] = "RESULT_ACCEPTANCE_BLOCKED"

    # --- Required field presence checks ---
    required_fields = [
        "schema_version",
        "task_id",
        "task_brief",
        "implementation_summary",
        "changed_files",
        "validation_results",
        "evidence_items",
        "not_run_items",
        "unknown_items",
        "approval_boundary",
        "result_acceptance_boundary",
        "final_status"
    ]
    for field in required_fields:
        if field not in data:
            result["status"] = "RESULT_ACCEPTANCE_SCHEMA_INVALID"
            result["blocked_reasons"].append(f"Required field missing: {field}")

    # If any required field is missing, stop further checks to avoid false positives
    if result["status"] == "RESULT_ACCEPTANCE_SCHEMA_INVALID":
        return result

    # --- changed_files checks ---
    changed_files = data.get("changed_files", [])
    if not isinstance(changed_files, list):
        result["status"] = "RESULT_ACCEPTANCE_SCHEMA_INVALID"
        result["blocked_reasons"].append("changed_files must be an array")
        return result

    for cf in changed_files:
        if not isinstance(cf, dict):
            result["blocked_reasons"].append("Each changed_files item must be an object")
            continue
        scope_status = cf.get("scope_status")
        hr_required = cf.get("human_review_required")
        if scope_status == "OUT_OF_SCOPE" and not hr_required:
            result["blocked_reasons"].append(
                f"OUT_OF_SCOPE changed file '{cf.get('path', '?')}' requires human_review_required: true"
            )
        if scope_status == "UNKNOWN" and not hr_required:
            result["blocked_reasons"].append(
                f"UNKNOWN scope_status for '{cf.get('path', '?')}' requires human_review_required: true"
            )

    # --- validation_results checks ---
    validation_results = data.get("validation_results", [])
    if not isinstance(validation_results, list):
        result["status"] = "RESULT_ACCEPTANCE_SCHEMA_INVALID"
        result["blocked_reasons"].append("validation_results must be an array")
        return result

    for vr in validation_results:
        if not isinstance(vr, dict):
            result["blocked_reasons"].append("Each validation_results item must be an object")
            continue
        vr_status = vr.get("status")
        hr_required = vr.get("human_review_required")
        if vr_status == "NOT_RUN" and not hr_required:
            # NOT_RUN without human_review_required=true means it is being treated as passing
            result["blocked_reasons"].append(
                f"validation_results item '{vr.get('name', '?')}' has status NOT_RUN "
                "but human_review_required is not true — NOT_RUN must not be treated as PASS"
            )
        if vr_status == "UNKNOWN" and not hr_required:
            result["blocked_reasons"].append(
                f"validation_results item '{vr.get('name', '?')}' has status UNKNOWN "
                "but human_review_required is not true"
            )

    # --- unknown_items checks ---
    unknown_items = data.get("unknown_items", [])
    if not isinstance(unknown_items, list):
        result["status"] = "RESULT_ACCEPTANCE_SCHEMA_INVALID"
        result["blocked_reasons"].append("unknown_items must be an array")
        return result

    for ui in unknown_items:
        if not isinstance(ui, dict):
            result["blocked_reasons"].append("Each unknown_items entry must be an object")
            continue
        if not ui.get("human_review_required"):
            result["blocked_reasons"].append(
                f"unknown_items entry '{ui.get('item_id', '?')}' requires human_review_required: true"
            )

    # --- not_run_items: must be an explicit array (empty is valid) ---
    not_run_items = data.get("not_run_items", [])
    if not isinstance(not_run_items, list):
        result["status"] = "RESULT_ACCEPTANCE_SCHEMA_INVALID"
        result["blocked_reasons"].append("not_run_items must be an array")
        return result

    # --- approval_boundary checks ---
    ab = data.get("approval_boundary", {})
    if not isinstance(ab, dict):
        result["blocked_reasons"].append("approval_boundary must be an object")
    else:
        required_ab_flags = [
            "pass_is_not_approval",
            "evidence_is_not_approval",
            "ci_pass_is_not_approval",
            "result_acceptance_is_not_approval",
            "human_review_required",
            "validator_does_not_grant_approval",
            "validator_does_not_grant_commit_authorization",
            "validator_does_not_grant_push_authorization",
            "validator_does_not_grant_merge_authorization",
            "validator_does_not_grant_release_authorization"
        ]
        for flag in required_ab_flags:
            if ab.get(flag) is not True:
                result["blocked_reasons"].append(
                    f"approval_boundary.{flag} must be true"
                )

    # --- result_acceptance_boundary checks ---
    rab = data.get("result_acceptance_boundary", {})
    if not isinstance(rab, dict):
        result["blocked_reasons"].append("result_acceptance_boundary must be an object")
    else:
        required_rab_flags = [
            "validator_checks_structure_only",
            "validator_does_not_check_semantic_correctness",
            "human_decision_required_for_acceptance"
        ]
        for flag in required_rab_flags:
            if rab.get(flag) is not True:
                result["blocked_reasons"].append(
                    f"result_acceptance_boundary.{flag} must be true"
                )

    # --- final_status checks ---
    final_status = data.get("final_status")
    allowed_statuses = [
        "READY_FOR_HUMAN_RESULT_REVIEW",
        "HUMAN_REVIEW_REQUIRED",
        "BLOCKED",
        "UNKNOWN_BLOCKED",
        "REJECTED_BY_VALIDATOR"
    ]
    if final_status == "APPROVED":
        result["blocked_reasons"].append(
            "final_status cannot be APPROVED — only a human can approve"
        )
    elif final_status not in allowed_statuses:
        result["blocked_reasons"].append(
            f"final_status '{final_status}' is not in allowed list: {allowed_statuses}"
        )

    # --- Forbidden authorization claim checks ---
    for auth_field in ["approval_granted", "commit_authorized", "push_authorized",
                       "merge_authorized", "release_authorized"]:
        if data.get(auth_field) is True:
            result["blocked_reasons"].append(f"{auth_field} cannot be true")

    # --- Determine final status ---
    if result["blocked_reasons"]:
        has_unknown = any("UNKNOWN" in r for r in result["blocked_reasons"])
        has_schema_error = result["status"] == "RESULT_ACCEPTANCE_SCHEMA_INVALID"
        if has_schema_error:
            pass  # Already set
        elif has_unknown:
            result["status"] = "RESULT_ACCEPTANCE_UNKNOWN_BLOCKED"
        else:
            result["status"] = "RESULT_ACCEPTANCE_BLOCKED"
    else:
        result["status"] = "RESULT_ACCEPTANCE_READY_FOR_HUMAN_REVIEW"
        result["message"] = (
            "Structural validation passed. "
            "Validator checks structure only — not semantic correctness. "
            "Approval, commit, push, merge, and release are NOT authorized by this script. "
            "Human Review is required."
        )

    return result


def main():
    parser = argparse.ArgumentParser(description="Task Quality Checker with Functional Intent Gate")
    parser.add_argument(
        "action",
        choices=["validate", "summarize", "validate-forbidden-evidence", "validate-result-acceptance"],
        help="Action to perform"
    )
    parser.add_argument("--package", required=False, help="Path to JSON package")
    parser.add_argument("--mapping", required=False, help="Path to Forbidden Behavior Mapping JSON")
    parser.add_argument("--result", required=False, help="Path to Result Acceptance JSON package")

    args = parser.parse_args()

    if args.action == "validate-result-acceptance":
        if not args.result:
            print("Error: --result is required for validate-result-acceptance")
            sys.exit(1)
        result = check_result_acceptance(args.result)
        print(json.dumps(result, indent=2))
        sys.exit(1 if "BLOCKED" in result["status"] or "INVALID" in result["status"] else 0)

    if args.action == "validate-forbidden-evidence":
        if not args.mapping:
            print("Error: --mapping is required for validate-forbidden-evidence")
            sys.exit(1)
        result = check_forbidden_evidence_mapping(args.mapping)
        print(json.dumps(result, indent=2))
        sys.exit(1 if "BLOCKED" in result["status"] or "INVALID" in result["status"] else 0)

    if not args.package:
        print("Error: --package is required for action " + args.action)
        sys.exit(1)

    result = check_task_quality(args.package)

    if args.action == "validate":
        print(json.dumps(result, indent=2))
        sys.exit(1 if result["status"] == "TASK_QUALITY_FUNCTIONAL_INTENT_BLOCKED" else 0)
    elif args.action == "summarize":
        status_line = f"Status: {result['status']}"
        print(status_line)
        if result["blocked_reasons"]:
            print("Blocked Reasons:")
            for r in result["blocked_reasons"]:
                print(f"  - {r}")
        if result["warnings"]:
            print("Warnings:")
            for w in result["warnings"]:
                print(f"  - {w}")
        sys.exit(1 if result["status"] == "TASK_QUALITY_FUNCTIONAL_INTENT_BLOCKED" else 0)

if __name__ == "__main__":
    main()
