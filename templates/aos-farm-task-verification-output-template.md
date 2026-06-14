```yaml
task_id: ""
verification_status: PASS | PASS_WITH_WARNINGS | BLOCKED | UNKNOWN

branch_check: PASS | BLOCKED | UNKNOWN
head_check: PASS | BLOCKED | UNKNOWN
origin_dev_check: PASS | BLOCKED | UNKNOWN
remote_baseline_check: PASS | BLOCKED | UNKNOWN
required_files_check: PASS | BLOCKED | UNKNOWN
allowed_files_check: PASS | BLOCKED | UNKNOWN
forbidden_files_check: PASS | BLOCKED | UNKNOWN
authorization_boundary_check: PASS | BLOCKED | UNKNOWN
checkpoint_state_check: PASS | BLOCKED | UNKNOWN
human_approval_simulation_check: PASS | BLOCKED | UNKNOWN

evidence:
  current_branch: ""
  head: ""
  origin_dev: ""
  dev_ahead_origin_dev_by: ""
  origin_dev_ahead_dev_by: ""
  created_files_seen: []
  modified_files_seen: []
  missing_required_files: []
  unauthorized_files_seen: []

authorization_status:
  execution_authorized_now: false
  commit_authorized_now: false
  push_authorized_now: false
  release_authorized_now: false
  production_use_authorized_now: false

checker_boundary:
  checker_grants_approval: false
  checker_grants_execution_authorization: false
  checker_grants_commit_authorization: false
  checker_grants_push_authorization: false
  checker_simulates_human_decision: false

final_recommendation: ""
final_status: ""
```

### Allowed Recommendation Phrases
- препятствий для Human Execution Authorization не найдено
- препятствий для commit не найдено
- препятствий для push не найдено
- механические blocker не найдены
- требуется human checkpoint
- BLOCKED: required evidence missing
- UNKNOWN: evidence unavailable

### Forbidden Recommendation Phrases
- approved
- execution approved
- commit approved
- push approved
- human approval completed
- Risk Profile assigned by checker
