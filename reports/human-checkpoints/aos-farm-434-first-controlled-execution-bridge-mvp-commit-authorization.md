checkpoint_status: APPROVED_FOR_COMMIT
commit_authorized: true
human_decision_required: true

authorized_commit_message: "docs: add first controlled execution bridge mvp"

exact_candidate_list:
  - aos/START_HERE.md
  - aos/docs/workflow/consumer-runtime-handoff.md
  - aos/docs/workflow/controlled-task-workflow.md
  - aos/docs/workflow/first-session-guide.md
  - aos/docs/workflow/first-controlled-execution.md
  - aos/prompts/controlled-execution.md
  - aos/templates/authorization/execution-authorization-package-template.md
  - aos/templates/checkpoints/human-execution-authorization-template.md
  - aos/templates/checkpoints/human-push-authorization-template.md
  - aos/templates/reports/execution-report-template.md
  - aos/templates/reports/verification-report-template.md
  - aos/templates/reports/evidence-review-template.md
  - aos/templates/task-briefs/controlled-task-brief-template.md
  - aos/templates/verification/post-execution-verification-template.md
  - reports/aos-farm-434-first-controlled-execution-bridge-mvp.md
  - reports/aos-farm-434-first-controlled-execution-bridge-mvp-commit-authorization-package.md
  - reports/human-checkpoints/aos-farm-434-first-controlled-execution-bridge-mvp-commit-authorization.md

validation_status:
  - git_diff_check: PASS
  - documented_markdown_validation_command: NOT_RUN

authorization_boundaries:
  - commit_is_not_yet_performed: true
  - push_is_not_authorized: true
  - AOS_FARM_435_is_not_authorized: true
  - exact_candidate_file_list_is_the_only_authorized_stage_commit_scope: true
  - unrelated_pre_existing_dirty_worktree_paths_are_out_of_scope: true
  - local_AOS_FARM_433_push_authorization_artifacts_are_out_of_scope: true
  - no_runner_automation_SQLite_RAG_vector_DB_CI_or_Spec_Kit_execution_was_added: true
