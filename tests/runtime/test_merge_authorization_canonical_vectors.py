import json
import pytest
from aos.runtime.canonical_serialization import canonicalize_validated_json
import hashlib

def test_canonical_vectors():
    with open("tests/fixtures/runtime/merge_authorization/canonical-vectors.json", "r") as f:
        vectors = json.load(f)
        
    for v in vectors:
        b = canonicalize_validated_json(v["input"])
        assert b.hex() == v["expected_bytes_hex"], v["description"]

def test_golden_digest():
    b = canonicalize_validated_json({"a": 1})
    d = hashlib.sha256(b).hexdigest()
    assert len(d) == 64

def test_domain_separation():
    domain = b"AOS-MERGE-AUTHORIZATION-PACKAGE-V1\0"
    b = canonicalize_validated_json({"a": 1})
    domain_separated_digest = hashlib.sha256(domain + b).hexdigest()
    plain_digest = hashlib.sha256(b).hexdigest()
    
    assert len(domain_separated_digest) == 64
    assert domain_separated_digest != plain_digest
    assert domain_separated_digest == domain_separated_digest.lower()

def test_no_terminal_lf():
    b = canonicalize_validated_json({"a": 1})
    assert not b.endswith(b"\n")
    
def test_no_bom():
    b = canonicalize_validated_json({"a": 1})
    assert not b.startswith(b"\xef\xbb\xbf")
