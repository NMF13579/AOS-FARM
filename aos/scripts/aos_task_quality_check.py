import sys
import json
import argparse
import os

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


def main():
    parser = argparse.ArgumentParser(description="Task Quality Checker with Functional Intent Gate")
    parser.add_argument("action", choices=["validate", "summarize", "validate-forbidden-evidence"], help="Action to perform")
    parser.add_argument("--package", required=False, help="Path to JSON package")
    parser.add_argument("--mapping", required=False, help="Path to Forbidden Behavior Mapping JSON")

    args = parser.parse_args()

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
