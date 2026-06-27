# Task Quality Acceptance Gate

## Purpose
The Task Quality Acceptance Gate acts as a mandatory verification layer after task execution. Its goal is to provide a structured, evidence-based mechanism for a human to determine whether a task successfully fulfilled its objectives before any commit, push, or lifecycle state mutation is authorized.

## Problem Statement
Historically, AI-generated "PASS" or "Evidence" markers have sometimes been misinterpreted as final approvals, leading to false confidence or bypass of human review. The lack of a formalized Acceptance Criteria tracking structure has made it difficult to assess if a task truly met all its required outcomes.

## Scope
* Establishing a standard model for Acceptance Criteria, Evidence Matrix, and functional status.
* Defining a read-only checker (Task Quality Checker MVP) to validate these models structurally.
* Presenting a User-Facing Acceptance Summary.
* Requiring an explicit Human Result Acceptance checkpoint.

## Non-Goals
* Automatically approving tasks.
* Executing tasks or tests (this is a static quality gate, not a runner).
* Mutating lifecycle states or advancing the task to completion without human review.
* Authorizing commits or pushes.

## Task Quality Flow
1. **Pre-execution**: Acceptance Criteria are defined.
2. **Execution**: Work is done and Evidence is generated.
3. **Verification**: The Evidence Matrix is populated.
4. **Validation**: The read-only Checker verifies that all required Criteria have corresponding Evidence, and determines the Functional Status.
5. **Review**: The User-Facing Acceptance Summary is presented.
6. **Decision**: Human performs Result Acceptance (ACCEPT_RESULT / NEEDS_CHANGES / REJECT_RESULT).

## Models
### Acceptance Criteria Model
A structured list defining what constitutes a successful outcome. Each criterion is marked as required or optional.

### Evidence Matrix Model
A mapping of Acceptance Criteria to explicit artifacts (files, URLs, test logs) demonstrating fulfillment.

### Functional Status Model
Based on the checker validation:
* `PASS`: All required criteria have evidence; no forbidden outputs.
* `PASS_WITH_WARNINGS`: Required criteria met, but optional ones missing.
* `BLOCKED`: Missing required evidence or forbidden outputs present.
* `NOT_ENOUGH_EVIDENCE`: Evidence is insufficient to determine state.
* `UNKNOWN` / `NOT_RUN`: Checker execution failed or not started.

### User-Facing Acceptance Summary Model
A markdown document summarizing the objectives, verified criteria, missing evidence, Functional Status, and required human decisions.

## Human Result Acceptance Boundary
The human must explicitly review the Summary and mark the task as accepted. No AI agent can self-approve.

## False PASS Resistance
The checker must actively resist false PASS claims:
* `UNKNOWN` is not `PASS`.
* `NOT_RUN` is not `PASS`.
* Detection of forbidden approval/completion claims in output forces a `BLOCKED` state.
* Evidence MUST exist and be explicitly referenced for all required criteria.

## Relation to Task Registry / Queue
Task Registry and Queue items track their Task Quality phase:
* `task_quality_required`: boolean
* `task_quality_package_path`: path/to/package.json
* `acceptance_criteria_path`: path/to/criteria.md
* `evidence_matrix_path`: path/to/matrix.md
* `user_acceptance_summary_path`: path/to/summary.md
* `task_quality_status`: NOT_RUN | PASS | PASS_WITH_WARNINGS | BLOCKED | NOT_ENOUGH_EVIDENCE
* `human_result_acceptance_status`: NOT_REQUESTED | HUMAN_REVIEW_REQUIRED | ACCEPTED | NEEDS_CHANGES | REJECTED

## Relation to Commit/Push Authorization
Task Quality PASS is **NOT** commit authorization or push authorization. It is merely a prerequisite. A human must still explicitly review the implementation and provide separate authorizations for git operations.
