from enum import Enum
from typing import Dict, Any, Optional
import re
from datetime import datetime, timezone

class WorkspaceLockState(Enum):
    ABSENT = "ABSENT"
    PRESENT_SELF = "PRESENT_SELF"
    PRESENT_OTHER = "PRESENT_OTHER"
    STALE = "STALE"
    CONFLICT = "CONFLICT"
    UNKNOWN = "UNKNOWN"
    NOT_CHECKED = "NOT_CHECKED"

class WorkspaceLockSourceType(Enum):
    EXPLICIT_VALIDATION_INPUT = "EXPLICIT_VALIDATION_INPUT"
    AUTHORITATIVE_SYSTEM_LOCK = "AUTHORITATIVE_SYSTEM_LOCK"
    UNKNOWN_SOURCE = "UNKNOWN_SOURCE"

def validate_workspace_instance_id(workspace_id: str) -> Dict[str, Any]:
    if not workspace_id:
        return {"status": "BLOCKED", "error_code": "MISSING_WORKSPACE_INSTANCE_ID"}
    if len(workspace_id) == 0:
        return {"status": "BLOCKED", "error_code": "EMPTY_WORKSPACE_INSTANCE_ID"}
    
    # Must only contain letters, numbers, dashes, underscores. No paths.
    if not re.match(r'^[a-zA-Z0-9_-]+$', workspace_id):
        return {"status": "BLOCKED", "error_code": "INVALID_WORKSPACE_INSTANCE_ID_CHARACTERS"}

    return {"status": "PASS", "error_code": None}

def validate_workspace_state_binding(validated_package: dict, repository_root: str) -> Dict[str, Any]:
    """Validates the repository baseline state against the execution package.

    This validator checks consistency of the repository working tree state.
    It does NOT establish, authenticate, or independently prove workspace lock
    authority. Workspace lock authority requires a separate verified_adapter_context
    supplied by an external integration boundary via evaluate_workspace_lock_lookup.

    Fail-closed on missing repository state check, dirty tracked state, and
    untracked inventory without explicit package permission.
    PASS from this validator is not approval.
    """
    try:
        from .package_binding import bind_repository
        repo_results = bind_repository(validated_package, repository_root)
    except Exception:
        # Fail-closed: any exception during binding (e.g., wrong input type)
        # must not propagate as an unhandled error. Treat as UNKNOWN_BLOCKED.
        return {"status": "UNKNOWN_BLOCKED", "error_code": "BINDING_EXCEPTION"}

    repository_state_status = None
    for res in repo_results:
        if res["check"] == "baseline_state":
            repository_state_status = res
            break
            
    if not repository_state_status:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REPOSITORY_STATE_CHECK"}
        
    if repository_state_status["status"] != "PASS":
        return repository_state_status
        
    state = repository_state_status["actual"]
    if state["staged_changes_present"] or state["unstaged_tracked_changes_present"]:
        return {"status": "BLOCKED", "error_code": "DIRTY_TRACKED_STATE", "actual_state": state}
        
    if state["untracked_inventory_present"]:
        # Only accepted if required_checks permits untracked
        required = validated_package.get("required_checks", {})
        if required.get("tracked_clean", False):
            return {"status": "PASS", "error_code": None, "actual_state": state}
        else:
             return {"status": "BLOCKED", "error_code": "UNTRACKED_INVENTORY_PRESENT", "actual_state": state}

    return {"status": "PASS", "error_code": None, "actual_state": state}

def validate_workspace_lock_record(record: Dict[str, Any], expected_workspace_id: str, expected_session_id: str, expected_package_id: str, expected_package_digest: str, expected_authorization_id: str) -> Dict[str, Any]:
    allowed_fields = {"workspace_instance_id", "session_id", "package_id", "package_digest", "authorization_id", "lock_id", "lock_state", "created_at", "expires_at", "source_type"}
    if set(record.keys()) - allowed_fields:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_FIELD_IN_WORKSPACE_LOCK"}
    
    for req in ["workspace_instance_id", "session_id", "package_id", "package_digest", "authorization_id", "lock_id", "lock_state", "created_at", "expires_at", "source_type"]:
        if req not in record:
            return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REQUIRED_FIELD"}
            
    if validate_workspace_instance_id(record["workspace_instance_id"])["status"] != "PASS":
        return {"status": "BLOCKED", "error_code": "INVALID_WORKSPACE_INSTANCE_ID_FORMAT"}
        
    if not isinstance(record["session_id"], str) or len(record["session_id"]) < 8 or len(record["session_id"]) > 256:
        return {"status": "BLOCKED", "error_code": "INVALID_SESSION_ID_FORMAT"}
        
    if not isinstance(record["package_digest"], str) or len(record["package_digest"]) != 64 or not record["package_digest"].islower() or not all(c in '0123456789abcdef' for c in record["package_digest"]):
        return {"status": "BLOCKED", "error_code": "INVALID_PACKAGE_DIGEST_FORMAT"}
        
    try:
        dt_c = datetime.strptime(record["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        dt_c = dt_c.replace(tzinfo=timezone.utc)
        dt_e = datetime.strptime(record["expires_at"], "%Y-%m-%dT%H:%M:%SZ")
        dt_e = dt_e.replace(tzinfo=timezone.utc)
        if dt_e <= dt_c:
             return {"status": "BLOCKED", "error_code": "EXPIRES_BEFORE_CREATED"}
    except ValueError:
        return {"status": "BLOCKED", "error_code": "INVALID_TIMESTAMP_FORMAT"}
        
    if record["source_type"] not in [e.value for e in WorkspaceLockSourceType]:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_SOURCE_TYPE"}
        
    if record["source_type"] == WorkspaceLockSourceType.AUTHORITATIVE_SYSTEM_LOCK.value:
         return {"status": "UNKNOWN_BLOCKED", "error_code": "SELF_DECLARED_AUTHORITATIVE_SYSTEM_LOCK"}

    state = record.get("lock_state")
    try:
        ls = WorkspaceLockState(state)
    except ValueError:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "INVALID_LOCK_STATE"}

    if ls == WorkspaceLockState.ABSENT:
        return {"status": "PASS", "error_code": None}

    # Only PRESENT_SELF requires exact matching
    if ls == WorkspaceLockState.PRESENT_SELF:
        if record["workspace_instance_id"] != expected_workspace_id:
            return {"status": "BLOCKED", "error_code": "WORKSPACE_INSTANCE_ID_MISMATCH"}
        if record["session_id"] != expected_session_id:
            return {"status": "BLOCKED", "error_code": "SESSION_ID_MISMATCH"}
        if record["package_id"] != expected_package_id:
            return {"status": "BLOCKED", "error_code": "PACKAGE_ID_MISMATCH"}
        if record["package_digest"] != expected_package_digest:
            return {"status": "BLOCKED", "error_code": "PACKAGE_DIGEST_MISMATCH"}
        if record["authorization_id"] != expected_authorization_id:
            return {"status": "BLOCKED", "error_code": "AUTHORIZATION_ID_MISMATCH"}
            
        return {"status": "PASS", "error_code": None}

    if ls in (WorkspaceLockState.PRESENT_OTHER, WorkspaceLockState.STALE, WorkspaceLockState.CONFLICT):
        return {"status": "BLOCKED", "error_code": f"UNSAFE_LOCK_STATE_{ls.value}"}
        
    return {"status": "UNKNOWN_BLOCKED", "error_code": f"INDETERMINATE_LOCK_STATE_{ls.value}"}

def evaluate_workspace_lock_lookup(lookup_result: Dict[str, Any], expected_workspace_id: str, expected_session_id: str, expected_package_id: str, expected_package_digest: str, expected_authorization_id: str, verified_adapter_context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Evaluates a workspace lock lookup result against the verified adapter context.

    Trust precondition contract:
    - verified_adapter_context is a trusted precondition supplied by an external
      integration boundary. It must be provided separately from the lookup result.
    - This validator checks consistency and maps workspace lock states.
    - This validator does NOT establish, authenticate, or independently prove
      adapter authority. The authority_verified field in verified_adapter_context
      is asserted by the external boundary, not proved by this function.
    - Claim ceiling: TRUST_PRECONDITION_ACCEPTED, ADAPTER_CONTEXT_CONSISTENCY_VALIDATED,
      LOOKUP_MAPPING_CONTRACT_VALIDATED, FAIL_CLOSED_ON_UNVERIFIED_CONTEXT.
    - Forbidden claims: ADAPTER_AUTHORITY_PROVEN, AUTHORITATIVE_LOCK_ABSENCE_ESTABLISHED,
      WORKSPACE_LOCK_ENFORCED, CROSS_PROCESS_SAFETY_ESTABLISHED.
    - PASS from this validator is not approval.
    """
    if not verified_adapter_context:
        return {"check": "workspace_lock_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "MISSING_VERIFIED_ADAPTER_CONTEXT", "expected": "ABSENT", "actual": None}

    if not lookup_result:
        return {"check": "workspace_lock_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "MISSING_LOOKUP_RESULT", "expected": "ABSENT", "actual": None}

    for req in ["lookup_status", "source_type", "adapter_capabilities"]:
        if req not in lookup_result:
            return {"check": "workspace_lock_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "MISSING_LOOKUP_FIELDS", "expected": "ABSENT", "actual": None}
            
    if lookup_result.get("adapter_id") != verified_adapter_context.get("adapter_id"):
        return {"check": "workspace_lock_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "ADAPTER_ID_MISMATCH", "expected": "ABSENT", "actual": None}

    status = lookup_result["lookup_status"]
    if status in ("NOT_RUN", "UNKNOWN"):
        return {"check": "workspace_lock_lookup", "status": "UNKNOWN_BLOCKED", "error_code": f"LOOKUP_STATUS_{status}", "expected": "ABSENT", "actual": status}

    if status == "FOUND" and "record" not in lookup_result:
        return {"check": "workspace_lock_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "FOUND_BUT_MISSING_RECORD", "expected": "ABSENT", "actual": status}

    if status == "FOUND":
        record = lookup_result["record"]
        rec_val = validate_workspace_lock_record(record, expected_workspace_id, expected_session_id, expected_package_id, expected_package_digest, expected_authorization_id)
        if rec_val["status"] != "PASS":
            return {"check": "workspace_lock_lookup", "status": rec_val["status"], "error_code": rec_val["error_code"], "expected": "ABSENT", "actual": record.get("lock_state")}
            
        ls_value = record.get("lock_state")
        try:
            ls = WorkspaceLockState(ls_value)
        except ValueError:
            return {"check": "workspace_lock_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "INVALID_LOCK_STATE", "expected": "ABSENT", "actual": ls_value}
    elif status == "NOT_FOUND":
        if not verified_adapter_context.get("authority_verified", False):
            return {"check": "workspace_lock_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "UNVERIFIED_AUTHORITY_CLAIM", "expected": "ABSENT", "actual": status}
        if not verified_adapter_context.get("durable", False):
            return {"check": "workspace_lock_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "NON_AUTHORITATIVE_ABSENCE", "expected": "ABSENT", "actual": status}
        ls = WorkspaceLockState.ABSENT
    else:
        ls = WorkspaceLockState.UNKNOWN
        
    if ls == WorkspaceLockState.ABSENT or ls == WorkspaceLockState.PRESENT_SELF:
        return {"check": "workspace_lock_lookup", "status": "PASS", "error_code": None, "expected": "ABSENT", "actual": ls.value}
    elif ls in (WorkspaceLockState.PRESENT_OTHER, WorkspaceLockState.STALE, WorkspaceLockState.CONFLICT):
        return {"check": "workspace_lock_lookup", "status": "BLOCKED", "error_code": f"UNSAFE_LOCK_STATE_{ls.value}", "expected": "ABSENT", "actual": ls.value}
    else:
        return {"check": "workspace_lock_lookup", "status": "UNKNOWN_BLOCKED", "error_code": f"INDETERMINATE_LOCK_STATE_{ls.value}", "expected": "ABSENT", "actual": ls.value}


class InMemoryTestWorkspaceLockAdapter:
    def __init__(self):
        self.store = {}
        self.capability_declaration = {
            "durable": False,
            "atomic_compare_and_set": False,
            "cross_process_safe": False,
            "production_ready": False,
            "authoritative": False,
            "atomic_acquire": False
        }

    def lookup_lock(self, workspace_instance_id: str) -> Dict[str, Any]:
        if workspace_instance_id in self.store:
            return {
                "lookup_status": "FOUND",
                "record": self.store[workspace_instance_id],
                "source_type": WorkspaceLockSourceType.EXPLICIT_VALIDATION_INPUT.value,
                "adapter_capabilities": self.capability_declaration
            }
        return {
            "lookup_status": "NOT_FOUND",
            "source_type": WorkspaceLockSourceType.EXPLICIT_VALIDATION_INPUT.value,
            "adapter_capabilities": self.capability_declaration
        }

    def set_test_lock_record(self, workspace_instance_id: str, record: Dict[str, Any]):
        self.store[workspace_instance_id] = record
