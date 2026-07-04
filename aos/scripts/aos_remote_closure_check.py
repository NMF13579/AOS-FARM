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
        return result.stdout.strip(), None
    except subprocess.CalledProcessError as e:
        return "UNKNOWN", f"Command failed: {cmd}"

def main():
    parser = argparse.ArgumentParser(description="AOS Remote Closure Check Helper")
    parser.add_argument("--target", default="dev", help="Target branch for closure check")
    parser.add_argument("--markdown", action="store_true", help="Output in Markdown format")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    if not args.json and not args.markdown:
        args.markdown = True

    warnings = []

    current_branch, _ = run_cmd("git branch --show-current")
    head_sha, _ = run_cmd("git rev-parse HEAD")
    origin_target_sha, _ = run_cmd(f"git rev-parse origin/{args.target}")
    
    ls_remote_out, err = run_cmd(f"git ls-remote origin refs/heads/{args.target}")
    ls_remote_target_sha = ls_remote_out.split()[0] if ls_remote_out else "UNKNOWN"
    if err:
        warnings.append(err)

    status_out, _ = run_cmd("git status --short --untracked-files=all")
    working_tree_clean = not bool(status_out)

    ahead_behind_state, _ = run_cmd(f"git rev-list --left-right --count origin/{args.target}...HEAD")
    last_commit_subject, _ = run_cmd("git log -1 --format=%s")
    last_commit_changed_files, _ = run_cmd("git show --name-status --oneline --no-renames HEAD | tail -n +2")

    origin_main_relation = "N/A"
    if args.target == "dev":
        origin_main_relation, _ = run_cmd("git rev-list --left-right --count origin/main...origin/dev")

    head_equals_origin_target = (head_sha == origin_target_sha and head_sha != "UNKNOWN")
    head_equals_ls_remote_target = (head_sha == ls_remote_target_sha and head_sha != "UNKNOWN")

    analysis_status = "REMOTE_CLOSURE_VERIFIED"
    if not working_tree_clean or not head_equals_origin_target or not head_equals_ls_remote_target:
        analysis_status = "REMOTE_CLOSURE_FAILED"
    
    if "UNKNOWN" in (head_sha, origin_target_sha, ls_remote_target_sha):
        analysis_status = "UNKNOWN_BLOCKED"

    notes = [
        "Remote closure verification is Evidence, not approval.",
        "Remote closure verification is not release authorization.",
        "UNKNOWN is not OK.",
        "NOT_RUN is not PASS.",
        "PASS is not approval.",
        "Commit authorization is not push authorization.",
        "Push authorization is not release authorization.",
        "No push was performed."
    ]

    data = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "project": PROJECT,
        "target": args.target,
        "current_branch": current_branch,
        "head_sha": head_sha,
        "origin_target_sha": origin_target_sha,
        "ls_remote_target_sha": ls_remote_target_sha,
        "head_equals_origin_target": head_equals_origin_target,
        "head_equals_ls_remote_target": head_equals_ls_remote_target,
        "working_tree_clean": working_tree_clean,
        "origin_main_relation_if_target_dev": origin_main_relation,
        "ahead_behind_state": ahead_behind_state,
        "last_commit_subject": last_commit_subject,
        "last_commit_changed_files": last_commit_changed_files.split('\n') if last_commit_changed_files else [],
        "analysis_status": analysis_status,
        "warnings": warnings,
        "notes": notes
    }

    if args.json:
        print(json.dumps(data, indent=2))
        return

    if args.markdown:
        print(f"# AOS Remote Closure Check (Target: {args.target})")
        print(f"\n**Analysis Status: {data['analysis_status']}**\n")
        print("## State")
        print(f"- Current Branch: {data['current_branch']}")
        print(f"- HEAD: {data['head_sha']}")
        print(f"- origin/{args.target}: {data['origin_target_sha']}")
        print(f"- ls-remote {args.target}: {data['ls_remote_target_sha']}")
        print(f"- Working Tree Clean: {data['working_tree_clean']}")
        print(f"- Ahead/Behind: {data['ahead_behind_state']}")
        print(f"\n## Last Commit")
        print(f"- {data['last_commit_subject']}")
        print("\n## Notes")
        for n in data['notes']:
            print(f"- {n}")

if __name__ == '__main__':
    main()
