# Human Result Acceptance Loop

## Purpose
The Human Result Acceptance Loop ensures that the outcome of a completed task is explicitly accepted by a human owner before any further action or lifecycle mutation occurs. Task Quality PASS provides evidence, but it does not equate to human acceptance.

## Scope
This loop applies to all tasks that have finished execution and passed the Task Quality Gate. It defines the formal process of presenting the task result to a human and recording their explicit decision.

## Non-goals
- This loop does not replace the Task Quality Gate.
- This loop does not execute code.
- This loop does not perform semantic validation of the product itself; it validates the process boundary.

## Decision Flow
1. Task completes execution.
2. Task Quality Gate is executed and produces a status (e.g., PASS or PASS_WITH_WARNINGS).
3. The result package (Task Brief, Quality Result, Evidence) is presented to the human owner.
4. Human owner reviews the package and makes an explicit decision: `ACCEPT_RESULT`, `NEEDS_CHANGES`, or `REJECT_RESULT`.
5. The decision is recorded.
6. Only if accepted and authorized separately, the task may proceed to the next lifecycle stage (e.g., commit/push).

## Decision Semantics

### ACCEPT_RESULT
The human owner accepts the delivered outcome of the task as satisfying the Task Brief.
- `ACCEPT_RESULT` does **not** authorize commit.
- `ACCEPT_RESULT` does **not** authorize push.
- `ACCEPT_RESULT` does **not** start the next task.

### NEEDS_CHANGES
The human owner finds the result unsatisfactory or incomplete.
- `NEEDS_CHANGES` requires a follow-up task candidate to be created for remediation.
- The current task result is not accepted for closure as complete.

### REJECT_RESULT
The human owner fundamentally rejects the result.
- `REJECT_RESULT` requires an explicit rejection reason.
- The work may be discarded or re-architected.

## Relationship to Task Quality Gate
Task Quality Gate is an automated or semi-automated verification that rules were followed. Task Quality PASS is not human result acceptance. Task Quality provides the Evidence for the human to make a decision.

## Relationship to Task Registry / Queue
Task result acceptance updates the task state, allowing the Registry to mark it as ready for closure or requiring follow-up. 
- `human_result_acceptance_required`: true/false
- `human_result_acceptance_decision_path`: path/to/decision
- `human_result_acceptance_status`: NOT_REQUESTED, HUMAN_REVIEW_REQUIRED, ACCEPTED, NEEDS_CHANGES, REJECTED
- `follow_up_task_required`: true/false
- `follow_up_task_candidate_path`: path/to/candidate
- `next_task_started`: false

## Relationship to Commit/Push Authorization
Acceptance of a result is strictly separated from authorization to mutate the repository.
Acceptance merely means the task output is approved as a result. A separate `commit_authorized` or `push_authorized` checkpoint is required.

## Forbidden Automation
- Human result acceptance cannot be inferred.
- No auto-approval of task results.
- No auto task closure upon Task Quality PASS.
- No auto next-task start.
- No auto commit or push based on acceptance.
- Lifecycle mutation remains forbidden unless separately authorized.

## Human Review Boundary
The decision `ACCEPT_RESULT`, `NEEDS_CHANGES`, or `REJECT_RESULT` must be made by a human. The Agent may prepare the summary and the decision package, but the actual decision field and `result_accepted_by_human` flag must be set by human intervention.
