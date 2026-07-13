import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "aos/scripts/aos_integration_shadow_workflow_check.py"
WORKFLOW = ".github/workflows/aos-advisory.yml"
CHECKOUT_SHA = "34e114876b0b11c390a56381ad16ebd13914f8d5"
SETUP_PYTHON_SHA = "a26af69be951a213d495a4c3e4e4022e16d87065"


def valid_workflow() -> str:
    return f"""name: AOS Integration Shadow

on:
  workflow_dispatch:
  push:
    branches:
      - build/**
  pull_request:
    branches:
      - dev

permissions:
  contents: read

concurrency:
  group: aos-integration-shadow-${{{{ github.workflow }}}}-${{{{ github.ref }}}}
  cancel-in-progress: true

jobs:
  aos-integration-shadow:
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    env:
      PYTHONDONTWRITEBYTECODE: "1"
      PYTHONUNBUFFERED: "1"
      PIP_DISABLE_PIP_VERSION_CHECK: "1"
    steps:
      - name: Checkout
        uses: actions/checkout@{CHECKOUT_SHA}
        with:
          persist-credentials: false

      - name: Set up Python
        uses: actions/setup-python@{SETUP_PYTHON_SHA}
        with:
          python-version: "3.9"

      - name: Environment report
        run: |
          set -euo pipefail
          python --version
          python -m pip --version

      - name: Install development dependencies
        run: |
          set -euo pipefail
          python -m pip install --requirement requirements-dev.txt

      - name: Validate workflow contract
        run: |
          set -euo pipefail
          python -B aos/scripts/aos_integration_shadow_workflow_check.py --workflow .github/workflows/aos-advisory.yml --json

      - name: Integration contract verifier tests
        run: |
          set -euo pipefail
          python -m pytest tests/scripts/test_aos_integration_contract_check.py tests/test_aos_validate.py tests/scripts/test_aos_conditional_scope_check.py -p no:cacheprovider

      - name: Control checks
        run: |
          set -euo pipefail
          python -B aos/scripts/aos_simple_control_contract_check.py --json
          python -m pytest tests/test_aos_semantic_guard.py -p no:cacheprovider
          python -B aos/scripts/aos_task_document_check.py task --validate-all
          git diff --check

      - name: Full validation
        run: |
          set -euo pipefail
          python -m pytest -p no:cacheprovider
"""


def make_repo(tmp_path: Path, text: str = None) -> Path:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=tmp_path, check=True)
    workflow_path = tmp_path / WORKFLOW
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_bytes((valid_workflow() if text is None else text).encode("utf-8"))
    subprocess.run(["git", "add", "--", WORKFLOW], cwd=tmp_path, check=True)
    return workflow_path


def run_checker(repo: Path, workflow: str = WORKFLOW):
    return subprocess.run(
        [sys.executable, "-B", str(CHECKER), "--workflow", workflow, "--json"],
        cwd=repo,
        text=True,
        capture_output=True,
    )


def result_json(completed):
    return json.loads(completed.stdout)


def test_valid_workflow_passes_and_grants_no_approval(tmp_path):
    workflow_path = make_repo(tmp_path)
    before = workflow_path.read_bytes()

    completed = run_checker(tmp_path)

    assert completed.returncode == 0, completed.stderr
    data = result_json(completed)
    assert data["final_status"] == "PASS"
    assert data["reason_code"] == "SHADOW_WORKFLOW_CONTRACT_VALID"
    assert data["technical_workflow_valid"] is True
    assert data["workflow_path"] == WORKFLOW
    assert data["workflow_name"] == "AOS Integration Shadow"
    assert data["job_name"] == "aos-integration-shadow"
    assert data["runner"] == "ubuntu-24.04"
    assert data["python_version"] == "3.9"
    assert data["action_refs_pinned"] is True
    assert data["permissions_read_only"] is True
    assert data["required_check_enabled"] is False
    assert data["platform_execution_verified"] is False
    assert data["approval_granted"] is False
    assert data["integration_authorized"] is False
    assert data["merge_authorized"] is False
    assert workflow_path.read_bytes() == before


def test_valid_workflow_output_is_deterministic(tmp_path):
    make_repo(tmp_path)

    first = run_checker(tmp_path)
    second = run_checker(tmp_path)

    assert first.returncode == 0
    assert first.stdout == second.stdout


def test_help_has_no_side_effects(tmp_path):
    completed = subprocess.run(
        [sys.executable, "-B", str(CHECKER), "--help"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 0
    assert "--workflow" in completed.stdout
    assert "--json" in completed.stdout
    assert not (tmp_path / ".git").exists()


def test_missing_workflow_blocks(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, stdout=subprocess.DEVNULL)

    completed = run_checker(tmp_path)

    assert completed.returncode == 2
    data = result_json(completed)
    assert data["final_status"] == "UNKNOWN_BLOCKED"
    assert data["reason_code"] == "SHADOW_WORKFLOW_PATH_INVALID"


def test_untracked_workflow_blocks(tmp_path):
    workflow_path = tmp_path / WORKFLOW
    workflow_path.parent.mkdir(parents=True)
    workflow_path.write_text(valid_workflow(), encoding="utf-8")
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, stdout=subprocess.DEVNULL)

    completed = run_checker(tmp_path)

    assert completed.returncode == 2
    data = result_json(completed)
    assert data["final_status"] == "UNKNOWN_BLOCKED"
    assert data["reason_code"] == "SHADOW_WORKFLOW_PATH_INVALID"


def test_workflow_symlink_blocks(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, stdout=subprocess.DEVNULL)
    target = tmp_path / "target.yml"
    target.write_text(valid_workflow(), encoding="utf-8")
    workflow_path = tmp_path / WORKFLOW
    workflow_path.parent.mkdir(parents=True)
    workflow_path.symlink_to(target)
    subprocess.run(["git", "add", "--", WORKFLOW], cwd=tmp_path, check=True)

    completed = run_checker(tmp_path)

    assert completed.returncode == 2
    assert result_json(completed)["reason_code"] == "SHADOW_WORKFLOW_PATH_INVALID"


def test_symlink_parent_blocks(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, stdout=subprocess.DEVNULL)
    real = tmp_path / "real-workflows"
    real.mkdir()
    (real / "aos-advisory.yml").write_text(valid_workflow(), encoding="utf-8")
    github = tmp_path / ".github"
    github.mkdir()
    (github / "workflows").symlink_to(real, target_is_directory=True)

    completed = run_checker(tmp_path)

    assert completed.returncode == 2
    assert result_json(completed)["reason_code"] == "SHADOW_WORKFLOW_PATH_INVALID"


def test_directory_path_blocks(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, stdout=subprocess.DEVNULL)
    (tmp_path / ".github/workflows/aos-advisory.yml").mkdir(parents=True)

    completed = run_checker(tmp_path)

    assert completed.returncode == 2
    assert result_json(completed)["reason_code"] == "SHADOW_WORKFLOW_PATH_INVALID"


def test_unsafe_workflow_path_blocks(tmp_path):
    make_repo(tmp_path)
    for workflow in [
        str((tmp_path / WORKFLOW).resolve()),
        "../.github/workflows/aos-advisory.yml",
        ".aos-tmp/aos-advisory.yml",
        ".github/workflows/other.yml",
    ]:
        completed = run_checker(tmp_path, workflow)
        assert completed.returncode == 2
        assert result_json(completed)["reason_code"] == "SHADOW_WORKFLOW_PATH_INVALID"


def test_bom_crlf_and_tabs_block(tmp_path):
    cases = [
        b"\xef\xbb\xbf" + valid_workflow().encode("utf-8"),
        valid_workflow().replace("\n", "\r\n").encode("utf-8"),
        valid_workflow().replace("name:", "\tname:", 1).encode("utf-8"),
    ]
    for raw in cases:
        repo = tmp_path / str(len(list(tmp_path.iterdir())))
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.DEVNULL)
        workflow_path = repo / WORKFLOW
        workflow_path.parent.mkdir(parents=True, exist_ok=True)
        workflow_path.write_bytes(raw)
        subprocess.run(["git", "add", "--", WORKFLOW], cwd=repo, check=True)
        completed = run_checker(repo)
        assert completed.returncode == 2
        assert result_json(completed)["final_status"] == "BLOCKED"


def blocked_for(text: str, tmp_path: Path):
    make_repo(tmp_path, text)
    completed = run_checker(tmp_path)
    assert completed.returncode == 2
    data = result_json(completed)
    assert data["final_status"] == "BLOCKED"
    assert data["technical_workflow_valid"] is False
    return data


def test_pinned_action_policy_blocks_bad_action_refs(tmp_path):
    replacements = [
        (f"actions/checkout@{CHECKOUT_SHA}", "actions/checkout@v4"),
        (f"actions/setup-python@{SETUP_PYTHON_SHA}", "actions/setup-python@v5"),
        (f"actions/checkout@{CHECKOUT_SHA}", "actions/cache@0123456789012345678901234567890123456789"),
        (f"actions/checkout@{CHECKOUT_SHA}", "third-party/action@0123456789012345678901234567890123456789"),
    ]
    for old, new in replacements:
        repo = tmp_path / new.replace("/", "_").replace("@", "_")
        repo.mkdir()
        blocked_for(valid_workflow().replace(old, new), repo)


def test_permission_and_secret_policy_blocks_unsafe_workflows(tmp_path):
    cases = [
        valid_workflow().replace("contents: read", "contents: write"),
        valid_workflow().replace("contents: read", "pull-requests: write"),
        valid_workflow().replace("timeout-minutes: 30", "permissions:\n      contents: read\n    timeout-minutes: 30"),
        valid_workflow().replace("python --version", "echo ${{ secrets.GITHUB_TOKEN }}"),
    ]
    for index, text in enumerate(cases):
        repo = tmp_path / str(index)
        repo.mkdir()
        blocked_for(text, repo)


def test_trigger_policy_blocks_unsafe_triggers(tmp_path):
    cases = [
        valid_workflow().replace("pull_request:", "pull_request_target:"),
        valid_workflow().replace("- build/**", "- dev"),
        valid_workflow().replace("- build/**", "- main"),
        valid_workflow().replace("workflow_dispatch:", "schedule:\n    - cron: '0 0 * * *'"),
        valid_workflow() + "\n  release:\n",
        valid_workflow() + "\n  tags:\n    - '*'\n",
    ]
    for index, text in enumerate(cases):
        repo = tmp_path / str(index)
        repo.mkdir()
        blocked_for(text, repo)


def test_checkout_and_python_policy_blocks_unsafe_values(tmp_path):
    cases = [
        valid_workflow().replace("persist-credentials: false", "persist-credentials: true"),
        valid_workflow().replace("persist-credentials: false", "token: ${{ github.token }}"),
        valid_workflow().replace('python-version: "3.9"', 'python-version: "3.x"'),
        valid_workflow().replace("python -m pip install --requirement requirements-dev.txt", "python -m pip install pytest"),
        valid_workflow().replace("python -m pip install --requirement requirements-dev.txt", "python -m pip install https://example.invalid/pkg.whl"),
    ]
    for index, text in enumerate(cases):
        repo = tmp_path / str(index)
        repo.mkdir()
        blocked_for(text, repo)


def test_required_steps_are_mandatory(tmp_path):
    cases = [
        valid_workflow().replace("python -B aos/scripts/aos_integration_shadow_workflow_check.py --workflow .github/workflows/aos-advisory.yml --json", ""),
        valid_workflow().replace("tests/scripts/test_aos_integration_contract_check.py tests/test_aos_validate.py tests/scripts/test_aos_conditional_scope_check.py", ""),
        valid_workflow().replace("python -m pytest -p no:cacheprovider", ""),
    ]
    for index, text in enumerate(cases):
        repo = tmp_path / str(index)
        repo.mkdir()
        blocked_for(text, repo)


def test_failure_suppression_and_write_commands_block(tmp_path):
    cases = [
        valid_workflow().replace("set -euo pipefail", "set +e", 1),
        valid_workflow().replace("python --version", "python --version || true"),
        valid_workflow().replace("name: Full validation", "continue-on-error: true\n      - name: Full validation"),
        valid_workflow().replace("name: Full validation", "if: always()\n      - name: Full validation"),
        valid_workflow().replace("python --version", "curl https://example.invalid"),
        valid_workflow().replace("python --version", "wget https://example.invalid"),
        valid_workflow().replace("python --version", "git push origin HEAD"),
        valid_workflow().replace("python --version", "git commit -m bad"),
        valid_workflow().replace("python --version", "gh pr create"),
    ]
    for index, text in enumerate(cases):
        repo = tmp_path / str(index)
        repo.mkdir()
        blocked_for(text, repo)


def test_cache_artifacts_timeout_and_concurrency_policy(tmp_path):
    cases = [
        valid_workflow().replace("python --version", "python --version\n          cache: pip"),
        valid_workflow().replace("python --version", "actions/upload-artifact@0123456789012345678901234567890123456789"),
        valid_workflow().replace("timeout-minutes: 30", "timeout-minutes: 31"),
        valid_workflow().replace("concurrency:\n  group: aos-integration-shadow-${{ github.workflow }}-${{ github.ref }}\n  cancel-in-progress: true\n\n", ""),
        valid_workflow().replace("cancel-in-progress: true", "cancel-in-progress: false"),
    ]
    for index, text in enumerate(cases):
        repo = tmp_path / str(index)
        repo.mkdir()
        blocked_for(text, repo)
