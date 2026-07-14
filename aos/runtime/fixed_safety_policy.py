FIXED_SAFETY_POLICY_VERSION = 1

FIXED_PROHIBITIONS = (
    "admin_bypass",
    "force_push",
    "branch_deletion",
    "release",
    "different_repository",
    "different_pull_request",
    "different_base_oid",
    "different_head_oid",
    "different_commit_set",
    "method_substitution"
)

def get_fixed_safety_policy() -> dict:
    return {
        "version": FIXED_SAFETY_POLICY_VERSION,
        "forbidden_actions": list(FIXED_PROHIBITIONS)
    }

def validate_against_fixed_policy(proposed_actions: list) -> bool:
    for action in proposed_actions:
        if action in FIXED_PROHIBITIONS:
            return False
    return True
