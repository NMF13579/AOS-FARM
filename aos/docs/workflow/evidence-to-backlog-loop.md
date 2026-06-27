# Evidence-to-Backlog Loop

## Purpose
The Evidence-to-Backlog Loop captures what was learned after a controlled task
has finished and turns that learning into reviewable follow-up material.

Flow:

```text
Evidence Review
-> Lessons Learned
-> Pipeline Hardening Backlog
-> Next Task Candidate
-> Human Review
```

This loop is a learning and framing step. It does not approve work, start work,
authorize execution, authorize commit, authorize push, authorize merge,
authorize release, or assign a Risk Profile.

## When This Loop Runs
Run this loop only after controlled execution has produced the available
post-execution evidence for one completed task.

Typical inputs may include:
- Evidence Report;
- Execution Report;
- Controlled Execution Guard results;
- `scopecheck` results if present;
- `postcheck` results if present;
- commit closure evidence if present;
- push closure evidence if present.

Missing optional evidence must be recorded as `NOT_RUN` or `UNKNOWN`, not
treated as `PASS`.

## Output Artifacts
The loop may produce reviewable artifacts with these roles:
- Post-Execution Review: records the evidence read and the review boundary.
- Lessons Learned: records what the completed task revealed.
- Pipeline Hardening Backlog Item: records a possible future improvement.
- Next Task Candidate: frames one possible follow-up task for human review.

These artifacts are not approval artifacts. They are not execution
authorization. They do not mutate lifecycle state by themselves.

## Lifecycle Boundary
The loop ends at `HUMAN_REVIEW_REQUIRED` unless a human explicitly authorizes
the next lifecycle transition.

The loop must not:
- start the next task;
- move a task into execution;
- mark a backlog item as authorized;
- convert a candidate into an approved task;
- treat readiness as approval;
- claim lifecycle completion as human acceptance.

## Human Review Boundary
Human review is required before any follow-up work can begin. If the human is
unavailable for a required decision, stop with `BLOCKED` or
`HUMAN_REVIEW_REQUIRED`.

Human review of this loop may decide to:
- request clarification;
- reject a lesson, backlog item, or candidate;
- ask for a new Task Brief;
- authorize a separate later checkpoint.

The loop itself cannot make any of those decisions on behalf of the human.

## Approval Boundary
The loop must state and preserve these boundaries:
- Evidence Review != approval.
- Lessons Learned != approval.
- Pipeline Hardening Backlog Item != execution authorization.
- Next Task Candidate != approved task.
- Validator PASS != approval.
- PASS != approval.
- Evidence != approval.
- CI PASS != approval.
- UNKNOWN != OK.
- NOT_RUN != PASS.
- Human approval cannot be simulated.
- Human unavailable for required decision -> `BLOCKED` or
  `HUMAN_REVIEW_REQUIRED`.

## Risk Profile Boundary
The loop may record the Risk Profile that was human-assigned for the completed
task being reviewed. It must not assign or downgrade a Risk Profile for a new
task.

If a Next Task Candidate is created, its Risk Profile is missing until a human
assigns one in a separate checkpoint or an approved deterministic classifier
does so under its own approved rules.

The agent must not self-assign `LOW_RISK_FAST`.

## Relation To Controlled Task Brief
The Controlled Task Brief remains the scope source for the completed task. This
loop may compare evidence against that brief, but it must not modify the brief
or expand its scope.

A Next Task Candidate produced by this loop is only candidate material. It is
not a Controlled Task Brief and cannot authorize execution.

## Relation To Execution Package
The Execution Package records the exact authorized execution boundary for the
completed task. This loop may cite package fields such as allowed files,
forbidden files, guard requirements, and expected evidence.

The loop must not edit an execution package or treat a package as authorization
for any new task.

## Relation To Evidence Report
The Evidence Report is an input to this loop. Evidence may include command
logs, validation output, test output, changed file lists, not-run lists,
unknowns, blockers, and closure evidence.

Evidence is not approval. Evidence Review is not approval. A clean evidence
review can support a human decision, but it cannot replace that decision.

## Relation To Future Validator Or Helper
A future validator or helper may check this loop for required fields,
forbidden claims, `UNKNOWN`/`OK` conflicts, `NOT_RUN`/`PASS` conflicts, and
approval-boundary violations.

That future validator or helper is not implemented by this document. Validator
PASS would still not approve work, authorize execution, authorize commit,
authorize push, authorize merge, authorize release, or assign a Risk Profile.

## Relation To Commit And Push Gates
Commit and push gates remain separate human-authorized steps.

This loop may read commit or push closure evidence if it exists, but it must
not create commit authorization, push authorization, merge authorization, or
release authorization.

Evidence Review, Lessons Learned, Pipeline Hardening Backlog Items, Next Task
Candidates, validator output, and closure evidence do not authorize commit or
push.

## Allowed Statuses
This loop may end with one of these statuses:
- `DRAFT`
- `READY_FOR_HUMAN_REVIEW`
- `HUMAN_REVIEW_REQUIRED`
- `BLOCKED`
- `UNKNOWN_BLOCKED`
- `REJECTED`

The normal Task 1 boundary is `HUMAN_REVIEW_REQUIRED`.

## Forbidden Status Output
This loop must not output:
- `APPROVED`

Only a human can approve a final result, protected/canonical change,
destructive operation, release, merge, lifecycle transition, scope expansion,
or next-stage transition.

## Allowed Actions
Within an explicitly scoped task, the loop may:
- read completed task evidence;
- summarize lessons learned;
- identify backlog candidates;
- draft a Next Task Candidate for human review;
- list `UNKNOWN`, `NOT_RUN`, and blockers;
- request human review.

## Forbidden Actions
The loop must not:
- approve work;
- simulate human approval;
- authorize execution;
- start the next task;
- auto-plan implementation;
- assign a Risk Profile;
- authorize commit;
- authorize push;
- authorize merge;
- authorize release;
- modify protected/canonical sources without checkpoint;
- hide `UNKNOWN`;
- treat `NOT_RUN` as `PASS`;
- treat validator output as approval.

## Stopping Condition
Stop with `BLOCKED`, `UNKNOWN_BLOCKED`, or `HUMAN_REVIEW_REQUIRED` if:
- required evidence is missing;
- a required status is unknown;
- the next action would require human approval;
- a Risk Profile decision is needed;
- scope expansion is needed;
- a protected/canonical change is needed;
- commit, push, merge, release, or production use is requested;
- a backlog item or candidate is being treated as authorized work.

## Final Boundary
The Evidence-to-Backlog Loop ends at human review. It does not start Task 2,
create templates, create examples, create fixtures, create validators, create
tests, create dogfood artifacts, commit, push, merge, tag, or release.
