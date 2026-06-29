---
task_id: "AOS-FARM-TASK-9004"
title: "Test Task"
type: "task"
template_level: "S"
status: "READY_FOR_EXECUTION"
queue_mode: "AUTO"
queue_position: null
queue_status: "NEXT"
queue_priority: "NORMAL"
risk_profile: "LOW_RISK_FAST"
risk_assigned_by: "human"
approval_status: "APPROVED"
human_checkpoint_required: true
validator_status: "VALIDATED"
evidence_status: "COLLECTED"
log_uri: ".aos-tmp/tasks/AOS-FARM-TASK-9004/agent-actions.log"
log_status: "IN_PROGRESS"
owner: "human"
created_at: "2026-06-29T04:33:59.443857+00:00"
updated_at: "2026-06-29T04:33:59.443857+00:00"
---
## Задача
Test
## Done когда
Test
## История
Test
## Evidence
Test
## ⛔ Решение
APPROVED
AOS-FARM Controlled Task Handoff Prompt

## Handoff Result
handoff_result:
  result_status: REPORTED
  reported_changed_files:
    - path: foo.py
  validation_results:
    status: PASS
    evidence: check passed
  stop_condition:
    status: STOPPED
    reason: human review
  authorization_claims:
    approval_claimed: false
    ready_for_execution_claimed: true
    commit_performed: false
    push_performed: false
