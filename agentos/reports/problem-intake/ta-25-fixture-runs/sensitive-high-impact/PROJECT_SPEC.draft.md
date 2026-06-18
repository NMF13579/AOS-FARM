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

The team wants a technical assignment for reviewing access to sensitive operational incident records.

## 3. Data Discovery

Only synthetic fixture content is used. Real data classes are unknown.

## 4. Information Flow

Sensitive incident notes -> candidate requirements -> human review package.

## 5. Access / Permissions

Access roles, audit requirements, and approval authority are not confirmed.

## 6. Problem Evidence

- Sensitive operational records may include private or security-relevant information.
- Access changes may affect protected workflows.
- Human review is mandatory before execution.

## 7. Optional Current Workflow

Incident details are shared manually with uneven access controls.

## 8. Requirements Draft

- Mark sensitive scope as needing human review.
- Preserve security and privacy unknowns.
- Keep execution authorization false.

## 9. Implementation Hints

No code implementation should be inferred from this fixture.

## 10. Negative Constraints

- Do not process real sensitive data in this fixture.
- Do not approve access model changes.
- Do not authorize implementation or production use.

## 11. Acceptance Criteria

- Generated drafts show privacy/security blockers.
- Validator report remains structural evidence only.

## 12. MVP

Candidate documentation only, no runtime or production processing.

## 13. UNKNOWN / Open Questions

- UNKNOWN: What exact data classes are in scope?
- UNKNOWN: Who is authorized to view each class?
- UNKNOWN: What retention and audit requirements apply?
- UNKNOWN: Is a separate domain checkpoint required?

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
data_discovery_depth: PARTIAL
information_flow_status: PARTIAL
access_permissions_status: PARTIAL
requirements_confidence: LOW
unknown_count: 4
contradiction_count: 0
inference_count: 0
implementation_hint_count: 1
critical_failure_count: 4
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
