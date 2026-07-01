# AOS-FARM.566 - Combined 564/565 Commit Authorization Package

Status: READY_FOR_COMMIT_AUTHORIZATION_REVIEW
Date: 2026-07-02

This package reviews the uncommitted AOS-FARM.564 and AOS-FARM.565 changes together.
It does not approve, stage, commit, push, merge, tag, or release anything.

## Baseline

- Branch: main
- HEAD: 992b247c87eef010c6dfd82d28b5a5b3bea0905b
- main: 992b247c87eef010c6dfd82d28b5a5b3bea0905b
- dev: 992b247c87eef010c6dfd82d28b5a5b3bea0905b
- origin/main: 992b247c87eef010c6dfd82d28b5a5b3bea0905b
- origin/dev: 992b247c87eef010c6dfd82d28b5a5b3bea0905b
- origin/main...HEAD: 0 0
- origin/main...origin/dev: 0 0
- Required fetch: PASS after scoped Git metadata escalation

## Changed Tracked Files

```text
M aos/scripts/aos_task_document_check.py
M tasks/AOS-FARM-TASK-0509.md
M tasks/AOS-FARM-TASK-0513.md
M tasks/AOS-FARM-TASK-0516.md
M tasks/AOS-FARM-TASK-0524.md
M tasks/AOS-FARM-TASK-0529.md
M tests/test_aos_task_document_check.py
```

Diff stat:

```text
aos/scripts/aos_task_document_check.py | 15 ++++++++++---
tasks/AOS-FARM-TASK-0509.md            |  2 +-
tasks/AOS-FARM-TASK-0513.md            |  4 ++--
tasks/AOS-FARM-TASK-0516.md            |  4 ++--
tasks/AOS-FARM-TASK-0524.md            |  4 ++--
tasks/AOS-FARM-TASK-0529.md            |  4 ++--
tests/test_aos_task_document_check.py  | 39 ++++++++++++++++++++++++++++++++++
7 files changed, 60 insertions(+), 12 deletions(-)
```

Forbidden path check:

```text
00_AOS_Core_Control.md: clean
01_AOS_Assembly_Pipelines_and_Build_Roadmap.md: clean
02_AOS_Governance_Control_Module_and_Safety_Rules.md: clean
.github/workflows: clean
aos/schemas: clean
aos/pipelines: clean
```

## Untracked Reports Proposed For Commit

```text
reports/aos-farm-564-active-manual-queue-lifecycle-remediation-report.md
reports/aos-farm-565-queue-next-candidate-status-semantics-fix-report.md
reports/aos-farm-566-combined-564-565-commit-authorization-package.md
```

Historical untracked reports/checkpoints remain out of scope and are not proposed for staging.

## Queue Metadata Review

The five Third Pass tasks no longer collide as active manual queue candidates:

```text
AOS-FARM-TASK-0509: queue_position=1, queue_status=DONE, approval_status=NOT_REQUESTED, commit_authorized=false, push_authorized=false
AOS-FARM-TASK-0513: queue_position=2, queue_status=DONE, approval_status=NOT_REQUESTED, commit_authorized=false, push_authorized=false
AOS-FARM-TASK-0516: queue_position=3, queue_status=DONE, approval_status=NOT_REQUESTED, commit_authorized=false, push_authorized=false
AOS-FARM-TASK-0524: queue_position=4, queue_status=DONE, approval_status=NOT_REQUESTED, commit_authorized=false, push_authorized=false
AOS-FARM-TASK-0529: queue_position=5, queue_status=DONE, approval_status=NOT_REQUESTED, commit_authorized=false, push_authorized=false
```

No `approval_status: APPROVED`, `commit_authorized: true`, or `push_authorized: true` was added.

## Queue Next Semantics

Before AOS-FARM.565, `queue --next` selected `AOS-FARM-TASK-0509` even though its queue status had been moved to `DONE`.

After AOS-FARM.565:

```text
Next task: AOS-FARM-TASK-0001
Next candidate is not approval.
Next candidate is not execution authorization.
Risk Profile must be assigned separately.
Human approval cannot be simulated.
```

Current next candidate inspection:

```text
task_id: AOS-FARM-TASK-0001
title: "Dogfood task for AOS-FARM.458"
status: DRAFT
queue_mode: AUTO
queue_position: null
queue_status: BACKLOG
risk_profile: UNKNOWN_BLOCKED
approval_status: NOT_APPROVED
```

Classification: acceptable as a backlog/next-candidate signal for queue ordering only. It is not approval, execution authorization, or risk-profile clearance.

## Validation Evidence

```text
python3 -m py_compile aos/scripts/aos_task_document_check.py
PASS
Note: initial sandbox run failed on macOS Python cache permission; rerun with scoped py_compile escalation passed.

python3 aos/scripts/aos_task_document_check.py task --validate-all
PASS: all tasks valid

python3 aos/scripts/aos_task_document_check.py queue --list
PASS: listed queue without duplicate active MANUAL queue_position failure

python3 aos/scripts/aos_task_document_check.py queue --next
PASS: returned AOS-FARM-TASK-0001 and did not return a DONE task

python3 -m unittest tests.test_aos_task_document_check.TestAOSTaskDocumentCheck.test_queue_list_readonly tests.test_aos_task_document_check.TestAOSTaskDocumentCheck.test_queue_next_readonly tests.test_aos_task_document_check.TestAOSTaskDocumentCheck.test_queue_next_skips_done_tasks
PASS: Ran 3 tests, OK

python3 -m unittest discover -s tests -p "test*.py"
PASS: Ran 72 tests, OK

git diff --check
PASS: no whitespace errors
```

Target readiness:

```text
AOS-FARM-TASK-0509: READY_FOR_HANDOFF
AOS-FARM-TASK-0513: READY_FOR_HANDOFF
AOS-FARM-TASK-0516: READY_FOR_HANDOFF
AOS-FARM-TASK-0524: READY_FOR_HANDOFF
AOS-FARM-TASK-0529: READY_FOR_HANDOFF
```

Each readiness output preserved:

```text
READY_FOR_HANDOFF is not approval
READY_FOR_HANDOFF is not READY_FOR_EXECUTION
READY_FOR_HANDOFF is not execution authorization
Commit is not authorized
Push is not authorized
```

## Review Conclusion

- AOS-FARM.564 status: READY_FOR_REVIEW
- AOS-FARM.565 status: READY_FOR_REVIEW
- AOS-FARM.566 status: READY_FOR_COMMIT_AUTHORIZATION_REVIEW

This package is not approval.
This package is not commit authorization.
This package is not push authorization.
This package is not release authorization.

PASS is not approval.
Evidence is not approval.
Readiness is not approval.
Queue PASS is not approval.
Human approval cannot be simulated.

## Proposed Commit

Suggested commit message:

```text
fix: repair manual queue lifecycle and next selection
```

Exact files proposed for staging:

```text
aos/scripts/aos_task_document_check.py
tests/test_aos_task_document_check.py
tasks/AOS-FARM-TASK-0509.md
tasks/AOS-FARM-TASK-0513.md
tasks/AOS-FARM-TASK-0516.md
tasks/AOS-FARM-TASK-0524.md
tasks/AOS-FARM-TASK-0529.md
reports/aos-farm-564-active-manual-queue-lifecycle-remediation-report.md
reports/aos-farm-565-queue-next-candidate-status-semantics-fix-report.md
reports/aos-farm-566-combined-564-565-commit-authorization-package.md
```

Do not stage historical untracked reports.
Do not commit without separate human commit authorization.
Do not push without separate human push authorization.
Do not merge, tag, or release.
