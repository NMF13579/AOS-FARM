# Controlled Execution Evidence Report Template

Use this template after controlled execution and before human review. NOT_RUN must not be listed as PASS. Evidence Report does not authorize commit. Evidence Report does not authorize push.

## Status
task_id:
task_title:
risk_profile:
risk_profile_assigned_by:
human_execution_authorization:
controlled_task_brief:
execution_package:
final_status:

## Human-readable Summary

### What changed
- [Plain-language summary, 1-5 bullets]

### What was checked
- [Commands, validators, review steps, or manual checks]

### What was not checked
- [Every skipped/unavailable check must remain NOT_RUN or explicitly unavailable. Do not convert NOT_RUN into PASS.]

### What remains UNKNOWN
- [List unresolved UNKNOWN items. If none, say "none found during this scoped review"]

### Decision needed
- [State whether a human decision is required and what the human must decide]

### Safety reminder
- PASS is not approval.
- Evidence is not approval.
- Human approval is separate wherever an approval boundary exists.

## Decision Needed

Human decision required: [yes/no/unknown]

Decision options:
1. Accept Evidence as sufficient for this scoped stage.
2. Request additional verification.
3. Reject result and reopen the task.
4. Block due to UNKNOWN, missing Evidence, or scope issue.

This decision block does not grant:
1. Release authorization.
2. Merge authorization.
3. Push authorization.
4. General approval outside the stated scope.
5. Lifecycle mutation unless explicitly authorized elsewhere.

## Guard Results
precheck:
scopecheck:
postcheck:

## Execution Scope
authorized_files:
changed_files:
out_of_scope_changes:

## Commands
commands_run:
commands_not_run:
commands_blocked:

## Evidence
tests:
validation:
manual_review_notes:

## NOT_RUN

## UNKNOWN

## BLOCKED

## Approval Boundary
PASS_is_not_approval: true
Evidence_is_not_approval: true
CI_PASS_is_not_approval: true
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
next_task_authorized: false

## Final Decision
final_status:
human_review_required:
