# PROJECT_SPEC.draft.md

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

## 1. Source Status

| Field | Value |
|---|---|
| Entry Route | EXISTING_SPEC_REVIEW |
| Problem Interview Status | NOT_REQUIRED_EXISTING_SPEC_REVIEW |
| Ready For Execution | false |
| Approval Status | NOT_APPROVED |
| Missing Sections Status | NEEDS_HUMAN_REVIEW |

## 2. User Vision

The source brief asks for a technical assignment to automate an intake flow, but also says automation must not start until the scope is clarified.

## 3. Data Discovery

No external data is involved in this fixture.

## 4. Information Flow

Contradictory brief -> candidate drafts -> UNKNOWN / Human Decisions Required.

## 5. Access / Permissions

Only the human operator may resolve the contradiction.

## 6. Problem Evidence

- The agent might treat contradictory instructions as permission to continue.
- The agent might hide a skip/blocker condition.

## 7. Optional Current Workflow

The user provides mixed instructions in one brief, and the agent must preserve the contradiction instead of smoothing it away.

## 8. Requirements Draft

- Preserve contradictions.
- Require human review.
- Keep authorization fields false.

## 9. Implementation Hints

NEEDS_HUMAN_REVIEW: Implementation Hints was not found in the existing material.

## 10. Negative Constraints

- Do not resolve contradictions by assumption.
- Do not authorize execution.
- Do not create a final Task Brief.

## 11. Acceptance Criteria

- Generated drafts include visible contradiction handling.
- Validator does not issue approval.

## 12. MVP

Candidate documentation only.

## 13. UNKNOWN / Open Questions

- UNKNOWN: Should automation continue, pause, or be split into a new task?
- UNKNOWN: Which instruction has priority?
- UNKNOWN: What exact scope is authorized?

## 14. Contradictions

The brief requests automation and also says automation must not start until scope is clarified.

## 15. Human Decisions Required

- Assign Risk Profile before any execution.
- Confirm whether candidate requirements are in scope.
- Confirm exact allowed and forbidden changes before implementation.
- Confirm acceptance criteria before execution.
- Confirm execution authorization separately; this runner never authorizes execution.
- Resolve or explicitly accept listed UNKNOWN items before finalization.

## 16. Final Status

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
