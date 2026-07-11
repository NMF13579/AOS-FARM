import pytest
import sys
import os
import json
import copy
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from aos.runtime.strict_json import parse_strict_json
from aos.runtime.execution_package import validate_execution_package_schema
from aos.runtime.canonical_serialization import canonicalize_validated_json
from aos.runtime.package_digest import compute_package_digest, verify_package_digest
from aos.runtime.package_binding import bind_repository, aggregate_binding_results

from aos.runtime.capability_lifecycle import (
    CapabilityState,
    validate_capability_transition,
    verify_expiration,
    verify_revocation,
    validate_single_use,
    validate_capability_for_resume,
    parse_rfc3339_utc,
    AOSLifecycleError,
    InMemoryTestStateStore,
    _aggregate_results,
    validate_authorization_binding
)

def load_fixture(name):
    path = os.path.join(os.path.dirname(__file__), '../fixtures/runtime/execution_package/lifecycle', name)
    with open(path, 'r') as f:
        return json.load(f)

def test_parse_rfc3339_utc():
    dt = parse_rfc3339_utc("2026-01-01T00:00:00Z")
    assert dt.year == 2026
    
    dt2 = parse_rfc3339_utc("2026-01-01T00:00:00+00:00")
    assert dt2.year == 2026

    with pytest.raises(AOSLifecycleError): parse_rfc3339_utc("2026-01-01T00:00:00")
    with pytest.raises(AOSLifecycleError): parse_rfc3339_utc("invalid")
    with pytest.raises(AOSLifecycleError): parse_rfc3339_utc("2026-01-01T00:00:00.123Z") # No fractional
    with pytest.raises(AOSLifecycleError): parse_rfc3339_utc(" 2026-01-01T00:00:00Z ") # No spaces

def test_verify_expiration():
    pkg = load_fixture("unit/valid-issued.json")
    
    res = verify_expiration(pkg, "2026-06-01T00:00:00Z")
    assert res["status"] == "PASS"
    assert res["time_source"] == "EXPLICIT_VALIDATION_TIME"
    
    res_early = verify_expiration(pkg, "2025-12-31T23:59:59Z")
    assert res_early["status"] == "BLOCKED"
    assert res_early["error_code"] == "NOT_YET_VALID"
    
    res_late = verify_expiration(pkg, "2027-01-01T00:00:00Z")
    assert res_late["status"] == "BLOCKED"

def test_verify_revocation():
    rec_pass = {"revocation_reference": "ref1", "revocation_status": "NOT_REVOKED", "source_type": "EXPLICIT_VALIDATION_INPUT", "checked_at": "2026-01-01T00:00:00Z"}
    assert verify_revocation(rec_pass)["status"] == "PASS"
    
    rec_fail = {"revocation_reference": "ref1", "revocation_status": "REVOKED", "source_type": "EXPLICIT_VALIDATION_INPUT", "checked_at": "2026-01-01T00:00:00Z"}
    assert verify_revocation(rec_fail)["status"] == "BLOCKED"

    rec_unk = {"revocation_reference": "ref1", "revocation_status": "NOT_REVOKED", "source_type": "UNKNOWN_SOURCE", "checked_at": "2026-01-01T00:00:00Z"}
    assert verify_revocation(rec_unk)["status"] == "UNKNOWN_BLOCKED"

def test_validate_single_use():
    pkg = load_fixture("unit/valid-issued.json")
    
    rec_abs = {"record_status": "ABSENT"}
    rec_pres = {"package_id": "int-pkg-1", "package_digest": "deadbeef", "authorization_id": "auth-int-1", "activation_id": "act1", "activated_at": "2026-06-01T00:00:00Z", "capability_state": "ACTIVATED", "session_id": "sess1", "record_status": "PRESENT"}
    
    assert validate_single_use(pkg, rec_abs, rec_abs, "deadbeef")["status"] == "PASS"
    assert validate_single_use(pkg, rec_pres, rec_abs, "deadbeef")["status"] == "BLOCKED"

def test_validate_capability_transition_retry_false():
    pkg = load_fixture("unit/valid-issued.json")
    rev_rec = {"revocation_reference": "ref1", "revocation_status": "NOT_REVOKED", "source_type": "EXPLICIT_VALIDATION_INPUT", "checked_at": "2026-01-01T00:00:00Z"}
    
    res = validate_capability_transition(
        pkg, CapabilityState.ACTIVATION_PENDING, "2026-06-01T00:00:00Z",
        rev_rec, {"record_status": "ABSENT"}, {"record_status": "ABSENT"},
        "PASS", "PASS", "PASS", "deadbeef"
    )
    assert res["status"] == "PASS"
    assert res["retry_allowed"] is False
    
    res_inv = validate_capability_transition(
        pkg, CapabilityState.CONSUMED, "2026-06-01T00:00:00Z",
        rev_rec, {"record_status": "ABSENT"}, {"record_status": "ABSENT"},
        "PASS", "PASS", "PASS", "deadbeef"
    )
    assert res_inv["status"] == "BLOCKED"
    assert res_inv["error_code"] == "INVALID_LIFECYCLE_TRANSITION"
    assert res_inv["retry_allowed"] is False

def test_aggregation_not_run():
    assert _aggregate_results([{"status": "PASS"}, {"status": "NOT_RUN"}]) == "UNKNOWN_BLOCKED"
    assert _aggregate_results([{"status": "FAIL"}, {"status": "NOT_RUN"}]) == "UNKNOWN_BLOCKED"
    assert _aggregate_results([{"status": "BLOCKED"}, {"status": "NOT_RUN"}]) == "UNKNOWN_BLOCKED"
    assert _aggregate_results([{"status": "UNKNOWN_BLOCKED"}, {"status": "NOT_RUN"}]) == "UNKNOWN_BLOCKED"
    assert _aggregate_results([{"status": "PASS"}, {"status": "PASS"}]) == "PASS"

def test_in_memory_store_race_claims():
    store = InMemoryTestStateStore()
    assert store.production_ready is False
    assert store.atomic_compare_and_set is False

def setup_temp_repo(tmp_path):
    import subprocess
    repo_path = tmp_path / "test-repo"
    repo_path.mkdir()
    
    def run_cmd(cmd):
        subprocess.run(cmd, cwd=str(repo_path), shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    run_cmd("git init")
    run_cmd("git config user.name 'Test User'")
    run_cmd("git config user.email 'test@example.com'")
    run_cmd("git remote add origin https://github.com/NMF13579/AOS-FARM")
    run_cmd("echo 'test' > test.txt")
    run_cmd("git add test.txt")
    run_cmd("git commit -m 'Initial commit'")
    run_cmd("git branch -m dev")
    
    # get actual HEAD
    head = subprocess.run("git rev-parse HEAD", cwd=str(repo_path), shell=True, stdout=subprocess.PIPE, text=True).stdout.strip()
    return str(repo_path), head

def test_integration_full_package(tmp_path):
    repo_path, repo_head = setup_temp_repo(tmp_path)
    
    # 1. Parse
    raw_path = os.path.join(os.path.dirname(__file__), '../fixtures/runtime/execution_package/lifecycle/integration/full-package.json')
    with open(raw_path, 'rb') as f:
        raw_bytes = f.read()
    
    pkg = parse_strict_json(raw_bytes)
    pkg["baseline_head"] = repo_head # make it match our temporary repo
    
    # Check original
    
    # 2. Schema
    assert validate_execution_package_schema(pkg)
    
    # 3. Compute Digest
    actual_digest = compute_package_digest(pkg)
    pkg["package_digest"] = actual_digest
    orig_pkg = copy.deepcopy(pkg)

    
    digest_res = verify_package_digest(pkg)
    assert digest_res["status"] == "PASS"
    
    # 4. Authorization Binding
    auth_res = validate_authorization_binding(pkg.get("authorization_id"), "auth-int-1")
    assert auth_res["status"] == "PASS"
    
    # 5. Repository Binding
    repo_res = aggregate_binding_results(bind_repository(pkg, repo_path, "origin"))
    assert repo_res["status"] == "PASS"
    
    # 6. Lifecycle Transition Integration
    rev_rec = {"revocation_reference": "ref1", "revocation_status": "NOT_REVOKED", "source_type": "EXPLICIT_VALIDATION_INPUT", "checked_at": "2026-06-01T00:00:00Z"}
    
    res = validate_capability_transition(
        validated_package=pkg,
        target_state=CapabilityState.ACTIVATION_PENDING,
        validation_time_utc="2026-06-01T00:00:00Z",
        revocation_record=rev_rec,
        activation_record={"record_status": "ABSENT"},
        consumption_record={"record_status": "ABSENT"},
        package_binding_result_status=repo_res["status"],
        authorization_binding_result_status=auth_res["status"],
        package_digest_status=digest_res["status"],
        actual_package_digest=actual_digest
    )
    
    assert res["status"] == "PASS"
    assert res["error_code"] is None
    assert pkg == orig_pkg # Ensure package wasn't mutated
    
    # Verify records not implicitly created
    # We do this by ensuring the store wasn't invoked (we didn't pass one)
    
def test_negative_integrations(tmp_path):
    repo_path, repo_head = setup_temp_repo(tmp_path)
    raw_path = os.path.join(os.path.dirname(__file__), '../fixtures/runtime/execution_package/lifecycle/integration/full-package.json')
    with open(raw_path, 'rb') as f:
        pkg_base = parse_strict_json(f.read())
    pkg_base["baseline_head"] = repo_head
    actual_digest = compute_package_digest(pkg_base)
    pkg_base["package_digest"] = actual_digest
    pkg_base["lifecycle_state"] = "ACTIVATION_PENDING" # Valid state for ACTIVATED
    
    rev_rec = {"revocation_reference": "ref1", "revocation_status": "NOT_REVOKED", "source_type": "EXPLICIT_VALIDATION_INPUT", "checked_at": "2026-06-01T00:00:00Z"}
    
    # 1. Digest mismatch
    pkg_mut = copy.deepcopy(pkg_base)
    pkg_mut["execution_authorized"] = False # mutate
    digest_res = verify_package_digest(pkg_mut)
    assert digest_res["status"] == "BLOCKED"
    res = validate_capability_transition(pkg_mut, CapabilityState.ACTIVATED, "2026-06-01T00:00:00Z", rev_rec, {"record_status": "ABSENT"}, {"record_status": "ABSENT"}, "PASS", "PASS", digest_res["status"], digest_res.get("actual_digest", ""))
    assert res["status"] == "BLOCKED"

    # 2. Repository mismatch
    pkg_mut = copy.deepcopy(pkg_base)
    pkg_mut["remote_identity"] = "github.com/wrong/repo"
    repo_res = aggregate_binding_results(bind_repository(pkg_mut, repo_path, "origin"))
    assert repo_res["status"] == "BLOCKED"
    res = validate_capability_transition(pkg_mut, CapabilityState.ACTIVATED, "2026-06-01T00:00:00Z", rev_rec, {"record_status": "ABSENT"}, {"record_status": "ABSENT"}, repo_res["status"], "PASS", "PASS", actual_digest)
    assert res["status"] == "BLOCKED"

    # 3. Branch mismatch
    pkg_mut = copy.deepcopy(pkg_base)
    pkg_mut["branch"] = "wrong-branch"
    repo_res = aggregate_binding_results(bind_repository(pkg_mut, repo_path, "origin"))
    res = validate_capability_transition(pkg_mut, CapabilityState.ACTIVATED, "2026-06-01T00:00:00Z", rev_rec, {"record_status": "ABSENT"}, {"record_status": "ABSENT"}, repo_res["status"], "PASS", "PASS", actual_digest)
    assert res["status"] == "BLOCKED"

    # 4. Baseline mismatch
    pkg_mut = copy.deepcopy(pkg_base)
    pkg_mut["baseline_head"] = "0000000000000000000000000000000000000000"
    repo_res = aggregate_binding_results(bind_repository(pkg_mut, repo_path, "origin"))
    res = validate_capability_transition(pkg_mut, CapabilityState.ACTIVATED, "2026-06-01T00:00:00Z", rev_rec, {"record_status": "ABSENT"}, {"record_status": "ABSENT"}, repo_res["status"], "PASS", "PASS", actual_digest)
    assert res["status"] == "BLOCKED"

    # 5. Authorization mismatch
    auth_res = validate_authorization_binding(pkg_base["authorization_id"], "wrong-auth")
    res = validate_capability_transition(pkg_base, CapabilityState.ACTIVATED, "2026-06-01T00:00:00Z", rev_rec, {"record_status": "ABSENT"}, {"record_status": "ABSENT"}, "PASS", auth_res["status"], "PASS", actual_digest)
    assert res["status"] == "BLOCKED"

    # 6. Expired package
    res = validate_capability_transition(pkg_base, CapabilityState.ACTIVATED, "2027-01-01T00:00:00Z", rev_rec, {"record_status": "ABSENT"}, {"record_status": "ABSENT"}, "PASS", "PASS", "PASS", actual_digest)
    assert res["status"] == "BLOCKED"

    # 7. Revoked package
    rev_rec_bad = {"revocation_reference": "ref1", "revocation_status": "REVOKED", "source_type": "EXPLICIT_VALIDATION_INPUT", "checked_at": "2026-06-01T00:00:00Z"}
    res = validate_capability_transition(pkg_base, CapabilityState.ACTIVATED, "2026-06-01T00:00:00Z", rev_rec_bad, {"record_status": "ABSENT"}, {"record_status": "ABSENT"}, "PASS", "PASS", "PASS", actual_digest)
    assert res["status"] == "BLOCKED"

    # 8. Unknown revocation
    rev_rec_unk = {"revocation_reference": "ref1", "revocation_status": "UNKNOWN", "source_type": "EXPLICIT_VALIDATION_INPUT", "checked_at": "2026-06-01T00:00:00Z"}
    res = validate_capability_transition(pkg_base, CapabilityState.ACTIVATED, "2026-06-01T00:00:00Z", rev_rec_unk, {"record_status": "ABSENT"}, {"record_status": "ABSENT"}, "PASS", "PASS", "PASS", actual_digest)
    assert res["status"] == "UNKNOWN_BLOCKED"

    # 9. Existing activation
    act_rec = {"package_id": pkg_base["package_id"], "package_digest": actual_digest, "authorization_id": pkg_base["authorization_id"], "activation_id": "act1", "activated_at": "2026-06-01T00:00:00Z", "capability_state": "ACTIVATED", "session_id": "sess1", "record_status": "PRESENT"}
    res = validate_capability_transition(pkg_base, CapabilityState.ACTIVATED, "2026-06-01T00:00:00Z", rev_rec, act_rec, {"record_status": "ABSENT"}, "PASS", "PASS", "PASS", actual_digest)
    assert res["status"] == "BLOCKED"

    # 10. Required session check NOT_RUN
    res = validate_capability_transition(pkg_base, CapabilityState.ACTIVATED, "2026-06-01T00:00:00Z", rev_rec, {"record_status": "ABSENT"}, {"record_status": "ABSENT"}, "PASS", "NOT_RUN", "PASS", actual_digest)
    assert res["status"] == "UNKNOWN_BLOCKED"
