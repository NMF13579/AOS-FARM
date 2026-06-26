checkpoint_status: APPROVED_FOR_COMMIT
commit_authorized: true
human_decision_required: true

authorized_commit_message: "docs: add first controlled execution flow audit"

exact_candidate_list:
  - reports/aos-farm-433-first-controlled-task-execution-flow-audit-and-design.md
  - reports/aos-farm-433-first-controlled-task-execution-flow-commit-authorization-package.md
  - reports/human-checkpoints/aos-farm-433-first-controlled-task-execution-flow-commit-authorization.md

authorization_boundaries:
  - Commit is not yet performed.
  - Push is explicitly NOT authorized.
  - AOS-FARM.434 is NOT authorized.
  - Unrelated pre-existing dirty worktree paths are out of scope.
  - Only the exact candidate list above may be staged and committed after explicit human approval.
  - No aos/, docs/, templates/, prompts/, or protected/canonical root files are authorized for this commit.
