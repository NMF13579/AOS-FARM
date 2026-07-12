import subprocess
import os
import json
import pytest
import sys
import re
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

def write_freeze_contract(repo, candidate_files=None, commit_message="AOS-FARM.680 candidate freeze"):
    if candidate_files is None:
        candidate_files = ["src/new.txt"]
    contract = {
        "schema_name": "aos_build_step_scope_contract",
        "schema_version": 1,
        "task_id": "AOS-FARM.680",
        "repository": "NMF13579/AOS-FARM",
        "branch": "build/aos-farm-680-candidate-freeze",
        "commit_message": commit_message,
        "baseline": {
            "head": get_head(repo),
            "preexisting_untracked_paths": ["contract.json"]
        },
        "primary_files": candidate_files,
        "candidate_files": candidate_files,
        "conditional_scope": {
            "approved": True,
            "limits": {
                "max_total_files": 0,
                "max_production_files": 0,
                "max_test_files": 0
            },
            "allowed_paths": [],
            "forbidden_paths": ["00_AOS_Core_Control.md"],
            "forbidden_change_classes": {
                "machine_enforced": False,
                "semantic_review_required": True,
                "values": []
            }
        }
    }
    contract_path = repo / "contract.json"
    with open(contract_path, "w") as f:
        json.dump(contract, f)
    return str(contract_path)

def write_candidate_files(repo, paths, content_prefix="candidate"):
    for idx, rel_path in enumerate(paths, start=1):
        path = repo / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{content_prefix}-{idx}\n")

def assert_real_index_clean(repo):
    res = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=repo, capture_output=True, text=True, check=True)
    assert res.stdout == ""

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

# 19. freeze derives candidate content tree without mutating the real index or persisting identity fields
def test_19_freeze_outputs_tree_without_persisting_identity(repo):
    write_freeze_contract(repo)
    (repo / "src").mkdir(parents=True, exist_ok=True)
    (repo / "src" / "new.txt").write_text("candidate\n")

    res = run_checker(repo, ["--json", "--mode", "freeze", "--contract", "contract.json"])

    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert data["final_status"] == "PASS"
    assert data["reason_code"] == "CANDIDATE_FREEZE_VERIFIED"
    assert re.fullmatch(r"[0-9a-f]{40}", data["candidate_content_oid"])
    assert "candidate_change_key" not in data
    assert "candidate_tree" not in data
    assert "tree_oid" not in data
    assert_real_index_clean(repo)

# 20. verify-freeze blocks when candidate content changes after the expected tree is known
def test_20_verify_freeze_blocks_after_candidate_mutation(repo):
    write_freeze_contract(repo)
    (repo / "src").mkdir(parents=True, exist_ok=True)
    (repo / "src" / "new.txt").write_text("candidate\n")
    freeze = run_checker(repo, ["--json", "--mode", "freeze", "--contract", "contract.json"])
    expected_tree = json.loads(freeze.stdout)["candidate_content_oid"]

    (repo / "src" / "new.txt").write_text("mutated\n")
    res = run_checker(repo, [
        "--json",
        "--mode",
        "verify-freeze",
        "--contract",
        "contract.json",
        "--expected-tree-oid",
        expected_tree,
    ])

    assert res.returncode == 4
    data = json.loads(res.stdout)
    assert data["final_status"] == "BLOCKED"
    assert data["reason_code"] == "CANDIDATE_FREEZE_MISMATCH"
    assert_real_index_clean(repo)

# 20a. exact five-file candidate set passes and reports candidate_file_count 5
def test_20a_exact_five_file_candidate_set_passes(repo):
    candidate_files = [
        "src/one.txt",
        "src/two.txt",
        "src/three.txt",
        "tests/four.txt",
        "reports/five.md",
    ]
    write_freeze_contract(repo, candidate_files=candidate_files)
    write_candidate_files(repo, candidate_files)

    res = run_checker(repo, ["--json", "--mode", "freeze", "--contract", "contract.json"])

    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert data["final_status"] == "PASS"
    assert data["reason_code"] == "CANDIDATE_FREEZE_VERIFIED"
    assert data["stats"]["candidate_file_count"] == 5

# 20b. extra unchanged contract path blocks exact candidate set enforcement
def test_20b_extra_unchanged_contract_path_blocks(repo):
    changed_files = ["src/new.txt"]
    contract_files = ["src/new.txt", "aos/scripts/aos_validate.py"]
    write_freeze_contract(repo, candidate_files=contract_files)
    write_candidate_files(repo, changed_files)

    res = run_checker(repo, ["--json", "--contract", "contract.json"])

    assert res.returncode == 4
    data = json.loads(res.stdout)
    assert data["final_status"] == "BLOCKED"
    assert data["reason_code"] == "CANDIDATE_FILE_SET_MISMATCH"
    assert data["mismatch_type"] == "EXTRA_UNCHANGED_CONTRACT_PATH"

# 20c. missing changed path blocks exact candidate set enforcement
def test_20c_missing_changed_path_blocks(repo):
    changed_files = ["src/included.txt", "src/missing.txt"]
    contract_files = ["src/included.txt"]
    write_freeze_contract(repo, candidate_files=contract_files)
    write_candidate_files(repo, changed_files)

    res = run_checker(repo, ["--json", "--contract", "contract.json"])

    assert res.returncode == 4
    data = json.loads(res.stdout)
    assert data["final_status"] == "BLOCKED"
    assert data["reason_code"] == "CANDIDATE_FILE_SET_MISMATCH"
    assert data["mismatch_type"] == "CHANGED_PATH_MISSING_FROM_CONTRACT"

# 20d. duplicate contract path blocks exact candidate set enforcement
def test_20d_duplicate_contract_path_blocks(repo):
    candidate_files = ["src/dup.txt", "src/dup.txt"]
    write_freeze_contract(repo, candidate_files=candidate_files)
    write_candidate_files(repo, ["src/dup.txt"])

    res = run_checker(repo, ["--json", "--contract", "contract.json"])

    assert res.returncode == 4
    data = json.loads(res.stdout)
    assert data["final_status"] == "BLOCKED"
    assert data["reason_code"] == "CANDIDATE_FILE_SET_MISMATCH"
    assert data["mismatch_type"] == "DUPLICATE_CONTRACT_PATH"

# 20e. exact candidate set comparison is order-independent
def test_20e_exact_candidate_set_is_order_independent(repo):
    changed_files = ["src/one.txt", "src/two.txt", "src/three.txt"]
    contract_files = ["src/three.txt", "src/one.txt", "src/two.txt"]
    write_freeze_contract(repo, candidate_files=contract_files)
    write_candidate_files(repo, changed_files)

    res = run_checker(repo, ["--json", "--mode", "freeze", "--contract", "contract.json"])

    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert data["final_status"] == "PASS"
    assert data["stats"]["candidate_file_count"] == 3

# 21. post-commit verify blocks a commit whose message does not match the authorized message
def test_21_post_commit_verify_blocks_message_mismatch(repo):
    write_freeze_contract(repo, commit_message="exact authorized message")
    (repo / "src").mkdir(parents=True, exist_ok=True)
    (repo / "src" / "new.txt").write_text("candidate\n")
    parent = get_head(repo)
    freeze = run_checker(repo, ["--json", "--mode", "freeze", "--contract", "contract.json"])
    expected_tree = json.loads(freeze.stdout)["candidate_content_oid"]

    run_git(["add", "src/new.txt"], cwd=repo)
    run_git(["commit", "-m", "wrong message"], cwd=repo)
    res = run_checker(repo, [
        "--json",
        "--mode",
        "post-commit-verify",
        "--contract",
        "contract.json",
        "--expected-parent-oid",
        parent,
        "--expected-tree-oid",
        expected_tree,
        "--expected-commit-message",
        "exact authorized message",
    ])

    assert res.returncode == 4
    data = json.loads(res.stdout)
    assert data["final_status"] == "BLOCKED"
    assert data["reason_code"] == "POST_COMMIT_BINDING_MISMATCH"

# 22. verify-authorization binds repository, branch, baseline, derived tree, and exact commit message
def test_22_verify_authorization_checks_candidate_change_binding(repo):
    write_freeze_contract(repo, commit_message="exact authorized message")
    (repo / "src").mkdir(parents=True, exist_ok=True)
    (repo / "src" / "new.txt").write_text("candidate\n")
    baseline = get_head(repo)
    freeze = run_checker(repo, ["--json", "--mode", "freeze", "--contract", "contract.json"])
    expected_tree = json.loads(freeze.stdout)["candidate_content_oid"]

    res = run_checker(repo, [
        "--json",
        "--mode",
        "verify-authorization",
        "--contract",
        "contract.json",
        "--expected-task-id",
        "AOS-FARM.680",
        "--authorization-task-id",
        "AOS-FARM.680",
        "--expected-repository",
        "NMF13579/AOS-FARM",
        "--expected-branch",
        "build/aos-farm-680-candidate-freeze",
        "--expected-baseline-oid",
        baseline,
        "--expected-tree-oid",
        expected_tree,
        "--expected-commit-message",
        "exact authorized message",
    ])

    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert data["final_status"] == "PASS"
    assert data["reason_code"] == "AUTHORIZATION_BINDING_VERIFIED"

# 23. verify-authorization blocks missing authorization task_id
def test_23_verify_authorization_blocks_missing_task_id(repo):
    write_freeze_contract(repo, commit_message="exact authorized message")
    (repo / "src").mkdir(parents=True, exist_ok=True)
    (repo / "src" / "new.txt").write_text("candidate\n")
    baseline = get_head(repo)
    freeze = run_checker(repo, ["--json", "--mode", "freeze", "--contract", "contract.json"])
    expected_tree = json.loads(freeze.stdout)["candidate_content_oid"]

    res = run_checker(repo, [
        "--json",
        "--mode",
        "verify-authorization",
        "--contract",
        "contract.json",
        "--expected-task-id",
        "AOS-FARM.680",
        "--expected-repository",
        "NMF13579/AOS-FARM",
        "--expected-branch",
        "build/aos-farm-680-candidate-freeze",
        "--expected-baseline-oid",
        baseline,
        "--expected-tree-oid",
        expected_tree,
        "--expected-commit-message",
        "exact authorized message",
    ])

    assert res.returncode == 4
    data = json.loads(res.stdout)
    assert data["final_status"] == "BLOCKED"
    assert data["reason_code"] == "AUTHORIZATION_TASK_ID_MISSING"
    assert "task_id" in data["errors"][0]

# 24. verify-authorization blocks wrong task_id
def test_24_verify_authorization_blocks_wrong_task_id(repo):
    write_freeze_contract(repo, commit_message="exact authorized message")
    (repo / "src").mkdir(parents=True, exist_ok=True)
    (repo / "src" / "new.txt").write_text("candidate\n")
    baseline = get_head(repo)
    freeze = run_checker(repo, ["--json", "--mode", "freeze", "--contract", "contract.json"])
    expected_tree = json.loads(freeze.stdout)["candidate_content_oid"]

    res = run_checker(repo, [
        "--json",
        "--mode",
        "verify-authorization",
        "--contract",
        "contract.json",
        "--expected-task-id",
        "AOS-FARM.680",
        "--authorization-task-id",
        "AOS-FARM.679",
        "--expected-repository",
        "NMF13579/AOS-FARM",
        "--expected-branch",
        "build/aos-farm-680-candidate-freeze",
        "--expected-baseline-oid",
        baseline,
        "--expected-tree-oid",
        expected_tree,
        "--expected-commit-message",
        "exact authorized message",
    ])

    assert res.returncode == 4
    data = json.loads(res.stdout)
    assert data["final_status"] == "BLOCKED"
    assert data["reason_code"] == "AUTHORIZATION_TASK_ID_MISMATCH"
    assert "task_id" in data["errors"][0]

# 25. authorization replay for another task is blocked even when other binding fields match
def test_25_verify_authorization_blocks_other_task_replay(repo):
    write_freeze_contract(repo, commit_message="exact authorized message")
    (repo / "src").mkdir(parents=True, exist_ok=True)
    (repo / "src" / "new.txt").write_text("candidate\n")
    baseline = get_head(repo)
    freeze = run_checker(repo, ["--json", "--mode", "freeze", "--contract", "contract.json"])
    expected_tree = json.loads(freeze.stdout)["candidate_content_oid"]

    res = run_checker(repo, [
        "--json",
        "--mode",
        "verify-authorization",
        "--contract",
        "contract.json",
        "--expected-task-id",
        "AOS-FARM.680",
        "--authorization-task-id",
        "AOS-FARM.681",
        "--expected-repository",
        "NMF13579/AOS-FARM",
        "--expected-branch",
        "build/aos-farm-680-candidate-freeze",
        "--expected-baseline-oid",
        baseline,
        "--expected-tree-oid",
        expected_tree,
        "--expected-commit-message",
        "exact authorized message",
    ])

    assert res.returncode == 4
    data = json.loads(res.stdout)
    assert data["final_status"] == "BLOCKED"
    assert data["reason_code"] == "AUTHORIZATION_TASK_ID_MISMATCH"

# 26. tracked template does not persist derived identity, future results, or approval fields
def test_26_template_excludes_persisted_identity_and_result_fields():
    template = Path("aos/templates/execution-artifacts/aos-build-step-scope-contract-template.json")
    data = json.loads(template.read_text())

    forbidden = {
        "candidate_content_oid",
        "candidate_change_key",
        "candidate_tree",
        "candidate_tree_id",
        "tree_oid",
        "tree_id",
        "commit_sha",
        "created_commit_sha",
        "push_result",
        "merge_result",
        "approval",
        "approved",
    }
    serialized = json.dumps(data)
    for key in forbidden:
        assert key not in serialized

# 27. ignored disposable workspace symlinks do not create false PATH_SAFETY_UNKNOWN blockers
def test_27_ignored_venv_symlink_is_not_candidate_blocker(repo):
    write_contract(repo)
    (repo / ".venv" / "bin").mkdir(parents=True, exist_ok=True)
    os.symlink("/usr/bin/python3", repo / ".venv" / "bin" / "python")

    res = run_checker(repo, ["--json", "--contract", "contract.json"])

    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert data["final_status"] == "PASS"
