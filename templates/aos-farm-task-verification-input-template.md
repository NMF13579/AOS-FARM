```yaml
task_id: ""
expected_branch: ""
expected_head: ""
expected_origin_dev: ""

required_files: []

allowed_created_files: []
allowed_modified_files: []

forbidden_created_files: []
forbidden_modified_files: []

expected_final_status: ""

must_be_false:
  - execution_authorized_now
  - commit_authorized_now
  - push_authorized_now
  - release_authorized_now
  - production_use_authorized_now

must_be_true: []

checkpoint_file: ""
checkpoint_expected_status: ""

human_approval_required_before_next_step: true
checker_may_report_no_mechanical_blockers: true
checker_must_not_authorize: true
```

### Example: AOS-FARM.142 Input
```yaml
task_id: AOS-FARM.142
expected_branch: dev
expected_head: 5664a74f767fb9fc0b0653113ca607c74f8cf5bb
expected_origin_dev: 5664a74f767fb9fc0b0653113ca607c74f8cf5bb

required_files:
  - 00_AOS_Core_Control.md
  - 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
  - 02_AOS_Governance_Control_Module_and_Safety_Rules.md
  - AGENTS.md
  - docs/operations/multi-environment-agent-workflow.md
  - reports/aos-farm-135-build-step-6-dogfood-evidence-report.md

allowed_created_files:
  - reports/aos-farm-142-build-step-7-controller-loop-scope-risk-batch-plan.md
  - reports/aos-farm-142-step-7-batch-1-execution-authorization-package.md
  - reports/human-checkpoints/aos-farm-142-step-7-batch-1-execution-authorization.md

checkpoint_file: reports/human-checkpoints/aos-farm-142-step-7-batch-1-execution-authorization.md
checkpoint_expected_status: PENDING_HUMAN_DECISION

must_be_false:
  - execution_authorized_now
  - commit_authorized_now
  - push_authorized_now
  - release_authorized_now
  - production_use_authorized_now
  - build_step_7_executed
  - staging_performed
  - commit_performed
  - push_performed
```
