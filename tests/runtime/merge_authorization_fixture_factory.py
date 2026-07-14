import copy

def ready_repository_identity():
    return {
        "owner_name": "org",
        "repository_name": "repo",
        "repository_node_id": "R_kgDO",
        "default_branch": "main",
        "visibility": "private"
    }

def ready_pull_request():
    return {
        "number": 1,
        "state": "OPEN",
        "is_draft": False,
        "base_branch": "main",
        "head_branch": "feature",
        "base_oid": "b" * 40,
        "head_oid": "a" * 40,
        "mergeable_state": "clean",
        "allowed_merge_methods": ["merge_commit", "squash", "rebase"],
        "base_repository_identity": ready_repository_identity(),
        "head_repository_identity": ready_repository_identity()
    }

def ready_commit_state():
    return {
        "complete": True,
        "items": ["a" * 40],
        "truncated": False,
        "duplicate": False
    }

def ready_changed_paths():
    return {
        "complete": True,
        "items": ["src/main.py"],
        "incomplete": False
    }

def ready_required_checks():
    return {
        "policy_unknown": False,
        "exact_head_oid": "a" * 40,
        "items": [
            {
                "head_oid": "a" * 40,
                "state": "completed",
                "conclusion": "success"
            }
        ]
    }

def ready_reviews():
    return {
        "complete": True,
        "approval_count": 1,
        "blocking_count": 0,
        "unresolved_state": False,
        "effective_reviews": {"user1": "APPROVED"},
        "blocking_reviews": []
    }

def ready_review_threads():
    return {
        "complete": True,
        "unresolved_count": 0,
        "incomplete": False,
        "unavailable": False
    }

def ready_codeowner_state():
    return {
        "unknown": False,
        "satisfied": True,
        "unsatisfied": False
    }

def ready_ruleset_state():
    return {
        "unknown_policy": False,
        "policy_violation": False,
        "unsupported_type": False
    }

def ready_branch_protection_state():
    return {
        "unknown_policy": False,
        "policy_violation": False,
        "unsupported_type": False,
        "allowed_merge_methods": ["merge_commit"]
    }

def ready_merge_queue_state():
    return {
        "unknown": False,
        "required": False,
        "supported": False
    }

def ready_deployment_state():
    return {
        "unknown": False,
        "required": False,
        "satisfied": False
    }

def ready_collection_completeness():
    return {
        "commits_complete": True,
        "pagination_complete": True
    }

def ready_live_state():
    return {
        "repository_identity": "org/repo",
        "pull_request": ready_pull_request(),
        "commits": ready_commit_state(),
        "changed_paths": ready_changed_paths(),
        "required_checks": ready_required_checks(),
        "required_review_policy": {
            "unknown": False,
            "required_approvals": 1,
            "conversation_resolution_required": True
        },
        "reviews": ready_reviews(),
        "review_threads": ready_review_threads(),
        "codeowner_state": ready_codeowner_state(),
        "rulesets": ready_ruleset_state(),
        "branch_protection": ready_branch_protection_state(),
        "merge_queue": ready_merge_queue_state(),
        "required_deployments": ready_deployment_state(),
        "collection_completeness": ready_collection_completeness()
    }

def ready_intent():
    return {
        "schema_version": 1,
        "operation": "merge",
        "repository": "org/repo",
        "pull_request": 1,
        "merge_method": "merge_commit",
        "expected_head_oid": "a" * 40
    }

def ready_protected_path_policy():
    return {
        "normalized_paths": ["protected/core.py"]
    }

def with_head_drift():
    state = ready_live_state()
    state["pull_request"]["head_oid"] = "c" * 40
    return state

def with_base_drift():
    state = ready_live_state()
    state["pull_request"]["base_oid"] = "c" * 40
    return state

def with_failing_required_check():
    state = ready_live_state()
    state["required_checks"]["items"][0]["conclusion"] = "failure"
    return state

def with_pending_required_check():
    state = ready_live_state()
    state["required_checks"]["items"][0]["state"] = "PENDING"
    state["required_checks"]["items"][0]["conclusion"] = None
    return state

def with_unresolved_review_thread():
    state = ready_live_state()
    state["review_threads"]["unresolved_count"] = 1
    return state

def with_blocking_review():
    state = ready_live_state()
    state["reviews"]["blocking_count"] = 1
    return state

def with_unknown_ruleset():
    state = ready_live_state()
    state["rulesets"]["unknown_policy"] = True
    return state

def with_incomplete_collection():
    state = ready_live_state()
    state["collection_completeness"]["commits_complete"] = False
    return state

def with_forbidden_merge_method():
    intent = ready_intent()
    intent["merge_method"] = "squash"
    return intent

def with_extra_package_file(artifacts: dict) -> dict:
    new_arts = copy.deepcopy(artifacts)
    new_arts["extra.txt"] = b"extra"
    return new_arts
