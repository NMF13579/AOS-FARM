# RAG Org KB UNKNOWN Resolution Addendum

```yaml
dogfood_run_id: rag-org-kb-dogfood-2026-06-20
artifact_type: unknown_resolution_addendum
artifact_status: DRAFT
approval_status: NOT_APPROVED
execution_status: NOT_AUTHORIZED
ready_for_execution: false
final_process_status: NEEDS_HUMAN_REVIEW
source_artifact: implementation-contract-draft.md
```

## Purpose

This addendum records human-selected resolutions for key UNKNOWN items discovered during the RAG Org KB dogfood package.

This addendum does not approve implementation, does not create a Task Brief, and does not make the package ready for execution.

## Resolved UNKNOWN Items

| UNKNOWN | Resolution | Status |
|---|---|---|
| First MVP slice | Document pipeline only | HUMAN_SELECTED_DRAFT_DECISION |
| MVP roles | Owner / Admin / User | HUMAN_SELECTED_DRAFT_DECISION |
| MVP document formats | PDF + DOCX + TXT/MD | HUMAN_SELECTED_DRAFT_DECISION |
| Chunking strategy | Hybrid: Markdown section-based chunking + fixed-size fallback for long sections | HUMAN_SELECTED_DRAFT_DECISION |
| Index storage backend | Abstract `VectorStore` interface, backend not selected | HUMAN_SELECTED_DRAFT_DECISION |
| Retention policy | Required, but exact retention duration not fixed in MVP contract | HUMAN_SELECTED_DRAFT_DECISION |
| Index lifecycle | Full minimal lifecycle: primary indexing + reindex + archive/delete cleanup | HUMAN_SELECTED_DRAFT_DECISION |

## MVP Slice Resolution

Selected first MVP slice: `Document pipeline only`.

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

Excluded from first MVP slice:

- full user-facing RAG chat;
- answer generation;
- advanced retrieval/ranking;
- conflict-aware answer synthesis;
- production-grade multi-tenant hardening.

## Role Resolution

Selected MVP roles:

- `Owner`
- `Admin`
- `User`

Draft role meaning:

- `Owner`: owns one knowledge base, can assign administrators, and can delete the knowledge base.
- `Admin`: can invite users, upload documents, review metadata, publish, archive, delete documents, and manage document pipeline operations.
- `User`: exists for role-based access scope and future document/search/chat visibility, even if first MVP focuses on document pipeline.

## Document Format Resolution

Selected MVP document formats:

- `PDF`
- `DOCX`
- `TXT`
- `MD`

Engineering warning:

`DOCX` increases parsing complexity because headings, tables, lists, and styling may not map cleanly into Markdown sections. This must be reflected in future validation and error handling.

## Chunking Resolution

Selected chunking strategy:

`Hybrid section-based chunking + fixed-size fallback`.

Draft behavior:

- convert document to Markdown;
- identify sections from Markdown structure;
- create chunks tied to source sections;
- split overly long sections with fixed-size fallback;
- preserve source section identity for later citation and highlighting.

## Index Storage Resolution

Selected index storage approach:

`Abstract VectorStore interface`.

Draft contract:

- persistent application storage keeps organizations, users, roles, documents, versions, chunks, jobs, and audit logs;
- embedding/search backend is accessed through `VectorStore`;
- concrete backend remains a future implementation decision.

Minimum `VectorStore` capabilities:

- add embeddings for chunks;
- search within permission-filtered scope;
- return chunk ids and scores;
- hide or delete embeddings for archived/deleted document versions;
- support reindex of a document version;
- detect or expose stale index state.

## Retention Resolution

Selected retention policy:

`Retention policy required, exact duration not fixed`.

Draft behavior:

- audit log is required;
- personal query history is required;
- unanswered/popular query analytics may be aggregated for owners/admins;
- exact retention duration remains a policy/configuration decision;
- production use requires human-approved retention policy.

## Index Lifecycle Resolution

Selected index lifecycle:

`Full minimal lifecycle`.

Included:

- primary indexing;
- reindex current version;
- archive/delete index cleanup;
- hide or remove chunks/embeddings for archived and deleted versions;
- stale index detection.

Reason:

Archived or deleted documents must not remain visible as active RAG sources.

## Remaining UNKNOWN Items

These items remain unresolved and must not be treated as OK:

- exact role/action matrix for first implementation;
- exact file parsing libraries or services;
- exact Markdown conversion rules for DOCX tables and complex PDFs;
- exact chunk size and overlap values;
- exact VectorStore backend;
- exact retrieval mode for future chat layer;
- exact retention durations for audit logs and query history;
- exact restore-from-archive behavior;
- exact conflict detection threshold;
- exact validation commands for first implementation Task Brief.

## Human Review Questions Before Task Brief

Priority questions:

- Should first implementation include any user-facing document browsing, or only admin document pipeline?
- Should `User` role be persisted in the first slice even if chat/search is deferred?
- What is the minimum acceptable DOCX/PDF parsing fidelity for MVP?
- Should archived document versions be recoverable or read-only archive only?
- Which object actions must be audited in the first Task Brief?

## Safety Boundary

- This addendum is not approval.
- This addendum is not execution authorization.
- This addendum does not create a Task Brief.
- This addendum does not authorize implementation.
- This addendum does not authorize production use.
- `DRAFT` remains `DRAFT`.
- `NEEDS_HUMAN_REVIEW` remains active.

## Final Status

```yaml
artifact_status: DRAFT
approval_status: NOT_APPROVED
execution_status: NOT_AUTHORIZED
ready_for_execution: false
final_process_status: NEEDS_HUMAN_REVIEW
```
