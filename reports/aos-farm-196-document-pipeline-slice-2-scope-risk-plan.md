# AOS-FARM.196 — Document Pipeline Slice 2 Scope and Risk Plan

## Current State (Slice 1)
- Ingests single files (TXT/MD/PDF/DOCX).
- Extracts metadata and calculates deterministic document ID (sha256).
- Has warnings for PDF/DOCX, and rejects other extensions.
- Returns `DocumentPipelineRecord` for a single document.
- Local execution only, no RAG, no network.

## Slice 2 Scope Definition
Goal: Implement the second minimal Document Pipeline slice focusing on batch document intake and local manifest generation.

Allowed Features:
- Batch document intake (processing multiple paths).
- Local manifest generation (`DocumentManifest` holding multiple records).
- Deterministic document status registry (registry by document ID).
- Stable output shape.
- Structured warning/error aggregation at the manifest level.
- Duplicate path/content handling (deduplicating by document ID).
- Bounded tests for multiple local documents.

Allowed Files:
- `agentos/pipelines/document_pipeline.py` (update)
- `tests/test_document_pipeline.py` (update)
- `agentos/pipelines/document_manifest.py` (new)
- `tests/test_document_manifest.py` (new)

Forbidden Features:
- chat-first RAG, retrieval chat, source-linked answers
- analytics, browsing, production RAG
- network dependency
- full validator suite, CI workflow, release
- destructive operations, cleanup
- protected/canonical changes

## Risk Profile Proposal
Proposed Risk Profile: **HIGH_RISK_PROTECTED**

Rationale:
This step expands pipeline capabilities to handle batches and manifest schemas. While it operates locally, ensuring deterministic and stable structures is critical for future retrieval components. A high risk profile ensures proper human checkpointing and boundary enforcement.
