from typing import Dict, List, Any, Optional
import json

class ContractValidationError(Exception):
    pass

def _check_type(val, allowed_types, allow_none=False, field_name=""):
    if val is None:
        if not allow_none:
            raise ContractValidationError(f"Field {field_name} cannot be null.")
        return
    if bool in allowed_types:
        if isinstance(val, bool):
            return
    if int in allowed_types:
        if isinstance(val, int) and not isinstance(val, bool):
            return
    for t in allowed_types:
        if t not in (bool, int) and isinstance(val, t):
            return
    raise ContractValidationError(f"Field {field_name} has invalid type {type(val).__name__}.")

def _reject_forbidden_types(val, field_name=""):
    if isinstance(val, bool):
        return
    if isinstance(val, (float, bytes)):
        raise ContractValidationError(f"Field {field_name} cannot be float or bytes.")
    if hasattr(val, 'isoformat') and callable(getattr(val, 'isoformat')):
        raise ContractValidationError(f"Field {field_name} cannot be datetime.")
    if isinstance(val, dict):
        for k, v in val.items():
            if not isinstance(k, str):
                raise ContractValidationError(f"Dictionary keys must be strings at {field_name}")
            _reject_forbidden_types(v, f"{field_name}.{k}")
    elif isinstance(val, list):
        for i, v in enumerate(val):
            _reject_forbidden_types(v, f"{field_name}[{i}]")

class RepositoryIdentity:
    def __init__(self, owner: str, name: str):
        _check_type(owner, [str], field_name="owner")
        _check_type(name, [str], field_name="name")
        self.owner = owner
        self.name = name

    def to_dict(self):
        return {"owner": self.owner, "name": self.name}

class PullRequestIdentity:
    def __init__(self, number: int, expected_head_oid: Optional[str] = None):
        _check_type(number, [int], field_name="number")
        if isinstance(number, bool):
            raise ContractValidationError("Pull request number cannot be a boolean")
        if number <= 0:
            raise ContractValidationError("Pull request number must be positive")
        _check_type(expected_head_oid, [str], allow_none=True, field_name="expected_head_oid")
        self.number = number
        self.expected_head_oid = expected_head_oid

    def to_dict(self):
        d = {"number": self.number}
        if self.expected_head_oid is not None:
            d["expected_head_oid"] = self.expected_head_oid
        return d

class PolicyFieldStatus:
    def __init__(self, field_name: str, status: str):
        _check_type(field_name, [str], field_name="field_name")
        _check_type(status, [str], field_name="status")
        self.field_name = field_name
        self.status = status

    def to_dict(self):
        return {"field_name": self.field_name, "status": self.status}

class CollectionCompleteness:
    def __init__(self, is_complete: bool):
        _check_type(is_complete, [bool], field_name="is_complete")
        self.is_complete = is_complete

    def to_dict(self):
        return {"is_complete": self.is_complete}

class DecisionState:
    def __init__(self, technical_gate_passed: bool, reason: str):
        _check_type(technical_gate_passed, [bool], field_name="technical_gate_passed")
        _check_type(reason, [str], field_name="reason")
        self.technical_gate_passed = technical_gate_passed
        self.reason = reason

    def to_dict(self):
        return {"technical_gate_passed": self.technical_gate_passed, "reason": self.reason}

class PackageCore:
    def __init__(self, repository_identity: str, pull_request: int, normalized_intent: dict,
                 fixed_safety_policy: dict, decision_state: dict, exact_merge_parameters: dict,
                 forbidden_actions: list, tool_identity: str):
        self.schema_version = 1
        self.operation = "merge"
        
        _check_type(repository_identity, [str], field_name="repository_identity")
        _check_type(pull_request, [int], field_name="pull_request")
        _check_type(normalized_intent, [dict], field_name="normalized_intent")
        _check_type(fixed_safety_policy, [dict], field_name="fixed_safety_policy")
        _check_type(decision_state, [dict], field_name="decision_state")
        _check_type(exact_merge_parameters, [dict], field_name="exact_merge_parameters")
        _check_type(forbidden_actions, [list], field_name="forbidden_actions")
        _check_type(tool_identity, [str], field_name="tool_identity")

        self.repository_identity = repository_identity
        self.pull_request = pull_request
        self.normalized_intent = normalized_intent
        self.fixed_safety_policy = fixed_safety_policy
        self.decision_state = decision_state
        self.exact_merge_parameters = exact_merge_parameters
        self.forbidden_actions = forbidden_actions
        self.tool_identity = tool_identity
        
        self._validate_no_forbidden_types()

    def _validate_no_forbidden_types(self):
        _reject_forbidden_types(self.to_dict(), "PackageCore")

    def to_dict(self):
        return {
            "schema_version": self.schema_version,
            "operation": self.operation,
            "repository_identity": self.repository_identity,
            "pull_request": self.pull_request,
            "normalized_intent": self.normalized_intent,
            "fixed_safety_policy": self.fixed_safety_policy,
            "decision_state": self.decision_state,
            "exact_merge_parameters": self.exact_merge_parameters,
            "forbidden_actions": self.forbidden_actions,
            "tool_identity": self.tool_identity
        }

class ToolIdentity:
    def __init__(self, name: str, version: str):
        _check_type(name, [str], field_name="name")
        _check_type(version, [str], field_name="version")
        self.name = name
        self.version = version

    def to_dict(self):
        return {"name": self.name, "version": self.version}

class VerificationResult:
    def __init__(self, status: str, details: str):
        if status not in ["PASS", "FAIL", "UNKNOWN", "NOT_RUN"]:
            raise ContractValidationError(f"Invalid status {status}")
        _check_type(details, [str], field_name="details")
        self.status = status
        self.details = details

    def to_dict(self):
        return {"status": self.status, "details": self.details}

class ResultEnvelope:
    def __init__(self, technical_status: str, approval_granted: bool, execution_authorized: bool, data: dict, verification_result: dict):
        if technical_status not in ["PASS", "FAIL", "UNKNOWN", "NOT_RUN"]:
            raise ContractValidationError(f"Invalid technical status {technical_status}")
        _check_type(approval_granted, [bool], field_name="approval_granted")
        _check_type(execution_authorized, [bool], field_name="execution_authorized")
        _check_type(data, [dict], field_name="data")
        _check_type(verification_result, [dict], field_name="verification_result")
        
        if approval_granted is not False:
            raise ContractValidationError("approval_granted must be False")
            
        if execution_authorized is not False:
            raise ContractValidationError("execution_authorized must be False")
        
        self.technical_status = technical_status
        self.approval_granted = approval_granted
        self.execution_authorized = execution_authorized
        self.data = data
        self.verification_result = verification_result
        self._validate_no_forbidden_types()

    def _validate_no_forbidden_types(self):
        _reject_forbidden_types(self.to_dict(), "ResultEnvelope")

    def to_dict(self):
        return {
            "technical_status": self.technical_status,
            "approval_granted": self.approval_granted,
            "execution_authorized": self.execution_authorized,
            "data": self.data,
            "verification_result": self.verification_result
        }
