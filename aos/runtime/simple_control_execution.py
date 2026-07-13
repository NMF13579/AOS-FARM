import datetime
import json
import subprocess
from pathlib import Path

from aos.runtime.simple_control_planning import bind_payload
from aos.runtime.simple_control_status import validation_result_with_details


EXPECTED_REPOSITORY = "NMF13579/AOS-FARM"
EXPECTED_BRANCH = "build/aos-farm-680-candidate-freeze"
EXPECTED_HEAD = "b1b9e7bd66db81598e1d02c0db9f4915d2b933af"
EXPECTED_REMOTE = "git@github.com:NMF13579/AOS-FARM.git"
ALLOWED_ACTION_TYPES = {"CREATE_FILE", "REPLACE_FILE"}
FORBIDDEN_ACTION_TYPES = {"DELETE", "MOVE", "RENAME", "ARCHIVE", "CLEANUP", "CHMOD", "SYMLINK", "GIT_ADD", "COMMIT", "PUSH", "MERGE", "RELEASE", "SHELL"}
EXECUTE_CONTRACT_BINDING = bind_payload({"command_id": "EXECUTE", "contract_version": 1, "mode": "orchestration_preview_only"})


class ExecutionError(Exception):
    pass


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _future_iso(hours=1):
    return (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=hours)).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_time(value):
    if not value:
        return None
    return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))


def _run_git(repo_root, args):
    result = subprocess.run(
        ["git", *args],
        cwd=str(Path(repo_root).resolve()),
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = result.stdout[:10000]
    stderr = result.stderr[:10000]
    if result.returncode != 0:
        raise ExecutionError(f"git {' '.join(args)} failed: {stderr or stdout}")
    return stdout.strip()


def safe_relative_path(repo_root, relative_path):
    if not isinstance(relative_path, str) or not relative_path:
        raise ExecutionError("path is required")
    candidate = Path(relative_path)
    if candidate.is_absolute():
        raise ExecutionError("absolute paths are forbidden")
    if any(part in {"..", ""} for part in candidate.parts):
        raise ExecutionError("path traversal is forbidden")
    root = Path(repo_root).resolve()
    unresolved = root
    for part in candidate.parts[:-1]:
        unresolved = unresolved / part
        if unresolved.exists() and unresolved.is_symlink():
            raise ExecutionError("symlink traversal is forbidden")
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ExecutionError("path outside repository is forbidden") from exc
    return candidate.as_posix()


def observe_repository(repo_root, expected_binding, target_paths):
    root = Path(repo_root).resolve()
    remote = _run_git(root, ["remote", "get-url", "origin"])
    branch = _run_git(root, ["branch", "--show-current"])
    head = _run_git(root, ["rev-parse", "HEAD"])
    tracked_diff = _run_git(root, ["diff", "--name-status"])
    staged_diff = _run_git(root, ["diff", "--cached", "--name-status"])
    checked_targets = []
    for path in target_paths:
        safe = safe_relative_path(root, path)
        checked_targets.append({"path": safe, "symlink": (root / safe).exists() and (root / safe).is_symlink()})
        if checked_targets[-1]["symlink"]:
            raise ExecutionError("target path is symlink")
    current = (
        expected_binding.get("repository") == EXPECTED_REPOSITORY
        and expected_binding.get("branch") == branch
        and expected_binding.get("head") == head
        and remote == EXPECTED_REMOTE
        and not tracked_diff
        and not staged_diff
    )
    observation = {
        "repository": EXPECTED_REPOSITORY,
        "remote": remote,
        "branch": branch,
        "head": head,
        "tracked_diff_empty": not bool(tracked_diff),
        "staged_diff_empty": not bool(staged_diff),
        "target_paths": checked_targets,
        "protected_or_canonical_impact": "false",
        "unexpected_target_conflicts": [],
        "current": current,
        "git_metadata_mutated": False,
        "fetch_performed": False,
    }
    if not current:
        raise ExecutionError("repository observation does not match expected baseline")
    return observation


def _proposal_from_bundle(bundle):
    proposal = bundle.get("scope_proposal")
    if not isinstance(proposal, dict):
        raise ExecutionError("scope proposal is required")
    return proposal


def _validate_ready_bundle(bundle):
    result = validation_result_with_details(bundle)
    if result.get("validation_status") != "PASS":
        raise ExecutionError("validation bundle must PASS contract validation")
    if result.get("derived_control_state") != "CONTROL_EXECUTION_AUTHORIZATION_REQUIRED":
        raise ExecutionError("bundle must be waiting for execution authorization")
    if result.get("unknowns") or result.get("blockers"):
        raise ExecutionError("UNKNOWN or blockers prevent execution preparation")
    return result


def _validate_actions(repo_root, request, proposal):
    write_scope = proposal.get("write_scope", {}).get("exact_paths", [])
    allowed_write_paths = {safe_relative_path(repo_root, path) for path in write_scope}
    seen = {}
    normalized_actions = []
    for action in request.get("planned_actions", []):
        action_type = action.get("action_type")
        if action_type in FORBIDDEN_ACTION_TYPES or action_type not in ALLOWED_ACTION_TYPES:
            raise ExecutionError(f"forbidden action type: {action_type}")
        path = safe_relative_path(repo_root, action.get("relative_path"))
        if path not in allowed_write_paths:
            return None, _scope_expansion(path, action, proposal)
        if path in seen and seen[path] != action_type:
            raise ExecutionError("conflicting action path")
        seen[path] = action_type
        if action.get("scope_binding") != proposal.get("proposal_binding"):
            raise ExecutionError("action scope binding mismatch")
        if action.get("proposed_content", {}).get("encoding") != "UTF-8":
            raise ExecutionError("proposed content encoding must be UTF-8")
        normalized = dict(action)
        normalized["relative_path"] = path
        normalized_actions.append(normalized)
    return normalized_actions, None


def _scope_expansion(path, action, proposal):
    return {
        "execution_package_created": False,
        "control_state": "CONTROL_SCOPE_EXPANSION_REQUIRED",
        "reason_code": "WRITE_SCOPE_EXPANSION_REQUIRED",
        "production_operation_started": False,
        "repository_files_modified": False,
        "scope_expansion_proposal": {
            "discovered_requirement": f"planned action outside confirmed write scope: {path}",
            "additional_write_paths": [path],
            "additional_actions": [action.get("action_id")],
            "Risk_Profile_impact": proposal.get("risk_recommendation", {}).get("recommended", "UNKNOWN"),
            "protected_or_canonical_impact": proposal.get("protected_or_canonical_impact", "unknown"),
            "destructive_impact": "false",
            "recommended_decision": ["expand_scope", "create_separate_task", "reduce_goal", "stop"],
        },
    }


def create_execution_request(bundle, planned_actions, repository_baseline):
    validation = _validate_ready_bundle(bundle)
    proposal = _proposal_from_bundle(bundle)
    confirmation = bundle["scope_confirmation"]
    risk = bundle["risk_profile_assignment"]
    request = {
        "request_version": 1,
        "request_id": "exec-request-" + proposal["proposal_binding"][:16],
        "task_id": bundle["task_id"],
        "proposal_binding": proposal["proposal_binding"],
        "scope_confirmation_binding": bind_payload(confirmation),
        "Risk_Profile_assignment_binding": bind_payload(risk),
        "validation_result_binding": bind_payload(validation),
        "requested_operation": "PREPARE_SCOPED_EXECUTION",
        "repository_baseline": repository_baseline,
        "read_scope": proposal.get("read_scope", {}).get("exact_paths", []),
        "write_scope": proposal.get("write_scope", {}).get("exact_paths", []),
        "forbidden_paths": proposal.get("write_scope", {}).get("forbidden_paths", []),
        "planned_actions": planned_actions,
        "required_validation": proposal.get("validation", {}).get("required", []),
        "mandatory_controls": proposal.get("mandatory_control_actions", []),
        "protected_or_canonical_impact": "false",
        "destructive_impact": "false",
        "lifecycle_impact": "false",
        "non_grants": ["commit", "push", "integration", "merge", "release", "lifecycle_mutation"],
    }
    request["request_binding"] = bind_payload(request)
    return request


def create_execution_authorization_witness(request, actor_reference):
    if not actor_reference:
        raise ExecutionError("actor_reference is required")
    return {
        "decision_type": "EXECUTION_AUTHORIZATION",
        "decision_id": "execution-" + request["request_binding"][:16],
        "task_id": request["task_id"],
        "proposal_binding": request["proposal_binding"],
        "execution_request_binding": request["request_binding"],
        "task_binding": bind_payload({"task_id": request["task_id"]}),
        "command_contract_binding": EXECUTE_CONTRACT_BINDING,
        "repository_baseline_binding": request["repository_baseline"],
        "candidate_binding": None,
        "operation_binding": None,
        "actor_reference": actor_reference,
        "actor_role": "human",
        "authentication_level": "LOCAL_DECLARED",
        "decision_channel": "CLI",
        "decision_value": "AUTHORIZED",
        "issued_at": now_iso(),
        "expires_at": _future_iso(),
        "single_use": True,
        "consumed_at": None,
        "grants": ["prepare_exact_execution_package"],
        "non_grants": ["production_file_mutation", "commit", "push", "integration", "merge", "release", "lifecycle_mutation"],
    }


def validate_execution_witness(witness, request, observation):
    if not isinstance(witness, dict):
        raise ExecutionError("execution authorization witness is required")
    if witness.get("decision_type") != "EXECUTION_AUTHORIZATION":
        raise ExecutionError("wrong execution witness decision type")
    if not witness.get("actor_reference"):
        raise ExecutionError("execution witness actor missing")
    if witness.get("task_id") != request.get("task_id"):
        raise ExecutionError("execution witness task binding mismatch")
    if witness.get("proposal_binding") != request.get("proposal_binding"):
        raise ExecutionError("execution witness proposal binding mismatch")
    if witness.get("execution_request_binding") != request.get("request_binding"):
        raise ExecutionError("execution witness request binding mismatch")
    if witness.get("repository_baseline_binding") != request.get("repository_baseline"):
        raise ExecutionError("execution witness repository baseline mismatch")
    if witness.get("consumed_at") is not None:
        raise ExecutionError("consumed single-use execution witness cannot be reused")
    expires = _parse_time(witness.get("expires_at"))
    if expires and expires <= datetime.datetime.now(datetime.timezone.utc):
        raise ExecutionError("execution witness expired")
    if "commit" in witness.get("grants", []) or "production_file_mutation" in witness.get("grants", []):
        raise ExecutionError("execution witness grants forbidden side effect")
    if not observation.get("current"):
        raise ExecutionError("repository observation is not current")
    return True


def _validate_request(bundle, request):
    validation = _validate_ready_bundle(bundle)
    proposal = _proposal_from_bundle(bundle)
    if request.get("request_version") != 1:
        raise ExecutionError("request_version must be 1")
    if request.get("task_id") != bundle.get("task_id"):
        raise ExecutionError("execution request task binding mismatch")
    if request.get("proposal_binding") != proposal.get("proposal_binding"):
        raise ExecutionError("execution request proposal binding mismatch")
    if request.get("scope_confirmation_binding") != bind_payload(bundle["scope_confirmation"]):
        raise ExecutionError("execution request scope confirmation binding mismatch")
    if request.get("Risk_Profile_assignment_binding") != bind_payload(bundle["risk_profile_assignment"]):
        raise ExecutionError("execution request Risk Profile binding mismatch")
    if request.get("requested_operation") != "PREPARE_SCOPED_EXECUTION":
        raise ExecutionError("unsupported requested operation")
    baseline = request.get("repository_baseline")
    if not isinstance(baseline, dict):
        raise ExecutionError("execution request repository baseline is required")
    for field in ["repository", "branch", "head"]:
        if not isinstance(baseline.get(field), str) or not baseline.get(field):
            raise ExecutionError(f"execution request repository baseline missing {field}")
    if request.get("repository_baseline") != proposal.get("repository_baseline_binding"):
        raise ExecutionError("execution request repository baseline mismatch")
    if any(value == "unknown" for value in [request.get("protected_or_canonical_impact"), request.get("destructive_impact"), request.get("lifecycle_impact")]):
        raise ExecutionError("UNKNOWN impact blocks execution preparation")
    return validation, proposal


def create_preview(bundle, request, witness, repository_root="."):
    validation, proposal = _validate_request(bundle, request)
    actions, expansion = _validate_actions(repository_root, request, proposal)
    if expansion:
        return expansion
    observation = observe_repository(repository_root, request["repository_baseline"], [a["relative_path"] for a in actions])
    validate_execution_witness(witness, request, observation)
    risk = bundle["risk_profile_assignment"]
    preview = {
        "preview_version": 1,
        "preview_id": "preview-" + request["request_binding"][:16],
        "task_id": request["task_id"],
        "proposal_version": proposal.get("proposal_version"),
        "repository": observation["repository"],
        "branch": observation["branch"],
        "head": observation["head"],
        "Risk_Profile": risk.get("selected_Risk_Profile"),
        "actor": witness.get("actor_reference"),
        "witness_expiry": witness.get("expires_at"),
        "read_scope": request.get("read_scope", []),
        "write_scope": request.get("write_scope", []),
        "planned_actions": actions,
        "protected_or_canonical_impact": request.get("protected_or_canonical_impact"),
        "destructive_impact": request.get("destructive_impact"),
        "lifecycle_impact": request.get("lifecycle_impact"),
        "required_validation": request.get("required_validation", []),
        "mandatory_controls": request.get("mandatory_controls", []),
        "grants": ["prepare_exact_execution_package"],
        "non_grants": ["production_file_mutation", *request.get("non_grants", [])],
        "blockers": [],
        "unknowns": [],
        "execution_request_valid": True,
        "execution_authorization_valid": True,
        "repository_observation_current": True,
        "execution_preview_created": True,
        "production_operation_started": False,
        "repository_files_modified": False,
        "control_state": "CONTROL_READY_FOR_EXECUTION",
        "operation_state": "OPERATION_PREVIEWED",
        "production_execution_available": False,
        "reason_code": "OPERATION_CONTROL_FOUNDATION_NOT_IMPLEMENTED",
    }
    preview["preview_binding"] = bind_payload(preview)
    preview["repository_observation"] = observation
    preview["validation_result_binding"] = request.get("validation_result_binding")
    return preview


def assemble_execution_package(bundle, request, witness, preview):
    observation = preview["repository_observation"]
    package = {
        "package_version": 1,
        "package_id": "execution-package-" + preview["preview_binding"][:16],
        "task_id": request["task_id"],
        "operation_class": "SCOPED_EXECUTION_PREPARATION",
        "request_binding": request["request_binding"],
        "preview_binding": preview["preview_binding"],
        "authorization_binding": bind_payload(witness),
        "repository_observation_binding": bind_payload(observation),
        "repository_baseline_binding": request["repository_baseline"],
        "candidate_actions": preview["planned_actions"],
        "required_validation": request.get("required_validation", []),
        "mandatory_controls": request.get("mandatory_controls", []),
        "execution_backend": {"status": "NOT_BOUND"},
        "production_execution": {"available": False, "reason_code": "OPERATION_CONTROL_FOUNDATION_NOT_IMPLEMENTED"},
        "grants": ["handoff_to_future_controlled_executor"],
        "non_grants": ["immediate_file_mutation", "commit", "push", "integration", "release", "lifecycle_mutation"],
        "approval": False,
        "evidence_of_success": False,
    }
    package["package_binding"] = bind_payload(package)
    return package


def assemble_orchestrator_result(bundle, request, witness, repository_root="."):
    preview = create_preview(bundle, request, witness, repository_root)
    if preview.get("control_state") == "CONTROL_SCOPE_EXPANSION_REQUIRED":
        return preview
    package = assemble_execution_package(bundle, request, witness, preview)
    return {
        "kind": "execute_preview",
        "execution_request_valid": True,
        "execution_authorization_valid": True,
        "repository_observation_current": True,
        "execution_preview_created": True,
        "execution_package_created": True,
        "production_operation_started": False,
        "repository_files_modified": False,
        "control_state": "CONTROL_READY_FOR_EXECUTION",
        "operation_state": "OPERATION_PREVIEWED",
        "production_execution_available": False,
        "reason_code": "OPERATION_CONTROL_FOUNDATION_NOT_IMPLEMENTED",
        "execution_preview": preview,
        "execution_package": package,
        "non_grants": package["non_grants"],
    }
