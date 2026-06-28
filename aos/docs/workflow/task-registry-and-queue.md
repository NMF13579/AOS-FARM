# AOS-FARM Task Registry and Queue Contract

## 1. Core Principles
- The Task Registry and Task Queue act as read-only Source of Truth inputs for verification and planning.
- **Canonical Model:** The YAML Task Registry and YAML Task Queue are the canonical structural source of truth.
- **Projection View:** The Markdown table queue is a human-readable projection and compatibility view only.
- They must not automatically execute code or mutate repository lifecycle state.
- **Queue position is not approval.**
- **show-current is not execution.**
- **show-next is not execution.**

## 2. Read-Only Constraint
- The CLI script (`aos_tasks.py`) and validator (`task_registry_validator.py`) are STRICTLY read-only tools.
- They MUST NOT write files, create commits, execute tasks, assign risk profiles, or mutate lifecycle states.

## 3. Purpose
Create a safe task-management control layer for AOS-FARM:
1. Task Registry — state of all known tasks.
2. Task Queue — ordered execution queue.
3. Workflow / State Machine — allowed and forbidden lifecycle transitions.
4. Automation / Validators — read-only validation, summary, show-current, show-next.

## 4. Source of Truth
- markdown_yaml_registry_queue: Source of Truth
- sqlite: future_derived_index_only
- rag_light: future_navigation_search_summary_only

Если future SQLite/RAG-light противоречит Markdown/YAML:
- winner: canonical_markdown_yaml
- derived_index_status: STALE_OR_INVALID
- final_status: HUMAN_REVIEW_REQUIRED

## 3. Task Registry
Registry may report task state.
Task ID is stable.

## 4. Task Queue
Queue may report current/next task.
Queue item ID is stable.

## 5. Stable identity rules
- Semantic title is never a task identifier.
- Task ID is stable.
- Queue item ID is stable.
- Queue order is not identity.

## 6. Queue revision rules
- Queue order changes require a new queue_revision.

## 7. Task lifecycle / state machine
registry_status_values:
  - CANDIDATE
  - QUEUED
  - SELECTED
  - TASK_BRIEF_DRAFT
  - WAITING_RISK_PROFILE
  - READY_FOR_EXECUTION
  - IN_PROGRESS
  - HUMAN_REVIEW_REQUIRED
  - BLOCKED
  - DEFERRED
  - REJECTED
  - REPLACED
  - CLOSED

## 8. Allowed transitions
- CANDIDATE → QUEUED
- QUEUED → SELECTED
- SELECTED → TASK_BRIEF_DRAFT
- TASK_BRIEF_DRAFT → WAITING_RISK_PROFILE
- WAITING_RISK_PROFILE → READY_FOR_EXECUTION
- READY_FOR_EXECUTION → IN_PROGRESS
- IN_PROGRESS → HUMAN_REVIEW_REQUIRED
- HUMAN_REVIEW_REQUIRED → CLOSED
- HUMAN_REVIEW_REQUIRED → BLOCKED
- HUMAN_REVIEW_REQUIRED → DEFERRED
- HUMAN_REVIEW_REQUIRED → REPLACED

## 9. Forbidden transitions
- CANDIDATE → IN_PROGRESS
- QUEUED → CLOSED
- PASS → APPROVED
- Evidence → approval
- READY_FOR_EXECUTION without human Risk Profile
- READY_FOR_EXECUTION without execution_authorized: true
- BLOCKED → IN_PROGRESS without unblock rule
- DEFERRED → SELECTED without explicit reactivation
- REPLACED → SELECTED
- CLOSED → IN_PROGRESS

## 10. Blocking / deferring / replacing tasks
Tasks can transition to BLOCKED, DEFERRED, or REPLACED from HUMAN_REVIEW_REQUIRED.

## 11. Summary counters
Registry and Queue will implement summary counters to track active and finished task counts.

## 12. Current task and next task selection
Queue may report current/next task based on queue order.
- CLOSED tasks are not selected.
- BLOCKED tasks are not selected.
- DEFERRED tasks are not selected unless explicitly reactivated.
- REPLACED tasks are not selected.
- show-next selects the first eligible task by queue_order.
- show-next reports selection but does not approve execution.

## 13. Approval and execution boundary
- PASS ≠ approval
- Evidence ≠ approval
- CI PASS ≠ approval
- UNKNOWN ≠ OK
- NOT_RUN ≠ PASS
- Human approval cannot be simulated
- Risk Profile assignment is human-only

READY_FOR_EXECUTION rule:
READY_FOR_EXECUTION требует:
risk_profile_assigned_by_human: true
risk_profile: not_null
execution_authorized: true
Иначе:
final_status: HUMAN_REVIEW_REQUIRED
или:
final_status: BLOCKED

## 14. Validator and CLI boundary
- Validator may block invalid state.
- CLI may inspect state.
- Registry/Queue/Validator/CLI must not approve, authorize, execute, commit, or push.

## 15. Future SQLite / RAG-light compatibility
future_sqlite_rag_light_design_considered: true
future_sqlite_may_read: true
future_sqlite_may_index: true
future_sqlite_may_cache: true
future_sqlite_may_report: true
future_sqlite_may_decide: false
future_sqlite_may_approve: false
future_sqlite_may_execute: false
future_sqlite_may_mutate_source_of_truth: false
future_rag_light_may_search: true
future_rag_light_may_summarize: true
future_rag_light_may_link_to_sources: true
future_rag_light_may_report_known_state: true
future_rag_light_may_approve: false
future_rag_light_may_execute: false
future_rag_light_may_assign_risk_profile: false
future_rag_light_may_mutate_lifecycle: false

## 16. Minimal examples
Templates/examples must include the following fields:
```yaml
schema_version: 1
task_id: AOS-FARM.442
queue_item_id: AOS-FARM.QUEUE.2026-06-27-01.001
queue_revision: 2026-06-27-01
queue_order: "001"
source_file: null
source_commit: null
source_hash: null
indexed_at: null
registry_status: QUEUED
lifecycle_stage: CANDIDATE
task_brief_status: NOT_CREATED
depends_on:
  - AOS-FARM.441
blocked_by: []
replaces: []
replaced_by: null
risk_profile_assigned_by_human: false
risk_profile: null
execution_authorized: false
commit_authorized: false
push_authorized: false
next_action: PREPARE_TASK_BRIEF
final_status: HUMAN_REVIEW_REQUIRED
```

## 17. Non-goals
No approval semantics or execution capabilities built directly into the Registry or Queue documents themselves.
