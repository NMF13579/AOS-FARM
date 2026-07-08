# AOS-FARM.641 — Scope Split Decision Record

## Decision problem

Decide whether terminal and legacy task exclusion work can be implemented safely as one stage or must be split into multiple human-gated stages.

This report is Evidence, not approval.

PASS is validation only, not approval.
Evidence is not approval.
CI PASS is not approval.
UNKNOWN is not OK.
NOT_RUN is not PASS.
EXCLUDED_TERMINAL is not PASS.
EXCLUDED_LEGACY is not PASS.
No blocker is closed by this report.
No blocker is partially remediated by this report.
No implementation is authorized by this report.
No schema change is authorized by this report.
No validator change is authorized by this report.
No registry creation is authorized by this report.
No task file change is authorized by this report.
No merge to main is authorized.
No release is authorized.

## Why implementation should be split

- validator semantics are safety-critical and currently gate every `tasks/*.md` record through `check_task_readiness`;
- legacy invalid ids such as `AOS-FARM.463` require quarantine semantics that cannot safely depend on ordinary valid task-header parsing;
- schema, templates, validator ordering, JSON output, and global aggregation are separate control surfaces and should not move atomically with blocker remediation;
- blockers must remain visible until exclusion semantics are fully specified, implemented, and tested;
- fail-closed rollback is clearer when contract, registry, implementation, and remediation are separated.

## Rejected all-in-one implementation option

Rejected option:

- schema + validator + tests + registry + blocker remediation in one stage

Rejected because:

- creates too much protected drift at once;
- makes it too easy for `EXCLUDED_*` to become implicit `PASS`;
- allows registry semantics to become de facto Source of Truth before checkpointing;
- makes it impossible to tell whether a regression comes from contract, registry, runtime, or remediation changes;
- increases risk that invalid legacy task ids silently stop being audited.

## Selected stage sequence

Selected recommendation:

1. `AOS-FARM.642 — Terminal/Legacy Exclusion Contract and Test Matrix`
2. `AOS-FARM.643 — Legacy Quarantine Registry Contract and Human Checkpoint`
3. `AOS-FARM.644 — Task Readiness Exclusion Schema and Validator Implementation`
4. `AOS-FARM.645 — Existing Blocker Remediation Using Approved Exclusion Semantics`

## Files allowed per future stage

### AOS-FARM.642

Default scope:

- reports only

Potential future implementation-adjacent surfaces only if separately approved:

- `tests/`
- `tests/fixtures/`
- `aos/schemas/task-document-header.schema.json`

### AOS-FARM.643

Potential future surfaces only if separately approved:

- `aos/registry/task-readiness-exclusions.md`
- `aos/schemas/task-document-header.schema.json`
- `tests/`
- `aos/reports/readiness/`

### AOS-FARM.644

Potential future surfaces:

- `aos/scripts/aos_task_document_check.py`
- `aos/scripts/aos_validate.py`
- `aos/scripts/aos_lifecycle_state.py`
- `aos/schemas/task-document-header.schema.json`
- `tests/test_aos_task_document_check.py`
- `tests/test_aos_validate.py`
- `tests/fixtures/...`
- `aos/templates/task-s.md`
- `aos/templates/task-m.md`
- `aos/templates/task-l.md`

### AOS-FARM.645

Potential future surfaces:

- `tasks/`
- `aos/registry/task-readiness-exclusions.md`
- `aos/reports/readiness/`

## Current blockers not closed in 641

- `AOS-FARM-TASK-0001`
- `AOS-FARM-TASK-060101`
- `AOS-FARM-TASK-060102`
- `AOS-FARM.463`

## Current blockers not partially remediated in 641

- `AOS-FARM-TASK-0001`
- `AOS-FARM-TASK-060101`
- `AOS-FARM-TASK-060102`
- `AOS-FARM.463`

## Registry/quarantine as separate human-gated surface

Decision:

- registry/quarantine must be a separate future stage before validator implementation.

Reason:

- `EXCLUDED_LEGACY` semantics depend on explicit witness rules for malformed legacy ids;
- a registry or manifest becomes canonical or lifecycle-adjacent;
- creation or use requires separate human checkpoint, explicit scope, Risk Profile decision, tests, Evidence, and separate commit/push authorization.

AOS-FARM.641 does not create a registry.

## Implementation dependency graph

`classification contract`
→ `witness fields`
→ `registry/quarantine contract`
→ `schema impact decision`
→ `validator ordering`
→ `JSON and audit output contract`
→ `aos_validate.py aggregation`
→ `test matrix`
→ `current blocker remediation`

Dependency rules:

- blocker remediation depends on approved witness model;
- blocker remediation depends on finished validator behavior;
- `AOS-FARM.463` handling depends on registry/quarantine decision;
- schema changes depend on human checkpoint;
- registry creation depends on human checkpoint;
- global readiness behavior depends on explicit `EXCLUDED_* != PASS` tests.

## Human checkpoint map

| Decision | Human checkpoint required |
|---|---|
| Add `EXCLUDED_TERMINAL` / `EXCLUDED_LEGACY` concepts | yes |
| Add terminal witness fields | yes |
| Add `RETIRED` / `SUPERSEDED` statuses | yes |
| Create registry/manifest | yes |
| Apply exclusion to `AOS-FARM.463` | yes |
| Close current blockers | yes |
| Change `aos_validate.py` global PASS behavior | yes |
| Treat `CLOSED` as terminal exclusion | yes |
| Treat `REJECTED` as terminal exclusion | yes |
| Change schema or templates | yes |
| Change validator exit behavior | yes |

## Future failure modes

- `EXCLUDED_TERMINAL` counted as `PASS`;
- `EXCLUDED_LEGACY` counted as `PASS`;
- invalid `task_id` silently accepted;
- wildcard or blanket exclusion introduced;
- registry suppresses blocker without human witness;
- `task --validate-all` skips discovered task files;
- `task --readiness-all` hides excluded tasks;
- `aos_validate.py --json` reports global `PASS` when malformed exclusions exist;
- `CLOSED` becomes escape hatch;
- `REJECTED` becomes false success state;
- `NOT_RUN` treated as `PASS`;
- Evidence treated as approval;
- CI PASS treated as approval;
- current blockers remediated before semantics exist.

Rollback boundary:

- fail closed;
- preserve audit output;
- revert by ordinary revert commit;
- no destructive cleanup;
- no history rewrite.

## Risks

- safety regression in readiness semantics;
- lifecycle-adjacent drift through schema/template/runtime mismatch;
- registry drift between task files and exclusion manifest;
- hidden normalization of malformed legacy task ids;
- false green aggregate status in `aos_validate.py`.

## Dependency order

Recommended dependency order is:

1. define exclusion concepts and witness contract
2. decide and gate legacy registry/quarantine model
3. implement schema and validator semantics
4. prove aggregation and test matrix
5. remediate existing blockers only after semantics are real

## Final recommendation

Reject all-in-one implementation.

Recommend a four-stage downstream split:

1. `AOS-FARM.642` for contract and test matrix
2. `AOS-FARM.643` for registry/quarantine contract and human checkpoint
3. `AOS-FARM.644` for schema/validator implementation
4. `AOS-FARM.645` for current blocker remediation under approved semantics

## Evidence boundary

Explicit statement:

Evidence, not approval.
