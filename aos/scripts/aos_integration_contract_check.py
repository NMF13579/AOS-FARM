#!/usr/bin/env python3
import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


PASS = "PASS"
HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
BLOCKED = "BLOCKED"
UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"

VALID_REASON = "INTEGRATION_CONTRACT_VALID"
CLAIM_CEILING = "ADVISORY_VALIDATED_DURABLE_INTEGRATION_CONTRACT"
FIXED_POINT_SEARCH_USED = False

REQUIRED_CHECKS_POLICY_V1 = [
    "aos-integration / candidate-binding",
    "aos-integration / contract",
    "aos-integration / focused-tests",
    "aos-integration / full-pytest",
    "aos-integration / protected-paths",
    "aos-integration / semantic-guard",
]

TOP_LEVEL_KEYS = {
    "schema_version",
    "contract_type",
    "contract_id",
    "task_id",
    "repository",
    "source",
    "target",
    "candidate",
    "integration",
    "check_policy",
    "invalidation",
    "authorization_boundary",
    "contract_binding",
}

NESTED_KEYS = {
    "repository": {"identity", "remote_url"},
    "source": {"branch", "commit_oid", "parent_oid", "tree_oid"},
    "target": {"branch", "expected_head_oid"},
    "candidate": {"manifest_binding", "files"},
    "integration": {"method", "exact_commit_preservation", "target_must_be_current"},
    "check_policy": {"policy_version", "required_checks", "advisory_checks"},
    "invalidation": {
        "source_commit_change",
        "target_head_change",
        "candidate_manifest_change",
        "check_policy_change",
        "integration_method_change",
    },
    "authorization_boundary": {
        "contract_is_approval",
        "integration_authorized",
        "merge_authorized",
        "release_authorized",
        "human_decision_required",
    },
}

CANDIDATE_FILE_KEYS = {"path", "state", "mode", "sha256", "previous_path"}
HEX40 = set("0123456789abcdef")
HEX64 = set("0123456789abcdef")
PROTECTED_PATHS = {
    "00_AOS_Core_Control.md",
    "01_AOS_Assembly_Pipelines_and_Build_Roadmap.md",
    "02_AOS_Governance_Control_Module_and_Safety_Rules.md",
    "AGENTS.md",
    "CODEOWNERS",
}
PROTECTED_PREFIXES = (".github/workflows/", ".github/CODEOWNERS")
ACTIVE_CONTRACT_PREFIX = "aos/integration/contracts/"
TEMPLATE_PREFIX = "aos/templates/execution-artifacts/"


class ContractError(Exception):
    def __init__(self, status, reason, errors=None, technical_valid=False, warnings=None):
        super().__init__(reason)
        self.status = status
        self.reason = reason
        self.errors = list(errors or [])
        self.technical_valid = technical_valid
        self.warnings = list(warnings or [])


def canonical_json_bytes(payload):
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(payload):
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def contract_binding_payload(contract):
    payload = copy.deepcopy(contract)
    payload.pop("contract_id", None)
    payload.pop("contract_binding", None)
    return payload


def compute_contract_binding(contract):
    return canonical_sha256(contract_binding_payload(contract))


def expected_contract_id(contract_binding):
    return f"integration-{contract_binding[:16]}"


def compute_candidate_manifest_binding(repository_identity, source_commit_oid, source_tree_oid, files):
    return canonical_sha256(
        {
            "binding_version": 1,
            "repository_identity": repository_identity,
            "source_commit_oid": source_commit_oid,
            "source_tree_oid": source_tree_oid,
            "files": files,
        }
    )


def duplicate_rejecting_pairs(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key: {key}")
        seen[key] = value
    return seen


def reject_json_constant(value):
    raise ValueError(f"unsupported JSON constant: {value}")


def load_strict_json(path):
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ContractError(UNKNOWN_BLOCKED, "CONTRACT_PARSE_INVALID", ["BOM is not allowed"])
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContractError(UNKNOWN_BLOCKED, "CONTRACT_PARSE_INVALID", [str(exc)]) from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=duplicate_rejecting_pairs,
            parse_constant=reject_json_constant,
        )
    except Exception as exc:
        raise ContractError(UNKNOWN_BLOCKED, "CONTRACT_PARSE_INVALID", [str(exc)]) from exc


def is_hex(value, length):
    if not isinstance(value, str) or len(value) != length:
        return False
    return all(c in (HEX40 if length == 40 else HEX64) for c in value)


def has_control_character(value):
    return any(ord(char) < 32 for char in value)


def safe_relative_path(path_value, allow_contract_path=False):
    if not isinstance(path_value, str) or not path_value:
        raise ValueError("path must be a non-empty string")
    if "\x00" in path_value or has_control_character(path_value):
        raise ValueError("path contains control character")
    raw = Path(path_value)
    if raw.is_absolute():
        raise ValueError("absolute path is forbidden")
    if "\\" in path_value:
        raise ValueError("backslash is forbidden")
    if any(part in {"", ".."} for part in raw.parts):
        raise ValueError("path traversal or empty segment is forbidden")
    normalized = raw.as_posix()
    if normalized.startswith(".git/") or normalized == ".git":
        raise ValueError(".git path is forbidden")
    if normalized.startswith(".aos-tmp/") or normalized == ".aos-tmp":
        raise ValueError(".aos-tmp path is forbidden")
    if allow_contract_path:
        if not normalized.startswith(ACTIVE_CONTRACT_PREFIX):
            raise ValueError("active integration contract must be under aos/integration/contracts/")
        if normalized.startswith(TEMPLATE_PREFIX):
            raise ValueError("template path cannot be active contract")
        if not (normalized.endswith(".json") or normalized.endswith(".yaml")):
            raise ValueError("contract extension must be .json or .yaml")
    return normalized


def path_has_symlink_component(repo_root, relative_path):
    current = repo_root
    for part in Path(relative_path).parts:
        current = current / part
        if current.exists() and current.is_symlink():
            return True
    return False


def run_git(repo_root, args):
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
    )
    if result.returncode != 0:
        raise ContractError(UNKNOWN_BLOCKED, "GIT_OBSERVATION_ERROR", [result.stderr.strip() or result.stdout.strip()])
    return result.stdout.strip()


def resolve_repository_root(value):
    path = Path(value)
    try:
        resolved = path.resolve(strict=True)
    except Exception as exc:
        raise ContractError(UNKNOWN_BLOCKED, "REPOSITORY_ROOT_INVALID", [str(exc)]) from exc
    if not (resolved / ".git").exists():
        raise ContractError(UNKNOWN_BLOCKED, "REPOSITORY_ROOT_INVALID", [".git context is unavailable"])
    return resolved


def resolve_contract_path(repo_root, contract_path_value):
    try:
        contract_path = safe_relative_path(contract_path_value, allow_contract_path=True)
    except ValueError as exc:
        raise ContractError(UNKNOWN_BLOCKED, "INTEGRATION_CONTRACT_PATH_INVALID", [str(exc)]) from exc
    target = repo_root / contract_path
    try:
        resolved = target.resolve(strict=False)
        resolved.relative_to(repo_root)
    except Exception as exc:
        raise ContractError(UNKNOWN_BLOCKED, "INTEGRATION_CONTRACT_PATH_INVALID", ["path resolves outside repository"]) from exc
    if not target.exists():
        raise ContractError(UNKNOWN_BLOCKED, "INTEGRATION_CONTRACT_PATH_INVALID", ["contract file is missing"])
    if path_has_symlink_component(repo_root, contract_path):
        raise ContractError(UNKNOWN_BLOCKED, "INTEGRATION_CONTRACT_PATH_INVALID", ["contract path must not contain symlink components"])
    if not target.is_file():
        raise ContractError(UNKNOWN_BLOCKED, "INTEGRATION_CONTRACT_PATH_INVALID", ["contract path must be a regular file"])
    try:
        run_git(repo_root, ["ls-files", "--error-unmatch", "--", contract_path])
    except ContractError as exc:
        raise ContractError(UNKNOWN_BLOCKED, "INTEGRATION_CONTRACT_PATH_INVALID", ["contract must be tracked by Git"]) from exc
    return contract_path, target


def validate_schema(contract):
    if not isinstance(contract, dict):
        raise ContractError(UNKNOWN_BLOCKED, "CONTRACT_SCHEMA_INVALID", ["contract must be an object"])
    unknown = sorted(set(contract) - TOP_LEVEL_KEYS)
    if unknown:
        raise ContractError(BLOCKED, "CONTRACT_SCHEMA_INVALID", [f"unknown top-level field: {field}" for field in unknown])
    missing = sorted(TOP_LEVEL_KEYS - set(contract))
    if missing:
        raise ContractError(BLOCKED, "CONTRACT_SCHEMA_INVALID", [f"missing field: {field}" for field in missing])
    if contract.get("schema_version") != 1:
        raise ContractError(BLOCKED, "UNSUPPORTED_SCHEMA_VERSION", ["schema_version must be 1"])
    if contract.get("contract_type") != "AOS_INTEGRATION_CONTRACT":
        raise ContractError(BLOCKED, "CONTRACT_SCHEMA_INVALID", ["contract_type must be AOS_INTEGRATION_CONTRACT"])
    for section, allowed_keys in NESTED_KEYS.items():
        value = contract.get(section)
        if not isinstance(value, dict):
            raise ContractError(BLOCKED, "CONTRACT_SCHEMA_INVALID", [f"{section} must be an object"])
        unknown_nested = sorted(set(value) - allowed_keys)
        missing_nested = sorted(allowed_keys - set(value))
        if unknown_nested or missing_nested:
            errors = [f"{section} unknown field: {field}" for field in unknown_nested]
            errors.extend(f"{section} missing field: {field}" for field in missing_nested)
            raise ContractError(BLOCKED, "CONTRACT_SCHEMA_INVALID", errors)
    if not is_hex(contract.get("contract_binding"), 64):
        raise ContractError(BLOCKED, "CONTRACT_BINDING_MISMATCH", ["contract_binding must be 64 lowercase hex"])
    contract_id = contract.get("contract_id")
    if not isinstance(contract_id, str) or not contract_id.startswith("integration-") or len(contract_id) != 28:
        raise ContractError(BLOCKED, "CONTRACT_ID_BINDING_MISMATCH", ["contract_id must match integration-<16-lowercase-hex>"])
    if not all(c in HEX64 for c in contract_id.removeprefix("integration-")):
        raise ContractError(BLOCKED, "CONTRACT_ID_BINDING_MISMATCH", ["contract_id must use lowercase hex"])
    files = contract.get("candidate", {}).get("files")
    if not isinstance(files, list):
        raise ContractError(BLOCKED, "CONTRACT_SCHEMA_INVALID", ["candidate.files must be a list"])


def verify_contract_binding(contract):
    computed = compute_contract_binding(contract)
    if contract.get("contract_binding") != computed:
        raise ContractError(BLOCKED, "CONTRACT_BINDING_MISMATCH", ["contract_binding does not match canonical payload"])
    expected_id = expected_contract_id(computed)
    if contract.get("contract_id") != expected_id:
        raise ContractError(BLOCKED, "CONTRACT_ID_BINDING_MISMATCH", ["contract_id does not derive from contract_binding"])
    return computed, expected_id


def validate_candidate_files(files):
    normalized = []
    seen_current = set()
    seen_previous = set()
    errors = []
    last_path = None
    for item in files:
        if not isinstance(item, dict):
            errors.append("candidate file entry must be an object")
            continue
        unknown = sorted(set(item) - CANDIDATE_FILE_KEYS)
        if unknown:
            errors.append(f"unknown candidate file field: {unknown[0]}")
            continue
        for required in ("path", "state", "mode", "sha256"):
            if required not in item:
                errors.append(f"candidate file missing {required}")
        try:
            path = safe_relative_path(item.get("path"))
        except ValueError as exc:
            errors.append(f"{item.get('path')}: {exc}")
            continue
        if last_path is not None and path < last_path:
            errors.append("candidate files must be lexicographically sorted")
        last_path = path
        if path in seen_current:
            errors.append(f"duplicate candidate path: {path}")
        seen_current.add(path)
        state = item.get("state")
        if state not in {"ADDED", "MODIFIED", "DELETED", "RENAMED"}:
            errors.append(f"invalid candidate state for {path}")
        mode = item.get("mode")
        if mode not in {"100644", "100755"}:
            errors.append(f"invalid mode for {path}")
        sha = item.get("sha256")
        if state == "DELETED":
            if sha is not None:
                errors.append(f"deleted file {path} must have null sha256")
        elif not is_hex(sha, 64):
            errors.append(f"file {path} must have 64 lowercase hex sha256")
        previous = item.get("previous_path")
        if state == "RENAMED":
            try:
                previous = safe_relative_path(previous)
            except ValueError as exc:
                errors.append(f"{item.get('previous_path')}: {exc}")
            if previous in seen_previous:
                errors.append(f"duplicate previous path: {previous}")
            seen_previous.add(previous)
        elif previous is not None:
            errors.append(f"previous_path only allowed for renamed file {path}")
        normalized_item = dict(item)
        normalized_item["path"] = path
        if previous is not None:
            normalized_item["previous_path"] = previous
        normalized.append(normalized_item)
    if errors:
        raise ContractError(BLOCKED, "CANDIDATE_FILES_INVALID", errors)
    return normalized


def validate_check_policy(policy):
    errors = []
    if policy.get("policy_version") != 1:
        errors.append("policy_version must be 1")
    required = policy.get("required_checks")
    advisory = policy.get("advisory_checks")
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        errors.append("required_checks must be a string list")
    if not isinstance(advisory, list) or not all(isinstance(item, str) for item in advisory):
        errors.append("advisory_checks must be a string list")
    if errors:
        raise ContractError(BLOCKED, "CHECK_POLICY_INVALID", errors)
    if required != sorted(required) or advisory != sorted(advisory):
        errors.append("check lists must be sorted")
    if len(set(required)) != len(required):
        errors.append("required_checks must be unique")
    if len(set(advisory)) != len(advisory):
        errors.append("advisory_checks must be unique")
    if required != REQUIRED_CHECKS_POLICY_V1:
        errors.append("required_checks do not match policy version 1")
    overlap = sorted(set(required) & set(advisory))
    if overlap:
        errors.append(f"required/advisory overlap: {overlap[0]}")
    if errors:
        raise ContractError(BLOCKED, "CHECK_POLICY_INVALID", errors)


def validate_authorization_boundary(boundary):
    illegal = []
    if boundary.get("contract_is_approval") is not False:
        illegal.append("contract_is_approval must be false")
    if boundary.get("integration_authorized") is not False:
        illegal.append("integration_authorized must be false")
    if boundary.get("merge_authorized") is not False:
        illegal.append("merge_authorized must be false")
    if boundary.get("release_authorized") is not False:
        illegal.append("release_authorized must be false")
    if boundary.get("human_decision_required") is not True:
        illegal.append("human_decision_required must be true")
    if illegal:
        raise ContractError(BLOCKED, "CONTRACT_ILLEGAL_AUTHORIZATION_CLAIM", illegal)


def validate_repository_fields(repo_root, contract):
    if contract["repository"]["identity"] != "NMF13579/AOS-FARM":
        raise ContractError(BLOCKED, "REPOSITORY_IDENTITY_MISMATCH", ["repository identity mismatch"])
    remote_url = run_git(repo_root, ["remote", "get-url", "origin"])
    if remote_url != contract["repository"]["remote_url"]:
        raise ContractError(BLOCKED, "REMOTE_URL_MISMATCH", ["origin URL mismatch"])
    if not contract["source"]["branch"].startswith("build/"):
        raise ContractError(BLOCKED, "SOURCE_BRANCH_INVALID", ["source branch must use build/ prefix"])
    if contract["target"]["branch"] != "dev":
        raise ContractError(BLOCKED, "TARGET_BRANCH_INVALID", ["target branch must be dev"])
    if contract["source"]["commit_oid"] == contract["target"]["expected_head_oid"]:
        raise ContractError(BLOCKED, "SOURCE_TARGET_RELATION_INVALID", ["source and target OIDs must differ"])


def validate_observed_oids(contract, observed_source_oid, observed_target_oid):
    if not is_hex(observed_source_oid, 40) or not is_hex(observed_target_oid, 40):
        raise ContractError(UNKNOWN_BLOCKED, "OBSERVED_OID_INVALID", ["observed OIDs must be 40 lowercase hex"])
    if observed_source_oid != contract["source"]["commit_oid"]:
        raise ContractError(BLOCKED, "SOURCE_COMMIT_STALE", ["observed source does not match contract source"])
    if observed_target_oid != contract["target"]["expected_head_oid"]:
        raise ContractError(BLOCKED, "TARGET_HEAD_STALE", ["observed target does not match contract target"])


def git_object_exists(repo_root, oid):
    subprocess.run(["git", "cat-file", "-e", f"{oid}^{{commit}}"], cwd=repo_root, check=True, capture_output=True, text=True)


def git_semantic_validation(repo_root, contract):
    source = contract["source"]
    target = contract["target"]
    try:
        git_object_exists(repo_root, source["commit_oid"])
        git_object_exists(repo_root, target["expected_head_oid"])
    except subprocess.CalledProcessError as exc:
        raise ContractError(UNKNOWN_BLOCKED, "GIT_OBSERVATION_ERROR", [exc.stderr.strip() or "required commit object missing"]) from exc
    parent_line = run_git(repo_root, ["rev-list", "--parents", "-n", "1", source["commit_oid"]]).split()
    if len(parent_line) < 2 or parent_line[1] != source["parent_oid"]:
        raise ContractError(BLOCKED, "SOURCE_PARENT_MISMATCH", ["source parent mismatch"])
    tree_oid = run_git(repo_root, ["rev-parse", f"{source['commit_oid']}^{{tree}}"])
    if tree_oid != source["tree_oid"]:
        raise ContractError(BLOCKED, "SOURCE_TREE_MISMATCH", ["source tree mismatch"])
    merge_base = run_git(repo_root, ["merge-base", "--is-ancestor", target["expected_head_oid"], source["commit_oid"]])
    if merge_base:
        pass
    # merge-base --is-ancestor prints no stdout; success is enough.


def diff_entries(repo_root, parent_oid, source_oid):
    raw = run_git(repo_root, ["diff-tree", "--no-commit-id", "-r", "--no-renames", "--raw", parent_oid, source_oid])
    entries = {}
    for line in raw.splitlines():
        if not line:
            continue
        meta, path = line.split("\t", 1)
        parts = meta.split()
        old_mode = parts[0].lstrip(":")
        new_mode = parts[1]
        status = parts[4]
        state = {"A": "ADDED", "M": "MODIFIED", "D": "DELETED"}.get(status)
        if state is None:
            raise ContractError(BLOCKED, "CANDIDATE_DIFF_MISMATCH", [f"unsupported diff status {status} for {path}"])
        entries[path] = {"state": state, "mode": new_mode if state != "DELETED" else old_mode}
    return entries


def blob_sha256(repo_root, commit_oid, path):
    result = subprocess.run(
        ["git", "show", f"{commit_oid}:{path}"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise ContractError(BLOCKED, "CANDIDATE_DIFF_MISMATCH", [f"source blob missing: {path}"])
    return hashlib.sha256(result.stdout).hexdigest()


def validate_candidate_manifest_and_diff(repo_root, contract, files):
    expected_manifest = compute_candidate_manifest_binding(
        contract["repository"]["identity"],
        contract["source"]["commit_oid"],
        contract["source"]["tree_oid"],
        files,
    )
    if contract["candidate"]["manifest_binding"] != expected_manifest:
        raise ContractError(BLOCKED, "CANDIDATE_MANIFEST_BINDING_MISMATCH", ["candidate manifest binding mismatch"])
    diff = diff_entries(repo_root, contract["source"]["parent_oid"], contract["source"]["commit_oid"])
    if set(diff) != {item["path"] for item in files}:
        raise ContractError(BLOCKED, "CANDIDATE_DIFF_MISMATCH", ["candidate paths do not match source diff"])
    for item in files:
        actual = diff[item["path"]]
        if actual["state"] != item["state"]:
            raise ContractError(BLOCKED, "CANDIDATE_DIFF_MISMATCH", [f"state mismatch for {item['path']}"])
        if item["state"] != "DELETED":
            if actual["mode"] != item["mode"]:
                raise ContractError(BLOCKED, "CANDIDATE_DIFF_MISMATCH", [f"mode mismatch for {item['path']}"])
            actual_sha = blob_sha256(repo_root, contract["source"]["commit_oid"], item["path"])
            if actual_sha != item["sha256"]:
                raise ContractError(BLOCKED, "CANDIDATE_DIFF_MISMATCH", [f"sha256 mismatch for {item['path']}"])


def protected_paths(files):
    found = []
    for item in files:
        path = item["path"]
        if path in PROTECTED_PATHS or any(path == prefix.rstrip("/") or path.startswith(prefix) for prefix in PROTECTED_PREFIXES):
            found.append(path)
    return sorted(found)


def validate_contract(repo_root, contract_path, observed_source_oid, observed_target_oid):
    contract = load_strict_json(repo_root / contract_path)
    validate_schema(contract)
    contract_binding, contract_id = verify_contract_binding(contract)
    files = validate_candidate_files(contract["candidate"]["files"])
    validate_check_policy(contract["check_policy"])
    validate_authorization_boundary(contract["authorization_boundary"])
    validate_repository_fields(repo_root, contract)
    validate_observed_oids(contract, observed_source_oid, observed_target_oid)
    git_semantic_validation(repo_root, contract)
    validate_candidate_manifest_and_diff(repo_root, contract, files)
    found_protected = protected_paths(files)
    if found_protected:
        return build_result(
            HUMAN_REVIEW_REQUIRED,
            "PROTECTED_PATH_INTEGRATION_REVIEW_REQUIRED",
            True,
            contract,
            contract_path,
            contract_binding,
            files,
            observed_source_oid,
            observed_target_oid,
            ["protected/canonical path requires human review"],
            [],
        )
    return build_result(
        PASS,
        VALID_REASON,
        True,
        contract,
        contract_path,
        contract_binding,
        files,
        observed_source_oid,
        observed_target_oid,
        [],
        [],
    )


def build_result(status, reason, technical_valid, contract=None, contract_path=None, contract_binding=None, files=None, observed_source_oid=None, observed_target_oid=None, errors=None, warnings=None):
    files = files or []
    found_protected = protected_paths(files)
    return {
        "checker": "aos_integration_contract_check",
        "schema_version": 1,
        "final_status": status,
        "reason_code": reason,
        "technical_contract_valid": bool(technical_valid),
        "contract_path": contract_path,
        "contract_id": contract.get("contract_id") if contract else None,
        "contract_binding": contract_binding or (contract.get("contract_binding") if contract else None),
        "contract_binding_verified": status in {PASS, HUMAN_REVIEW_REQUIRED} and bool(contract),
        "contract_id_verified": status in {PASS, HUMAN_REVIEW_REQUIRED} and bool(contract),
        "candidate_manifest_binding": contract.get("candidate", {}).get("manifest_binding") if contract else None,
        "repository_identity": contract.get("repository", {}).get("identity") if contract else None,
        "source_commit_oid": contract.get("source", {}).get("commit_oid") if contract else None,
        "target_expected_oid": contract.get("target", {}).get("expected_head_oid") if contract else None,
        "observed_source_oid": observed_source_oid,
        "observed_target_oid": observed_target_oid,
        "candidate_file_count": len(files),
        "protected_paths": found_protected,
        "required_checks": contract.get("check_policy", {}).get("required_checks", []) if contract else [],
        "platform_enforced": False,
        "approval_granted": False,
        "integration_authorized": False,
        "merge_authorized": False,
        "release_authorized": False,
        "claim_ceiling": CLAIM_CEILING,
        "errors": list(errors or []),
        "warnings": list(warnings or []),
    }


def print_and_exit(result):
    print(json.dumps(result, indent=2, sort_keys=True))
    status = result["final_status"]
    if status == PASS:
        raise SystemExit(0)
    if status == HUMAN_REVIEW_REQUIRED:
        raise SystemExit(3)
    raise SystemExit(2)


def main():
    parser = argparse.ArgumentParser(description="AOS integration contract checker")
    parser.add_argument("--contract", required=True, help="Repository-relative active integration contract path")
    parser.add_argument("--repository-root", required=True, help="Repository root")
    parser.add_argument("--observed-source-oid", required=True, help="Observed source commit OID")
    parser.add_argument("--observed-target-oid", required=True, help="Observed target commit OID")
    parser.add_argument("--json", action="store_true", required=True, help="Output JSON")
    args = parser.parse_args()

    contract = None
    contract_path = None
    try:
        repo_root = resolve_repository_root(args.repository_root)
        contract_path, _target = resolve_contract_path(repo_root, args.contract)
        result = validate_contract(repo_root, contract_path, args.observed_source_oid, args.observed_target_oid)
        print_and_exit(result)
    except ContractError as exc:
        result = build_result(
            exc.status,
            exc.reason,
            exc.technical_valid,
            contract,
            contract_path or args.contract,
            None,
            [],
            args.observed_source_oid,
            args.observed_target_oid,
            exc.errors,
            exc.warnings,
        )
        print_and_exit(result)


if __name__ == "__main__":
    main()
