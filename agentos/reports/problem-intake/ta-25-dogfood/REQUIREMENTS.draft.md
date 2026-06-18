# REQUIREMENTS.draft.md

```yaml
artifact_status: DRAFT
approval_status: NOT_APPROVED
automation_status: RUNNER_V2_EXISTING_SPEC_REVIEW_ONLY
production_status: NOT_PRODUCTION
intake_route: EXISTING_SPEC_REVIEW
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
commit_authorized: false
push_authorized: false
release_authorized: false
production_use_authorized: false
final_status: NEEDS_HUMAN_REVIEW
```

## Functional Requirements

- FR-001: Candidate behavior extracted from source material.
  - Source: existing specification review
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
  - Detail: - Preserve safety fields in every generated draft.
- Set `ready_for_execution: false`.
- Set `execution_authorized: false`.
- Set `implementation_authorized: false`.
- Carry open questions into UNKNOWN / Human Decisions Required.

## Data Requirements

- DATA-001: Candidate data handling scope.
  - Sensitive: UNKNOWN
  - Status: NEEDS_HUMAN_REVIEW
  - Detail: The source brief contains problem, user, current workflow, target outcome, constraints, risks, open questions, and acceptance criteria.

## Access Requirements

- ACCESS-001: Candidate access / permission scope.
  - Status: NEEDS_HUMAN_REVIEW
  - Detail: Only the human operator may approve execution, commit, push, release, or production use.

## Non-Functional Requirements

- NFR-001: Non-functional requirements are not finalized by this runner.
  - Status: NEEDS_HUMAN_REVIEW

## Constraints

- CON-001: Candidate constraints and non-goals.
  - Status: CANDIDATE_CONSTRAINT
  - Detail: - The generated artifacts must remain drafts.
- The output must not approve execution.
- The output must not create a final Task Brief.
- Unknowns must remain visible and blocking.

## Security / Privacy

- SEC-001: Security, privacy, and risk handling require human review.
  - Status: NEEDS_HUMAN_REVIEW
  - Detail: - False readiness claims.
- Approval boundary drift.
- Treating validator evidence as approval.

## Acceptance Criteria

- AC-001: Candidate acceptance criteria.
  - Status: CANDIDATE_ACCEPTANCE_CRITERION
  - Detail: - Required draft files are generated.
- Validator report is generated.
- UNKNOWN remains visible.
- No output declares approval or execution authorization.

## Out of Scope

- Final Task Brief creation.
- Execution authorization.
- Implementation authorization.
- Production use.

## UNKNOWN / Open Questions

- UNKNOWN: Human must confirm the final allowed file set before implementation.
- UNKNOWN: Human must confirm whether the generated candidate requirements are acceptable.

## Human Decisions Required

- Assign Risk Profile before any execution.
- Confirm whether candidate requirements are in scope.
- Confirm exact allowed and forbidden changes before implementation.
- Confirm acceptance criteria before execution.
- Confirm execution authorization separately; this runner never authorizes execution.
- Resolve or explicitly accept listed UNKNOWN items before finalization.

## Final Status

```yaml
artifact_type: technical_assignment_intake_draft
intake_depth: EXISTING_SPEC_REVIEW
problem_interview_status: NOT_REQUIRED_EXISTING_SPEC_REVIEW
problem_evidence_level: UNKNOWN
data_discovery_depth: PARTIAL
information_flow_status: PARTIAL
access_permissions_status: PARTIAL
requirements_confidence: LOW
unknown_count: 2
contradiction_count: 1
inference_count: 0
implementation_hint_count: 1
critical_failure_count: 2
ready_for_requirements_review: true_with_risks
ready_for_execution: false
approval_status: NOT_APPROVED
execution_authorized: false
implementation_authorized: false
commit_authorized: false
push_authorized: false
deploy_authorized: false
production_use_authorized: false
final_status: NEEDS_HUMAN_REVIEW
```
