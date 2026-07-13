#!/usr/bin/env python3
"""Fail-closed static checker for the AOS integration shadow workflow."""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


WORKFLOW_PATH = ".github/workflows/aos-advisory.yml"
WORKFLOW_NAME = "AOS Integration Shadow"
JOB_NAME = "aos-integration-shadow"
RUNNER = "ubuntu-24.04"
PYTHON_VERSION = "3.9"
CHECKOUT_SHA = "34e114876b0b11c390a56381ad16ebd13914f8d5"
SETUP_PYTHON_SHA = "a26af69be951a213d495a4c3e4e4022e16d87065"
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def base_result(status, reason, workflow_sha256=None, errors=None, warnings=None):
    return {
        "checker": "aos_integration_shadow_workflow_check",
        "schema_version": 1,
        "final_status": status,
        "reason_code": reason,
        "technical_workflow_valid": status == "PASS",
        "workflow_path": WORKFLOW_PATH,
        "workflow_sha256": workflow_sha256,
        "workflow_name": WORKFLOW_NAME,
        "job_name": JOB_NAME,
        "runner": RUNNER,
        "python_version": PYTHON_VERSION,
        "action_refs_pinned": status == "PASS",
        "permissions_read_only": status == "PASS",
        "failure_suppression_present": False,
        "required_check_enabled": False,
        "platform_execution_verified": False,
        "approval_granted": False,
        "integration_authorized": False,
        "merge_authorized": False,
        "errors": errors or [],
        "warnings": warnings or [],
    }


def emit(result):
    print(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False))


def path_parts_are_safe(path):
    return path == WORKFLOW_PATH and "\\" not in path and "\x00" not in path


def validate_workflow_path(workflow_arg):
    if not path_parts_are_safe(workflow_arg):
        raise ValueError("workflow path must be exactly .github/workflows/aos-advisory.yml")
    candidate = Path(workflow_arg)
    if candidate.is_absolute() or ".." in candidate.parts or ".aos-tmp" in candidate.parts:
        raise ValueError("workflow path is unsafe")
    root = Path.cwd().resolve()
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("workflow path escapes repository root") from exc
    for parent in [root / ".github", root / ".github" / "workflows"]:
        if parent.exists() and parent.is_symlink():
            raise ValueError("workflow parent is a symlink")
    workflow = root / candidate
    if workflow.is_symlink() or not workflow.is_file():
        raise ValueError("workflow is not a regular file")
    subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", WORKFLOW_PATH],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    return workflow


def add_error(errors, condition, message):
    if condition:
        errors.append(message)


def line_present(text, line):
    return any(existing == line for existing in text.splitlines())


def validate_text(raw):
    errors = []
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append("UTF-8 BOM is forbidden")
    if b"\r" in raw:
        errors.append("CRLF or CR line endings are forbidden")
    if b"\t" in raw:
        errors.append("tabs are forbidden")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, ["workflow is not valid UTF-8"]
    if "\n---" in text or text.lstrip().startswith("---"):
        errors.append("multi-document YAML marker is forbidden")
    return text, errors


def validate_policy(text):
    errors = []
    add_error(errors, not line_present(text, f"name: {WORKFLOW_NAME}"), "workflow display name mismatch")
    required_snippets = [
        "on:\n  workflow_dispatch:\n  push:\n    branches:\n      - build/**\n  pull_request:\n    branches:\n      - dev",
        "permissions:\n  contents: read",
        "concurrency:\n  group: aos-integration-shadow-${{ github.workflow }}-${{ github.ref }}\n  cancel-in-progress: true",
        f"  {JOB_NAME}:",
        "    runs-on: ubuntu-24.04",
        "    timeout-minutes: 30",
        '      PYTHONDONTWRITEBYTECODE: "1"',
        '      PYTHONUNBUFFERED: "1"',
        '      PIP_DISABLE_PIP_VERSION_CHECK: "1"',
        f"        uses: actions/checkout@{CHECKOUT_SHA}",
        "          persist-credentials: false",
        f"        uses: actions/setup-python@{SETUP_PYTHON_SHA}",
        f'          python-version: "{PYTHON_VERSION}"',
        "          set -euo pipefail\n          python --version\n          python -m pip --version",
        "          set -euo pipefail\n          python -m pip install --requirement requirements-dev.txt",
        "python -B aos/scripts/aos_integration_shadow_workflow_check.py --workflow .github/workflows/aos-advisory.yml --json",
        "python -m pytest tests/scripts/test_aos_integration_contract_check.py tests/test_aos_validate.py tests/scripts/test_aos_conditional_scope_check.py -p no:cacheprovider",
        "python -B aos/scripts/aos_simple_control_contract_check.py --json",
        "python -m pytest tests/test_aos_semantic_guard.py -p no:cacheprovider",
        "python -B aos/scripts/aos_task_document_check.py task --validate-all",
        "git diff --check",
        "          set -euo pipefail\n          python -m pytest -p no:cacheprovider",
    ]
    for snippet in required_snippets:
        add_error(errors, snippet not in text, f"required workflow snippet missing: {snippet.splitlines()[0]}")

    forbidden_patterns = [
        (r"(?m)^\s*pull_request_target:", "pull_request_target trigger is forbidden"),
        (r"(?m)^\s*workflow_run:", "workflow_run trigger is forbidden"),
        (r"(?m)^\s*schedule:", "schedule trigger is forbidden"),
        (r"(?m)^\s*repository_dispatch:", "repository_dispatch trigger is forbidden"),
        (r"(?m)^\s*issue_comment:", "issue_comment trigger is forbidden"),
        (r"(?m)^\s*deployment:", "deployment trigger is forbidden"),
        (r"(?m)^\s*release:", "release trigger is forbidden"),
        (r"(?m)^\s*tags:", "tag trigger is forbidden"),
        (r"(?s)push:\s*\n\s*branches:\s*\n\s*-\s+dev\b", "push to dev is forbidden"),
        (r"(?s)push:\s*\n\s*branches:\s*\n\s*-\s+main\b", "push to main is forbidden"),
        (r"(?m)^ {4,}permissions:", "job-level permissions are forbidden"),
        (r"\b[a-z-]+:\s*write\b", "write permissions are forbidden"),
        (r"secrets[.\[]", "secrets are forbidden"),
        (r"persist-credentials:\s*true", "checkout credentials persistence is forbidden"),
        (r"(?m)^\s*token:", "custom checkout token is forbidden"),
        (r"python-version:\s*[\"']?(3\.x|latest|\*)[\"']?", "floating Python version is forbidden"),
        (r"python\s+-m\s+pip\s+install\s+pytest\b", "ad-hoc pytest installation is forbidden"),
        (r"pip\s+install\s+https?://", "URL dependency installation is forbidden"),
        (r"continue-on-error:\s*true", "continue-on-error is forbidden"),
        (r"\|\|\s*true", "failure suppression with || true is forbidden"),
        (r"set\s+\+e", "set +e is forbidden"),
        (r"if:\s*always\(\)", "if: always() is forbidden"),
        (r"\bcurl\b", "curl is forbidden"),
        (r"\bwget\b", "wget is forbidden"),
        (r"\bgit\s+push\b", "git push is forbidden"),
        (r"\bgit\s+commit\b", "git commit is forbidden"),
        (r"\bgh\s+pr\s+create\b", "pull request creation is forbidden"),
        (r"\bactions/cache@", "cache action is forbidden"),
        (r"(?m)^\s*cache:", "cache configuration is forbidden"),
        (r"\bactions/upload-artifact@", "artifact upload is forbidden"),
        (r"\bupload-artifact\b", "artifact upload is forbidden"),
        (r"timeout-minutes:\s*(3[1-9]|[4-9][0-9]|[1-9][0-9]{2,})", "timeout exceeds 30 minutes"),
        (r"cancel-in-progress:\s*false", "concurrency cancellation must be enabled"),
    ]
    for pattern, message in forbidden_patterns:
        add_error(errors, re.search(pattern, text) is not None, message)

    uses = re.findall(r"(?m)^\s*uses:\s*([^\s]+)\s*$", text)
    allowed_uses = {
        f"actions/checkout@{CHECKOUT_SHA}",
        f"actions/setup-python@{SETUP_PYTHON_SHA}",
    }
    add_error(errors, set(uses) != allowed_uses or len(uses) != 2, "only pinned checkout and setup-python actions are allowed")
    for action in uses:
        if "@" not in action:
            errors.append(f"action ref missing: {action}")
            continue
        repo, ref = action.rsplit("@", 1)
        if repo not in {"actions/checkout", "actions/setup-python"}:
            errors.append(f"third-party or unknown action is forbidden: {repo}")
        if not HEX40.fullmatch(ref):
            errors.append(f"action ref must be a full 40-character SHA: {action}")
    return errors


def check_workflow(workflow_arg):
    try:
        workflow = validate_workflow_path(workflow_arg)
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        return base_result(
            "UNKNOWN_BLOCKED",
            "SHADOW_WORKFLOW_PATH_INVALID",
            errors=[str(exc)],
        )
    try:
        raw = workflow.read_bytes()
    except OSError as exc:
        return base_result(
            "UNKNOWN_BLOCKED",
            "SHADOW_WORKFLOW_PATH_INVALID",
            errors=[str(exc)],
        )
    workflow_sha256 = hashlib.sha256(raw).hexdigest()
    text, errors = validate_text(raw)
    if text is not None:
        errors.extend(validate_policy(text))
    if errors:
        result = base_result(
            "BLOCKED",
            "SHADOW_WORKFLOW_CONTRACT_VIOLATION",
            workflow_sha256=workflow_sha256,
            errors=errors,
        )
        result["failure_suppression_present"] = any(
            "suppression" in error or "continue-on-error" in error or "set +e" in error
            for error in errors
        )
        return result
    return base_result("PASS", "SHADOW_WORKFLOW_CONTRACT_VALID", workflow_sha256=workflow_sha256)


def main(argv=None):
    parser = argparse.ArgumentParser(description="AOS integration shadow workflow checker")
    parser.add_argument("--workflow", required=True, help="Repository-relative workflow path")
    parser.add_argument("--json", action="store_true", required=True, help="Output JSON")
    args = parser.parse_args(argv)
    result = check_workflow(args.workflow)
    emit(result)
    if result["final_status"] == "PASS":
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
