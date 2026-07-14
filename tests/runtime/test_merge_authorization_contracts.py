import pytest
from aos.runtime.merge_authorization_contracts import (
    PullRequestIdentity, PackageCore, ResultEnvelope, ContractValidationError, VerificationResult
)

def test_required_fields():
    pr = PullRequestIdentity(number=1)
    assert pr.number == 1
    with pytest.raises(ContractValidationError):
        PullRequestIdentity(number=None)

def test_unknown_fields():
    with pytest.raises(TypeError):
        PullRequestIdentity(number=1, unknown=True)

def test_allowed_semantic_types():
    with pytest.raises(ContractValidationError):
        PullRequestIdentity(number="1") 

def test_float_rejection():
    with pytest.raises(ContractValidationError, match="float"):
        ResultEnvelope(technical_status="PASS", approval_granted=False, execution_authorized=False, data={"a": 1.23}, verification_result={})

def test_bool_as_int_rejection():
    with pytest.raises(ContractValidationError, match="bool"):
        PullRequestIdentity(number=True)

def test_package_id_format():
    pass

def test_result_envelope_invariants():
    env = ResultEnvelope(technical_status="PASS", approval_granted=False, execution_authorized=False, data={}, verification_result={})
    assert env.technical_status == "PASS"
    assert env.approval_granted is False
    assert env.execution_authorized is False

def test_approval_granted_cannot_become_true_through_technical_pass():
    env = ResultEnvelope(technical_status="PASS", approval_granted=False, execution_authorized=False, data={}, verification_result={})
    assert env.approval_granted is False
    with pytest.raises(ContractValidationError):
        ResultEnvelope(technical_status="PASS", approval_granted="True", execution_authorized=False, data={}, verification_result={})
    with pytest.raises(ContractValidationError, match="approval_granted must be False"):
        ResultEnvelope(technical_status="PASS", approval_granted=True, execution_authorized=False, data={}, verification_result={})

def test_execution_authorized_cannot_be_true():
    with pytest.raises(ContractValidationError, match="execution_authorized must be False"):
        ResultEnvelope(technical_status="PASS", approval_granted=False, execution_authorized=True, data={}, verification_result={})

def test_unknown_remains_distinct_from_fail():
    env = ResultEnvelope(technical_status="UNKNOWN", approval_granted=False, execution_authorized=False, data={}, verification_result={})
    assert env.technical_status == "UNKNOWN"
    with pytest.raises(ContractValidationError):
        ResultEnvelope(technical_status="INVALID", approval_granted=False, execution_authorized=False, data={}, verification_result={})

def test_not_run_remains_distinct_from_pass():
    env = ResultEnvelope(technical_status="NOT_RUN", approval_granted=False, execution_authorized=False, data={}, verification_result={})
    assert env.technical_status == "NOT_RUN"
