# First Controlled Execution

## Purpose
This guide explains the first safe path from a finished `Controlled Task Brief` to `Human Execution Authorization`, then to Controlled Execution Guard `precheck`, then to `Controlled Execution`, then to `scopecheck`, `postcheck`, and `Evidence Review`.

It is written for a non-programmer or vibe-coder user.

## When To Use
Use this guide only after all of the following are true:
- You already selected one task from the manual task queue.
- You already created a `Controlled Task Brief` for that task.
- You are ready to decide whether the agent may execute that exact task.

Do not use this guide to:
- create a new task from scratch;
- approve future tasks;
- authorize commit or push;
- skip Human Execution Authorization.

## What You Need First
Before starting this step, you need:
- one selected queue item;
- one completed `Controlled Task Brief`;
- a human who can assign the Risk Profile;
- a human who can explicitly authorize or reject execution.

If any of these are missing, stop with `BLOCKED`.

## What Is Still Not Authorized
At this stage:
- `Controlled Task Brief` is not approval.
- readiness is not approval.
- `PASS` is not approval.
- `Evidence` is not approval.
- commit is not authorized.
- push is not authorized.

## Step-By-Step Flow

### Step 1: Pick Exactly One Task
Choose one task from the queue that is ready for execution authorization.

Current step:
- Queue selection

Required input:
- the queue item
- the linked `Controlled Task Brief`

Expected output:
- one exact task to review

Stop with `BLOCKED` if:
- multiple tasks are being mixed together;
- the task is still only a draft;
- the queue item does not match the brief.

### Step 2: Open The Controlled Task Brief
Read the full brief before authorizing anything.

Check:
- the exact goal;
- allowed changes;
- forbidden changes;
- validation plan;
- expected output;
- unknown or blocked handling.

Current step:
- Brief review

Required input:
- completed `Controlled Task Brief`

Expected output:
- clear understanding of what the agent may and may not do

Stop with `BLOCKED` if:
- allowed scope is missing;
- forbidden scope is missing;
- the brief is ambiguous;
- the brief asks for commit, push, release, production use, or unrelated cleanup.

### Step 3: Human Assigns The Risk Profile
The agent may suggest a Risk Profile, but the human must assign it.

Important:
- `LOW_RISK_FAST` cannot be self-assigned by the agent.
- missing Risk Profile assignment means execution is blocked.

Current step:
- Risk decision

Required input:
- reviewed brief
- human decision

Expected output:
- one explicit human-assigned Risk Profile

### Step 4: Create Human Execution Authorization
Create a separate Human Execution Authorization artifact for this exact task.

Copy this:

```text
I assign Risk Profile: <RISK_PROFILE>.
I authorize Controlled Execution for this exact Controlled Task Brief only:
<brief_id / file path>
Allowed scope:
<exact scope>
Forbidden:
commit, push, merge, release, production use, destructive operations,
protected/canonical changes unless explicitly listed,
runner/runtime/CI/DB/RAG/vector/SQLite/Spec Kit unless explicitly listed.
Human approval applies only to this execution task.
It does not authorize future tasks.
```

Current step:
- Human authorization

Required input:
- reviewed brief
- human-assigned Risk Profile

Expected output:
- explicit go/no-go authorization for one exact execution task

Stop with `BLOCKED` if:
- there is no human authorization;
- the authorization does not match the brief;
- the Risk Profile is not assigned by a human.

### Step 5: Give The Agent The Controlled Execution Prompt
Use the copy-ready prompt in `aos/prompts/controlled-execution.md`.

You should provide the agent with:
- the completed `Controlled Task Brief`;
- the Human Execution Authorization;
- any exact file paths or evidence expectations listed in the brief.

Current step:
- Agent handoff

Required input:
- brief
- human authorization
- Risk Profile

Expected output:
- an execution attempt that either runs safely or stops with `BLOCKED`

Copy this:

```text
Execute only the authorized Controlled Task Brief.
Before editing files:
- verify required sources;
- verify human execution authorization;
- verify branch and repo state;
- verify human-assigned Risk Profile;
- verify allowed and forbidden scope.
If anything is missing, ambiguous, UNKNOWN, NOT_RUN, or outside scope, stop with BLOCKED.
Do not commit.
Do not push.
Return an Execution Report with Evidence.
```

### Step 6: Run Controlled Execution Guard Precheck
Before execution starts, run the guard against the execution package or equivalent artifact set.

Example:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos precheck --package <package.yaml>
```

For a filled valid package example, see `aos/reports/examples/README.md`.

Current step:
- Guard precheck

Expected output:
- `PASS`, `BLOCKED`, `UNKNOWN_BLOCKED`, or `HUMAN_REVIEW_REQUIRED`

Important:
- Guard PASS is not approval.
- Guard PASS does not authorize commit.
- Guard PASS does not authorize push.

Stop if:
- precheck returns `BLOCKED`;
- precheck returns `UNKNOWN_BLOCKED`;
- precheck returns `HUMAN_REVIEW_REQUIRED`.

### Step 7: Agent Performs Controlled Execution
Before editing files, the agent must verify:
- the completed `Controlled Task Brief` is present;
- Human Execution Authorization exists for that exact brief;
- the human-assigned Risk Profile is present;
- any package, report, or evidence paths named in the brief are present or clearly expected;
- the current branch and repository state are safe enough for the task;
- allowed and forbidden scope are explicit;
- nothing requires scope expansion.

The agent must not:
- approve anything as human;
- commit;
- push;
- expand scope;
- treat `UNKNOWN` as acceptable;
- treat `NOT_RUN` as `PASS`.

Current step:
- Controlled execution

Expected output:
- one `Execution Report`
- collected Evidence

### Step 8: Run Controlled Execution Guard Scopecheck
After execution and before Evidence Review, verify the changed-file boundary.

Example:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos scopecheck --package <package.yaml> --changed-files <changed-files-list>
```

Important:
- `BLOCKED` means stop.
- `UNKNOWN_BLOCKED` means stop and ask for human/project-owner review.
- `HUMAN_REVIEW_REQUIRED` means a required human checkpoint or boundary decision is missing or incomplete.

### Step 9: Create The Execution Report
Create the `Execution Report` before final evidence review.

Use:
- `aos/templates/reports/execution-report-template.md`

The report should reflect:
- what files changed;
- what validations ran;
- PASS / NOT_RUN / UNKNOWN separation;
- whether scope stayed inside authorization.

### Step 10: Run Controlled Execution Guard Postcheck
Before finalizing Evidence Review, verify the evidence/report boundary.

Example:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package <package.yaml> --report <evidence-report.md>
```

Important:
- Guard PASS is not approval.
- Guard PASS does not authorize commit.
- Guard PASS does not authorize push.
- `BLOCKED` means stop.
- `UNKNOWN_BLOCKED` means stop and ask for human/project-owner review.
- `HUMAN_REVIEW_REQUIRED` means a required human checkpoint or boundary decision is missing or incomplete.

### Step 11: Review The Execution Report And Evidence
After execution, review what the agent claims it changed and what Evidence it provides.

Use:
- `aos/templates/reports/evidence-review-template.md`
- `aos/templates/reports/verification-report-template.md`

Check:
- what files changed;
- what validations ran;
- what did not run;
- whether scope stayed inside authorization;
- whether any unresolved questions remain.

Current step:
- Evidence Review

Expected output:
- explicit human review result

Important:
- Evidence Review is not commit approval.
- Evidence Review is not push approval.
- Guard PASS is not commit approval.
- Guard PASS is not push approval.

### Step 12: Separate Commit And Push Decisions
Only after human review of the Evidence:
- prepare commit authorization;
- after commit and post-commit verification, prepare push authorization.

These are separate decisions.

`Execution Authorization` does not authorize:
- commit;
- push;
- merge;
- release.

### Step 13: Capture Post-Execution Learning
After Evidence Review and any available closure evidence, use the
Evidence-to-Backlog Loop to record lessons learned, possible hardening backlog
items, and a Next Task Candidate for human review.

Use:
- `aos/docs/workflow/evidence-to-backlog-loop.md`

Important:
- Evidence Review is not approval.
- Lessons Learned are not approval.
- Pipeline Hardening Backlog Items are not execution authorization.
- Next Task Candidates are not approved tasks.
- Validator PASS is not approval.
- The loop does not authorize commit, push, merge, release, or the next task.

## User Checklist Before Execution
- [ ] I selected exactly one queue item.
- [ ] I reviewed the full `Controlled Task Brief`.
- [ ] Allowed and forbidden scope are explicit.
- [ ] A human assigned the Risk Profile.
- [ ] A human created explicit execution authorization.
- [ ] I ran Controlled Execution Guard `precheck`.
- [ ] I am using the controlled execution prompt.
- [ ] I understand that commit and push are still not authorized.

## Human Execution Authorization Boundary
Human Execution Authorization:
- applies to one exact brief only;
- applies to one exact scope only;
- does not authorize future tasks;
- does not authorize commit or push;
- must stop if the task becomes ambiguous.

## Evidence Review Boundary
Evidence Review should answer:
- Did the agent stay inside the authorized scope?
- What validations passed?
- What validations were `NOT_RUN`?
- What remains `UNKNOWN`?
- Are there unresolved questions?
- Did `scopecheck` stay inside authorized changed-file boundaries?
- Did `postcheck` confirm the Evidence boundary disclosures?

Evidence Review must say clearly:
- `PASS` is not approval.
- Evidence is not commit approval.
- the next step is commit authorization only if the human approves.
- Guard PASS is not approval.

## Status Handling

| Status | Meaning | Required action |
|---|---|---|
| PASS | The guard check passed. | Continue only to the next already-authorized step. PASS is not approval. |
| BLOCKED | A boundary violation, forbidden claim, missing artifact, or unsafe state was detected. | Stop. Fix the input/scope or request human/project-owner review. |
| UNKNOWN_BLOCKED | The state cannot be safely classified. | Stop. Human/project-owner review is required. UNKNOWN is not OK. |
| HUMAN_REVIEW_REQUIRED | A required human checkpoint, Risk Profile assignment, or authorization is missing/incomplete. | Stop. Obtain a real human decision. Human approval cannot be simulated. |
| NOT_RUN | A check did not run. | Do not treat as PASS. Run it or record honestly as NOT_RUN. |

Guard PASS does not authorize commit.
Guard PASS does not authorize push.
Evidence does not authorize commit.
CI PASS does not authorize push.
Commit requires a separate human commit authorization.
Push requires a separate human push authorization.

## BLOCKED Conditions
Stop with `BLOCKED` if:
- the brief is missing or ambiguous;
- Human Execution Authorization is missing;
- Risk Profile assignment is missing;
- guard `precheck`, `scopecheck`, or `postcheck` returns `BLOCKED`;
- guard `precheck`, `scopecheck`, or `postcheck` returns `UNKNOWN_BLOCKED`;
- guard `precheck`, `scopecheck`, or `postcheck` returns `HUMAN_REVIEW_REQUIRED`;
- scope is unclear;
- the task requires extra files not in scope;
- validation status is missing and cannot be clarified;
- the agent asks to commit or push during execution.

## Non-Goals
This guide does not:
- automate execution;
- replace human review;
- authorize future tasks;
- authorize post-execution backlog work;
- authorize commit or push;
- change lifecycle taxonomy;
- enable runner, CI, database, RAG, vector DB, or Spec Kit execution.
