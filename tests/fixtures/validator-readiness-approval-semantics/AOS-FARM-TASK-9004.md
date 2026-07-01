---
task_id: AOS-FARM-TASK-9004
title: "Fixture 4"
type: implementation_task
status: READY_FOR_EXECUTION
approval_status: APPROVED
risk_profile: LOW_RISK_FAST
risk_profile_proposed: LOW_RISK_FAST
risk_profile_assigned_by_human: LOW_RISK_FAST
risk_assigned_by: test_fixture
validator_status: PENDING
log_status: NOT_RUN
log_uri: .aos-tmp/tasks/AOS-FARM-TASK-9004/log.txt
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
ready_for_execution: true
execution_authorized: true
approval_granted: true
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
---

## Задача
Test fixture for semantic case: AOS-FARM-TASK-FIXTURE-04

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
# Synthetic APPROVED for testing
approval_status: APPROVED
approval_granted: true
execution_authorized: true
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
```

This is a synthetic approved fixture only. It is not a real approval. It must not be copied into real task files without explicit human approval.
