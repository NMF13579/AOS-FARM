from .strict_json import AOSRuntimeError

# Explicit schema definitions. True means required, False means optional. Nullable is False for all.
# format: field_name: (required, expected_type)
SCHEMA_FIELDS = {
    "schema_version": (True, int),
    "package_id": (True, str),
    "task_id": (True, str),
    "authorization_id": (True, str),
    "repository_id": (True, str),
    "remote_identity": (True, str),
    "branch": (True, str),
    "baseline_head": (True, str),
    "baseline_state_digest": (True, str),
    "platform_profile": (True, str),
    "execution_environment_id": (True, str),
    "execution_mode": (True, str),
    "risk_profile": (True, str),
    "lifecycle_state": (True, str),
    "execution_authorized": (True, bool),
    "allowed_operations": (True, list),
    "allowed_paths": (True, list),
    "read_only_paths": (True, list),
    "forbidden_paths": (True, list),
    "issued_at": (True, str),
    "nonce": (True, str),
    "issuer": (True, str),
    "issuer_authority": (True, str),
    "issuer_domain": (True, str),
    
    # Optional fields (nullable: False)
    "package_revision": (False, int),
    "authorization_witness_digest": (False, str),
    "policy_version": (False, int),
    "policy_digest": (False, str),
    "protected_path_registry_version": (False, int),
    "protected_path_registry_digest": (False, str),
    "not_before": (False, str),
    "expires_at": (False, str),
    "single_use": (False, bool),
    "maximum_sessions": (False, int),
    "resume_allowed": (False, bool),
    "package_digest_algorithm": (False, str),
    "package_digest": (False, str),
    "signature_algorithm": (False, str),
    "issuer_key_id": (False, str),
    "package_signature": (False, str),
    "verification_key_reference": (False, str),
    "revocation_reference": (False, str),
    "capability_state_reference": (False, str)
}

def validate_execution_package_schema(obj):
    if not isinstance(obj, dict):
        raise AOSRuntimeError("ERROR", "INVALID_FIELD_TYPE", "Package must be an object", "schema")
    
    if "schema_version" not in obj:
        raise AOSRuntimeError("ERROR", "SCHEMA_VERSION_MISSING", "schema_version is missing", "schema")
    
    if obj["schema_version"] != 1:
        raise AOSRuntimeError("ERROR", "SCHEMA_VERSION_UNSUPPORTED", f"Unsupported schema_version: {obj['schema_version']}", "schema")
    
    for field, (is_required, expected_type) in SCHEMA_FIELDS.items():
        if field in obj:
            v = obj[field]
            if v is None:
                raise AOSRuntimeError("ERROR", "INVALID_FIELD_TYPE", f"Field {field} cannot be null", "schema", path=field)
            if not isinstance(v, expected_type):
                # Note: bool is a subclass of int in python, so isinstance(True, int) is True, 
                # but isinstance(1, bool) is False. To be safe:
                if expected_type is int and isinstance(v, bool):
                    raise AOSRuntimeError("ERROR", "INVALID_FIELD_TYPE", f"Field {field} must be {expected_type.__name__}, got bool", "schema", path=field)
                if not isinstance(v, expected_type):
                    raise AOSRuntimeError("ERROR", "INVALID_FIELD_TYPE", f"Field {field} must be {expected_type.__name__}", "schema", path=field)
        else:
            if is_required:
                raise AOSRuntimeError("ERROR", "MISSING_REQUIRED_FIELD", f"Missing required field: {field}", "schema", path=field)
    
    for k in obj.keys():
        if k not in SCHEMA_FIELDS:
            raise AOSRuntimeError("ERROR", "UNKNOWN_FIELD", f"Unknown field: {k}", "schema", path=k)
            
    return True
