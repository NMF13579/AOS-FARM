# PROJECT_SPEC.draft.md

```yaml
artifact_status: DRAFT
approval_status: NOT_APPROVED
automation_status: MANUAL_CHAT_DIRECT_TA_DRAFT_ONLY
production_status: NOT_PRODUCTION
intake_route: DIRECT_TA_DRAFT
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
| Entry Route | DIRECT_TA_DRAFT |
| Problem Interview Status | SKIPPED_BY_USER |
| Ready For Execution | false |
| Approval Status | NOT_APPROVED |
| Missing Sections Status | NEEDS_HUMAN_REVIEW |

## 2. User Vision

Organizations need a universal RAG platform where owners and administrators manage knowledge bases and documents, while users ask questions and receive source-linked answers drawn only from information they are allowed to see.

## 3. Data Discovery

The system includes organizations, knowledge bases, users, job roles, invitations, uploaded or authored documents, extracted metadata, Markdown conversions, sections, chunks, source links, versions, archive states, analytics summaries, and audit logs.

## 4. Information Flow

Owner creates base -> invites users -> assigns administrators -> document upload or authored text -> automatic metadata extraction -> administrator review -> draft or publish choice -> Markdown conversion -> sectioning -> chunking -> indexing -> user chat/search over selected accessible bases -> answer with source links -> admin/owner analytics and audit review.

## 5. Access / Permissions

- One knowledge base has one owner.
- Owner can appoint administrators and delete the base.
- Owner and administrator can invite users, manage roles, upload documents, publish, archive, and delete documents.
- Users only search and view information within role-based visibility.
- Users may belong to multiple organizations and search across all, several, or one allowed base.
- Archived, processing, and error states are visible only to owners and administrators.

## 6. Problem Evidence

- Organizations need fast access to current internal information.
- Answers must remain tied to explicit source documents.
- Role-based access and multiple organizations create visibility complexity.
- Users need both chat-first access and document browsing.

## 7. Optional Current Workflow

This draft was assembled directly from a direct brief. Detailed current-state pain mapping was not expanded through problem interview and remains partially undiscovered.

## 8. Requirements Draft

- Support one or more knowledge bases per organization.
- Allow users to search across all, selected, or one accessible base.
- Support file upload and direct text entry for document creation.
- Automatically extract metadata and require administrator review before acceptance.
- Convert documents to Markdown and index by section/chunk.
- Show source links for each answer segment and highlight the source section.
- Track versions by title and document date heuristics with admin confirmation.
- Detect conflicts between documents without auto-blocking publication.
- Provide unanswered query and popular query analytics per base.
- Log all documentation and user-related changes.

## 9. Implementation Hints

- Chat is the first user entry point.
- Document list/search is the secondary navigation path.
- Workflow states inside the product must not be treated as AOS approval semantics.

## 10. Negative Constraints

- The draft must not imply execution authorization.
- The draft must not imply implementation authorization.
- The system must not automatically decide the final authoritative document in a conflict.
- Personal knowledge bases are out of scope for this case.
- UNKNOWN items must remain visible.

## 11. Acceptance Criteria

- Users can receive source-linked answers restricted by their role visibility.
- Owners and administrators can manage bases, users, documents, and visibility rules.
- Published documents become searchable only after indexing.
- Old versions archive instead of being silently overwritten.
- Conflict and no-answer situations are surfaced honestly.
- No output declares approval or execution authorization.

## 12. MVP

MVP covers organizational knowledge bases, invitation-driven access, role-based visibility, source-linked chat, document browsing, version/archive flow, unanswered/popular query analytics, and audit logs.

## 13. UNKNOWN / Open Questions

- UNKNOWN: exact ranking logic across multiple bases is not defined.
- UNKNOWN: detailed tag taxonomy is not defined.
- UNKNOWN: invitation/account lifecycle edge cases remain partial.
- UNKNOWN: full analytics/reporting model is not finalized.

## 14. Contradictions

- None explicit yet, but conflicting document content is expected and must be represented rather than hidden.

## 15. Human Decisions Required

- Confirm role and visibility edge cases.
- Confirm first implementation scope for conflict resolution tooling.
- Confirm analytics depth for administrators and owners.
- Assign downstream Risk Profile before any implementation task.
- Authorize execution separately if a future scoped task is prepared.

## 16. Final Status

```yaml
artifact_type: technical_assignment_intake_draft
intake_depth: DIRECT_TA_DRAFT
problem_interview_status: SKIPPED_BY_USER
problem_evidence_level: LOW
data_discovery_depth: MEDIUM
information_flow_status: MEDIUM
access_permissions_status: PARTIAL
requirements_confidence: MEDIUM
unknown_count: 4
contradiction_count: 1
inference_count: 1
implementation_hint_count: 3
critical_failure_count: 0
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
