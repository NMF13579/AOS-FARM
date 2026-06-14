# AOS-FARM.118 — Step 5 Batch 1 Execution Authorization Package

## Goal
Authorize the execution of `AOS-FARM.120` (Code Assembly Pipeline MVP Batch).

## Bounded Scope (Exact File List)
The execution of `AOS-FARM.120` is strictly limited to creating/modifying the following files:

1. `docs/assembly/code-assembly-pipeline-mvp.md`
2. `templates/code-assembly-mvp-input-template.md`
3. `templates/code-assembly-mvp-execution-report-template.md`
4. `templates/code-assembly-mvp-evidence-report-template.md`
5. `templates/code-assembly-mvp-human-review-template.md`
6. `reports/aos-farm-code-assembly-pipeline-mvp-report.md`

## Forbidden Operations
Unless explicitly overridden by human authorization, the following operations are forbidden during `AOS-FARM.120`:
- Runtime enforcement creation
- Validator implementation
- CI workflow changes
- Protected/canonical file changes
- Spec Kit commands execution
- Destructive operations
- Automatic merge
- Release
- Production use

## Manual Review Expectations
Before validator implementation is established, the pipeline will heavily rely on:
- `manual_human_review_required: true`
- `validator_status: NOT_RUN` (never treated as pass)
- `not_run_treated_as_pass: false`
- `evidence_required: true`

## Next Step
Human must review this package and fill out the human execution authorization checkpoint at `reports/human-checkpoints/aos-farm-118-step-5-batch-1-execution-authorization.md`.
