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

We need a better way to collect technical assignment details from a short user idea.

## 3. Data Discovery

NEEDS_HUMAN_REVIEW: Data Discovery was not found in the existing material.

## 4. Information Flow

NEEDS_HUMAN_REVIEW: Information Flow was not found in the existing material.

## 5. Access / Permissions

NEEDS_HUMAN_REVIEW: Access / Permissions was not found in the existing material.

## 6. Problem Evidence

NEEDS_HUMAN_REVIEW: Problem Evidence / Known Risks was not found in the existing material.

## 7. Optional Current Workflow

NEEDS_HUMAN_REVIEW: Current Workflow was not found in the existing material.

## 8. Requirements Draft

NEEDS_HUMAN_REVIEW: Requirements Draft was not found in the existing material.

## 9. Implementation Hints

NEEDS_HUMAN_REVIEW: Implementation Hints was not found in the existing material.

## 10. Negative Constraints

NEEDS_HUMAN_REVIEW: Negative Constraints / Constraints was not found in the existing material.

## 11. Acceptance Criteria

NEEDS_HUMAN_REVIEW: Acceptance Criteria was not found in the existing material.

## 12. MVP

NEEDS_HUMAN_REVIEW: MVP was not found in the existing material.

## 13. UNKNOWN / Open Questions

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

## 14. Contradictions

NEEDS_HUMAN_REVIEW: Contradictions was not found in the existing material.

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
