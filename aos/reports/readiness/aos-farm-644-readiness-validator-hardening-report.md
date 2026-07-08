# AOS-FARM.644 — Readiness Validator Hardening Report

This report is Evidence, not approval.
PASS is validation only, not approval.
Evidence is not approval.
CI PASS is not approval.
EXCLUDED_TERMINAL is not PASS.
EXCLUDED_LEGACY is not PASS.
No commit is authorized.
No push is authorized.
No merge to main is authorized.
No release is authorized.

## Stage purpose

AOS-FARM.644 is a controlled tests/report-first hardening stage that locks the readiness validator behavior already proven by AOS-FARM.642 and AOS-FARM.643 Evidence.

This stage preserves the current fail-closed validator contract and adds focused regression coverage for:

- terminal exclusion acceptance boundaries;
- legacy exclusion acceptance boundaries;
- malformed exclusion fail-closed behavior;
- fail-closed Risk Profile and human-assignment enforcement where exposed by the current contract;
- aggregate readiness and `aos_validate.py --json` PASS boundaries;
- explicit confirmation that PASS output does not create approval semantics.

## Required source review

Reviewed before execution in required order:

1. `00_AOS_Core_Control.md`
2. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
3. `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

Reviewed Evidence basis:

- `aos/reports/readiness/aos-farm-642-terminal-legacy-exclusion-implementation-report.md`
- `aos/reports/readiness/aos-farm-642-blocker-remediation-report.md`
- `aos/reports/readiness/aos-farm-643-human-review-blocker-resolution-decision-record.md`
- `aos/reports/readiness/aos-farm-643-blocker-resolution-application-report.md`

Inspected current validator/test surfaces:

- `aos/scripts/aos_task_document_check.py`
- `aos/scripts/aos_validate.py`
- `aos/scripts/aos_lifecycle_state.py`
- `aos/schemas/task-document-header.schema.json`
- `tests/test_aos_task_readiness_exclusions.py`
- `tests/test_aos_validate.py`

## Baseline commit

- branch created: `build/aos-farm-644-readiness-validator-hardening-from-evidence`
- baseline `HEAD`: `063334d449ae45fb6b0f9da51e82f9862973d386`
- baseline `origin/dev`: `063334d449ae45fb6b0f9da51e82f9862973d386`
- baseline `origin/main`: `e77d8011b84946340e428db2c7547f0285be0713`
- baseline `origin/dev...HEAD`: `0 0`

## Baseline validation

Observed baseline behavior on this exact branch baseline:

| Command | Result | Exit | Interpretation |
|---|---:|---:|---|
| `python3 aos/scripts/aos_validate.py --json` | `PASS` | `0` | Aggregate validator output already reflects AOS-FARM.643-applied exclusions with no active readiness blockers. |
| `python3 aos/scripts/aos_task_document_check.py task --readiness-all` | `PASS` | `0` | Current readiness contract reports three `EXCLUDED_TERMINAL`, one `EXCLUDED_LEGACY`, and zero active blockers. |
| `python3 aos/scripts/aos_task_document_check.py task --validate-all` | `PASS` | `0` | Structural task validation remains clean. |
| `python3 aos/scripts/aos_architecture_document_check.py validate-all --json` | `PASS` | `0` | Architecture validator remains clean. |
| `python3 -m unittest discover -s tests` | `PASS` | `0` | Full baseline test suite passes before hardening edits. |
| `git diff --check` | `PASS` | `0` | No whitespace or patch-format defects at baseline. |

Baseline readiness audit counts:

- `active_ready_count: 9`
- `active_blocked_count: 0`
- `active_human_review_required_count: 0`
- `excluded_terminal_count: 3`
- `excluded_legacy_count: 1`
- `malformed_exclusion_count: 0`

## Evidence reviewed from AOS-FARM.642–643

AOS-FARM.642 established the validator/report contract for:

- `EXCLUDED_TERMINAL`
- `EXCLUDED_LEGACY`
- `MALFORMED_EXCLUSION`
- explicit non-approval statements in readiness and aggregate output
- fail-closed handling for missing or ambiguous witness

AOS-FARM.643 then applied human-scoped witness to live blocker tasks so that the current baseline now truthfully reports:

- `AOS-FARM-TASK-0001` as `EXCLUDED_TERMINAL`
- `AOS-FARM-TASK-060101` as `EXCLUDED_TERMINAL`
- `AOS-FARM-TASK-060102` as `EXCLUDED_TERMINAL`
- `AOS-FARM.463` as `EXCLUDED_LEGACY`

The hardening target for AOS-FARM.644 is therefore the current post-643 contract, not the earlier pre-resolution blocker state.

## Evidence-derived behavior matrix

| Scenario | Expected behavior | Covered by test | Notes |
|---|---|---:|---|
| valid terminal exclusion | `EXCLUDED_TERMINAL`, visible in audit, not `PASS` | yes | `test_rejected_task_with_explicit_witness_is_excluded_terminal_not_pass` |
| valid legacy exclusion | `EXCLUDED_LEGACY`, visible in audit, not `PASS` | yes | `test_invalid_legacy_task_with_explicit_witness_is_excluded_legacy` |
| malformed exclusion | fail closed as `MALFORMED_EXCLUSION` | yes | covered by existing malformed witness test plus missing/invalid type and invalid closure subtype tests |
| missing Risk Profile | fail closed | yes | current contract reports `BLOCKED` with `risk_profile is missing` |
| agent-assigned Risk Profile | fail closed; agent assignment does not satisfy human assignment requirement | yes | current contract exposes this through `risk_assigned_by` |
| missing human witness | fail closed as `MALFORMED_EXCLUSION` | yes | covered for missing field and sentinel unavailable witness |
| `UNKNOWN_BLOCKED` | does not pass aggregate readiness | yes | aggregate readiness stays non-pass with active blocker count |
| `NOT_RUN` | does not pass aggregate readiness | yes | aggregate readiness stays non-pass with `HUMAN_REVIEW_REQUIRED` count |
| aggregate readiness PASS boundary | `aos_validate.py --json` PASS requires no active blockers and no malformed exclusions in structured readiness output | yes | mocked `aos_validate.py` tests assert `BLOCKED` and `UNKNOWN_BLOCKED` boundaries |
| approval boundary | PASS output does not create approval semantics | yes | existing plus new `aos_validate.py` JSON assertions keep approval/commit/push/release flags false |

## Fixture strategy

- inline temporary fixtures used: yes, via test-local temporary `tasks/` directories
- persistent fixtures added: none
- live task files modified: no
- fixture scope issues: none

No new fixture files were needed because the existing tests already use isolated generated task documents that can express the evidence-derived contract precisely without touching live tasks.

## Tests added / modified

Modified `tests/test_aos_task_readiness_exclusions.py` to add focused regression coverage for:

- terminal exclusion with `closure_type: COMPLETED` failing closed under the current contract;
- missing `readiness_exclusion_type` failing closed;
- invalid `readiness_exclusion_type` failing closed;
- missing `risk_profile` failing closed;
- agent-assigned Risk Profile failing closed;
- missing human witness field failing closed;
- aggregate readiness non-pass behavior for `UNKNOWN_BLOCKED`;
- aggregate readiness non-pass behavior for `NOT_RUN`.

Modified `tests/test_aos_validate.py` to add focused regression coverage for:

- `aos_validate.py --json` refusing `PASS` when structured readiness output still contains active blockers;
- `aos_validate.py --json` preserving explicit non-approval booleans and not-pass statements even when aggregate status is `PASS`.

## Approval boundary statement

This stage does not:

- claim approval;
- claim `READY_FOR_EXECUTION`;
- claim `READY_FOR_RELEASE`;
- authorize commit;
- authorize push;
- authorize merge to main;
- authorize release.

The hardening output is limited to regression tests plus this report artifact. Any later commit or push requires a separate human authorization phrase.

## Whether validator code changed

Validator code changed: no.

This stage is tests/report only. The current validator contract already matched the AOS-FARM.642–643 Evidence and the AOS-FARM.644 hardening expectations that are expressible without schema or lifecycle expansion.

## Implementation summary

- tests added: focused regression cases inside existing readiness and aggregate validator suites
- tests modified:
  - `tests/test_aos_task_readiness_exclusions.py`
  - `tests/test_aos_validate.py`
- fixtures added: none
- validator files changed: none
- schema changed: no
- live task files changed: no
- reports created:
  - `aos/reports/readiness/aos-farm-644-readiness-validator-hardening-report.md`

## Final validation

| Command | Result | Exit | Interpretation |
|---|---:|---:|---|
| `python3 aos/scripts/aos_validate.py --json` | `PASS` | `0` | Aggregate output remains clean with no active blockers or malformed exclusions. |
| `python3 aos/scripts/aos_task_document_check.py task --readiness-all` | `PASS` | `0` | Readiness audit remains truthful: three `EXCLUDED_TERMINAL`, one `EXCLUDED_LEGACY`, zero active blockers. |
| `python3 aos/scripts/aos_task_document_check.py task --validate-all` | `PASS` | `0` | Structural task validation remains clean after hardening edits. |
| `python3 aos/scripts/aos_architecture_document_check.py validate-all --json` | `PASS` | `0` | Architecture validator remains clean. |
| `python3 -m unittest discover -s tests` | `PASS` | `0` | Full suite passes with `268` tests. |
| `python3 -m unittest tests.test_aos_task_readiness_exclusions tests.test_aos_validate` | `PASS` | `0` | Focused hardening suites pass with `21` tests. |
| `git diff --check` | `PASS` | `0` | No whitespace or patch-format defects after edits. |

## Changed file classification

| File | Category | Why allowed | Risk |
|---|---|---|---|
| `tests/test_aos_task_readiness_exclusions.py` | test hardening | allowed focused readiness regression coverage | low |
| `tests/test_aos_validate.py` | test hardening | allowed aggregate validator regression coverage | low |
| `aos/reports/readiness/aos-farm-644-readiness-validator-hardening-report.md` | stage report | explicitly required artifact for this stage | low |

## Current validator contract limitations

- `MALFORMED_EXCLUSION` current contract state is available directly.
- Risk Profile assignment source is exposed through `risk_assigned_by`.
- Exclusion human witness presence is exposed through `readiness_exclusion_human_checkpoint`, but witness provenance is presence-based rather than a richer structured actor record.
- Aggregate readiness structured fields used by `aos_validate.py --json` are:
  - `status`
  - `counts`
  - `active_blockers`
  - `excluded_terminal_tasks`
  - `excluded_legacy_tasks`
  - `malformed_exclusions`
  - `explicit_not_pass_statement`

Contract gaps intentionally left unchanged in this stage:

- no separate structured field for “who authored the exclusion witness record” beyond the witness checkpoint text itself;
- no richer structured approval-boundary field beyond the existing top-level booleans and explicit not-pass statements;
- no finer subtype field for malformed exclusions beyond current reason strings.

These are future hardening candidates only. They do not justify schema or lifecycle change in AOS-FARM.644.

## Residual risks

- The current contract treats `closure_type: COMPLETED` as non-terminal for exclusion purposes. That behavior is now locked by tests, but any future desire to broaden terminal semantics would require separate human-authorized design work.
- Some approval-boundary semantics are asserted through existing booleans and messages rather than a richer typed contract.
- Human witness provenance is still text/witness-field based rather than a more structured checkpoint object. That is outside the authorized scope for this stage.

## Future hardening candidates

- Add a separate, explicitly human-authorized design stage if richer structured witness provenance becomes necessary.
- Add more direct unit coverage around `build_readiness_report()` JSON shape if future changes expand aggregate reporting fields.
- If future work wants to distinguish more malformed-exclusion subtypes structurally, do that only in a separately authorized schema/contract stage.
