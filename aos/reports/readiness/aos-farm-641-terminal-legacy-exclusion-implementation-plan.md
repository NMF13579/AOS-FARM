# AOS-FARM.641 — Terminal and Legacy Task Exclusion Implementation Plan

## Stage title

AOS-FARM.641 — Terminal and Legacy Task Exclusion Implementation Planning and Scope Split

## Status

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

## Source review

Reviewed required canonical sources in required order:

1. `00_AOS_Core_Control.md`
2. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
3. `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

Reviewed AOS-FARM.640 design basis:

- `aos/reports/readiness/aos-farm-640-terminal-state-semantics-design.md`
- `aos/reports/readiness/aos-farm-640-legacy-blocker-exclusion-decision-record.md`

Applied source conclusions:

- fail closed on unknown or ambiguous semantics;
- approval, readiness, validation, and Evidence must stay separate;
- lifecycle-adjacent and canonical surfaces require human checkpointing;
- protected implementation must not be merged with blocker remediation.

## Baseline validation

Branch baseline:

- branch: `build/aos-farm-641-terminal-legacy-exclusion-implementation-planning`
- `HEAD`: `07ea2b5bed5a89874378f3c218e1a3dbcc7129b2`
- `origin/dev`: `07ea2b5bed5a89874378f3c218e1a3dbcc7129b2`
- `origin/main`: `e77d8011b84946340e428db2c7547f0285be0713`
- `origin/dev...HEAD`: `0 0`

Baseline command summary from `/.aos-tmp/`:

| Command | Result | Exit | Interpretation |
|---|---:|---:|---|
| `python3 aos/scripts/aos_validate.py --json` | `UNKNOWN_BLOCKED` | `0` | Expected aggregate fail-closed because readiness is failing. |
| `python3 aos/scripts/aos_task_document_check.py task --readiness-all` | `FAILED` | `1` | Expected; same four blockers remain visible. |
| `python3 aos/scripts/aos_task_document_check.py task --validate-all` | `PASS` | `0` | Expected; task discovery and structural validation still pass. |
| `python3 aos/scripts/aos_architecture_document_check.py validate-all --json` | `PASS` | `0` | Expected. |
| `python3 -m unittest discover -s tests` | `PASS` | `0` | Expected. |
| `git diff --check` | `PASS` | `0` | Expected. |

Observed readiness blockers remain:

- `AOS-FARM-TASK-0001`
- `AOS-FARM-TASK-060101`
- `AOS-FARM-TASK-060102`
- `AOS-FARM.463`

## AOS-FARM.640 design summary

AOS-FARM.640 established the safe future direction and preserved these constraints:

- `task --validate-all` must keep discovering every `tasks/*.md`.
- `task --readiness-all` must not silently skip excluded tasks.
- any future terminal exclusion must emit `EXCLUDED_TERMINAL`, not `PASS`.
- any future legacy exclusion must emit `EXCLUDED_LEGACY`, not `PASS`.
- malformed exclusion attempts must fail closed.
- malformed legacy ids such as `AOS-FARM.463` may require a separate human-gated registry or manifest rather than header-only witness.

## Current blockers

| Blocker | Current issue | Future treatment boundary in this plan |
|---|---|---|
| `AOS-FARM-TASK-0001` | `risk_profile: UNKNOWN_BLOCKED`, not approved, not execution-authorized, `validator_status: NOT_RUN`, `evidence_status: NOT_RUN` | Remains active blocker until future remediation or valid terminal witness exists. |
| `AOS-FARM-TASK-060101` | human-assigned risk exists, but readiness still blocks on approval/execution/evidence/validator status | Remains active blocker until future remediation or valid terminal witness exists. |
| `AOS-FARM-TASK-060102` | unknown risk and other readiness gaps remain | Remains active blocker until future remediation or valid terminal witness exists. |
| `AOS-FARM.463` | invalid legacy `task_id` plus ordinary readiness gaps | Candidate only for future legacy quarantine or migration path after separate checkpointed implementation. |

## Current validator/schema/test surfaces

Current implementation facts from read-only inspection:

- `aos/scripts/aos_task_document_check.py` enforces `task_id` regex `^AOS-FARM-TASK-\d+$` inside `check_task_readiness` before any terminal-state interpretation.
- `cmd_task_readiness_all()` iterates every `tasks/*.md` and returns non-zero if any task is not `READY_FOR_HANDOFF`.
- `aos/scripts/aos_validate.py` aggregates `task --readiness-all` and upgrades overall status to `UNKNOWN_BLOCKED` when readiness failures remain visible in orchestration output.
- `aos/scripts/aos_lifecycle_state.py` does not include `CLOSED` in `VALID_LIFECYCLE_STATES`, while the task schema and task validator accept `CLOSED`.
- `aos/schemas/task-document-header.schema.json` currently has no exclusion-specific witness fields.
- `aos/templates/task-s.md`, `task-m.md`, and `task-l.md` currently expose no exclusion witness contract.
- `tests/test_aos_task_document_check.py` covers current `READY_FOR_HANDOFF` / blocked semantics and would require explicit extension for any new exclusion states.
- `tests/test_aos_validate.py` currently protects orchestration boundaries only and does not cover exclusion aggregation semantics.

## Implementation risks

- validator semantics are safety-critical and can accidentally convert exclusion into implicit success;
- schema changes are lifecycle-adjacent because they redefine acceptable task header semantics;
- a registry or quarantine manifest becomes canonical or lifecycle-adjacent Source of Truth;
- malformed legacy ids can be accidentally normalized or hidden if contract order is wrong;
- mixing semantic introduction with blocker remediation would make regression attribution and rollback unsafe;
- `CLOSED` and `REJECTED` can become false success escape hatches if reused without explicit exclusion witness;
- global `aos_validate.py` status can become misleading if exclusions are counted as `PASS`.

## Risk Profile recommendation

- recommended Risk Profile for downstream implementation sequence: `HIGH_RISK_PROTECTED`
- Risk Profile assignment in project state: `HUMAN_REQUIRED_NOT_ASSIGNED_BY_AGENT`

## Implementation split options

### Option 1. Single-stage implementation

Schema + validator + tests + registry handling + blocker remediation in one stage.

Decision: rejected.

Reasons:

- too many safety-critical surfaces change at once;
- impossible to prove `EXCLUDED_*` stays separate from `PASS` while also remediating blockers in the same stage;
- registry and remediation would be introduced before witness governance is settled;
- rollback and blame assignment become ambiguous.

### Option 2. Two-stage split

Contract first, then implementation + remediation.

Decision: safer than single-stage, but still too compressed because registry/quarantine remains unresolved.

### Option 3. Three-stage split

Contract, then validator/registry, then remediation.

Decision: plausible but still couples registry checkpoint and validator implementation too tightly.

### Option 4. Four-stage split

Contract/test matrix, then registry checkpoint, then schema/validator implementation, then blocker remediation.

Decision: selected.

Reasons:

- isolates witness contract from runtime behavior;
- keeps registry creation behind a separate human gate;
- forces validator semantics to stabilize before any blocker is touched;
- preserves fail-closed rollback boundaries between semantic introduction and blocker application.

## Selected downstream sequence

Recommended downstream sequence:

1. `AOS-FARM.642 — Terminal/Legacy Exclusion Contract and Test Matrix`
2. `AOS-FARM.643 — Legacy Quarantine Registry Contract and Human Checkpoint`
3. `AOS-FARM.644 — Task Readiness Exclusion Schema and Validator Implementation`
4. `AOS-FARM.645 — Existing Blocker Remediation Using Approved Exclusion Semantics`

## Conservative vs implementation-adjacent mode for AOS-FARM.642

Conservative mode:

- `AOS-FARM.642` creates contract and test-matrix reports only;
- no schema edits;
- no test edits;
- no validator edits;
- no task edits.

Implementation-adjacent mode:

- `AOS-FARM.642` may edit schema/tests only if separately authorized by explicit human checkpoint and Risk Profile decision.

Recommendation:

- default `AOS-FARM.642` to conservative contract/test-matrix planning only.
- do not infer schema or test edit permission from AOS-FARM.641.

## Future file scope by stage

### AOS-FARM.642

Default scope:

- reports only

Potential future surfaces only if separately authorized:

- `tests/`
- `tests/fixtures/`
- `aos/schemas/task-document-header.schema.json`

### AOS-FARM.643

Potential future surfaces only if separately authorized:

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

### AOS-FARM.645

Potential future surfaces:

- `tasks/`
- `aos/registry/task-readiness-exclusions.md`
- `aos/reports/readiness/`

## Minimum viable implementation contract

Minimum future classifications:

- `EXCLUDED_TERMINAL`
- `EXCLUDED_LEGACY`
- `MALFORMED_EXCLUSION`

Minimum future rules:

- `EXCLUDED_TERMINAL` is not `PASS`.
- `EXCLUDED_LEGACY` is not `PASS`.
- `MALFORMED_EXCLUSION` is blocker state.
- `task --validate-all` must discover every `tasks/*.md`.
- `task --readiness-all` must not silently skip any `tasks/*.md`.
- invalid `task_id` must not be silently normalized.
- no wildcard, mass, or blanket exclusion.
- every exclusion requires per-task witness.
- human witness must be explicit.
- dependency and supersession integrity must be checked.
- `CLOSED` alone must not become an escape hatch.
- `REJECTED` must not become a false success state.

## Implementation dependency graph

Required dependency order:

`terminal/legacy classification contract`
→ `required witness fields`
→ `registry/manifest contract for legacy quarantine`
→ `schema impact decision`
→ `validator classification order`
→ `JSON and audit output contract`
→ `aos_validate.py aggregation behavior`
→ `test matrix`
→ `current blocker remediation`

Required dependency rules:

- blocker remediation depends on completed validator behavior;
- blocker remediation depends on approved witness model;
- `AOS-FARM.463` treatment depends on registry/quarantine decision;
- schema changes depend on human checkpoint;
- registry creation depends on human checkpoint;
- global readiness behavior depends on explicit `EXCLUDED_* != PASS` tests.

## Test matrix outline

Minimum future test groups:

- terminal exclusion accepted but reported as `EXCLUDED_TERMINAL`, not `PASS`;
- legacy exclusion accepted but reported as `EXCLUDED_LEGACY`, not `PASS`;
- malformed exclusion reported as blocker and remains visible in output;
- invalid legacy `task_id` remains invalid and visible;
- `task --validate-all` still enumerates every `tasks/*.md`;
- `task --readiness-all` still prints every discovered task;
- `aos_validate.py --json` does not report global `PASS` when malformed exclusions exist;
- `CLOSED` without witness remains non-success;
- `REJECTED` without witness remains non-success;
- wildcard or blanket exclusion input is rejected;
- supersession/dependency witness errors fail closed.

## Registry/quarantine boundary

Recommendation:

- registry/quarantine must be a separate future stage before validator implementation.

Reason:

- validator behavior for `EXCLUDED_LEGACY` depends on the registry witness contract, especially for malformed legacy ids such as `AOS-FARM.463`.

Boundary:

- registry/manifest is canonical or lifecycle-adjacent;
- creating or modifying it requires separate human checkpoint, explicit scope, Risk Profile decision, tests, Evidence, and separate commit/push authorization;
- AOS-FARM.641 must not create registry.

## Future failure modes and rollback boundaries

Future failure modes to guard against:

- `EXCLUDED_TERMINAL` counted as `PASS`;
- `EXCLUDED_LEGACY` counted as `PASS`;
- invalid `task_id` silently accepted;
- wildcard exclusion introduced;
- registry suppresses blocker without human witness;
- `task --validate-all` skips `tasks/*.md`;
- `task --readiness-all` hides exclusions;
- `aos_validate.py --json` reports global `PASS` with malformed exclusions;
- `CLOSED` becomes escape hatch;
- `REJECTED` becomes false success state;
- `NOT_RUN` treated as `PASS`;
- Evidence treated as approval;
- CI PASS treated as approval;
- current blockers remediated before semantics exist.

Rollback boundary:

- any unsafe implementation must fail closed;
- audit output must remain preserved;
- reversal must be by normal revert commit;
- no destructive cleanup or history rewrite.

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

## No mass exclusion rule

Future exclusion semantics must remain per-task only.

Forbidden future shortcuts:

- wildcard exclusion;
- directory-level exclusion;
- status-only blanket exclusion;
- registry-only bulk suppression;
- silent quarantine without explicit witness.

## Approval and lifecycle boundary

AOS-FARM.641 may recommend future implementation sequence.

AOS-FARM.641 does not:

- authorize implementation;
- authorize schema edits;
- authorize validator edits;
- authorize registry creation;
- authorize task mutation;
- close blockers;
- mutate lifecycle;
- create release readiness.

## Non-goals

- no validator implementation;
- no schema edits;
- no template edits;
- no tests or fixture edits;
- no task edits;
- no registry creation;
- no blocker remediation;
- no blocker suppression;
- no Risk Profile assignment by agent.

## Future implementation task recommendation

Recommended likely next stage:

`AOS-FARM.642 — Terminal/Legacy Exclusion Contract and Test Matrix`

Recommended downstream sequence after that:

- `AOS-FARM.643 — Legacy Quarantine Registry Contract and Human Checkpoint`
- `AOS-FARM.644 — Task Readiness Exclusion Schema and Validator Implementation`
- `AOS-FARM.645 — Existing Blocker Remediation Using Approved Exclusion Semantics`

This recommendation is planning output only, not approval.
