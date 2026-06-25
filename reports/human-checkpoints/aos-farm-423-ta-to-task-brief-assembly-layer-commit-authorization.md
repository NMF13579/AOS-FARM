checkpoint_status: APPROVED_FOR_COMMIT
commit_authorized: true
human_decision_required: true

authorized_commit_message: "docs: add technical assignment task brief assembly layer"

exact_candidate_list:
  - reports/aos-farm-420-ta-to-task-brief-assembly-gap-audit-and-design.md
  - aos/docs/workflow/technical-assignment-to-task-brief.md
  - aos/prompts/task-brief-builder.md
  - aos/templates/task-briefs/task-breakdown-template.md
  - aos/templates/task-queue-template.md
  - aos/START_HERE.md
  - aos/docs/workflow/first-session-guide.md
  - aos/templates/task-briefs/controlled-task-brief-template.md
  - reports/aos-farm-421-ta-to-task-brief-assembly-layer-implementation-report.md
  - reports/aos-farm-422-ta-to-task-brief-assembly-layer-post-execution-verification.md
  - reports/aos-farm-423-ta-to-task-brief-assembly-layer-commit-authorization-package.md
  - reports/human-checkpoints/aos-farm-423-ta-to-task-brief-assembly-layer-commit-authorization.md

authorization_boundaries:
  - If approved, the future commit may stage and commit ONLY the exact candidate set listed above.
  - Push is explicitly NOT authorized.
