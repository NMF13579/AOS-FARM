# TA 25 Dogfood Input

## Problem Statement

The Technical Assignment intake process needs to convert an existing user brief into reviewable draft artifacts without implying approval or execution authorization.

## Target User

AOS human operator and IDE/controller agent preparing a scoped implementation task.

## Current Workflow

The operator writes a free-form brief, then the agent manually extracts project intent, requirements, open questions, and review boundaries.

## Desired Outcome

Create deterministic draft artifacts for existing-spec review: `PROJECT_SPEC.draft.md`, `REQUIREMENTS.draft.md`, a problem report, a checklist, validator evidence, and a human review package candidate.

## Constraints

- The generated artifacts must remain drafts.
- The output must not approve execution.
- The output must not create a final Task Brief.
- Unknowns must remain visible and blocking.

## Known Risks

- False readiness claims.
- Approval boundary drift.
- Treating validator evidence as approval.

## Open Questions

- Human must confirm the final allowed file set before implementation.
- Human must confirm whether the generated candidate requirements are acceptable.

## Data Discovery

The source brief contains problem, user, current workflow, target outcome, constraints, risks, open questions, and acceptance criteria.

## Information Flow

Existing brief -> TA intake drafts -> bridge candidate inputs -> validator evidence -> Human Review Package.

## Access / Permissions

Only the human operator may approve execution, commit, push, release, or production use.

## Requirements

- Preserve safety fields in every generated draft.
- Set `ready_for_execution: false`.
- Set `execution_authorized: false`.
- Set `implementation_authorized: false`.
- Carry open questions into UNKNOWN / Human Decisions Required.

## Acceptance Criteria

- Required draft files are generated.
- Validator report is generated.
- UNKNOWN remains visible.
- No output declares approval or execution authorization.

## MVP

Automate only `EXISTING_SPEC_REVIEW`; interview routes remain manual.

## Implementation Hints

Use deterministic Markdown extraction and structural validator checks only.

## Contradictions

None known in the fixture input.
