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

The project needs intake drafts for a reporting workflow, but the source brief does not identify the data inventory.

## 3. Data Discovery

NEEDS_HUMAN_REVIEW: Data Discovery was not found in the existing material.

## 4. Information Flow

Notes and summaries are expected to become reviewable requirements, but exact source systems are unknown.

## 5. Access / Permissions

Access model is not confirmed.

## 6. Problem Evidence

Unknown data sources may hide privacy, ownership, or access-control requirements.

## 7. Optional Current Workflow

Reports are assembled manually from notes and chat summaries.

## 8. Requirements Draft

- Mark data discovery as missing.
- Require human review before execution.
- Preserve visible UNKNOWN items.

## 9. Implementation Hints

NEEDS_HUMAN_REVIEW: Implementation Hints was not found in the existing material.

## 10. Negative Constraints

- Do not infer data sources.
- Do not infer retention policy.
- Do not authorize implementation while data discovery is unknown.

## 11. Acceptance Criteria

- Generated drafts expose missing data discovery.
- Validator evidence does not convert missing data into approval.

## 12. MVP

Create candidate drafts only.

## 13. UNKNOWN / Open Questions

- UNKNOWN: Data Discovery missing or insufficient in source material.
- UNKNOWN: What data sources are used?
- UNKNOWN: What fields are sensitive?
- UNKNOWN: Who owns the source data?
- UNKNOWN: What retention policy applies?

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
information_flow_status: PARTIAL
access_permissions_status: PARTIAL
requirements_confidence: LOW
unknown_count: 5
contradiction_count: 0
inference_count: 0
implementation_hint_count: 0
critical_failure_count: 5
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
