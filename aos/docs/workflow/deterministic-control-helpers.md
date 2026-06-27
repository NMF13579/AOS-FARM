# Deterministic Control Helpers

## Purpose

This document defines the contract for deterministic control helpers inside the
product-facing `aos/` layer.

Deterministic helpers are optional protocol helpers. They may read Markdown or
YAML artifacts, check required fields, detect forbidden claims, and return
deterministic status output for human review.

## Product Folder Boundary

The `aos/` folder is the product-facing layer for transferable workflow guides,
templates, examples, prompts, and optional helper tooling.

The repository root control files remain canonical control sources:
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

The `aos/` layer does not replace those root canonical sources. It packages
product-facing workflow material under the authority of those sources.

Markdown and YAML remain the Source of Truth for workflow definitions,
authorization boundaries, scope boundaries, and human checkpoints described by
the product-facing layer.

## Helper Contract

Deterministic control helpers may:
- read scoped Markdown or YAML artifacts;
- validate required fields and required disclosures;
- detect forbidden claims or missing boundaries;
- report deterministic status such as `PASS`, `BLOCKED`,
  `HUMAN_REVIEW_REQUIRED`, `UNKNOWN_BLOCKED`, or `NOT_RUN`;
- help a human or agent verify that a workflow artifact stays inside its stated
  protocol boundary.

Deterministic control helpers are not runners.

Deterministic control helpers do not approve.

Deterministic control helpers do not assign Risk Profile.

Deterministic control helpers do not authorize execution.

Deterministic control helpers do not commit or push.

Deterministic control helpers do not merge or release.

## Safety Boundary

The following safety rules remain active in the product-facing `aos/` layer:
- PASS is not approval.
- Evidence is not approval.
- CI PASS is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Human approval cannot be simulated.
- protected/canonical changes require human checkpoint.
- destructive operations are forbidden by default.

If a helper output conflicts with Markdown or YAML workflow artifacts, the
artifact remains authoritative until a human updates it through the proper
checkpoint.

## Non-Authority Boundary

Helpers do not convert technical checks into human decisions.

Helpers do not create execution authorization, commit authorization, or push
authorization flags.

Helpers do not mark the agent as the assigner of Risk Profile.

Helpers do not replace human review, human approval, canonical root control
sources, or protected-file checkpoints.

## Stopping Rule

If a helper finds missing authority, missing required fields, forbidden claims,
unknown scope, or a protected/canonical boundary issue, the safe result is
`BLOCKED`, `UNKNOWN_BLOCKED`, or `HUMAN_REVIEW_REQUIRED` according to the
workflow contract being checked.
