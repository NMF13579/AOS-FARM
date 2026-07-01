# Missing Data Discovery Fixture Input

## Problem Statement

The project needs intake drafts for a reporting workflow, but the source brief does not identify the data inventory.

## Target User

Operations lead reviewing internal reports.

## Current Workflow

Reports are assembled manually from notes and chat summaries.

## Desired Outcome

Create draft requirements that expose missing data discovery before implementation.

## Constraints

- Do not infer data sources.
- Do not infer retention policy.
- Do not authorize implementation while data discovery is unknown.

## Known Risks

Unknown data sources may hide privacy, ownership, or access-control requirements.

## Open Questions

- What data sources are used?
- What fields are sensitive?
- Who owns the source data?
- What retention policy applies?

## Information Flow

Notes and summaries are expected to become reviewable requirements, but exact source systems are unknown.

## Access / Permissions

Access model is not confirmed.

## Requirements

- Mark data discovery as missing.
- Require human review before execution.
- Preserve visible UNKNOWN items.

## Acceptance Criteria

- Generated drafts expose missing data discovery.
- Validator evidence does not convert missing data into approval.

## MVP

Create candidate drafts only.
