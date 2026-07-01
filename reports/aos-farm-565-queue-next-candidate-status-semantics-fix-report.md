# AOS-FARM.565 Queue Next Candidate Status Semantics Fix Report

## Status

```yaml
stage: AOS-FARM.565
status: READY_FOR_REVIEW
risk_profile: MEDIUM_RISK_GUIDED
baseline_commit: 992b247c87eef010c6dfd82d28b5a5b3bea0905b
branch: main
aos_farm_564_state: still_uncommitted_in_working_tree
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
```

## Scope

This stage fixed only queue next-candidate selection semantics in:

- `aos/scripts/aos_task_document_check.py`
- `tests/test_aos_task_document_check.py`

This stage preserved the uncommitted AOS-FARM.564 task metadata remediation and did not edit task queue metadata further.

No changes were made to:

- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
- schemas
- workflows
- unrelated validator behavior
- runtime/product files outside the queue helper

No historical reports were cleaned or archived. No commit, push, merge, tag, or release was performed.

## Baseline

```text
git branch --show-current: main
HEAD: 992b247c87eef010c6dfd82d28b5a5b3bea0905b
main: 992b247c87eef010c6dfd82d28b5a5b3bea0905b
dev: 992b247c87eef010c6dfd82d28b5a5b3bea0905b
origin/main: 992b247c87eef010c6dfd82d28b5a5b3bea0905b
origin/dev: 992b247c87eef010c6dfd82d28b5a5b3bea0905b
origin/main...HEAD: 0 0
origin/main...origin/dev: 0 0
```

`git fetch origin` initially hit the known `.git/FETCH_HEAD` metadata permission boundary and was rerun as the same command with elevated Git metadata access.

## Before Behavior

Before this fix, after AOS-FARM.564:

```text
python3 aos/scripts/aos_task_document_check.py queue --next
Next task: AOS-FARM-TASK-0509
Next candidate is not approval.
Next candidate is not execution authorization.
Risk Profile must be assigned separately.
Human approval cannot be simulated.
```

This was semantically wrong because `AOS-FARM-TASK-0509` had `queue_status: DONE`.

## Change

Added explicit next-candidate filtering:

```python
NEXT_CANDIDATE_QUEUE_STATUSES = {"BACKLOG", "NEXT", "IN_PROGRESS"}
NON_NEXT_LIFECYCLE_STATUSES = {"BLOCKED", "CLOSED", "REJECTED"}
```

`queue --list` still lists all non-`CLOSED` queue entries. `queue --next` now filters the ranked queue and selects only eligible next candidates.

Excluded from next-candidate selection:

- `queue_status: DONE`
- `queue_status: BLOCKED`
- lifecycle `status: BLOCKED`
- lifecycle `status: CLOSED`
- lifecycle `status: REJECTED`

No new queue status vocabulary was added.

## Test Coverage

Added focused test:

```text
TestAOSTaskDocumentCheck.test_queue_next_skips_done_tasks
```

The test uses an isolated temporary `tasks/` directory and verifies:

- a `DONE` task is not selected by `queue --next`;
- the next eligible backlog task is selected instead;
- existing queue readonly tests remain intact.

## After Behavior

```text
python3 aos/scripts/aos_task_document_check.py queue --next
Next task: AOS-FARM-TASK-0001
Next candidate is not approval.
Next candidate is not execution authorization.
Risk Profile must be assigned separately.
Human approval cannot be simulated.
```

`queue --next` no longer returns DONE tasks.

## Validation Evidence

```text
python3 -m py_compile aos/scripts/aos_task_document_check.py
PASS
```

```text
python3 aos/scripts/aos_task_document_check.py task --validate-all
PASS: all tasks valid
```

```text
python3 aos/scripts/aos_task_document_check.py queue --list
Queue list complete. No files written.
```

```text
python3 aos/scripts/aos_task_document_check.py queue --next
Next task: AOS-FARM-TASK-0001
Next candidate is not approval.
Next candidate is not execution authorization.
Risk Profile must be assigned separately.
Human approval cannot be simulated.
```

```text
python3 -m unittest tests.test_aos_task_document_check.TestAOSTaskDocumentCheck.test_queue_list_readonly tests.test_aos_task_document_check.TestAOSTaskDocumentCheck.test_queue_next_readonly tests.test_aos_task_document_check.TestAOSTaskDocumentCheck.test_queue_next_skips_done_tasks
Ran 3 tests in 0.090s
OK
```

```text
python3 -m unittest discover -s tests -p "test*.py"
Ran 72 tests in 1.370s
OK
```

Target task readiness remained consistent:

```text
AOS-FARM-TASK-0509: READY_FOR_HANDOFF
AOS-FARM-TASK-0513: READY_FOR_HANDOFF
AOS-FARM-TASK-0516: READY_FOR_HANDOFF
AOS-FARM-TASK-0524: READY_FOR_HANDOFF
AOS-FARM-TASK-0529: READY_FOR_HANDOFF
```

Each readiness output preserved:

```text
READY_FOR_HANDOFF is not approval.
READY_FOR_HANDOFF is not READY_FOR_EXECUTION.
READY_FOR_HANDOFF is not execution authorization.
Commit is not authorized.
Push is not authorized.
```

## Files Changed

AOS-FARM.565 changed:

- `aos/scripts/aos_task_document_check.py`
- `tests/test_aos_task_document_check.py`
- `reports/aos-farm-565-queue-next-candidate-status-semantics-fix-report.md`

Preserved from uncommitted AOS-FARM.564:

- `tasks/AOS-FARM-TASK-0509.md`
- `tasks/AOS-FARM-TASK-0513.md`
- `tasks/AOS-FARM-TASK-0516.md`
- `tasks/AOS-FARM-TASK-0524.md`
- `tasks/AOS-FARM-TASK-0529.md`
- `reports/aos-farm-564-active-manual-queue-lifecycle-remediation-report.md`

## Final Boundaries

- PASS is not approval.
- Evidence is not approval.
- Readiness is not approval.
- Queue PASS is not approval.
- Queue next selection is not execution authorization.
- Commit is not authorized.
- Push is not authorized.
- Merge is not authorized.
- Release is not authorized.
- Human review remains required before commit authorization.

## Final Status

```yaml
AOS_FARM_565_STATUS: READY_FOR_REVIEW
approved: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
```
