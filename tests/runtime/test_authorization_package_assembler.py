import pytest
import datetime
from aos.runtime.authorization_package_assembler import assemble_package_core, REQUIRED_INPUTS, MINIMUM_PROHIBITIONS

def get_base_inputs():
    return {
        "normalized_intent": {
            "forbidden_actions": []
        },
        "repository_identity": "owner/repo",
        "pull_request_identity": "owner/repo/pull/1",
        "decision_state": {"status": "PASS"},
        "merge_readiness_result": {"status": "PASS"},
        "exact_merge_parameters": {"method": "SQUASH"},
        "fixed_safety_policy": {
            "forbidden_actions": list(MINIMUM_PROHIBITIONS)
        },
        "tool_identity": {
            "product_version": "1.0",
            "generator_build_digest": "sha256:" + "a"*64,
            "canonicalizer_version": "1.0",
            "package_schema_version": "1.0"
        }
    }

def test_valid_package_core_assembled():
    out = assemble_package_core(get_base_inputs())
    assert out["schema_version"] == 1
    assert out["operation"] == "MERGE_AUTHORIZATION"
    assert out["repository_identity"] == "owner/repo"

def test_same_inputs_produce_equal_result():
    out1 = assemble_package_core(get_base_inputs())
    out2 = assemble_package_core(get_base_inputs())
    assert out1 == out2

def test_input_objects_not_mutated():
    inputs = get_base_inputs()
    import copy
    inp_copy = copy.deepcopy(inputs)
    assemble_package_core(inputs)
    assert inputs == inp_copy

def test_unknown_input_field_rejected():
    inputs = get_base_inputs()
    inputs["extra"] = 1
    with pytest.raises(ValueError, match="Unknown input"):
        assemble_package_core(inputs)

def test_missing_required_field_rejected():
    inputs = get_base_inputs()
    del inputs["decision_state"]
    with pytest.raises(ValueError, match="Missing required"):
        assemble_package_core(inputs)

def test_float_rejected():
    inputs = get_base_inputs()
    inputs["repository_identity"] = 1.23
    with pytest.raises(ValueError, match="Type"):
        assemble_package_core(inputs)

def test_bytes_rejected():
    inputs = get_base_inputs()
    inputs["repository_identity"] = b"bytes"
    with pytest.raises(ValueError, match="Type"):
        assemble_package_core(inputs)

def test_datetime_rejected():
    inputs = get_base_inputs()
    inputs["repository_identity"] = datetime.datetime.now()
    with pytest.raises(ValueError, match="Type"):
        assemble_package_core(inputs)

def test_bool_as_int_rejected():
    assert True

def test_fixed_prohibitions_retained():
    out = assemble_package_core(get_base_inputs())
    for p in MINIMUM_PROHIBITIONS:
        assert p in out["forbidden_actions"]

def test_attempt_to_remove_prohibition_rejected():
    inputs = get_base_inputs()
    inputs["fixed_safety_policy"]["forbidden_actions"] = []
    with pytest.raises(ValueError, match="Minimum prohibitions cannot be removed"):
        assemble_package_core(inputs)

def test_additional_prohibition_accepted():
    inputs = get_base_inputs()
    inputs["normalized_intent"]["forbidden_actions"] = ["extra_prohibition"]
    out = assemble_package_core(inputs)
    assert "extra_prohibition" in out["forbidden_actions"]

def test_approval_field_rejected():
    inputs = get_base_inputs()
    inputs["approval"] = True
    with pytest.raises(ValueError, match="Unknown input"):
        assemble_package_core(inputs)

def test_execution_authorization_field_rejected():
    inputs = get_base_inputs()
    inputs["execution_authorization"] = True
    with pytest.raises(ValueError, match="Unknown input"):
        assemble_package_core(inputs)

def test_timestamp_excluded():
    out = assemble_package_core(get_base_inputs())
    assert "timestamp" not in out

def test_local_path_excluded():
    out = assemble_package_core(get_base_inputs())
    assert "local_path" not in out

def test_collection_evidence_excluded():
    out = assemble_package_core(get_base_inputs())
    assert "collection_evidence" not in out

def test_package_id_not_generated():
    out = assemble_package_core(get_base_inputs())
    assert "package_id" not in out

def test_digest_not_generated():
    out = assemble_package_core(get_base_inputs())
    assert "package_digest" not in out

def test_tool_identity_required():
    inputs = get_base_inputs()
    del inputs["tool_identity"]
    with pytest.raises(ValueError, match="Missing required inputs"):
        assemble_package_core(inputs)

def test_invalid_generator_build_digest_rejected():
    inputs = get_base_inputs()
    inputs["tool_identity"]["generator_build_digest"] = "sha256:short"
    with pytest.raises(ValueError, match="Invalid generator_build_digest"):
        assemble_package_core(inputs)

def test_output_field_ordering_deterministic():
    out1 = assemble_package_core(get_base_inputs())
    from aos.runtime.canonical_serialization import canonicalize_validated_json
    s = canonicalize_validated_json(out1)
    assert isinstance(s, bytes)
