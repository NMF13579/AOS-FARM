# REQUIREMENTS.draft.md

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

## Functional Requirements

- FR-001: The system must support organizations with one or more knowledge bases.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-002: Each knowledge base must have exactly one owner at a time.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-003: Owners may appoint administrators and delete a knowledge base.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-004: Owners and administrators may invite users by email and manage role-based access.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-005: Users may belong to multiple organizations and search across all, selected, or one accessible base.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-006: Owners and administrators may upload files or enter text directly as document input.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-007: The system must automatically extract document metadata and require manual administrator review before acceptance.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-008: Published documents must convert to Markdown, split into sections, chunk, and index before becoming searchable to users.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-009: Each answer segment must link to the source document, source section, and source knowledge base.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-010: Users must be able to browse documents and filter by base, tags, and upload date.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-011: Owners and administrators must have extra filters for status, roles, upload date, drafts, and archive state.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-012: If multiple sources conflict, the system must disclose the conflict, show each source position, and indicate which source was loaded most recently.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-013: Conflict detection during upload must warn administrators without blocking publication.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-014: When a document is corrected, a new version must be created and the old version archived.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-015: The system must detect possible version continuity by document title and document date, with administrator choice to accept as new version or keep as separate document.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-016: Users must see personal query history.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-017: Owners and administrators must see unanswered-query and popular-query analytics per base.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-018: The system must log all user-related and documentation-related changes.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true

## Data Requirements

- DATA-001: Documents must store title, description, category, target roles, upload timestamp, effective date, and optional expiration.
  - Status: CANDIDATE_REQUIREMENT
- DATA-002: Document states must support at least: `draft`, `processing`, `available`, `error`, `archived`.
  - Status: CANDIDATE_REQUIREMENT
- DATA-003: Audit logs must store actor, timestamp, target object, action, old value, and new value.
  - Status: CANDIDATE_REQUIREMENT

## Access Requirements

- ACCESS-001: Access visibility is determined by one or more assigned job roles.
  - Status: CANDIDATE_REQUIREMENT
- ACCESS-002: Archived, processing, and error documents are visible only to owners and administrators.
  - Status: CANDIDATE_REQUIREMENT
- ACCESS-003: Personal histories remain private, but analytics aggregates are visible to owners and administrators for bases they manage.
  - Status: CANDIDATE_REQUIREMENT
- ACCESS-004: Final role/access edge cases remain unresolved and require human review.
  - Status: NEEDS_HUMAN_REVIEW

## Non-Functional Requirements

- NFR-001: The first user entry page should be chat-first.
  - Status: CANDIDATE_REQUIREMENT
- NFR-002: Source traceability must be strong enough for a user to open the exact Markdown document and highlighted section.
  - Status: CANDIDATE_REQUIREMENT
- NFR-003: System processing states must be visible to administrators instead of being hidden.
  - Status: CANDIDATE_REQUIREMENT

## Constraints

- CON-001: Organizations only in this scope; no personal knowledge bases.
  - Status: CANDIDATE_CONSTRAINT
- CON-002: Workflow status inside the product must not be treated as AOS approval or execution authorization.
  - Status: CANDIDATE_CONSTRAINT
- CON-003: Problem interview was skipped, so confidence remains lower and UNKNOWN remains blocking for future implementation decisions.
  - Status: CANDIDATE_CONSTRAINT

## Security / Privacy

- SEC-001: Cross-organization access isolation and audit behavior require later human review.
  - Status: NEEDS_HUMAN_REVIEW

## Acceptance Criteria

- AC-001: A user can ask questions and receive source-linked answers limited to visible documents.
  - Status: CANDIDATE_ACCEPTANCE_CRITERION
- AC-002: A user can browse visible documents and filter them by base, tags, and upload date.
  - Status: CANDIDATE_ACCEPTANCE_CRITERION
- AC-003: Owners and administrators can manage documents, access, and analytics for their bases.
  - Status: CANDIDATE_ACCEPTANCE_CRITERION
- AC-004: Conflicts, unanswered queries, versioning, and archive behavior remain visible instead of being silently hidden.
  - Status: CANDIDATE_ACCEPTANCE_CRITERION

## Out of Scope

- Personal knowledge bases.
- Execution authorization.
- Implementation authorization.
- Production release decisions.
- Methodology changes.

## UNKNOWN / Open Questions

- UNKNOWN: exact ranking logic across multiple bases is not defined.
- UNKNOWN: detailed tag taxonomy is not defined.
- UNKNOWN: full invitation/account lifecycle edge cases remain partial.
- UNKNOWN: analytics and reporting depth is not finalized.

## Human Decisions Required

- Confirm cross-organization and multi-role edge cases.
- Confirm conflict handling UX depth for MVP.
- Confirm analytics scope beyond unanswered/popular queries.
- Assign Risk Profile before any implementation.
- Authorize any later execution separately.

## Final Status

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
