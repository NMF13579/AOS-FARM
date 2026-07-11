from enum import Enum
from typing import Dict, Any, Optional
import hashlib
import re
from .strict_json import AOSRuntimeError
from .canonical_serialization import canonicalize_validated_json
from datetime import datetime, timezone

class ReplayState(Enum):
    UNSEEN = "UNSEEN"
    RESERVED = "RESERVED"
    CONSUMED = "CONSUMED"
    REVOKED = "REVOKED"
    CONFLICT = "CONFLICT"
    UNKNOWN = "UNKNOWN"
    NOT_CHECKED = "NOT_CHECKED"

class ReplaySourceType(Enum):
    EXPLICIT_VALIDATION_INPUT = "EXPLICIT_VALIDATION_INPUT"
    DURABLE_ATOMIC_STORE = "DURABLE_ATOMIC_STORE"
    UNKNOWN_SOURCE = "UNKNOWN_SOURCE"

def validate_nonce(nonce: str) -> Dict[str, Any]:
    if not nonce:
        return {"status": "BLOCKED", "error_code": "MISSING_NONCE"}
    if len(nonce) < 8 or len(nonce) > 64:
        return {"status": "BLOCKED", "error_code": "INVALID_NONCE_LENGTH"}
    if not re.match(r'^[a-zA-Z0-9_-]+$', nonce):
        return {"status": "BLOCKED", "error_code": "INVALID_NONCE_CHARACTERS"}
    return {"status": "PASS", "error_code": None}

def generate_replay_key(package_id: str, package_digest: str, authorization_id: str, nonce: str, session_id: str) -> str:
    projection = {
        "schema_version": 1,
        "package_id": package_id,
        "package_digest": package_digest,
        "authorization_id": authorization_id,
        "nonce": nonce,
        "session_id": session_id
    }
    canonical_bytes = canonicalize_validated_json(projection)
    return hashlib.sha256(canonical_bytes).hexdigest()

def validate_replay_record(record: Dict[str, Any], expected_key: str, expected_package_id: str, expected_package_digest: str, expected_authorization_id: str, expected_nonce: str, expected_session_id: str) -> Dict[str, Any]:
    allowed_fields = {"replay_key", "package_id", "package_digest", "authorization_id", "nonce", "session_id", "record_state", "recorded_at", "source_type"}
    if set(record.keys()) - allowed_fields:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_FIELD_IN_REPLAY_RECORD"}
    
    for req in ["replay_key", "package_id", "package_digest", "authorization_id", "nonce", "session_id", "record_state", "recorded_at", "source_type"]:
        if req not in record:
            return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REQUIRED_FIELD"}
            
    if not isinstance(record["replay_key"], str) or len(record["replay_key"]) != 64 or not record["replay_key"].islower() or not all(c in '0123456789abcdef' for c in record["replay_key"]):
        return {"status": "BLOCKED", "error_code": "INVALID_REPLAY_KEY_FORMAT"}
        
    if not isinstance(record["package_digest"], str) or len(record["package_digest"]) != 64 or not record["package_digest"].islower() or not all(c in '0123456789abcdef' for c in record["package_digest"]):
        return {"status": "BLOCKED", "error_code": "INVALID_PACKAGE_DIGEST_FORMAT"}

    if validate_nonce(record["nonce"])["status"] != "PASS":
        return {"status": "BLOCKED", "error_code": "INVALID_NONCE_FORMAT"}
        
    if not isinstance(record["session_id"], str) or len(record["session_id"]) < 8 or len(record["session_id"]) > 256:
        return {"status": "BLOCKED", "error_code": "INVALID_SESSION_ID_FORMAT"}
        
    try:
        dt = datetime.strptime(record["recorded_at"], "%Y-%m-%dT%H:%M:%SZ")
        dt = dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return {"status": "BLOCKED", "error_code": "INVALID_RECORDED_AT_TIMESTAMP"}

    if record["replay_key"] != expected_key:
        return {"status": "BLOCKED", "error_code": "REPLAY_KEY_MISMATCH"}
    if record["package_id"] != expected_package_id:
        return {"status": "BLOCKED", "error_code": "PACKAGE_ID_MISMATCH"}
    if record["package_digest"] != expected_package_digest:
        return {"status": "BLOCKED", "error_code": "PACKAGE_DIGEST_MISMATCH"}
    if record["authorization_id"] != expected_authorization_id:
        return {"status": "BLOCKED", "error_code": "AUTHORIZATION_ID_MISMATCH"}
    if record["nonce"] != expected_nonce:
        return {"status": "BLOCKED", "error_code": "NONCE_MISMATCH"}
    if record["session_id"] != expected_session_id:
        return {"status": "BLOCKED", "error_code": "SESSION_ID_MISMATCH"}

    if record["source_type"] not in [e.value for e in ReplaySourceType]:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_SOURCE_TYPE"}

    if record["source_type"] == ReplaySourceType.DURABLE_ATOMIC_STORE.value:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "SELF_DECLARED_DURABLE_ATOMIC_STORE"}

    state = record.get("record_state")
    try:
        rs = ReplayState(state)
    except ValueError:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "INVALID_RECORD_STATE"}

    if rs == ReplayState.UNSEEN:
        return {"status": "PASS", "error_code": None}
    elif rs in (ReplayState.RESERVED, ReplayState.CONSUMED, ReplayState.REVOKED, ReplayState.CONFLICT):
        return {"status": "BLOCKED", "error_code": "UNSAFE_REPLAY_STATE"}
    else:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "INDETERMINATE_REPLAY_STATE"}

def evaluate_replay_lookup(lookup_result: Dict[str, Any], verified_adapter_context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Evaluates a replay lookup result against the verified adapter context.

    Trust precondition contract:
    - verified_adapter_context is a trusted precondition supplied by an external
      integration boundary. It must be provided separately from the lookup result.
    - This validator checks consistency and maps replay states.
    - This validator does NOT establish, authenticate, or independently prove
      adapter authority. The authority_verified field in verified_adapter_context
      is asserted by the external boundary, not proved by this function.
    - Claim ceiling: TRUST_PRECONDITION_ACCEPTED, ADAPTER_CONTEXT_CONSISTENCY_VALIDATED,
      LOOKUP_MAPPING_CONTRACT_VALIDATED, FAIL_CLOSED_ON_UNVERIFIED_CONTEXT.
    - Forbidden claims: ADAPTER_AUTHORITY_PROVEN, AUTHORITATIVE_REPLAY_ABSENCE_ESTABLISHED,
      REPLAY_PROTECTION_ENFORCED, NONCE_SINGLE_USE_ENFORCED, ATOMIC_NONCE_CONSUMPTION_ENFORCED.
    - PASS from this validator is not approval.
    - CONTRACT_DEFINED_WITH_EXTERNAL_TRUST_PRECONDITION applies to positive test contexts.
    """
    if not verified_adapter_context:
        return {"check": "replay_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "MISSING_VERIFIED_ADAPTER_CONTEXT", "expected": "UNSEEN", "actual": None}
        
    if not lookup_result:
        return {"check": "replay_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "MISSING_LOOKUP_RESULT", "expected": "UNSEEN", "actual": None}
        
    for req in ["lookup_status", "source_type", "store_capabilities"]:
        if req not in lookup_result:
            return {"check": "replay_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "MISSING_LOOKUP_FIELDS", "expected": "UNSEEN", "actual": None}
            
    status = lookup_result["lookup_status"]
    if status in ("NOT_RUN", "UNKNOWN"):
        return {"check": "replay_lookup", "status": "UNKNOWN_BLOCKED", "error_code": f"LOOKUP_STATUS_{status}", "expected": "UNSEEN", "actual": status}

    if status == "FOUND" and "record" not in lookup_result:
        return {"check": "replay_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "FOUND_BUT_MISSING_RECORD", "expected": "UNSEEN", "actual": status}

    if lookup_result.get("adapter_id") != verified_adapter_context.get("adapter_id"):
        return {"check": "replay_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "ADAPTER_ID_MISMATCH", "expected": "UNSEEN", "actual": None}

    if status == "FOUND":
        rs_value = lookup_result["record"].get("record_state")
        try:
            rs = ReplayState(rs_value)
        except ValueError:
            return {"check": "replay_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "INVALID_RECORD_STATE", "expected": "UNSEEN", "actual": rs_value}
    elif status == "NOT_FOUND":
        if not verified_adapter_context.get("authority_verified", False):
            return {"check": "replay_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "UNVERIFIED_AUTHORITY_CLAIM", "expected": "UNSEEN", "actual": status}
        if not verified_adapter_context.get("durable", False):
            return {"check": "replay_lookup", "status": "UNKNOWN_BLOCKED", "error_code": "NON_AUTHORITATIVE_ABSENCE", "expected": "UNSEEN", "actual": status}
        rs = ReplayState.UNSEEN
    else:
        rs = ReplayState.UNKNOWN
        
    if rs == ReplayState.UNSEEN:
        return {"check": "replay_lookup", "status": "PASS", "error_code": None, "expected": "UNSEEN", "actual": "UNSEEN"}
    elif rs in (ReplayState.RESERVED, ReplayState.CONSUMED, ReplayState.REVOKED, ReplayState.CONFLICT):
        return {"check": "replay_lookup", "status": "BLOCKED", "error_code": f"UNSAFE_REPLAY_STATE_{rs.value}", "expected": "UNSEEN", "actual": rs.value}
    else:
        return {"check": "replay_lookup", "status": "UNKNOWN_BLOCKED", "error_code": f"INDETERMINATE_REPLAY_STATE_{rs.value}", "expected": "UNSEEN", "actual": rs.value}

class InMemoryTestReplayStore:
    def __init__(self):
        self.store = {}
        self.capability_declaration = {
            "durable": False,
            "atomic_compare_and_set": False,
            "cross_process_safe": False,
            "production_ready": False,
            "authoritative": False
        }

    def lookup_replay_record(self, replay_key: str) -> Dict[str, Any]:
        if replay_key in self.store:
            return {
                "lookup_status": "FOUND",
                "record": self.store[replay_key],
                "source_type": ReplaySourceType.EXPLICIT_VALIDATION_INPUT.value,
                "store_capabilities": self.capability_declaration
            }
        return {
            "lookup_status": "NOT_FOUND",
            "source_type": ReplaySourceType.EXPLICIT_VALIDATION_INPUT.value,
            "store_capabilities": self.capability_declaration
        }

    def set_test_replay_record(self, replay_key: str, record: Dict[str, Any]):
        self.store[replay_key] = record
        
    def set_test_replay_state(self, replay_key: str, state: ReplayState):
        if replay_key in self.store:
            self.store[replay_key]["record_state"] = state.value
