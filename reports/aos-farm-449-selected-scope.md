# AOS-FARM.449 — Selected Scope

```yaml
document_type: selected_scope
task_id: AOS-FARM.449
task_title: Task Registry / Queue Helper Hardening
branch: build/task-registry-queue-helper-hardening
base_branch: dev
base_commit: fac85dbd54c878aed8466a2bdffa8cf10a8181c8
risk_profile_assigned_by_human: true
risk_profile: MEDIUM_RISK_GUIDED
execution_authorized: true
commit_authorized: false
push_authorized: false
release_authorized: false
created_at: "2026-06-28"
```

## Goal

Harden the Task Registry / Queue helper layer so the user and agent can clearly
see:

- current task
- next candidate
- blocked tasks
- done tasks
- invalid transitions
- human action required
- whether execution, commit, and push are authorized

This stage prepares the project for the first real controlled code task later,
but must not start AOS-FARM.450.

## In-Scope Files

| File | Action |
|---|---|
| `aos/scripts/aos_task_queue_helper.py` | CREATE — new hardened CLI helper |
| `aos/tools/optional/task_registry_validator.py` | HARDEN — add missing invariant checks |
| `tests/fixtures/task_queue_valid.yaml` | CREATE |
| `tests/fixtures/task_queue_invalid_candidate_as_approved.yaml` | CREATE |
| `tests/fixtures/task_queue_invalid_transition.yaml` | CREATE |
| `tests/fixtures/task_queue_missing_human_authorization.yaml` | CREATE |
| `tests/test_aos_task_queue_helper.py` | CREATE |
| `reports/aos-farm-449-selected-scope.md` | CREATE (this file) |
| `reports/aos-farm-449-controlled-task-brief.md` | CREATE |
| `reports/aos-farm-449-human-execution-authorization-record.md` | CREATE |
| `reports/aos-farm-449-changed-files.yaml` | CREATE |
| `reports/aos-farm-449-execution-report.md` | CREATE |
| `reports/aos-farm-449-evidence-report.md` | CREATE |
| `reports/aos-farm-449-evidence-review.md` | CREATE |
| `reports/aos-farm-449-lessons-learned.md` | CREATE |
| `reports/aos-farm-449-next-task-candidate.md` | CREATE |
| `reports/aos-farm-449-final-closure-report.md` | CREATE |

## Out-of-Scope (Forbidden) Files

- `00_AOS_Core_Control.md` — protected/canonical
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` — protected/canonical
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md` — protected/canonical
- Any file outside the above In-Scope list
- `/.aos-tmp/` — must not store Evidence, reports, or canonical files there

## Pre-Existing Untracked Files (Out-of-Scope)

A large set of pre-existing untracked files with `" 2.md"` suffix and other
historical reports were observed at baseline. These are **not touched** by this
task. They are recorded as out-of-scope pre-existing state.

## AOS Invariants in Force

```text
PASS ≠ approval
Evidence ≠ approval
CI PASS ≠ approval
UNKNOWN ≠ OK
NOT_RUN ≠ PASS
Human approval cannot be simulated
Queue position ≠ approval
Next Task Candidate ≠ approved task
Risk Profile must not be self-assigned by agent
Commit authorization ≠ push authorization
Push authorization ≠ release authorization
```
