# AOS-FARM.440.2 Templates + Examples Report

## Status
task_id: AOS-FARM.440.2
task_name: Templates + Examples
risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by: human
branch: build/evidence-to-backlog-loop-mvp
baseline_sha: d612284028fea7984f3d8833a2b2b427c47e8d99
origin_dev_sha: d612284028fea7984f3d8833a2b2b427c47e8d99
ahead_behind: 0 0
target_path_collision_result: PASS
commit_performed: false
push_performed: false
merge_performed: false
release_performed: false
next_task_started: false
human_review_required: true
final_status: HUMAN_REVIEW_REQUIRED

## Scope
AOS-FARM.440 Task 2 only:
- AOS-FARM.440.3 Templates for Review / Lessons / Backlog / Next Task Candidate.
- AOS-FARM.440.5 Examples and Dogfood Fixtures.

Task 3 validator/helper code, tests, and dogfood artifacts were not created.

## Dirty Worktree Boundary
The local worktree was dirty before Task 2. Pre-existing out-of-scope state
included deleted paths under `agentos/reports/problem-intake/**`, untracked
artifacts under `reports/**`, and untracked artifacts under
`reports/human-checkpoints/**`.

Those paths were preserved and were not included in Task 2 scope. Task 1 files
were preserved as in-scope AOS-FARM.440 baseline artifacts and were not
reverted.

## Files Created
- `aos/templates/reviews/post-execution-review-template.md`
- `aos/templates/reviews/lessons-learned-template.md`
- `aos/templates/backlog/pipeline-hardening-backlog-item-template.md`
- `aos/templates/task-briefs/next-task-candidate-template.md`
- `aos/templates/reviews/README.md`
- `aos/templates/backlog/README.md`
- `aos/prompts/post-execution-review.md`
- `aos/reports/examples/evidence-to-backlog/README.md`
- `aos/reports/examples/evidence-to-backlog/post-execution-review-example.md`
- `aos/reports/examples/evidence-to-backlog/lessons-learned-example.md`
- `aos/reports/examples/evidence-to-backlog/pipeline-hardening-backlog-item-example.md`
- `aos/reports/examples/evidence-to-backlog/next-task-candidate-example.md`
- `aos/reports/examples/evidence-to-backlog/fixtures/valid/post-execution-review.md`
- `aos/reports/examples/evidence-to-backlog/fixtures/valid/lessons-learned.md`
- `aos/reports/examples/evidence-to-backlog/fixtures/valid/backlog-item.md`
- `aos/reports/examples/evidence-to-backlog/fixtures/valid/next-task-candidate.md`
- `aos/reports/examples/evidence-to-backlog/fixtures/negative/not-run-treated-as-pass.md`
- `aos/reports/examples/evidence-to-backlog/fixtures/negative/unknown-treated-as-ok.md`
- `aos/reports/examples/evidence-to-backlog/fixtures/negative/candidate-claims-approval.md`
- `aos/reports/examples/evidence-to-backlog/fixtures/negative/risk-profile-self-assigned.md`
- `aos/reports/examples/evidence-to-backlog/fixtures/negative/execution-authorized-inside-candidate.md`
- `reports/aos-farm-440-2-templates-examples-report.md`

## Files Edited
- `aos/templates/README.md`
- `aos/templates/task-briefs/README.md`

## Templates Added
- Post-Execution Review template.
- Lessons Learned template.
- Pipeline Hardening Backlog Item template.
- Next Task Candidate template.

## Examples Added
- Evidence-to-Backlog examples README.
- Post-Execution Review example.
- Lessons Learned example.
- Pipeline Hardening Backlog Item example.
- Next Task Candidate example.

## Fixtures Added
- Valid Post-Execution Review fixture.
- Valid Lessons Learned fixture.
- Valid Pipeline Hardening Backlog Item fixture.
- Valid Next Task Candidate fixture.
- Negative NOT_RUN treated as PASS fixture.
- Negative UNKNOWN treated as OK fixture.
- Negative candidate claims approval fixture.
- Negative Risk Profile self-assigned fixture.
- Negative execution authorized inside candidate fixture.

## Safety Invariants Preserved
- Evidence Review ≠ approval.
- Lessons Learned ≠ approval.
- Pipeline Hardening Backlog Item ≠ execution authorization.
- Next Task Candidate ≠ approved task.
- Validator PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Human unavailable for required decision → BLOCKED or HUMAN_REVIEW_REQUIRED.

## Forbidden Surfaces Not Touched
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
- `03_AOS_Future_and_Legacy_Reference_OPTIONAL.md`
- `agentos/**`
- `aos/docs/workflow/**`
- `aos/docs/user-guide/project-map.md`
- `aos/START_HERE.md`
- `aos/tools/optional/**`
- `aos/scripts/**`
- `tests/**`
- validator/helper files
- CI files
- release files
- merge automation files
- RAG-light files
- SQLite files

## Validation Commands Run
- `git diff --check -- <Task 2 paths>`
- `git diff --stat -- <Task 2 paths>`
- `git status --short -- <Task 2 paths>`
- `rg -n "APPROVED|approved task|execution_authorized: true|commit_authorized: true|push_authorized: true|auto-approval|auto-execution|auto-planner|runner|SQLite|RAG" <Task 2 paths>`

## Validation Result
validation_result: PASS

Forbidden-claim matches are expected only in prohibitions, warnings, explicit
boundary statements, or intentionally invalid negative fixtures.

## UNKNOWN
- none

## NOT_RUN
- Task 3 validator/helper code: NOT_RUN; out of scope.
- tests: NOT_RUN; out of scope.
- dogfood artifacts: NOT_RUN; out of scope.
- staging: NOT_RUN; forbidden by Task 2 prompt.
- commit: NOT_RUN; forbidden by Task 2 prompt.
- push: NOT_RUN; forbidden by Task 2 prompt.
- merge: NOT_RUN; forbidden by Task 2 prompt.
- tag: NOT_RUN; forbidden by Task 2 prompt.
- release: NOT_RUN; forbidden by Task 2 prompt.

## BLOCKED
- none

## Remaining Gaps
- Human review is required before Task 3 or any commit/push preparation.
- No validator/helper implementation exists in Task 2 scope.
- No tests were added in Task 2 scope.
- No dogfood artifact was created in Task 2 scope.

## Final Boundary
Task 2 stops at `HUMAN_REVIEW_REQUIRED`.
