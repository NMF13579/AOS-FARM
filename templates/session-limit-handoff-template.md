# Session-Limit Handoff Template

## Handoff Metadata
- **task_id:** [Task ID]
- **session_limit_detected:** [true]
- **limit_type:** [Token Limit / Usage Limit / Timeout / Pre-Commit Safety / Pre-Push Safety]

## Progress State
- **current_phase:** [Phase]
- **completed_work:** [List]
- **incomplete_work:** [List]

## Working Tree State
- **files_created_or_modified:** [List]
- **files_not_yet_verified:** [List]
- **branch:** [Branch name]
- **HEAD:** [Commit SHA]
- **origin_dev:** [Commit SHA]
- **working_tree_status:** [Clean / Dirty]
- **staged_files:** [List]

## Authorization
- **authorization_state:** [Execution / Commit / Push / None]
- **commit_authorized:** [true / false]
- **push_authorized:** [true / false]
- **release_authorized:** [true / false]
- **production_use_authorized:** [true / false]

## Next Steps
- **next_safe_action:** [Action]
- **recommended_next_model_tier:** [Cheap / Standard / Expensive]
- **final_safe_status:** [Status enum]
- **do_not_continue_rules:** [DO NOT start commit or push if near limit. Write this handoff instead.]
