# AOS-FARM.645 — Readiness Validator Contract Audit and Next Hardening Decision

This report is Evidence, not approval.
PASS is validation only, not approval.
Evidence is not approval.
CI PASS is not approval.
UNKNOWN is not OK.
NOT_RUN is not PASS.
EXCLUDED_TERMINAL is not PASS.
EXCLUDED_LEGACY is not PASS.
Human approval cannot be simulated.
Human witness cannot be fabricated.
Agent cannot assign Risk Profile.
AOS-FARM.645 does not authorize the next recommended stage.
AOS-FARM.645 does not promote implementation details to canonical contract.
Canonical promotion requires explicit human checkpoint.

## 1. Stage purpose

AOS-FARM.645 is a controlled report/decision-only audit of the current readiness validator contract after AOS-FARM.642, AOS-FARM.643, and AOS-FARM.644.

The goal is to:

- inventory the current observed contract;
- map AOS-FARM.644 coverage to that contract;
- classify remaining gaps by safety impact;
- choose exactly one minimal next hardening direction.

This stage is not implementation, schema evolution, lifecycle redesign, registry creation, approval, release, merge-to-main, or live task remediation.

## 2. Source review

Reviewed in required order:

1. `00_AOS_Core_Control.md`
2. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
3. `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

Reviewed AOS-FARM.642–644 Evidence:

- `aos/reports/readiness/aos-farm-642-terminal-legacy-exclusion-implementation-report.md`
- `aos/reports/readiness/aos-farm-642-blocker-remediation-report.md`
- `aos/reports/readiness/aos-farm-643-human-review-blocker-resolution-decision-record.md`
- `aos/reports/readiness/aos-farm-643-blocker-resolution-application-report.md`
- `aos/reports/readiness/aos-farm-644-readiness-validator-hardening-report.md`

Read-only inspected current validator/test surfaces:

- `aos/scripts/aos_task_document_check.py`
- `aos/scripts/aos_validate.py`
- `aos/scripts/aos_lifecycle_state.py`
- `aos/schemas/task-document-header.schema.json`
- `tests/test_aos_task_readiness_exclusions.py`
- `tests/test_aos_validate.py`

Protected live task files were not inspected in this stage because AOS-FARM.642–644 Evidence plus current validator/test surfaces were sufficient for the contract audit.

## 3. Baseline commit

- branch: `build/aos-farm-645-readiness-validator-contract-audit-decision`
- `HEAD`: `b6e69e64e7c91e1c5b68eee9852963884905e624`
- `origin/dev`: `b6e69e64e7c91e1c5b68eee9852963884905e624`
- `origin/main`: `e77d8011b84946340e428db2c7547f0285be0713`
- `origin/dev...HEAD`: `0 0`
- remote target branch check: absent on origin

## 4. Baseline validation

| Command | Result | Exit | Interpretation |
|---|---:|---:|---|
| `python3 aos/scripts/aos_validate.py --json` | `PASS` | `0` | Aggregate output passes while preserving explicit non-approval booleans and readiness audit visibility. |
| `python3 aos/scripts/aos_task_document_check.py task --readiness-all` | `PASS` | `0` | Current readiness audit reports `9` ready tasks, `3` `EXCLUDED_TERMINAL`, `1` `EXCLUDED_LEGACY`, `0` active blockers, `0` malformed exclusions. |
| `python3 aos/scripts/aos_task_document_check.py task --validate-all` | `PASS` | `0` | Structural task validation remains clean. |
| `python3 aos/scripts/aos_architecture_document_check.py validate-all --json` | `PASS` | `0` | Architecture validation remains clean. |
| `python3 -m unittest discover -s tests` | `PASS` | `0` | Full unit suite passes at baseline. |
| `git diff --check` | `PASS` | `0` | No whitespace or patch-format defects at baseline. |

Observed baseline readiness counts from the structured audit:

- `active_ready_count: 9`
- `active_blocked_count: 0`
- `active_human_review_required_count: 0`
- `excluded_terminal_count: 3`
- `excluded_legacy_count: 1`
- `malformed_exclusion_count: 0`

## 5. Evidence strength order used

1. Canonical root sources `00/01/02` for governance, approval, Risk Profile, and fail-closed semantics.
2. Current structured validator output and current code behavior in `aos_task_document_check.py` and `aos_validate.py`.
3. Committed regression tests in `tests/test_aos_task_readiness_exclusions.py` and `tests/test_aos_validate.py`.
4. AOS-FARM.642–644 reports for historical intent and already-proven boundaries.
5. Human-readable output and report phrases only where they mirror current implementation.
6. Inference only where explicitly labeled as inference.

Inferred behavior was not treated as canonical contract.

## 6. AOS-FARM.642–644 Evidence summary

- AOS-FARM.642 established the current exclusion model: `EXCLUDED_TERMINAL`, `EXCLUDED_LEGACY`, `MALFORMED_EXCLUSION`, exact-match witness scope, malformed fail-closed handling, and aggregate readiness visibility in `aos_validate.py --json`.
- AOS-FARM.642 also added the current schema fields for exclusion witness and terminal subtype support, but did not grant approval or lifecycle authority.
- AOS-FARM.643 applied human-scoped witness to the four known blocker tasks so that the current baseline now truthfully reports three terminal exclusions and one legacy exclusion, all still explicitly not `PASS`.
- AOS-FARM.644 did not change validator logic; it hardened the current observed contract with regression coverage for valid terminal/legacy exclusion, malformed exclusion, `UNKNOWN_BLOCKED`, `NOT_RUN`, aggregate `PASS` boundaries, and top-level non-approval booleans.

## 7. Current readiness validator contract inventory

| Contract item | Current representation | Classification | Notes |
|---|---|---|---|
| readiness status | `READY_FOR_HANDOFF`, `BLOCKED`, `HUMAN_REVIEW_REQUIRED`, `EXCLUDED_TERMINAL`, `EXCLUDED_LEGACY`, `MALFORMED_EXCLUSION` | `OBSERVED_STABLE_CONTRACT_CANDIDATE` | Exposed by `check_task_readiness()` and `build_readiness_report()`. |
| terminal exclusion | Structured readiness state plus exclusion task list in `readiness_audit.excluded_terminal_tasks` | `OBSERVED_STABLE_CONTRACT_CANDIDATE` | Requires explicit witness, exact id match, allowed lifecycle status, and allowed terminal subtype. |
| legacy exclusion | Structured readiness state plus exclusion task list in `readiness_audit.excluded_legacy_tasks` | `OBSERVED_STABLE_CONTRACT_CANDIDATE` | Limited to invalid legacy ids with exact witness. |
| malformed exclusion | Structured readiness state plus `readiness_audit.malformed_exclusions` | `OBSERVED_STABLE_CONTRACT_CANDIDATE` | Fail-closed blocker state. |
| `UNKNOWN_BLOCKED` | Aggregate `overall_status` when readiness audit is `UNKNOWN_BLOCKED` or command output exposes unknown blockers | `OBSERVED_STABLE_CONTRACT_CANDIDATE` | Enforced in `determine_overall_status()` and readiness override logic. |
| `NOT_RUN` | Underlying task-level blocker/human-review reason; never converted to `PASS` | `PARTIAL_CONTRACT` | Strongly enforced at task level and covered by tests, but not surfaced as a dedicated structured aggregate field. |
| aggregate `PASS` boundary | `aos_validate.py --json` top-level `overall_status` plus readiness counts and blocker lists | `OBSERVED_STABLE_CONTRACT_CANDIDATE` | `PASS` allowed only when command set passes and readiness audit is not blocked/unknown. |
| structured JSON fields | top-level `overall_status`, `readiness_audit`, `approval_claimed`, `commit_authorized`, `push_authorized`, `release_authorized`, `results` | `OBSERVED_STABLE_CONTRACT_CANDIDATE` | Shape is currently stable in code and tests. |
| text-only safety statements | `explicit_not_pass_statement` string list and CLI output phrases | `TEXT_ONLY_SAFETY_SIGNAL` | Important but string-based rather than typed. |
| approval-related booleans / absence of approval booleans | top-level booleans are all `false`; no approval-granting readiness field exists | `OBSERVED_STABLE_CONTRACT_CANDIDATE` | Current contract exposes absence of approval authority at aggregate level. |
| human witness fields | Validated from task headers, but not re-exposed in structured readiness audit entries | `PARTIAL_CONTRACT` | Present in schema and validation logic; not present in JSON audit output. |
| Risk Profile fields | `risk_profile` and `risk_assigned_by` are validated at task level; forbidden agent assignment blocks readiness | `PARTIAL_CONTRACT` | Current audit output exposes resulting readiness only, not assignment source per task. |
| terminal / legacy exclusion audit fields | Per-category task lists and counts are present in readiness audit | `OBSERVED_STABLE_CONTRACT_CANDIDATE` | Stable and structured. |
| malformed exclusion audit fields | `malformed_exclusions` list and count are present in readiness audit | `OBSERVED_STABLE_CONTRACT_CANDIDATE` | Stable and structured. |

## 8. Contract item classification

### `OBSERVED_STABLE_CONTRACT_CANDIDATE`

- readiness status set
- exclusion category counts and per-task audit lists
- malformed exclusion as fail-closed blocker
- aggregate `PASS` boundary
- top-level non-approval booleans
- aggregate readiness JSON shape currently asserted by tests

### `CURRENT_IMPLEMENTATION_DETAIL`

- exact wording of some human-readable reason strings
- exact ordering of CLI lines outside the tested contract surface
- exact composition of raw command list inside `VALIDATION_COMMANDS`

### `TEXT_ONLY_SAFETY_SIGNAL`

- `"EXCLUDED_TERMINAL is not PASS"`
- `"EXCLUDED_LEGACY is not PASS"`
- `"MALFORMED_EXCLUSION is blocker state"`
- CLI phrases such as `"PASS is not approval"` and `"Evidence is not approval"`

### `PARTIAL_CONTRACT`

- `NOT_RUN` semantics at aggregate JSON level
- human witness provenance
- Risk Profile assignment source visibility
- approval boundary inside readiness audit itself, beyond top-level booleans

### `MISSING_CONTRACT`

- no typed readiness-audit field that records witness provenance or witness availability outcome per excluded task
- no typed readiness-audit field that records Risk Profile assignment source for audited tasks

### `HUMAN_DECISION_REQUIRED`

- whether any observed stable candidates should be promoted to canonical contract in a later stage

### `NO_ACTION_REQUIRED`

- no schema change, lifecycle change, registry creation, or live-task mutation is required to complete this audit

## 9. Explicit canonical promotion boundary

Observed stable contract candidates in this report are audit findings only.

They are not canonical promotion.

This report does not promote implementation details to canonical contract.

Canonical promotion requires an explicit later human checkpoint.

## 10. AOS-FARM.644 coverage map

| Behavior | Covered | Coverage type | Gap |
|---|---:|---|---|
| terminal exclusion | yes | mixed | Current tests prove acceptance and not-pass boundary, but do not assert typed witness provenance in aggregate JSON because no such field exists. |
| legacy exclusion | yes | mixed | Same gap: no typed witness provenance field in structured aggregate output. |
| malformed exclusion | yes | mixed | Reason strings are covered more than typed malformed subtype fields. |
| `UNKNOWN_BLOCKED` | yes | structured | Covered through aggregate JSON behavior; no additional gap for current stage. |
| `NOT_RUN` | yes | text | Covered through readiness output text and aggregate non-pass behavior; no dedicated typed aggregate field. |
| aggregate `PASS` boundary | yes | structured | Covered in `tests/test_aos_validate.py`. |
| approval boundary | yes | structured + text | Top-level booleans are covered, but readiness-audit-local typed boundary fields are absent. |
| human witness boundary | no | none | Validation logic exists, but AOS-FARM.644 did not add structured contract assertions for witness provenance or witness state in JSON output. |
| Risk Profile assignment source | no | none | Validation logic rejects agent assignment, but structured readiness audit does not expose assignment source. |

## 11. Gap analysis

| Gap | Risk class | Evidence | Recommended handling |
|---|---|---|---|
| Human witness provenance is validated but not exposed in structured readiness-audit entries. | `HIGH_PRIORITY_HARDENING_GAP` | Current code validates `readiness_exclusion_human_checkpoint`, but `readiness_audit` task entries only expose `task_id`, `readiness`, and `notes`. | Prefer typed JSON contract hardening rather than schema or lifecycle change. |
| Risk Profile assignment source is safety-critical at task validation time but not exposed in structured readiness-audit entries. | `HIGH_PRIORITY_HARDENING_GAP` | `risk_assigned_by` blocks readiness when agent/self, but aggregate JSON only exposes resulting readiness and notes. | Prefer typed JSON contract hardening. |
| `NOT_RUN` semantics are enforced but surfaced mainly through reason strings rather than dedicated typed aggregate fields. | `MEDIUM_PRIORITY_CONTRACT_GAP` | Tests cover non-pass behavior, but the contract is partly text-driven. | Consider typed JSON contract field for blocker-category semantics. |
| Approval boundary inside readiness audit relies partly on top-level booleans and partly on text-only not-pass statements. | `MEDIUM_PRIORITY_CONTRACT_GAP` | `approval_claimed`, `commit_authorized`, `push_authorized`, `release_authorized` are present only at the top level. | Consider readiness-audit-local typed boundary fields in a future hardening slice. |
| Text-only safety phrases are relied on for human-readable clarity. | `LOW_PRIORITY_DOCUMENTATION_GAP` | `explicit_not_pass_statement` is a string list, not a typed enum/boolean contract. | Leave unchanged unless a later typed-contract stage is authorized. |
| JSON field stability for the current observed shape is only partially locked by tests. | `MEDIUM_PRIORITY_CONTRACT_GAP` | Current tests assert key fields but not a fuller contract manifest. | Extend contract tests only in a later authorized hardening stage. |
| No schema or lifecycle change is required to express the missing structured audit visibility. | `NO_ACTION_REQUIRED` | Gaps are in output contract visibility, not task-header schema capability or lifecycle semantics. | Keep schema and lifecycle unchanged in this stage. |

## 12. Risk classification

Overall audit classification: next hardening is justified, but no current blocking safety defect was found in the live baseline.

Reasoning:

- current baseline validation is fully `PASS`;
- current exclusion handling remains fail-closed;
- approval authority is not created by validator output;
- no false `PASS` condition was observed;
- remaining gaps are primarily contract-visibility and future-brittleness gaps, not current truthfulness failures.

## 13. Next hardening decision

- primary decision: `JSON_CONTRACT_HARDENING_RECOMMENDED`
- rationale: the most concentrated remaining gap is not schema or lifecycle semantics; it is that current safety-critical witness and Risk Profile provenance are validated but not expressed as typed structured readiness-audit contract fields.

## 14. Compact next-stage recommendation

- proposed next stage id: `AOS-FARM.646`
- proposed next stage title: `Readiness JSON Contract Hardening for Witness and Risk Provenance`
- next stage goal: add narrowly scoped structured readiness-audit fields for exclusion witness provenance and Risk Profile assignment source, and lock them with tests, without changing task schema, lifecycle semantics, approval semantics, or exclusion meaning.
- compact recommendation only: if a later stage is authorized, prefer JSON output hardening over schema/lifecycle redesign because the current contract gap is visibility and stability, not missing validation logic.

No execution authorization is created by this recommendation.

## 15. Explicit out-of-scope list

Out of scope for AOS-FARM.645:

- validator code changes
- test changes
- schema changes
- lifecycle logic changes
- registry creation
- live task mutation
- protected/canonical source changes
- commit
- push
- merge to main
- tag
- release
- canonical promotion

## 16. Safety boundary statement

The audit confirms the following boundaries remain intact in the current baseline:

- PASS is validation only, not approval.
- Evidence is not approval.
- CI PASS is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- EXCLUDED_TERMINAL is not PASS.
- EXCLUDED_LEGACY is not PASS.
- MALFORMED_EXCLUSION is fail-closed.
- Human approval cannot be simulated.
- Human witness cannot be fabricated.
- Agent cannot assign Risk Profile.
- Validation contract does not create approval authority.
- Report conclusions do not create execution authority.
- Next-stage recommendation does not authorize next-stage execution.

## 17. Residual risks

- Some safety semantics remain string-based rather than typed structured contract, especially for `NOT_RUN` explanations and explicit not-pass phrases.
- Human witness provenance and Risk Profile assignment source are currently easier to infer from implementation and task headers than from aggregate JSON alone.
- Future refactors could change readiness-audit entry detail without immediately breaking all intended contract expectations unless a later JSON contract stage hardens them more explicitly.

These are hardening candidates, not proof of current false `PASS`.

## 18. Commit/push boundary statement

This stage stops at report production, validation, diff review, and final audit return.

No commit was performed.
No push was performed.
No merge to main was performed.
No release action was performed.

Any later commit or push requires separate explicit human authorization.
