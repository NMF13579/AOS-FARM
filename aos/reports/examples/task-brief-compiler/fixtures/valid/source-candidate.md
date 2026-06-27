# Valid Source Candidate For Compiler Fixture

candidate_task_id: AOS-FARM.FIXTURE.COMPILER.CANDIDATE
source_backlog_item: GAP-COMPILER-001
source_evidence: reports/compiler-evidence.md
candidate_goal: draft a review-only controlled task brief from accepted candidate material
candidate_scope: create one review-only task brief draft in the product-facing aos layer
out_of_scope: execution authorization, Risk Profile assignment, commit, push, merge, release, next-task start
allowed_files: aos/docs/workflow/, aos/templates/task-briefs/
forbidden_files: 00_AOS_Core_Control.md, 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md, 02_AOS_Governance_Control_Module_and_Safety_Rules.md
validation_plan: verify field completeness, preserve false authorization flags, stop at human review
proposed_risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by: null
execution_authorized: false
commit_authorized: false
push_authorized: false
approval_claimed: false
status: DRAFT

Safety notes:
- PASS is not approval.
- Evidence is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Human approval cannot be simulated.
