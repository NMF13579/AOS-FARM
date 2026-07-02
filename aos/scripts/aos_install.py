#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path

def get_repo_root():
    current_dir = Path.cwd().resolve()
    while current_dir.name != '':
        if (current_dir / '.git').exists():
            return current_dir
        if current_dir.parent == current_dir:
            break
        current_dir = current_dir.parent
    
    # Fallback to current working directory if .git is not found
    return Path.cwd().resolve()

def check_path_safety(target_path: Path, repo_root: Path):
    try:
        # Prevent escaping repo root
        if not target_path.resolve().is_relative_to(repo_root.resolve()):
            return False, "target path escapes repo root"
    except ValueError:
        return False, "target path escapes repo root or ambiguous"
    
    # Prevent writing into .git/
    if ".git" in target_path.parts:
        return False, "target path points into .git/"
        
    # Prevent writing into .aos-tmp/
    if ".aos-tmp" in target_path.parts:
        return False, "target path points into /.aos-tmp/"
        
    # Prevent product code inside /project/
    # /project/ is documentation workspace
    if "project" in target_path.parts:
        idx = target_path.parts.index("project")
        if idx + 1 < len(target_path.parts):
            sub_folder = target_path.parts[idx+1]
            forbidden_project_folders = {"src", "tests", "app", "pages", "public", "lib", "backend", "frontend"}
            if sub_folder in forbidden_project_folders:
                return False, f"planned product code inside /project/ ({sub_folder})"
                
    return True, ""

def format_install_plan(status, apply_status, source_root, target_root, planned_creates, existing_targets, conflicts, warnings, blocked_reasons):
    plan = []
    plan.append("# AOS-FARM Installer Plan\n")
    plan.append(f"**install_status:** {status}")
    plan.append(f"**apply_status:** {apply_status}\n")
    plan.append(f"**source_root:** `{source_root}`")
    plan.append(f"**target_root:** `{target_root}`\n")
    plan.append("## WARNING")
    plan.append("This install plan is Evidence only.")
    plan.append("Evidence is not approval.")
    plan.append("Dry-run PASS is not approval.")
    plan.append("Human approval cannot be simulated.\n")
    plan.append("---")
    
    plan.append("\n### planned_creates")
    if planned_creates:
        for p in planned_creates:
            plan.append(f"- {p}")
    else:
        plan.append("- [none]")

    plan.append("\n### existing_targets")
    if existing_targets:
        for e in existing_targets:
            plan.append(f"- {e}")
    else:
        plan.append("- [none]")

    plan.append("\n### conflicts")
    if conflicts:
        for c in conflicts:
            plan.append(f"- {c['source']} -> {c['target']} ({c['reason']})")
    else:
        plan.append("- [none]")

    plan.append("\n### warnings")
    if warnings:
        for w in warnings:
            plan.append(f"- {w}")
    else:
        plan.append("- [none]")

    plan.append("\n### blocked_reasons")
    if blocked_reasons:
        for b in blocked_reasons:
            plan.append(f"- {b}")
    else:
        plan.append("- [none]")

    plan.append("\n---")
    plan.append("\n**approval_claimed:** false")
    plan.append("**execution_authorized:** false")
    plan.append("**files_changed:** false")

    return "\n".join(plan)

def run_dry_run():
    repo_root = get_repo_root()
    aos_root = repo_root / "aos" / "root"
    
    planned_creates = []
    existing_targets = []
    conflicts = []
    warnings = []
    blocked_reasons = []
    
    status = "UNKNOWN_BLOCKED"
    
    if not aos_root.exists() or not aos_root.is_dir():
        blocked_reasons.append("/aos/root/ is missing or not a directory")
        status = "BLOCKED"
    else:
        for root, _, files in os.walk(aos_root):
            for file in files:
                source_file = Path(root) / file
                relative_path = source_file.relative_to(aos_root)
                target_file = repo_root / relative_path
                
                safe, reason = check_path_safety(target_file, repo_root)
                if not safe:
                    blocked_reasons.append(f"Unsafe path {relative_path}: {reason}")
                    continue
                
                if target_file.exists():
                    existing_targets.append(f"/{relative_path}")
                    conflicts.append({
                        "source": f"aos/root/{relative_path}",
                        "target": f"{relative_path}",
                        "reason": "target file already exists"
                    })
                else:
                    planned_creates.append(f"aos/root/{relative_path} -> /{relative_path}")

        if blocked_reasons:
            status = "BLOCKED"
        elif conflicts:
            status = "HUMAN_REVIEW_REQUIRED"
        elif warnings:
            status = "PASS_WITH_WARNINGS"
        else:
            status = "PASS"

    plan = format_install_plan(
        status=status,
        apply_status="NOT_IMPLEMENTED",
        source_root="/aos/root/",
        target_root="/",
        planned_creates=planned_creates,
        existing_targets=existing_targets,
        conflicts=conflicts,
        warnings=warnings,
        blocked_reasons=blocked_reasons
    )
    print(plan)

def main():
    parser = argparse.ArgumentParser(description="AOS Installer")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry-run install")
    parser.add_argument("--apply", action="store_true", help="Apply the install plan")
    
    args = parser.parse_args()
    
    if args.apply:
        print("install_status: BLOCKED")
        print("apply_status: NOT_IMPLEMENTED")
        print("files_changed: false")
        print("approval_claimed: false")
        print("execution_authorized: false")
        sys.exit(0)
    elif args.dry_run:
        run_dry_run()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
