# Sensitive High Impact Fixture Input

## Problem Statement

The team wants a technical assignment for reviewing access to sensitive operational incident records.

## Target User

Security and operations reviewers.

## Current Workflow

Incident details are shared manually with uneven access controls.

## Desired Outcome

Produce draft requirements that expose privacy, security, and human approval gates before any implementation work.

## Constraints

- Do not process real sensitive data in this fixture.
- Do not approve access model changes.
- Do not authorize implementation or production use.

## Known Risks

- Sensitive operational records may include private or security-relevant information.
- Access changes may affect protected workflows.
- Human review is mandatory before execution.

## Open Questions

- What exact data classes are in scope?
- Who is authorized to view each class?
- What retention and audit requirements apply?
- Is a separate domain checkpoint required?

## Data Discovery

Only synthetic fixture content is used. Real data classes are unknown.

## Information Flow

Sensitive incident notes -> candidate requirements -> human review package.

## Access / Permissions

Access roles, audit requirements, and approval authority are not confirmed.

## Requirements

- Mark sensitive scope as needing human review.
- Preserve security and privacy unknowns.
- Keep execution authorization false.

## Acceptance Criteria

- Generated drafts show privacy/security blockers.
- Validator report remains structural evidence only.

## MVP

Candidate documentation only, no runtime or production processing.

## Implementation Hints

No code implementation should be inferred from this fixture.
