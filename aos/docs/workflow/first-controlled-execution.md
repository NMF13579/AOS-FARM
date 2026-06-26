# First Controlled Execution

## Purpose
This guide explains the first safe path from a finished `Controlled Task Brief` to `Human Execution Authorization`, then to `Controlled Execution`, then to `Evidence Review`.

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

### Step 6: Agent Performs Controlled Execution
Before editing files, the agent must verify:
- required sources are readable;
- the current branch and repository state are safe enough for the task;
- Human Execution Authorization exists;
- the Risk Profile was assigned by a human;
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

### Step 7: Review The Execution Report And Evidence
After execution, review what the agent claims it changed and what Evidence it provides.

Use:
- `aos/templates/reports/execution-report-template.md`
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

### Step 8: Separate Commit And Push Decisions
Only after human review of the Evidence:
- prepare commit authorization;
- later, after commit, prepare push authorization.

These are separate decisions.

`Execution Authorization` does not authorize:
- commit;
- push;
- merge;
- release.

## User Checklist Before Execution
- [ ] I selected exactly one queue item.
- [ ] I reviewed the full `Controlled Task Brief`.
- [ ] Allowed and forbidden scope are explicit.
- [ ] A human assigned the Risk Profile.
- [ ] A human created explicit execution authorization.
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

Evidence Review must say clearly:
- `PASS` is not approval.
- Evidence is not commit approval.
- the next step is commit authorization only if the human approves.

## BLOCKED Conditions
Stop with `BLOCKED` if:
- required sources are missing;
- the brief is missing or ambiguous;
- Human Execution Authorization is missing;
- Risk Profile assignment is missing;
- scope is unclear;
- the task requires extra files not in scope;
- validation status is missing and cannot be clarified;
- the agent asks to commit or push during execution.

## Non-Goals
This guide does not:
- automate execution;
- replace human review;
- authorize future tasks;
- authorize commit or push;
- change lifecycle taxonomy;
- enable runner, CI, database, RAG, vector DB, or Spec Kit execution.
