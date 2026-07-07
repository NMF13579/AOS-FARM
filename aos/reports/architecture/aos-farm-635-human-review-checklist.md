# AOS-FARM.635 — Architecture-to-Task Export Human Review Checklist
## Status
review_status: DRAFT_HUMAN_REVIEW_REQUIRED
approval_status: NOT_APPROVED
execution_authorization: NOT_AUTHORIZED
risk_profile_assignment: NOT_ASSIGNED
## Review target
- Architecture artifact: tests/fixtures/architecture/aos_farm_633_valid_task_breakdown_dogfood.md
- Export artifact: aos/reports/architecture/aos-farm-634-architecture-to-task-export-dogfood-report.md
- Task Brief draft/export output: DEFERRED_GAP / NOT_PRESENT
- Evidence report: aos/reports/architecture/aos-farm-634-architecture-to-task-export-dogfood-report.md
- Artifact inventory: aos/reports/architecture/aos-farm-635-artifact-inventory.md
- Final status report: aos/reports/architecture/aos-farm-635-final-status.md
## Non-approval notice
This checklist is not approval by itself.
PASS is not approval.
Evidence is not approval.
CI PASS is not approval.
UNKNOWN is not OK.
NOT_RUN is not PASS.
Human approval cannot be simulated.
## Required checks
- [ ] Architecture artifact is identifiable.
- [ ] Export artifact is traceable to architecture artifact.
- [ ] Export does not mutate lifecycle.
- [ ] Export does not assign Risk Profile.
- [ ] Export does not claim approval.
- [ ] Export does not treat PASS as approval.
- [ ] Export does not treat Evidence as approval.
- [ ] Export does not treat CI PASS as approval.
- [ ] Export does not treat NOT_RUN as PASS.
- [ ] Export does not treat UNKNOWN as OK.
- [ ] Downstream Task Brief boundary is explicit.
- [ ] Task Brief draft/export artifact status is recorded.
- [ ] Deferred gaps are recorded but not fixed in AOS-FARM.635.
- [ ] Forbidden operations are preserved.
- [ ] Human decision is required before downstream drafting.
- [ ] Separate authorization is required before commit.
- [ ] Separate authorization is required before push.
- [ ] Separate authorization is required before merge/release.
## Human decision options
- [ ] ACCEPT_FOR_TASK_BRIEF_DRAFTING_ONLY
- [ ] REJECT_EXPORT_CONTRACT
- [ ] REQUEST_ADDITIONAL_DOGFOOD
- [ ] BLOCKED_MISSING_EVIDENCE
- [ ] BLOCKED_SCOPE_UNCLEAR
- [ ] OTHER: __________
## Human decision record
Decision:
Reviewer:
Date:
Notes:
## Required standalone phrase for drafting-only decision
HUMAN_REVIEW_RECORDED_DRAFTING_ONLY is allowed only if the human provides this standalone phrase outside quoted plan, code block, assistant text, or task document:
AOS HUMAN DECISION AOS-FARM.635 ACCEPT_FOR_TASK_BRIEF_DRAFTING_ONLY
Without that phrase, the safe default final status remains:
HUMAN_REVIEW_PACKAGE_READY
