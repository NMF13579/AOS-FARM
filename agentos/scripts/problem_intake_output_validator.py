#!/usr/bin/env python3
import argparse
import os
import re
import sys

REQUIRED_FILES = {
    "PROJECT_SPEC.draft.md",
    "REQUIREMENTS.draft.md",
    "problem-interview-report.md",
    "requirements-checklist-draft.md",
    "problem-intake-run-report.md"
}

REQUIRED_FIELDS_ALL = {
    "artifact_status: DRAFT",
    "approval_status: NOT_APPROVED",
    "automation_status: MVP_RUNNER_ONLY",
    "production_status: NOT_PRODUCTION"
}

# The run report has some dynamic fields that need regex matching for the valid permutations
RUN_REPORT_FIELDS_REGEX = [
    r"run_status:\s*(DRAFT_CREATED|INCOMPLETE|FAILED)",
    r"draft_status:\s*(DRAFT_ONLY|INCOMPLETE)",
    r"validation_status:\s*(BASIC_STRUCTURE_CHECKED|NEEDS_HUMAN_REVIEW|NOT_VALIDATED)",
    r"approval_status:\s*NOT_APPROVED"
]

UNSAFE_CLAIMS = [
    "PASS",
    "APPROVED",
    "PRODUCTION_READY",
    "IMPLEMENTATION_AUTHORIZED",
    "EXECUTION_AUTHORIZED",
    "HUMAN_APPROVED",
    "READY_FOR_RELEASE"
]

SAFE_PREFIXES = [
    "NOT_APPROVED",
    "NOT_PRODUCTION",
    "NOT_VALIDATED",
    "NOT_RUN"
]

def check_false_claims(content: str) -> list:
    # Replace safe prefixes with placeholders to avoid matching safe negative forms
    safe_content = content
    for safe in SAFE_PREFIXES:
        safe_content = safe_content.replace(safe, "SAFE_PLACEHOLDER")
    
    found_claims = []
    # Using word boundaries for safe isolation
    for claim in UNSAFE_CLAIMS:
        pattern = r'\b' + re.escape(claim) + r'\b'
        if re.search(pattern, safe_content):
            found_claims.append(claim)
            
    return found_claims

def generate_report(args, results: dict, report_path: str):
    content = "# Problem Intake Output Validator Report\n\n"
    content += "## 1. Task Metadata\n"
    content += f"- **Run Directory**: `{args.run_dir}`\n"
    
    content += "\n## 2. Run Directory\n"
    content += f"- Analyzed Path: `{os.path.abspath(args.run_dir)}`\n"
    
    content += "\n## 3. Required File Inventory\n"
    for f in REQUIRED_FILES:
        status = "Found" if f in results['found_files'] else "Missing"
        content += f"- {f}: {status}\n"
        
    content += "\n## 4. Unexpected File Inventory\n"
    if results['unexpected_files']:
        for f in results['unexpected_files']:
            content += f"- {f}\n"
    else:
        content += "- None\n"
        
    content += "\n## 5. Status Field Check Results\n"
    if results['field_errors']:
        for err in results['field_errors']:
            content += f"- {err}\n"
    else:
        content += "- All required status fields present in all files.\n"
        
    content += "\n## 6. False Claim Scan Results\n"
    if results['false_claims']:
        for f, claims in results['false_claims'].items():
            content += f"- {f}: Found unsafe claims: {', '.join(claims)}\n"
    else:
        content += "- No unsafe claims found.\n"
        
    content += "\n## 7. Final Validator Status\n"
    content += "```yaml\n"
    content += f"validator_status: {results['validator_status']}\n"
    content += f"structure_status: {results['structure_status']}\n"
    content += f"status_field_status: {results['status_field_status']}\n"
    content += f"false_claim_status: {results['false_claim_status']}\n"
    content += "approval_status: NOT_APPROVED\n"
    content += "production_status: NOT_PRODUCTION\n"
    content += "```\n"
    
    content += "\n## 8. Limitations\n"
    content += "- The validator does not verify semantic quality, business correctness, product-market fit, human approval, production readiness, completeness of requirements, or implementation readiness.\n"
    
    content += "\n## 9. Recommended Next Task\n"
    content += "AOS-FARM.TA-17 — Problem Intake Output Validator Evidence Review\n"
    
    try:
        os.makedirs(os.path.dirname(os.path.abspath(report_path)), exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing report: {e}")
        sys.exit(2)

def main():
    parser = argparse.ArgumentParser(description="Problem Intake Output Validator")
    parser.add_argument("--run-dir", required=True, help="Path to the problem intake run directory")
    parser.add_argument("--report", help="Path to output markdown report")
    args = parser.parse_args()

    run_dir = args.run_dir
    
    if not os.path.exists(run_dir):
        print(f"Error: Run directory '{run_dir}' does not exist.")
        sys.exit(2)
    if not os.path.isdir(run_dir):
        print(f"Error: Run directory '{run_dir}' is not a directory.")
        sys.exit(2)
        
    try:
        actual_files = set(os.listdir(run_dir))
    except Exception as e:
        print(f"Error reading directory '{run_dir}': {e}")
        sys.exit(2)

    found_required = actual_files.intersection(REQUIRED_FILES)
    missing_required = REQUIRED_FILES - actual_files
    unexpected_files = actual_files - REQUIRED_FILES

    structure_valid = not bool(missing_required or unexpected_files)
    
    field_errors = []
    false_claims = {}
    
    for filename in found_required:
        filepath = os.path.join(run_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            field_errors.append(f"Error reading {filename}: {e}")
            continue
            
        # Check globally required fields for every artifact
        for field in REQUIRED_FIELDS_ALL:
            if field not in content:
                field_errors.append(f"{filename} missing required field: {field}")
                
        # Check run-report specific fields
        if filename == "problem-intake-run-report.md":
            for pattern in RUN_REPORT_FIELDS_REGEX:
                if not re.search(pattern, content):
                    field_errors.append(f"{filename} missing or invalid field matching: {pattern}")
                    
        # Check for false positive claims (e.g., APPROVED vs NOT_APPROVED)
        claims = check_false_claims(content)
        if claims:
            false_claims[filename] = claims

    status_fields_valid = len(field_errors) == 0
    false_claims_valid = len(false_claims) == 0
    
    structure_status = "STRUCTURE_CHECKED" if structure_valid else "STRUCTURE_INVALID"
    status_field_status = "STATUS_FIELDS_CHECKED" if status_fields_valid else "STATUS_FIELDS_INVALID"
    false_claim_status = "NO_UNSAFE_CLAIMS_FOUND" if false_claims_valid else "UNSAFE_CLAIMS_FOUND"
    
    validation_passed = structure_valid and status_fields_valid and false_claims_valid
    validator_status = "VALIDATION_COMPLETE" if validation_passed else "VALIDATION_FAILED"
    
    results = {
        "found_files": found_required,
        "missing_files": missing_required,
        "unexpected_files": unexpected_files,
        "field_errors": field_errors,
        "false_claims": false_claims,
        "structure_status": structure_status,
        "status_field_status": status_field_status,
        "false_claim_status": false_claim_status,
        "validator_status": validator_status
    }
    
    if args.report:
        generate_report(args, results, args.report)
        
    print(f"validator_status: {validator_status}")
    print(f"structure_status: {structure_status}")
    print(f"status_field_status: {status_field_status}")
    print(f"false_claim_status: {false_claim_status}")
    
    if validation_passed:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
