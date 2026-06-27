# Task Brief Compiler Contract

## Purpose

This document defines the safe documentation-only transition from an accepted
`Next Task Candidate` plus a valid selection decision to a `Task Brief` draft.

Flow:

```text
accepted Next Task Candidate
-> valid Selection Decision
-> Task Brief draft
-> HUMAN_REVIEW_REQUIRED
```

The compiler described here is a contract only. It may create a Task Brief
draft only.

## What The Compiler Does Not Do

The compiler must not authorize execution.

The compiler must not assign Risk Profile.

The compiler must not approve a task.

The compiler must not start a task.

The compiler must not commit.

The compiler must not push.

The compiler must not merge.

The compiler must not release.

The compiler is not a runner and does not create executable tasks.

## Required Preconditions

Before a Task Brief draft may be created, all of the following must be true:
- source candidate exists;
- source candidate remains `DRAFT`;
- selection decision exists;
- `selection_decision: ACCEPT`;
- selection artifact passes the selection validator;
- `execution_authorized` remains `false`;
- `task_brief_authorized` remains `false` unless a separate human checkpoint
  exists;
- `risk_profile_assigned_by_human` remains `false` unless a separate human
  checkpoint exists;
- `next_task_started` remains `false`.

If any precondition is missing, ambiguous, or unknown, stop with `BLOCKED`,
`UNKNOWN_BLOCKED`, or `HUMAN_REVIEW_REQUIRED`.

## Task Brief Draft Fields

Every compiler-produced Task Brief draft must preserve these fields:
- `task_brief_draft_status: DRAFT`
- `source_candidate:`
- `source_selection_decision:`
- `candidate_goal:`
- `scope:`
- `out_of_scope:`
- `allowed_files:`
- `forbidden_files:`
- `validation_plan:`
- `proposed_risk_profile:`
- `risk_profile_assigned_by_human: false`
- `execution_authorized: false`
- `commit_authorized: false`
- `push_authorized: false`
- `human_review_required: true`
- `final_status: HUMAN_REVIEW_REQUIRED`

## Safety Semantics

This contract must preserve these semantics:
- compiled draft is not executable until human review and explicit authorization;
- PASS is validation result only, not approval;
- Evidence is not approval;
- CI PASS is not approval;
- UNKNOWN is not OK;
- NOT_RUN is not PASS;
- Human approval cannot be simulated.

## Boundary To Execution

An accepted candidate plus a valid selection decision may justify drafting a
Task Brief, but that does not authorize the Task Brief for execution.

The draft remains review-only until a later human review and explicit
authorization step occurs under its own scoped task and checkpoint.

## Example Behavior

A Task Brief draft example must be review-only.

It must not claim approval.

It must not claim execution authorization.

It must not assign Risk Profile.

It must not authorize commit or push.

It must not start the next task.

It must end at `HUMAN_REVIEW_REQUIRED`.
