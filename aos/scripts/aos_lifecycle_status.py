import argparse
import datetime
import json
import subprocess
import sys
import os

SCHEMA_VERSION = "1.0"
PROJECT = "AOS-FARM"

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip(), None
    except subprocess.CalledProcessError as e:
        return "UNKNOWN", f"Command failed: {cmd}"

def main():
    parser = argparse.ArgumentParser(description="AOS Lifecycle Status Helper")
    parser.add_argument("--markdown", action="store_true", help="Output in Markdown format")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--compact", action="store_true", help="Compact output mode")
    parser.add_argument("--summary", action="store_true", help="Summary output mode")
    parser.add_argument("--next", action="store_true", help="Output next safe checkpoint guidance")
    args = parser.parse_args()

    if not args.json and not args.markdown and not args.next:
        args.markdown = True

    warnings = []
    
    # Try to reuse baseline summary
    baseline_data = {}
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        baseline_script = os.path.join(base_dir, "aos_baseline_summary.py")
        res = subprocess.run([sys.executable, baseline_script, "--json"], capture_output=True, text=True, check=True)
        baseline_data = json.loads(res.stdout)
    except Exception as e:
        warnings.append(f"Could not load baseline summary: {e}")
        baseline_data = {
            "current_branch": "UNKNOWN",
            "head_sha": "UNKNOWN",
            "origin_dev_sha": "UNKNOWN",
            "origin_main_sha": "UNKNOWN",
            "working_tree_summary": "UNKNOWN",
            "last_commit_subject": "UNKNOWN"
        }

    detected_task = "UNKNOWN"
    detected_lifecycle_phase = "UNKNOWN"
    last_completed_task = "UNKNOWN"
    last_remote_closure = "UNKNOWN"
    evidence = []
    missing_evidence = []
    open_unknowns = []
    
    # Simple best-effort inference
    branch = baseline_data.get("current_branch", "UNKNOWN")
    if branch.startswith("build/"):
        detected_task = branch.split("build/")[-1]
        detected_lifecycle_phase = "IMPLEMENTATION"
    elif branch.startswith("work/"):
        detected_task = branch.split("work/")[-1]
        detected_lifecycle_phase = "IMPLEMENTATION"
    else:
        detected_lifecycle_phase = "BASE"
        
    last_subject = baseline_data.get("last_commit_subject", "UNKNOWN")
    if "(AOS-FARM" in last_subject:
        start_idx = last_subject.find("(AOS-FARM") + 1
        end_idx = last_subject.find(")", start_idx)
        if end_idx != -1:
            last_completed_task = last_subject[start_idx:end_idx]

    notes = [
        "Generated status summary is not Source of Truth.",
        "Generated status summary is not approval.",
        "UNKNOWN is not OK.",
        "NOT_RUN is not PASS.",
        "PASS is not approval.",
        "Evidence is not approval.",
        "Local trace boundary: /.aos-tmp/logs/ is local-only, ignored, disposable, not Evidence, not approval, not Source of Truth."
    ]
    
    analysis_status = "STATUS_COLLECTED"
    if "UNKNOWN" in (branch, baseline_data.get("head_sha", "UNKNOWN")):
        analysis_status = "UNKNOWN_BLOCKED"

    data = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "project": PROJECT,
        "branch": branch,
        "head": baseline_data.get("head_sha", "UNKNOWN"),
        "origin_dev": baseline_data.get("origin_dev_sha", "UNKNOWN"),
        "origin_main": baseline_data.get("origin_main_sha", "UNKNOWN"),
        "working_tree": baseline_data.get("working_tree_summary", "UNKNOWN"),
        "detected_task": detected_task,
        "detected_lifecycle_phase": detected_lifecycle_phase,
        "last_completed_task": last_completed_task,
        "last_remote_closure": last_remote_closure,
        "analysis_status": analysis_status,
        "evidence": evidence,
        "missing_evidence": missing_evidence,
        "open_unknowns": open_unknowns,
        "warnings": warnings,
        "next_required_human_checkpoint": "Review and Approval",
        "allowed_next_actions": ["Review", "Test", "Draft Report"],
        "forbidden_actions": ["Commit", "Push", "Merge", "Release", "Mutate Lifecycle"],
        "source_of_truth_note": "Generated status summary is not Source of Truth.",
        "approval_note": "Generated status summary is not approval.",
        "notes": notes
    }

    if args.json:
        print(json.dumps(data, indent=2))
        return

    if args.next:
        print("## Next Safe Checkpoint Guidance\n")
        print(f"Current phase: {data['detected_lifecycle_phase']}")
        print(f"Next safe checkpoint: {data['next_required_human_checkpoint']}")
        print("Why this checkpoint is next: Ensures human oversight before any state mutation.")
        print("Required human decision: Explicit authorization to proceed.")
        print("Forbidden actions: " + ", ".join(data['forbidden_actions']))
        print("Action executed: no")
        print("\nNext safe checkpoint is guidance only.")
        print("It is not authorization.")
        print("Action executed: no.")
        return

    if args.compact:
        print(f"**AOS Lifecycle Status: {data['analysis_status']}**")
        print(f"Branch: {data['branch']} | Phase: {data['detected_lifecycle_phase']}")
        print(f"Task: {data['detected_task']}")
        print("Safety Notes:")
        for n in data['notes']:
            print(f"- {n}")
        return

    if args.summary:
        print(f"# AOS Lifecycle Summary: {data['analysis_status']}\n")
        print(f"**Branch:** {data['branch']} | **HEAD:** {data['head']}")
        print(f"**Phase:** {data['detected_lifecycle_phase']}")
        print(f"**Task:** {data['detected_task']}")
        print(f"**Last Completed Task:** {data['last_completed_task']}")
        print("\n**Safety Notes:**")
        for n in data['notes']:
            print(f"- {n}")
        return

    if args.markdown:
        print("# AOS Lifecycle Status\n")
        print("## Generated At")
        print(f"{data['generated_at']}\n")
        print("## Analysis Status")
        print(f"**{data['analysis_status']}**\n")
        print("## Current State")
        print(f"- Branch: {data['branch']}")
        print(f"- HEAD: {data['head']}")
        print(f"- Detected Task: {data['detected_task']}")
        print(f"- Phase: {data['detected_lifecycle_phase']}")
        print(f"- Last Completed Task: {data['last_completed_task']}\n")
        print("## Safety Notes")
        for n in data['notes']:
            print(f"- {n}")

if __name__ == '__main__':
    main()
