# AOS-FARM.523 — Readiness vs Approval Validator Semantics Conflict Review

```yaml
report_id: AOS-FARM.523
report_type: readiness_vs_approval_validator_semantics_conflict_review
status: READY_FOR_HUMAN_REVIEW
source_reports:
  - reports/aos-farm-521-third-pass-report-only-package-closure-rereview.md
  - reports/aos-farm-522-task-canonical-schema-completion-report.md
target_validator: aos/scripts/aos_task_document_check.py
target_tasks:
  - tasks/AOS-FARM-TASK-0509.md
  - tasks/AOS-FARM-TASK-0513.md
  - tasks/AOS-FARM-TASK-0516.md
approval_granted: false
execution_authorized: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
```

## Summary
The AOS-FARM.523 Conflict Review investigated the impasse identified in AOS-FARM.522. The `aos_task_document_check.py` tool strictly couples `READY_FOR_EXECUTION` with `approval_status: APPROVED`. However, canonical AOS-FARM governance strongly separates execution readiness from approval. Applying `APPROVED` to unapproved tasks to pass validation would violate the foundational invariants against simulating or falsifying human approval. This report catalogs the conflict and provides safe options for a future design task.

## Source Reports Reviewed
- `reports/aos-farm-521-third-pass-report-only-package-closure-rereview.md`
- `reports/aos-farm-522-task-canonical-schema-completion-report.md`

## Validator Logic Findings
The Python validator inherently enforces: `status READY_FOR_EXECUTION without explicit APPROVED approval_status`.
- **Finding 1:** The validator uses `approval_status: APPROVED` as a hard prerequisite for `status: READY_FOR_EXECUTION`.
- **Finding 2:** The validator heavily conflates human execution authorization (`execution_authorized: true`) and readiness (`ready_for_execution`) with total task approval.
- **Finding 3:** By enforcing this, the validator lacks the granularity to support "Execution Authorized but Not Approved" stages (like Report-Only Draft Tasks).

## Task Schema Comparison
- **Target Tasks (0509, 0513, 0516):** Hold `status: READY_FOR_EXECUTION` and `execution_authorized: true` (for past report generation only) but firmly hold `approval_granted: false`. They lack the `approval_status` YAML field entirely.
- **Valid Tasks (0001, 0468):** Currently hold `status: DRAFT` and `approval_status: NOT_APPROVED`. The conflation logic has not hit them yet because they are safely parked in `DRAFT` status.

## Canonical Safety Findings
Canonical sources (`00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`) unequivocally state:
- `PASS ≠ approval.`
- `Evidence ≠ approval.`
- `Human approval cannot be simulated.`
- `READY_FOR_EXECUTION` means "ready to execute if no blockers", it explicitly is *not* approval.
- `execution_authorized` and `approval` are treated as separate lifecycle mutations.
The Python validator directly contradicts these rules by demanding `APPROVED` for readiness.

## Conflict Classification
**MIXED**
The target tasks legitimately suffer from a `TASK_SCHEMA_GAP` (missing required baseline fields like `type`, `queue_priority`, `owner`, and text sections). However, there is a fundamental `APPROVAL_SEMANTICS_CONFLICT` inside the validator script where it couples readiness and approval, actively blocking safe resolution.

## Why adding approval_status: APPROVED is unsafe
Injecting `approval_status: APPROVED` into the target tasks would technically satisfy the validator, but would inject a false "fake human approval" into the system record. This directly breaches the `00_AOS_Core_Control.md` invariant: "Human approval cannot be simulated", resulting in a highly unsafe system state where tasks appear fully approved when they were only authorized for report-only execution.

## Safe Resolution Options
1. **Introduce approval_status values that do not imply approval**
   - *Example values:* `NOT_APPROVED`, `HUMAN_REVIEW_REQUIRED`, `EXECUTION_AUTHORIZED_NOT_APPROVED`
   - *Notes:* Requires validator change; cannot be done in this stage. Preserves PASS ≠ approval.

2. **Separate readiness_status from approval_status**
   - *Example fields:* `readiness_status: READY_FOR_EXECUTION`, `approval_status: NOT_APPROVED`, `execution_authorized: true`
   - *Notes:* Cleaner semantics; requires validator/schema update. Preserves READY_FOR_EXECUTION ≠ approval.

3. **Treat READY_FOR_EXECUTION as requiring execution authorization, not approval**
   - *Notes:* Validator should check human Risk Profile assignment + `execution_authorized: true`, not `APPROVED` `approval_status`. Requires validator changes.

4. **Keep legacy validator strictness and change task lifecycle**
   - *Notes:* Not recommended if it forces fake approval or downgrades already authorized report-only tasks.

5. **Mark 0509/0513/0516 as report-only non-canonical task artifacts**
   - *Notes:* May avoid validator readiness path by skipping them in the tool, but weakens task lifecycle integration.

## Recommended Option
**Option 3 (Treat READY_FOR_EXECUTION as requiring execution authorization, not approval)** combined with **Option 2 (Separate readiness_status from approval)**. This fully aligns the validator code with the canonical text sources (00, 01, 02) enforcing strict separation of powers without simulating approval.

## Recommended Next Stage
**AOS-FARM.524 — Validator Readiness/Approval Semantics Design Task Draft**
This should be a design task draft to safely plan the target model before executing any validator patches or task migrations.

## Validation Commands Run
- `python3 aos/scripts/aos_task_document_check.py task --readiness tasks/AOS-FARM-TASK-0509.md` (Failed)
- `python3 aos/scripts/aos_task_document_check.py task --validate-all` (Failed)

## Git Status and Diff
- `git status -sb`: Clean, no canonical files modified.
- `git diff --stat`: 0 tracked files modified.

## Blockers and Exceptions
- **BLOCKED**: AOS-FARM-TASK-0509, 0513, and 0516 remain blocked from validation until the semantics mismatch is officially patched via human checkpoint.
- **UNKNOWN_BLOCKED**: None.
- **NOT_RUN**: None.

## Authority Statement
This conflict review is not approval.
This conflict review does not authorize validator changes.
This conflict review does not authorize task file changes.
This conflict review does not authorize execution.
This conflict review does not authorize commit, push, merge, or release.

## Final Status
REVIEW_STATUS: READY_FOR_HUMAN_REVIEW
