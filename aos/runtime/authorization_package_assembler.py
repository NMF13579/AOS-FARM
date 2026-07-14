import copy
import re
from typing import Dict, Any

MINIMUM_PROHIBITIONS = {
    "admin_bypass",
    "force_push",
    "branch_deletion",
    "release",
    "different_repository",
    "different_pull_request",
    "different_base_oid",
    "different_head_oid",
    "different_commit_set",
    "method_substitution"
}

REQUIRED_INPUTS = {
    "normalized_intent",
    "repository_identity",
    "pull_request_identity",
    "decision_state",
    "merge_readiness_result",
    "exact_merge_parameters",
    "fixed_safety_policy",
    "tool_identity"
}

FORBIDDEN_OUTPUT_FIELDS = {
    "package_id",
    "package_digest",
    "artifact_manifest",
    "verification_result",
    "human_preview",
    "timestamp",
    "local_path",
    "temporary_directory",
    "collection_evidence",
    "raw_error",
    "approval",
    "execution_authorization"
}

def _check_strict_types(obj: Any):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                raise ValueError("Keys must be strings")
            _check_strict_types(v)
    elif isinstance(obj, list):
        for item in obj:
            _check_strict_types(item)
    elif type(obj) is bool:
        pass
    elif type(obj) is int:
        pass
    elif isinstance(obj, str):
        pass
    elif obj is None:
        pass
    else:
        raise ValueError(f"Type {type(obj)} not allowed")

def assemble_package_core(inputs: Dict[str, Any]) -> Dict[str, Any]:
    _check_strict_types(inputs)
    
    missing = REQUIRED_INPUTS - set(inputs.keys())
    if missing:
        raise ValueError(f"Missing required inputs: {missing}")
        
    unknown = set(inputs.keys()) - REQUIRED_INPUTS
    if unknown:
        raise ValueError(f"Unknown input fields: {unknown}")
        
    tool_identity = inputs["tool_identity"]
    for f in ["product_version", "generator_build_digest", "canonicalizer_version", "package_schema_version"]:
        if f not in tool_identity:
            raise ValueError(f"Missing tool_identity field: {f}")
            
    digest = tool_identity["generator_build_digest"]
    if not isinstance(digest, str) or not re.match(r"^sha256:[a-f0-9]{64}$", digest):
        raise ValueError("Invalid generator_build_digest format")
        
    safety_policy = inputs["fixed_safety_policy"]
    policy_prohibitions = set(safety_policy.get("forbidden_actions", []))
    
    if not MINIMUM_PROHIBITIONS.issubset(policy_prohibitions):
        raise ValueError("Minimum prohibitions cannot be removed")
        
    input_prohibitions = set(inputs.get("normalized_intent", {}).get("forbidden_actions", []))
    combined_prohibitions = set(policy_prohibitions) | input_prohibitions | set(MINIMUM_PROHIBITIONS)
    
    output = {
        "schema_version": 1,
        "operation": "MERGE_AUTHORIZATION",
        "repository_identity": copy.deepcopy(inputs["repository_identity"]),
        "pull_request": copy.deepcopy(inputs["pull_request_identity"]),
        "normalized_intent": copy.deepcopy(inputs["normalized_intent"]),
        "fixed_safety_policy": copy.deepcopy(inputs["fixed_safety_policy"]),
        "decision_state": copy.deepcopy(inputs["decision_state"]),
        "exact_merge_parameters": copy.deepcopy(inputs["exact_merge_parameters"]),
        "forbidden_actions": sorted(list(combined_prohibitions)),
        "tool_identity": copy.deepcopy(inputs["tool_identity"])
    }
    
    for f in FORBIDDEN_OUTPUT_FIELDS:
        if f in output:
            raise ValueError(f"Forbidden output field present: {f}")
            
    return output
