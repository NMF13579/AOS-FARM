# AOS-FARM.TA-18 — Problem Intake MVP Batch Commit Authorization Package

## 1. Task Metadata
* **Task ID**: AOS-FARM.TA-18
* **Mode**: Commit authorization preparation / report-only / no commit / no push
* **Repository**: AOS-FARM
* **Branch**: dev
* **Current HEAD**: (Current local branch HEAD)
* **Current origin/dev**: (Current remote tracking branch HEAD)
* **Ahead/Behind Status**: (Aligned with local development)

## 2. Batch Scope
This batch covers the end-to-end implementation and evidence generation for the Minimal Problem Intake Runner MVP (Tasks TA-11 through TA-17). The scope includes gap analysis, runner design, runner implementation, a controlled example run, output validator design, output validator implementation, and the final evidence review.

## 3. Candidate File Set
The exact files pending commit authorization are:
* `reports/aos-farm-ta-11-problem-intake-automation-gap-recovery-plan.md`
* `reports/aos-farm-ta-12-minimal-problem-intake-runner-mvp-design.md`
* `agentos/scripts/problem_intake_runner.py`
* `agentos/reports/problem-intake/examples/ta-14-example-input.md`
* `agentos/reports/problem-intake/ta-14-example-run/PROJECT_SPEC.draft.md`
* `agentos/reports/problem-intake/ta-14-example-run/REQUIREMENTS.draft.md`
* `agentos/reports/problem-intake/ta-14-example-run/problem-interview-report.md`
* `agentos/reports/problem-intake/ta-14-example-run/requirements-checklist-draft.md`
* `agentos/reports/problem-intake/ta-14-example-run/problem-intake-run-report.md`
* `reports/aos-farm-ta-14-problem-intake-example-run-evidence.md`
* `reports/aos-farm-ta-15-problem-intake-runner-output-validator-design.md`
* `agentos/scripts/problem_intake_output_validator.py`
* `reports/aos-farm-ta-16-problem-intake-output-validator-run-report.md`
* `reports/aos-farm-ta-16-problem-intake-output-validator-implementation-report.md`
* `reports/aos-farm-ta-17-problem-intake-output-validator-evidence-review.md`
* `reports/aos-farm-ta-18-problem-intake-mvp-batch-commit-authorization-package.md`
* `reports/human-checkpoints/aos-farm-ta-18-problem-intake-mvp-batch-commit-authorization.md`

## 4. Excluded Files
No newly created TA-11 through TA-18 files have been excluded from this batch. The remainder of the untracked files in the repository belong to unrelated active or past execution branches and are intentionally excluded from this specific commit payload.

## 5. Safety Semantics
```yaml
approval_status: NOT_APPROVED
production_status: NOT_PRODUCTION
semantic_quality_status: NOT_VALIDATED
full_automation_status: NOT_PROVEN
commit_authorized_now: false
push_authorized_now: false
```

## 6. Recommended Commit Message
```text
feat: add problem intake runner mvp
```

## 7. Human Authorization Requirement
**CRITICAL**: Commit may only occur after the human checkpoint (`reports/human-checkpoints/aos-farm-ta-18-problem-intake-mvp-batch-commit-authorization.md`) is explicitly updated with:
```yaml
checkpoint_status: APPROVED_FOR_COMMIT
commit_authorized: true
authorized_commit_message: "feat: add problem intake runner mvp"
authorized_candidate_files:
  - (Exact list of files from Section 3)
```

## 8. Non-Goals
This task does not commit, push, release, approve production use, or validate semantic quality. It exists solely to prepare the exact file set and checkpoint required to advance the implementation safely.
