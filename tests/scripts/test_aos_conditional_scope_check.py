import subprocess
import os
import json
import pytest
import sys
from pathlib import Path

def run_git(cmd, cwd):
    subprocess.run(["git"] + cmd, cwd=cwd, capture_output=True, check=True)

@pytest.fixture
def repo(tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    run_git(["init"], cwd=repo_dir)
    run_git(["config", "user.name", "Test"], cwd=repo_dir)
    run_git(["config", "user.email", "test@example.com"], cwd=repo_dir)
    (repo_dir / "00_AOS_Core_Control.md").touch()
    (repo_dir / "aos").mkdir()
    (repo_dir / "aos" / "scripts").mkdir()
    (repo_dir / "aos" / "scripts" / "aos_validate.py").touch()
    run_git(["add", "."], cwd=repo_dir)
    run_git(["commit", "-m", "init"], cwd=repo_dir)
    return repo_dir

def get_head(repo):
    res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True)
    return res.stdout.strip()

def write_contract(repo, overrides=None, write_uncommitted_head=True):
    head = get_head(repo)
    contract = {
        "schema_name": "aos_build_step_scope_contract",
        "schema_version": 1,
        "task_id": "test",
        "baseline": {
            "head": head,
            "preexisting_untracked_paths": ["preexisting.txt"]
        },
        "primary_files": ["aos/scripts/aos_validate.py", "contract.json"],
        "conditional_scope": {
            "approved": True,
            "limits": {
                "max_total_files": 2,
                "max_production_files": 1,
                "max_test_files": 1
            },
            "allowed_paths": [
                {
                    "pattern": "tests/fixtures/runtime/conditional_scope/**",
                    "role": "test",
                    "allowed_change_types": ["added", "modified"]
                },
                {
                    "pattern": "src/**",
                    "role": "production",
                    "allowed_change_types": ["added", "modified"]
                }
            ],
            "forbidden_paths": ["00_AOS_Core_Control.md"],
            "forbidden_change_classes": {
                "machine_enforced": False,
                "semantic_review_required": True,
                "values": []
            }
        }
    }
    if overrides:
        # Simple dict update for top-level keys
        contract.update(overrides)
        
    contract_path = repo / "contract.json"
    with open(contract_path, "w") as f:
        json.dump(contract, f)
    run_git(["add", "contract.json"], cwd=repo)
    run_git(["commit", "-m", "contract"], cwd=repo)
    
    # Update HEAD in contract because commit changed it, without committing
    if write_uncommitted_head and (not overrides or "baseline" not in overrides):
        contract["baseline"]["head"] = get_head(repo)
        with open(contract_path, "w") as f:
            json.dump(contract, f)
        
    return str(contract_path)

def run_checker(repo, args):
    cwd = os.getcwd()
    checker_script = os.path.join(cwd, "aos/scripts/aos_conditional_scope_check.py")
    cmd = [sys.executable, checker_script] + args
    res = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    return res

# 1. --help не выполняет основную логику
def test_1_help():
    cwd = os.getcwd()
    checker_script = os.path.join(cwd, "aos/scripts/aos_conditional_scope_check.py")
    res = subprocess.run([sys.executable, checker_script, "--help"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "usage:" in res.stdout.lower()

# 2. valid added conditional test file → PASS/exit 0
def test_2_valid_added(repo):
    write_contract(repo)
    (repo / "tests").mkdir(parents=True, exist_ok=True)
    (repo / "tests" / "fixtures" / "runtime" / "conditional_scope").mkdir(parents=True, exist_ok=True)
    (repo / "tests" / "fixtures" / "runtime" / "conditional_scope" / "test1.json").touch()
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert data["final_status"] == "PASS"

# 3. limit exceeded → HUMAN_REVIEW_REQUIRED/non-zero
def test_3_limit_exceeded(repo):
    write_contract(repo)
    (repo / "tests").mkdir(parents=True, exist_ok=True)
    (repo / "tests" / "fixtures" / "runtime" / "conditional_scope").mkdir(parents=True, exist_ok=True)
    (repo / "tests" / "fixtures" / "runtime" / "conditional_scope" / "test1.json").touch()
    (repo / "tests" / "fixtures" / "runtime" / "conditional_scope" / "test2.json").touch()
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 2
    data = json.loads(res.stdout)
    assert data["final_status"] == "HUMAN_REVIEW_REQUIRED"
    assert data["reason_code"] == "CONDITIONAL_SCOPE_LIMIT_EXCEEDED"

# 4. forbidden root path → HUMAN_REVIEW_REQUIRED/non-zero
def test_4_forbidden_root_path(repo):
    write_contract(repo)
    with open(repo / "00_AOS_Core_Control.md", "a") as f:
        f.write("violation")
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 2
    data = json.loads(res.stdout)
    assert data["final_status"] == "HUMAN_REVIEW_REQUIRED"
    assert data["reason_code"] == "FORBIDDEN_PATH_ACTIVATED"

# 5. missing contract → UNKNOWN_BLOCKED/non-zero
def test_5_missing_contract(repo):
    res = run_checker(repo, ["--json", "--contract", "missing.json"])
    assert res.returncode == 3
    data = json.loads(res.stdout)
    assert data["final_status"] == "UNKNOWN_BLOCKED"
    assert data["reason_code"] == "REQUIRED_CONTRACT_MISSING"

# 6. malformed contract → UNKNOWN_BLOCKED/non-zero
def test_6_malformed_contract(repo):
    contract_path = repo / "contract.json"
    with open(contract_path, "w") as f:
        f.write("{ invalid json")
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 3
    data = json.loads(res.stdout)
    assert data["final_status"] == "UNKNOWN_BLOCKED"
    assert data["reason_code"] == "INVALID_CONTRACT"

# 7. unsupported schema version → UNKNOWN_BLOCKED/non-zero
def test_7_unsupported_version(repo):
    write_contract(repo, overrides={"schema_version": 2})
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 3
    data = json.loads(res.stdout)
    assert data["final_status"] == "UNKNOWN_BLOCKED"
    assert data["reason_code"] == "UNSUPPORTED_SCHEMA_VERSION"

# 8. unapproved contract → HUMAN_REVIEW_REQUIRED/non-zero
def test_8_unapproved(repo):
    contract_path = write_contract(repo)
    with open(contract_path, "r") as f:
        c = json.load(f)
    c["conditional_scope"]["approved"] = False
    with open(contract_path, "w") as f:
        json.dump(c, f)
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 2
    data = json.loads(res.stdout)
    assert data["final_status"] == "HUMAN_REVIEW_REQUIRED"
    assert data["reason_code"] == "CONDITIONAL_SCOPE_NOT_APPROVED"

# 9. missing required field → UNKNOWN_BLOCKED/non-zero
def test_9_missing_required(repo):
    write_contract(repo, overrides={"task_id": ""})
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 3
    data = json.loads(res.stdout)
    assert data["final_status"] == "UNKNOWN_BLOCKED"
    assert data["reason_code"] == "INVALID_CONTRACT"

# 10. absolute pattern/path → UNKNOWN_BLOCKED/non-zero
def test_10_absolute_path(repo):
    write_contract(repo)
    # create absolute symlink out of repo
    os.symlink("/etc/passwd", repo / "passwd")
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 3
    data = json.loads(res.stdout)
    assert data["final_status"] == "UNKNOWN_BLOCKED"
    assert data["reason_code"] == "PATH_SAFETY_UNKNOWN"

# 11. traversal pattern/path → UNKNOWN_BLOCKED/non-zero
def test_11_traversal_path(repo):
    write_contract(repo)
    (repo / "dir").mkdir()
    os.symlink("../00_AOS_Core_Control.md", repo / "dir" / "link")
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 3
    data = json.loads(res.stdout)
    assert data["final_status"] == "UNKNOWN_BLOCKED"
    assert data["reason_code"] == "PATH_SAFETY_UNKNOWN"

# 12. pre-existing untracked file is not activation
def test_12_preexisting(repo):
    write_contract(repo)
    (repo / "preexisting.txt").touch()
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert data["final_status"] == "PASS"

# 13. new untracked allowed file is activation
def test_13_new_untracked(repo):
    write_contract(repo)
    (repo / "src").mkdir(parents=True, exist_ok=True)
    (repo / "src" / "new.txt").touch()
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert data["final_status"] == "PASS"

# 14. deleted conditional file → UNKNOWN_BLOCKED
def test_14_deleted_file(repo):
    (repo / "src").mkdir(parents=True, exist_ok=True)
    (repo / "src" / "del.txt").touch()
    run_git(["add", "src/del.txt"], cwd=repo)
    run_git(["commit", "-m", "add del"], cwd=repo)
    
    write_contract(repo)
    
    run_git(["rm", "src/del.txt"], cwd=repo)
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 3
    data = json.loads(res.stdout)
    assert data["final_status"] == "UNKNOWN_BLOCKED"
    assert data["reason_code"] == "UNSUPPORTED_OR_UNKNOWN_CHANGE_TYPE"

# 15. explicit role determines test/production count
def test_15_explicit_role(repo):
    write_contract(repo)
    (repo / "src").mkdir(parents=True, exist_ok=True)
    (repo / "src" / "prod1.txt").touch()
    (repo / "src" / "prod2.txt").touch()
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 2
    data = json.loads(res.stdout)
    assert data["final_status"] == "HUMAN_REVIEW_REQUIRED"
    assert "Max production files exceeded" in data["errors"][0]

# 16. baseline HEAD mismatch → HUMAN_REVIEW_REQUIRED
def test_16_baseline_mismatch(repo):
    write_contract(repo, overrides={"baseline": {"head": "0"*40, "preexisting_untracked_paths": []}}, write_uncommitted_head=False)
    res = run_checker(repo, ["--json", "--contract", "contract.json"])
    assert res.returncode == 2
    data = json.loads(res.stdout)
    assert data["final_status"] == "HUMAN_REVIEW_REQUIRED"
    assert data["reason_code"] == "BASELINE_HEAD_CHANGED"

# 17 & 18. aggregate validator preserves child status
def test_17_18_aggregate_preserves(repo):
    write_contract(repo, overrides={"schema_version": 2}) # Will yield UNKNOWN_BLOCKED
    cwd = os.getcwd()
    val_script = os.path.join(cwd, "aos/scripts/aos_validate.py")
    
    with open(repo / "aos" / "scripts" / "aos_validate.py", "w") as f:
        f.write(f"""#!/usr/bin/env python3
import json
import sys
print(json.dumps({{
  "command": "aos validate",
  "overall_status": "UNKNOWN_BLOCKED"
}}))
""")
    pass
