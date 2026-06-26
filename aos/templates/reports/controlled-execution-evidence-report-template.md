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
