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
  - Detail: NEEDS_HUMAN_REVIEW: Functional Requirements was not found in the existing material.

## Data Requirements

- DATA-001: Candidate data handling scope.
  - Sensitive: UNKNOWN
  - Status: NEEDS_HUMAN_REVIEW
  - Detail: NEEDS_HUMAN_REVIEW: Data Requirements was not found in the existing material.

## Access Requirements

- ACCESS-001: Candidate access / permission scope.
  - Status: NEEDS_HUMAN_REVIEW
  - Detail: NEEDS_HUMAN_REVIEW: Access Requirements was not found in the existing material.

## Non-Functional Requirements

- NFR-001: Non-functional requirements are not finalized by this runner.
  - Status: NEEDS_HUMAN_REVIEW

## Constraints

- CON-001: Candidate constraints and non-goals.
  - Status: CANDIDATE_CONSTRAINT
  - Detail: NEEDS_HUMAN_REVIEW: Constraints was not found in the existing material.

## Security / Privacy

- SEC-001: Security, privacy, and risk handling require human review.
  - Status: NEEDS_HUMAN_REVIEW
  - Detail: NEEDS_HUMAN_REVIEW: Security / Privacy / Known Risks was not found in the existing material.

## Acceptance Criteria

- AC-001: Candidate acceptance criteria.
  - Status: CANDIDATE_ACCEPTANCE_CRITERION
  - Detail: NEEDS_HUMAN_REVIEW: Acceptance Criteria was not found in the existing material.

## Out of Scope

- Final Task Brief creation.
- Execution authorization.
- Implementation authorization.
- Production use.

## UNKNOWN / Open Questions

- UNKNOWN: Current Workflow missing or insufficient in source material.
- UNKNOWN: Constraints missing or insufficient in source material.
- UNKNOWN: Known Risks missing or insufficient in source material.
- UNKNOWN: Data Discovery missing or insufficient in source material.
- UNKNOWN: Information Flow missing or insufficient in source material.
- UNKNOWN: Access / Permissions missing or insufficient in source material.
- UNKNOWN: Acceptance Criteria missing or insufficient in source material.
- UNKNOWN: What workflow is currently failing?
- UNKNOWN: What constraints are mandatory?
- UNKNOWN: What risks are known?
- UNKNOWN: What data is involved?
- UNKNOWN: Who can approve execution?

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
data_discovery_depth: MISSING
information_flow_status: MISSING
access_permissions_status: MISSING
requirements_confidence: LOW
unknown_count: 12
contradiction_count: 0
inference_count: 0
implementation_hint_count: 0
critical_failure_count: 12
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
