# AOS-FARM.607 - Lifecycle State Reconciliation Final Report

## 1. Baseline Summary

Baseline status:

```text
AOS-FARM.607 BASELINE STATUS: UNKNOWN_BLOCKED
```

Confirmed baseline conflict:
- queue helper selected `AOS-FARM-TASK-060101`.
- dashboard and validator embedded dashboard surfaced `AOS-FARM-TASK-0509`.
- `AOS-FARM-TASK-0509` has `queue_status: DONE`.
- `AOS-FARM-TASK-060101` is `DRAFT` / `BACKLOG` with `risk_profile: UNKNOWN_BLOCKED`.
- `/.aos-tmp/write_report.py` was flagged as Source-of-Truth boundary risk.
- execution, approval, commit, push, and release remained forbidden.

## 2. Files Changed

Documentation:
- `aos/docs/workflow/lifecycle-state-reconciliation.md`
- `aos/docs/workflow/task-candidate-to-task-conversion.md`
- `aos/docs/workflow/review-package-output-policy.md`

Scripts:
- `aos/scripts/aos_lifecycle_state.py`
- `aos/scripts/aos_task_document_check.py`
- `aos/scripts/aos_queue_dashboard.py`
- `aos/scripts/aos_next_task_selection.py`
- `aos/scripts/aos_validate.py`
- `aos/scripts/aos_review_package.py`

Tests and fixtures:
- `tests/test_aos_lifecycle_state.py`
- `tests/test_aos_lifecycle_reconciliation.py`
- `tests/test_aos_review_package.py`
- `tests/fixtures/lifecycle-state/done-ranked-first.md`
- `tests/fixtures/lifecycle-state/draft-unknown-candidate.md`
- `tests/fixtures/lifecycle-state/evidence-present-not-approved.md`

Reports:
- `reports/aos-farm-607-lifecycle-state-reconciliation-dogfood-report.md`
- `reports/aos-farm-607-lifecycle-state-reconciliation-final-report.md`

## 3. Commands Run

Required sources were read in order:
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

Validation commands run with `PYTHONPYCACHEPREFIX=/private/tmp/aos-farm-pycache-audit`:
- `python3 -m py_compile aos/scripts/aos_lifecycle_state.py`
- `python3 -m py_compile aos/scripts/aos_task_document_check.py`
- `python3 -m py_compile aos/scripts/aos_queue_dashboard.py`
- `python3 -m py_compile aos/scripts/aos_next_task_selection.py`
- `python3 -m py_compile aos/scripts/aos_review_package.py`
- `python3 aos/scripts/aos_task_document_check.py task --validate-all`
- `python3 aos/scripts/aos_task_document_check.py queue --list`
- `python3 aos/scripts/aos_task_document_check.py queue --next`
- `python3 aos/scripts/aos_validate.py all`
- `python3 -m unittest discover -s tests`
- `python3 aos/scripts/aos_lifecycle_state.py --json`
- `python3 aos/scripts/aos_lifecycle_state.py --text`
- `python3 aos/scripts/aos_lifecycle_state.py --task tasks/AOS-FARM-TASK-060101.md --json`
- `python3 aos/scripts/aos_lifecycle_state.py --explain`
- `python3 aos/scripts/aos_lifecycle_state.py --check-consistency`

Candidate checker commands were not run because no candidate checker script was added.

## 4. Commands NOT_RUN And Why

NOT_RUN:
- `python3 -m py_compile aos/scripts/aos_candidate_conversion_check.py`
- `python3 aos/scripts/aos_candidate_conversion_check.py tasks/AOS-FARM-TASK-060101.md --json`
- `python3 aos/scripts/aos_candidate_conversion_check.py tasks/AOS-FARM-TASK-060101.md --text`

Reason:
- Candidate checker was optional and was deferred to avoid expanding the stage beyond the documentation checklist requirement.

## 5. Validation Output Summary

Required validation was run with `PYTHONPYCACHEPREFIX=/private/tmp/aos-farm-pycache-audit`.

Compile checks:
- `aos/scripts/aos_lifecycle_state.py`: PASS
- `aos/scripts/aos_task_document_check.py`: PASS
- `aos/scripts/aos_queue_dashboard.py`: PASS
- `aos/scripts/aos_next_task_selection.py`: PASS
- `aos/scripts/aos_review_package.py`: PASS

Lifecycle CLI live repo output:
- selected task: `AOS-FARM-TASK-060101`
- lifecycle state: `DRAFT`
- next safe action: `HUMAN_REVIEW_REQUIRED`
- execution allowed: false
- approval granted: false
- commit allowed: false
- push allowed: false

Expected fail-closed validation:
- `aos_validate.py all` completed with `Overall Status: UNKNOWN_BLOCKED`.
- This is acceptable only as truthful blocked status, not PASS.

Full tests:
- `python3 -m unittest discover -s tests`: PASS, 140 tests.

## 6. New Lifecycle Reconciler Behavior

New script:

```text
aos/scripts/aos_lifecycle_state.py
```

Supported commands:
- `python3 aos/scripts/aos_lifecycle_state.py --json`
- `python3 aos/scripts/aos_lifecycle_state.py --text`
- `python3 aos/scripts/aos_lifecycle_state.py --task tasks/AOS-FARM-TASK-060101.md --json`
- `python3 aos/scripts/aos_lifecycle_state.py --explain`
- `python3 aos/scripts/aos_lifecycle_state.py --check-consistency`

Behavior:
- reads task files and derived queue signals
- selects the first ranked eligible task
- skips `DONE` tasks as non-candidates
- reports blockers and unknowns
- defaults permission flags to false
- does not write files
- does not mutate lifecycle state
- does not create Evidence
- does not approve

## 7. Queue/Dashboard Reconciliation Result

Queue/dashboard disagreement is resolved by using the same candidate boundary:
- `queue --next` selects `AOS-FARM-TASK-060101`.
- dashboard selects `AOS-FARM-TASK-060101`.
- next-task reconciliation selects `AOS-FARM-TASK-060101`.
- Lifecycle Reconciler selects `AOS-FARM-TASK-060101`.

The reconciler still reports that `AOS-FARM-TASK-0509` is ranked first but skipped because `queue_status` is `DONE`.

## 8. Candidate Conversion Boundary Result

Created:

```text
aos/docs/workflow/task-candidate-to-task-conversion.md
```

It defines:
- required checklist fields
- allowed outputs: `READY_FOR_HUMAN_REVIEW`, `BLOCKED`, `UNKNOWN_BLOCKED`
- forbidden outputs: `READY_FOR_EXECUTION`, `APPROVED`, `LOW_RISK_FAST`, commit/push/release authorization
- default false permission flags
- human Risk Profile boundary

Optional candidate checker script was not added.

## 9. .aos-tmp Classification

`/.aos-tmp/` remains:
- local-only
- ignored by git
- disposable
- not Source of Truth
- not Evidence storage
- not approval storage
- not checkpoint storage

Known risk:
- pre-existing `/.aos-tmp/write_report.py` remains classified as Source-of-Truth boundary risk by self-test.

No AOS-FARM.607 reports, Evidence, or checkpoints were written into `/.aos-tmp/`.

Cleanup was not authorized and was not performed.

## 10. Known Limitations

- Lifecycle Reconciler is a read-only interpreter, not runtime enforcement.
- Candidate conversion has documentation checklist coverage only; no candidate checker script was added.
- `aos_validate.py all` can remain `UNKNOWN_BLOCKED` due to pre-existing blocked task states.
- `/.aos-tmp/write_report.py` remains unresolved because cleanup was forbidden.
- No lifecycle state was mutated to resolve `AOS-FARM-TASK-060101` blockers.

## 11. Remaining UNKNOWN_BLOCKED

Remaining blocked state:
- `AOS-FARM-TASK-060101` has `risk_profile: UNKNOWN_BLOCKED`.
- `AOS-FARM-TASK-060101` has `validator_status: NOT_RUN`.
- `AOS-FARM-TASK-060101` has `evidence_status: NOT_RUN`.
- `AOS-FARM-TASK-060101` has no execution authorization.
- broader validation may remain `UNKNOWN_BLOCKED`.
- `.aos-tmp` boundary risk remains.

## 12. Human Decisions Required

Still required:
- human review of AOS-FARM.607 implementation
- decision whether to authorize commit
- decision whether to authorize push
- decision whether to authorize any later cleanup of `.aos-tmp`
- separate human Risk Profile / execution authorization for `AOS-FARM-TASK-060101` if that task is to proceed

## 13. Commit Authorization Status

Commit authorization: NOT_GRANTED.

No commit was made.

## 14. Push Authorization Status

Push authorization: NOT_GRANTED.

No push was made.

## 15. Release Authorization Status

Release authorization: NOT_GRANTED.

No merge or release was made.

## 16. Final Status

READY_FOR_HUMAN_REVIEW

This status is an implementation handoff status only. It is not approval and does not authorize commit, push, release, or next-task execution.
