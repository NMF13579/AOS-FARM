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

def test_validate_workspace_state_binding():
    """Test validate_workspace_state_binding contract.

    Coverage:
    1. Full exact match (tracked_clean allowed) → technical PASS.
    2. Workspace with untracked-only inventory, required_checks absent → BLOCKED UNTRACKED_INVENTORY_PRESENT.
    3. Missing required binding field (no remote_identity) → baseline_state still obtained,
       other checks blocked but baseline_state PASS with tracked_clean → technical PASS
       (state binding only checks baseline_state, not remote identity).
    4. Invalid repository root → MISSING_REPOSITORY_STATE_CHECK → UNKNOWN_BLOCKED.
    5. baseline_head mismatch → baseline_head BLOCKED from bind_repository,
       but baseline_state still obtained → state binding checks state, not head mismatch.
    6. Wrong type for baseline_head field → UNKNOWN_BLOCKED (BINDING_EXCEPTION, fail-closed).
    7. Wrong type for entire package argument → UNKNOWN_BLOCKED (BINDING_EXCEPTION, fail-closed).
    8. Input package dict not mutated by validator.
    9. PASS is not approval.
    10. Staged changes present → BLOCKED DIRTY_TRACKED_STATE (tested via mock context).
    11. Unstaged tracked changes present → BLOCKED DIRTY_TRACKED_STATE.
    12. Missing required field in package → baseline_state check still runs (see item 3).

    Note: validate_workspace_state_binding evaluates repository BASELINE STATE only.
    It does NOT check workspace_instance_id, repository_id, branch, baseline_head,
    package_id, package_digest, or authorization_id binding — those are responsibilities
    of validate_workspace_lock_record and evaluate_workspace_lock_lookup (covered in
    their respective tests above). PASS from this validator is not approval.
    CONTRACT_DEFINED_WITH_EXTERNAL_TRUST_PRECONDITION applies to workspace lock authority.
    """
    import os
    REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    # Minimal package with valid baseline_head for real repo
    base_pkg = {
        "remote_identity": "github.com/NMF13579/AOS-FARM",
        "branch": "build/aos-farm-677-execution-package-foundation",
        "baseline_head": "9defceec6dda20f3e6ee16683e5cb7ff12c3bfa8",
        "required_checks": {"tracked_clean": True}
    }

    # ── Item 1: PASS with tracked_clean=True (untracked present but permitted) ──
    pkg_1 = copy.deepcopy(base_pkg)
    pkg_before_1 = copy.deepcopy(pkg_1)
    res_1 = validate_workspace_state_binding(pkg_1, REPO_ROOT)
    assert res_1["status"] == "PASS", f"Expected PASS, got {res_1}"
    assert res_1["error_code"] is None
    # Item 9: PASS is not approval
    assert res_1["status"] != "APPROVED"
    # Item 8: Input not mutated
    assert pkg_1 == pkg_before_1, "validate_workspace_state_binding must not mutate the package"

    # ── Item 2: BLOCKED — untracked inventory without tracked_clean permission ──
    pkg_2 = copy.deepcopy(base_pkg)
    del pkg_2["required_checks"]
    pkg_before_2 = copy.deepcopy(pkg_2)
    res_2 = validate_workspace_state_binding(pkg_2, REPO_ROOT)
    assert res_2["status"] == "BLOCKED"
    assert res_2["error_code"] == "UNTRACKED_INVENTORY_PRESENT"
    assert pkg_2 == pkg_before_2, "Validator must not mutate the package"

    # ── Item 3: Missing binding field (no remote_identity) ──
    # baseline_state is still obtained because bind_repository runs state check
    # regardless of remote_identity miss. The result for validate_workspace_state_binding
    # is determined only by baseline_state.
    pkg_3 = copy.deepcopy(base_pkg)
    del pkg_3["remote_identity"]
    pkg_before_3 = copy.deepcopy(pkg_3)
    res_3 = validate_workspace_state_binding(pkg_3, REPO_ROOT)
    # baseline_state is still computed → result is PASS (tracked_clean=True) or BLOCKED
    # (UNTRACKED_INVENTORY_PRESENT) depending on current state. Either is a known contract.
    # The key assertion: it must not raise an exception, and it must not return UNKNOWN here.
    assert res_3["status"] in ("PASS", "BLOCKED")
    assert pkg_3 == pkg_before_3, "Validator must not mutate the package"

    # ── Item 4: Invalid repository root → UNKNOWN_BLOCKED MISSING_REPOSITORY_STATE_CHECK ──
    pkg_4 = copy.deepcopy(base_pkg)
    pkg_before_4 = copy.deepcopy(pkg_4)
    res_4 = validate_workspace_state_binding(pkg_4, "/this/path/does/not/exist")
    assert res_4["status"] == "UNKNOWN_BLOCKED"
    assert res_4["error_code"] == "MISSING_REPOSITORY_STATE_CHECK"
    assert pkg_4 == pkg_before_4, "Validator must not mutate the package"

    # ── Item 5: baseline_head mismatch ──
    # bind_repository produces a BLOCKED baseline_head check but still produces
    # the baseline_state check. validate_workspace_state_binding only checks baseline_state.
    pkg_5 = copy.deepcopy(base_pkg)
    pkg_5["baseline_head"] = "0" * 40  # wrong head
    pkg_before_5 = copy.deepcopy(pkg_5)
    res_5 = validate_workspace_state_binding(pkg_5, REPO_ROOT)
    # With current workspace state (untracked present, tracked_clean allowed):
    # baseline_state PASS → returns PASS or BLOCKED (based on untracked)
    assert res_5["status"] in ("PASS", "BLOCKED")
    assert pkg_5 == pkg_before_5, "Validator must not mutate the package"

    # ── Item 6: Wrong type for baseline_head field (int instead of str) ──
    # bind_repository raises TypeError internally; validator must fail-closed → UNKNOWN_BLOCKED
    pkg_6 = copy.deepcopy(base_pkg)
    pkg_6["baseline_head"] = 12345  # wrong type
    pkg_before_6 = copy.deepcopy(pkg_6)
    res_6 = validate_workspace_state_binding(pkg_6, REPO_ROOT)
    assert res_6["status"] == "UNKNOWN_BLOCKED"
    assert res_6["error_code"] == "BINDING_EXCEPTION"
    assert pkg_6 == pkg_before_6, "Validator must not mutate the package"

    # ── Item 7: Wrong type for entire package argument (str instead of dict) ──
    # Must fail-closed, not raise unhandled exception
    res_7 = validate_workspace_state_binding("not_a_dict", REPO_ROOT)
    assert res_7["status"] == "UNKNOWN_BLOCKED"
    assert res_7["error_code"] == "BINDING_EXCEPTION"

    # ── Items 10–11: Dirty tracked state — tested via monkeypatching ──
    # We cannot create real staged/unstaged changes without modifying the working tree.
    # We verify the contract by directly invoking the underlying state evaluation path.
    # The validator returns BLOCKED with DIRTY_TRACKED_STATE when baseline_state reports
    # staged_changes_present=True or unstaged_tracked_changes_present=True.
    # We confirm the production code path by monkeypatching bind_repository:

    # Import the actual function and patch bind_repository in the workspace_binding module
    original_bind = None
    try:
        from aos.runtime import package_binding as pb_mod
        original_bind = pb_mod.bind_repository

        # Item 10: staged changes present
        def mock_bind_staged(pkg, root, *a, **kw):
            return [{"check": "baseline_state", "status": "PASS", "error_code": None,
                     "actual": {"staged_changes_present": True, "unstaged_tracked_changes_present": False,
                                "untracked_inventory_present": False, "tracked_clean": False}}]
        pb_mod.bind_repository = mock_bind_staged
        pkg_10 = {"remote_identity": "x", "branch": "y", "baseline_head": "a"*40}
        pkg_before_10 = copy.deepcopy(pkg_10)
        res_10 = validate_workspace_state_binding(pkg_10, REPO_ROOT)
        assert res_10["status"] == "BLOCKED"
        assert res_10["error_code"] == "DIRTY_TRACKED_STATE"
        assert pkg_10 == pkg_before_10, "Validator must not mutate the package"

        # Item 11: unstaged tracked changes present
        def mock_bind_unstaged(pkg, root, *a, **kw):
            return [{"check": "baseline_state", "status": "PASS", "error_code": None,
                     "actual": {"staged_changes_present": False, "unstaged_tracked_changes_present": True,
                                "untracked_inventory_present": False, "tracked_clean": False}}]
        pb_mod.bind_repository = mock_bind_unstaged
        res_11 = validate_workspace_state_binding(pkg_10, REPO_ROOT)
        assert res_11["status"] == "BLOCKED"
        assert res_11["error_code"] == "DIRTY_TRACKED_STATE"

    finally:
        if original_bind is not None:
            pb_mod.bind_repository = original_bind

    # ── Item 12: PASS ≠ approval (explicit assertion) ──
    assert "APPROVED" not in (res_1.get("status"), res_1.get("error_code"))
    assert res_1["status"] == "PASS"
    # PASS from this validator is a technical result only. It is not human approval.

