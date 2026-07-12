import pytest
import copy
from aos.runtime.workspace_binding import (
    WorkspaceLockState, WorkspaceLockSourceType, validate_workspace_instance_id,
    validate_workspace_lock_record, evaluate_workspace_lock_lookup,
    InMemoryTestWorkspaceLockAdapter, validate_workspace_state_binding
)

def test_validate_workspace_instance_id_valid():
    res = validate_workspace_instance_id("valid_workspace-123_abc")
    assert res["status"] == "PASS"

def test_validate_workspace_instance_id_invalid():
    assert validate_workspace_instance_id("")["error_code"] == "MISSING_WORKSPACE_INSTANCE_ID"
    assert validate_workspace_instance_id("../malicious")["error_code"] == "INVALID_WORKSPACE_INSTANCE_ID_CHARACTERS"
    assert validate_workspace_instance_id("C:\\Windows")["error_code"] == "INVALID_WORKSPACE_INSTANCE_ID_CHARACTERS"
    assert validate_workspace_instance_id("space here")["error_code"] == "INVALID_WORKSPACE_INSTANCE_ID_CHARACTERS"
    assert validate_workspace_instance_id("forward/slash")["error_code"] == "INVALID_WORKSPACE_INSTANCE_ID_CHARACTERS"

def test_validate_workspace_lock_record_valid_present_self():
    record = {
        "workspace_instance_id": "ws_1",
        "session_id": "sess_1_valid",
        "package_id": "pkg_1",
        "package_digest": "a" * 64,
        "authorization_id": "auth_1",
        "lock_id": "lock_123",
        "lock_state": WorkspaceLockState.PRESENT_SELF.value,
        "created_at": "2026-07-10T12:00:00Z",
        "expires_at": "2026-07-10T13:00:00Z",
        "source_type": WorkspaceLockSourceType.EXPLICIT_VALIDATION_INPUT.value
    }
    res = validate_workspace_lock_record(record, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1")
    assert res["status"] == "PASS"

def test_validate_workspace_lock_record_negative():
    record = {
        "workspace_instance_id": "ws_1",
        "session_id": "sess_1_valid",
        "package_id": "pkg_1",
        "package_digest": "a" * 64,
        "authorization_id": "auth_1",
        "lock_id": "lock_123",
        "lock_state": WorkspaceLockState.PRESENT_SELF.value,
        "created_at": "2026-07-10T12:00:00Z",
        "expires_at": "2026-07-10T13:00:00Z",
        "source_type": WorkspaceLockSourceType.EXPLICIT_VALIDATION_INPUT.value
    }

    # Unknown field
    bad = dict(record)
    bad["unknown"] = 1
    assert validate_workspace_lock_record(bad, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1")["error_code"] == "UNKNOWN_FIELD_IN_WORKSPACE_LOCK"

    # Missing required field
    bad = dict(record)
    del bad["lock_id"]
    assert validate_workspace_lock_record(bad, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1")["error_code"] == "MISSING_REQUIRED_FIELD"

    # Bad expiration
    bad = dict(record)
    bad["expires_at"] = "2026-07-10T11:00:00Z"
    assert validate_workspace_lock_record(bad, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1")["error_code"] == "EXPIRES_BEFORE_CREATED"

    # Mismatches
    assert validate_workspace_lock_record(record, "ws_2", "sess_1_valid", "pkg_1", "a" * 64, "auth_1")["error_code"] == "WORKSPACE_INSTANCE_ID_MISMATCH"
    assert validate_workspace_lock_record(record, "ws_1", "sess_2", "pkg_1", "a" * 64, "auth_1")["error_code"] == "SESSION_ID_MISMATCH"
    assert validate_workspace_lock_record(record, "ws_1", "sess_1_valid", "pkg_2", "a" * 64, "auth_1")["error_code"] == "PACKAGE_ID_MISMATCH"
    assert validate_workspace_lock_record(record, "ws_1", "sess_1_valid", "pkg_1", "b" * 64, "auth_1")["error_code"] == "PACKAGE_DIGEST_MISMATCH"
    assert validate_workspace_lock_record(record, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_2")["error_code"] == "AUTHORIZATION_ID_MISMATCH"

    # Authoritative source rejection
    bad = dict(record)
    bad["source_type"] = WorkspaceLockSourceType.AUTHORITATIVE_SYSTEM_LOCK.value
    assert validate_workspace_lock_record(bad, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1")["error_code"] == "SELF_DECLARED_AUTHORITATIVE_SYSTEM_LOCK"

def test_evaluate_workspace_lock_lookup():
    valid_ctx = {
        "adapter_id": "test_adapter_01",
        "adapter_type": "EXPLICIT_VALIDATION_INPUT",
        "absence_semantics": "ABSENT",
        "namespace_scope": "test",
        "authority_verified": True,
        "durable": True,
        "cross_process_safe": True
    }

    # Missing verified context
    assert evaluate_workspace_lock_lookup(None, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1")["error_code"] == "MISSING_VERIFIED_ADAPTER_CONTEXT"

    # Missing lookup result
    assert evaluate_workspace_lock_lookup(None, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1", valid_ctx)["error_code"] == "MISSING_LOOKUP_RESULT"

    lookup = {
        "lookup_status": "FOUND",
        "source_type": WorkspaceLockSourceType.EXPLICIT_VALIDATION_INPUT.value,
        "adapter_capabilities": {},
        "adapter_id": "test_adapter_01"
    }
    assert evaluate_workspace_lock_lookup(lookup, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1", valid_ctx)["error_code"] == "FOUND_BUT_MISSING_RECORD"

    record = {
        "workspace_instance_id": "ws_1",
        "session_id": "sess_1_valid",
        "package_id": "pkg_1",
        "package_digest": "a" * 64,
        "authorization_id": "auth_1",
        "lock_id": "lock_123",
        "lock_state": WorkspaceLockState.PRESENT_SELF.value,
        "created_at": "2026-07-10T12:00:00Z",
        "expires_at": "2026-07-10T13:00:00Z",
        "source_type": WorkspaceLockSourceType.EXPLICIT_VALIDATION_INPUT.value
    }

    lookup["record"] = record
    assert evaluate_workspace_lock_lookup(lookup, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1", valid_ctx)["status"] == "PASS"

    record["lock_state"] = WorkspaceLockState.PRESENT_OTHER.value
    assert evaluate_workspace_lock_lookup(lookup, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1", valid_ctx)["status"] == "BLOCKED"

    # Authority Spoofing Negative Tests
    # 1. Adapter ID mismatch
    lookup["adapter_id"] = "spoofed_adapter"
    assert evaluate_workspace_lock_lookup(lookup, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1", valid_ctx)["error_code"] == "ADAPTER_ID_MISMATCH"

    # 2. Lock lookup NOT_FOUND with unverified authority claim
    lookup["lookup_status"] = "NOT_FOUND"
    lookup["adapter_id"] = "test_adapter_01"
    bad_ctx = dict(valid_ctx)
    bad_ctx["authority_verified"] = False
    assert evaluate_workspace_lock_lookup(lookup, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1", bad_ctx)["error_code"] == "UNVERIFIED_AUTHORITY_CLAIM"

    # 3. Lock lookup NOT_FOUND with non-authoritative absence (durable=False)
    bad_ctx = dict(valid_ctx)
    bad_ctx["durable"] = False
    assert evaluate_workspace_lock_lookup(lookup, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1", bad_ctx)["error_code"] == "NON_AUTHORITATIVE_ABSENCE"

    # 4. Valid NOT_FOUND
    assert evaluate_workspace_lock_lookup(lookup, "ws_1", "sess_1_valid", "pkg_1", "a" * 64, "auth_1", valid_ctx)["status"] == "PASS"

def test_in_memory_adapter():
    adapter = InMemoryTestWorkspaceLockAdapter()
    assert adapter.capability_declaration["durable"] is False
    assert adapter.capability_declaration["atomic_acquire"] is False

    adapter.set_test_lock_record("ws_1", {"lock_state": WorkspaceLockState.PRESENT_SELF.value})
    assert adapter.lookup_lock("ws_1")["record"]["lock_state"] == WorkspaceLockState.PRESENT_SELF.value

def _workspace_binding_base_package():
    return {
        "remote_identity": "github.com/NMF13579/AOS-FARM",
        "branch": "build/aos-farm-680-candidate-freeze",
        "baseline_head": "1caac06c1bd3ad96bfcfdb8433bd208aabb75dc4",
    }


def _mock_baseline_state(
    *,
    staged_changes_present=False,
    unstaged_tracked_changes_present=False,
    untracked_inventory_present=False,
    tracked_clean=True,
):
    return {
        "staged_changes_present": staged_changes_present,
        "unstaged_tracked_changes_present": unstaged_tracked_changes_present,
        "untracked_inventory_present": untracked_inventory_present,
        "tracked_clean": tracked_clean,
    }


def _patch_bind_repository(monkeypatch, results):
    from aos.runtime import package_binding as pb_mod

    def mock_bind_repository(validated_package, repository_root, *args, **kwargs):
        return copy.deepcopy(results)

    monkeypatch.setattr(pb_mod, "bind_repository", mock_bind_repository)


@pytest.mark.parametrize(
    ("state", "required_checks", "expected_status", "expected_error_code"),
    [
        (
            _mock_baseline_state(
                staged_changes_present=False,
                unstaged_tracked_changes_present=False,
                untracked_inventory_present=False,
                tracked_clean=True,
            ),
            None,
            "PASS",
            None,
        ),
        (
            _mock_baseline_state(
                staged_changes_present=False,
                unstaged_tracked_changes_present=False,
                untracked_inventory_present=True,
                tracked_clean=True,
            ),
            None,
            "BLOCKED",
            "UNTRACKED_INVENTORY_PRESENT",
        ),
        (
            _mock_baseline_state(
                staged_changes_present=False,
                unstaged_tracked_changes_present=False,
                untracked_inventory_present=True,
                tracked_clean=True,
            ),
            {"tracked_clean": True},
            "PASS",
            None,
        ),
        (
            _mock_baseline_state(
                staged_changes_present=True,
                unstaged_tracked_changes_present=False,
                untracked_inventory_present=False,
                tracked_clean=False,
            ),
            None,
            "BLOCKED",
            "DIRTY_TRACKED_STATE",
        ),
        (
            _mock_baseline_state(
                staged_changes_present=False,
                unstaged_tracked_changes_present=True,
                untracked_inventory_present=False,
                tracked_clean=False,
            ),
            None,
            "BLOCKED",
            "DIRTY_TRACKED_STATE",
        ),
    ],
)
def test_validate_workspace_state_binding(monkeypatch, state, required_checks, expected_status, expected_error_code):
    """Deterministic repository-state contract for validate_workspace_state_binding.

    This test validates the mapping from bind_repository baseline_state output
    to validate_workspace_state_binding result. It intentionally does not use
    the active repository's real untracked inventory as a fixture.
    """
    _patch_bind_repository(
        monkeypatch,
        [
            {
                "check": "baseline_state",
                "status": "PASS",
                "error_code": None,
                "expected": None,
                "actual": state,
                "message": "Reported",
            }
        ],
    )
    pkg = _workspace_binding_base_package()
    if required_checks is not None:
        pkg["required_checks"] = required_checks

    pkg_before = copy.deepcopy(pkg)
    result = validate_workspace_state_binding(pkg, "/unused/repository/root")

    assert result["status"] == expected_status
    assert result["error_code"] == expected_error_code
    assert pkg == pkg_before, "validate_workspace_state_binding must not mutate the package"
    assert result["status"] != "APPROVED"


def test_validate_workspace_state_binding_missing_baseline_state(monkeypatch):
    _patch_bind_repository(
        monkeypatch,
        [
            {
                "check": "remote_identity",
                "status": "PASS",
                "error_code": None,
                "expected": "github.com/NMF13579/AOS-FARM",
                "actual": "github.com/NMF13579/AOS-FARM",
                "message": "Match",
            }
        ],
    )
    pkg = _workspace_binding_base_package()
    pkg_before = copy.deepcopy(pkg)

    result = validate_workspace_state_binding(pkg, "/unused/repository/root")

    assert result["status"] == "UNKNOWN_BLOCKED"
    assert result["error_code"] == "MISSING_REPOSITORY_STATE_CHECK"
    assert pkg == pkg_before, "validate_workspace_state_binding must not mutate the package"


def test_validate_workspace_state_binding_missing_binding_field_still_uses_baseline_state(monkeypatch):
    _patch_bind_repository(
        monkeypatch,
        [
            {
                "check": "remote_identity",
                "status": "UNKNOWN_BLOCKED",
                "error_code": "MISSING_REQUIRED_FIELD",
                "expected": None,
                "actual": None,
                "message": "Required",
            },
            {
                "check": "baseline_state",
                "status": "PASS",
                "error_code": None,
                "expected": None,
                "actual": _mock_baseline_state(
                    staged_changes_present=False,
                    unstaged_tracked_changes_present=False,
                    untracked_inventory_present=False,
                    tracked_clean=True,
                ),
                "message": "Reported",
            },
        ],
    )
    pkg = _workspace_binding_base_package()
    del pkg["remote_identity"]
    pkg_before = copy.deepcopy(pkg)

    result = validate_workspace_state_binding(pkg, "/unused/repository/root")

    assert result["status"] == "PASS"
    assert result["error_code"] is None
    assert pkg == pkg_before, "validate_workspace_state_binding must not mutate the package"
    assert result["status"] != "APPROVED"


def test_validate_workspace_state_binding_invalid_repository_root():
    pkg = _workspace_binding_base_package()
    pkg["required_checks"] = {"tracked_clean": True}
    pkg_before = copy.deepcopy(pkg)

    result = validate_workspace_state_binding(pkg, "/this/path/does/not/exist")

    assert result["status"] == "UNKNOWN_BLOCKED"
    assert result["error_code"] == "MISSING_REPOSITORY_STATE_CHECK"
    assert pkg == pkg_before, "validate_workspace_state_binding must not mutate the package"


def test_validate_workspace_state_binding_wrong_baseline_head_type_fails_closed():
    import os

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    pkg = _workspace_binding_base_package()
    pkg["required_checks"] = {"tracked_clean": True}
    pkg["baseline_head"] = 12345
    pkg_before = copy.deepcopy(pkg)

    result = validate_workspace_state_binding(pkg, repo_root)

    assert result["status"] == "UNKNOWN_BLOCKED"
    assert result["error_code"] == "BINDING_EXCEPTION"
    assert pkg == pkg_before, "validate_workspace_state_binding must not mutate the package"


def test_validate_workspace_state_binding_wrong_package_type_fails_closed():
    import os

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    result = validate_workspace_state_binding("not_a_dict", repo_root)

    assert result["status"] == "UNKNOWN_BLOCKED"
    assert result["error_code"] == "BINDING_EXCEPTION"


# --- F-2 Parity and Contract Tests ---

@pytest.mark.parametrize(
    ("session_id", "expected_accepts"),
    [
        ("session_123", True),
        ("session-123", True),
        ("Session_ABC-123", True),
        ("", False),
        ("short", False),
        ("a" * 257, False),
        ("sess 123", False),
        ("sess/123", False),
        ("sess:123", False),
        ("sess.123", False),
        ("sess!123", False),
        ("sessю123", False),
        (None, False),
        (123, False),
    ],
)
def test_workspace_lock_session_id_accept_reject_parity(session_id, expected_accepts):
    import copy
    from aos.runtime.session_binding import validate_session_id

    # invalid-type tests (None, 123) should use a stable valid ID as expected_session_id
    # invalid characters should use the same ID as expected_session_id for invalid-but-equal check
    if session_id is None or isinstance(session_id, int):
        expected_session_id = "session_123"
    else:
        expected_session_id = session_id

    record = {
        "workspace_instance_id": "valid_workspace",
        "package_id": "pkg_1",
        "package_digest": "a"*64,
        "authorization_id": "auth_1",
        "lock_id": "lock",
        "lock_state": "PRESENT_SELF",
        "created_at": "2026-07-10T12:00:00Z",
        "expires_at": "2026-07-10T13:00:00Z",
        "source_type": "EXPLICIT_VALIDATION_INPUT",
        "session_id": session_id
    }
    record_before = copy.deepcopy(record)

    try:
        session_result = validate_session_id(session_id)
        session_accepts = session_result["status"] == "PASS"
    except TypeError:
        session_accepts = False

    w_res = validate_workspace_lock_record(record, "valid_workspace", expected_session_id, "pkg_1", "a"*64, "auth_1")
    workspace_accepts = w_res["status"] == "PASS"

    assert session_accepts is expected_accepts
    assert workspace_accepts is expected_accepts
    assert session_accepts == workspace_accepts

    if not workspace_accepts:
        assert w_res["error_code"] == "INVALID_SESSION_ID_FORMAT"

    assert record == record_before

def test_workspace_lock_invalid_but_equal():
    import copy
    record = {
        "workspace_instance_id": "valid_workspace",
        "package_id": "pkg_1",
        "package_digest": "a"*64,
        "authorization_id": "auth_1",
        "lock_id": "lock",
        "lock_state": "PRESENT_SELF",
        "created_at": "2026-07-10T12:00:00Z",
        "expires_at": "2026-07-10T13:00:00Z",
        "source_type": "EXPLICIT_VALIDATION_INPUT",
        "session_id": "sess/123"
    }
    record_before = copy.deepcopy(record)

    w_res = validate_workspace_lock_record(record, "valid_workspace", "sess/123", "pkg_1", "a"*64, "auth_1")

    assert w_res["status"] == "BLOCKED"
    assert w_res["error_code"] == "INVALID_SESSION_ID_FORMAT"
    assert record == record_before

def test_workspace_lock_valid_format_mismatch():
    import copy
    record = {
        "workspace_instance_id": "valid_workspace",
        "package_id": "pkg_1",
        "package_digest": "a"*64,
        "authorization_id": "auth_1",
        "lock_id": "lock",
        "lock_state": "PRESENT_SELF",
        "created_at": "2026-07-10T12:00:00Z",
        "expires_at": "2026-07-10T13:00:00Z",
        "source_type": "EXPLICIT_VALIDATION_INPUT",
        "session_id": "session_123"
    }
    record_before = copy.deepcopy(record)

    w_res = validate_workspace_lock_record(record, "valid_workspace", "session_456", "pkg_1", "a"*64, "auth_1")

    assert w_res["status"] == "BLOCKED"
    assert w_res["error_code"] == "SESSION_ID_MISMATCH"
    assert record == record_before

def test_workspace_id_empty_string():
    res = validate_workspace_instance_id("")
    assert res["status"] == "BLOCKED"
    assert res["error_code"] == "MISSING_WORKSPACE_INSTANCE_ID"
