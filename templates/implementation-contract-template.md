# Implementation Contract Template

```yaml
artifact_type: implementation_contract
artifact_status: DRAFT
approval_status: NOT_APPROVED
execution_status: NOT_AUTHORIZED
ready_for_task_brief: false
```

## 1. Source Inputs

- Project / case id:
- Input route: `[PROBLEM_INTERVIEW | DIRECT_BRIEF | OTHER]`
- Source artifacts:
  - `PROJECT_SPEC`:
  - `REQUIREMENTS`:
  - problem interview:
  - human review notes:
- Source confidence:
- Known source limitations:

## 2. Implementation Goal

Describe the engineering goal in implementation-ready terms.

## 3. In Scope

List only capabilities, objects, states, and interfaces included in the proposed implementation contract.

## 4. Out of Scope

List excluded capabilities, deferred features, and explicitly forbidden assumptions.

## 5. Data Model

For each entity:

- entity name:
- purpose:
- key fields:
- relationships:
- ownership:
- uniqueness constraints:
- lifecycle/state fields:
- audit requirements:
- UNKNOWN:

## 6. State Machine / Lifecycle

For each stateful object:

- object:
- states:
- allowed transitions:
- blocked transitions:
- actor or system trigger:
- failure states:
- terminal states:
- UNKNOWN:

## 7. RBAC / Permissions

- roles:
- permissions by role:
- visibility rules:
- ownership rules:
- administrative actions:
- forbidden actions:
- cross-tenant or cross-organization boundaries:
- UNKNOWN:

## 8. API / Interface Contracts, If Applicable

For each interface:

- interface name:
- caller:
- inputs:
- outputs:
- authorization rules:
- failure modes:
- idempotency or retry behavior:
- evidence/logging expectations:
- UNKNOWN:

## 9. Storage / Persistence Contracts, If Applicable

- persistence model:
- required records:
- derived records:
- immutable records:
- retention expectations:
- archival behavior:
- deletion behavior:
- migration assumptions:
- UNKNOWN:

## 10. Error Handling

- user-visible errors:
- administrator-visible errors:
- retryable failures:
- non-retryable failures:
- partial-success behavior:
- unsupported input behavior:
- escalation to human review:
- UNKNOWN:

## 11. Nonfunctional Constraints

- security:
- privacy:
- performance:
- availability:
- auditability:
- traceability:
- maintainability:
- portability:
- operational visibility:
- UNKNOWN:

## 12. Observability / Evidence Expectations

- required logs:
- required reports:
- required status fields:
- required validation outputs:
- evidence files expected:
- NOT_RUN disclosures:
- UNKNOWN disclosures:

## 13. Safety Boundaries

- This contract is not approval.
- This contract is not execution authorization.
- This contract does not write product code.
- This contract does not start Code Assembly Pipeline.
- `PASS` does not equal approval.
- Evidence does not equal approval.
- `UNKNOWN` does not equal OK.
- `NOT_RUN` does not equal PASS.
- Human approval cannot be simulated.

## 14. Remaining UNKNOWN

| UNKNOWN | Source location | Why it matters | Blocks Task Brief? | Human decision needed |
|---|---|---|---|---|
| | | | | |

## 15. Implementation Readiness Decision

Allowed values:

- `READY_FOR_MVP_SLICE_PLAN_WITH_WARNINGS`
- `HUMAN_REVIEW_REQUIRED`
- `UNKNOWN_BLOCKED`
- `NOT_READY_FOR_TASK_BRIEF`

Decision:

```text
UNKNOWN_BLOCKED
```

Reason:

## 16. Human Review Requirements

- decisions required:
- risk profile required:
- protected/canonical review required:
- execution authorization required:
- questions before Task Brief:
