# Multi-Environment Handoff Template

## Handoff Metadata
- **handoff_id:** [Unique ID]
- **from_environment:** [Source Environment]
- **to_environment:** [Target Environment]
- **current_branch:** [Branch name]
- **HEAD:** [Commit SHA]
- **origin_dev:** [Commit SHA]
- **local_ahead_origin_dev_by:** [Count]
- **origin_dev_ahead_local_by:** [Count]
- **working_tree_status:** [Clean / Dirty]

## Workflow State
- **current_task:** [Task ID]
- **current_phase:** [Planning / Execution / Verification / Audit / Closure]
- **completed_steps:** [List]
- **incomplete_steps:** [List]
- **last_final_status:** [Status enum]
- **next_safe_task:** [Action description]
- **blocked:** [true / false]
- **required_human_action:** [Description of action needed]

## Authorization Status
- **execution_authorized_now:** [true / false]
- **commit_authorized_now:** [true / false]
- **push_authorized_now:** [true / false]
- **release_authorized_now:** [true / false]
- **production_use_authorized_now:** [true / false]

## File State
- **files_created_or_modified:** [List]
- **files_not_yet_verified:** [List]
- **pending_untracked_files:** [List]
- **pending_modified_files:** [List]
- **pending_staged_files:** [List]
- **exact_checkpoint_paths:** [List]

## Routing and Limits
- **model_tier_used:** [Cheap / Standard / Expensive]
- **routing_decisions_made:** [List]
- **session_limit_reason:** [Token limit / Usage limit / User interruption]

## Final Boundary Note
[Explicitly state that this handoff acts as Evidence and does NOT convert PASS, Evidence, or model choices into human approval.]
