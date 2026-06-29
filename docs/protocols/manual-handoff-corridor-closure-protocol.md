# Manual Handoff Corridor Closure Protocol

## 1. Purpose
Defines how a task safely traverses the manual handoff corridor from scoped agent execution to human review without implicitly gaining approval, READY_FOR_EXECUTION, commit authorization, push authorization, or release authorization.

## 2. Scope
This protocol covers the behavior of AI Agents traversing the execution boundary where execution has been explicitly authorized but approval is withheld (`NOT_APPROVED`). It enforces that moving through readiness to handoff generation and result-review leaves the system correctly blocked pending human review.

## 3. Non-goals
- Does not introduce a runner.
- Does not introduce autonomous execution.
- Does not introduce approval simulation.
- Does not introduce automatic commit.
- Does not introduce automatic push.
- Does not introduce release authorization.
- Does not change validator behavior.
- Does not change lifecycle semantics.
- Does not change protected/canonical files.
- Does not change workflow files.

## 4. Required inputs
- Human decision specifying High/Protected risk profile with explicit `execution_authorized: true`.
- Target task file accurately reflecting human intent.
- Target branch with accurate HEAD and origin/dev sync state.

## 5. Required human decision fields
A valid manual handoff corridor requires a human decision containing:
- `execution_authorized: true`
- `commit_authorized: false`
- `push_authorized: false`
- `release_authorized: false`
- `required_final_state: READY_FOR_HUMAN_REVIEW`

## 6. Required task file fields
- `risk_profile`: Must accurately match human assignment (e.g., `HIGH_RISK_PROTECTED`).
- `risk_assigned_by`: `human`
- `approval_status`: `NOT_APPROVED`
- `execution_authorized`: `true`
- `commit_authorized`: `false`
- `push_authorized`: `false`
- `release_authorized`: `false`

## 7. Required Evidence fields
- `validator_status`: Only as required by schema. Not approval.
- `evidence_status`: Only as required by schema. Not approval.

## 8. Required handoff_result fields
After agent execution, the task file must be appended with:
- `result_status`
- `agent_claimed_status`
- `reported_changed_files`
- `validation_results` (including evidence of execution constraints)
- `stop_condition`
- `authorization_claims` (must report false for approval, execution readiness, commit, push, and release).

## 9. Required validation commands
Agents must perform baseline integrity checks:
- `python3 -m py_compile aos/scripts/aos_task_document_check.py`
- `python3 aos/scripts/aos_task_document_check.py task --validate-all`
- `python3 aos/scripts/aos_task_document_check.py task --readiness <task_file>`
- `python3 aos/scripts/aos_task_document_check.py task --handoff-prompt <task_file>`
- `python3 aos/scripts/aos_task_document_check.py task --result-review <task_file>`
- `python3 aos/scripts/aos_task_document_check.py registry --check`
- `python3 aos/scripts/aos_task_document_check.py queue --list`

## 10. Required result-review behavior
A task must achieve `RESULT_REVIEW_PASS` to leave the execution phase safely, demonstrating all requested validations successfully ran. `RESULT_REVIEW_PASS` acts strictly as an evidence formatting and structural integrity validation.

## 11. Human review boundary
Once `RESULT_REVIEW_PASS` is achieved, the task is structurally complete for execution but must transition to `READY_FOR_HUMAN_REVIEW`. It cannot self-assign `READY_FOR_EXECUTION` or `APPROVED`.

## 12. Commit authorization boundary
Commit requires an explicit, separate human authorization.

## 13. Push authorization boundary
Push requires an explicit, separate human authorization.

## 14. Release authorization boundary
Release requires an explicit, separate human authorization.

## 15. Stop conditions
Agents must stop execution and await human instructions if:
- Validation outputs `HUMAN_REVIEW_REQUIRED`, `BLOCKED`, or `UNKNOWN_BLOCKED`.
- Scope threatens to expand into unauthorized files.
- Task execution results are fully documented and prepared for review.

## 16. Forbidden claims
Agents must not simulate human action or manipulate metadata to claim safety clearance they have not received.

## 17. Protected/canonical boundary
Protected/canonical changes require explicit human checkpoint. No changes are permitted during the handoff corridor unless the target file is explicitly permitted by scope. Destructive operations are forbidden by default.

## 18. UNKNOWN / NOT_RUN / PASS semantics
- PASS is not approval.
- CI PASS is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.

## 19. READY_FOR_HANDOFF semantics
- READY_FOR_HANDOFF is not approval.
- READY_FOR_HANDOFF is not READY_FOR_EXECUTION.
- Handoff prompt is not approval.
- Handoff result is not approval.

## 20. RESULT_REVIEW_PASS semantics
- RESULT_REVIEW_PASS is not approval.
- RESULT_REVIEW_PASS is not READY_FOR_EXECUTION.
- RESULT_REVIEW_PASS is not commit authorization.
- RESULT_REVIEW_PASS is not push authorization.

## 21. Final allowed states
The task must end in either:
- `READY_FOR_HUMAN_REVIEW`
- `BLOCKED` (or `HUMAN_REVIEW_REQUIRED`)
Human unavailable for required review/checkpoint/approval means BLOCKED or HUMAN_REVIEW_REQUIRED.

## 22. Minimal checklist for future agents
- [ ] Read human instructions. Verify `execution_authorized: true` and `approval_status: NOT_APPROVED`.
- [ ] Run `git fetch` and `git status`. Verify clean boundary.
- [ ] Run `--readiness`.
- [ ] Extract `--handoff-prompt` scope instructions.
- [ ] Execute target work.
- [ ] Populate `handoff_result`.
- [ ] Run `--result-review`.
- [ ] Verify `RESULT_REVIEW_PASS`.
- [ ] Explicitly refuse to commit/push. Stop execution.

## Invariants
* PASS is not approval.
* Evidence is not approval.
* CI PASS is not approval.
* UNKNOWN is not OK.
* NOT_RUN is not PASS.
* Human approval cannot be simulated.
* READY_FOR_HANDOFF is not approval.
* READY_FOR_HANDOFF is not READY_FOR_EXECUTION.
* Handoff prompt is not approval.
* Handoff result is not approval.
* RESULT_REVIEW_PASS is not approval.
* RESULT_REVIEW_PASS is not READY_FOR_EXECUTION.
* RESULT_REVIEW_PASS is not commit authorization.
* RESULT_REVIEW_PASS is not push authorization.
* Commit authorization is separate from push authorization.
* Push authorization is separate from release authorization.
* Human unavailable for required review/checkpoint/approval means BLOCKED or HUMAN_REVIEW_REQUIRED.
* Scope must not expand without explicit human permission.
* Protected/canonical changes require human checkpoint.
* Destructive operations are forbidden by default.
