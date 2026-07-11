import copy
import hashlib
import hmac
from .strict_json import AOSRuntimeError
from .canonical_serialization import canonicalize_validated_json
from .execution_package import validate_execution_package_schema

def build_digest_payload(validated_package: dict) -> dict:
    """
    Creates a digest projection of the package.
    Fully excludes package_digest and package_signature.
    Returns an independent deep copy of the projected structure.
    """
    if not isinstance(validated_package, dict):
        raise AOSRuntimeError("ERROR", "INVALID_PACKAGE_TYPE", "Package must be an object", "digest")
        
    projection = copy.deepcopy(validated_package)
    
    if "package_digest" in projection:
        del projection["package_digest"]
        
    if "package_signature" in projection:
        del projection["package_signature"]
        
    return projection

def compute_package_digest(validated_package: dict) -> str:
    """
    Computes the SHA-256 digest of the projected package payload using RFC 8785 canonicalization.
    """
    # 1. Project
    projection = build_digest_payload(validated_package)
    
    # 2. Canonicalize
    # This automatically verifies the domain boundary and produces UTF-8 canonical bytes.
    try:
        canonical_bytes = canonicalize_validated_json(projection)
    except AOSRuntimeError as e:
        raise AOSRuntimeError("ERROR", "DIGEST_PAYLOAD_CANONICALIZATION_FAILED", str(e), "digest", e.path)
        
    # 3. Digest
    hasher = hashlib.sha256()
    hasher.update(canonical_bytes)
    return hasher.hexdigest()

def verify_package_digest(validated_package: dict) -> dict:
    """
    Verifies the package_digest of a package.
    """
    if "package_digest" not in validated_package:
        return {
            "status": "UNKNOWN_BLOCKED",
            "error_code": "PACKAGE_DIGEST_MISSING",
            "expected_digest": None,
            "actual_digest": None,
            "algorithm": None,
            "message": "package_digest is missing"
        }
        
    expected_digest = validated_package["package_digest"]
    
    # Validate representation
    if not isinstance(expected_digest, str):
        return {
            "status": "BLOCKED",
            "error_code": "INVALID_DIGEST_FORMAT",
            "expected_digest": None,
            "actual_digest": None,
            "algorithm": None,
            "message": "package_digest must be string"
        }
        
    if len(expected_digest) != 64 or not expected_digest.islower() or not all(c in '0123456789abcdef' for c in expected_digest):
        return {
            "status": "BLOCKED",
            "error_code": "INVALID_DIGEST_FORMAT",
            "expected_digest": expected_digest,
            "actual_digest": None,
            "algorithm": None,
            "message": "package_digest must be 64 lowercase hexadecimal characters"
        }
        
    algorithm = validated_package.get("package_digest_algorithm", "sha256")
    if algorithm != "sha256":
        return {
            "status": "UNKNOWN_BLOCKED",
            "error_code": "UNSUPPORTED_DIGEST_ALGORITHM",
            "expected_digest": expected_digest,
            "actual_digest": None,
            "algorithm": algorithm,
            "message": f"Unsupported digest algorithm: {algorithm}"
        }
        
    try:
        actual_digest = compute_package_digest(validated_package)
    except AOSRuntimeError as e:
        return {
            "status": "BLOCKED",
            "error_code": e.error_code,
            "expected_digest": expected_digest,
            "actual_digest": None,
            "algorithm": "sha256",
            "message": e.message
        }
        
    if hmac.compare_digest(expected_digest, actual_digest):
        return {
            "status": "PASS",
            "error_code": None,
            "expected_digest": expected_digest,
            "actual_digest": actual_digest,
            "algorithm": "sha256",
            "message": "Digest matches"
        }
    else:
        return {
            "status": "BLOCKED",
            "error_code": "DIGEST_MISMATCH",
            "expected_digest": expected_digest,
            "actual_digest": actual_digest,
            "algorithm": "sha256",
            "message": "Digest verification failed"
        }
