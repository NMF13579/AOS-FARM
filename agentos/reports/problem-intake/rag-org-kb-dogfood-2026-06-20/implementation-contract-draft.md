# RAG Org KB Implementation Contract Draft

```yaml
dogfood_run_id: rag-org-kb-dogfood-2026-06-20
artifact_type: implementation_contract_draft
input_mode: DIRECT_TA_DRAFT
problem_interview_status: SKIPPED_BY_USER
artifact_status: DRAFT
approval_status: NOT_APPROVED
execution_status: NOT_AUTHORIZED
ready_for_execution: false
final_process_status: NEEDS_HUMAN_REVIEW
```

## 1. Metadata

- dogfood_run_id: `rag-org-kb-dogfood-2026-06-20`
- artifact_type: `implementation_contract_draft`
- input_mode: `DIRECT_TA_DRAFT`
- problem_interview_status: `SKIPPED_BY_USER`
- status: `DRAFT`
- approval_status: `NOT_APPROVED`
- execution_status: `NOT_AUTHORIZED`
- ready_for_execution: false

## 2. Purpose

This artifact bridges the current product/discovery draft and any future implementation Task Briefs.

Its purpose is to convert the current RAG product description into a more engineering-ready contract without approving implementation, without creating a Task Brief, and without claiming execution readiness.

## 3. Engineering Readiness Assessment

What is currently strong:

- roles and high-level permissions are described;
- document lifecycle intent is partially described;
- source-linked answer behavior is described;
- versioning, archive behavior, unanswered query analytics, and audit logging are identified;
- multi-organization and multi-base usage is explicitly in scope.

What is still not implementation-ready:

- the data model is not yet normalized into explicit entities and constraints;
- exact state transitions are not fully formalized;
- RBAC is not yet expressed as an enforceable matrix;
- indexing behavior is not fully specified;
- retrieval behavior is not fully specified;
- answer format and failure behavior need a tighter contract;
- unresolved UNKNOWN items still affect implementation choices.

## 4. Domain Entities / Data Model Draft

### Organization

- purpose: top-level business boundary for ownership, users, and one or more knowledge bases
- key fields:
  - organization_id
  - organization_name
  - status
  - created_at
  - created_by_user_id
- relationships:
  - has many `KnowledgeBase`
  - has many `User` memberships
- uniqueness constraints if known:
  - organization_id unique
- UNKNOWN:
  - whether organization slug must be globally unique

### Workspace or Tenant

- purpose: technical isolation boundary for organization data
- key fields:
  - tenant_id
  - organization_id
  - tenant_status
- relationships:
  - belongs to `Organization`
  - contains `KnowledgeBase`, `User`, `AuditEvent`
- uniqueness constraints if known:
  - one active tenant per organization assumed for MVP
- UNKNOWN:
  - whether `Workspace` and `Organization` are separate persisted concepts or the same object in MVP

### KnowledgeBase

- purpose: searchable document collection within an organization
- key fields:
  - knowledge_base_id
  - organization_id
  - owner_user_id
  - base_name
  - base_status
  - created_at
- relationships:
  - belongs to `Organization`
  - has one owner `User`
  - has many `Document`
  - has many access mappings via `AccessScope`
- uniqueness constraints if known:
  - one knowledge base id unique
  - one owner at a time
- UNKNOWN:
  - whether base name must be unique inside organization

### Document

- purpose: logical current document identity independent of version count
- key fields:
  - document_id
  - knowledge_base_id
  - current_version_id
  - document_title
  - document_category
  - document_status
  - effective_date
  - expiration_date_nullable
- relationships:
  - belongs to `KnowledgeBase`
  - has many `DocumentVersion`
  - has many role visibility assignments
- uniqueness constraints if known:
  - document_id unique
- UNKNOWN:
  - whether title is unique within category/base

### DocumentVersion

- purpose: immutable published or archived revision of a document
- key fields:
  - document_version_id
  - document_id
  - version_number_or_label
  - source_id
  - md_content_pointer
  - version_status
  - created_at
  - created_by_user_id
- relationships:
  - belongs to `Document`
  - has one `DocumentSource`
  - has one `DocumentMetadata`
  - has many `Chunk`
  - has many `IndexJob`
- uniqueness constraints if known:
  - document_version_id unique
  - one current version per document
- UNKNOWN:
  - exact version numbering strategy

### DocumentSource

- purpose: original user-provided source material for a version
- key fields:
  - source_id
  - source_type (`file` or `editor_text`)
  - original_filename_nullable
  - mime_type_nullable
  - source_storage_pointer
  - uploaded_at
  - uploaded_by_user_id
- relationships:
  - belongs to one `DocumentVersion`
- uniqueness constraints if known:
  - source_id unique
- UNKNOWN:
  - supported file formats for MVP

### DocumentMetadata

- purpose: reviewed metadata used for visibility, lifecycle, and search filters
- key fields:
  - metadata_id
  - document_version_id
  - title
  - description
  - category
  - tag_list
  - upload_timestamp
  - effective_date
  - expiration_date_nullable
  - extracted_role_targets
  - reviewed_by_user_id
- relationships:
  - belongs to `DocumentVersion`
- uniqueness constraints if known:
  - metadata_id unique
- UNKNOWN:
  - whether tags are free text or controlled vocabulary

### Chunk

- purpose: retrieval unit produced from Markdown sections
- key fields:
  - chunk_id
  - document_version_id
  - section_id_or_path
  - chunk_text
  - chunk_order
  - visibility_scope_snapshot
- relationships:
  - belongs to `DocumentVersion`
  - has one or more `EmbeddingRecord`
- uniqueness constraints if known:
  - chunk_id unique
  - chunk order unique within version
- UNKNOWN:
  - chunk sizing and overlap rules

### EmbeddingRecord

- purpose: vector representation of a chunk for retrieval
- key fields:
  - embedding_id
  - chunk_id
  - embedding_model_id
  - embedding_vector_pointer
  - created_at
  - embedding_status
- relationships:
  - belongs to `Chunk`
- uniqueness constraints if known:
  - one active embedding per chunk per embedding model
- UNKNOWN:
  - whether MVP stores vectors internally or through an external vector store

### IndexJob

- purpose: tracks parsing, chunking, and indexing work for a document version
- key fields:
  - index_job_id
  - document_version_id
  - requested_by_user_id_or_system
  - job_type
  - started_at
  - completed_at_nullable
  - job_status
  - error_summary_nullable
- relationships:
  - belongs to `DocumentVersion`
  - has one `IndexStatus`
- uniqueness constraints if known:
  - index_job_id unique
- UNKNOWN:
  - concurrency policy for multiple index jobs on same version

### IndexStatus

- purpose: current searchable/index health state for a document version
- key fields:
  - index_status_id
  - document_version_id
  - searchability_state
  - last_successful_indexed_at
  - last_failed_at_nullable
  - stale_state_flag
- relationships:
  - belongs to `DocumentVersion`
- uniqueness constraints if known:
  - one active status record per document version
- UNKNOWN:
  - whether `IndexStatus` is a separate persisted entity or derived projection

### User

- purpose: authenticated actor inside one or more organizations
- key fields:
  - user_id
  - email
  - display_name
  - account_status
  - registration_state
  - created_at
- relationships:
  - has many org memberships
  - has many `Role` assignments
  - has many `Query`
  - has many `AuditEvent`
- uniqueness constraints if known:
  - email unique globally assumed
- UNKNOWN:
  - account lifecycle states beyond invited/active

### Role

- purpose: named responsibility and visibility grouping
- key fields:
  - role_id
  - organization_id_or_base_scope
  - role_name
  - role_type
  - role_status
- relationships:
  - assigned to many `User`
  - linked to many `Permission`
  - linked to many `AccessScope`
- uniqueness constraints if known:
  - role name likely unique within scope
- UNKNOWN:
  - whether there are global/system roles plus organization roles in MVP

### Permission

- purpose: discrete allowed action or visibility capability
- key fields:
  - permission_id
  - permission_code
  - permission_description
- relationships:
  - many-to-many with `Role`
- uniqueness constraints if known:
  - permission_code unique
- UNKNOWN:
  - full permission catalog for MVP

### AccessScope

- purpose: binds users/roles to base/document visibility scope
- key fields:
  - access_scope_id
  - knowledge_base_id
  - role_id
  - document_category_or_selector
  - access_level
- relationships:
  - belongs to `KnowledgeBase`
  - belongs to `Role`
- uniqueness constraints if known:
  - scope rule uniqueness within base/role/selector combination
- UNKNOWN:
  - exact selector model for document-level versus category-level scope

### Query

- purpose: user search/chat input event
- key fields:
  - query_id
  - user_id
  - organization_id_context
  - selected_base_scope
  - query_text
  - created_at
  - answer_status
- relationships:
  - belongs to `User`
  - has many `RetrievalResult`
  - may have one `Answer`
- uniqueness constraints if known:
  - query_id unique
- UNKNOWN:
  - retention policy for full query text

### RetrievalResult

- purpose: candidate evidence set returned by retrieval before answer synthesis
- key fields:
  - retrieval_result_id
  - query_id
  - chunk_id
  - rank_position
  - score
  - visibility_check_result
- relationships:
  - belongs to `Query`
  - references `Chunk`
- uniqueness constraints if known:
  - unique query/chunk pair
- UNKNOWN:
  - score normalization across multiple knowledge bases

### Answer

- purpose: final user-facing response generated from retrieval evidence
- key fields:
  - answer_id
  - query_id
  - answer_text
  - answer_status
  - generated_at
  - insufficient_evidence_flag
  - conflict_detected_flag
- relationships:
  - belongs to `Query`
  - has many `Citation`
- uniqueness constraints if known:
  - one current answer per query assumed for MVP
- UNKNOWN:
  - whether regenerated answers overwrite or append

### Citation

- purpose: user-facing link between answer segments and source material
- key fields:
  - citation_id
  - answer_id
  - document_version_id
  - chunk_id
  - section_path
  - knowledge_base_id
  - cited_text_snippet
- relationships:
  - belongs to `Answer`
  - references `DocumentVersion` and `Chunk`
- uniqueness constraints if known:
  - citation_id unique
- UNKNOWN:
  - maximum citations per answer in MVP

### AuditEvent

- purpose: immutable audit trail for user-related and documentation-related changes
- key fields:
  - audit_event_id
  - actor_user_id
  - event_type
  - target_object_type
  - target_object_id
  - old_value_snapshot
  - new_value_snapshot
  - created_at
- relationships:
  - belongs to `User`
  - references arbitrary target object
- uniqueness constraints if known:
  - audit_event_id unique
- UNKNOWN:
  - retention duration and redaction policy

## 5. Document Lifecycle State Machine

### States

- `DRAFT`
- `UPLOADED`
- `PARSING`
- `PARSED`
- `CHUNKING`
- `CHUNKED`
- `INDEXING`
- `INDEXED`
- `AVAILABLE`
- `ARCHIVED`
- `DELETED`
- `INDEX_ERROR`

### Transition: DRAFT -> UPLOADED

- trigger: owner/admin accepts draft input for ingestion
- actor/system component: owner/admin
- required preconditions:
  - document source present
  - metadata reviewed
- failure behavior:
  - remain in `DRAFT`
  - validation issue shown to owner/admin
- visibility to users:
  - owner/admin only
- audit requirement:
  - log draft acceptance

### Transition: UPLOADED -> PARSING

- trigger: ingestion job starts
- actor/system component: system
- required preconditions:
  - source file/text stored
- failure behavior:
  - move to `INDEX_ERROR` if processing cannot begin
- visibility to users:
  - owner/admin only
- audit requirement:
  - log processing start

### Transition: PARSING -> PARSED

- trigger: source converted into Markdown representation
- actor/system component: parser
- required preconditions:
  - supported format or supported text input
- failure behavior:
  - move to `INDEX_ERROR`
  - preserve error details
- visibility to users:
  - owner/admin only
- audit requirement:
  - log parse completion or parse failure

### Transition: PARSED -> CHUNKING

- trigger: section splitting begins
- actor/system component: system
- required preconditions:
  - parsed Markdown exists
- failure behavior:
  - move to `INDEX_ERROR`
- visibility to users:
  - owner/admin only
- audit requirement:
  - log chunking start

### Transition: CHUNKING -> CHUNKED

- trigger: chunk generation completes
- actor/system component: system
- required preconditions:
  - parsed sections available
- failure behavior:
  - move to `INDEX_ERROR`
- visibility to users:
  - owner/admin only
- audit requirement:
  - log chunking completion or failure

### Transition: CHUNKED -> INDEXING

- trigger: embedding/index job starts
- actor/system component: system
- required preconditions:
  - chunk set created
- failure behavior:
  - move to `INDEX_ERROR`
- visibility to users:
  - owner/admin only
- audit requirement:
  - log indexing start

### Transition: INDEXING -> INDEXED

- trigger: index job completes successfully
- actor/system component: system
- required preconditions:
  - all required chunk/index writes succeed
- failure behavior:
  - move to `INDEX_ERROR`
- visibility to users:
  - owner/admin only until availability transition
- audit requirement:
  - log indexing success/failure

### Transition: INDEXED -> AVAILABLE

- trigger: searchable status is published
- actor/system component: system
- required preconditions:
  - indexing succeeded
  - document not archived/deleted
- failure behavior:
  - remain `INDEXED` or revert to `INDEX_ERROR`
- visibility to users:
  - end users if access scope allows
- audit requirement:
  - log availability event

### Transition: AVAILABLE -> ARCHIVED

- trigger: admin/owner archives current version or replaces by new version
- actor/system component: owner/admin
- required preconditions:
  - document version exists
- failure behavior:
  - remain `AVAILABLE`
- visibility to users:
  - hidden from end users
  - visible to owner/admin
- audit requirement:
  - log archival reason and actor

### Transition: AVAILABLE or ARCHIVED -> DELETED

- trigger: owner/admin deletes document
- actor/system component: owner/admin
- required preconditions:
  - delete permission
- failure behavior:
  - remain previous state
- visibility to users:
  - hidden from end users
- audit requirement:
  - log delete event

### Transition: any processing state -> INDEX_ERROR

- trigger: parsing/chunking/indexing failure
- actor/system component: system
- required preconditions:
  - processing exception or unrecoverable validation failure
- failure behavior:
  - persist error details
  - keep user-invisible state
- visibility to users:
  - owner/admin only
- audit requirement:
  - log failure with error summary

## 6. RBAC Matrix Draft

| Role | Object | Action | Draft Permission |
|---|---|---|---|
| System Admin | Organization | create knowledge base | UNKNOWN |
| Organization Admin | KnowledgeBase | create knowledge base | UNKNOWN |
| Knowledge Base Manager | KnowledgeBase | create knowledge base | YES |
| Document Uploader | Document | upload document | YES |
| Reviewer | DocumentMetadata | edit metadata | YES |
| Reviewer | Document | approve document for availability | YES |
| Knowledge Base Manager | Document | archive document | YES |
| Knowledge Base Manager | Document | delete document | YES |
| Knowledge Base Manager | Document | restore document | UNKNOWN |
| Knowledge Base Manager | IndexJob | trigger reindex | YES |
| End User | KnowledgeBase | query knowledge base | YES, scope-limited |
| End User | Citation | view citations | YES, scope-limited |
| Auditor | AuditEvent | view audit log | YES |
| Knowledge Base Manager | User/Role | manage user access | YES |
| Organization Admin | User/Role | manage user access | YES |
| System Admin | AuditEvent | view audit log | UNKNOWN |
| End User | AuditEvent | view audit log | NO |

Notes:

- `Knowledge Base Manager` is the closest engineering abstraction for owner/admin operational rights inside one knowledge base.
- `Organization Admin`, `System Admin`, `Reviewer`, `Document Uploader`, and `Auditor` remain draft roles for implementation analysis and may collapse into a smaller MVP role set.
- Final role model remains subject to human review.

## 7. Indexing Contract

- Successful indexing means:
  - document source converted to Markdown
  - sections created
  - chunks created
  - chunk embeddings/index records created
  - index status marked searchable
- A document becomes searchable only when lifecycle reaches `AVAILABLE`.
- Partial indexing failure behavior:
  - document must not become user-searchable
  - state moves to `INDEX_ERROR`
  - owner/admin can see error
- Reindexing behavior:
  - creates a new index job record
  - may reuse current document version
  - must update index status and audit log
- Document update effect on old chunks:
  - old version chunks remain tied to archived version
  - current retrieval should target current searchable version only unless history mode is later introduced
- Deletion behavior:
  - deleted content must be removed or hidden from retrieval results
  - deletion outcome must be logged
- Stale index detection:
  - if current version changes without successful reindex, index status must indicate stale/not available
- Logging:
  - index job requested
  - index job started
  - index job completed
  - index job failed
  - searchable availability changed

## 8. Retrieval Contract

- Retrieval assumptions:
  - lexical / vector / hybrid remains open
  - MVP default assumption: `hybrid_or_vector_biased` is UNKNOWN and needs human/engineering decision
- Default MVP retrieval mode:
  - recommended draft default: start with simple retriever plus permission filters
  - exact mode remains UNKNOWN
- Permission filtering:
  - retrieval must exclude chunks from inaccessible document versions before answer generation
- `top_k` behavior:
  - MVP should use a fixed configurable `top_k`
  - exact value UNKNOWN
- Ranking assumptions:
  - rank by retriever score inside filtered scope
  - cross-base ranking strategy UNKNOWN
- Merge across multiple knowledge bases:
  - retrieval scope may span all selected accessible bases
  - answer citations must show knowledge base origin per source
- Weak match behavior:
  - if evidence is too weak, system should report that answer is not found or evidence is insufficient
- Conflicting documents:
  - retrieval may include conflicting sources
  - answer generation must disclose conflict rather than silently choose one
- Partial access behavior:
  - if user lacks access to some relevant sources, system must not cite or expose them
  - whether the system explains that hidden sources exist is UNKNOWN

## 9. Chat Answer Contract

- Expected answer format:
  - direct answer text
  - segmented source citations
  - each cited segment linked to source document and section
- Mandatory citations:
  - yes, for answer segments grounded in documents
- Maximum number of cited sources:
  - UNKNOWN for MVP
- Insufficient evidence behavior:
  - system should explicitly state that answer was not found or evidence is insufficient
- Conflict behavior:
  - system must disclose conflicting sources and summarize what each says
  - should indicate which source was loaded most recently
- UNKNOWN representation:
  - unknown or unresolved information should be stated explicitly, not guessed
- Assistant must not invent:
  - hidden sources
  - unsupported policy claims
  - fake certainty
  - document authority decisions that belong to admins
- How users see source documents:
  - click citation -> open Markdown document page -> highlight source section
- Confidence labels:
  - optional only
  - not required for MVP
  - if later added, must not imply approval

## 10. Error Handling Contract

- Unsupported file format:
  - reject ingestion
  - keep document non-searchable
  - show admin-visible error
  - log event
- Parsing failure:
  - move to `INDEX_ERROR`
  - preserve source and error summary
- OCR failure if applicable:
  - OCR applicability UNKNOWN
  - if used and OCR fails, move to `INDEX_ERROR`
- Oversized file:
  - reject or defer processing based on configured size limit
  - limit value UNKNOWN
- Duplicate document:
  - warn owner/admin
  - allow upload as separate document if user chooses
- Conflicting metadata:
  - warn owner/admin
  - require manual correction before acceptance
- Permission mismatch:
  - deny user access to restricted content
  - log admin-visible access changes, not necessarily every read event unless later required
- Index job timeout:
  - mark job failed or timed out
  - set `INDEX_ERROR`
  - allow retry/reindex
- Retrieval returns no results:
  - answer state should be "answer not found"
  - record analytics signal for unanswered query
- Source deleted after answer generation:
  - historical answer may reference a no-longer-available source
  - future retrieval must exclude deleted source
  - exact user-facing behavior UNKNOWN

## 11. Audit and Retention Contract

- Events that must be logged:
  - create/update/archive/delete document
  - metadata edit
  - publish action
  - version replacement
  - invitation send
  - user activation state changes
  - role assignment changes
  - owner transfer
  - access rule changes
  - index job lifecycle changes
- Who can see audit events:
  - owner/admin
  - possible auditor role
  - final visibility rules remain draft
- Retention assumptions:
  - retention period UNKNOWN
  - audit should be treated as durable by default
- Deletion/archive semantics:
  - archive keeps historical visibility for owner/admin
  - delete hides/removes from normal use but audit record remains
- Whether answers and queries are logged:
  - user personal query history yes
  - admin analytics aggregates yes
  - exact retention and privacy treatment UNKNOWN
- Privacy/security warnings:
  - cross-organization isolation is critical
  - query history is personal and should not become broad admin-visible chat transcript by default

## 12. MVP Slice Boundary

Recommended narrow first MVP implementation slice:

- document upload
- direct text ingestion
- document metadata extraction + manual admin review
- document version record
- Markdown conversion contract
- chunk creation contract
- indexing job record
- index status tracking
- admin visibility of processing/indexing state

Reasoning:

- this slice exercises the document pipeline and audit trail
- it avoids full production chat complexity too early
- it produces engineering evidence for the riskiest content lifecycle pieces first

Full production RAG chat is out of scope for the first implementation slice and should be handled in a later scoped Task Brief.

## 13. Out of Scope For First Implementation

- multi-tenant production hardening
- advanced hybrid ranking
- full semantic conflict resolution
- external connector sync
- automatic approval of documents
- production-grade security certification
- autonomous deletion
- release or production use
- full cross-base query analytics sophistication
- final polished user chat experience

## 14. Remaining UNKNOWN

- exact ranking logic across multiple bases
- exact chunk sizing and overlap
- supported file formats for MVP
- OCR support in MVP
- retention duration for audit and query history
- exact role catalog for engineering implementation
- whether restore-from-archive is supported in MVP
- exact stale index detection policy
- exact limit on cited sources
- exact tag taxonomy
- exact behavior when hidden but relevant sources exist

## 15. Human Review Questions

Priority 1:

- What is the narrowest first MVP slice the human owner wants implemented first?
- What exact roles exist in MVP, and which draft roles can be collapsed?
- Should the first implementation include any user-facing chat, or only the document ingestion/indexing pipeline?

Priority 2:

- What file formats must be supported in MVP?
- What is the required conflict detection behavior threshold?
- What ranking/retrieval approach is acceptable for the first MVP slice?

Priority 3:

- What retention rules apply to query history and audit logs?
- Should deleted documents remain recoverable for owner/admin in MVP?
- What analytics beyond unanswered/popular queries are actually required?

## 16. Final Status

```yaml
artifact_status: DRAFT
approval_status: NOT_APPROVED
execution_status: NOT_AUTHORIZED
ready_for_execution: false
final_process_status: NEEDS_HUMAN_REVIEW
```
