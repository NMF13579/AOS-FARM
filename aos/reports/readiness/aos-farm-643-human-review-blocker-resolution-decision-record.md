# AOS-FARM.643 — Human Review Blocker Resolution Decision Record

This Decision Record is Evidence, not approval.
PASS is validation only, not approval.
Evidence is not approval.
CI PASS is not approval.
Human witness is scoped to listed blocker ids only.
No release is authorized.
No merge to main is authorized.
No READY_FOR_EXECUTION is claimed.
No READY_FOR_RELEASE is claimed.

## Stage title

AOS-FARM.643 — Human Review Blocker Resolution Decision

## Source review

Reviewed in required order:

1. `00_AOS_Core_Control.md`
2. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
3. `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

Reviewed design/evidence basis:

- `aos/reports/readiness/aos-farm-642-terminal-legacy-exclusion-implementation-report.md`
- `aos/reports/readiness/aos-farm-642-blocker-remediation-report.md`

Reviewed blocker files:

- `tasks/AOS-FARM-TASK-0001.md`
- `tasks/AOS-FARM-TASK-060101.md`
- `tasks/AOS-FARM-TASK-060102.md`
- `tasks/AOS-FARM.463.md`

## Baseline state

- branch: `build/aos-farm-643-human-review-blocker-resolution-decision`
- baseline `HEAD`: `aa8de0f7310eb4c3d6c4c16e2fecf3adbacf7eed`
- baseline `origin/dev`: `aa8de0f7310eb4c3d6c4c16e2fecf3adbacf7eed`
- baseline `origin/main`: `e77d8011b84946340e428db2c7547f0285be0713`
- baseline `origin/dev...HEAD`: `0 0`
- baseline `aos_validate.py --json`: `UNKNOWN_BLOCKED`
- baseline `task --readiness-all`: `FAILED`
- baseline blocker set:
  - `AOS-FARM-TASK-0001`
  - `AOS-FARM-TASK-060101`
  - `AOS-FARM-TASK-060102`
  - `AOS-FARM.463`

## AOS-FARM.642 context

AOS-FARM.642 added fail-closed support for:

- `EXCLUDED_TERMINAL`
- `EXCLUDED_LEGACY`
- `MALFORMED_EXCLUSION`
- readiness audit visibility in `aos_validate.py --json`

AOS-FARM.642 also fixed the schema/validator contract so that exclusion witness can be applied only when all required fields exist and no forbidden inference is made.

## Per-blocker decision analysis

| Blocker id | Pre-state | Exact human decision | Exact allowed action | Witness exists in this prompt | Task-file change allowed | Application blocked | Why |
|---|---|---|---|---|---|---|---|
| `AOS-FARM-TASK-0001` | `BLOCKED` | `APPLY_TERMINAL_WITNESS` | Apply only AOS-FARM.642 schema-supported terminal witness fields | yes | no | yes | Current validator allows terminal exclusion only when `status` is `REJECTED` or `CLOSED`, but this prompt does not explicitly authorize a matching lifecycle status/terminal subtype mutation. Inferring rejection/closure would simulate a human decision. |
| `AOS-FARM-TASK-060101` | `HUMAN_REVIEW_REQUIRED` | `APPLY_TERMINAL_WITNESS` | Apply only AOS-FARM.642 schema-supported terminal witness fields | yes | no | yes | Same fail-closed boundary as `AOS-FARM-TASK-0001`. Existing status is `HUMAN_REVIEW_REQUIRED`, which cannot activate terminal exclusion under AOS-FARM.642 without extra lifecycle semantics not explicitly granted here. |
| `AOS-FARM-TASK-060102` | `BLOCKED` | `APPLY_RISK_PROFILE_ASSIGNMENT` | Apply only AOS-FARM.642 schema-supported human Risk Profile assignment witness | yes | yes | no | `risk_profile` and `risk_assigned_by` are existing schema-supported fields and do not require validator/schema/code changes. |
| `AOS-FARM.463` | `BLOCKED` | `APPLY_LEGACY_WITNESS` | Apply only AOS-FARM.642 schema-supported legacy witness fields | yes | yes | no | Existing validator contract supports explicit inline legacy exclusion for this exact invalid id without renaming, normalization, migration, registry creation, or code changes. |

## Why terminal witness application is blocked

The AOS-FARM.642 validator contract requires:

- `readiness_exclusion_type: TERMINAL`
- `readiness_exclusion_task_id == task_id`
- explicit human witness fields
- `status: REJECTED` or `status: CLOSED`
- if `status: CLOSED`, a valid `closure_type`

This prompt provides a human terminal/readiness decision, but it does not explicitly provide:

- `REJECTED` as a human rejection decision; or
- `CLOSED` plus an explicit terminal subtype such as `RETIRED`, `SUPERSEDED`, or `COMPLETED`

Applying terminal exclusion without those lifecycle semantics would require an inferred human decision. That is forbidden.

## Why these decisions are not approval

- They do not set `approval_status: APPROVED`.
- They do not set `execution_authorized: true`.
- They do not authorize commit, push, merge, release, or deployment.
- `EXCLUDED_TERMINAL` and `EXCLUDED_LEGACY` remain explicitly not `PASS`.

## Why these decisions are not release authorization

- The prompt explicitly says release remains unauthorized.
- No release field is switched to true.
- Validation output, if passing for any command, remains Evidence only.

## Why these decisions are not merge authorization

- The prompt explicitly says merge to main remains unauthorized.
- No merge field is switched to true.
- No branch integration action is requested or performed.

## Residual blockers

Residual active blockers remain after safe application because:

- `AOS-FARM-TASK-0001` still needs an explicit lifecycle-compatible terminal decision or other separately authorized remediation.
- `AOS-FARM-TASK-060101` still needs an explicit lifecycle-compatible terminal decision or other separately authorized remediation.
- `AOS-FARM-TASK-060102` can receive human risk assignment, but approval/evidence/validator blockers remain fail-closed.

## Final expected validation effect

Expected safe effect after applying only authorized witness that fits the AOS-FARM.642 contract:

- `AOS-FARM.463` should move from active blocker to `EXCLUDED_LEGACY`.
- `AOS-FARM-TASK-060102` should no longer fail for `risk_profile: UNKNOWN_BLOCKED`, but it should remain non-ready because approval/validator/evidence conditions are still not satisfied.
- `task --validate-all` should remain `PASS`.
- `architecture validate-all` should remain `PASS`.
- `unittest discover` should remain `PASS`.
- readiness should remain fail-closed because not all blockers are no longer active.

## AOS-FARM.643 Prompt 1b Continuation

Continuation prompt reviewed on the existing branch:

- branch confirmed: `build/aos-farm-643-human-review-blocker-resolution-decision`
- `HEAD`: `aa8de0f7310eb4c3d6c4c16e2fecf3adbacf7eed`
- `origin/dev`: `aa8de0f7310eb4c3d6c4c16e2fecf3adbacf7eed`
- `origin/main`: `e77d8011b84946340e428db2c7547f0285be0713`
- `origin/dev...HEAD`: `0 0`

Current AOS-FARM.643 tracked changes before continuation were still limited to:

- `tasks/AOS-FARM-TASK-060102.md`
- `tasks/AOS-FARM.463.md`
- `aos/reports/readiness/aos-farm-643-human-review-blocker-resolution-decision-record.md`
- `aos/reports/readiness/aos-farm-643-blocker-resolution-application-report.md`

Continuation-specific decision analysis:

- `AOS-FARM-TASK-0001`
  - existing supported lifecycle fields are identifiable: `status`, `closure_type`, optional `superseded_by`, and the existing readiness exclusion witness fields.
  - safe lifecycle value selection still fails closed because the current prompt does not specify one exact validator-compatible terminal meaning among `REJECTED`, `CLOSED+RETIRED`, `CLOSED+SUPERSEDED`, or `CLOSED+COMPLETED`.
  - choosing one would require inferred human intent.
- `AOS-FARM-TASK-060101`
  - same fail-closed boundary as `AOS-FARM-TASK-0001`.
- `AOS-FARM-TASK-060102`
  - repo inspection found no existing schema-supported field whose exact meaning is “human review completed without approval”.
  - approval/execution fields cannot be repurposed to bypass review.
- `AOS-FARM.463`
  - existing `EXCLUDED_LEGACY` witness remains valid and unchanged.

Continuation outcome:

- no additional task-file lifecycle witness was safely applicable without inference;
- `AOS-FARM-TASK-0001` remains `BLOCKED`;
- `AOS-FARM-TASK-060101` remains `HUMAN_REVIEW_REQUIRED`;
- `AOS-FARM-TASK-060102` remains `HUMAN_REVIEW_REQUIRED`;
- `AOS-FARM.463` remains `EXCLUDED_LEGACY`.

## AOS-FARM.643 Prompt 1c Exact Lifecycle Witness Input

Prompt 1c removes lifecycle ambiguity by explicitly providing:

- `AOS-FARM-TASK-0001`: `status: CLOSED`, `closure_type: RETIRED`
- `AOS-FARM-TASK-060101`: `status: CLOSED`, `closure_type: RETIRED`

Exact lifecycle witness application authorized in Prompt 1c:

- existing terminal exclusion witness fields only
- no new fields
- no schema changes
- no validator changes
- no lifecycle code changes

Prompt 1c also explicitly preserves:

- `AOS-FARM-TASK-060102` as `HUMAN_REVIEW_REQUIRED` unless a pre-existing precise non-approval completion field exists
- `AOS-FARM.463` as `EXCLUDED_LEGACY`

Prompt 1c application outcome under validator output:

- `AOS-FARM-TASK-060101` became `EXCLUDED_TERMINAL`
- `AOS-FARM.463` remained `EXCLUDED_LEGACY`
- `AOS-FARM-TASK-060102` remained `HUMAN_REVIEW_REQUIRED`
- `AOS-FARM-TASK-0001` became `MALFORMED_EXCLUSION` because its terminal witness was present while `risk_profile` remained `UNKNOWN_BLOCKED`

## AOS-FARM.643 Prompt 1d Residual Blocker Closure Input

Prompt 1d provides exact residual decisions for the remaining two unresolved blockers without requiring inference:

- `AOS-FARM-TASK-0001`
  - `risk_profile: HIGH_RISK_PROTECTED`
  - `risk_assigned_by: human`
  - preserve `status: CLOSED`
  - preserve `closure_type: RETIRED`
  - preserve existing terminal witness
- `AOS-FARM-TASK-060102`
  - preserve `risk_profile: HIGH_RISK_PROTECTED`
  - preserve `risk_assigned_by: human`
  - apply `status: CLOSED`
  - apply `closure_type: COMPLETED`
  - apply terminal witness only if required by current validators

Residual decision analysis:

| Blocker id | Pre-state before Prompt 1d | Exact human decision | Supported fields identifiable | Safe application allowed | Expected validator boundary |
|---|---|---|---|---|---|
| `AOS-FARM-TASK-0001` | `MALFORMED_EXCLUSION` | assign human Risk Profile and preserve existing `CLOSED`/`RETIRED` terminal witness | yes | yes | should clear `risk_profile is UNKNOWN_BLOCKED` and allow `EXCLUDED_TERMINAL` if no other blocker remains |
| `AOS-FARM-TASK-060101` | `EXCLUDED_TERMINAL` | keep existing state | yes | no task-file change required | should remain `EXCLUDED_TERMINAL` |
| `AOS-FARM-TASK-060102` | `HUMAN_REVIEW_REQUIRED` | preserve human Risk Profile, set `CLOSED` + `COMPLETED`, no invented review-completion field | yes | yes | current validator may still keep it active because `COMPLETED` is not one of the terminal exclusion closure types |
| `AOS-FARM.463` | `EXCLUDED_LEGACY` | keep existing state | yes | no task-file change required | should remain `EXCLUDED_LEGACY` |

Why Prompt 1d is still not approval:

- it does not set `approval_status: APPROVED`
- it does not set any execution, commit, push, merge, or release authorization to true
- `EXCLUDED_TERMINAL` and `EXCLUDED_LEGACY` remain not `PASS`
- `CLOSED` is lifecycle state only, not approval

Prompt 1d validation outcome:

- `AOS-FARM-TASK-0001` became `EXCLUDED_TERMINAL`
- `AOS-FARM-TASK-060101` remained `EXCLUDED_TERMINAL`
- `AOS-FARM.463` remained `EXCLUDED_LEGACY`
- `AOS-FARM-TASK-060102` became `MALFORMED_EXCLUSION`

Exact validator reason for `AOS-FARM-TASK-060102` after Prompt 1d:

- `readiness_exclusion_type must be one of ['LEGACY', 'TERMINAL']`
- `closure_type: COMPLETED` is schema-supported, but under the current validator contract `closure_type` is treated as exclusion-state input and `COMPLETED` is not a valid terminal exclusion closure type

## AOS-FARM.643 Prompt 1e Correct Malformed Exclusion for AOS-FARM-TASK-060102

Prompt 1e provides an exact human correction for the remaining malformed exclusion:

- target blocker: `AOS-FARM-TASK-060102`
- preserve `risk_profile: HIGH_RISK_PROTECTED`
- preserve `risk_assigned_by: human`
- apply `status: CLOSED`
- replace invalid `closure_type: COMPLETED` with `closure_type: RETIRED`
- apply `readiness_exclusion_type: TERMINAL`
- apply the existing schema-supported terminal exclusion witness fields required by the AOS-FARM.642 validator contract

Prompt 1e also explicitly preserves already-valid states:

- `AOS-FARM-TASK-0001`: keep `EXCLUDED_TERMINAL`
- `AOS-FARM-TASK-060101`: keep `EXCLUDED_TERMINAL`
- `AOS-FARM.463`: keep `EXCLUDED_LEGACY`

Prompt 1e is not approval because:

- it does not set `approval_status: APPROVED`
- it does not authorize `READY_FOR_EXECUTION`
- it does not authorize `READY_FOR_RELEASE`
- it does not authorize commit, push, merge, release, or deployment
