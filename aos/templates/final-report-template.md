# Final Report Template

> **GUIDANCE BOUNDARY:**
> This document is a template for execution and Evidence final reports.
> It is guidance and navigation only.
> Canonical governance remains in `00_AOS_Core_Control.md`,
> `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and
> `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
> This template does not grant approval, execution permission, commit permission,
> push permission, merge permission, release permission, or lifecycle mutation
> permission.

---

> **MANDATORY STATEMENT:**
> This report is Evidence/reporting only.
> It is not approval.
> It does not authorize lifecycle mutation, commit, push, merge, release,
> or next-stage transition.

---

## Instructions for Use

Copy this template and fill in all sections for the completed task or stage.
Do not mark status as `APPROVED` or `READY_FOR_AUTO_EXECUTION`.
The final status must be `READY_FOR_HUMAN_REVIEW`.

---

```markdown
# Final Report — [Task / Stage ID]

## Result

status: READY_FOR_HUMAN_REVIEW
<!-- Do not write APPROVED or READY_FOR_AUTO_EXECUTION. -->

---

## Task / Stage

task_or_stage: 
<!-- Example: AOS-FARM.571 Stage 3 — Documentation Implementation -->

---

## Branch / HEAD

branch: 
head_commit: 

---

## Changed Files

<!-- List every file created or modified during this task. -->
files_created:
  - 

files_modified:
  - 

---

## Summary of Changes

<!-- Describe what was changed and why, in plain language. -->
summary: 

---

## Validation Run

<!-- List every validation command run during or after implementation. -->
validation_commands_run:
  - command: 
    result: 
    <!-- Options: PASS / FAIL / NOT_RUN -->

---

## Validation Results

<!-- Summarize the overall result of validation. -->
<!-- Reminder: PASS is not approval. -->
validation_summary: 
<!-- Example: "All py_compile checks passed. Unit test discovery found 0 tests.
     NOT_RUN: integration tests (environment unavailable)." -->

---

## Evidence

<!-- List all Evidence artifacts collected during this task. -->
evidence:
  - 

---

## Not-Run

<!-- List all validation steps that were not run. -->
<!-- NOT_RUN is not PASS. -->
not_run:
  - validation_step: 
    reason: 

---

## Unknowns

<!-- List any unknown states discovered during this task. -->
unknowns:
  - 

---

## Blockers

<!-- List any blockers that remain after this task. -->
blockers:
  - 

---

## Safety Boundary Check

<!-- Confirm each invariant was maintained. -->
pass_equals_approval: false
<!-- PASS ≠ approval — confirm: false means it was NOT treated as approval -->

evidence_equals_approval: false
ci_pass_equals_approval: false
unknown_treated_as_ok: false
not_run_treated_as_pass: false
human_approval_simulated: false
scope_expanded_without_permission: false

---

## Protected/Canonical Files Touched

protected_canonical_files_touched: 
<!-- Answer: No / Yes (if Yes, list which files and confirm checkpoint existed) -->
files_if_yes:
  - 

---

## Lifecycle Mutation

lifecycle_mutation_performed: 
<!-- Answer: No / Yes (if Yes, describe what was mutated and confirm authorization) -->
description_if_yes: 

---

## Approval Claimed

approval_claimed: 
<!-- Answer: No / Yes (should always be No — agents do not claim approval) -->

---

## Commit Performed

commit_performed: 
<!-- Answer: No / Yes — if Yes, commit must have had explicit human authorization -->
commit_hash_if_yes: 
commit_authorization_checkpoint_if_yes: 

---

## Push Performed

push_performed: 
<!-- Answer: No / Yes — if Yes, push must have had explicit human authorization -->
push_authorization_checkpoint_if_yes: 

---

## Human Review Required

human_review_required: true
<!-- Always true for READY_FOR_HUMAN_REVIEW status -->
review_notes: 
<!-- What specifically does the human need to review? -->

---

## Next Recommended Action

<!-- What is the recommended next safe step? -->
<!-- Do not phrase as "proceed" or "approved" — phrase as a recommendation only. -->
next_recommended_action: 

---

## Final Boundary Statement

This report is Evidence/reporting only.
It is not approval.
It does not authorize lifecycle mutation, commit, push, merge, release,
or next-stage transition.
Human decision is still required before any of those actions may be taken.
```

---

*This template is guidance only. It does not grant execution, commit, push,
merge, release, or approval permission. Canonical governance in 00/01/02
always takes precedence.*
