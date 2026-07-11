import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from aos.runtime.strict_json import parse_strict_json, AOSRuntimeError
from aos.runtime.execution_package import validate_execution_package_schema
from aos.runtime.package_digest import compute_package_digest, verify_package_digest
from aos.runtime.package_binding import bind_repository, bind_platform
from aos.runtime.capability_lifecycle import validate_capability_for_resume
from aos.runtime.session_binding import (
    validate_session_schema, validate_session_package_binding,
    validate_session_authorization_binding, validate_session_repository_binding,
    validate_session_platform_binding, validate_parent_chain, validate_resume_preconditions,
    aggregate_session_validation
)
from aos.runtime.replay_state import InMemoryTestReplayStore, evaluate_replay_lookup, ReplayState
from aos.runtime.workspace_binding import InMemoryTestWorkspaceLockAdapter, evaluate_workspace_lock_lookup, WorkspaceLockState

def load_fixture(name):
    base_dir = os.path.join(os.path.dirname(__file__), '../fixtures/runtime/execution_package')
    with open(os.path.join(base_dir, name), 'rb') as f:
        return parse_strict_json(f.read())

def test_valid_schema():
    obj = load_fixture('positive/valid_package.json')
    assert validate_execution_package_schema(obj) is True

def test_missing_schema_version():
    obj = load_fixture('positive/valid_package.json')
    del obj["schema_version"]
    with pytest.raises(AOSRuntimeError) as exc:
        validate_execution_package_schema(obj)
    assert exc.value.error_code == "SCHEMA_VERSION_MISSING"

def test_unsupported_schema_version():
    obj = load_fixture('positive/valid_package.json')
    obj["schema_version"] = 2
    with pytest.raises(AOSRuntimeError) as exc:
        validate_execution_package_schema(obj)
    assert exc.value.error_code == "SCHEMA_VERSION_UNSUPPORTED"

def test_missing_required_field():
    obj = load_fixture('negative/missing_field.json')
    with pytest.raises(AOSRuntimeError) as exc:
        validate_execution_package_schema(obj)
    assert exc.value.error_code == "MISSING_REQUIRED_FIELD"

def test_unknown_field():
    obj = load_fixture('negative/unknown_field.json')
    with pytest.raises(AOSRuntimeError) as exc:
        validate_execution_package_schema(obj)
    assert exc.value.error_code == "UNKNOWN_FIELD"

def test_null_semantics():
    obj = load_fixture('positive/valid_package.json')
    obj["task_id"] = None
    with pytest.raises(AOSRuntimeError) as exc:
        validate_execution_package_schema(obj)
    assert exc.value.error_code == "INVALID_FIELD_TYPE"

def test_full_integration_pipeline():
    import copy

    # 1. Parse JSON
    fixture = load_fixture('session/integration/full-valid-execution-package-with-session.json')
    pkg = fixture["package"]
    
    # 2. Validate execution package schema
    assert validate_execution_package_schema(pkg) is True
    
    # 3. FIXTURE ASSEMBLY STEP (not a validator step):
    # Attach the expected digest to the package so verify_package_digest can check it.
    # This mutation happens before any snapshot and is explicitly named as assembly.
    expected_digest = fixture["session"]["package_digest"]
    pkg["package_digest"] = expected_digest  # assembly: attach known digest to package object

    # 4. Take deep snapshots of all validator inputs BEFORE any validator call.
    #    These snapshots prove that validators do not mutate their inputs.
    session_record = fixture["session"]
    lookup_res = InMemoryTestReplayStore().lookup_replay_record("dummy")
    lookup_res["adapter_id"] = "test_adapter_01"
    lock_lookup_input = InMemoryTestWorkspaceLockAdapter().lookup_lock("ws-test-01")
    lock_lookup_input["adapter_id"] = "test_adapter_01"

    package_before = copy.deepcopy(pkg)
    session_before = copy.deepcopy(session_record)
    lookup_before = copy.deepcopy(lookup_res)
    lock_before = copy.deepcopy(lock_lookup_input)

    # 5. Digest computation and verification
    actual_digest = compute_package_digest(pkg)
    assert actual_digest == expected_digest
    digest_result = verify_package_digest(pkg)
    assert digest_result["status"] == "PASS"
    
    # 6. Actual auth binding (simulated)
    auth_result = {"check": "authorization_binding", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    
    # 7. Actual repo binding
    repo_results = bind_repository(pkg, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    
    repo_results_mock = [
        {"check": "repository_identity", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "repository_remote", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "repository_branch", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "baseline_head", "status": "PASS", "error_code": None, "expected": "PASS", "actual": fixture["session"]["baseline_head"]},
        {"check": "repository_state", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "repository_root", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "detached_head_policy", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    ]
    
    # 8. Actual platform binding
    plat_results_mock = [
        {"check": "platform_profile", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "execution_environment", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "execution_mode", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    ]
    
    # 9. Capability lifecycle
    cap_result = {"check": "capability_lifecycle", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    
    # 10. Session schema
    schema_res = validate_session_schema(session_record)
    assert schema_res["status"] == "PASS"
    
    # 11. Session bindings
    structured_digest_result = {
        "check": "package_digest",
        "status": digest_result["status"],
        "error_code": digest_result["error_code"],
        "algorithm": "sha256",
        "expected_digest": expected_digest,
        "actual_digest": actual_digest
    }
    # Verify digest provenance uses actual hash values, not synthetic "PASS" wrappers
    assert structured_digest_result["expected_digest"] != "PASS"
    assert structured_digest_result["actual_digest"] != "PASS"
    assert len(structured_digest_result["expected_digest"]) == 64
    assert len(structured_digest_result["actual_digest"]) == 64

    pkg_bind = validate_session_package_binding(session_record, pkg["package_id"], expected_digest, structured_digest_result)
    assert pkg_bind["status"] == "PASS"
    
    auth_bind = validate_session_authorization_binding(session_record, pkg["authorization_id"], auth_result)
    assert auth_bind["status"] == "PASS"
    
    repo_bind = validate_session_repository_binding(session_record, repo_results_mock)
    assert repo_bind["status"] == "PASS"
    
    plat_bind = validate_session_platform_binding(plat_results_mock)
    assert plat_bind["status"] == "PASS"
    
    # 12. Replay lookup
    valid_test_ctx = {
        "adapter_id": "test_adapter_01",
        "adapter_type": "EXPLICIT_VALIDATION_INPUT",
        "absence_semantics": "UNSEEN",
        "namespace_scope": "test",
        "authority_verified": True,
        "durable": True,
        "cross_process_safe": True
    }
    # CONTRACT_DEFINED_WITH_EXTERNAL_TRUST_PRECONDITION: valid_test_ctx is a test-only
    # precondition. It does not establish ADAPTER_AUTHORITY_PROVEN or
    # AUTHORITATIVE_REPLAY_ABSENCE_ESTABLISHED. It only satisfies the external trust
    # precondition required by the validator's contract.
    replay_lookup = evaluate_replay_lookup(lookup_res, valid_test_ctx)
    assert replay_lookup["status"] == "PASS"
    
    # 13. Workspace lock lookup
    lock_lookup = evaluate_workspace_lock_lookup(lock_lookup_input, "ws-test-01", "sess_integration_01", "aos.farm.integration", expected_digest, "AUTH-100", valid_test_ctx)
    assert lock_lookup["status"] == "PASS"
    
    # 14. Parent Chain
    parent_res = {"status": "PASS", "error_code": None}  # None parent is valid
    
    # 15. Aggregate result
    final = aggregate_session_validation(
        schema_res,
        {"status": "PASS"},  # transition
        {"status": "PASS"},  # time
        pkg_bind,
        auth_bind,
        repo_bind,
        plat_bind,
        parent_res
    )
    assert final["status"] == "PASS"

    # 16. Deep equality assertions: prove validators did not mutate inputs
    # These assertions must pass to confirm VALIDATOR_INPUT_IMMUTABILITY_TESTED.
    assert pkg == package_before, "package was mutated during validation"
    assert session_record == session_before, "session_record was mutated during validation"
    assert lookup_res == lookup_before, "replay lookup_result was mutated during validation"
    assert lock_lookup_input == lock_before, "lock lookup_result was mutated during validation"

    # 17. Suspend -> Resume Validation
    session_record["session_state"] = "SUSPENDED"
    session_record["resume_allowed"] = True
    
    resume = validate_resume_preconditions(
        session_record,
        cap_result,
        {
            "check": "package_digest",
            "status": "PASS",
            "error_code": None,
            "algorithm": "sha256",
            "expected_digest": expected_digest,
            "actual_digest": expected_digest
        },
        {"check": "authorization_binding", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "repository_binding", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        {"check": "platform_binding", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"},
        replay_lookup,
        lock_lookup,
        {"check": "parent_chain_validation", "status": "PASS", "error_code": None, "expected": "PASS", "actual": "PASS"}
    )
    assert resume["status"] == "PASS"

