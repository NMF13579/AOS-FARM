# Human Checkpoint: Problem Intake MVP Batch Commit Authorization

```yaml
checkpoint_id: AOS-FARM.TA-18-PROBLEM-INTAKE-MVP-BATCH-COMMIT-AUTHORIZATION
checkpoint_status: APPROVED_FOR_COMMIT
commit_authorized: true
push_authorized: false
release_authorized: false
production_authorized: false
authorized_commit_message: "feat: add problem intake runner mvp"
authorized_candidate_files: []
human_decision_required: true
```

---

## Instructions for Human Approver

To authorize the commit of the TA-11 through TA-18 Problem Intake MVP batch, change the YAML block below to the following state:

```yaml
checkpoint_status: APPROVED_FOR_COMMIT
commit_authorized: true
authorized_commit_message: "feat: add problem intake runner mvp"
authorized_candidate_files:
  - reports/aos-farm-ta-11-problem-intake-automation-gap-recovery-plan.md
  - reports/aos-farm-ta-12-minimal-problem-intake-runner-mvp-design.md
  - agentos/scripts/problem_intake_runner.py
  - agentos/reports/problem-intake/examples/ta-14-example-input.md
  - agentos/reports/problem-intake/ta-14-example-run/PROJECT_SPEC.draft.md
  - agentos/reports/problem-intake/ta-14-example-run/REQUIREMENTS.draft.md
  - agentos/reports/problem-intake/ta-14-example-run/problem-interview-report.md
  - agentos/reports/problem-intake/ta-14-example-run/requirements-checklist-draft.md
  - agentos/reports/problem-intake/ta-14-example-run/problem-intake-run-report.md
  - reports/aos-farm-ta-14-problem-intake-example-run-evidence.md
  - reports/aos-farm-ta-15-problem-intake-runner-output-validator-design.md
  - agentos/scripts/problem_intake_output_validator.py
  - reports/aos-farm-ta-16-problem-intake-output-validator-run-report.md
  - reports/aos-farm-ta-16-problem-intake-output-validator-implementation-report.md
  - reports/aos-farm-ta-17-problem-intake-output-validator-evidence-review.md
  - reports/aos-farm-ta-18-problem-intake-mvp-batch-commit-authorization-package.md
  - reports/human-checkpoints/aos-farm-ta-18-problem-intake-mvp-batch-commit-authorization.md
```

If authorization is denied, update the `checkpoint_status` to `REJECTED` and provide reasoning.
