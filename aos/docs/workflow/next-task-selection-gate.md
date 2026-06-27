# Next Task Selection Gate

## Purpose

This workflow defines the human decision gate that runs after a `Next Task
Candidate` has been drafted.

Flow:

```text
Next Task Candidate
-> Human Selection Gate
-> Selection Decision Artifact
-> HUMAN_REVIEW_REQUIRED
```

This gate formalizes the human decision step before any Task Brief draft
preparation may begin.

## What This Gate Does Not Do

This gate does not approve a task.

This gate does not assign Risk Profile.

This gate does not authorize execution.

This gate does not authorize commit or push.

This gate does not start the next task.

This gate is not a runner and does not create executable tasks.

## Required Boundary Fields

Every selection artifact must preserve these fields:
- `candidate_status: DRAFT`
- `selection_decision:`
- `execution_authorized: false`
- `task_brief_authorized: false`
- `risk_profile_assigned_by_human: false`
- `next_task_started: false`
- `human_review_required: true`
- `final_status: HUMAN_REVIEW_REQUIRED`

## Decision Options

### ACCEPT

`ACCEPT` means the candidate is accepted for Task Brief draft preparation only.

`ACCEPT` does not mean the task is approved.

`ACCEPT` does not assign Risk Profile.

`ACCEPT` does not authorize execution.

`ACCEPT` does not authorize commit.

`ACCEPT` does not authorize push.

`ACCEPT` does not start the next task.

### CLARIFY

`CLARIFY` means more human or user clarification is required before the
candidate can move forward.

### DEFER

`DEFER` means the candidate is postponed and should not move forward now.

### REJECT

`REJECT` means the candidate is rejected and must not be compiled into a Task
Brief draft.

### REPLACE

`REPLACE` means the human wants a different candidate instead of the current
one.

## Safety Semantics

This gate must preserve these semantics:
- PASS is not approval.
- Evidence is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Human approval cannot be simulated.

## Boundary To Task Brief Work

This gate may point to Task Brief draft preparation as a later possible step,
but it does not authorize that step by itself.

If a Task Brief draft is needed after selection, that later work must be
opened as its own scoped task.

## Stopping Rule

Stop with `HUMAN_REVIEW_REQUIRED`, `BLOCKED`, or `UNKNOWN_BLOCKED` if:
- the candidate is missing;
- the decision is ambiguous;
- the artifact implies execution, commit, push, or approval;
- Risk Profile assignment is being inferred;
- the next task is being treated as already started.
