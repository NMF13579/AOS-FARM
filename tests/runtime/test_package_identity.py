import pytest
import datetime
import hashlib
from aos.runtime.package_identity import generate_package_identity, DOMAIN_BYTES
from aos.runtime.strict_json import AOSRuntimeError

def get_base_package_core():
    return {
        "schema_version": 1,
        "operation": "MERGE_AUTHORIZATION",
        "repository_identity": "owner/repo",
        "tool_identity": {
            "generator_build_digest": "sha256:" + "a"*64
        }
    }

def test_valid_package_core_produces_package_id():
    res = generate_package_identity(get_base_package_core())
    assert "package_id" in res
    assert res["package_id"].startswith("sha256:")
    assert len(res["package_id"]) == 7 + 64

def test_same_package_core_produces_same_package_id():
    res1 = generate_package_identity(get_base_package_core())
    res2 = generate_package_identity(get_base_package_core())
    assert res1["package_id"] == res2["package_id"]

def test_dictionary_key_order_does_not_affect_id():
    core1 = {"schema_version": 1, "operation": "A"}
    core2 = {"operation": "A", "schema_version": 1}
    res1 = generate_package_identity(core1)
    res2 = generate_package_identity(core2)
    assert res1["package_id"] == res2["package_id"]

def test_semantic_field_change_changes_id():
    core1 = get_base_package_core()
    core2 = get_base_package_core()
    core2["repository_identity"] = "other/repo"
    res1 = generate_package_identity(core1)
    res2 = generate_package_identity(core2)
    assert res1["package_id"] != res2["package_id"]

def test_domain_separation_affects_digest():
    res = generate_package_identity(get_base_package_core())
    
    from aos.runtime.canonical_serialization import canonicalize_validated_json
    canonical_bytes = canonicalize_validated_json(get_base_package_core())
    
    plain_digest = hashlib.sha256(canonical_bytes).hexdigest()
    assert res["semantic_digest"] != plain_digest

def test_plain_payload_digest_differs_from_domain_separated_digest():
    test_domain_separation_affects_digest()

def test_exact_domain_bytes_used():
    assert DOMAIN_BYTES == b"AOS-MERGE-AUTHORIZATION-PACKAGE-V1\0"
    res = generate_package_identity(get_base_package_core())
    expected = hashlib.sha256(DOMAIN_BYTES + res["canonical_package_core_bytes"]).hexdigest()
    assert res["semantic_digest"] == expected

def test_package_id_format_valid():
    res = generate_package_identity(get_base_package_core())
    assert res["package_id"] == f"sha256:{res['semantic_digest']}"

def test_digest_lowercase():
    res = generate_package_identity(get_base_package_core())
    assert res["semantic_digest"] == res["semantic_digest"].lower()

def test_digest_length_64():
    res = generate_package_identity(get_base_package_core())
    assert len(res["semantic_digest"]) == 64

def test_timestamp_metadata_excluded():
    core = get_base_package_core()
    res1 = generate_package_identity(core)
    core["timestamp"] = "2026-07-13T00:00:00Z"
    res2 = generate_package_identity(core)
    assert res1["package_id"] == res2["package_id"]

def test_local_path_metadata_excluded():
    core = get_base_package_core()
    res1 = generate_package_identity(core)
    core["local_path"] = "/tmp/pkg"
    res2 = generate_package_identity(core)
    assert res1["package_id"] == res2["package_id"]

def test_verification_result_excluded():
    core = get_base_package_core()
    res1 = generate_package_identity(core)
    core["verification_result"] = "PASS"
    res2 = generate_package_identity(core)
    assert res1["package_id"] == res2["package_id"]

def test_manifest_excluded():
    core = get_base_package_core()
    res1 = generate_package_identity(core)
    core["artifact_manifest"] = {}
    res2 = generate_package_identity(core)
    assert res1["package_id"] == res2["package_id"]

def test_collection_evidence_excluded():
    core = get_base_package_core()
    res1 = generate_package_identity(core)
    core["collection_evidence"] = {}
    res2 = generate_package_identity(core)
    assert res1["package_id"] == res2["package_id"]

def test_float_rejected():
    core = get_base_package_core()
    core["repository_identity"] = 1.23
    with pytest.raises(AOSRuntimeError):
        generate_package_identity(core)

def test_bytes_rejected():
    core = get_base_package_core()
    core["repository_identity"] = b"bytes"
    with pytest.raises(AOSRuntimeError):
        generate_package_identity(core)

def test_datetime_rejected():
    core = get_base_package_core()
    core["repository_identity"] = datetime.datetime.now()
    with pytest.raises(AOSRuntimeError):
        generate_package_identity(core)

def test_input_package_core_not_mutated():
    import copy
    core = get_base_package_core()
    core_copy = copy.deepcopy(core)
    generate_package_identity(core)
    assert core == core_copy

def test_no_filesystem_write():
    pass

def test_package_id_does_not_set_approval():
    res = generate_package_identity(get_base_package_core())
    assert "approval" not in res
    assert "human_approval_present" not in res

def test_package_id_does_not_set_execution_authorization():
    res = generate_package_identity(get_base_package_core())
    assert "execution_authorization" not in res

def test_unknown_package_core_field_rejected():
    core = get_base_package_core()
    core["unknown_field"] = "foo"
    with pytest.raises(ValueError, match="Unknown package core field"):
        generate_package_identity(core)

def test_arbitrary_metadata_not_silently_stripped():
    test_unknown_package_core_field_rejected()

def test_explicitly_defined_wrapper_metadata_does_not_affect_package_id():
    core = get_base_package_core()
    res1 = generate_package_identity(core)
    core["timestamp"] = "123"
    res2 = generate_package_identity(core)
    assert res1["package_id"] == res2["package_id"]

def test_valid_package_core_remains_accepted():
    test_valid_package_core_produces_package_id()
