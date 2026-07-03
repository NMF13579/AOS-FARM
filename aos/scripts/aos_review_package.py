#!/usr/bin/env python3
"""
Review & Handoff Package Generator
Read-only git/package inspection.
Never outputs APPROVED.
"""

import argparse
import subprocess
import json
import sys
from pathlib import Path

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return None
        return result.stdout.strip()
    except Exception:
        return None

def artifact_summary(path_value):
    if not path_value:
        return None
    path = Path(path_value)
    return {
        "path": path_value,
        "exists": path.exists(),
        "is_file": path.is_file(),
    }

def render_markdown(output):
    lines = [
        "# Review & Handoff Package",
        "",
        f"package_status: {output['package_status']}",
        f"branch: {output['branch']}",
        f"head: {output['head']}",
        f"since: {output['since']}",
        f"validation_status: {output['validation_status']}",
        "approval_claimed: false",
        "commit_authorized: false",
        "push_authorized: false",
        "release_authorized: false",
        "",
        "## Boundary",
        "- Review Package is not approval.",
        "- Review Package is not commit authorization.",
        "- Review Package is not push authorization.",
        "- Review Package is not release authorization.",
        "- Evidence is not approval.",
        "- PASS is not approval.",
        "",
        "## Input Artifacts",
    ]
    artifacts = output.get("artifacts", {})
    if artifacts:
        for name, summary in artifacts.items():
            if summary is None:
                continue
            if isinstance(summary, list):
                for item in summary:
                    if item is not None:
                        lines.append(f"- {name}: {item['path']} (exists={str(item['exists']).lower()}, is_file={str(item['is_file']).lower()})")
            else:
                lines.append(f"- {name}: {summary['path']} (exists={str(summary['exists']).lower()}, is_file={str(summary['is_file']).lower()})")
    else:
        lines.append("- none supplied")
    lines.extend(["", "## Diff Stat"])
    if output.get("diff_stat"):
        lines.extend(f"- {line}" for line in output["diff_stat"])
    else:
        lines.append("- none")
    lines.extend(["", "## Untracked Files"])
    if output.get("untracked_files"):
        lines.extend(f"- {line}" for line in output["untracked_files"])
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"

def main():
    parser = argparse.ArgumentParser(description="AOS Review & Handoff Package Generator")
    parser.add_argument("--since", default="origin/dev", help="Git ref to compare against")
    parser.add_argument("--include-validation", action="store_true", help="Run read-only validation commands")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--task-brief", help="Path to the task brief reviewed")
    parser.add_argument("--execution-package", help="Path to the controlled execution package reviewed")
    parser.add_argument("--changed-files", help="Path to the changed-files artifact reviewed")
    parser.add_argument("--session-record", help="Path to the session record reviewed")
    parser.add_argument("--result-package", help="Path to the result package reviewed")
    parser.add_argument("--execution-report", help="Path to the execution report reviewed")
    parser.add_argument("--evidence-report", help="Path to the evidence report reviewed")
    parser.add_argument("--guard-output", action="append", default=[], help="Path to a guard output artifact reviewed; may be repeated")
    parser.add_argument(
        "--output",
        help="Write a markdown Review & Handoff Package to this path. WARNING: --output writes a file. Do not use --output during read-only audit unless file creation is explicitly authorized.",
    )
    args = parser.parse_args()

    # Git inspection
    branch = run_command(["git", "branch", "--show-current"]) or "UNKNOWN"
    head = run_command(["git", "rev-parse", "HEAD"]) or "UNKNOWN"
    diff_stat = run_command(["git", "diff", "--stat", args.since]) or ""
    untracked = run_command(["git", "status", "--short", "--untracked-files=all"]) or ""

    validation_status = "NOT_RUN"
    validation_results = []

    if args.include_validation:
        try:
            val_result = subprocess.run(["python3", "aos/scripts/aos_validate.py", "all", "--json"], capture_output=True, text=True)
            if val_result.returncode == 0:
                try:
                    val_data = json.loads(val_result.stdout)
                    validation_status = val_data.get("overall_status", "UNKNOWN")
                    validation_results = val_data.get("results", [])
                except json.JSONDecodeError:
                    validation_status = "FAILED"
            else:
                validation_status = "FAILED"
        except Exception:
            validation_status = "FAILED"

    # Determine status
    if branch == "UNKNOWN" or head == "UNKNOWN":
        package_status = "UNKNOWN_BLOCKED"
    elif validation_status in ["FAILED", "BLOCKED", "FAILED_OR_BLOCKED", "UNKNOWN_BLOCKED"]:
        package_status = "CHANGES_REQUIRED"
    elif validation_status == "NOT_RUN":
        package_status = "READY_FOR_HUMAN_REVIEW"
    else:
        package_status = "READY_FOR_HUMAN_REVIEW"

    # Hardcoded safety fields
    approval_claimed = False
    commit_authorized = False
    push_authorized = False
    release_authorized = False
    artifacts = {
        "task_brief": artifact_summary(args.task_brief),
        "execution_package": artifact_summary(args.execution_package),
        "changed_files": artifact_summary(args.changed_files),
        "session_record": artifact_summary(args.session_record),
        "result_package": artifact_summary(args.result_package),
        "execution_report": artifact_summary(args.execution_report),
        "evidence_report": artifact_summary(args.evidence_report),
        "guard_output": [artifact_summary(path) for path in args.guard_output],
    }

    output = {
        "package_status": package_status,
        "branch": branch,
        "head": head,
        "since": args.since,
        "validation_status": validation_status,
        "approval_claimed": approval_claimed,
        "commit_authorized": commit_authorized,
        "push_authorized": push_authorized,
        "release_authorized": release_authorized,
        "review_package_is_not_approval": True,
        "review_package_is_not_commit_authorization": True,
        "review_package_is_not_push_authorization": True,
        "review_package_is_not_release_authorization": True,
        "diff_stat": diff_stat.split('\n') if diff_stat else [],
        "untracked_files": untracked.split('\n') if untracked else [],
        "artifacts": artifacts,
    }
    if args.include_validation:
        output["validation_results"] = validation_results

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_markdown(output), encoding="utf-8")

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print("=== Review & Handoff Package ===")
        print(f"Status: {package_status}")
        print(f"Branch: {branch}")
        print(f"HEAD: {head}")
        print(f"Since: {args.since}")
        print(f"Validation Status: {validation_status}")
        print("---")
        print(f"Approval Claimed: {approval_claimed}")
        print(f"Commit Authorized: {commit_authorized}")
        print(f"Push Authorized: {push_authorized}")
        print(f"Release Authorized: {release_authorized}")
        print("Review Package Is Approval: False")
        print("Review Package Authorizes Commit: False")
        print("Review Package Authorizes Push: False")
        print("Review Package Authorizes Release: False")
        if args.output:
            print(f"Output Written: {args.output}")
        print("---")
        print("Input Artifacts:")
        for name, summary in artifacts.items():
            if isinstance(summary, list):
                for item in summary:
                    print(f"{name}: {item}")
            else:
                print(f"{name}: {summary}")
        print("---")
        print("Diff Stat:")
        print(diff_stat)
        print("---")
        print("Untracked Files:")
        print(untracked)

if __name__ == "__main__":
    main()
