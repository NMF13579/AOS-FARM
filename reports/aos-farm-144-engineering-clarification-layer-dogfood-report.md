# AOS-FARM.144 Engineering Clarification Layer Dogfood Report

```yaml
task_id: AOS-FARM.144
artifact_type: dogfood_report
artifact_status: DRAFT
approval_status: NOT_APPROVED
execution_status: EXECUTION_REPORTED
case_used: rag-org-kb-dogfood-2026-06-20
ready_for_task_brief: false
final_status: HUMAN_REVIEW_REQUIRED
```

## 1. Case Used

Dogfood case:

`agentos/reports/problem-intake/rag-org-kb-dogfood-2026-06-20`

Reason:

- It is the existing complex technical case that already showed `PROJECT_SPEC` and `REQUIREMENTS` are not enough for agent coding.
- It includes `PROJECT_SPEC.draft.md`, `REQUIREMENTS.draft.md`, an implementation contract draft, and an UNKNOWN resolution addendum.

## 2. PROJECT_SPEC / REQUIREMENTS Input Summary

The case describes a multi-organization RAG knowledge base platform where owners/admins manage knowledge bases, documents, users, roles, versions, analytics, and audit logs, while users search or ask questions against only visible information.

Key requirements include:

- organizations with one or more knowledge bases;
- one owner per knowledge base;
- admins and owners managing users and documents;
- file upload and direct text input;
- metadata extraction with admin review;
- Markdown conversion, sectioning, chunking, and indexing;
- source-linked answers;
- version/archive handling;
- conflict disclosure;
- unanswered/popular query analytics;
- audit logging.

Input confidence warning:

- problem interview was skipped;
- requirements confidence is medium;
- access permissions are partial;
- UNKNOWN remains blocking for implementation.

## 3. Engineering Clarification Output Summary

The Engineering Clarification layer adds implementation-relevant structure:

- a normalized entity model;
- document and indexing lifecycle;
- role/permission boundary;
- first MVP slice narrowed to document pipeline only;
- `VectorStore` abstraction instead of choosing a concrete backend;
- parsing/chunking/indexing contract warnings;
- remaining human decisions before Task Brief.

## 4. Data Model

Draft entities identified:

- Organization
- Workspace or Tenant
- KnowledgeBase
- Document
- DocumentVersion
- DocumentSource
- DocumentMetadata
- Chunk
- EmbeddingRecord
- IndexJob
- IndexStatus
- User
- Role
- Permission
- AccessScope
- Query
- RetrievalResult
- Answer
- Citation
- AuditEvent

MVP slice warning:

The first MVP should not implement the full chat/retrieval answer model. For the selected document-pipeline slice, entities after indexing can remain future-contract references.

## 5. State Machine

Important state machines:

- document source intake: uploaded/authored -> metadata extracted -> admin review;
- document version: draft -> processing -> available -> archived or error;
- indexing job: queued -> running -> succeeded or failed;
- index status: not indexed -> current -> stale -> failed -> archived/removed;
- invitation/account lifecycle: partially known and still unresolved.

## 6. RBAC

Draft MVP roles:

- Owner
- Admin
- User

Draft role boundary:

- Owner can manage knowledge base ownership, assign administrators, and delete the knowledge base.
- Admin can invite users, upload documents, review metadata, publish/archive/delete documents, and manage document pipeline operations.
- User exists for visibility scoping and future search/chat, even if first MVP focuses on document pipeline.

Remaining RBAC UNKNOWN:

- exact role/action matrix;
- multi-organization membership edge cases;
- category-level versus document-level visibility selector;
- whether `User` role should be persisted in the first document-pipeline slice.

## 7. MVP Slice Boundary

Selected first MVP slice:

`Document pipeline only`

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
- admin visibility of processing states.

Excluded:

- full user-facing RAG chat;
- answer generation;
- advanced retrieval/ranking;
- conflict-aware answer synthesis;
- production-grade multi-tenant hardening.

## 8. Technical Contracts

Draft contracts:

- input formats: PDF, DOCX, TXT, MD;
- conversion: source documents convert to Markdown before section/chunk processing;
- chunking: Markdown section-based chunking plus fixed-size fallback for long sections;
- indexing: `IndexJob` and `IndexStatus` record work and searchability state;
- vector storage: abstract `VectorStore` interface, concrete backend unresolved;
- archive/delete cleanup: archived/deleted documents must not remain visible as active sources.

## 9. Error Handling

Required error handling:

- unsupported file format;
- conversion failure;
- metadata extraction failure;
- admin rejection or correction;
- indexing failure;
- stale index detection;
- archive/delete cleanup failure.

Failures must be visible to owners/admins and must not be converted into PASS.

## 10. Nonfunctional Constraints

Required constraints:

- source traceability;
- organization/tenant isolation;
- role-based visibility enforcement;
- audit logging for user and document changes;
- retention policy for audit/query history;
- operational visibility into document processing states.

Production warning:

Retention duration, concrete vector backend, and parsing fidelity are not fixed. Production use remains unauthorized.

## 11. Remaining UNKNOWN

Count: 10

Remaining UNKNOWN list:

1. Exact role/action matrix for first implementation.
2. Exact file parsing libraries or services.
3. Exact Markdown conversion rules for DOCX tables and complex PDFs.
4. Exact chunk size and overlap values.
5. Exact VectorStore backend.
6. Exact retrieval mode for future chat layer.
7. Exact retention durations for audit logs and query history.
8. Exact restore-from-archive behavior.
9. Exact conflict detection threshold.
10. Exact validation commands for first implementation Task Brief.

## 12. Task Brief Readiness

Result:

```text
NOT_READY_FOR_TASK_BRIEF
```

Reason:

The case is closer to Task Brief readiness after Engineering Clarification, but unresolved RBAC, parsing, chunking, backend, retention, archive, conflict, and validation decisions still affect implementation scope and validation.

Recommended next step:

Create a targeted UNKNOWN Resolution Addendum for the document-pipeline MVP before drafting a Task Brief.

## 13. Safety Boundary

- This dogfood report is Evidence, not approval.
- This report does not authorize implementation.
- This report does not start Code Assembly Pipeline.
- `UNKNOWN` does not equal OK.
- `NOT_RUN` does not equal PASS.
