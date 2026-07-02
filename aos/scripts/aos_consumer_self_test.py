#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from pathlib import Path

def get_repo_root():
    current_dir = Path.cwd().resolve()
    while current_dir.name != '':
        if (current_dir / '.git').exists():
            return current_dir
        if current_dir.parent == current_dir:
            break
        current_dir = current_dir.parent
    return Path.cwd().resolve()

def check_package_integrity(repo_root):
    required_files = [
        "aos/docs/ROUTES.md",
        "aos/docs/START-RU.md",
        "aos/docs/INSTALL.md",
        "aos/docs/STORAGE.md",
        "aos/docs/AUTHORIZATION-COMMANDS.md",
        "aos/docs/AGENT-ENTRYPOINTS.md",
        "aos/docs/SELF-TEST.md",
        "aos/docs/WORKSPACE-BOUNDARY.md",
        "aos/scripts/aos_install.py",
        "aos/scripts/aos_consumer_self_test.py",
        "aos/templates/install-plan.md",
        "aos/root/llms.txt",
        "aos/root/AGENTS.md"
    ]
    
    missing = []
    for f in required_files:
        if not (repo_root / f).exists():
            missing.append(f)
            
    advisory_template = "aos/root/.github/workflows/aos-advisory.yml"
    advisory_present = (repo_root / advisory_template).exists()
    
    status = "PASS"
    warnings = []
    
    if missing:
        status = "BLOCKED"
    elif not advisory_present:
        warnings.append(f"{advisory_template} is missing (optional)")
        status = "PASS_WITH_WARNINGS"
        
    return {
        "status": status,
        "missing_required": missing,
        "advisory_template_present": advisory_present,
        "warnings": warnings
    }

def check_target_install_state(repo_root):
    state = {}
    warnings = []
    human_review = False
    
    # Check advisory workflow
    adv_target = repo_root / ".github/workflows/aos-advisory.yml"
    adv_template = repo_root / "aos/root/.github/workflows/aos-advisory.yml"
    if adv_target.exists():
        state["advisory_workflow"] = "deployed"
    elif adv_template.exists():
        state["advisory_workflow"] = "pending_from_template"
    else:
        state["advisory_workflow"] = "missing_template"
        
    # Check llms.txt
    if (repo_root / "llms.txt").exists():
        state["llms.txt"] = "deployed"
    elif (repo_root / "aos/root/llms.txt").exists():
        state["llms.txt"] = "pending_from_template"
    else:
        state["llms.txt"] = "missing_template"
        
    # Check AGENTS.md
    if (repo_root / "AGENTS.md").exists():
        state["AGENTS.md"] = "deployed"
    elif (repo_root / "aos/root/AGENTS.md").exists():
        state["AGENTS.md"] = "pending_from_template"
    else:
        state["AGENTS.md"] = "missing_template"
        
    # Check project workspace boundary
    forbidden_project_folders = ["src", "tests", "app", "pages", "public", "lib", "backend", "frontend"]
    found_forbidden = []
    if (repo_root / "project").exists():
        for f in forbidden_project_folders:
            if (repo_root / "project" / f).exists():
                found_forbidden.append(f"project/{f}")
                
    if found_forbidden:
        warnings.append(f"Unexpected product code folders found: {', '.join(found_forbidden)}")
        human_review = True
        
    # Check .aos-tmp boundary
    tmp_dir = repo_root / ".aos-tmp"
    found_in_tmp = []
    if tmp_dir.exists() and tmp_dir.is_dir():
        for file in tmp_dir.rglob('*'):
            if file.is_file():
                f = file.name.lower()
                if "report" in f or "evidence" in f or f in ["agents.md", "llms.txt", "task.md", "00_aos_core_control.md"]:
                    found_in_tmp.append(str(file.relative_to(tmp_dir)))
                    
    if found_in_tmp:
        warnings.append(f"Source of Truth artifacts found in /.aos-tmp/: {', '.join(found_in_tmp)}")
        human_review = True
        
    status = "HUMAN_REVIEW_REQUIRED" if human_review else "PASS"
    
    return {
        "status": status,
        "file_states": state,
        "unexpected_project_folders": found_forbidden,
        "unexpected_tmp_files": found_in_tmp,
        "warnings": warnings
    }

def get_safety_boundaries():
    return [
        "self-test PASS ≠ approval",
        "self-test PASS ≠ execution permission",
        "self-test PASS ≠ apply permission",
        "self-test PASS ≠ push permission",
        "self-test PASS ≠ release permission",
        "Evidence ≠ approval",
        "CI PASS ≠ approval",
        "UNKNOWN ≠ OK",
        "NOT_RUN ≠ PASS",
        "Human approval cannot be simulated",
        "/.aos-tmp/ is never Source of Truth"
    ]

def run_installer_dry_run(repo_root):
    installer_script = repo_root / "aos/scripts/aos_install.py"
    if not installer_script.exists():
        return {"status": "NOT_RUN", "evidence": "Installer script missing"}
        
    try:
        # Run safely as read-only subprocess
        result = subprocess.run(
            [sys.executable, str(installer_script), "--dry-run"],
            cwd=str(repo_root),
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        status_line = "UNKNOWN"
        for line in output.split('\n'):
            if "install_status:" in line:
                status_line = line.split("install_status:")[1].strip()
                
        return {
            "status": "COMPLETED",
            "dry_run_install_status": status_line,
            "evidence_note": "Dry-run output is Evidence only."
        }
    except Exception as e:
        return {"status": "NOT_RUN", "evidence": f"Failed to execute dry-run: {str(e)}"}

def calculate_final_status(pkg_status, tgt_status):
    if pkg_status == "BLOCKED" or tgt_status == "BLOCKED":
        return "BLOCKED"
    if pkg_status == "UNKNOWN_BLOCKED" or tgt_status == "UNKNOWN_BLOCKED":
        return "UNKNOWN_BLOCKED"
    if pkg_status == "HUMAN_REVIEW_REQUIRED" or tgt_status == "HUMAN_REVIEW_REQUIRED":
        return "HUMAN_REVIEW_REQUIRED"
    if pkg_status == "PASS_WITH_WARNINGS" or tgt_status == "PASS_WITH_WARNINGS":
        return "PASS_WITH_WARNINGS"
    return "PASS"

def main():
    repo_root = get_repo_root()
    
    pkg_res = check_package_integrity(repo_root)
    tgt_res = check_target_install_state(repo_root)
    dry_run_res = run_installer_dry_run(repo_root)
    safety = get_safety_boundaries()
    
    final_status = calculate_final_status(pkg_res["status"], tgt_res["status"])
    
    report = {
        "stage": "AOS-FARM.581",
        "command": "Consumer Self-Test",
        "package_integrity": pkg_res,
        "target_install_state": tgt_res,
        "installer_dry_run": dry_run_res,
        "safety_boundaries": safety,
        "final_status": final_status
    }
    
    # 1. Human readable summary
    print("=== AOS Consumer Self-Test ===")
    print(f"Package Integrity: {pkg_res['status']}")
    if pkg_res['missing_required']:
        print("  Missing: " + ", ".join(pkg_res['missing_required']))
    if pkg_res['warnings']:
        for w in pkg_res['warnings']:
            print(f"  Warning: {w}")
            
    print(f"\nTarget Install State: {tgt_res['status']}")
    for f, state in tgt_res['file_states'].items():
        print(f"  {f}: {state}")
    if tgt_res['warnings']:
        for w in tgt_res['warnings']:
            print(f"  Warning: {w}")
            
    print(f"\nInstaller Dry-Run (Evidence Only): {dry_run_res.get('dry_run_install_status', 'NOT_RUN')}")
    
    print("\nSafety Boundaries:")
    for s in safety:
        print(f"  {s}")
        
    print(f"\nFinal Status: {final_status}")
    print("==============================\n")
    
    # 2. Machine-readable block
    print("--- JSON REPORT ---")
    print(json.dumps(report, indent=2))
    print("-------------------")
    
    # Return non-zero if blocked
    if final_status in ["BLOCKED", "UNKNOWN_BLOCKED"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
