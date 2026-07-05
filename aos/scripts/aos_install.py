#!/usr/bin/env python3
import os
import sys
import argparse
import shutil
from pathlib import Path

FIXED_AOS_GITIGNORE_BLOCK = """
# AOS local temporary workspace
/.aos-tmp/
"""

def get_repo_root():
    current_dir = Path.cwd().resolve()
    while current_dir.name != '':
        if (current_dir / '.git').exists():
            return current_dir
        if current_dir.parent == current_dir:
            break
        current_dir = current_dir.parent
    return Path.cwd().resolve()

def check_path_safety(target_path: Path, repo_root: Path):
    try:
        if not target_path.resolve().is_relative_to(repo_root.resolve()):
            return False, "target path escapes repo root"
    except ValueError:
        return False, "target path escapes repo root or ambiguous"

    if ".git" in target_path.parts:
        return False, "target path points into .git/"
    if ".aos-tmp" in target_path.parts:
        return False, "target path points into /.aos-tmp/"
    if "project" in target_path.parts:
        idx = target_path.parts.index("project")
        if idx + 1 < len(target_path.parts):
            sub_folder = target_path.parts[idx+1]
            forbidden_project_folders = {"src", "tests", "app", "pages", "public", "lib", "backend", "frontend"}
            if sub_folder in forbidden_project_folders:
                return False, f"planned product code inside /project/ ({sub_folder})"

    return True, ""

def is_gitignore_safe(target_file: Path):
    if not target_file.exists():
        return True, "missing"
    try:
        content = target_file.read_text(encoding="utf-8")
        if "\0" in content:
            return False, "binary-like content"
        if "<<<<<<< HEAD" in content or "=======" in content or ">>>>>>>" in content:
            return False, "merge conflict markers found"
        return True, content
    except UnicodeDecodeError:
        return False, "encoding failure (not utf-8)"
    except Exception as e:
        return False, f"not readable: {e}"

def build_install_plan(target_repo_root: Path, source_package_root: Path):
    plan = {
        "planned_creates": [],
        "existing_targets": [],
        "conflicts": [],
        "warnings": [],
        "blocked_reasons": [],
        "status": "UNKNOWN_BLOCKED",
        "actions": [] # List of tuples (action_type, source, target, meta)
    }

    aos_source = source_package_root / "aos"
    aos_root = aos_source / "root"

    if not aos_source.exists() or not aos_source.is_dir():
        plan["blocked_reasons"].append(f"source package /aos/ is missing or not a directory: {aos_source}")
        plan["status"] = "BLOCKED"
        return plan

    if not aos_root.exists() or not aos_root.is_dir():
        plan["blocked_reasons"].append(f"source package /aos/root/ is missing or not a directory: {aos_root}")
        plan["status"] = "BLOCKED"
        return plan

    # Plan for /aos/ folder
    target_aos = target_repo_root / "aos"
    if target_aos.exists():
        plan["existing_targets"].append("/aos/")
        plan["conflicts"].append({
            "source": "aos/",
            "target": "aos/",
            "reason": "target folder already exists"
        })
    else:
        plan["planned_creates"].append("aos/ -> /aos/")
        plan["actions"].append(("copy_tree", aos_source, target_aos, None))

    # Plan for root files
    for root, _, files in os.walk(aos_root):
        for file in files:
            source_file = Path(root) / file
            relative_path = source_file.relative_to(aos_root)
            relative_str = str(relative_path).replace("\\", "/")

            if relative_str in ["ROOT_INSTALL_GUIDE.md", "ROOT_FILES_MANIFEST.md", "gitignore.snippet"]:
                continue

            if relative_str in ["README_AOS_SECTION.md", "README.md"]:
                continue # Do not modify README in this stage

            if relative_str.startswith(".github/workflows/"):
                continue # Do not touch workflows in this stage

            target_file = target_repo_root / relative_path
            safe, reason = check_path_safety(target_file, target_repo_root)
            if not safe:
                plan["blocked_reasons"].append(f"Unsafe path {relative_path}: {reason}")
                continue

            if relative_str == ".gitignore.template":
                target_file = target_repo_root / ".gitignore"
                safe, reason_or_content = is_gitignore_safe(target_file)
                if not safe:
                    plan["conflicts"].append({"source": "aos/root/.gitignore.template", "target": ".gitignore", "reason": f"unsafe .gitignore: {reason_or_content}"})
                elif reason_or_content == "missing":
                    plan["planned_creates"].append("aos/root/.gitignore.template -> /.gitignore")
                    plan["actions"].append(("create", source_file, target_file, None))
                else:
                    if "/.aos-tmp/" in reason_or_content:
                        plan["actions"].append(("no_change", source_file, target_file, "already contains /.aos-tmp/"))
                    else:
                        plan["planned_creates"].append("fixed AOS block -> existing /.gitignore append")
                        plan["actions"].append(("append_gitignore", None, target_file, FIXED_AOS_GITIGNORE_BLOCK))
                continue

            if target_file.exists():
                plan["existing_targets"].append(f"/{relative_path}")
                plan["conflicts"].append({
                    "source": f"aos/root/{relative_path}",
                    "target": f"{relative_path}",
                    "reason": "target file already exists"
                })
            else:
                plan["planned_creates"].append(f"aos/root/{relative_path} -> /{relative_path}")
                plan["actions"].append(("create", source_file, target_file, None))

    if plan["blocked_reasons"]:
        plan["status"] = "BLOCKED"
    elif plan["conflicts"]:
        plan["status"] = "HUMAN_REVIEW_REQUIRED"
    elif plan["warnings"]:
        plan["status"] = "PASS_WITH_WARNINGS"
    else:
        plan["status"] = "PASS"

    return plan

def format_install_plan(plan, apply_status, source_root, target_root):
    output = []
    output.append("# AOS-FARM Installer Plan\n")
    output.append(f"**install_status:** {plan['status']}")
    output.append(f"**apply_status:** {apply_status}\n")
    output.append(f"**source_root:** `{source_root}`")
    output.append(f"**target_root:** `{target_root}`\n")
    output.append("## WARNING")
    output.append("This install plan is Evidence only.")
    output.append("Evidence is not approval.")
    output.append("Dry-run PASS is not approval.")
    output.append("Human approval cannot be simulated.\n")
    output.append("---")

    output.append("\n### planned_creates")
    if plan["planned_creates"]:
        for p in plan["planned_creates"]:
            output.append(f"- {p}")
    else:
        output.append("- [none]")

    output.append("\n### existing_targets")
    if plan["existing_targets"]:
        for e in plan["existing_targets"]:
            output.append(f"- {e}")
    else:
        output.append("- [none]")

    output.append("\n### conflicts")
    if plan["conflicts"]:
        for c in plan["conflicts"]:
            output.append(f"- {c['source']} -> {c['target']} ({c['reason']})")
    else:
        output.append("- [none]")

    output.append("\n### warnings")
    if plan["warnings"]:
        for w in plan["warnings"]:
            output.append(f"- {w}")
    else:
        output.append("- [none]")

    output.append("\n### blocked_reasons")
    if plan["blocked_reasons"]:
        for b in plan["blocked_reasons"]:
            output.append(f"- {b}")
    else:
        output.append("- [none]")

    output.append("\n---")
    output.append("\n**approval_claimed:** false")
    output.append("**execution_authorized:** false")

    return "\n".join(output)

def print_tutor_explanation(plan, apply_mode_requested, apply_status):
    print("\n" + "="*50)
    print("TUTOR EXPLANATION")
    print("="*50)
    print("Tutor output is explanatory only.")
    print("Tutor output is not approval.")
    print("Tutor output does not authorize execution, commit, push, merge, or release.\n")

    if apply_status == "APPLY_DONE":
        print("Apply was completed successfully.")
        print("The target repo now has the required AOS first-start files.")
        print("Apply DONE is not approval.")
        print("READY_FOR_FIRST_START is not execution authorization.")
        print("="*50 + "\n")
        return

    print("What was found in the repository:")
    if plan["existing_targets"]:
        print("  Existing AOS target paths found. (e.g. AGENTS.md, llms.txt, or aos folder)")
    else:
        print("  No conflicting AOS target paths found.")

    print("\nWhat the installer wants to create:")
    if plan["planned_creates"]:
        for p in plan["planned_creates"]:
            print(f"  * {p}")
    else:
        print("  Nothing to create.")

    print("\nWhy apply is allowed or blocked:")
    print("  Safe apply is for first deployment from an AOS package into a target repo where /aos/ does not already exist.")
    if plan["status"] == "PASS":
        if apply_mode_requested:
            print(f"  Apply was blocked ({apply_status}) because exact confirmation or required flags were missing.")
        else:
            print("  Apply is allowed because there are no existing target files. Run with --apply, --safe-create-and-gitignore-append, and exact --confirm to execute.")
    else:
        print(f"  Apply is blocked (install_status: {plan['status']}) due to conflicts or blockers. HUMAN_REVIEW_REQUIRED.")
        print("  If /aos/ already exists, safe apply stops rather than merge or overwrite. Use self-test, Doctor, and manual root template review instead.")
        print("  Note: manual copy ≠ safe apply, dry-run PASS ≠ installed, safe apply conflict ≠ failure to approve.")

    print("\nWhy AGENTS.md and llms.txt are not modified automatically:")
    print("  These are canonical safety and control boundaries. Only a Human is authorized to merge or approve changes to them.")

    print("\nWhat will be done with .gitignore:")
    print("  Only a controlled append of the fixed AOS block (/.aos-tmp/) is permitted if the file is safe to modify.")

    print("\nWhat does HUMAN_REVIEW_REQUIRED mean?")
    print("  It means the installer encountered a state it cannot safely overwrite or resolve. A Human must inspect the conflict and decide how to proceed manually.")

    print("\nWhat does READY_FOR_FIRST_START mean?")
    print("  It means all required files exist on disk, and you can now proceed with AOS initialization.")

    print("\nWhat to do next:")
    if plan["status"] == "PASS" and apply_status != "APPLY_DONE":
        print("  Provide explicit confirmation to safely create the files.")
    elif apply_status == "APPLY_DONE" or plan["status"] == "HUMAN_REVIEW_REQUIRED":
        print("  Inspect the working tree, manually resolve any remaining conflicts, and follow the FIRST-START guide.")
    print("="*50 + "\n")


def apply_plan(plan):
    files_changed = []

    for action, source, target, meta in plan["actions"]:
        if action == "create":
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            files_changed.append(str(target))
        elif action == "copy_tree":
            shutil.copytree(source, target, dirs_exist_ok=True)
            files_changed.append(str(target))
        elif action == "append_gitignore":
            with target.open("a", encoding="utf-8") as f:
                if target.stat().st_size > 0:
                    try:
                        with target.open("r", encoding="utf-8") as r:
                            content = r.read()
                            if not content.endswith("\n"):
                                f.write("\n")
                    except:
                        f.write("\n")
                f.write(meta)
            files_changed.append(str(target))

    return files_changed

def main(source_package_root=None):
    parser = argparse.ArgumentParser(description="AOS Installer")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry-run install")
    parser.add_argument("--apply", action="store_true", help="Apply the install plan")
    parser.add_argument("--safe-create-and-gitignore-append", action="store_true", help="Explicit mode to safely create and append to .gitignore")
    parser.add_argument("--confirm", type=str, help="Exact confirmation string")
    parser.add_argument("--tutor", action="store_true", help="Enable Tutor explanation mode")

    args = parser.parse_args()

    target_repo_root = get_repo_root()

    if source_package_root is None:
        # Resolve source_package_root from this script: scripts/aos -> aos -> AOS-FARM
        source_package_root = Path(__file__).resolve().parent.parent.parent
    else:
        source_package_root = Path(source_package_root)

    plan = build_install_plan(target_repo_root, source_package_root)

    apply_status = "NOT_REQUESTED"
    files_changed = []
    pre_apply_plan_status = plan["status"]

    if args.apply:
        if not args.safe_create_and_gitignore_append:
            print("apply_status: APPLY_BLOCKED")
            print("reason: explicit safe apply mode flag required")
            print("files_changed: []")
            print("partial_writes: false")
            sys.exit(1)
        elif args.confirm is None:
            print("apply_status: APPLY_BLOCKED")
            print("reason: explicit Human confirmation required")
            print("files_changed: []")
            print("partial_writes: false")
            sys.exit(1)
        elif args.confirm != "AOS INSTALL SAFE CREATE OK":
            print("apply_status: APPLY_BLOCKED")
            print("reason: exact Human confirmation string mismatch")
            print("files_changed: []")
            print("partial_writes: false")
            sys.exit(1)
        elif plan["status"] not in ["PASS", "PASS_WITH_WARNINGS"]:
            print(f"apply_status: {plan['status']}")
            print("reason: blockers or conflicts exist")
            print("files_changed: []")
            print("partial_writes: false")
            if args.tutor:
                print_tutor_explanation(plan, True, plan["status"])
            sys.exit(1)
        else:
            # Plan is PASS and confirmations match.
            apply_status = "APPLY_DONE"
            files_changed = apply_plan(plan)
    elif not args.dry_run:
        # Default is dry-run essentially, if nothing provided
        # Let's see prompt for `python aos_install.py` without args
        parser.print_help()
        sys.exit(1)

    if args.apply and apply_status == "APPLY_DONE":
        print(f"pre_apply_plan_status: {pre_apply_plan_status}")
        print("apply_status: APPLY_DONE")
        print("target_install_state: INSTALLED")
        print("installation_readiness: READY_FOR_FIRST_START")
        print("approval_claimed: false")
        print("execution_authorized: false")
        print(f"**files_changed:** {files_changed}")
    else:
        formatted_plan = format_install_plan(
            plan,
            apply_status,
            "/aos/root/",
            "/"
        )
        print(formatted_plan)
        print("**files_changed:** []")

    if args.tutor:
        print_tutor_explanation(plan, args.apply, apply_status)

if __name__ == "__main__":
    main()
