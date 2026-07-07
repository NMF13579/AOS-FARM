# AOS-FARM.635 — Downstream Task Brief Decision Record
## Status
decision_record_status: DRAFT_HUMAN_REVIEW_REQUIRED
approval_status: NOT_APPROVED
execution_authorization: NOT_AUTHORIZED
risk_profile_assignment: NOT_ASSIGNED
## Decision boundary
This document records the downstream decision boundary after Architecture-to-Task Export dogfood.
It is not execution approval.
It is not release approval.
It is not Risk Profile assignment.
It is not READY_FOR_EXECUTION.
It is not automatic approval.
## Inputs
- AOS-FARM.634 Evidence: aos/reports/architecture/aos-farm-634-architecture-to-task-export-dogfood-report.md
- Architecture artifact: tests/fixtures/architecture/aos_farm_633_valid_task_breakdown_dogfood.md
- Export artifact: aos/reports/architecture/aos-farm-634-architecture-to-task-export-dogfood-report.md
- Task Brief draft/export artifact, if present: DEFERRED_GAP / NOT_PRESENT
- Human review checklist: aos/reports/architecture/aos-farm-635-human-review-checklist.md
- Artifact inventory: aos/reports/architecture/aos-farm-635-artifact-inventory.md
- Final status report: aos/reports/architecture/aos-farm-635-final-status.md
## Task Brief draft/export artifact status
task_brief_draft_status: PRESENT_REVIEW_BLOCKED
Notes:
AOS-FARM.634 identified deferred gaps around missing template files and missing contract semantics.
AOS-FARM.635 does not create a new Task Brief draft by default.
If no concrete Task Brief draft/export artifact exists after inspection, this may be recorded as:
task_brief_draft_status: NOT_PRESENT
Missing Task Brief draft is not FAIL for AOS-FARM.635.
## Deferred gaps carried from AOS-FARM.634
1. Resolve missing template files:
   - aos/templates/aos_architecture_export.md
   - aos/templates/aos_task_brief_template.md
2. Map and implement validation for missing contract semantics, including:
   - source_lifecycle_status
   - forbidden_changes
   - validation_plan
3. Update strict scope check script to correctly handle git status paths containing quotes and spaces.
These gaps are not fixed by AOS-FARM.635.
## Decision options
1. ACCEPT_FOR_TASK_BRIEF_DRAFTING_ONLY
2. REJECT_EXPORT_CONTRACT
3. REQUEST_ADDITIONAL_DOGFOOD
4. BLOCKED_MISSING_EVIDENCE
5. BLOCKED_SCOPE_UNCLEAR
## Agent technical assessment
This assessment is not approval, not Risk Profile assignment, and not execution authorization.
agent_assessment:
  suggested_next_action: READY_FOR_HUMAN_TASK_BRIEF_DECISION
  confidence: MEDIUM
  rationale: AOS-FARM.634 Evidence is present and reviewable, but deferred gaps remain. AOS-FARM.635 can record the downstream decision boundary without fixing exporter/template gaps or creating a new Task Brief draft.
  approval_claim: false
  risk_profile_assigned: false
  execution_authorization_claim: false
Allowed suggested_next_action values:
- READY_FOR_HUMAN_TASK_BRIEF_DECISION
- REQUEST_ADDITIONAL_DOGFOOD
- BLOCKED_MISSING_EVIDENCE
- BLOCKED_SCOPE_UNCLEAR
- REJECT_EXPORT_CONTRACT
## Human decision
Decision:
Reviewer:
Date:
Explicit Risk Profile assignment, if any:
Execution authorization:
Commit authorization:
Push authorization:
Merge authorization:
Release authorization:
Notes:
## Required standalone phrase for drafting-only decision
HUMAN_REVIEW_RECORDED_DRAFTING_ONLY requires this standalone human phrase:
AOS HUMAN DECISION AOS-FARM.635 ACCEPT_FOR_TASK_BRIEF_DRAFTING_ONLY
Without that phrase, the default final status remains:
HUMAN_REVIEW_PACKAGE_READY
## Safety notes
- PASS is not approval.
- Evidence is not approval.
- CI PASS is not approval.
- NOT_RUN is not PASS.
- UNKNOWN is not OK.
- Human approval cannot be simulated.
- Risk Profile cannot be assigned by agent.
- Commit authorization is not push authorization.
- Push authorization is not merge authorization.
- Merge authorization is not release authorization.
