from aos.runtime.fixed_safety_policy import get_fixed_safety_policy, validate_against_fixed_policy

def test_required_prohibitions_present():
    policy = get_fixed_safety_policy()
    assert "admin_bypass" in policy["forbidden_actions"]
    assert "force_push" in policy["forbidden_actions"]
    assert "release" in policy["forbidden_actions"]
    assert "method_substitution" in policy["forbidden_actions"]

def test_stable_version():
    policy = get_fixed_safety_policy()
    assert policy["version"] == 1

def test_human_data_cannot_remove_prohibition():
    assert validate_against_fixed_policy(["admin_bypass"]) is False
    assert validate_against_fixed_policy(["force_push"]) is False
    assert validate_against_fixed_policy(["normal_merge"]) is True

def test_returned_policy_cannot_mutate_global_constant():
    policy = get_fixed_safety_policy()
    policy["forbidden_actions"].remove("admin_bypass")
    
    policy2 = get_fixed_safety_policy()
    assert "admin_bypass" in policy2["forbidden_actions"]
