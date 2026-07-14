import hashlib
import copy
from aos.runtime.canonical_serialization import canonicalize_validated_json

DOMAIN_BYTES = b"AOS-MERGE-AUTHORIZATION-PACKAGE-V1\0"

EXCLUDED_FIELDS = {
    "package_id",
    "timestamp",
    "local_path",
    "verification_result",
    "artifact_manifest",
    "collection_evidence",
    "package_generation_counter",
    "approval",
    "execution_authorization"
}

KNOWN_CORE_FIELDS = {
    "schema_version",
    "operation",
    "repository_identity",
    "pull_request",
    "normalized_intent",
    "fixed_safety_policy",
    "decision_state",
    "exact_merge_parameters",
    "forbidden_actions",
    "tool_identity"
}

def generate_package_identity(package_core: dict) -> dict:
    core_copy = copy.deepcopy(package_core)
    
    for field in EXCLUDED_FIELDS:
        core_copy.pop(field, None)
        
    for k in core_copy:
        if k not in KNOWN_CORE_FIELDS:
            raise ValueError(f"Unknown package core field: {k}")
            
    canonical_bytes = canonicalize_validated_json(core_copy)
    
    digest_input = DOMAIN_BYTES + canonical_bytes
    digest_hex = hashlib.sha256(digest_input).hexdigest()
    
    return {
        "package_id": f"sha256:{digest_hex}",
        "semantic_digest": digest_hex,
        "canonical_package_core_bytes": canonical_bytes
    }
