# Manual Handoff Corridor Consumer Path

## 1. Purpose
This document explains the full manual handoff corridor for users of the AOS-FARM target project. It provides a safe workflow for delegating scoped work to an AI agent while keeping full control and authorization in the hands of the human owner.

## 2. Who this guide is for
This guide is for end users and owners of the repository who want to safely assign tasks to AI agents without allowing autonomous code execution, commit, push, or release.

## 3. What the corridor does
The manual handoff corridor enforces a strict boundary between what the agent does (scoped execution) and what the human owner does (authorization and approval).

1. User creates or selects task file.
2. Validator checks readiness.
3. If READY_FOR_HANDOFF → user gives handoff prompt to agent.
4. Agent performs only scoped work.
5. Agent writes handoff_result.
6. Validator checks result-review.
7. If RESULT_REVIEW_PASS → human reviews result.
8. Human may authorize commit.
9. Human may separately authorize push.
10. Release remains separate.

## 4. What the corridor does not do
The corridor does not simulate human approval. It does not automatically execute changes. It does not allow agents to bypass required checkpoints.

## 5. Required files
Task files and agent reports. Root files (00, 01, 02) are AOS-FARM development canonical sources and are not runtime prerequisites for the target project.

## 6. Step 1 — Create or receive a task file
Create a task file. The task must explicitly assign a Risk Profile.

## 7. Step 2 — Check readiness
Run the readiness validator against the task file.
READY_FOR_HANDOFF means the task can be handed to an agent for scoped work.
READY_FOR_HANDOFF is not approval.
READY_FOR_HANDOFF is not READY_FOR_EXECUTION.
READY_FOR_HANDOFF is not commit authorization.
READY_FOR_HANDOFF is not push authorization.
READY_FOR_HANDOFF is not release authorization.

## 8. Step 3 — Generate handoff prompt
Handoff prompt is an instruction package for an agent.
It does not approve the task.
It does not authorize lifecycle mutation.
It does not authorize commit.
It does not authorize push.
It does not authorize release.

## 9. Step 4 — Give scoped work to an agent
Provide the handoff prompt to the agent. The agent must perform only the scoped work defined in the task.

## 10. Step 5 — Receive handoff_result
handoff_result is the agent's structured report of what it did.
It is not approval.
It is not READY_FOR_EXECUTION.
It is not commit authorization.
It is not push authorization.
It is not release authorization.

## 11. Step 6 — Run result-review
Run the result-review validator.
RESULT_REVIEW_PASS means the reported result is structurally reviewable.
It is not approval.
It is not READY_FOR_EXECUTION.
It is not commit authorization.
It is not push authorization.
It is not release authorization.

## 12. Step 7 — Human review
Human review is required before commit/push decisions.
Human approval cannot be simulated by an agent.
Human approval cannot be inferred from PASS, Evidence, readiness, result-review, or CI.

## 13. Step 8 — Commit decision
Commit authorization is separate from push authorization.
Commit does not mean push.

## 14. Step 9 — Push decision
Push authorization is separate from release authorization.
Push does not mean release.

## 15. What each status means
Statuses like PASS or Evidence only describe the state of structural checks.

## 16. What each status does not mean
They do not substitute human approval.
CI PASS is not approval.

## 17. Common mistakes
- Mistake: Treating PASS as approval.
  Correct: PASS only means a check passed.
- Mistake: Treating Evidence as approval.
  Correct: Evidence supports review but does not approve anything.
- Mistake: Treating READY_FOR_HANDOFF as READY_FOR_EXECUTION.
  Correct: READY_FOR_HANDOFF only allows scoped handoff.
- Mistake: Treating RESULT_REVIEW_PASS as approval.
  Correct: RESULT_REVIEW_PASS only means the result is structurally reviewable.
- Mistake: Letting the agent decide Risk Profile.
  Correct: agent may propose Risk Profile, but human assigns it.
- Mistake: Combining commit and push.
  Correct: commit and push require separate human decisions.
- Mistake: Treating push as release.
  Correct: release requires separate human decision.
- Mistake: Letting agent continue after UNKNOWN.
  Correct: UNKNOWN is not OK; stop or request human review.

## 18. Safe stop conditions
Agents must safely stop when tasks are blocked, require human review, or finish scoped execution without lifecycle mutation authority.

## 19. Minimal user checklist
Before giving work to an agent:
- [ ] Task file exists.
- [ ] Risk Profile is assigned by human.
- [ ] execution_authorized is explicit and scoped.
- [ ] commit_authorized is false unless human explicitly allowed commit.
- [ ] push_authorized is false unless human explicitly allowed push.
- [ ] release_authorized is false.
- [ ] readiness check returns READY_FOR_HANDOFF.
- [ ] handoff prompt does not claim approval.
- [ ] handoff prompt does not authorize commit.
- [ ] handoff prompt does not authorize push.
- [ ] handoff prompt does not authorize release.

After agent work:
- [ ] handoff_result exists.
- [ ] changed files are listed.
- [ ] validation Evidence is recorded in the report.
- [ ] result-review returns RESULT_REVIEW_PASS.
- [ ] no forbidden files changed.
- [ ] no protected/canonical files changed without checkpoint.
- [ ] validator was not changed.
- [ ] workflows were not changed.
- [ ] no approval was claimed.
- [ ] no READY_FOR_EXECUTION was claimed.
- [ ] no commit happened without separate human decision.
- [ ] no push happened without separate human decision.
- [ ] no release happened without separate human decision.

## 20. Example user flow
This provides a standard template for how users should orchestrate the manual handoff and verification cycle.
