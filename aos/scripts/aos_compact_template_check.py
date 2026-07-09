import argparse
import json
import os
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "Header",
    "Compact Path Contract",
    "Variant selection",
    "Friction budget",
    "Compact Task Card",
    "Eligibility review",
    "Exclusion review",
    "Scoped Change Plan",
    "Pre-Execution Decision Prompt",
    "Execution Authorization Boundary",
    "Minimal Evidence Summary",
    "Evidence Sufficiency Matrix",
    "UNKNOWN / NOT_RUN Summary",
    "Post-Execution Decision Prompt",
    "Future Boundary Reminder",
    "General Boundary Reminder",
    "Transition-to-Full-Path Trigger Summary",
    "Risk Profile Handling",
    "Template-Local Notes"
]

REQUIRED_PHRASES = [
    (r"(PASS \u2260 approval|PASS is not approval)", "PASS is not approval"),
    (r"(Evidence \u2260 approval|Evidence is not approval)", "Evidence is not approval"),
    (r"(CI PASS \u2260 approval|CI PASS is not approval)", "CI PASS is not approval"),
    (r"(UNKNOWN \u2260 OK|UNKNOWN is not OK)", "UNKNOWN is not OK"),
    (r"(NOT_RUN \u2260 PASS|NOT_RUN is not PASS)", "NOT_RUN is not PASS"),
    (r"(Compact eligibility is not approval|compact eligibility is not approval)", "Compact eligibility is not approval"),
    (r"(Compact selection is not execution authorization|compact selection is not execution authorization)", "Compact selection is not execution authorization"),
    (r"(Human approval cannot be simulated|human approval cannot be simulated)", "Human approval cannot be simulated"),
    (r"(Agent must not assign Risk Profile|agent must not assign risk profile)", "Agent must not assign Risk Profile"),
    (r"(Commit authorization \u2260 push authorization|Commit authorization is not push authorization|Commit authorization is separate)", "Commit authorization is not push authorization"),
    (r"(Push authorization \u2260 merge authorization|Push authorization is not merge authorization)", "Push authorization is not merge authorization"),
    (r"(Merge authorization \u2260 release authorization|Merge authorization is not release authorization)", "Merge authorization is not release authorization"),
    (r"(Template is not Source of Truth|This template is not Source of Truth for governance)", "Template is not Source of Truth"),
    (r"(00/01/02 source precedence applies|00/01/02 win according to source precedence)", "00/01/02 source precedence applies"),
    (r"(Execution authorization does not grant commit/push/merge/release|Execution authorization does not grant commit, push, merge, release)", "Execution authorization does not grant commit/push/merge/release")
]

FORBIDDEN_WORDS = [
    "APPROVED",
    "AUTO_APPROVED",
    "CI_APPROVED",
    "READY_FOR_EXECUTION",
    "APPROVED_FOR_EXECUTION",
    "READY_FOR_RELEASE",
    "APPROVED_FOR_RELEASE",
    "READY_TO_MERGE",
    "READY_TO_RELEASE",
    "COMPACT_APPROVED",
    "VALIDATOR_APPROVED",
    "TEMPLATE_APPROVED",
    "CHECKER_APPROVED",
    "approved by validation",
    "safe to merge",
    "safe to release",
    "no human review needed"
]

SAFE_NEGATIVE_CONTEXTS = [
    r"PASS is not approval",
    r"PASS \u2260 approval",
    r"Evidence is not approval",
    r"Evidence \u2260 approval",
    r"CI PASS is not approval",
    r"CI PASS \u2260 approval",
    r"Do not use APPROVED",
    r"Forbidden final statuses:\s*APPROVED",
    r"Commit authorization is not push authorization",
    r"Commit authorization \u2260 push authorization",
    r"UNKNOWN \u2260 OK",
    r"NOT_RUN \u2260 PASS",
    r"Compact eligibility is not approval",
    r"Compact selection is not execution authorization",
    r"Human approval cannot be simulated",
    r"Agent must not assign Risk Profile",
    r"Push authorization is not merge authorization",
    r"Merge authorization is not release authorization",
    r"Template is not Source of Truth",
    r"Execution authorization does not grant commit/push/merge/release"
]

def find_repo_root(start_dir: Path) -> Path:
    current = start_dir.resolve()
    while True:
        has_00 = (current / "00_AOS_Core_Control.md").exists()
        has_01 = (current / "01_AOS_Assembly_Pipelines_and_Build_Roadmap.md").exists()
        has_02 = (current / "02_AOS_Governance_Control_Module_and_Safety_Rules.md").exists()
        has_aos = (current / "aos").is_dir()

        if has_00 and has_01 and has_02 and has_aos:
            return current

        parent = current.parent
        if parent == current:
            break
        current = parent
    return None

def is_safe_negative(line, word):
    for ctx in SAFE_NEGATIVE_CONTEXTS:
        if re.search(ctx, line, re.IGNORECASE):
            return True
    return False

def check_template(file_path: Path):
    checks = []

    try:
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()
    except Exception as e:
        checks.append({
            "name": "File Read",
            "status": "UNKNOWN_BLOCKED",
            "severity": "BLOCKED",
            "message": f"Could not read file: {e}",
            "evidence": str(file_path)
        })
        return checks

    # 1. Required Headings
    for heading in REQUIRED_HEADINGS:
        if heading == "Header":
            if not lines or not lines[0].startswith("#"):
                checks.append({
                    "name": f"Missing Section: {heading}",
                    "status": "FAIL",
                    "severity": "FAIL",
                    "message": f"Missing required section: {heading}",
                    "evidence": heading
                })
            else:
                checks.append({
                    "name": f"Section: {heading}",
                    "status": "PASS",
                    "severity": "INFO",
                    "message": f"Found required section: {heading}",
                    "evidence": lines[0] if lines else ""
                })
            continue

        found = any(heading.lower() in line.lower() for line in lines)
        if not found:
            checks.append({
                "name": f"Missing Section: {heading}",
                "status": "FAIL",
                "severity": "FAIL",
                "message": f"Missing required section: {heading}",
                "evidence": heading
            })
        else:
            checks.append({
                "name": f"Section: {heading}",
                "status": "PASS",
                "severity": "INFO",
                "message": f"Found required section: {heading}",
                "evidence": heading
            })

    # 2. Required Phrases
    for pattern, desc in REQUIRED_PHRASES:
        found = any(re.search(pattern, line, re.IGNORECASE) for line in lines)
        if not found:
            checks.append({
                "name": f"Missing Phrase: {desc}",
                "status": "FAIL",
                "severity": "FAIL",
                "message": f"Missing required phrase: {desc}",
                "evidence": desc
            })
        else:
            checks.append({
                "name": f"Phrase: {desc}",
                "status": "PASS",
                "severity": "INFO",
                "message": f"Found required phrase: {desc}",
                "evidence": desc
            })

    # 3. Forbidden Words
    for i, line in enumerate(lines):
        for word in FORBIDDEN_WORDS:
            if word in line:
                if is_safe_negative(line, word):
                    checks.append({
                        "name": f"Safe Negative Reminder: {word}",
                        "status": "PASS",
                        "severity": "INFO",
                        "message": f"Forbidden word '{word}' used in safe negative context.",
                        "evidence": f"Line {i+1}: {line.strip()}"
                    })
                else:
                    # Ambiguous or unsafe
                    if "approval" in line.lower() or "ready" in line.lower() or "safe" in line.lower() or word == "APPROVED":
                        status = "BLOCKED"
                        sev = "BLOCKED"
                    else:
                        status = "HUMAN_REVIEW_REQUIRED"
                        sev = "HUMAN_REVIEW_REQUIRED"

                    checks.append({
                        "name": f"Forbidden Word: {word}",
                        "status": status,
                        "severity": sev,
                        "message": f"Unsafe or ambiguous use of forbidden word: {word}",
                        "evidence": f"Line {i+1}: {line.strip()}"
                    })

    # 4. Same block commit+push
    for i in range(len(lines) - 1):
        if ("AOS COMMIT OK" in lines[i] and "AOS PUSH OK" in lines[i+1]) or \
           ("AOS PUSH OK" in lines[i] and "AOS COMMIT OK" in lines[i+1]):
            checks.append({
                "name": "Same-Block Commit+Push",
                "status": "BLOCKED",
                "severity": "BLOCKED",
                "message": "same-block commit+push violation detected",
                "evidence": f"Line {i+1}-{i+2}"
            })

    # 5. Source of truth claim
    sot_pattern = r"(template is the source of truth|this template is the source of truth|this template is the source of truth for governance)"
    for i, line in enumerate(lines):
        if re.search(sot_pattern, line, re.IGNORECASE) and not is_safe_negative(line, "Source of Truth"):
            checks.append({
                "name": "Source of Truth Claim",
                "status": "BLOCKED",
                "severity": "BLOCKED",
                "message": "Source of Truth authority claim detected",
                "evidence": f"Line {i+1}: {line.strip()}"
            })

    # 6. Checker PASS grants approval
    pg_pattern = r"(checker pass grants approval|checker pass is approval|eligibility grants execution)"
    for i, line in enumerate(lines):
        if re.search(pg_pattern, line, re.IGNORECASE):
            checks.append({
                "name": "False Approval Claim",
                "status": "BLOCKED",
                "severity": "BLOCKED",
                "message": "Checker PASS or eligibility wrongly claims approval/execution",
                "evidence": f"Line {i+1}: {line.strip()}"
            })

    return checks

def determine_final_status(checks):
    if any(c["status"] == "UNKNOWN_BLOCKED" for c in checks):
        return "UNKNOWN_BLOCKED"
    if any(c["status"] == "BLOCKED" for c in checks):
        return "BLOCKED"
    if any(c["status"] == "HUMAN_REVIEW_REQUIRED" for c in checks):
        return "HUMAN_REVIEW_REQUIRED"
    if any(c["status"] == "FAIL" for c in checks):
        return "FAIL"
    if any(c["status"] == "NOT_RUN" for c in checks):
        return "NOT_RUN"
    return "PASS"

def main():
    parser = argparse.ArgumentParser(description="Compact Template Integrity Checker")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--target", type=str, help="Path to compact template file")

    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    if not repo_root:
        report = {
            "final_status": "UNKNOWN_BLOCKED",
            "target_path": args.target or "UNKNOWN",
            "checks": [],
            "failures": ["UNKNOWN_BLOCKED_REPO_ROOT_UNCLEAR"],
            "warnings": [],
            "blocked_reasons": ["UNKNOWN_BLOCKED_REPO_ROOT_UNCLEAR"],
            "unknown_reasons": ["UNKNOWN_BLOCKED_REPO_ROOT_UNCLEAR"],
            "advisory_only": True,
            "approval_granted": False,
            "execution_authorized": False,
            "commit_authorized": False,
            "push_authorized": False,
            "merge_authorized": False,
            "release_authorized": False
        }
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print("UNKNOWN_BLOCKED_REPO_ROOT_UNCLEAR")
        sys.exit(1)

    target_path_str = args.target if args.target else "aos/templates/compact/compact-safe-path-template.md"
    target_path = (repo_root / target_path_str).resolve()

    try:
        target_path.relative_to(repo_root)
    except ValueError:
        report = {
            "final_status": "BLOCKED",
            "target_path": str(target_path),
            "checks": [],
            "failures": ["Target path is outside repository root"],
            "warnings": [],
            "blocked_reasons": ["Target path is outside repository root"],
            "unknown_reasons": [],
            "advisory_only": True,
            "approval_granted": False,
            "execution_authorized": False,
            "commit_authorized": False,
            "push_authorized": False,
            "merge_authorized": False,
            "release_authorized": False
        }
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"BLOCKED: Target path is outside repository root: {target_path}")
        sys.exit(1)

    checks = check_template(target_path)
    final_status = determine_final_status(checks)

    failures = [c["message"] for c in checks if c["status"] == "FAIL"]
    warnings = [c["message"] for c in checks if c["status"] == "WARNING"]
    blocked = [c["message"] for c in checks if c["status"] == "BLOCKED"]
    unknowns = [c["message"] for c in checks if c["status"] == "UNKNOWN_BLOCKED"]

    report = {
        "final_status": final_status,
        "target_path": str(target_path.relative_to(repo_root)),
        "checks": checks,
        "failures": failures,
        "warnings": warnings,
        "blocked_reasons": blocked,
        "unknown_reasons": unknowns,
        "advisory_only": True,
        "approval_granted": False,
        "execution_authorized": False,
        "commit_authorized": False,
        "push_authorized": False,
        "merge_authorized": False,
        "release_authorized": False
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Final Status: {final_status}")
        for c in checks:
            if c["status"] != "PASS":
                print(f"[{c['status']}] {c['name']}: {c['message']} ({c['evidence']})")

    if final_status == "PASS":
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
