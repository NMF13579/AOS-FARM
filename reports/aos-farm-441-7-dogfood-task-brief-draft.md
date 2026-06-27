# Compiled Task Brief Draft

task_brief_draft_status: DRAFT
source_candidate: aos/reports/examples/task-brief-compiler/fixtures/valid/source-candidate.md
source_selection_decision: aos/reports/examples/task-brief-compiler/fixtures/valid/accepted-selection.md
candidate_goal: draft a review-only controlled task brief from accepted candidate material
scope: create one review-only task brief draft in the product-facing aos layer
out_of_scope: execution authorization, Risk Profile assignment, commit, push, merge, release, next-task start
allowed_files: aos/docs/workflow/, aos/templates/task-briefs/
forbidden_files: 00_AOS_Core_Control.md, 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md, 02_AOS_Governance_Control_Module_and_Safety_Rules.md
validation_plan: verify field completeness, preserve false authorization flags, stop at human review
proposed_risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by_human: false
execution_authorized: false
commit_authorized: false
push_authorized: false
human_review_required: true
final_status: HUMAN_REVIEW_REQUIRED

## Safety Boundary
- This draft is review-only.
- This draft is not executable until human review and explicit authorization.
- This draft does not assign Risk Profile.
- This draft does not authorize execution.
- This draft does not authorize commit or push.
- This draft does not start the next task.
- PASS is validation result only, not approval.
- Evidence is not approval.
- CI PASS is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Human approval cannot be simulated.
