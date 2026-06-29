---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Task Brief Draft Example

task_brief_draft_status: DRAFT
source_candidate: aos/reports/examples/evidence-to-backlog/next-task-candidate-example.md
source_selection_decision: aos/reports/examples/next-task-selection/selection-accept-example.md
candidate_goal: prepare a review-only Task Brief draft from an accepted next-task candidate
scope: create one draft Task Brief for human review
out_of_scope:
- execution authorization
- Risk Profile assignment
- commit
- push
- merge
- release
- next-task start
allowed_files:
- aos/docs/workflow/
- aos/templates/task-briefs/
- aos/reports/examples/task-brief-compiler/
forbidden_files:
- 00_AOS_Core_Control.md
- 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
- 02_AOS_Governance_Control_Module_and_Safety_Rules.md
validation_plan:
- review field completeness
- review boundary flags remain false
- stop at human review
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
