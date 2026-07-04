import argparse
import datetime
import json
import subprocess
import sys

SCHEMA_VERSION = "1.0"
PROJECT = "AOS-FARM"

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return ""

def main():
    parser = argparse.ArgumentParser(description="AOS Review Package Helper")
    parser.add_argument("--mode", required=True, choices=["human-review", "commit-authorization", "push-authorization", "remote-closure"])
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--files", nargs="*", default=[])
    parser.add_argument("--target-branch", required=True)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    current_branch = run_cmd("git branch --show-current")
    head_sha = run_cmd("git rev-parse HEAD")
    origin_target_sha = run_cmd(f"git rev-parse origin/{args.target_branch}")
    
    staged_out = run_cmd("git diff --cached --name-only")
    staged_files = staged_out.split() if staged_out else []
    
    modified_out = run_cmd("git diff --name-only")
    modified_tracked_files = modified_out.split() if modified_out else []
    
    untracked_out = run_cmd("git ls-files --others --exclude-standard")
    untracked_files = untracked_out.split() if untracked_out else []
    
    all_changed = set(staged_files + modified_tracked_files + untracked_files)
    declared_files = set(args.files)
    
    files_in_scope = list(all_changed.intersection(declared_files))
    files_outside_scope = list(all_changed.difference(declared_files))
    
    diff_summary = run_cmd("git diff --stat")
    last_commit_summary = run_cmd("git log -1 --oneline")
    
    analysis_status = "REVIEW_PACKAGE_COLLECTED"
    if files_outside_scope:
        analysis_status = "BLOCKED"
        
    notes = [
        "Review package is not approval.",
        "Generated review package is not Source of Truth.",
        "Evidence is not approval.",
        "PASS is not approval.",
        "UNKNOWN is not OK.",
        "NOT_RUN is not PASS.",
        "Commit authorization is not push authorization.",
        "Push authorization is not release authorization.",
        "No push was performed."
    ]

    data = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "task": args.task_id,
        "mode": args.mode,
        "branch_head_remote_state": f"{current_branch} | {head_sha} | {origin_target_sha}",
        "working_tree": "CLEAN" if not all_changed else "DIRTY",
        "files_in_scope": files_in_scope,
        "files_outside_scope": files_outside_scope,
        "diff_summary": diff_summary,
        "last_commit_summary": last_commit_summary,
        "validation_snapshot": "NOT_RUN",
        "unknowns": [],
        "forbidden_changes_check": "PASS" if not files_outside_scope else "FAIL",
        "human_decision_required": "Yes",
        "recommended_next_prompt": f"Authorize {args.mode} for {args.task_id}",
        "safety_notes": notes,
        "analysis_status": analysis_status
    }

    if args.format == "json":
        print(json.dumps(data, indent=2))
        return

    print(f"# AOS Review Package: {args.task_id}")
    print(f"**Mode:** {args.mode}")
    print(f"**Analysis Status:** {data['analysis_status']}\n")
    
    print("## Branch / HEAD / Remote State")
    print(data['branch_head_remote_state'])
    
    print("\n## Working Tree")
    print(data['working_tree'])
    
    print("\n## Files in Scope")
    for f in data['files_in_scope']:
        print(f"- {f}")
        
    print("\n## Files Outside Scope")
    for f in data['files_outside_scope']:
        print(f"- {f}")
        
    print("\n## Diff Summary")
    print(data['diff_summary'])
    
    print("\n## Last Commit Summary")
    print(data['last_commit_summary'])
    
    print("\n## Validation Snapshot")
    print(data['validation_snapshot'])
    
    print("\n## UNKNOWNs")
    print("None")
    
    print("\n## Forbidden Changes Check")
    print(data['forbidden_changes_check'])
    
    print("\n## Human Decision Required")
    print(data['human_decision_required'])
    
    print("\n## Recommended Next Prompt")
    print(data['recommended_next_prompt'])
    
    print("\n## Safety Notes")
    for n in data['safety_notes']:
        print(f"- {n}")

if __name__ == '__main__':
    main()
