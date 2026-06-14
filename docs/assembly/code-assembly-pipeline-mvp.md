# Code Assembly Pipeline MVP

This document defines the Minimum Viable Product (MVP) for the AOS-FARM Code Assembly Pipeline.

## 1. Goal
Provide a controlled, auditable flow for converting a Task Brief into a verified, authorized code change, strictly governed by human review and bounded scope.

## 2. Pipeline Flow
The Code Assembly Pipeline MVP enforces the following sequential flow:

1. **Task Brief**: The explicit, bounded goal and scope of the requested change.
2. **Scoped Code Change**: The exact files modified to fulfill the brief.
3. **Diff Evidence**: A record of the exact code changes made (e.g., `git diff`).
4. **Checks/Tests Evidence**: Results of any available read-only checks or tests to verify the change.
5. **Execution Report**: A summary report of what was executed, confirming adherence to the bounded scope.
6. **Evidence Report**: A comprehensive report combining diffs and check results for human review.
7. **Human Review**: Explicit human authorization or rejection of the proposed changes based on the Execution and Evidence reports.

## 3. Current Limitations & Safety Rules
Before automated validator implementation is established in future steps, the pipeline enforces these strict safety rules:

- **manual_human_review_required:** `true` (Human review is non-negotiable).
- **validator_status:** `NOT_RUN` (Automated validators are not yet active).
- **not_run_treated_as_pass:** `false` (`NOT_RUN` is never a `PASS`).
- **evidence_required:** `true` (Decisions must be based on documented evidence).

## 4. Required Artifacts
Executing the MVP requires generating specific artifacts based on the provided templates:
- Input constraints (`code-assembly-mvp-input-template.md`)
- Execution summary (`code-assembly-mvp-execution-report-template.md`)
- Evidence collection (`code-assembly-mvp-evidence-report-template.md`)
- Human approval/rejection (`code-assembly-mvp-human-review-template.md`)
