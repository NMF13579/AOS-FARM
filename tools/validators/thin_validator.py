#!/usr/bin/env python3
import sys
import argparse
import os
import re

def main():
    parser = argparse.ArgumentParser(description="Thin Validator for AOS-FARM")
    parser.add_argument("--input", required=True, help="Path to input file")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(2)

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(2)

    content_lower = content.lower()
    findings = []

    # 4.1. Required fields check
    has_task_id = "task_id" in content_lower
    has_status = "final_status" in content_lower or "checkpoint_status" in content_lower
    if not (has_task_id and has_status):
        findings.append({
            "finding_type": "missing_required_field",
            "message": "Missing required field: task_id or final_status/checkpoint_status"
        })

    # 4.2. Fake approval phrase check
    fake_approval_phrases = [
        "approved: true",
        "approval_granted: true",
        "human_approved: true",
        "commit_authorized: true",
        "push_authorized: true"
    ]
    
    # Context check: If it's a checkpoint, human_decision MUST be present.
    is_checkpoint = "human_decision" in content_lower and "checkpoint_status" in content_lower
    if not is_checkpoint:
        for phrase in fake_approval_phrases:
            if phrase in content_lower:
                findings.append({
                    "finding_type": "fake_approval_claim",
                    "message": f"Found potential fake approval phrase outside human checkpoint context: '{phrase}'"
                })

    # 4.3. UNKNOWN/OK conflict check
    if "unknown" in content_lower:
        if re.search(r'\b(ok|pass|clean|no blockers)\b', content_lower):
            findings.append({
                "finding_type": "unknown_ok_conflict",
                "message": "Found UNKNOWN state mixed with OK/PASS/clean/no blockers claims"
            })

    # 4.4. NOT_RUN/PASS conflict check
    not_run_phrases = ["not_run", "validation_not_run", "test_not_run"]
    has_not_run = any(phrase in content_lower for phrase in not_run_phrases)
    if has_not_run and "pass" in content_lower:
        findings.append({
            "finding_type": "not_run_pass_conflict",
            "message": "Found NOT_RUN claim mixed with PASS claim"
        })

    # 4.5. Forbidden claims check
    forbidden_claims = [
        "release approved",
        "production approved",
        "human approval simulated",
        "ci pass means approval",
        "evidence means approval"
    ]
    for claim in forbidden_claims:
        if claim in content_lower:
            findings.append({
                "finding_type": "forbidden_claim",
                "message": f"Found forbidden claim: '{claim}'"
            })

    # Output Summary
    print(f"--- Thin Validator Execution Report ---")
    print(f"Input: {args.input}")
    if findings:
        print("Status: FAIL")
        for finding in findings:
            print(f"- [{finding['finding_type']}] {finding['message']}")
        sys.exit(1)
    else:
        print("Status: PASS")
        sys.exit(0)

if __name__ == "__main__":
    main()
