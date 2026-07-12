import datetime
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

from aos.runtime.simple_control_planning import bind_payload


MAX_STDOUT = 20000
MAX_MESSAGE_SUBJECT = 120
MAX_MESSAGE_BODY = 4000
GIT_TIMEOUT = 15
BUILD_REF_RE = re.compile(r"^refs/heads/build/[A-Za-z0-9._/-]+$")


class GitControlError(Exception):
    pass


def active_repository_root():
    return Path(__file__).resolve().parents[2]


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def future_iso(hours=1):
    return (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=hours)).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(value):
    if not value:
        return None
    return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))


def run_git(cwd, args, timeout=GIT_TIMEOUT):
    if not isinstance(args, list):
        raise GitControlError("git args must be an argv list")
    forbidden = [
        ["add", "-A"],
        ["add", "."],
        ["commit", "-a"],
        ["commit", "--amend"],
        ["reset"],
        ["clean"],
        ["checkout"],
        ["switch"],
        ["rebase"],
        ["merge"],
    ]
    for pattern in forbidden:
        if args[: len(pattern)] == pattern:
            raise GitControlError(f"forbidden git invocation: {' '.join(args)}")
    if args and args[0] == "push":
        if any(part.startswith("--force") or part in {"--mirror", "--all", "--tags"} for part in args):
            raise GitControlError("forbidden push option")
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    result = subprocess.run(
        ["git", *args],
        cwd=str(Path(cwd).resolve()),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        env=env,
    )
    stdout = result.stdout[:MAX_STDOUT]
    stderr = result.stderr[:MAX_STDOUT]
    if result.returncode != 0:
        raise GitControlError(stderr or stdout or f"git {' '.join(args)} failed")
    return stdout.strip()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_repo_path(root, relative_path):
    if not isinstance(relative_path, str) or not relative_path:
        raise GitControlError("relative path is required")
    path = Path(relative_path)
    if path.is_absolute():
        raise GitControlError("absolute path is forbidden")
    if any(part in {"..", ""} for part in path.parts):
        raise GitControlError("path traversal is forbidden")
    repo = Path(root).resolve()
    target = (repo / path).resolve()
    try:
        target.relative_to(repo)
    except ValueError as exc:
        raise GitControlError("repository escape is forbidden") from exc
    current = repo
    for part in path.parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise GitControlError("symlink candidate path is forbidden")
    if target.exists() and target.is_dir():
        raise GitControlError("directory candidate path is forbidden")
    return path.as_posix()


def active_git_write_guard(root):
    if Path(root).resolve() == active_repository_root().resolve():
        raise GitControlError("active AOS-FARM repository Git write is not authorized")


def file_state(root, relative_path):
    tracked = run_git(root, ["ls-files", "--", relative_path])
    if tracked:
        return "MODIFIED"
    return "UNTRACKED"


def create_candidate_manifest(root, paths, task_id, repository_binding):
    seen = set()
    files = []
    for path in paths:
        safe = safe_repo_path(root, path)
        if safe in seen:
            raise GitControlError("duplicate candidate path")
        seen.add(safe)
        target = Path(root) / safe
        if not target.exists() or not target.is_file():
            raise GitControlError("candidate file must exist as regular file")
        files.append(
            {
                "relative_path": safe,
                "expected_state": file_state(root, safe),
                "content_sha256": sha256_file(target),
                "size_bytes": target.stat().st_size,
            }
        )
    manifest = {
        "manifest_version": 1,
        "manifest_id": "manifest-" + bind_payload(files)[:16],
        "repository_binding": repository_binding,
        "task_id": task_id,
        "files": sorted(files, key=lambda item: item["relative_path"]),
        "forbidden_paths": [],
        "unexpected_paths_policy": "BLOCK",
        "deletions_allowed": False,
        "renames_allowed": False,
    }
    manifest["candidate_binding"] = bind_payload({k: v for k, v in manifest.items() if k != "candidate_binding"})
    return manifest


def validate_manifest(root, manifest):
    if not isinstance(manifest, dict) or manifest.get("manifest_version") != 1:
        raise GitControlError("invalid candidate manifest")
    expected = manifest.get("candidate_binding")
    payload = dict(manifest)
    payload.pop("candidate_binding", None)
    if bind_payload(payload) != expected:
        raise GitControlError("candidate manifest binding mismatch")
    seen = set()
    for item in manifest.get("files", []):
        path = safe_repo_path(root, item.get("relative_path"))
        if path in seen:
            raise GitControlError("duplicate candidate path")
        seen.add(path)
        target = Path(root) / path
        if not target.exists() or not target.is_file():
            raise GitControlError("candidate file missing")
        if sha256_file(target) != item.get("content_sha256"):
            raise GitControlError("candidate digest mismatch")
    if manifest.get("deletions_allowed") or manifest.get("renames_allowed"):
        raise GitControlError("delete and rename are forbidden")
    return True


def staged_tree_binding_from_manifest(manifest):
    return bind_payload({"files": [{"path": f["relative_path"], "sha256": f["content_sha256"]} for f in manifest.get("files", [])]})


def validate_commit_message(subject, body):
    if not isinstance(subject, str) or not subject.strip() or "\n" in subject or len(subject) > MAX_MESSAGE_SUBJECT:
        raise GitControlError("invalid commit subject")
    if not isinstance(body, str) or len(body) > MAX_MESSAGE_BODY:
        raise GitControlError("invalid commit body")


def create_commit_request(manifest, operation_id, subject, body, repository_baseline):
    validate_commit_message(subject, body)
    request = {
        "request_version": 1,
        "request_id": "commit-request-" + manifest["candidate_binding"][:16],
        "operation_id": operation_id,
        "task_id": manifest.get("task_id"),
        "candidate_manifest_binding": manifest["candidate_binding"],
        "repository_baseline": repository_baseline,
        "commit_message": {"subject": subject, "body": body},
        "expected_paths": [item["relative_path"] for item in manifest.get("files", [])],
        "expected_staged_tree_binding": staged_tree_binding_from_manifest(manifest),
        "non_grants": ["push", "integration", "merge", "release", "lifecycle_mutation"],
    }
    request["commit_message_binding"] = bind_payload(request["commit_message"])
    request["request_binding"] = bind_payload({k: v for k, v in request.items() if k != "request_binding"})
    return request


def create_commit_preview(root, manifest, request):
    validate_manifest(root, manifest)
    return {
        "preview_version": 1,
        "preview_id": "commit-preview-" + request["request_binding"][:16],
        "repository": manifest["repository_binding"].get("repository"),
        "branch": manifest["repository_binding"].get("branch"),
        "current_HEAD": manifest["repository_binding"].get("head"),
        "candidate_paths": request.get("expected_paths", []),
        "file_digests": {item["relative_path"]: item["content_sha256"] for item in manifest.get("files", [])},
        "staged_state_before": run_git(root, ["diff", "--cached", "--name-only"]),
        "expected_staged_tree_binding": request.get("expected_staged_tree_binding"),
        "commit_message": request.get("commit_message"),
        "grants": ["stage_exact_candidate_manifest", "create_one_ordinary_commit"],
        "non_grants": request.get("non_grants", []),
        "preview_created": True,
        "staging_started": False,
        "commit_started": False,
        "push_started": False,
        "commit_signing_status": "REPOSITORY_DEFAULT",
        "hooks_policy": "DO_NOT_BYPASS",
    }


def create_commit_witness(manifest, request, preview, actor_reference):
    if not actor_reference:
        raise GitControlError("actor_reference is required")
    return {
        "decision_type": "COMMIT_AUTHORIZATION",
        "decision_id": "commit-" + request["request_binding"][:16],
        "task_id": request.get("task_id"),
        "task_binding": bind_payload({"task_id": request.get("task_id")}),
        "operation_id": request.get("operation_id"),
        "operation_binding": request.get("operation_id"),
        "candidate_manifest_binding": manifest.get("candidate_binding"),
        "commit_request_binding": request.get("request_binding"),
        "commit_preview_binding": preview.get("preview_binding"),
        "command_contract_binding": bind_payload({"command_id": "COMMIT", "contract_version": 1}),
        "repository_baseline_binding": request.get("repository_baseline"),
        "expected_staged_tree_binding": request.get("expected_staged_tree_binding"),
        "commit_message_binding": request.get("commit_message_binding"),
        "proposal_binding": None,
        "execution_request_binding": None,
        "candidate_binding": manifest.get("candidate_binding"),
        "actor_reference": actor_reference,
        "actor_role": "human",
        "authentication_level": "LOCAL_DECLARED",
        "decision_channel": "CLI",
        "decision_value": "AUTHORIZED",
        "issued_at": now_iso(),
        "expires_at": future_iso(),
        "single_use": True,
        "consumed_at": None,
        "grants": ["stage_exact_candidate_manifest", "create_one_ordinary_commit"],
        "non_grants": ["amend", "history_rewrite", "push", "integration", "merge", "release", "lifecycle_mutation"],
        "agent_generated_record_is_human_approval": False,
        "evidence_can_replace_witness": False,
        "expired_decision_usable": False,
        "consumed_single_use_decision_usable": False,
    }


def validate_commit_witness(witness, manifest, request):
    if not isinstance(witness, dict):
        raise GitControlError("commit witness required")
    if witness.get("decision_type") != "COMMIT_AUTHORIZATION":
        raise GitControlError("wrong commit witness decision type")
    if not witness.get("actor_reference"):
        raise GitControlError("commit witness actor missing")
    if witness.get("candidate_manifest_binding") != manifest.get("candidate_binding"):
        raise GitControlError("commit witness candidate binding mismatch")
    if witness.get("commit_request_binding") != request.get("request_binding"):
        raise GitControlError("commit witness request binding mismatch")
    if witness.get("repository_baseline_binding") != request.get("repository_baseline"):
        raise GitControlError("commit witness baseline mismatch")
    if witness.get("expected_staged_tree_binding") != request.get("expected_staged_tree_binding"):
        raise GitControlError("commit witness staged tree mismatch")
    if witness.get("commit_message_binding") != request.get("commit_message_binding"):
        raise GitControlError("commit witness message binding mismatch")
    if witness.get("consumed_at") is not None:
        raise GitControlError("commit witness consumed")
    expires = parse_time(witness.get("expires_at"))
    if expires and expires <= datetime.datetime.now(datetime.timezone.utc):
        raise GitControlError("commit witness expired")
    grants = set(witness.get("grants", []))
    if "push" in grants or "integration" in grants or "history_rewrite" in grants:
        raise GitControlError("commit witness grants forbidden operation")
    return True


def git_store(root):
    path = Path(root) / ".aos-tmp" / "simple-control" / "git"
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_record(root, operation_id):
    path = git_store(root) / f"{operation_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_record(root, operation_id, record):
    path = git_store(root) / f"{operation_id}.json"
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(record, sort_keys=True, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def current_binding(root):
    return {
        "repository": "SANDBOX/AOS-FARM",
        "branch": run_git(root, ["branch", "--show-current"]),
        "head": run_git(root, ["rev-parse", "HEAD"]),
    }


def validate_baseline(root, expected):
    actual = current_binding(root)
    if actual.get("branch") != expected.get("branch") or actual.get("head") != expected.get("head"):
        raise GitControlError("repository baseline changed")


def verify_staged_tree(root, manifest):
    staged = run_git(root, ["diff", "--cached", "--name-only"]).splitlines()
    expected_paths = [item["relative_path"] for item in manifest.get("files", [])]
    if sorted(staged) != sorted(expected_paths):
        raise GitControlError("unexpected staged path")
    entries = []
    for path in expected_paths:
        data = git_blob_bytes(root, path)
        entries.append({"path": path, "sha256": sha256_bytes(data)})
    return bind_payload({"files": sorted(entries, key=lambda item: item["path"])})


def git_blob_bytes(root, path):
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    result = subprocess.run(
        ["git", "show", f":{path}"],
        cwd=str(Path(root).resolve()),
        capture_output=True,
        timeout=GIT_TIMEOUT,
        check=False,
        env=env,
    )
    if result.returncode != 0:
        raise GitControlError((result.stderr or result.stdout)[:MAX_STDOUT].decode("utf-8", errors="replace"))
    return result.stdout


def commit_result(root, request, commit_oid):
    return {
        "result_version": 1,
        "operation_id": request.get("operation_id"),
        "commit_state": "COMMIT_COMPLETED",
        "commit_oid": commit_oid,
        "parent_oid": run_git(root, ["rev-parse", f"{commit_oid}^"]),
        "commit_message_binding": request.get("commit_message_binding"),
        "push_performed": False,
        "integration_performed": False,
        "approval_granted": False,
        "Evidence_status": "NOT_RUN",
    }


def reconcile_commit(root, manifest, request):
    record = read_record(root, request["operation_id"])
    if record and record.get("commit_state") == "COMMIT_COMPLETED":
        commit_oid = record.get("commit_oid")
        if run_git(root, ["rev-parse", "HEAD"]) == commit_oid:
            result = dict(record)
            result["reconciliation_result"] = "COMMIT_ALREADY_COMPLETED_VERIFIED"
            result["side_effect_repeated"] = False
            return result
    staged = run_git(root, ["diff", "--cached", "--name-only"])
    if staged:
        return {"reconciliation_result": "COMMIT_NOT_CREATED_INDEX_STAGED", "automatic_retry": False, "side_effect_repeated": False}
    return {"reconciliation_result": "SAFE_TO_RETRY_COMMIT", "automatic_retry": True, "side_effect_repeated": False}


def apply_commit(root, manifest, request, witness):
    active_git_write_guard(root)
    validate_manifest(root, manifest)
    if read_record(root, request["operation_id"]):
        return reconcile_commit(root, manifest, request)
    validate_commit_witness(witness, manifest, request)
    validate_baseline(root, request.get("repository_baseline", {}))
    if run_git(root, ["diff", "--cached", "--name-only"]):
        raise GitControlError("unexpected staged path")
    paths = [item["relative_path"] for item in manifest.get("files", [])]
    run_git(root, ["add", "--", *paths])
    staged_binding = verify_staged_tree(root, manifest)
    if staged_binding != request.get("expected_staged_tree_binding"):
        raise GitControlError("staged tree mismatch")
    message = request["commit_message"]
    args = ["commit", "-m", message["subject"]]
    if message.get("body"):
        args.extend(["-m", message["body"]])
    run_git(root, args)
    commit_oid = run_git(root, ["rev-parse", "HEAD"])
    if run_git(root, ["diff", "--cached", "--name-only"]):
        raise GitControlError("index not clean after commit")
    result = commit_result(root, request, commit_oid)
    write_record(root, request["operation_id"], result)
    return result


def validate_build_ref(ref):
    if not isinstance(ref, str) or ref.startswith(":") or "*" in ref or not BUILD_REF_RE.fullmatch(ref):
        raise GitControlError("target ref must be exact build branch")
    if ref in {"refs/heads/dev", "refs/heads/main"} or ref.startswith("refs/tags/"):
        raise GitControlError("target ref is forbidden")
    return True


def observe_remote_ref(root, remote_name, target_ref):
    validate_build_ref(target_ref)
    output = run_git(root, ["ls-remote", "--refs", remote_name, target_ref])
    if not output:
        return None
    parts = output.split()
    if len(parts) < 2 or parts[1] != target_ref:
        raise GitControlError("remote ref observation ambiguous")
    return parts[0]


def create_push_request(root, operation_id, task_id, commit_result_payload, remote_name, target_ref, expected_remote_oid):
    validate_build_ref(target_ref)
    remote_url = run_git(root, ["remote", "get-url", remote_name])
    source = commit_result_payload["commit_oid"]
    request = {
        "request_version": 1,
        "request_id": "push-request-" + source[:16],
        "operation_id": operation_id,
        "task_id": task_id,
        "repository_binding": {
            "repository": "SANDBOX/AOS-FARM",
            "branch": run_git(root, ["branch", "--show-current"]),
            "head": source,
        },
        "remote": {
            "name": remote_name,
            "url_binding": bind_payload({"url": remote_url}),
            "target_ref": target_ref,
            "expected_remote_oid": expected_remote_oid,
        },
        "source_commit_oid": source,
        "commit_result_binding": bind_payload(commit_result_payload),
        "force": False,
        "delete": False,
        "non_grants": ["integration", "merge", "release", "lifecycle_mutation"],
    }
    request["request_binding"] = bind_payload({k: v for k, v in request.items() if k != "request_binding"})
    return request


def create_push_preview(root, request):
    remote_oid = observe_remote_ref(root, request["remote"]["name"], request["remote"]["target_ref"])
    return {
        "preview_version": 1,
        "preview_id": "push-preview-" + request["request_binding"][:16],
        "source_commit_oid": request["source_commit_oid"],
        "remote_oid": remote_oid,
        "target_ref": request["remote"]["target_ref"],
        "preview_created": True,
        "push_started": False,
        "integration_started": False,
    }


def create_push_witness(push_request, actor_reference):
    if not actor_reference:
        raise GitControlError("actor_reference is required")
    preview = {"preview_binding": bind_payload({"request": push_request["request_binding"]})}
    return {
        "decision_type": "PUSH_AUTHORIZATION",
        "decision_id": "push-" + push_request["request_binding"][:16],
        "task_id": push_request.get("task_id"),
        "task_binding": bind_payload({"task_id": push_request.get("task_id")}),
        "operation_id": push_request.get("operation_id"),
        "operation_binding": push_request.get("operation_id"),
        "commit_oid": push_request.get("source_commit_oid"),
        "commit_result_binding": push_request.get("commit_result_binding"),
        "push_request_binding": push_request.get("request_binding"),
        "push_preview_binding": preview["preview_binding"],
        "command_contract_binding": bind_payload({"command_id": "PUSH", "contract_version": 1}),
        "remote_name": push_request["remote"]["name"],
        "remote_url_binding": push_request["remote"]["url_binding"],
        "target_ref": push_request["remote"]["target_ref"],
        "expected_remote_oid": push_request["remote"].get("expected_remote_oid"),
        "repository_baseline_binding": push_request.get("repository_binding"),
        "proposal_binding": None,
        "execution_request_binding": None,
        "candidate_binding": push_request.get("commit_result_binding"),
        "actor_reference": actor_reference,
        "actor_role": "human",
        "authentication_level": "LOCAL_DECLARED",
        "decision_channel": "CLI",
        "decision_value": "AUTHORIZED",
        "issued_at": now_iso(),
        "expires_at": future_iso(),
        "single_use": True,
        "consumed_at": None,
        "grants": ["push_exact_commit_to_exact_build_ref"],
        "non_grants": ["push_other_commit", "push_other_ref", "push_to_dev", "push_to_main", "force_push", "tag_push", "integration", "merge", "release", "branch_deletion", "lifecycle_mutation"],
        "agent_generated_record_is_human_approval": False,
        "evidence_can_replace_witness": False,
        "expired_decision_usable": False,
        "consumed_single_use_decision_usable": False,
    }


def validate_push_witness(witness, request):
    if not isinstance(witness, dict):
        raise GitControlError("push witness required")
    if witness.get("decision_type") != "PUSH_AUTHORIZATION":
        raise GitControlError("wrong push witness decision type")
    if not witness.get("actor_reference"):
        raise GitControlError("push witness actor missing")
    if witness.get("commit_oid") != request.get("source_commit_oid"):
        raise GitControlError("push witness commit mismatch")
    if witness.get("push_request_binding") != request.get("request_binding"):
        raise GitControlError("push witness request mismatch")
    if witness.get("remote_url_binding") != request["remote"].get("url_binding"):
        raise GitControlError("push witness remote mismatch")
    if witness.get("target_ref") != request["remote"].get("target_ref"):
        raise GitControlError("push witness target ref mismatch")
    if witness.get("expected_remote_oid") != request["remote"].get("expected_remote_oid"):
        raise GitControlError("push witness expected remote mismatch")
    if witness.get("consumed_at") is not None:
        raise GitControlError("push witness consumed")
    expires = parse_time(witness.get("expires_at"))
    if expires and expires <= datetime.datetime.now(datetime.timezone.utc):
        raise GitControlError("push witness expired")
    grants = set(witness.get("grants", []))
    if "integration" in grants or "merge" in grants or "release" in grants:
        raise GitControlError("push witness grants forbidden operation")
    return True


def reconcile_push(root, request):
    remote_oid = observe_remote_ref(root, request["remote"]["name"], request["remote"]["target_ref"])
    if remote_oid == request["source_commit_oid"]:
        return {"reconciliation_result": "PUSH_ALREADY_COMPLETED_VERIFIED", "side_effect_repeated": False, "automatic_retry": False}
    if remote_oid == request["remote"].get("expected_remote_oid"):
        return {"reconciliation_result": "SAFE_TO_RETRY_PUSH", "side_effect_repeated": False, "automatic_retry": True}
    return {"reconciliation_result": "REMOTE_ADVANCED_UNEXPECTEDLY", "side_effect_repeated": False, "automatic_retry": False, "human_review_required": True}


def apply_push(root, request, witness):
    active_git_write_guard(root)
    validate_build_ref(request["remote"]["target_ref"])
    if request.get("force") or request.get("delete"):
        raise GitControlError("force and delete push are forbidden")
    if run_git(root, ["rev-parse", "HEAD"]) != request.get("source_commit_oid"):
        raise GitControlError("source commit is not current HEAD")
    validate_push_witness(witness, request)
    current_remote = observe_remote_ref(root, request["remote"]["name"], request["remote"]["target_ref"])
    if current_remote == request["source_commit_oid"]:
        return reconcile_push(root, request)
    if current_remote != request["remote"].get("expected_remote_oid"):
        return {"push_state": "PUSH_BLOCKED", "reconciliation_result": "REMOTE_ADVANCED_UNEXPECTEDLY", "automatic_retry": False, "integration_performed": False}
    refspec = f"{request['source_commit_oid']}:{request['remote']['target_ref']}"
    run_git(root, ["push", "--porcelain", request["remote"]["name"], refspec])
    verified = observe_remote_ref(root, request["remote"]["name"], request["remote"]["target_ref"])
    if verified != request["source_commit_oid"]:
        return {"push_state": "PUSH_RECONCILIATION_REQUIRED", "reconciliation_result": "PUSH_PARTIAL_OR_UNKNOWN", "automatic_retry": False, "integration_performed": False}
    result = {
        "result_version": 1,
        "operation_id": request.get("operation_id"),
        "push_state": "PUSH_COMPLETED",
        "commit_oid": request.get("source_commit_oid"),
        "target_ref": request["remote"]["target_ref"],
        "remote_oid": verified,
        "integration_performed": False,
        "release_performed": False,
        "approval_granted": False,
    }
    write_record(root, request["operation_id"], result)
    return result
