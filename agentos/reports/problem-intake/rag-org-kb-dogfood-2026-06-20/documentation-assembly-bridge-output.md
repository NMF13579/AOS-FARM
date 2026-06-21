# RAG Org KB Documentation Assembly Bridge Output

```yaml
dogfood_run_id: rag-org-kb-dogfood-2026-06-20
artifact_type: documentation_assembly_bridge_output
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
- artifact_type: `documentation_assembly_bridge_output`
- input_mode: `DIRECT_TA_DRAFT`
- problem_interview_status: `SKIPPED_BY_USER`
- artifact_status: `DRAFT`
- approval_status: `NOT_APPROVED`
- execution_status: `NOT_AUTHORIZED`
- ready_for_execution: false
- final_process_status: `NEEDS_HUMAN_REVIEW`

## 2. Purpose

This artifact bridges the RAG Org KB product/discovery draft, implementation contract draft, and UNKNOWN resolution addendum into a human-reviewable Documentation Assembly package.

It prepares the package for review and future implementation planning, but it does not authorize execution, does not create a Task Brief, and does not approve implementation.

## 3. Source Artifacts Reviewed

- `input.md`
- `PROJECT_SPEC.draft.md`
- `REQUIREMENTS.draft.md`
- `requirements-checklist-draft.md`
- `implementation-contract-draft.md`
- `unknown-resolution-addendum.md`
- `problem-intake-run-report.md`

## 4. Package Summary

The RAG Org KB case describes an organizational knowledge base platform where each organization can create one or more knowledge bases, invite users, assign roles, upload or author documents, manage document lifecycle, and eventually provide source-linked retrieval/chat answers.

Core concept:

- organizational knowledge bases with owner/admin/user access;
- document upload and text-entry workflows;
- automatic metadata extraction followed by manual admin review;
- document conversion to Markdown, section extraction, chunk creation, and indexing;
- role-based visibility by user job roles;
- future retrieval/chat layer with mandatory citations to internal source documents;
- audit logging for document, user, role, and access changes;
- retention policy requirement, with exact retention duration unresolved.

The case used direct brief mode rather than a full problem interview. This is accepted for dogfood, but confidence is lower than an interview-based package.

## 5. Resolved Decisions Carried Forward

The following seven UNKNOWN items were resolved in `unknown-resolution-addendum.md` and are carried forward as draft human-selected decisions:

| Area | Carried-forward decision |
|---|---|
| First MVP slice | `Document pipeline only` |
| MVP roles | `Owner / Admin / User` |
| MVP document formats | `PDF + DOCX + TXT/MD` |
| Chunking strategy | Hybrid Markdown section-based chunking with fixed-size fallback for long sections |
| Index storage backend | Abstract `VectorStore` interface, concrete backend not selected |
| Retention policy | Retention policy required, exact duration not fixed |
| Index lifecycle | Full minimal lifecycle: primary indexing, reindex, archive/delete cleanup |

## 6. Engineering Bridge Summary

### Data Model Direction

The implementation contract identifies the likely domain model:

- `Organization`
- `Workspace` or `Tenant`
- `KnowledgeBase`
- `Document`
- `DocumentVersion`
- `DocumentSource`
- `DocumentMetadata`
- `Chunk`
- `EmbeddingRecord`
- `IndexJob`
- `IndexStatus`
- `User`
- `Role`
- `Permission`
- `AccessScope`
- `Query`
- `RetrievalResult`
- `Answer`
- `Citation`
- `AuditEvent`

For the first implementation slice, the strongest engineering direction is to persist organizations, users, roles, knowledge bases, documents, document versions, metadata, chunks, index jobs, index status, and audit events. Retrieval/chat entities should remain draft or deferred unless a later Task Brief explicitly includes them.

### Document Lifecycle

The document lifecycle direction is:

```text
DRAFT
-> UPLOADED
-> PARSING
-> PARSED
-> CHUNKING
-> CHUNKED
-> INDEXING
-> INDEXED
-> AVAILABLE
```

Exception and terminal states:

- `ARCHIVED`
- `DELETED`
- `INDEX_ERROR`

Every state transition should preserve actor, trigger, timestamp, preconditions, failure behavior, visibility, and audit requirements in any future Task Brief.

### RBAC Simplification

The implementation contract explored a broader engineering RBAC matrix, but the addendum narrows the first MVP role set to:

- `Owner`
- `Admin`
- `User`

Draft simplification:

- `Owner`: owns one knowledge base, appoints administrators, deletes the knowledge base.
- `Admin`: invites users, uploads documents, reviews metadata, publishes, archives, deletes documents, and manages document pipeline operations.
- `User`: exists for access-scope and future visibility behavior even if first implementation focuses on the document pipeline.

Exact role/action permissions remain a human-review item before Task Brief generation.

### Indexing Contract

The indexing contract should treat successful indexing as the point where a document version has:

- converted Markdown content;
- sections extracted;
- chunks created;
- embeddings or index records created through the index abstraction;
- index status updated;
- failures captured in visible admin-facing error states;
- audit events recorded for state changes.

Archived or deleted document versions must not remain visible as active RAG sources. Reindex and archive/delete cleanup are part of the selected minimal lifecycle.

### VectorStore Abstraction

The selected direction is an abstract `VectorStore` interface rather than selecting a concrete backend now.

Minimum future interface expectations:

- add embeddings for chunks;
- search within permission-filtered scope;
- return chunk ids and scores;
- hide or delete embeddings for archived/deleted document versions;
- support reindex of a document version;
- detect or expose stale index state.

The concrete backend remains unresolved and must not be assumed.

### MVP Slice Boundary

The first implementation slice is narrowed to `Document pipeline only`.

Included:

- document upload;
- manual text entry;
- metadata extraction;
- manual metadata review;
- document version record;
- Markdown conversion;
- section extraction;
- chunk creation;
- indexing job record;
- index status tracking;
- admin visibility of document processing states.

Excluded from first implementation slice unless explicitly re-authorized:

- full user-facing RAG chat;
- answer generation;
- advanced retrieval/ranking;
- conflict-aware answer synthesis;
- production-grade multi-tenant hardening.

### Remaining UNKNOWN

Remaining UNKNOWN items must stay visible:

- exact role/action matrix for first implementation;
- exact file parsing libraries or services;
- exact Markdown conversion rules for DOCX tables and complex PDFs;
- exact chunk size and overlap values;
- exact `VectorStore` backend;
- exact retrieval mode for future chat layer;
- exact retention durations for audit logs and query history;
- exact restore-from-archive behavior;
- exact conflict detection threshold;
- exact validation commands for a future first implementation Task Brief.

## 7. Readiness For Human Review

Ready for human review:

- product/discovery draft quality;
- implementation contract direction;
- resolved UNKNOWN decisions;
- narrowed first MVP slice;
- remaining UNKNOWN list;
- safety boundary between product workflow approval and AOS approval.

Not ready for execution:

- no Task Brief exists;
- no Risk Profile has been assigned by a human for execution;
- exact permissions, parser choices, chunk sizes, retention duration, and validation commands remain unresolved;
- direct brief mode lowers confidence relative to a problem-interview package.

## 8. Explicit Non-Goals

- No Task Brief yet.
- No implementation yet.
- No production RAG chat in the first MVP slice.
- No release authorization.
- No production use authorization.
- No AOS approval is created by this artifact.
- No domain workflow publish/availability state is treated as AOS approval.

## 9. Final Bridge Status

```yaml
bridge_status: READY_FOR_HUMAN_REVIEW_PACKAGE
approval_status: NOT_APPROVED
execution_status: NOT_AUTHORIZED
ready_for_execution: false
final_process_status: NEEDS_HUMAN_REVIEW
```
