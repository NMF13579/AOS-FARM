# AOS-FARM.642 — Terminal/Legacy Exclusion Implementation Report

This report is Evidence, not approval.
PASS is validation only, not approval.
Evidence is not approval.
CI PASS is not approval.
UNKNOWN is not OK.
NOT_RUN is not PASS.
EXCLUDED_TERMINAL is not PASS.
EXCLUDED_LEGACY is not PASS.
MALFORMED_EXCLUSION is blocker state.
No release is authorized.
No merge to main is authorized.

## Stage title

AOS-FARM.642 — Terminal/Legacy Exclusion Implementation and Blocker Remediation

## Source review

Reviewed before implementation in required order:

1. `00_AOS_Core_Control.md`
2. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
3. `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

Reviewed design basis:

- `aos/reports/readiness/aos-farm-640-terminal-state-semantics-design.md`
- `aos/reports/readiness/aos-farm-640-legacy-blocker-exclusion-decision-record.md`
- `aos/reports/readiness/aos-farm-641-terminal-legacy-exclusion-implementation-plan.md`
- `aos/reports/readiness/aos-farm-641-scope-split-decision-record.md`

Applied invariants:

- fail closed on unknown or ambiguous exclusion witness;
- keep approval, readiness, validation, and Evidence separate;
- preserve full `tasks/*.md` discovery for both `task --validate-all` and `task --readiness-all`;
- do not let `REJECTED`, `CLOSED`, or invalid legacy ids become implicit success states.

## Baseline validation

Baseline branch state:

- branch: `build/aos-farm-642-terminal-legacy-exclusion-implementation`
- `HEAD`: `316aa578d582fbceb49254572ba42c0548b4d2af`
- `origin/dev`: `316aa578d582fbceb49254572ba42c0548b4d2af`
- `origin/main`: `e77d8011b84946340e428db2c7547f0285be0713`
- `origin/dev...HEAD`: `0 0`

Baseline command summary:

| Command | Result | Exit | Interpretation |
|---|---:|---:|---|
| `python3 aos/scripts/aos_validate.py --json` | `UNKNOWN_BLOCKED` | `0` | Expected fail-closed aggregate because readiness blockers remain. |
| `python3 aos/scripts/aos_task_document_check.py task --readiness-all` | `FAILED` | `1` | Expected; same four blockers remained visible. |
| `python3 aos/scripts/aos_task_document_check.py task --validate-all` | `PASS` | `0` | Expected structural validity. |
| `python3 aos/scripts/aos_architecture_document_check.py validate-all --json` | `PASS` | `0` | Expected. |
| `python3 -m unittest discover -s tests` | `PASS` | `0` | Expected. |
| `git diff --check` | `PASS` | `0` | Expected. |

Observed baseline blockers:

- `AOS-FARM-TASK-0001`
- `AOS-FARM-TASK-060101`
- `AOS-FARM-TASK-060102`
- `AOS-FARM.463`

## AOS-FARM.640 / AOS-FARM.641 design basis

Design and planning reports established:

- `EXCLUDED_TERMINAL`, `EXCLUDED_LEGACY`, and `MALFORMED_EXCLUSION` must be separate from `PASS`;
- malformed witness must stay blocker-visible;
- `REJECTED` and `CLOSED` cannot become escape hatches;
- invalid legacy ids must remain visible and must not be silently normalized;
- wildcard, pattern, mass, and blanket exclusion are forbidden;
- exclusion requires explicit per-task witness with explicit human checkpoint reference;
- `AOS-FARM.463` needs explicit handling but does not require a generalized registry if inline handling can remain fail-closed.

## Final contract

Frozen implementation contract:

- `EXCLUDED_TERMINAL`
  - allowed only for a single task with explicit per-task witness;
  - requires exact `readiness_exclusion_task_id == task_id`;
  - requires explicit human checkpoint reference, source evidence, readiness applicability, and `approval_granted: false`;
  - allowed only when the task is `REJECTED` or `CLOSED` with a valid terminal subtype;
  - remains visible in audit output and is not counted as `READY_FOR_HANDOFF`.
- `EXCLUDED_LEGACY`
  - allowed only for a single invalid legacy task id with explicit per-task witness;
  - does not normalize the invalid id;
  - remains visible in audit output and is not counted as `READY_FOR_HANDOFF`.
- `MALFORMED_EXCLUSION`
  - any incomplete, wildcard, mass, blanket, ambiguous, review-pending, or witness-missing exclusion request;
  - blocks readiness and prevents truthful aggregate `PASS`.

Witness model:

- human witness cannot be created, inferred, fabricated, or backfilled;
- sentinel values such as `REQUIRED_NOT_AVAILABLE` and `HUMAN_REVIEW_REQUIRED` remain fail-closed and do not activate exclusion;
- agent-authored exclusion fields without explicit existing witness do not activate exclusion.

No-false-PASS rules preserved:

- `EXCLUDED_TERMINAL != PASS`
- `EXCLUDED_LEGACY != PASS`
- `MALFORMED_EXCLUSION = blocker`
- `NOT_RUN != PASS`
- Evidence is not approval
- CI PASS is not approval

## Registry/quarantine decision

Decision: no registry created.

Reason:

- inline per-task witness is sufficient to express and validate terminal/legacy exclusion semantics;
- `AOS-FARM.463` can be handled explicitly without silent normalization by evaluating exclusion request fields before treating the invalid id as a readiness blocker;
- current live blockers do not have explicit human checkpoint witness, so no active exclusion needed a registry entry;
- creating `aos/registry/task-readiness-exclusions.md` would add another control surface without improving safety for this stage.

Boundary confirmation:

- no generalized exclusion mechanism created;
- no wildcard, mass, blanket, or future-facing registry semantics introduced;
- `AOS-FARM.463` remains explicitly supported as an invalid legacy id candidate while still failing closed when witness is absent.

## Implementation summary

Changed implementation surfaces:

- `aos/scripts/aos_task_document_check.py`
  - added explicit exclusion witness validation;
  - added `EXCLUDED_TERMINAL`, `EXCLUDED_LEGACY`, and `MALFORMED_EXCLUSION` readiness outputs;
  - kept full discovery of every `tasks/*.md`;
  - added readiness category counts and explicit not-pass statements to audit output;
  - blocked `REJECTED` and `CLOSED` from acting as implicit readiness success without explicit witness.
- `aos/scripts/aos_validate.py`
  - added `readiness_audit` JSON output with per-category counts and per-task audit lists;
  - kept fail-closed aggregate behavior by forcing malformed/blocked readiness audit states out of global `PASS`.
- `aos/scripts/aos_lifecycle_state.py`
  - reconciled helper semantics so `CLOSED` is a recognized lifecycle state.
- `aos/schemas/task-document-header.schema.json`
  - documented optional exclusion witness fields and terminal subtype fields.

Template changes:

- none

Lifecycle mutation:

- none

Registry creation:

- none

## Schema changes

Added optional schema properties for:

- `readiness_exclusion_task_id`
- `readiness_exclusion_type`
- `readiness_exclusion_reason`
- `readiness_exclusion_source_evidence`
- `readiness_exclusion_human_checkpoint`
- `readiness_exclusion_applies_to_readiness`
- `readiness_exclusion_approval_granted`
- `readiness_exclusion_created_in_stage`
- `readiness_exclusion_review_required`
- `closure_type`
- `superseded_by`

These fields document witness expectations only. They do not grant approval.

## Validator changes

Implemented validator/runtime behavior:

- exact-match per-task witness enforcement;
- explicit rejection of wildcard, mass, and blanket exclusion targets;
- explicit rejection of missing or review-pending human witness;
- explicit rejection of `REJECTED` and `CLOSED` without witness;
- explicit rejection of invalid supersession targets;
- full `tasks/*.md` enumeration preserved in both validation and readiness paths.

## Aggregation changes

`aos_validate.py --json` now includes:

- `readiness_audit.status`
- `readiness_audit.counts`
- `active_blockers`
- `excluded_terminal_tasks`
- `excluded_legacy_tasks`
- `malformed_exclusions`
- explicit `EXCLUDED_* is not PASS` statements

Aggregate behavior remains fail-closed:

- malformed exclusion -> `UNKNOWN_BLOCKED`
- active blockers -> `BLOCKED` or `UNKNOWN_BLOCKED`
- no exclusion is counted as active ready

## Audit / JSON behavior

Human-readable `task --readiness-all` now reports:

- each task row;
- active ready/blocker/human-review counts;
- excluded terminal count;
- excluded legacy count;
- malformed exclusion count;
- explicit statements that `EXCLUDED_*` are not `PASS`.

JSON `aos_validate.py --json` now reports:

- category counts;
- excluded/malformed task lists;
- active blocker list;
- aggregate status that remains non-pass when exclusions are malformed or blockers remain.

## Tests added or updated

Added:

- `tests/test_aos_task_readiness_exclusions.py`
  - proves `EXCLUDED_TERMINAL` is not `PASS`;
  - proves `EXCLUDED_LEGACY` is not `PASS`;
  - proves malformed exclusion blocks readiness;
  - rejects wildcard, mass, and blanket exclusions;
  - proves invalid legacy id is not silently accepted;
  - proves `CLOSED` and `REJECTED` alone are not escape hatches;
  - proves `NOT_RUN` and Evidence-only states remain fail-closed.

Updated:

- `tests/test_aos_validate.py`
  - asserts `readiness_audit` is present in JSON output;
  - proves malformed exclusions force non-pass aggregate status.

Mid-stage broad test coverage executed:

- `python3 -m unittest tests.test_aos_task_document_check tests.test_aos_task_readiness_exclusions tests.test_aos_validate tests.test_aos_lifecycle_state`
- result: `PASS`

## PRE_REMEDIATION_GATE

Result: PASS

Evidence:

- `python3 aos/scripts/aos_task_document_check.py task --validate-all` -> `PASS`
- `python3 aos/scripts/aos_task_document_check.py task --readiness-all` -> blocker set preserved, exclusion counters present, no malformed exclusion
- `python3 aos/scripts/aos_validate.py --json` -> aggregate remains `UNKNOWN_BLOCKED`, `readiness_audit` present
- `python3 -m unittest discover -s tests` -> `PASS`
- `git diff --check` -> `PASS`

Gate conclusions:

- `EXCLUDED_TERMINAL != PASS` proven
- `EXCLUDED_LEGACY != PASS` proven
- `MALFORMED_EXCLUSION` blocks readiness proven
- wildcard/mass/blanket exclusion rejection proven
- invalid legacy id not silently accepted proven
- explicit human witness is required
- excluded tasks remain in audit output
- no false aggregate `PASS` for malformed exclusion

## Failure modes covered

- wildcard exclusion
- mass exclusion
- blanket exclusion
- review-pending witness presented as active exclusion
- invalid legacy id silently normalized
- `REJECTED` treated as readiness success
- `CLOSED` treated as readiness success
- `NOT_RUN` treated as `PASS`
- Evidence treated as approval
- malformed supersession target

## Fail-closed behavior

If exclusion witness is incomplete, ambiguous, or review-pending:

- readiness returns `MALFORMED_EXCLUSION`;
- aggregate status cannot truthfully become `PASS`;
- the task remains visible in audit output.

If no explicit human witness exists:

- the task stays blocked or human-review-required;
- no agent-authored field activates exclusion.

## Human witness handling

- no human witness was created in this stage;
- no human checkpoint was inferred;
- no Risk Profile was assigned by agent;
- no existing task file was mutated before the gate;
- sentinel values remain explicit fail-closed markers, not approval substitutes.

## Approval / lifecycle boundary

- implementation of semantics does not approve any task;
- implementation of semantics does not authorize execution, commit, push, merge, release, or deployment;
- no lifecycle mutation was performed by this report;
- root canonical sources `00/01/02` were not changed;
- templates were not changed.

## Final validation summary

Final command summary:

| Command | Result | Exit | Interpretation |
|---|---:|---:|---|
| `python3 aos/scripts/aos_validate.py --json` | `UNKNOWN_BLOCKED` | `0` | Aggregate remains fail-closed because active blockers remain. |
| `python3 aos/scripts/aos_task_document_check.py task --readiness-all` | `FAILED` | `1` | Same four blockers remain visible; no exclusions were activated. |
| `python3 aos/scripts/aos_task_document_check.py task --validate-all` | `PASS` | `0` | All task documents still validate structurally. |
| `python3 aos/scripts/aos_architecture_document_check.py validate-all --json` | `PASS` | `0` | Architecture checks unaffected. |
| `python3 -m unittest discover -s tests` | `PASS` | `0` | Full unit test suite passed after implementation. |
| `git diff --check` | `PASS` | `0` | No whitespace or patch-format errors. |

Final readiness counts:

- active ready: `9`
- active blocked: `3`
- active human review required: `1`
- excluded terminal: `0`
- excluded legacy: `0`
- malformed exclusion: `0`

This is truthful fail-closed output, not approval.
