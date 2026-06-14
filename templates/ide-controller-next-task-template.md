# IDE Controller Next Task Directive

## Task Definition
- **task_id:** [Task ID]
- **mode:** [Execution / Verification / Recovery / Audit]
- **repository:** [Repo]
- **branch:** [Branch]
- **risk_profile:** [Profile]
- **token_budget:** [Cheap / Standard / Expensive]
- **model_routing:** [Target Role/Model]
- **context:** [Background context]
- **goal:** [Goal description]

## Sources and Rules
- **required_sources:** [List]
- **source_precedence:** [00 > 01 > 02]

## Bounded Scope
- **scope:** [Summary]
- **allowed_actions:** [List]
- **forbidden_actions:** [List]

## Execution
- **required_checks:** [List of pre-execution checks]
- **session_limit_rule:** [Stop before limit; write handoff if interrupted]

## Output Requirements
- **expected_outputs:** [List of files]
- **expected_final_report:** [Report details]
- **allowed_final_statuses:** [List]
- **final_fail_closed_rule:** [Rule condition for failing closed]
