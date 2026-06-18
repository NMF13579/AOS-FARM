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
  - Detail: - Preserve contradictions.
- Require human review.
- Keep authorization fields false.

## Data Requirements

- DATA-001: Candidate data handling scope.
  - Sensitive: UNKNOWN
  - Status: NEEDS_HUMAN_REVIEW
  - Detail: No external data is involved in this fixture.

## Access Requirements

- ACCESS-001: Candidate access / permission scope.
  - Status: NEEDS_HUMAN_REVIEW
  - Detail: Only the human operator may resolve the contradiction.

## Non-Functional Requirements

- NFR-001: Non-functional requirements are not finalized by this runner.
  - Status: NEEDS_HUMAN_REVIEW

## Constraints

- CON-001: Candidate constraints and non-goals.
  - Status: CANDIDATE_CONSTRAINT
  - Detail: - Do not resolve contradictions by assumption.
- Do not authorize execution.
- Do not create a final Task Brief.

## Security / Privacy

- SEC-001: Security, privacy, and risk handling require human review.
  - Status: NEEDS_HUMAN_REVIEW
  - Detail: - The agent might treat contradictory instructions as permission to continue.
- The agent might hide a skip/blocker condition.

## Acceptance Criteria

- AC-001: Candidate acceptance criteria.
  - Status: CANDIDATE_ACCEPTANCE_CRITERION
  - Detail: - Generated drafts include visible contradiction handling.
- Validator does not issue approval.

## Out of Scope

- Final Task Brief creation.
- Execution authorization.
- Implementation authorization.
- Production use.

## UNKNOWN / Open Questions

- UNKNOWN: Should automation continue, pause, or be split into a new task?
- UNKNOWN: Which instruction has priority?
- UNKNOWN: What exact scope is authorized?

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
unknown_count: 3
contradiction_count: 1
inference_count: 0
implementation_hint_count: 0
critical_failure_count: 3
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
