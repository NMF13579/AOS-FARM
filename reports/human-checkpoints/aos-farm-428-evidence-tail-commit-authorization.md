checkpoint_status: APPROVED_FOR_COMMIT
commit_authorized: true
human_decision_required: false

commit_target_details:
  - proposed_commit_message: "docs: record task brief assembly evidence tail"
  - exact_candidate_count: 7
  - exact_candidate_list:
    - reports/aos-farm-424-ta-to-task-brief-assembly-layer-commit-execution-report.md
    - reports/aos-farm-425-ta-to-task-brief-assembly-layer-push-authorization-package.md
    - reports/human-checkpoints/aos-farm-425-ta-to-task-brief-assembly-layer-push-authorization.md
    - reports/aos-farm-426-ta-to-task-brief-assembly-layer-push-execution-report.md
    - reports/aos-farm-426-ta-to-task-brief-assembly-layer-push-and-remote-baseline-closure.md
    - reports/aos-farm-428-evidence-tail-commit-authorization-package.md
    - reports/human-checkpoints/aos-farm-428-evidence-tail-commit-authorization.md

authorization_boundaries:
  - statement: A future commit may stage and commit only the exact candidate set listed above.
  - statement: Push is NOT authorized.
  - statement: Unrelated deletions in agentos/reports/* are strictly EXCLUDED.
