# AOS-FARM.434 — First Controlled Execution User-Facing Bridge MVP

task_id: AOS-FARM.434
task_name: First Controlled Execution User-Facing Bridge MVP
mode: implementation_mvp
risk_profile: MEDIUM_RISK_GUIDED
branch: build/first-controlled-execution-bridge-mvp
head_before: 34087dccbbe035cb8bbc6b3289a0d29b8744a7a8
origin_dev: 34087dccbbe035cb8bbc6b3289a0d29b8744a7a8
ahead_behind_before: 0 0
final_status: AOS_FARM_434_FIRST_CONTROLLED_EXECUTION_BRIDGE_MVP_READY_FOR_REVIEW

## 1. Scope
This task creates the minimal user-facing bridge from `Controlled Task Brief` to `Human Execution Authorization`, then to `Controlled Execution`, then to `Evidence Review`.

## 2. Non-goals
- No runner
- No automation
- No SQLite
- No RAG-light
- No vector DB
- No CI workflows
- No Spec Kit execution
- No commit/push/release
- No lifecycle taxonomy changes
- No unrelated dirty worktree cleanup

## 3. Required Sources Verification
- `00_AOS_Core_Control.md`: present and read
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`: present and read
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`: present and read

## 4. Repository Baseline
- Baseline branch for implementation: `build/first-controlled-execution-bridge-mvp`
- `HEAD before changes`: `34087dccbbe035cb8bbc6b3289a0d29b8744a7a8`
- `origin/dev`: `34087dccbbe035cb8bbc6b3289a0d29b8744a7a8`
- `ahead/behind before`: `0 0`
- Pre-existing unrelated `D` and `??` worktree paths were observed and kept out of scope.
- Pre-existing local AOS-FARM.433 push-authorization artifacts were treated as out of scope and not used as Source of Truth.

## 5. Implemented Files
- `aos/docs/workflow/first-controlled-execution.md`
- `aos/prompts/controlled-execution.md`
- `aos/templates/reports/evidence-review-template.md`
- `reports/aos-farm-434-first-controlled-execution-bridge-mvp.md`

## 6. Modified Files
- `aos/START_HERE.md`
- `aos/docs/workflow/first-session-guide.md`
- `aos/docs/workflow/controlled-task-workflow.md`
- `aos/docs/workflow/consumer-runtime-handoff.md`
- `aos/templates/task-briefs/controlled-task-brief-template.md`
- `aos/templates/checkpoints/human-execution-authorization-template.md`
- `aos/templates/reports/execution-report-template.md`
- `aos/templates/reports/verification-report-template.md`
- `aos/templates/verification/post-execution-verification-template.md`
- `aos/templates/checkpoints/human-push-authorization-template.md`
- `aos/templates/authorization/execution-authorization-package-template.md`

## 7. Deferred Items
- No runner or automation work was implemented.
- No commit/push/release flow changes were implemented.
- No broader policy rewrite was attempted beyond the narrow branch-neutral push template wording fix.
- Pre-existing local AOS-FARM.433 push-authorization artifacts remained untouched and out of scope.

## 8. Safety Invariant Preservation
The implementation visibly preserves:
- `PASS != approval`
- `Evidence != approval`
- `CI PASS != approval`
- `UNKNOWN != OK`
- `NOT_RUN != PASS`
- Human approval cannot be simulated
- Scope must not expand without explicit human permission
- Controlled Task Brief != execution approval
- Human Execution Authorization is required before execution
- Commit authorization remains separate
- Push authorization remains separate
- Agent may propose Risk Profile but cannot assign it
- `LOW_RISK_FAST` cannot be self-assigned by the agent

## 9. User Path After Remediation
1. Pick one queue task.
2. Open the `Controlled Task Brief`.
3. Review scope and boundaries.
4. Human assigns Risk Profile.
5. Human creates execution authorization.
6. User copies the controlled execution prompt.
7. Agent verifies sources, authorization, Risk Profile, branch/repo state, and scope.
8. Agent executes only the authorized task.
9. Agent returns `Execution Report` with Evidence.
10. Human performs Evidence Review.
11. Commit authorization is prepared separately.
12. Push authorization is prepared separately.

## 10. Validation Results
- `git diff --check`: PASS
- Existing repo Markdown validation command: NOT_RUN
- Reason if NOT_RUN remains: no documented safe markdown validation command was found in the inspected repository entrypoints and workflow docs

## 11. Known Limitations
- The repository still contains unrelated pre-existing dirty worktree paths.
- This MVP improves the first user-facing bridge, but it does not automate safety checks.
- Commit and push authorization artifacts remain separate future steps.

## 12. Commit Readiness
Implementation is ready for human review, but not committed.

## 13. Next Safe Step
Human reviews the diff and, if accepted, prepares separate Human Commit Authorization for AOS-FARM.434.
