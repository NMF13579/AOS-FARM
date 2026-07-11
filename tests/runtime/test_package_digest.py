import pytest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from aos.runtime.strict_json import AOSRuntimeError
from aos.runtime.package_digest import build_digest_payload, compute_package_digest, verify_package_digest
from aos.runtime.canonical_serialization import canonicalize_validated_json

def test_independent_digest_vector():
    base_dir = os.path.join(os.path.dirname(__file__), '../fixtures/runtime/execution_package/digest')
    
    with open(os.path.join(base_dir, 'valid_unsigned_package.json'), 'r') as f:
        pkg = json.load(f)
        
    with open(os.path.join(base_dir, 'valid_unsigned_package.expected-payload.json'), 'r') as f:
        expected_payload = json.load(f)
        
    with open(os.path.join(base_dir, 'valid_unsigned_package.expected-canonical.json'), 'rb') as f:
        expected_canonical = f.read()
        
    with open(os.path.join(base_dir, 'valid_unsigned_package.expected.sha256'), 'r') as f:
        expected_sha256 = f.read().strip()
        
    # 1. Test Payload Projection matches exactly (using canonical serialization)
    payload = build_digest_payload(pkg)
    assert canonicalize_validated_json(payload) == canonicalize_validated_json(expected_payload)
    
    # 2. Test Canonical bytes matches explicitly derived vector
    assert canonicalize_validated_json(payload) == expected_canonical
    
    # 3. Test Digest
    assert compute_package_digest(pkg) == expected_sha256

def test_build_digest_payload():
    original = {
        "schema_version": 1,
        "package_digest": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
        "package_signature": "sig123",
        "nested": {"key": "value"}
    }
    projected = build_digest_payload(original)
    
    assert "package_digest" not in projected
    assert "package_signature" not in projected
    assert "nested" in projected
    
    assert "package_digest" in original
    assert "package_signature" in original
    
    projected["nested"]["key"] = "mutated"
    assert original["nested"]["key"] == "value"

def test_verify_package_digest():
    package = {"a": 1}
    expected_digest = compute_package_digest(package)
    package["package_digest"] = expected_digest
    
    res = verify_package_digest(package)
    assert res["status"] == "PASS"
    
    package_missing = {"a": 1}
    res_missing = verify_package_digest(package_missing)
    assert res_missing["status"] == "UNKNOWN_BLOCKED"
    assert res_missing["error_code"] == "PACKAGE_DIGEST_MISSING"
    
    package_mismatch = {"a": 2, "package_digest": expected_digest}
    res_mismatch = verify_package_digest(package_mismatch)
    assert res_mismatch["status"] == "BLOCKED"
    assert res_mismatch["error_code"] == "DIGEST_MISMATCH"

    package_invalid = {"a": 1, "package_digest": "abc"}
    res_invalid = verify_package_digest(package_invalid)
    assert res_invalid["status"] == "BLOCKED"
    assert res_invalid["error_code"] == "INVALID_DIGEST_FORMAT"

    package_algo = {"a": 1, "package_digest": expected_digest, "package_digest_algorithm": "sha512"}
    res_algo = verify_package_digest(package_algo)
    assert res_algo["status"] == "UNKNOWN_BLOCKED"
    assert res_algo["error_code"] == "UNSUPPORTED_DIGEST_ALGORITHM"
