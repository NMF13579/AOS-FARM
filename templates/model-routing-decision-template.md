# Model Routing Decision

## Decision Metadata
- **routing_decision_id:** [Unique ID]
- **task_id:** [Task ID]
- **task_type:** [Description]
- **current_environment:** [Environment]

## Routing Choice
- **selected_role:** [Controller / Executor / Verifier / Auditor / Router / Handoff Writer]
- **selected_model_tier:** [Cheap / Standard / Expensive]
- **escalation_model_tier:** [Standard / Expensive / None]
- **reason_for_selection:** [Rationale]

## Boundaries and Capabilities
- **authority_sensitive:** [true / false]
- **human_checkpoint_required_before_next_phase:** [true / false]
- **can_delegate_to_cheaper_model:** [true / false]
- **can_escalate_to_expensive_model:** [true / false]
- **can_continue_after_model_switch:** [true / false]
- **approval_state_unchanged:** `true`
- **routing_decision_is_not_approval:** `true`
- **required_report_inclusion:** [true / false]
