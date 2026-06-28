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

def main():
    parser = argparse.ArgumentParser(description="Task Quality Checker with Functional Intent Gate")
    parser.add_argument("action", choices=["validate", "summarize"], help="Action to perform")
    parser.add_argument("--package", required=True, help="Path to JSON package")
    
    args = parser.parse_args()

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
