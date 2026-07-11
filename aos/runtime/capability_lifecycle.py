import re
from datetime import datetime, timezone
from typing import Dict, Any, List

class AOSLifecycleError(Exception):
    pass

class CapabilityState:
    ISSUED = "ISSUED"
    ACTIVATION_PENDING = "ACTIVATION_PENDING"
    ACTIVATED = "ACTIVATED"
    CONSUMED = "CONSUMED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    REJECTED = "REJECTED"
    COMPROMISED = "COMPROMISED"
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"
    UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"

TERMINAL_STATES = {
    CapabilityState.CONSUMED,
    CapabilityState.EXPIRED,
    CapabilityState.REVOKED,
    CapabilityState.REJECTED,
    CapabilityState.COMPROMISED
}

VALID_STATES = {
    CapabilityState.ISSUED,
    CapabilityState.ACTIVATION_PENDING,
    CapabilityState.ACTIVATED,
    CapabilityState.CONSUMED,
    CapabilityState.EXPIRED,
    CapabilityState.REVOKED,
    CapabilityState.REJECTED,
    CapabilityState.COMPROMISED,
    CapabilityState.RECOVERY_REQUIRED,
    CapabilityState.UNKNOWN_BLOCKED
}

ALLOWED_TRANSITIONS = {
    (CapabilityState.ISSUED, CapabilityState.ACTIVATION_PENDING),
    (CapabilityState.ACTIVATION_PENDING, CapabilityState.ACTIVATED),
    (CapabilityState.ACTIVATED, CapabilityState.CONSUMED),
    (CapabilityState.ISSUED, CapabilityState.EXPIRED),
    (CapabilityState.ISSUED, CapabilityState.REVOKED),
    (CapabilityState.ISSUED, CapabilityState.REJECTED),
    (CapabilityState.ACTIVATION_PENDING, CapabilityState.EXPIRED),
    (CapabilityState.ACTIVATION_PENDING, CapabilityState.REVOKED),
    (CapabilityState.ACTIVATION_PENDING, CapabilityState.REJECTED),
    (CapabilityState.ACTIVATED, CapabilityState.EXPIRED),
    (CapabilityState.ACTIVATED, CapabilityState.REVOKED),
    (CapabilityState.ACTIVATED, CapabilityState.COMPROMISED),
    (CapabilityState.ACTIVATED, CapabilityState.RECOVERY_REQUIRED)
}

RFC3339_STRICT_UTC_REGEX = re.compile(
    r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:Z|\+00:00)$"
)

def parse_rfc3339_utc(time_str: str) -> datetime:
    if not isinstance(time_str, str):
        raise AOSLifecycleError("INVALID_TIMESTAMP")
    if not RFC3339_STRICT_UTC_REGEX.match(time_str):
        raise AOSLifecycleError("INVALID_TIMESTAMP_FORMAT")
        
    normalized = time_str.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(normalized)
        return dt
    except ValueError:
        raise AOSLifecycleError("INVALID_TIMESTAMP")

def verify_expiration(validated_package: Dict[str, Any], validation_time_utc: str) -> Dict[str, Any]:
    if validation_time_utc is None:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_TIME", "message": "Unknown time source", "time_source": "UNKNOWN_TIME"}
        
    try:
        vt = parse_rfc3339_utc(validation_time_utc)
    except AOSLifecycleError as e:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_TIME", "message": str(e), "time_source": "UNKNOWN_TIME"}

    issued_at_str = validated_package.get("issued_at")
    not_before_str = validated_package.get("not_before")
    expires_at_str = validated_package.get("expires_at")
    
    if not issued_at_str or not expires_at_str:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_TIME_BOUNDS"}
        
    try:
        issued_at = parse_rfc3339_utc(issued_at_str)
        expires_at = parse_rfc3339_utc(expires_at_str)
        not_before = parse_rfc3339_utc(not_before_str) if not_before_str else None
        
        if not_before:
            if issued_at > not_before:
                return {"status": "BLOCKED", "error_code": "INVALID_TIME_RANGE"}
            if not_before >= expires_at:
                return {"status": "BLOCKED", "error_code": "INVALID_TIME_RANGE"}
        else:
            if issued_at >= expires_at:
                return {"status": "BLOCKED", "error_code": "INVALID_TIME_RANGE"}
                
        if not_before and vt < not_before:
            return {"status": "BLOCKED", "error_code": "NOT_YET_VALID", "time_source": "EXPLICIT_VALIDATION_TIME", "validation_time": validation_time_utc}
            
        if vt >= expires_at:
            return {"status": "BLOCKED", "error_code": "EXPIRED", "time_source": "EXPLICIT_VALIDATION_TIME", "validation_time": validation_time_utc}
            
        return {"status": "PASS", "error_code": None, "message": "TIME_VALID", "time_source": "EXPLICIT_VALIDATION_TIME", "validation_time": validation_time_utc}
        
    except AOSLifecycleError as e:
        return {"status": "BLOCKED", "error_code": "INVALID_TIMESTAMP", "message": str(e)}

def verify_revocation(revocation_record: Dict[str, Any]) -> Dict[str, Any]:
    if not revocation_record:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_REVOCATION"}
        
    reference = revocation_record.get("revocation_reference")
    status = revocation_record.get("revocation_status")
    source_type = revocation_record.get("source_type")
    checked_at = revocation_record.get("checked_at")
    
    if reference is None:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REVOCATION_REFERENCE"}
    if reference == "":
        return {"status": "BLOCKED", "error_code": "EMPTY_REVOCATION_REFERENCE"}
    
    if not source_type or source_type == "UNKNOWN_SOURCE":
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_REVOCATION_SOURCE"}
    if not status:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REVOCATION_STATUS"}
    if not checked_at:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_CHECKED_AT"}
        
    try:
        parse_rfc3339_utc(checked_at)
    except AOSLifecycleError:
        return {"status": "BLOCKED", "error_code": "INVALID_CHECKED_AT"}

    res = {"authoritative": False}

    if status == "NOT_REVOKED":
        res["status"] = "PASS"
        res["error_code"] = None
    elif status == "REVOKED":
        res["status"] = "BLOCKED"
        res["error_code"] = "REVOKED"
    elif status in ["UNKNOWN", "NOT_CHECKED"]:
        res["status"] = "UNKNOWN_BLOCKED"
        res["error_code"] = f"REVOCATION_{status}"
    else:
        res["status"] = "UNKNOWN_BLOCKED"
        res["error_code"] = "INVALID_REVOCATION_STATUS"
        
    return res

def validate_authorization_binding(package_authorization_id: str, expected_authorization_id: str) -> Dict[str, Any]:
    if not package_authorization_id:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_PACKAGE_AUTHORIZATION_ID", "expected": expected_authorization_id, "actual": package_authorization_id}
    if not expected_authorization_id:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_EXPECTED_AUTHORIZATION_ID", "expected": expected_authorization_id, "actual": package_authorization_id}
        
    if package_authorization_id == expected_authorization_id:
        return {"status": "PASS", "error_code": None, "expected": expected_authorization_id, "actual": package_authorization_id}
    else:
        return {"status": "BLOCKED", "error_code": "AUTHORIZATION_MISMATCH", "expected": expected_authorization_id, "actual": package_authorization_id}

def validate_activation_record(activation_record: Dict[str, Any], expected_package_id: str, expected_package_digest: str, expected_authorization_id: str) -> Dict[str, Any]:
    astat = activation_record.get("record_status")
    
    if astat == "ABSENT":
        return {"status": "PASS", "record_status": "ABSENT"}
    elif astat == "UNKNOWN":
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_ACTIVATION_STATE"}
    elif astat == "CONFLICT":
        return {"status": "BLOCKED", "error_code": "ACTIVATION_CONFLICT"}
    elif astat != "PRESENT":
        return {"status": "UNKNOWN_BLOCKED", "error_code": "INVALID_RECORD_STATUS"}
        
    required_fields = ["package_id", "package_digest", "authorization_id", "activation_id", "activated_at", "capability_state", "session_id", "record_status"]
    for f in required_fields:
        if f not in activation_record:
            return {"status": "UNKNOWN_BLOCKED", "error_code": f"MISSING_FIELD_{f}"}
            
    for k in activation_record.keys():
        if k not in required_fields:
            return {"status": "UNKNOWN_BLOCKED", "error_code": f"UNKNOWN_FIELD_{k}"}
            
    if activation_record["package_id"] != expected_package_id:
        return {"status": "BLOCKED", "error_code": "ACTIVATION_PACKAGE_MISMATCH"}
    if activation_record["package_digest"] != expected_package_digest:
        return {"status": "BLOCKED", "error_code": "ACTIVATION_DIGEST_MISMATCH"}
    if activation_record["authorization_id"] != expected_authorization_id:
        return {"status": "BLOCKED", "error_code": "ACTIVATION_AUTHORIZATION_MISMATCH"}
        
    if not activation_record["activation_id"]:
        return {"status": "BLOCKED", "error_code": "EMPTY_ACTIVATION_ID"}
    if not activation_record["session_id"] and activation_record["session_id"] is not None:
        # Assuming explicit nullable policy allows None or non-empty string
        return {"status": "BLOCKED", "error_code": "INVALID_SESSION_ID"}
        
    try:
        parse_rfc3339_utc(activation_record["activated_at"])
    except AOSLifecycleError:
        return {"status": "BLOCKED", "error_code": "INVALID_ACTIVATION_TIMESTAMP"}
        
    if activation_record["capability_state"] not in VALID_STATES:
        return {"status": "BLOCKED", "error_code": "INVALID_CAPABILITY_STATE"}
        
    return {"status": "PASS", "record_status": "PRESENT"}

def validate_consumption_record(consumption_record: Dict[str, Any], expected_package_id: str, expected_package_digest: str, expected_authorization_id: str) -> Dict[str, Any]:
    cstat = consumption_record.get("record_status")
    
    if cstat == "ABSENT":
        return {"status": "PASS", "record_status": "ABSENT"}
    elif cstat == "UNKNOWN":
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_CONSUMPTION_STATE"}
    elif cstat == "CONFLICT":
        return {"status": "BLOCKED", "error_code": "CONSUMPTION_CONFLICT"}
    elif cstat != "PRESENT":
        return {"status": "UNKNOWN_BLOCKED", "error_code": "INVALID_RECORD_STATUS"}
        
    required_fields = ["package_id", "package_digest", "authorization_id", "consumption_id", "consumed_at", "session_id", "record_status"]
    for f in required_fields:
        if f not in consumption_record:
            return {"status": "UNKNOWN_BLOCKED", "error_code": f"MISSING_FIELD_{f}"}
            
    for k in consumption_record.keys():
        if k not in required_fields:
            return {"status": "UNKNOWN_BLOCKED", "error_code": f"UNKNOWN_FIELD_{k}"}
            
    if consumption_record["package_id"] != expected_package_id:
        return {"status": "BLOCKED", "error_code": "CONSUMPTION_PACKAGE_MISMATCH"}
    if consumption_record["package_digest"] != expected_package_digest:
        return {"status": "BLOCKED", "error_code": "CONSUMPTION_DIGEST_MISMATCH"}
    if consumption_record["authorization_id"] != expected_authorization_id:
        return {"status": "BLOCKED", "error_code": "CONSUMPTION_AUTHORIZATION_MISMATCH"}
        
    if not consumption_record["consumption_id"]:
        return {"status": "BLOCKED", "error_code": "EMPTY_CONSUMPTION_ID"}
    if not consumption_record["session_id"] and consumption_record["session_id"] is not None:
        return {"status": "BLOCKED", "error_code": "INVALID_SESSION_ID"}
        
    try:
        parse_rfc3339_utc(consumption_record["consumed_at"])
    except AOSLifecycleError:
        return {"status": "BLOCKED", "error_code": "INVALID_CONSUMPTION_TIMESTAMP"}
        
    return {"status": "PASS", "record_status": "PRESENT"}

def validate_single_use(
    validated_package: Dict[str, Any],
    activation_record: Dict[str, Any],
    consumption_record: Dict[str, Any],
    package_digest: str
) -> Dict[str, Any]:
    is_single_use = validated_package.get("single_use")
    if not isinstance(is_single_use, bool):
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_SINGLE_USE_FLAG"}
        
    expected_pkg_id = validated_package.get("package_id")
    expected_auth_id = validated_package.get("authorization_id")

    if not activation_record:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_ACTIVATION_RECORD_STRUCT"}
    if not consumption_record:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "MISSING_CONSUMPTION_RECORD_STRUCT"}
        
    ares = validate_activation_record(activation_record, expected_pkg_id, package_digest, expected_auth_id)
    if ares["status"] != "PASS":
        return ares
        
    cres = validate_consumption_record(consumption_record, expected_pkg_id, package_digest, expected_auth_id)
    if cres["status"] != "PASS":
        return cres

    astat = ares["record_status"]
    cstat = cres["record_status"]

    if cstat == "PRESENT":
        return {"status": "BLOCKED", "error_code": "ALREADY_CONSUMED"}
        
    if is_single_use and astat == "PRESENT":
        return {"status": "BLOCKED", "error_code": "DUPLICATE_ACTIVATION_BLOCKED"}
        
    return {"status": "PASS", "error_code": None}

def _aggregate_results(results: List[Dict[str, Any]]) -> str:
    precedence = {"UNKNOWN_BLOCKED": 0, "BLOCKED": 1, "FAIL": 2, "PASS": 4}
    worst_status = "PASS"
    worst_score = 4
    
    for r in results:
        s = r.get("status", "UNKNOWN_BLOCKED")
        if s == "NOT_RUN":
            return "UNKNOWN_BLOCKED"
            
        score = precedence.get(s, 0)
        if score < worst_score:
            worst_score = score
            worst_status = s
    return worst_status

def validate_capability_transition(
    validated_package: Dict[str, Any],
    target_state: str,
    validation_time_utc: str,
    revocation_record: Dict[str, Any],
    activation_record: Dict[str, Any],
    consumption_record: Dict[str, Any],
    package_binding_result_status: str,
    authorization_binding_result_status: str,
    package_digest_status: str,
    actual_package_digest: str
) -> Dict[str, Any]:
    
    source_state = validated_package.get("lifecycle_state")
    
    if not source_state or source_state not in VALID_STATES or source_state == CapabilityState.UNKNOWN_BLOCKED:
        return {
            "status": "UNKNOWN_BLOCKED", "error_code": "INVALID_LIFECYCLE_STATE",
            "source_state": source_state, "target_state": target_state,
            "retry_allowed": False, "terminal": True, "message": "Unknown source state"
        }
        
    if source_state in TERMINAL_STATES:
        return {
            "status": "BLOCKED", "error_code": "TERMINAL_STATE",
            "source_state": source_state, "target_state": target_state,
            "retry_allowed": False, "terminal": True, "message": "Already terminal"
        }
        
    if (source_state, target_state) not in ALLOWED_TRANSITIONS:
        return {
            "status": "BLOCKED", "error_code": "INVALID_LIFECYCLE_TRANSITION",
            "source_state": source_state, "target_state": target_state,
            "retry_allowed": False, "terminal": target_state in TERMINAL_STATES,
            "message": "Transition not allowed"
        }
        
    checks = []
    
    exp_res = verify_expiration(validated_package, validation_time_utc)
    checks.append(exp_res)
    
    if target_state in [CapabilityState.ACTIVATION_PENDING, CapabilityState.ACTIVATED]:
        rev_res = verify_revocation(revocation_record)
        checks.append(rev_res)
        
    if target_state in [CapabilityState.ACTIVATED, CapabilityState.CONSUMED]:
        su_res = validate_single_use(validated_package, activation_record, consumption_record, actual_package_digest)
        checks.append(su_res)
        
        checks.append({"status": package_binding_result_status})
        checks.append({"status": authorization_binding_result_status})
        checks.append({"status": package_digest_status})
        
    aggregated = _aggregate_results(checks)
    
    if aggregated == "PASS":
        return {
            "status": "PASS", "error_code": None,
            "source_state": source_state, "target_state": target_state,
            "retry_allowed": False, "terminal": target_state in TERMINAL_STATES,
            "message": "Transition technically valid"
        }
    else:
        return {
            "status": aggregated, "error_code": "TRANSITION_PRECONDITIONS_FAILED",
            "source_state": source_state, "target_state": target_state,
            "retry_allowed": False, 
            "terminal": False,
            "message": "Preconditions failed"
        }

def validate_capability_for_resume(
    validated_package: Dict[str, Any],
    validation_time_utc: str,
    revocation_record: Dict[str, Any],
    package_binding_result_status: str
) -> Dict[str, Any]:
    source_state = validated_package.get("lifecycle_state")
    if not source_state or source_state not in VALID_STATES or source_state == CapabilityState.UNKNOWN_BLOCKED:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "UNKNOWN_STATE"}
    if source_state in TERMINAL_STATES:
        return {"status": "BLOCKED", "error_code": "TERMINAL_STATE"}
        
    exp_res = verify_expiration(validated_package, validation_time_utc)
    if exp_res["status"] != "PASS":
        return exp_res
        
    rev_res = verify_revocation(revocation_record)
    if rev_res["status"] != "PASS":
        return rev_res
        
    if package_binding_result_status != "PASS":
        if package_binding_result_status == "NOT_RUN":
            return {"status": "UNKNOWN_BLOCKED", "error_code": "BINDING_FAILED"}
        return {"status": package_binding_result_status, "error_code": "BINDING_FAILED"}
        
    return {"status": "PASS"}

class AtomicStateStoreProtocol:
    durable = False
    atomic_compare_and_set = False
    cross_process_safe = False
    production_ready = False
    
    def lookup_activation(self, package_id: str) -> str:
        raise NotImplementedError
    def lookup_consumption(self, package_id: str) -> str:
        raise NotImplementedError
    def compare_and_set_activation(self, package_id: str, new_record: dict) -> bool:
        raise NotImplementedError
    def compare_and_set_consumption(self, package_id: str, new_record: dict) -> bool:
        raise NotImplementedError

class InMemoryTestStateStore(AtomicStateStoreProtocol):
    durable = False
    atomic_compare_and_set = False
    cross_process_safe = False
    production_ready = False
    
    def __init__(self):
        self.activations = {}
        self.consumptions = {}
        
    def lookup_activation(self, package_id: str) -> str:
        return "PRESENT" if package_id in self.activations else "ABSENT"
        
    def lookup_consumption(self, package_id: str) -> str:
        return "PRESENT" if package_id in self.consumptions else "ABSENT"
        
    def compare_and_set_activation(self, package_id: str, new_record: dict) -> bool:
        if package_id in self.activations:
            return False
        self.activations[package_id] = new_record
        return True
        
    def compare_and_set_consumption(self, package_id: str, new_record: dict) -> bool:
        if package_id in self.consumptions:
            return False
        self.consumptions[package_id] = new_record
        return True
