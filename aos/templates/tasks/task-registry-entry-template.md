# Task Registry Entry Template

```yaml
schema_version: 1
task_id: AOS-FARM.XXX
title: "<task title>"
source_file: null
source_commit: null
source_hash: null
indexed_at: null
registry_status: CANDIDATE
lifecycle_stage: CANDIDATE
depends_on: []
blocked_by: []
replaces: []
replaced_by: null
task_brief_status: NOT_CREATED
risk_profile_assigned_by_human: false
risk_profile: null
execution_authorized: false
commit_authorized: false
push_authorized: false
next_action: PREPARE_TASK_BRIEF
final_status: HUMAN_REVIEW_REQUIRED
```

## Template Rules
- Task ID is stable.
- Title is not identity.
- Registry entry may report task state.
- Registry entry must not approve, authorize, execute, commit, or push.
- SQLite/RAG-light metadata fields do not create authority.
- **Queue position is not approval.**
- **show-current is not execution.**
- **show-next is not execution.**
