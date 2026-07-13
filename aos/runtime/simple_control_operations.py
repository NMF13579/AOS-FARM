import base64
import datetime
import json
import os
import re
from pathlib import Path

from aos.runtime.simple_control_planning import bind_payload


OPERATION_ID_RE = re.compile(r"^op-[a-f0-9]{24,64}$")
PROTECTED_ROOT_FILES = {
    "00_AOS_Core_Control.md",
    "01_AOS_Assembly_Pipelines_and_Build_Roadmap.md",
    "02_AOS_Governance_Control_Module_and_Safety_Rules.md",
}
PROTECTED_PREFIXES = {
    "aos/templates/execution-packages/",
}
SUPPORTED_ACTIONS = {"CREATE_FILE", "REPLACE_FILE"}
MAX_ACTIONS = 20
MAX_FILE_BYTES = 1024 * 1024
MAX_TOTAL_BYTES = 5 * 1024 * 1024
MAX_RECORD_BYTES = 256 * 1024
MAX_ERROR_LENGTH = 4000


class OperationError(Exception):
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


def canonical_payload(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(data):
    import hashlib

    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    import hashlib

    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_operation_id(execution_package):
    package_binding = require_package_binding(execution_package)
    return "op-" + package_binding[:32]


def validate_operation_id(operation_id):
    if not isinstance(operation_id, str) or not OPERATION_ID_RE.fullmatch(operation_id):
        raise OperationError("malformed operation_id")
    return operation_id


def require_package_binding(execution_package):
    if not isinstance(execution_package, dict):
        raise OperationError("execution package is required")
    expected = execution_package.get("package_binding")
    if not expected:
        raise OperationError("execution package binding is required")
    payload = dict(execution_package)
    payload.pop("package_binding", None)
    actual = bind_payload(payload)
    if actual != expected:
        raise OperationError("execution package binding mismatch")
    return expected


def require_repository_baseline(execution_package, owner):
    baseline = execution_package.get("repository_baseline_binding")
    if not isinstance(baseline, dict):
        raise OperationError(f"{owner} repository baseline is required")
    for field in ["repository", "branch", "head"]:
        if not isinstance(baseline.get(field), str) or not baseline.get(field):
            raise OperationError(f"{owner} repository baseline missing {field}")
    return baseline


def witness_binding(witness):
    return bind_payload(witness)


def create_production_execution_witness(operation_id, execution_package, actor_reference):
    validate_operation_id(operation_id)
    if not actor_reference:
        raise OperationError("actor_reference is required")
    package_binding = require_package_binding(execution_package)
    package_baseline = require_repository_baseline(execution_package, "execution package")
    return {
        "decision_type": "PRODUCTION_EXECUTION_AUTHORIZATION",
        "decision_id": "production-" + operation_id[3:19],
        "task_id": execution_package.get("task_id"),
        "task_binding": bind_payload({"task_id": execution_package.get("task_id")}),
        "operation_binding": operation_id,
        "proposal_binding": execution_package.get("proposal_binding") or execution_package.get("request_binding"),
        "execution_request_binding": execution_package.get("request_binding"),
        "execution_preview_binding": execution_package.get("preview_binding"),
        "execution_package_binding": package_binding,
        "command_contract_binding": bind_payload({"command_id": "EXECUTE", "contract_version": 1, "mode": "controlled_local_write"}),
        "repository_baseline_binding": package_baseline,
        "candidate_binding": package_binding,
        "actor_reference": actor_reference,
        "actor_role": "human",
        "authentication_level": "LOCAL_DECLARED",
        "decision_channel": "CLI",
        "decision_value": "AUTHORIZED",
        "issued_at": now_iso(),
        "expires_at": future_iso(),
        "single_use": True,
        "consumed_at": None,
        "grants": ["apply_exact_execution_package_once"],
        "non_grants": [
            "scope_expansion",
            "protected_canonical_write",
            "destructive_operation",
            "commit",
            "push",
            "integration",
            "merge",
            "release",
            "lifecycle_mutation",
        ],
        "agent_generated_record_is_human_approval": False,
        "evidence_can_replace_witness": False,
        "expired_decision_usable": False,
        "consumed_single_use_decision_usable": False,
    }


def validate_production_witness(witness, operation_id, execution_package):
    validate_operation_id(operation_id)
    package_binding = require_package_binding(execution_package)
    if not isinstance(witness, dict):
        raise OperationError("production execution witness is required")
    package_baseline = require_repository_baseline(execution_package, "execution package")
    witness_baseline = witness.get("repository_baseline_binding")
    if not isinstance(witness_baseline, dict):
        raise OperationError("production witness repository baseline is required")
    if witness.get("decision_type") != "PRODUCTION_EXECUTION_AUTHORIZATION":
        raise OperationError("wrong production witness decision type")
    if not witness.get("actor_reference"):
        raise OperationError("production witness actor missing")
    if witness.get("operation_binding") != operation_id:
        raise OperationError("production witness operation binding mismatch")
    if witness.get("execution_package_binding") != package_binding:
        raise OperationError("production witness package binding mismatch")
    if witness_baseline != package_baseline:
        raise OperationError("production witness repository baseline mismatch")
    if witness.get("single_use") is not True:
        raise OperationError("production witness must be single-use")
    if witness.get("consumed_at") is not None:
        raise OperationError("consumed production witness cannot be reused")
    expires = parse_time(witness.get("expires_at"))
    if expires and expires <= datetime.datetime.now(datetime.timezone.utc):
        raise OperationError("production witness expired")
    grants = set(witness.get("grants", []))
    forbidden = {"commit", "push", "integration", "merge", "release", "lifecycle_mutation", "production_file_mutation"}
    if grants & forbidden:
        raise OperationError("production witness grants forbidden operation")
    if "apply_exact_execution_package_once" not in grants:
        raise OperationError("production witness missing apply grant")
    return True


def safe_relative_path(repository_root, relative_path):
    if not isinstance(relative_path, str) or not relative_path:
        raise OperationError("relative path is required")
    candidate = Path(relative_path)
    if candidate.is_absolute():
        raise OperationError("absolute paths are forbidden")
    if any(part in {"..", ""} for part in candidate.parts):
        raise OperationError("path traversal is forbidden")
    normalized = candidate.as_posix()
    if normalized in PROTECTED_ROOT_FILES or any(normalized.startswith(prefix) for prefix in PROTECTED_PREFIXES):
        raise OperationError("protected or canonical path is blocked")
    root = Path(repository_root).resolve()
    current = root
    for part in candidate.parts[:-1]:
        current = current / part
        if current.exists() and current.is_symlink():
            raise OperationError("symlink parent component is blocked")
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise OperationError("repository escape is blocked") from exc
    if resolved.exists() and resolved.is_symlink():
        raise OperationError("target symlink is blocked")
    return normalized


def content_bytes(action):
    proposed = action.get("proposed_content", {})
    if proposed.get("encoding") != "UTF-8":
        raise OperationError("proposed content must be UTF-8")
    if "text" in proposed:
        data = proposed["text"].encode("utf-8")
    elif "base64" in proposed:
        data = base64.b64decode(proposed["base64"], validate=True)
    else:
        raise OperationError("proposed content bytes are required")
    if len(data) != proposed.get("size_bytes"):
        raise OperationError("proposed content size mismatch")
    if sha256_bytes(data) != proposed.get("sha256"):
        raise OperationError("proposed content digest mismatch")
    return data


def validate_actions(execution_package, repository_root):
    actions = execution_package.get("candidate_actions", [])
    if not isinstance(actions, list):
        raise OperationError("candidate actions must be a list")
    if len(actions) > MAX_ACTIONS:
        raise OperationError("operation limit exceeded")
    seen = {}
    total = 0
    normalized = []
    for raw in actions:
        action = dict(raw)
        action_type = action.get("action_type")
        if action_type not in SUPPORTED_ACTIONS:
            raise OperationError("unsupported action type")
        path = safe_relative_path(repository_root, action.get("relative_path"))
        if path in seen:
            raise OperationError("duplicate action target")
        seen[path] = action_type
        data = content_bytes(action)
        total += len(data)
        if len(data) > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
            raise OperationError("operation limit exceeded")
        action["relative_path"] = path
        action["_content_bytes"] = data
        normalized.append(action)
    return sorted(normalized, key=lambda item: item["relative_path"])


class OperationStore:
    def __init__(self, repository_root):
        self.repository_root = Path(repository_root).resolve()
        base = self.repository_root / ".aos-tmp" / "simple-control"
        self.base = base
        self.operations = base / "operations"
        self.locks = base / "locks"
        self.consumed = base / "consumed"

    def ensure(self):
        self.operations.mkdir(parents=True, exist_ok=True)
        self.locks.mkdir(parents=True, exist_ok=True)
        self.consumed.mkdir(parents=True, exist_ok=True)

    def record_path(self, operation_id):
        return self.operations / f"{operation_id}.json"

    def lock_path(self, operation_id):
        return self.locks / f"{operation_id}.lock"

    def consumed_path(self, binding):
        return self.consumed / f"{binding}.json"

    def read_record(self, operation_id):
        path = self.record_path(operation_id)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise OperationError("operation record is malformed") from exc

    def write_record(self, record):
        self.ensure()
        data = json.dumps(record, sort_keys=True, indent=2, ensure_ascii=False)
        if len(data.encode("utf-8")) > MAX_RECORD_BYTES:
            raise OperationError("operation record size limit exceeded")
        path = self.record_path(record["operation_id"])
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(data, encoding="utf-8")
        os.replace(tmp, path)

    def create_record_exclusive(self, record):
        self.ensure()
        path = self.record_path(record["operation_id"])
        data = json.dumps(record, sort_keys=True, indent=2, ensure_ascii=False)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        try:
            fd = os.open(path, flags, 0o600)
        except FileExistsError as exc:
            raise OperationError("operation already recorded") from exc
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())

    def acquire_lock(self, operation_id):
        self.ensure()
        path = self.lock_path(operation_id)
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as exc:
            raise OperationError("operation already claimed") from exc
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps({"operation_id": operation_id, "claimed_at": now_iso()}))
            handle.flush()
            os.fsync(handle.fileno())

    def consume_witness(self, binding, operation_id, package_binding):
        self.ensure()
        path = self.consumed_path(binding)
        payload = {"witness_binding": binding, "operation_id": operation_id, "package_binding": package_binding, "consumed_at": now_iso()}
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as exc:
            raise OperationError("authorization witness already consumed") from exc
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, sort_keys=True))
            handle.flush()
            os.fsync(handle.fileno())


def initial_record(operation_id, execution_package, authorization_binding, actions):
    timestamp = now_iso()
    return {
        "operation_record_version": 1,
        "operation_id": operation_id,
        "task_id": execution_package.get("task_id"),
        "execution_package_binding": execution_package.get("package_binding"),
        "authorization_binding": authorization_binding,
        "repository_baseline_binding": execution_package.get("repository_baseline_binding"),
        "operation_state": "OPERATION_REQUESTED",
        "requested_actions": [{k: v for k, v in action.items() if k != "_content_bytes"} for action in actions],
        "completed_actions": [],
        "created_at": timestamp,
        "updated_at": timestamp,
        "started_at": None,
        "completed_at": None,
        "side_effect_started": False,
        "side_effect_verified": False,
        "preimage_results": [],
        "postimage_results": [],
        "last_error": None,
        "reconciliation_required": False,
        "approval_status": "NOT_PROVIDED",
        "Evidence_status": "NOT_RUN",
    }


def update_record(store, record, state, **fields):
    record["operation_state"] = state
    record["updated_at"] = now_iso()
    record.update(fields)
    store.write_record(record)


def verify_preconditions(repository_root, actions):
    root = Path(repository_root).resolve()
    results = []
    for action in actions:
        target = root / action["relative_path"]
        expected = action.get("expected_preimage", {})
        if action["action_type"] == "CREATE_FILE":
            if expected.get("existence") is not False:
                raise OperationError("CREATE_FILE requires absent preimage")
            if target.exists():
                raise OperationError("CREATE_FILE target already exists")
            parent = target.parent
            if not parent.exists() or not parent.is_dir() or parent.is_symlink():
                raise OperationError("CREATE_FILE parent is invalid")
            results.append({"action_id": action.get("action_id"), "path": action["relative_path"], "status": "ABSENT"})
        elif action["action_type"] == "REPLACE_FILE":
            if not target.exists() or not target.is_file() or target.is_symlink():
                raise OperationError("REPLACE_FILE target is invalid")
            actual = sha256_file(target)
            if actual != expected.get("sha256"):
                raise OperationError("preimage mismatch")
            results.append({"action_id": action.get("action_id"), "path": action["relative_path"], "status": "MATCH", "sha256": actual})
    return results


def fsync_parent(path):
    if not hasattr(os, "O_DIRECTORY"):
        raise OperationError("directory fsync is unavailable")
    try:
        fd = os.open(str(Path(path).parent), os.O_RDONLY | os.O_DIRECTORY)
    except OSError as exc:
        raise OperationError("directory fsync open failed") from exc
    try:
        os.fsync(fd)
    except OSError as exc:
        raise OperationError("directory fsync failed") from exc
    finally:
        os.close(fd)


def apply_action(repository_root, action):
    root = Path(repository_root).resolve()
    target = root / action["relative_path"]
    data = action["_content_bytes"]
    if action["action_type"] == "CREATE_FILE":
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        fsync_parent(target)
    elif action["action_type"] == "REPLACE_FILE":
        old_mode = stat_mode(target)
        tmp = target.with_name(f".{target.name}.{os.getpid()}.{action.get('action_id')}.tmp")
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, old_mode)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(tmp, old_mode)
            os.replace(tmp, target)
            fsync_parent(target)
        except Exception:
            try:
                tmp.unlink()
            except OSError:
                pass
            raise
    final = sha256_file(target)
    expected = action.get("proposed_content", {}).get("sha256")
    if final != expected:
        raise OperationError("postimage mismatch")
    return {"action_id": action.get("action_id"), "path": action["relative_path"], "sha256": final}


def stat_mode(path):
    import stat

    return stat.S_IMODE(Path(path).stat().st_mode)


def active_repository_guard(repository_root):
    if Path(repository_root).resolve() == active_repository_root().resolve():
        raise OperationError("controlled write backend cannot apply to active AOS-FARM repository in this task")


def operation_result(operation_id, state, **fields):
    result = {
        "result_version": 1,
        "operation_id": operation_id,
        "operation_state": state,
        "control_state": "CONTROL_CHANGES_PREPARED" if state == "OPERATION_COMPLETED" else "CONTROL_BLOCKED",
        "side_effect_started": False,
        "side_effect_verified": False,
        "commit_performed": False,
        "push_performed": False,
        "integration_performed": False,
        "approval_status": "NOT_PROVIDED",
        "Evidence_status": "NOT_RUN",
        "rollback_available": False,
        "platform_enforced": False,
    }
    result.update(fields)
    return result


def apply_execution_package(execution_package, witness, operation_id, repository_root, store_root=None):
    validate_operation_id(operation_id)
    active_repository_guard(repository_root)
    package_binding = require_package_binding(execution_package)
    expected_operation_id = create_operation_id(execution_package)
    if operation_id != expected_operation_id:
        raise OperationError("operation_id does not match execution package")
    validate_production_witness(witness, operation_id, execution_package)
    actions = validate_actions(execution_package, repository_root)
    store = OperationStore(store_root or repository_root)
    existing = store.read_record(operation_id)
    if existing:
        if existing.get("execution_package_binding") != package_binding:
            return operation_result(operation_id, "OPERATION_FAILED", reason_code="OPERATION_BINDING_CONFLICT")
        if existing.get("operation_state") == "OPERATION_COMPLETED":
            reconciliation = reconcile_operation(execution_package, operation_id, repository_root)
            reconciliation["side_effect_repeated"] = False
            return reconciliation
        if existing.get("operation_state") in {"OPERATION_STARTED", "OPERATION_VERIFYING", "OPERATION_RECONCILIATION_REQUIRED"}:
            return operation_result(operation_id, "OPERATION_RECONCILIATION_REQUIRED", reason_code="OPERATION_ALREADY_STARTED", reconciliation_required=True)

    authorization_binding = witness_binding(witness)
    record = initial_record(operation_id, execution_package, authorization_binding, actions)
    store.create_record_exclusive(record)
    try:
        store.acquire_lock(operation_id)
    except OperationError:
        update_record(store, record, "OPERATION_RECONCILIATION_REQUIRED", reconciliation_required=True, last_error="operation already claimed")
        return operation_result(operation_id, "OPERATION_RECONCILIATION_REQUIRED", reason_code="OPERATION_ALREADY_CLAIMED", reconciliation_required=True)

    update_record(store, record, "OPERATION_CONFIRMED")
    try:
        preimages = verify_preconditions(repository_root, actions)
        update_record(store, record, "OPERATION_PRECONDITIONS_VERIFIED", preimage_results=preimages)
        store.consume_witness(authorization_binding, operation_id, package_binding)
        update_record(store, record, "OPERATION_STARTED", started_at=now_iso(), side_effect_started=True)
        completed = []
        postimages = []
        for action in actions:
            try:
                post = apply_action(repository_root, action)
            except Exception as exc:
                message = str(exc)[:MAX_ERROR_LENGTH]
                update_record(
                    store,
                    record,
                    "OPERATION_RECONCILIATION_REQUIRED",
                    completed_actions=[item["action_id"] for item in completed],
                    postimage_results=postimages,
                    last_error=message,
                    reconciliation_required=True,
                    side_effect_started=True,
                )
                return operation_result(
                    operation_id,
                    "OPERATION_RECONCILIATION_REQUIRED",
                    reason_code="PARTIAL_OPERATION_RECONCILIATION_REQUIRED",
                    completed_actions=[item["action_id"] for item in completed],
                    reconciliation_required=True,
                    side_effect_started=True,
                    side_effect_verified=False,
                )
            completed.append(action)
            postimages.append(post)
            update_record(store, record, "OPERATION_VERIFYING", completed_actions=[item["action_id"] for item in completed], postimage_results=postimages, side_effect_started=True)
        update_record(
            store,
            record,
            "OPERATION_COMPLETED",
            completed_actions=[item["action_id"] for item in completed],
            postimage_results=postimages,
            side_effect_started=True,
            side_effect_verified=True,
            completed_at=now_iso(),
        )
        return operation_result(
            operation_id,
            "OPERATION_COMPLETED",
            side_effect_started=True,
            side_effect_verified=True,
            completed_actions=[item["action_id"] for item in completed],
            postimage_results=postimages,
        )
    except OperationError as exc:
        update_record(store, record, "OPERATION_FAILED", last_error=str(exc)[:MAX_ERROR_LENGTH], side_effect_started=False)
        raise


def target_state(repository_root, action):
    target = Path(repository_root).resolve() / action["relative_path"]
    preimage = action.get("expected_preimage", {})
    post = action.get("proposed_content", {}).get("sha256")
    if not target.exists():
        if preimage.get("existence") is False:
            return "pre"
        return "unknown"
    if not target.is_file() or target.is_symlink():
        return "unknown"
    actual = sha256_file(target)
    if actual == post:
        return "post"
    if preimage.get("existence") is True and actual == preimage.get("sha256"):
        return "pre"
    return "unknown"


def reconcile_operation(execution_package, operation_id, repository_root, store_root=None):
    validate_operation_id(operation_id)
    package_binding = require_package_binding(execution_package)
    actions = validate_actions(execution_package, repository_root)
    states = [target_state(repository_root, action) for action in actions]
    if all(state == "post" for state in states):
        result = "ALREADY_COMPLETED_VERIFIED"
        operation_state = "OPERATION_COMPLETED"
        automatic_retry = False
    elif all(state == "pre" for state in states):
        result = "SAFE_TO_RETRY"
        operation_state = "OPERATION_PRECONDITIONS_VERIFIED"
        automatic_retry = True
    elif "unknown" in states:
        result = "UNKNOWN_BLOCKED"
        operation_state = "OPERATION_RECONCILIATION_REQUIRED"
        automatic_retry = False
    else:
        result = "PARTIALLY_COMPLETED"
        operation_state = "OPERATION_RECONCILIATION_REQUIRED"
        automatic_retry = False
    return {
        "reconciliation_version": 1,
        "operation_id": operation_id,
        "execution_package_binding": package_binding,
        "reconciliation_result": result,
        "operation_state": operation_state,
        "control_state": "CONTROL_UNKNOWN_BLOCKED" if result == "UNKNOWN_BLOCKED" else ("CONTROL_CHANGES_PREPARED" if result == "ALREADY_COMPLETED_VERIFIED" else "CONTROL_BLOCKED"),
        "automatic_retry": automatic_retry,
        "human_review_required": result in {"PARTIALLY_COMPLETED", "BLOCKED", "UNKNOWN_BLOCKED"},
        "side_effect_repeated": False,
        "rollback_available": False,
    }
