import pytest
from aos.runtime.session_binding import (
    SessionState, SessionIdentitySource, validate_session_schema,
    validate_session_transition, validate_session_time_contract,
    validate_session_package_binding, validate_session_authorization_binding,
    validate_session_platform_binding, validate_session_repository_binding,
    validate_parent_chain, validate_resume_preconditions, aggregate_session_validation
)

def test_validate_session_schema_valid():
    record = {
        "schema_version": 1,
        "session_id": "sess_1_valid",
        "session_state": SessionState.PENDING.value,
        "session_revision": 1,
        "created_at": "2026-07-10T12:00:00Z",
        "updated_at": "2026-07-10T12:00:00Z",
        "package_id": "pkg_1",
        "package_digest": "a" * 64,
        "authorization_id": "auth_1",
        "baseline_head": "0123456789abcdef0123456789abcdef01234567",
        "nonce": "n1_abcde",
        "workspace_instance_id": "ws_1",
        "resume_allowed": True,
        "session_identity_source": SessionIdentitySource.EXPLICIT_VALIDATION_INPUT.value,
        "parent_session_id": None
    }
    res = validate_session_schema(record)
    assert res["status"] == "PASS"

def test_validate_session_schema_negative():
    record = {
        "schema_version": 1,
        "session_id": "sess_1_valid",
        "session_state": SessionState.PENDING.value,
        "session_revision": 1,
        "created_at": "2026-07-10T12:00:00Z",
        "updated_at": "2026-07-10T12:00:00Z",
        "package_id": "pkg_1",
        "package_digest": "a" * 64,
        "authorization_id": "auth_1",
        "baseline_head": "0123456789abcdef0123456789abcdef01234567",
        "nonce": "n1_abcde",
        "workspace_instance_id": "ws_1",
        "resume_allowed": True,
        "session_identity_source": SessionIdentitySource.EXPLICIT_VALIDATION_INPUT.value,
        "parent_session_id": None
    }
    
    bad = dict(record)
    bad["unknown_field"] = 1
    assert validate_session_schema(bad)["error_code"] == "UNKNOWN_FIELD_IN_SESSION_RECORD"
    
    bad = dict(record)
    del bad["session_id"]
    assert validate_session_schema(bad)["error_code"] == "MISSING_REQUIRED_FIELD"
    
    bad = dict(record)
    bad["session_identity_source"] = SessionIdentitySource.VERIFIED_EXTERNAL_SOURCE.value
    assert validate_session_schema(bad)["error_code"] == "UNVERIFIED_SESSION_IDENTITY_SOURCE"
    
    bad = dict(record)
    bad["resume_allowed"] = "true" # not bool
    assert validate_session_schema(bad)["error_code"] == "INVALID_RESUME_ALLOWED_TYPE"

def test_validate_parent_chain():
    # Pass
    res = validate_parent_chain(
        "sess_current",
        {"check": "parent_session_lookup", "status": "PASS", "error_code": None, "expected": "PASS", "actual": {"session_id": "sess_parent"}},
        ["sess_parent", "sess_grandparent"],
        True
    )
    assert res["status"] == "PASS"
    
    # Missing lookup
    assert validate_parent_chain("sess_current", None, [], True)["status"] == "UNKNOWN_BLOCKED"
    
    # Bad provenance
    assert validate_parent_chain(
        "sess_current",
        {"check": "WRONG_CHECK", "status": "PASS", "error_code": None, "expected": "PASS", "actual": {}},
        [], True
    )["status"] == "UNKNOWN_BLOCKED"
    
    # Cycle
    res = validate_parent_chain(
        "sess_current",
        {"check": "parent_session_lookup", "status": "PASS", "error_code": None, "expected": "PASS", "actual": {"session_id": "sess_current"}},
        ["sess_current", "sess_grandparent"],
        True
    )
    assert res["error_code"] == "PARENT_CHAIN_CYCLE_DETECTED"
    
    # Duplicate ancestor
    res = validate_parent_chain(
        "sess_current",
        {"check": "parent_session_lookup", "status": "PASS", "error_code": None, "expected": "PASS", "actual": {"session_id": "sess_parent"}},
        ["sess_parent", "sess_parent"],
        True
    )
    assert res["error_code"] == "DUPLICATE_ANCESTOR_DETECTED"
    
    # Incomplete chain
    res = validate_parent_chain(
        "sess_current",
        {"check": "parent_session_lookup", "status": "PASS", "error_code": None, "expected": "PASS", "actual": {"session_id": "sess_parent"}},
        ["sess_parent"],
        False
    )
    assert res["error_code"] == "INCOMPLETE_PARENT_CHAIN"

def test_validate_resume_preconditions():
    session_record = {"session_state": SessionState.SUSPENDED.value, "resume_allowed": True}
    cap = {"check": "capability_lifecycle", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    dig = {"check": "package_digest", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    aut = {"check": "authorization_binding", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    repo = {"check": "repository_binding", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    plat = {"check": "platform_binding", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    rep = {"check": "replay_lookup", "status": "PASS", "error_code": None, "expected": "UNSEEN", "actual": "UNSEEN"}
    lock = {"check": "workspace_lock_lookup", "status": "PASS", "error_code": None, "expected": "ABSENT", "actual": "ABSENT"}
    par = {"check": "parent_chain_validation", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    
    res = validate_resume_preconditions(session_record, cap, dig, aut, repo, plat, rep, lock, par)
    assert res["status"] == "PASS"

    # Consumed replay blocks
    rep_bad = {"check": "replay_lookup", "status": "BLOCKED", "error_code": "UNSAFE_REPLAY_STATE_CONSUMED", "expected": "UNSEEN", "actual": "CONSUMED"}
    assert validate_resume_preconditions(session_record, cap, dig, aut, repo, plat, rep_bad, lock, par)["status"] == "BLOCKED"
    
    # Fabricated provenance blocks
    cap_bad = {"status": "PASS"} # missing provenance
    assert validate_resume_preconditions(session_record, cap_bad, dig, aut, repo, plat, rep, lock, par)["status"] == "UNKNOWN_BLOCKED"

def test_bindings():
    session_record = {
        "package_id": "pkg_1",
        "package_digest": "a" * 64,
        "authorization_id": "auth_1",
        "baseline_head": "1" * 40
    }
    
    # 1. Package Digest Binding
    digest_result = {
        "check": "package_digest",
        "status": "PASS",
        "error_code": None,
        "algorithm": "sha256",
        "expected_digest": "a" * 64,
        "actual_digest": "a" * 64
    }
    assert validate_session_package_binding(session_record, "pkg_1", "a" * 64, digest_result)["status"] == "PASS"
    
    # Negative tests for package digest binding
    bad_res = dict(digest_result)
    bad_res["status"] = "BLOCKED"
    assert validate_session_package_binding(session_record, "pkg_1", "a" * 64, bad_res)["status"] == "BLOCKED"
    
    # Fabricated PASS
    bad_res = dict(digest_result)
    bad_res["expected_digest"] = "PASS"
    bad_res["actual_digest"] = "PASS"
    assert validate_session_package_binding(session_record, "pkg_1", "a" * 64, bad_res)["error_code"] == "FABRICATED_DIGEST_PROVENANCE"
    
    # Mismatch package ID
    assert validate_session_package_binding(session_record, "pkg_2", "a" * 64, digest_result)["error_code"] == "PACKAGE_ID_MISMATCH"
    
    # Mismatch digest
    bad_res = dict(digest_result)
    bad_res["expected_digest"] = "b" * 64
    assert validate_session_package_binding(session_record, "pkg_1", "b" * 64, bad_res)["error_code"] == "SESSION_EXPECTED_DIGEST_MISMATCH"
    
    bad_res = dict(digest_result)
    bad_res["actual_digest"] = "b" * 64
    assert validate_session_package_binding(session_record, "pkg_1", "a" * 64, bad_res)["error_code"] == "EXPECTED_ACTUAL_DIGEST_MISMATCH"
    
    # Unsupported algorithm
    bad_res = dict(digest_result)
    bad_res["algorithm"] = "md5"
    assert validate_session_package_binding(session_record, "pkg_1", "a" * 64, bad_res)["error_code"] == "UNSUPPORTED_DIGEST_ALGORITHM"
    
    # Missing required field
    bad_res = dict(digest_result)
    del bad_res["algorithm"]
    assert validate_session_package_binding(session_record, "pkg_1", "a" * 64, bad_res)["error_code"] == "MALFORMED_DIGEST_VERIFICATION_PROVENANCE"

    # Invalid expected digest format
    bad_res = dict(digest_result)
    bad_res["expected_digest"] = "short"
    assert validate_session_package_binding(session_record, "pkg_1", "a" * 64, bad_res)["error_code"] == "INVALID_EXPECTED_DIGEST_FORMAT"

    # Bare PASS
    assert validate_session_package_binding(session_record, "pkg_1", "a" * 64, {"status": "PASS"})["error_code"] == "MALFORMED_DIGEST_VERIFICATION_PROVENANCE"
    
    # Wrong check
    bad_res = dict(digest_result)
    bad_res["check"] = "other_check"
    assert validate_session_package_binding(session_record, "pkg_1", "a" * 64, bad_res)["error_code"] == "WRONG_CHECK_IDENTITY_EXPECTED_package_digest"
    
    # 2. Authorization Binding
    auth_result = {
        "check": "authorization_binding",
        "status": "PASS",
        "error_code": None,
        "expected": "PASS",
        "actual": "PASS"
    }
    assert validate_session_authorization_binding(session_record, "auth_1", auth_result)["status"] == "PASS"
    assert validate_session_authorization_binding(session_record, "auth_2", auth_result)["status"] == "BLOCKED"
    
    # Platform
    plat_res = [
        {"check": "platform_profile", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "execution_environment", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "execution_mode", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    ]
    assert validate_session_platform_binding(plat_res)["status"] == "PASS"
    
    plat_res_bad = plat_res[:-1]
    assert validate_session_platform_binding(plat_res_bad)["status"] == "UNKNOWN_BLOCKED"
    
    # Repo
    repo_res = [
        {"check": "repository_identity", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "repository_remote", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "repository_branch", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "baseline_head", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "1"*40},
        {"check": "repository_state", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "repository_root", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "detached_head_policy", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    ]
    assert validate_session_repository_binding(session_record, repo_res)["status"] == "PASS"
    
    repo_res_bad = repo_res[:-1]
    assert validate_session_repository_binding(session_record, repo_res_bad)["status"] == "UNKNOWN_BLOCKED"
