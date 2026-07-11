import pytest
from aos.runtime.replay_state import (
    ReplayState, ReplaySourceType, validate_nonce, generate_replay_key,
    validate_replay_record, evaluate_replay_lookup, InMemoryTestReplayStore
)
from aos.runtime.canonical_serialization import canonicalize_validated_json
import hashlib

def test_validate_nonce_valid():
    res = validate_nonce("abc123XYZ!")
    assert res["status"] == "BLOCKED" # Because '!' is invalid
    res = validate_nonce("abc123XYZ-_")
    assert res["status"] == "PASS"

def test_validate_nonce_negative():
    assert validate_nonce(None)["error_code"] == "MISSING_NONCE"
    assert validate_nonce("")["error_code"] == "MISSING_NONCE"
    assert validate_nonce("short")["error_code"] == "INVALID_NONCE_LENGTH"
    assert validate_nonce("a " * 10)["error_code"] == "INVALID_NONCE_CHARACTERS"
    assert validate_nonce("a/b/c/d/e/f/g")["error_code"] == "INVALID_NONCE_CHARACTERS"

def test_generate_replay_key_fixed_vector():
    package_id = "pkg_fixed_01"
    package_digest = "a" * 64
    authorization_id = "auth_fixed_01"
    nonce = "fixed_nonce_123"
    session_id = "sess_fixed_01"
    
    # Expected canonical JSON
    expected_canonical = b'{"authorization_id":"auth_fixed_01","nonce":"fixed_nonce_123","package_digest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","package_id":"pkg_fixed_01","schema_version":1,"session_id":"sess_fixed_01"}'
    
    # Expected SHA-256 computed externally
    expected_digest = hashlib.sha256(expected_canonical).hexdigest()
    
    key = generate_replay_key(package_id, package_digest, authorization_id, nonce, session_id)
    assert key == expected_digest

def test_raw_concatenation_ambiguity():
    key1 = generate_replay_key("pkg_1", "digest_1", "auth_1", "nonce123", "sess_1")
    key2 = generate_replay_key("pkg", "_1digest_1", "auth_1", "nonce123", "sess_1")
    assert key1 != key2

def test_validate_replay_record_valid():
    record = {
        "replay_key": "a" * 64,
        "package_id": "pkg_1",
        "package_digest": "b" * 64,
        "authorization_id": "auth_1",
        "nonce": "n1_abcde",
        "session_id": "sess_1_valid",
        "record_state": ReplayState.UNSEEN.value,
        "recorded_at": "2026-07-10T12:00:00Z",
        "source_type": ReplaySourceType.EXPLICIT_VALIDATION_INPUT.value
    }
    res = validate_replay_record(record, "a" * 64, "pkg_1", "b" * 64, "auth_1", "n1_abcde", "sess_1_valid")
    assert res["status"] == "PASS"

def test_validate_replay_record_negative():
    record = {
        "replay_key": "a" * 64,
        "package_id": "pkg_1",
        "package_digest": "b" * 64,
        "authorization_id": "auth_1",
        "nonce": "n1_abcde",
        "session_id": "sess_1_valid",
        "record_state": ReplayState.UNSEEN.value,
        "recorded_at": "2026-07-10T12:00:00Z",
        "source_type": ReplaySourceType.EXPLICIT_VALIDATION_INPUT.value
    }
    
    # Unknown field
    bad = dict(record)
    bad["unknown"] = True
    assert validate_replay_record(bad, "a" * 64, "pkg_1", "b" * 64, "auth_1", "n1_abcde", "sess_1_valid")["error_code"] == "UNKNOWN_FIELD_IN_REPLAY_RECORD"
    
    # Bad timestamp
    bad = dict(record)
    bad["recorded_at"] = "2026-07-10T12:00:00+00:00"
    assert validate_replay_record(bad, "a" * 64, "pkg_1", "b" * 64, "auth_1", "n1_abcde", "sess_1_valid")["error_code"] == "INVALID_RECORDED_AT_TIMESTAMP"

    # Durable source
    bad = dict(record)
    bad["source_type"] = ReplaySourceType.DURABLE_ATOMIC_STORE.value
    assert validate_replay_record(bad, "a" * 64, "pkg_1", "b" * 64, "auth_1", "n1_abcde", "sess_1_valid")["error_code"] == "SELF_DECLARED_DURABLE_ATOMIC_STORE"

def test_validate_replay_record_states():
    record = {
        "replay_key": "a" * 64,
        "package_id": "pkg_1",
        "package_digest": "b" * 64,
        "authorization_id": "auth_1",
        "nonce": "n1_abcde",
        "session_id": "sess_1_valid",
        "recorded_at": "2026-07-10T12:00:00Z",
        "source_type": ReplaySourceType.EXPLICIT_VALIDATION_INPUT.value
    }
    for state in [ReplayState.RESERVED, ReplayState.CONSUMED, ReplayState.REVOKED, ReplayState.CONFLICT]:
        rec = dict(record)
        rec["record_state"] = state.value
        res = validate_replay_record(rec, "a" * 64, "pkg_1", "b" * 64, "auth_1", "n1_abcde", "sess_1_valid")
        assert res["status"] == "BLOCKED"
        assert res["error_code"] == "UNSAFE_REPLAY_STATE"

def test_evaluate_replay_lookup():
    valid_ctx = {
        "adapter_id": "test_adapter_01",
        "adapter_type": "EXPLICIT_VALIDATION_INPUT",
        "absence_semantics": "UNSEEN",
        "namespace_scope": "test",
        "authority_verified": True,
        "durable": True,
        "cross_process_safe": True
    }
    
    # Missing verified context
    assert evaluate_replay_lookup({"lookup_status": "FOUND"})["error_code"] == "MISSING_VERIFIED_ADAPTER_CONTEXT"
    
    # Missing lookup result
    assert evaluate_replay_lookup(None, valid_ctx)["error_code"] == "MISSING_LOOKUP_RESULT"
    
    # Missing lookup fields
    assert evaluate_replay_lookup({"lookup_status": "FOUND"}, valid_ctx)["error_code"] == "MISSING_LOOKUP_FIELDS"
    
    # NOT_RUN
    lookup = {
        "lookup_status": "NOT_RUN",
        "source_type": "EXPLICIT_VALIDATION_INPUT",
        "store_capabilities": {},
        "adapter_id": "test_adapter_01"
    }
    assert evaluate_replay_lookup(lookup, valid_ctx)["error_code"] == "LOOKUP_STATUS_NOT_RUN"

    # FOUND but missing record
    lookup = {
        "lookup_status": "FOUND",
        "source_type": "EXPLICIT_VALIDATION_INPUT",
        "store_capabilities": {},
        "adapter_id": "test_adapter_01"
    }
    assert evaluate_replay_lookup(lookup, valid_ctx)["error_code"] == "FOUND_BUT_MISSING_RECORD"

    # Found UNSEEN
    lookup["record"] = {"record_state": ReplayState.UNSEEN.value}
    assert evaluate_replay_lookup(lookup, valid_ctx)["status"] == "PASS"

    # Found CONSUMED
    lookup["record"] = {"record_state": ReplayState.CONSUMED.value}
    assert evaluate_replay_lookup(lookup, valid_ctx)["status"] == "BLOCKED"
    
    # Authority Spoofing Negative Tests
    # 1. Adapter ID mismatch
    lookup["adapter_id"] = "spoofed_adapter"
    assert evaluate_replay_lookup(lookup, valid_ctx)["error_code"] == "ADAPTER_ID_MISMATCH"
    
    # 2. Replay lookup NOT_FOUND with unverified authority claim
    lookup["lookup_status"] = "NOT_FOUND"
    lookup["adapter_id"] = "test_adapter_01"
    bad_ctx = dict(valid_ctx)
    bad_ctx["authority_verified"] = False
    assert evaluate_replay_lookup(lookup, bad_ctx)["error_code"] == "UNVERIFIED_AUTHORITY_CLAIM"
    
    # 3. Replay lookup NOT_FOUND with non-authoritative absence (durable=False)
    bad_ctx = dict(valid_ctx)
    bad_ctx["durable"] = False
    assert evaluate_replay_lookup(lookup, bad_ctx)["error_code"] == "NON_AUTHORITATIVE_ABSENCE"
    
    # 4. Valid NOT_FOUND
    assert evaluate_replay_lookup(lookup, valid_ctx)["status"] == "PASS"

def test_in_memory_store():
    store = InMemoryTestReplayStore()
    assert store.capability_declaration["durable"] is False
    assert store.capability_declaration["production_ready"] is False
    
    store.set_test_replay_record("key1", {"record_state": ReplayState.RESERVED.value})
    assert store.lookup_replay_record("key1")["record"]["record_state"] == ReplayState.RESERVED.value
    
    store.set_test_replay_state("key1", ReplayState.CONSUMED)
    assert store.lookup_replay_record("key1")["record"]["record_state"] == ReplayState.CONSUMED.value
