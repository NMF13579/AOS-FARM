# RAG Organization Knowledge Base Dogfood Input

## Problem Statement

Organizations need a universal RAG system that gives users fast access to current internal information while preserving source traceability, role-based access, and controlled document lifecycle.

## Target User

- Knowledge base owner.
- Knowledge base administrator.
- Organization user with one or more job roles.

## Current Workflow

The target workflow is being defined directly from an existing brief without a problem interview. The system is intended for organizations that need searchable internal knowledge with source-linked answers and controlled document access.

## Desired Outcome

Create a draft technical assignment for a multi-organization RAG platform where organizations can create one or more knowledge bases, upload or author documents, manage access by job role, and provide chat answers linked to exact source sections.

## Constraints

- This dogfood run skips problem interview and proceeds as direct TA draft.
- Resulting artifacts must remain `DRAFT`.
- No artifact may imply execution or implementation authorization.
- Organizations only; no personal user knowledge bases in this scope.
- Access visibility is determined by job roles, and a user may hold multiple roles.
- Published documents become user-available only after conversion, sectioning, chunking, and indexing complete.

## Known Risks

- Role and access combinations can become complex across multiple organizations and multiple bases.
- Workflow approval inside the app must not be confused with AOS approval semantics.
- Conflict detection between documents may surface inconsistent information that still requires human judgment.
- Automatic metadata extraction and version detection may be imperfect and need administrator correction.

## Open Questions

- Exact ranking logic for multi-base retrieval is not defined.
- Precise tagging taxonomy is not defined.
- Detailed invitation and account lifecycle edge cases are not fully defined.
- Exact analytics depth beyond unanswered/popular queries is not finalized.

## Data Discovery

Core objects include organizations, knowledge bases, users, roles, invitations, documents, document versions, sections, chunks, chat answers, document sources, access rules, audit log entries, and analytics aggregates for unanswered and popular queries.

## Information Flow

Organization owner creates knowledge base -> invites users -> assigns administrators -> administrators/owners upload file or enter text -> system extracts metadata -> administrator reviews metadata -> document becomes draft or published -> published document converts to Markdown -> splits into sections -> chunks and indexes -> users search or ask chat questions across allowed bases -> answers link back to source documents and highlighted sections.

## Access / Permissions

- One knowledge base has exactly one owner at a time.
- Owner and administrator can upload documents and manage access by role.
- Only owner can appoint administrators and delete a knowledge base.
- Owner and administrator can invite users.
- Archived and processing/error states are visible only to owner and administrator.
- Users may belong to multiple organizations and search across one, several, or all accessible bases.

## Requirements

- Users can ask chat questions and browse documents.
- Each answer segment must link to a source document and highlighted section.
- Access is controlled by job roles, and users may have multiple roles.
- Owners and administrators can upload file-based or text-authored documents.
- Metadata is extracted automatically and verified manually before acceptance.
- Documents may be draft, processing, available, error, or archived.
- New versions archive old versions.
- Conflicts are detected and shown, but not auto-blocked.
- Audit logging captures all documentation and user-related changes.

## Acceptance Criteria

- Draft artifacts describe the RAG system scope, document lifecycle, access model, and source-traceable answer behavior.
- UNKNOWN items remain visible.
- No artifact claims approval or execution authorization.
- The direct TA route is explicitly recorded as lower-confidence than a problem interview route.

## MVP

First scope is organizational knowledge bases only, with chat, document browsing, role-based access, document lifecycle handling, unanswered/popular query analytics, and source-linked answers.

## Implementation Hints

- Main user entry is chat-first.
- Search scope can be all accessible bases, several selected bases, or one selected base.
- Answer traceability down to Markdown section is essential.

## Contradictions

- None explicitly identified yet, but document conflict detection is a required product behavior.
