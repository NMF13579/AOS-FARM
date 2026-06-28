# AOS-FARM.456 — Forbidden Behavior Evidence Mapping Task Brief

## 1. Task identity
- **Task ID**: AOS-FARM.456
- **Status**: DRAFT_FOR_HUMAN_EXECUTION_AUTHORIZATION

## 2. Purpose
Forbidden behaviors must no longer remain bare declarations. Each forbidden behavior must have an Evidence mapping or explicit NOT_RUN / UNKNOWN / HUMAN_REVIEW_REQUIRED handling.

AOS-FARM.456 continues AOS-FARM.454 and AOS-FARM.455.
AOS-FARM.454 added `functional_intent` and `forbidden_behaviors` to Task Quality Package.
AOS-FARM.455 added human-readable SELF_TEST Functional Verification Bridge.
AOS-FARM.456 maps `forbidden_behaviors` to Evidence and verification status.

## 3. Problem statement
`functional_intent.forbidden_behaviors` → forbidden behavior evidence mapping → evidence item → verification method → verification status → Human Review note.

## 4. Scope
In scope for later implementation phase:
- `aos/templates/forbidden-behavior-evidence-mapping.md`
- `aos/schemas/forbidden-behavior-evidence-mapping.schema.json`
- `aos/scripts/aos_task_quality_check.py`
- `tests/fixtures/forbidden_behavior_evidence_mapping/`
- `tests/test_forbidden_behavior_evidence_mapping.py`
- `reports/aos-farm-456-forbidden-behavior-evidence-mapping-concept.md`
- `reports/aos-farm-456-dogfood-report.md`
- `reports/aos-farm-456-evidence-report.md`
- `reports/aos-farm-456-human-review-request-no-approval.md`

## 5. Out of scope
No canonical governance rewrite.
No changes to `00_AOS_Core_Control.md`.
No changes to `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`.
No changes to `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
No changes to `aos/SELF_TEST.md`.
No CI.
No runner.
No autonomous execution.
No approval automation.
No auto-fix.
No auto-commit.
No auto-push.
No merge.
No release.
No RAG-light.
No SQLite.
No runtime runners.
No AOS-FARM.457.

## 6. Allowed files for implementation phase
See Scope.

## 7. Forbidden files
See Out of scope.

## 8. Expected implementation shape
A new schema/template for evidence mapping, extension of the validator to handle mapping explicitly, tests for the validator extension, and related reports.

## 9. Validator boundary
The validator may only check binary/structural facts:
- mapping file exists
- mapping file parses
- schema_version exists
- task_id exists
- related_quality_package exists
- forbidden_behavior_evidence_mappings is present
- mapping items are non-empty when forbidden_behaviors exist
- each mapping has verification_status
- NOT_RUN is explicit
- UNKNOWN is explicit
- approval_boundary exists
- final_status is not APPROVED
- validator does not grant approval
- validator does not grant commit authorization
- validator does not grant push authorization
- validator does not grant merge authorization
- validator does not grant release authorization

Validator must not check:
- semantic absence of forbidden behavior
- sufficiency of Evidence by meaning
- whether the task can be approved
- whether commit/push/merge/release is authorized

## 10. Approval boundary
- PASS is not approval.
- Evidence is not approval.
- CI PASS is not approval.
- Mapping validation is not approval.
- Human approval cannot be simulated.
- Validator cannot grant approval.
- Validator cannot grant commit authorization.
- Validator cannot grant push authorization.
- Validator cannot grant merge authorization.
- Validator cannot grant release authorization.

## 11. Risk Profile
- **Suggested Risk Profile**: HIGH_RISK_PROTECTED
- Human Risk Profile assignment required.
- Agent cannot assign LOW_RISK_FAST.
- Human execution authorization required before implementation.

## 12. Human checkpoints
- Risk Profile Assignment
- Execution Authorization
- Final Review (Pre-Commit / Pre-Push)

## 13. Definition of Done
The task is done when all tests pass, reports are generated, and a Human Review Request is created, without bypassing any safety boundaries.

## 14. Execution status
DRAFT_FOR_HUMAN_EXECUTION_AUTHORIZATION
