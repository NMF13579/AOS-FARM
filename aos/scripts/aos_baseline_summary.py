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
    parser = argparse.ArgumentParser(description="AOS Baseline Summary Helper")
    parser.add_argument("--markdown", action="store_true", help="Output in Markdown format")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--compact", action="store_true", help="Compact output mode")
    parser.add_argument("--summary", action="store_true", help="Summary output mode")
    parser.add_argument("--target-branch", default="dev", help="Target branch for comparison")
    args = parser.parse_args()

    if not args.json and not args.markdown:
        args.markdown = True

    warnings = []
    
    current_branch, err = run_cmd("git branch --show-current")
    if err: warnings.append(err)
    
    head_sha, err = run_cmd("git rev-parse HEAD")
    if err: warnings.append(err)
    
    origin_dev_sha, err = run_cmd("git rev-parse origin/dev")
    if err: warnings.append(err)
    
    origin_main_sha, err = run_cmd("git rev-parse origin/main")
    if err: warnings.append(err)
    
    ls_remote_dev_out, err = run_cmd("git ls-remote origin refs/heads/dev")
    ls_remote_dev_sha = "UNKNOWN"
    if err: 
        warnings.append(err)
    elif ls_remote_dev_out:
        ls_remote_dev_sha = ls_remote_dev_out.split()[0]
        
    ls_remote_main_out, err = run_cmd("git ls-remote origin refs/heads/main")
    ls_remote_main_sha = "UNKNOWN"
    if err:
        warnings.append(err)
    elif ls_remote_main_out:
        ls_remote_main_sha = ls_remote_main_out.split()[0]
        
    origin_dev_head_ab, err = run_cmd("git rev-list --left-right --count origin/dev...HEAD")
    if err: warnings.append(err)
    
    origin_main_head_ab, err = run_cmd("git rev-list --left-right --count origin/main...HEAD")
    if err: warnings.append(err)
    
    origin_main_origin_dev_ab, err = run_cmd("git rev-list --left-right --count origin/main...origin/dev")
    if err: warnings.append(err)
    
    working_tree_summary, err = run_cmd("git status -sb")
    if err: warnings.append(err)
    
    porcelain_status, err = run_cmd("git status --porcelain")
    if err: warnings.append(err)
    
    staged_files_count = 0
    modified_files_count = 0
    untracked_files_count = 0
    untracked_files_summary = []
    
    if porcelain_status != "UNKNOWN" and porcelain_status:
        for line in porcelain_status.split('\n'):
            if len(line) < 2:
                continue
            status_code = line[:2]
            file_name = line[3:]
            
            if status_code == '??':
                untracked_files_count += 1
                untracked_files_summary.append(file_name)
            else:
                if status_code[0] in ('M', 'A', 'D', 'R', 'C'):
                    staged_files_count += 1
                if status_code[1] in ('M', 'D'):
                    modified_files_count += 1

    working_tree_clean = (staged_files_count == 0 and modified_files_count == 0 and untracked_files_count == 0)
    
    last_commit_subject, err = run_cmd("git log -1 --format=%s")
    if err: warnings.append(err)
    
    last_commit_show, err = run_cmd("git show --name-status --oneline --no-renames HEAD")
    last_commit_changed_files = []
    if err: 
        warnings.append(err)
    elif last_commit_show and last_commit_show != "UNKNOWN":
        lines = last_commit_show.split('\n')
        if len(lines) > 1:
            last_commit_changed_files = lines[1:]
            
    notes = [
        "Generated baseline summary is not Source of Truth.",
        "Generated baseline summary is not approval.",
        "Baseline Evidence is not approval.",
        "UNKNOWN is not OK.",
        "NOT_RUN is not PASS.",
        "PASS is not approval.",
        "No commit was performed.",
        "No push was performed.",
        "Local trace boundary: /.aos-tmp/logs/ is local-only, ignored, disposable, not Evidence, not approval, not Source of Truth."
    ]
    
    analysis_status = "BASELINE_COLLECTED"
    if "UNKNOWN" in (current_branch, head_sha, origin_dev_sha, origin_main_sha, 
                     ls_remote_dev_sha, ls_remote_main_sha, origin_dev_head_ab, 
                     origin_main_head_ab, origin_main_origin_dev_ab):
        analysis_status = "UNKNOWN_BLOCKED"
    
    data = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "project": PROJECT,
        "target_branch": args.target_branch,
        "current_branch": current_branch,
        "head_sha": head_sha,
        "origin_dev_sha": origin_dev_sha,
        "origin_main_sha": origin_main_sha,
        "ls_remote_dev_sha": ls_remote_dev_sha,
        "ls_remote_main_sha": ls_remote_main_sha,
        "origin_dev_head_ahead_behind": origin_dev_head_ab,
        "origin_main_head_ahead_behind": origin_main_head_ab,
        "origin_main_origin_dev_ahead_behind": origin_main_origin_dev_ab,
        "working_tree_summary": working_tree_summary,
        "working_tree_clean": working_tree_clean,
        "staged_files_count": staged_files_count,
        "modified_files_count": modified_files_count,
        "untracked_files_count": untracked_files_count,
        "untracked_files_summary": untracked_files_summary,
        "last_commit_subject": last_commit_subject,
        "last_commit_changed_files": last_commit_changed_files,
        "analysis_status": analysis_status,
        "warnings": warnings,
        "notes": notes
    }
    
    if args.json:
        print(json.dumps(data, indent=2))
    elif args.compact:
        print(f"**AOS Baseline: {data['analysis_status']}**")
        print(f"Current: {data['current_branch']} | HEAD: {data['head_sha']}")
        print(f"Target: {data['target_branch']} | origin/dev: {data['origin_dev_sha']}")
        print("Safety Notes:")
        for n in data['notes']:
            print(f"- {n}")
    elif args.summary:
        print(f"# AOS Baseline Summary: {data['analysis_status']}\n")
        print(f"**Branch:** {data['current_branch']} | **HEAD:** {data['head_sha']}")
        print(f"**Target:** {data['target_branch']} | **origin/dev:** {data['origin_dev_sha']}")
        print(f"**Ahead/Behind:** origin/dev...HEAD: {data['origin_dev_head_ahead_behind']}")
        print(f"**Working Tree Clean:** {data['working_tree_clean']}")
        if data['untracked_files_summary']:
            print(f"**Untracked:** {len(data['untracked_files_summary'])} files")
        if data['warnings']:
            print("\n**Warnings:**")
            for w in data['warnings']:
                print(f"- {w}")
        print("\n**Safety Notes:**")
        for n in data['notes']:
            print(f"- {n}")
    elif args.markdown:
        print("# AOS Baseline Summary\n")
        
        print("## Generated At")
        print(f"{data['generated_at']}\n")
        
        print("## Project")
        print(f"{data['project']}\n")
        
        print("## Target Branch")
        print(f"{data['target_branch']}\n")
        
        print("## Branch / HEAD")
        print(f"Current Branch: {data['current_branch']}")
        print(f"HEAD SHA: {data['head_sha']}\n")
        
        print("## Remote State")
        print(f"origin/dev: {data['origin_dev_sha']}")
        print(f"origin/main: {data['origin_main_sha']}")
        print(f"ls-remote dev: {data['ls_remote_dev_sha']}")
        print(f"ls-remote main: {data['ls_remote_main_sha']}\n")
        
        print("## Ahead / Behind")
        print(f"origin/dev...HEAD: {data['origin_dev_head_ahead_behind']}")
        print(f"origin/main...HEAD: {data['origin_main_head_ahead_behind']}")
        print(f"origin/main...origin/dev: {data['origin_main_origin_dev_ahead_behind']}\n")
        
        print("## Working Tree")
        print(f"Clean: {data['working_tree_clean']}")
        print(f"Staged: {data['staged_files_count']}")
        print(f"Modified: {data['modified_files_count']}")
        print(f"Untracked: {data['untracked_files_count']}")
        print(f"Summary:\n```\n{data['working_tree_summary']}\n```")
        if data['untracked_files_summary']:
            print("Untracked files:")
            for uf in data['untracked_files_summary']:
                print(f"- {uf}")
        print("\n", end="")
        
        print("## Last Commit")
        print(f"Subject: {data['last_commit_subject']}")
        print("Changed files:")
        for cf in data['last_commit_changed_files']:
            print(f"- {cf}")
        print("\n", end="")
        
        print("## Warnings")
        if data['warnings']:
            for w in data['warnings']:
                print(f"- {w}")
        else:
            print("No warnings.")
        print("\n", end="")
        
        print("## Safety Notes")
        for n in data['notes']:
            print(f"- {n}")
        print("\n", end="")
        
        print("## Analysis Status")
        print(f"**{data['analysis_status']}**")

if __name__ == '__main__':
    main()
