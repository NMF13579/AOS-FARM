# AOS-FARM.165 - RAG Dogfood UNKNOWN Resolution Package

```yaml
task_id: AOS-FARM.165
artifact_type: rag_dogfood_unknown_resolution_package
mode: documentation_clarification_only
branch: build/implementation-contract-readiness-gate-mvp
head: b3bb93d51a0c427d4b936eaacaa3a34c4bf72a5c
origin_dev: a3042e8c96ebbba6e7246c9d6e586aa81cda3d27
origin_build_implementation_contract_readiness_gate_mvp: b3bb93d51a0c427d4b936eaacaa3a34c4bf72a5c
source_case: agentos/reports/problem-intake/rag-org-kb-dogfood-2026-06-20
human_confirmation_recorded: true
approval_status: NOT_APPROVED
execution_status: NOT_AUTHORIZED
task_brief_started: false
code_assembly_started: false
dev_integration_authorized: false
release_authorized: false
production_use_authorized: false
recommended_next_step: READINESS_RECHECK_ONLY
final_status: AOS_FARM_165_RAG_DOGFOOD_UNKNOWN_RESOLUTION_PACKAGE_CREATED
```

## Purpose

This package records the human-confirmed clarification decisions for the RAG Org KB dogfood case UNKNOWN items identified by the Implementation Contract Readiness Gate dogfood run.

This package is documentation/clarification only.

It does not approve implementation, does not create or start a Task Brief, does not start Code Assembly, does not authorize dev integration, and does not authorize release or production use.

## Source Context

Prior state:

- Problem interview was skipped and represented as direct draft, not a completed discovery interview.
- AOS-FARM.158 readiness gate result was `UNKNOWN_BLOCKED`.
- Task Brief was not started.
- Code Assembly was not started.
- Runtime, validator suite, and CI were not created.
- AOS-FARM.164 recorded working branch closure with `PASS_WITH_WARNINGS`.

This package narrows the UNKNOWN set enough to support a future readiness recheck. It does not itself change lifecycle state.

## Human-Confirmed Decision Set

```yaml
mvp_slice: document_pipeline_only
user_role_in_first_slice: persist_only_no_user_flows
pdf_docx_support: best_effort_with_warnings
parser_backend: defer_to_task_brief_after_codebase_inspection
chunking: section_first_fallback_1200_tokens_overlap_150
vectorstore_backend: defer_backend_keep_interface
audit_retention: 365_days
processing_log_retention: 90_days
archive_restore: restore_deferred
chat_retrieval: out_of_mvp
validation_policy: discover_existing_commands_then_targeted_tests_not_run_is_not_pass
```

## UNKNOWN Resolution Matrix

| Prior UNKNOWN | Resolution | Status | Task Brief Impact |
|---|---|---|---|
| Exact role/action matrix for first implementation | Use the MVP RBAC matrix below. `User` is persisted only; no user-facing flows in first slice. | RESOLVED_BY_HUMAN_DECISION | Task Brief may scope admin document pipeline actions only. |
| Exact file parsing libraries or services | Use a `DocumentParser` abstraction. Concrete library/service selection is deferred to Task Brief after codebase inspection. | RESOLVED_AS_CONSTRAINED_TASK_BRIEF_DISCOVERY | Task Brief must inspect existing stack and name chosen parser dependency before implementation. |
| Exact Markdown conversion rules for DOCX tables and complex PDFs | Best-effort conversion. Preserve headings, lists, table text, extracted text, and warnings. Ambiguous structure creates `conversion_warning`, not false PASS. | RESOLVED_BY_HUMAN_DECISION | Task Brief must include warning/error behavior. |
| Exact chunk size and overlap values | Section-first chunking; fallback max chunk `1200 tokens`; overlap `150 tokens`; preserve `source_section_id`. | RESOLVED_BY_HUMAN_DECISION | Task Brief may implement chunking against these values. |
| Exact VectorStore backend | Keep abstract `VectorStore` interface; concrete backend deferred because chat/retrieval is out of first MVP slice. | DEFERRED_OUT_OF_MVP_WITH_REASON | Task Brief must not require production vector backend for first slice unless separately authorized. |
| Exact retrieval mode for future chat layer | Out of MVP. Chat/retrieval mode is deferred. | DEFERRED_OUT_OF_MVP_WITH_REASON | No chat/retrieval implementation in first Task Brief. |
| Exact retention durations for audit logs and query history | Audit logs: `365 days`. Document processing logs: `90 days`. Personal query history deferred because chat is out of MVP. | RESOLVED_BY_HUMAN_DECISION | Task Brief may use these minimum retention values for first slice. |
| Exact restore-from-archive behavior | Restore from archive is deferred. First slice supports archive/delete cleanup and hides archived/deleted documents from active index visibility. | DEFERRED_OUT_OF_MVP_WITH_REASON | Task Brief must not implement restore unless separately authorized. |
| Exact conflict detection threshold | Conflict-aware answer synthesis and retrieval conflict threshold are out of MVP because chat/retrieval is out of MVP. | DEFERRED_OUT_OF_MVP_WITH_REASON | No conflict detection threshold needed for first document-pipeline Task Brief. |
| Exact validation commands for first implementation Task Brief | Discover existing repo commands first, then add targeted parser/chunk/index-status tests if runtime exists. `NOT_RUN` remains `NOT_RUN`, not `PASS`. | RESOLVED_AS_VALIDATION_POLICY | Task Brief must list discovered commands and explicit not-run reasons. |

## MVP RBAC Matrix

| Action | Owner | Admin | User | Notes |
|---|---:|---:|---:|---|
| Create/manage knowledge base metadata | YES | NO | NO | Owner owns the knowledge base boundary. |
| Assign or remove admins | YES | NO | NO | Admin assignment remains owner-controlled. |
| Delete or archive knowledge base | YES | NO | NO | Destructive operations require explicit product safeguards in any future Task Brief. |
| Invite users | YES | YES | NO | Admin may invite users for the owned knowledge base scope. |
| Upload documents | YES | YES | NO | First slice is admin document pipeline. |
| Manual text entry | YES | YES | NO | Treated as document input. |
| Review/edit extracted metadata | YES | YES | NO | Required before publish if metadata is uncertain. |
| Publish document version | YES | YES | NO | Publish makes a version visible to active document pipeline state. |
| Archive document version | YES | YES | NO | Archived versions must be hidden from active index visibility. |
| Delete document version | YES | YES | NO | Delete triggers cleanup/hide behavior for chunks and index state. |
| Reindex document version | YES | YES | NO | Reindex is allowed for current document version only. |
| View document processing status | YES | YES | NO | Admin visibility only in first slice. |
| User-facing browse/search/chat | NO | NO | NO | Out of first MVP slice. |

## Document Parsing / Conversion Contract

- `TXT` and `MD`: full first-slice support.
- `PDF` and `DOCX`: accepted with best-effort parsing.
- Parser output must include extracted text or Markdown, source metadata where available, and parser/conversion warnings.
- Complex tables, styling, lists, and PDF layout ambiguity must be represented as warnings when fidelity is uncertain.
- A warning is not a clean PASS.
- Empty extraction, unreadable file, unsupported encryption, or parser failure must produce an explicit failure state.

## Chunking Contract

- Prefer section-based chunks from Markdown structure.
- Fallback to fixed-size chunks when sections are too long or structure is unavailable.
- Fallback max chunk size: `1200 tokens`.
- Fallback overlap: `150 tokens`.
- Preserve source document id, version id, source section id when available, chunk order, and conversion warning references.

## Index / Vector Boundary

The first MVP slice may create document chunk records, indexing job records, index status records, reindex flow, and archive/delete cleanup semantics.

The first MVP slice must not require a concrete production vector database unless a later human-authorized Task Brief explicitly adds it.

## Retention Boundary

- Audit logs: retain for at least `365 days`.
- Document processing logs: retain for at least `90 days`.
- Personal query history: deferred because chat/retrieval is out of MVP.
- Production retention policy remains a future human-approved policy decision.

## Readiness Recheck Recommendation

Recommended next action:

```yaml
next_task_type: readiness_recheck
may_create_task_brief: false
may_start_code_assembly: false
may_authorize_execution: false
expected_question: can_the_updated_decision_set_proceed_toward_task_brief_preparation
```

The future readiness recheck may evaluate whether these decisions are sufficient to prepare a Task Brief draft. The recheck result, even if `READY_FOR_TASK_BRIEF`, is still not approval and still not execution permission.

## Remaining Boundaries

- Direct draft is still not a completed discovery interview.
- This package is not approval.
- This package is not execution authorization.
- This package does not create a Task Brief.
- This package does not start Code Assembly.
- This package does not authorize runtime, validator suite, CI, dev integration, merge, release, or production use.
- `PASS` is not approval.
- Evidence is not approval.
- `UNKNOWN` is not OK.
- `NOT_RUN` is not `PASS`.
- Human approval cannot be simulated.

## Validation Note

This package was created as a new report only.

It does not modify the original RAG dogfood artifacts, protected/canonical sources, gate MVP files, old untracked evidence-tail artifacts, runtime files, validator files, or CI files.
