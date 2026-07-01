import re
import os

fixtures = [
    ("tests/fixtures/validator-readiness-approval-semantics/ready_for_execution_without_approval_is_valid_readiness.md",
     "AOS-FARM-TASK-FIXTURE-01", "Fixture 1", "READY_FOR_EXECUTION", "NOT_REQUESTED", True, True, False),
    ("tests/fixtures/validator-readiness-approval-semantics/rejected_approval_blocks_readiness.md",
     "AOS-FARM-TASK-FIXTURE-02", "Fixture 2", "READY_FOR_EXECUTION", "REJECTED", True, True, False),
    ("tests/fixtures/validator-readiness-approval-semantics/execution_not_authorized_blocks_readiness.md",
     "AOS-FARM-TASK-FIXTURE-03", "Fixture 3", "READY_FOR_EXECUTION", "NOT_REQUESTED", True, False, False),
    ("tests/fixtures/validator-readiness-approval-semantics/approved_task_still_requires_explicit_approval_fields.md",
     "AOS-FARM-TASK-FIXTURE-04", "Fixture 4", "READY_FOR_EXECUTION", "APPROVED", True, True, True)
]

for filepath, task_id, title, status, approval, ready_exec, exec_auth, app_granted in fixtures:
    content = f"""---
task_id: {task_id}
title: "{title}"
type: implementation_task
status: {status}
approval_status: {approval}
risk_profile: LOW_RISK_FAST
risk_profile_proposed: LOW_RISK_FAST
risk_profile_assigned_by_human: LOW_RISK_FAST
risk_assigned_by: test_fixture
validator_status: PENDING
log_status: NOT_RUN
log_uri: .aos-tmp/fixtures/validator-readiness-approval-semantics/{os.path.basename(filepath)}.log
template_level: task
owner: test_fixture
queue_position: 1
queue_mode: MANUAL
queue_priority: NORMAL
queue_status: IN_PROGRESS
human_checkpoint_required: false
created_at: null
updated_at: null
evidence_status: PENDING
ready_for_execution: {'true' if ready_exec else 'false'}
execution_authorized: {'true' if exec_auth else 'false'}
approval_granted: {'true' if app_granted else 'false'}
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
---

## Задача
Test fixture for semantic case: {task_id}

## Context
This is a synthetic fixture. It is test-only.

## Problem
Protects the validator semantics for readiness and approval decoupling.

## Scope
Focused readiness/approval semantic fixture only.

## Risk
Synthetic fixture only; not real task authorization. Synthetic Risk Profile values are test-only. This fixture does not authorize an agent to assign LOW_RISK_FAST in real tasks.

## Non-goals
No real approval, no commit/push/release authorization.

## Done когда
Fixture produces expected readiness outcome.

## Evidence
Fixture file plus validator output only. log_uri is local-only scratch pointer, not Evidence and not Source of Truth. .aos-tmp is disposable and not Source of Truth.
Evidence is not approval. Validator PASS is not approval. READY_FOR_EXECUTION is not approval.

## История
Created in 531, updated in 538 for schema completion.

## ⛔ Решение
```yaml
decision_status: READY_FOR_HUMAN_REVIEW
approval_granted: {'true' if app_granted else 'false'}
execution_authorized: {'true' if exec_auth else 'false'}
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
```
"""
    if app_granted:
        content += "\nThis is a synthetic approved fixture only. It is not a real approval. It must not be copied into real task files without explicit human approval.\n"
    
    with open(filepath, "w") as f:
        f.write(content)
