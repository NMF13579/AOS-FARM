schema_version: 1
package_type: code_execution_package
task_id: AOS-FARM.453
task_title: Add Overengineering Review Gate to Code Execution Corridor
source_task_brief: reports/aos-farm-453-task-brief.md
execution_authorized: true
execution_authorization_source: explicit_human_command_in_chat
risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by_human: true
risk_profile_assigned_by: human
implementation_scope: Add lightweight overengineering review controls to Code Execution Corridor templates and validator reporting.
allowed_files:
  - aos/templates/code-execution-package-template.md
  - aos/templates/code-quality-review-template.md
  - aos/scripts/aos_code_quality_control.py
  - tests/test_aos_code_quality_control.py
  - tests/fixtures/code_quality_control/
  - reports/aos-farm-453-*.md
forbidden_files:
  - 00_AOS_Core_Control.md
  - 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
  - 02_AOS_Governance_Control_Module_and_Safety_Rules.md
  - aos/root/AGENTS.md
  - README.md
  - START_HERE*
  - .github/workflows/
overengineering_controls:
  expected_change_size: small
  max_touched_files_soft: 5
  max_new_files_soft: 2
  max_added_lines_soft: 250
  max_new_dependencies: 0
  max_new_classes_soft: 0
  max_new_functions_soft: 2
  architecture_change_allowed: false
  future_only_code_allowed: false
  scope_expansion_allowed: false
  validator_semantics_change_allowed: false
  validator_reporting_extension_allowed: true
  lifecycle_semantics_change_allowed: false
  protected_canonical_change_allowed: false
  compression_review_required: true
  simpler_alternative_required: true
deterministic_code_boundary:
  allowed:
    - field presence checks
    - overengineering_controls presence check
    - structured warnings
    - explicit human_review_required true
    - explicit approval_granted false
    - explicit commit/push/release authorization false
  forbidden:
    - automatic approval
    - automatic rejection by complexity budget
    - lifecycle mutation
    - Risk Profile assignment
    - commit authorization
    - push authorization
    - release authorization
    - auto-fix loop
    - autonomous runner behavior
required_tests:
  - python3 -m unittest -v tests/test_aos_code_quality_control.py
required_checks:
  - git diff --check
  - git diff --stat
  - git diff --name-status
  - protected/canonical diff check
  - validator validate-package check
  - validator summarize check
stop_before_commit: true
stop_before_push: true
stop_before_release: true
human_review_required: true
approval_granted: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
approval_record_creation_allowed: false
lifecycle_mutation_authorized: false
