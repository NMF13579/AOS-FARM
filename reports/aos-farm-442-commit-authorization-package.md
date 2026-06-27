task_id: AOS-FARM.442.13
parent_task_id: AOS-FARM.442
title: Commit Authorization Package
branch: build/task-registry-queue-contract-mvp
risk_profile: HIGH_RISK_PROTECTED
execution_authorized_by_human: true
commit_requested: true
commit_authorized: false
push_authorized: false
commit_performed: false
push_performed: false
recommended_commit_message: "feat: add task registry and queue contract mvp"

# 1. Scope summary
This package implements the MVP for Task Registry and Task Queue Contracts, including templates, examples, read-only validation CLI and unittests.

# 2. Created/modified files
```
aos/docs/workflow/task-registry-and-queue.md
aos/reports/examples/task-registry/README.md
aos/reports/examples/task-registry/task-queue-example.md
aos/reports/examples/task-registry/task-registry-example.md
aos/scripts/aos_tasks.py
aos/templates/tasks/task-queue-template.md
aos/templates/tasks/task-registry-entry-template.md
aos/tools/optional/task_registry_validator.py
reports/aos-farm-442-0-candidate-acceptance-report.md
reports/aos-farm-442-1-branch-baseline-report.md
reports/aos-farm-442-10-tests-report.md
reports/aos-farm-442-11r-dogfood-show-next-mismatch-recovery-report.md
reports/aos-farm-442-1r-existing-branch-reuse-verification-report.md
reports/aos-farm-442-2-dirty-boundary-classification-report.md
reports/aos-farm-442-5-registry-queue-contract-docs-report.md
reports/aos-farm-442-6-templates-and-examples-report.md
reports/aos-farm-442-7-workflow-state-machine-contract-review-report.md
reports/aos-farm-442-8-validator-design-report.md
reports/aos-farm-442-9-read-only-inspection-cli-report.md
reports/aos-farm-442-commit-authorization-package.md
reports/aos-farm-442-dogfood-report.md
reports/aos-farm-442-dogfood-show-current.json
reports/aos-farm-442-dogfood-show-next.json
reports/aos-farm-442-dogfood-summary.json
reports/aos-farm-442-dogfood-task-queue.md
reports/aos-farm-442-dogfood-task-registry.md
reports/aos-farm-442-final-review-report.md
reports/aos-farm-442-task-brief-draft.md
reports/human-checkpoints/aos-farm-442-execution-authorization.md
tests/task_registry/test_task_registry_validator.py
```

# 3. Validation summary
unit_tests_passed: true
example_cli_validate_passed: true
example_cli_summary_passed: true
example_cli_show_current_passed: true
example_cli_show_next_passed: true
dogfood_cli_validate_passed: true
dogfood_cli_summary_passed: true
dogfood_cli_show_current_passed: true
dogfood_cli_show_next_passed: true
diff_check_passed: true
changed_files_within_authorized_scope: true

# 4. Dogfood summary
dogfood_initial_status: BLOCKED
dogfood_initial_reason: dogfood_failed
dogfood_recovery_status: PASS
dogfood_recovery_root_cause: "show-next used show-current selection logic"
dogfood_expected_show_next_matched_after_recovery: true

# 5. Recovery summary
Dogfood recovery applied a fix in the task_registry_validator to allow show-next to pick the *next* eligible task occurring after the currently *SELECTED* task in the queue, instead of defaulting to returning the current task again.

# 6. Safety boundary confirmation
PASS_is_not_approval: true
Evidence_is_not_approval: true
CI_PASS_is_not_approval: true
UNKNOWN_is_not_OK: true
NOT_RUN_is_not_PASS: true
human_approval_cannot_be_simulated: true
risk_profile_assignment_human_only: true
commit_requires_human_checkpoint: true
push_requires_separate_human_checkpoint: true

# 7. Out-of-scope confirmation
protected_canonical_sources_modified: false
agentos_paths_modified: false
github_paths_modified: false
release_paths_modified: false
runner_behavior_introduced: false
auto_approval_introduced: false
auto_execution_introduced: false
sqlite_implementation_introduced: false
rag_light_implementation_introduced: false
dirty_boundary_cleanup_performed: false
aos_farm_441_closure_report_committed: false

# 8. Commit request
A commit is requested for the authorized scope defined in AOS-FARM.442. 

# 9. Human decision required
human_decision_required: true
allowed_human_decisions:
  - APPROVED_FOR_COMMIT
  - REJECTED
  - NEEDS_CHANGES
commit_authorization_checkpoint_required: reports/human-checkpoints/aos-farm-442-commit-authorization.md
if_approved_next_step: AOS-FARM.442.14 Human Commit Authorization
if_rejected_next_step: BLOCKED
if_needs_changes_next_step: HUMAN_REVIEW_REQUIRED
final_status: HUMAN_REVIEW_REQUIRED
