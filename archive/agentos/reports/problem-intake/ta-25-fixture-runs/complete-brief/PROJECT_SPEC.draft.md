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

The Technical Assignment intake process needs to convert an existing user brief into reviewable draft artifacts without implying approval or execution authorization.

## 3. Data Discovery

The source brief contains problem, user, current workflow, target outcome, constraints, risks, open questions, and acceptance criteria.

## 4. Information Flow

Existing brief -> TA intake drafts -> bridge candidate inputs -> validator evidence -> Human Review Package.

## 5. Access / Permissions

Only the human operator may approve execution, commit, push, release, or production use.

## 6. Problem Evidence

- False readiness claims.
- Approval boundary drift.
- Treating validator evidence as approval.

## 7. Optional Current Workflow

The operator writes a free-form brief, then the agent manually extracts project intent, requirements, open questions, and review boundaries.

## 8. Requirements Draft

- Preserve safety fields in every generated draft.
- Set `ready_for_execution: false`.
- Set `execution_authorized: false`.
- Set `implementation_authorized: false`.
- Carry open questions into UNKNOWN / Human Decisions Required.

## 9. Implementation Hints

Use deterministic Markdown extraction and structural validator checks only.

## 10. Negative Constraints

- The generated artifacts must remain drafts.
- The output must not approve execution.
- The output must not create a final Task Brief.
- Unknowns must remain visible and blocking.

## 11. Acceptance Criteria

- Required draft files are generated.
- Validator report is generated.
- UNKNOWN remains visible.
- No output declares approval or execution authorization.

## 12. MVP

Automate only `EXISTING_SPEC_REVIEW`; interview routes remain manual.

## 13. UNKNOWN / Open Questions

- UNKNOWN: Human must confirm the final allowed file set before implementation.
- UNKNOWN: Human must confirm whether the generated candidate requirements are acceptable.

## 14. Contradictions

None known in the fixture input.

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
