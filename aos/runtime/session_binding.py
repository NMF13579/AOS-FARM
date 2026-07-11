from enum import Enum
from typing import Dict, Any, List, Optional
import re
from datetime import datetime, timezone
from .strict_json import AOSRuntimeError
from .package_digest import build_digest_payload, verify_package_digest
from .package_binding import bind_repository, bind_platform
from .capability_lifecycle import CapabilityState

class SessionState(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUSPENDED = "SUSPENDED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ABORTED = "ABORTED"
    UNKNOWN = "UNKNOWN"

class SessionIdentitySource(Enum):
    EXPLICIT_VALIDATION_INPUT = "EXPLICIT_VALIDATION_INPUT"
    VERIFIED_EXTERNAL_SOURCE = "VERIFIED_EXTERNAL_SOURCE"
    UNKNOWN_SOURCE = "UNKNOWN_SOURCE"

def validate_session_id(session_id: str) -> Dict[str, Any]:
    if not session_id:
         return {"status": "BLOCKED", "error_code": "MISSING_SESSION_ID"}
    if len(session_id) < 8 or len(session_id) > 256:
         return {"status": "BLOCKED", "error_code": "INVALID_SESSION_ID_LENGTH"}
    if not re.match(r'^[a-zA-Z0-9_-]+$', session_id):
         return {"status": "BLOCKED", "error_code": "INVALID_SESSION_ID_CHARACTERS"}
    return {"status": "PASS", "error_code": None}

def validate_session_schema(session_record: Dict[str, Any]) -> Dict[str, Any]:
    allowed_fields = {
        "schema_version", "session_id", "session_state", "session_revision",
        "created_at", "updated_at", "package_id", "package_digest",
        "authorization_id", "baseline_head", "nonce", "workspace_instance_id",
        "resume_allowed", "session_identity_source", "parent_session_id"
    }
    
    if set(session_record.keys()) - allowed_fields:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_FIELD_IN_SESSION_RECORD"}
        
    for req in ["schema_version", "session_id", "session_state", "session_revision", "created_at", "updated_at", "package_id", "package_digest", "authorization_id", "baseline_head", "nonce", "workspace_instance_id", "resume_allowed", "session_identity_source"]:
        if req not in session_record:
            return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REQUIRED_FIELD"}
            
    if session_record["schema_version"] != 1:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNSUPPORTED_SCHEMA_VERSION"}
        
    if not isinstance(session_record["session_revision"], int) or session_record["session_revision"] < 1:
        return {"status": "BLOCKED", "error_code": "INVALID_SESSION_REVISION"}
        
    if not isinstance(session_record["resume_allowed"], bool):
         return {"status": "UNKNOWN_BLOCKED", "error_code": "INVALID_RESUME_ALLOWED_TYPE"}
         
    if validate_session_id(session_record["session_id"])["status"] != "PASS":
        return {"status": "BLOCKED", "error_code": "INVALID_SESSION_ID_FORMAT"}
        
    if not isinstance(session_record["package_digest"], str) or len(session_record["package_digest"]) != 64 or not session_record["package_digest"].islower() or not all(c in '0123456789abcdef' for c in session_record["package_digest"]):
        return {"status": "BLOCKED", "error_code": "INVALID_PACKAGE_DIGEST_FORMAT"}

    from .replay_state import validate_nonce
    if validate_nonce(session_record["nonce"])["status"] != "PASS":
        return {"status": "BLOCKED", "error_code": "INVALID_NONCE_FORMAT"}
        
    if not re.match(r'^[0-9a-f]{40}$', session_record["baseline_head"]):
        return {"status": "BLOCKED", "error_code": "INVALID_BASELINE_HEAD_FORMAT"}

    from .workspace_binding import validate_workspace_instance_id
    if validate_workspace_instance_id(session_record["workspace_instance_id"])["status"] != "PASS":
        return {"status": "BLOCKED", "error_code": "INVALID_WORKSPACE_INSTANCE_ID_FORMAT"}

    try:
        dt_c = datetime.strptime(session_record["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        dt_u = datetime.strptime(session_record["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
        if dt_u < dt_c:
             return {"status": "BLOCKED", "error_code": "UPDATED_BEFORE_CREATED"}
    except ValueError:
        return {"status": "BLOCKED", "error_code": "INVALID_TIMESTAMP_FORMAT"}
        
    if session_record["session_identity_source"] not in [e.value for e in SessionIdentitySource]:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_SESSION_IDENTITY_SOURCE"}
        
    if session_record["session_identity_source"] == SessionIdentitySource.VERIFIED_EXTERNAL_SOURCE.value:
        # Fails closed because there is no verified adapter explicitly linked in the schema parameters right now.
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNVERIFIED_SESSION_IDENTITY_SOURCE"}
        
    state = session_record["session_state"]
    try:
        ss = SessionState(state)
    except ValueError:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "INVALID_SESSION_STATE"}
        
    if "parent_session_id" in session_record:
        if session_record["parent_session_id"] is None:
             # Allowed, distinct from missing
             pass
        elif validate_session_id(session_record["parent_session_id"])["status"] != "PASS":
             return {"status": "BLOCKED", "error_code": "INVALID_PARENT_SESSION_ID"}

    return {"status": "PASS", "error_code": None}

def validate_session_transition(current_state: SessionState, next_state: SessionState) -> Dict[str, Any]:
    transitions = {
        SessionState.PENDING: {SessionState.RUNNING, SessionState.ABORTED},
        SessionState.RUNNING: {SessionState.COMPLETED, SessionState.FAILED, SessionState.SUSPENDED, SessionState.ABORTED},
        SessionState.SUSPENDED: {SessionState.RUNNING, SessionState.ABORTED},
        SessionState.COMPLETED: set(),
        SessionState.FAILED: set(),
        SessionState.ABORTED: set(),
        SessionState.UNKNOWN: set()
    }
    
    if next_state in transitions.get(current_state, set()):
        return {"status": "PASS", "error_code": None}
    return {"status": "BLOCKED", "error_code": "INVALID_STATE_TRANSITION"}

def validate_session_time_contract(current_timestamp: str, updated_at: str) -> Dict[str, Any]:
    try:
        dt_c = datetime.strptime(current_timestamp, "%Y-%m-%dT%H:%M:%SZ")
        dt_u = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
        if dt_c < dt_u:
             return {"status": "BLOCKED", "error_code": "TIME_TRAVEL_DETECTED"}
    except ValueError:
        return {"status": "BLOCKED", "error_code": "INVALID_TIMESTAMP_FORMAT"}
    return {"status": "PASS", "error_code": None}

def _validate_structured_result(result: Dict[str, Any], expected_check: str) -> Dict[str, Any]:
    if not result:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_STRUCTURED_RESULT"}
    for req in ["check", "status", "error_code", "expected", "actual"]:
        if req not in result:
             return {"status": "UNKNOWN_BLOCKED", "error_code": "MALFORMED_STRUCTURED_RESULT"}
    if result["check"] != expected_check:
        return {"status": "UNKNOWN_BLOCKED", "error_code": f"WRONG_CHECK_IDENTITY_EXPECTED_{expected_check}"}
    return {"status": "PASS", "error_code": None}

def normalize_digest_verification_result(digest_result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "check": "package_digest",
        "status": digest_result.get("status", "UNKNOWN_BLOCKED"),
        "error_code": digest_result.get("error_code", "MISSING_ERROR_CODE"),
        "algorithm": digest_result.get("algorithm", "UNKNOWN_ALGORITHM"),
        "expected_digest": digest_result.get("expected_digest"),
        "actual_digest": digest_result.get("actual_digest")
    }

def validate_session_package_binding(session_record: dict, package_id: str, package_digest: str, digest_verification_result: Dict[str, Any]) -> Dict[str, Any]:
    if not digest_verification_result:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_DIGEST_VERIFICATION_PROVENANCE"}
        
    for req in ["check", "status", "error_code", "algorithm", "expected_digest", "actual_digest"]:
        if req not in digest_verification_result:
             return {"status": "UNKNOWN_BLOCKED", "error_code": "MALFORMED_DIGEST_VERIFICATION_PROVENANCE"}
             
    if digest_verification_result["check"] != "package_digest":
        return {"status": "UNKNOWN_BLOCKED", "error_code": "WRONG_CHECK_IDENTITY_EXPECTED_package_digest"}
        
    if digest_verification_result["algorithm"] != "sha256":
        return {"status": "BLOCKED", "error_code": "UNSUPPORTED_DIGEST_ALGORITHM"}
        
    if digest_verification_result.get("expected_digest") == "PASS" or digest_verification_result.get("actual_digest") == "PASS":
        return {"status": "BLOCKED", "error_code": "FABRICATED_DIGEST_PROVENANCE"}
        
    if digest_verification_result["status"] != "PASS":
         return {"status": "BLOCKED", "error_code": "DIGEST_VERIFICATION_FAILED"}
         
    exp_dig = digest_verification_result["expected_digest"]
    act_dig = digest_verification_result["actual_digest"]
    
    if not isinstance(exp_dig, str) or len(exp_dig) != 64 or not exp_dig.islower() or not all(c in '0123456789abcdef' for c in exp_dig):
        return {"status": "BLOCKED", "error_code": "INVALID_EXPECTED_DIGEST_FORMAT"}
        
    if not isinstance(act_dig, str) or len(act_dig) != 64 or not act_dig.islower() or not all(c in '0123456789abcdef' for c in act_dig):
        return {"status": "BLOCKED", "error_code": "INVALID_ACTUAL_DIGEST_FORMAT"}
         
    if exp_dig != session_record["package_digest"]:
         return {"status": "BLOCKED", "error_code": "SESSION_EXPECTED_DIGEST_MISMATCH"}
         
    if exp_dig != package_digest:
         return {"status": "BLOCKED", "error_code": "PACKAGE_EXPECTED_DIGEST_MISMATCH"}
         
    if act_dig != exp_dig:
         return {"status": "BLOCKED", "error_code": "EXPECTED_ACTUAL_DIGEST_MISMATCH"}
         
    if session_record["package_id"] != package_id:
         return {"status": "BLOCKED", "error_code": "PACKAGE_ID_MISMATCH"}
         
    return {"status": "PASS", "error_code": None}

def validate_session_authorization_binding(session_record: dict, package_authorization_id: str, authorization_verification_result: Dict[str, Any]) -> Dict[str, Any]:
    if _validate_structured_result(authorization_verification_result, "authorization_binding")["status"] != "PASS":
         return {"status": "UNKNOWN_BLOCKED", "error_code": "INVALID_AUTHORIZATION_VERIFICATION_PROVENANCE"}
         
    if authorization_verification_result["status"] != "PASS":
         return {"status": "BLOCKED", "error_code": "AUTHORIZATION_VERIFICATION_FAILED"}
         
    if session_record["authorization_id"] != package_authorization_id:
         return {"status": "BLOCKED", "error_code": "AUTHORIZATION_ID_MISMATCH"}
         
    return {"status": "PASS", "error_code": None}

def validate_session_platform_binding(platform_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    required_checks = {"platform_profile", "execution_environment", "execution_mode"}
    found_checks = set()
    
    for res in platform_results:
         if _validate_structured_result(res, res["check"])["status"] != "PASS":
             return {"status": "UNKNOWN_BLOCKED", "error_code": "INVALID_PLATFORM_PROVENANCE"}
         if res["check"] in found_checks:
             return {"status": "UNKNOWN_BLOCKED", "error_code": "DUPLICATE_PLATFORM_CHECK"}
         if res["check"] in required_checks:
             found_checks.add(res["check"])
             if res["status"] != "PASS":
                 return {"status": "BLOCKED", "error_code": f"PLATFORM_CHECK_FAILED_{res['check']}"}
                 
    if required_checks - found_checks:
         return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REQUIRED_PLATFORM_CHECK"}
         
    return {"status": "PASS", "error_code": None}

def validate_session_repository_binding(session_record: dict, repo_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    required_checks = {"repository_identity", "repository_remote", "repository_branch", "baseline_head", "repository_state", "repository_root", "detached_head_policy"}
    found_checks = set()
    
    for res in repo_results:
         if _validate_structured_result(res, res["check"])["status"] != "PASS":
             return {"status": "UNKNOWN_BLOCKED", "error_code": "INVALID_REPOSITORY_PROVENANCE"}
         if res["check"] in found_checks:
             return {"status": "UNKNOWN_BLOCKED", "error_code": "DUPLICATE_REPOSITORY_CHECK"}
             
         if res["check"] in required_checks:
             found_checks.add(res["check"])
             if res["status"] != "PASS":
                 return {"status": "BLOCKED", "error_code": f"REPOSITORY_CHECK_FAILED_{res['check']}"}
             
             # Actual value checking against session record
             if res["check"] == "baseline_head" and res["actual"] != session_record["baseline_head"]:
                 return {"status": "BLOCKED", "error_code": "BASELINE_HEAD_MISMATCH"}

    if required_checks - found_checks:
         return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REQUIRED_REPOSITORY_CHECK"}

    return {"status": "PASS", "error_code": None}

def validate_parent_chain(current_session_id: str, parent_lookup_result: Optional[Dict[str, Any]], supplied_parent_chain: List[str], chain_complete: bool) -> Dict[str, Any]:
    if parent_lookup_result is None:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_PARENT_LOOKUP"}
        
    if _validate_structured_result(parent_lookup_result, "parent_session_lookup")["status"] != "PASS":
        return {"status": "UNKNOWN_BLOCKED", "error_code": "INVALID_PARENT_LOOKUP_PROVENANCE"}
        
    status = parent_lookup_result["status"]
    if status == "ABSENT":
        return {"status": "BLOCKED", "error_code": "PARENT_SESSION_NOT_FOUND"}
    elif status == "UNKNOWN":
        return {"status": "UNKNOWN_BLOCKED", "error_code": "PARENT_SESSION_UNKNOWN"}
    elif status == "CONFLICT":
        return {"status": "BLOCKED", "error_code": "PARENT_SESSION_CONFLICT"}
    elif status != "PASS":
         return {"status": "UNKNOWN_BLOCKED", "error_code": "INDETERMINATE_PARENT_STATUS"}
         
    if not parent_lookup_result.get("actual"):
         return {"status": "UNKNOWN_BLOCKED", "error_code": "PRESENT_BUT_MISSING_PARENT_OBJECT"}
         
    if current_session_id in supplied_parent_chain:
         return {"status": "BLOCKED", "error_code": "PARENT_CHAIN_CYCLE_DETECTED"}
         
    if len(supplied_parent_chain) != len(set(supplied_parent_chain)):
         return {"status": "BLOCKED", "error_code": "DUPLICATE_ANCESTOR_DETECTED"}
         
    if not chain_complete:
         return {"status": "UNKNOWN_BLOCKED", "error_code": "INCOMPLETE_PARENT_CHAIN"}
         
    if parent_lookup_result.get("compromised", False):
         return {"status": "BLOCKED", "error_code": "COMPROMISED_ANCESTOR_DETECTED"}
         
    return {"status": "PASS", "error_code": None}

def validate_resume_preconditions(
    session_record: Dict[str, Any],
    capability_result: Dict[str, Any],
    digest_result: Dict[str, Any],
    authorization_result: Dict[str, Any],
    repository_result: Dict[str, Any],
    platform_result: Dict[str, Any],
    replay_lookup: Dict[str, Any],
    workspace_lock_lookup: Dict[str, Any],
    parent_chain_result: Dict[str, Any]
) -> Dict[str, Any]:
    try:
        ss = SessionState(session_record.get("session_state"))
    except ValueError:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "INVALID_SESSION_STATE"}

    if ss != SessionState.SUSPENDED:
         return {"status": "BLOCKED", "error_code": "SESSION_NOT_SUSPENDED"}
         
    if session_record.get("resume_allowed") is not True:
         return {"status": "BLOCKED", "error_code": "RESUME_NOT_ALLOWED_IN_SESSION"}
         
    # Handle digest separately due to different provenance shape
    dig_norm = normalize_digest_verification_result(digest_result)
    if dig_norm["status"] != "PASS" or dig_norm["check"] != "package_digest":
        return {"status": "UNKNOWN_BLOCKED", "error_code": "INVALID_PROVENANCE_PACKAGE_DIGEST"}
        
    for r, name in [
        (capability_result, "capability_lifecycle"),
        (authorization_result, "authorization_binding"),
        (repository_result, "repository_binding"),
        (platform_result, "platform_binding"),
        (replay_lookup, "replay_lookup"),
        (workspace_lock_lookup, "workspace_lock_lookup"),
        (parent_chain_result, "parent_chain_validation")
    ]:
         if _validate_structured_result(r, name)["status"] != "PASS":
              return {"status": "UNKNOWN_BLOCKED", "error_code": f"INVALID_PROVENANCE_{name.upper()}"}
         if r["status"] != "PASS":
              return {"status": "BLOCKED", "error_code": f"PRECONDITION_FAILED_{name.upper()}"}
              
    # For replay lookup, PASS ensures UNSEEN state (based on replay evaluation)
    if replay_lookup["actual"] != "UNSEEN":
         return {"status": "BLOCKED", "error_code": "UNSAFE_REPLAY_STATE_FOR_RESUME"}
         
    # For lock lookup, PASS ensures ABSENT or PRESENT_SELF with exact match.
    if workspace_lock_lookup["actual"] not in ("ABSENT", "PRESENT_SELF"):
         return {"status": "BLOCKED", "error_code": "UNSAFE_WORKSPACE_LOCK_STATE_FOR_RESUME"}

    return {"status": "PASS", "error_code": None}

def aggregate_session_validation(
    schema_res: Dict[str, Any],
    transition_res: Dict[str, Any],
    time_res: Dict[str, Any],
    package_res: Dict[str, Any],
    auth_res: Dict[str, Any],
    repo_res: Dict[str, Any],
    platform_res: Dict[str, Any],
    parent_res: Dict[str, Any]
) -> Dict[str, Any]:
    for res, name in [
        (schema_res, "schema"), (transition_res, "transition"),
        (time_res, "time"), (package_res, "package"),
        (auth_res, "auth"), (repo_res, "repo"),
        (platform_res, "platform"), (parent_res, "parent")
    ]:
        if res["status"] != "PASS":
             return {"status": res["status"], "error_code": f"AGGREGATION_FAILED_{name.upper()}_{res.get('error_code', 'UNKNOWN')}"}
             
    return {"status": "PASS", "error_code": None}
