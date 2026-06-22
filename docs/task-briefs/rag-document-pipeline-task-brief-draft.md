# AOS-FARM.184 - Scoped RAG Document Pipeline Task Brief Draft

```yaml
task_id: AOS-FARM.184
artifact_type: scoped_task_brief_draft
status: DRAFT_FOR_HUMAN_REVIEW_ONLY
repository: AOS-FARM
branch: build/implementation-contract-readiness-gate-mvp
risk_profile_assigned_by_human: MEDIUM_RISK_GUIDED
authorization_checkpoint: reports/human-checkpoints/aos-farm-182-task-brief-creation-authorization.md
authorized_scope: Document pipeline only
implementation_authorized: false
code_assembly_authorized: false
runtime_authorized: false
validator_suite_authorized: false
ci_authorized: false
release_authorized: false
production_use_authorized: false
```

## Purpose

Draft a scoped future implementation task brief for the first RAG-related product slice, limited strictly to the document pipeline.

This draft is for human review only. It does not authorize implementation, Code Assembly, runtime, validator suite, CI, release, or production use.

## Source Inputs

- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
- `reports/aos-farm-181-final-dev-remote-baseline-closure.md`
- `reports/aos-farm-182-task-brief-scope-and-authorization-package.md`
- `reports/human-checkpoints/aos-farm-182-task-brief-creation-authorization.md`
- `reports/aos-farm-165-rag-dogfood-unknown-resolution-package.md`
- `reports/aos-farm-166-rag-dogfood-readiness-recheck.md`

## Strict Scope

The future implementation task, if separately authorized later, must be limited to:

```yaml
product_scope: Document pipeline only
allowed_runtime_surface: not_authorized_by_this_draft
allowed_code_assembly_surface: not_authorized_by_this_draft
```

Allowed product behavior to describe for a future implementation task:

- document intake;
- file metadata;
- best-effort parser boundary;
- DOCX/PDF handling as warnings or bounded behavior if already defined;
- resolved chunking policy;
- storage/indexing boundary for document pipeline only;
- validation commands as planned checks, not executed PASS unless actually run.

## Non-Goals

The following are out of scope:

- chat-first RAG;
- chat UI;
- retrieval chat;
- source-linked answer generation;
- analytics;
- browsing;
- conflict handling;
- production RAG;
- full RBAC implementation;
- archive restore implementation;
- Code Assembly execution;
- implementation execution;
- runtime implementation;
- validator suite implementation;
- CI implementation;
- release;
- production use.

## Assumptions

- The first slice remains Document pipeline only.
- The full interview gap remains and must be disclosed in future review.
- Validation quality gap remains and must be disclosed in future review.
- Old unrelated untracked artifacts require a separate cleanup line.
- Existing old/local AOS-FARM.184 Step 9 validator artifacts are unrelated numeric-collision artifacts and must not be touched.
- Parser library or service selection requires future codebase inspection before implementation.
- Validation commands must be discovered from the repository during a future implementation planning step.

## UNKNOWN / Deferred Items

| Item | Status | Required handling |
|---|---|---|
| Full interview gap | CARRIED_FORWARD | Disclose in all future review and implementation authorization materials. |
| Validation quality gap | CARRIED_FORWARD | Planned checks must not be reported as PASS unless actually run. |
| Parser dependency selection | DEFERRED_TO_FUTURE_CODEBASE_INSPECTION | Future implementation task must inspect the existing stack before selecting libraries/services. |
| Production vector backend | OUT_OF_SCOPE | Do not implement unless separately authorized. |
| Chat/retrieval behavior | OUT_OF_SCOPE | Do not implement in the document-pipeline slice. |
| Archive restore | OUT_OF_SCOPE | Do not implement unless separately authorized. |
| Conflict-aware answer synthesis | OUT_OF_SCOPE | Do not implement in the document-pipeline slice. |
| Old unrelated untracked artifacts | SEPARATE_CLEANUP_LINE | Do not touch as part of this line. |

## Required Files / Artifacts for a Future Implementation Task

A future implementation task brief must identify exact code files only after codebase inspection. At minimum, it must include:

- exact file list for document intake changes;
- exact file list for file metadata changes;
- exact parser boundary or adapter files, if implementation is later authorized;
- exact storage/indexing files for document-pipeline-only state, if implementation is later authorized;
- exact test/check commands discovered from the repository;
- explicit `NOT_RUN` entries for checks that are planned but not executed;
- explicit evidence files and expected final report paths.

This draft does not create or authorize those implementation files.

## Validation Plan

Validation for a future implementation task must be recorded as planned checks until actually run. It should include:

- repository command discovery;
- existing unit/integration test command discovery, if present;
- targeted parser warning behavior checks, if implementation is later authorized;
- targeted chunking policy checks, if implementation is later authorized;
- targeted document metadata and indexing-status checks, if implementation is later authorized;
- negative checks confirming no chat UI, retrieval chat, source-linked answer generation, analytics, browsing, conflict handling, or production RAG behavior was added.

`NOT_RUN` must remain `NOT_RUN`. Planned validation is not PASS.

## Safety Boundaries

- Task Brief draft does not authorize implementation.
- Code Assembly remains unauthorized.
- Runtime remains unauthorized.
- Validator suite remains unauthorized.
- CI remains unauthorized.
- Release remains unauthorized.
- Production use remains unauthorized.
- Human review is required before any implementation lifecycle transition.
- PASS is not approval.
- Evidence is not approval.
- CI PASS is not approval.
- Readiness Gate result is not approval.
- `READY_FOR_TASK_BRIEF` is not approval.
- `UNKNOWN` is not OK.
- `NOT_RUN` is not PASS.
- Human approval cannot be simulated.

## Final Boundary Rule

This document is a draft Task Brief for human review only.

It does not authorize implementation, Code Assembly, runtime, validator suite, CI, release, production use, protected/canonical changes, cleanup, destructive operations, staging, commit, or push.

