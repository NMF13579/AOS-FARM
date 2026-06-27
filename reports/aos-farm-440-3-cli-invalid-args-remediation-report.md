# AOS-FARM.440.3.F1 CLI Invalid-Argument Final Status Remediation Report

## Status
task_id: AOS-FARM.440.3.F1
task_name: CLI Invalid-Argument Final Status Remediation
risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by: human
blocking_review: AOS-FARM.440.R3
branch: build/evidence-to-backlog-loop-mvp
baseline_sha: d612284028fea7984f3d8833a2b2b427c47e8d99
origin_dev_sha: d612284028fea7984f3d8833a2b2b427c47e8d99
ahead_behind: 0 0
commit_performed: false
push_performed: false
merge_performed: false
release_performed: false
next_task_started: false
human_review_required: true
final_status: HUMAN_REVIEW_REQUIRED

## Blocked Reason
AOS-FARM.440.R3 found that invalid CLI arguments used default argparse
behavior, printed usage, exited non-zero, and did not emit machine-readable
output containing `final_status`.

## Scope
This remediation only changed invalid-argument reporting for the
Evidence-to-Backlog CLI wrapper and added test coverage for that behavior.

Task 4 was not started. No dogfood artifacts were created.

## Dirty Worktree Boundary
The local worktree was dirty before remediation. Pre-existing out-of-scope
state included deleted paths under `agentos/reports/problem-intake/**`,
untracked artifacts under `reports/**`, untracked artifacts under
`reports/human-checkpoints/**`, and uncommitted Task 1, Task 2, and Task 3
artifacts.

Those paths were preserved and were not included in this remediation scope.

## Files Created
- `reports/aos-farm-440-3-cli-invalid-args-remediation-report.md`

## Files Edited
- `aos/scripts/aos_evidence_to_backlog.py`
- `tests/evidence_to_backlog/test_evidence_to_backlog_validator.py`
- `reports/aos-farm-440-3-validator-tests-report.md`

## Behavior Before
- Supported valid commands worked.
- Missing files returned JSON with `final_status: BLOCKED`.
- Invalid arguments printed argparse usage and exited `2`.
- Invalid arguments did not emit machine-readable `final_status`.

## Behavior After
- Invalid arguments still exit non-zero.
- Invalid arguments emit JSON containing `final_status: BLOCKED`.
- Invalid argument JSON includes:
  - `final_status`
  - `errors`
  - `command`
  - `approval_claimed: false`
  - `execution_authorized: false`
  - `commit_authorized: false`
  - `push_authorized: false`
  - `next_task_started: false`
- Invalid argument output does not claim approval or authorization.

## Tests Added Or Updated
- Added unittest coverage for `python3 aos/scripts/aos_evidence_to_backlog.py validate-review` without required arguments.
- The test verifies non-zero exit, `final_status`, `final_status: BLOCKED`, no forbidden final status, and no approval claim.

## Validation Commands Run
- `python3 -m unittest discover -s tests/evidence_to_backlog -p 'test_evidence_to_backlog_validator.py'`
- `python3 aos/scripts/aos_evidence_to_backlog.py validate-chain --review aos/reports/examples/evidence-to-backlog/fixtures/valid/post-execution-review.md --lessons aos/reports/examples/evidence-to-backlog/fixtures/valid/lessons-learned.md --item aos/reports/examples/evidence-to-backlog/fixtures/valid/backlog-item.md --candidate aos/reports/examples/evidence-to-backlog/fixtures/valid/next-task-candidate.md`
- `python3 aos/scripts/aos_evidence_to_backlog.py validate-review`
- `python3 aos/scripts/aos_evidence_to_backlog.py unknown-command`
- negative fixture CLI checks for NOT_RUN/PASS, UNKNOWN/OK, candidate approval, Risk Profile self-assignment, and execution authorization.
- `git diff --check -- <remediation paths>`
- `git diff --stat -- <remediation paths>`
- `git status --short -- <remediation paths>`
- targeted forbidden-claim `rg` on remediation paths.

## Test Commands Run
- `python3 -m unittest discover -s tests/evidence_to_backlog -p 'test_evidence_to_backlog_validator.py'`

## Test Result
test_result: PASS

## Invalid Argument Result
invalid_argument_result: PASS

Both invalid argument commands exited non-zero and emitted JSON containing
`final_status: BLOCKED`.

## Safety Invariants Preserved
- PASS != approval.
- Evidence != approval.
- CI PASS != approval.
- UNKNOWN != OK.
- NOT_RUN != PASS.
- Human approval cannot be simulated.
- Next Task Candidate != approved task.
- Pipeline Hardening Backlog Item != execution authorization.
- Lessons Learned != approval.
- Evidence Review != approval.
- Validator PASS != approval.
- Agent must not self-assign LOW_RISK_FAST.

## Forbidden Surfaces Not Touched
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
- `03_AOS_Future_and_Legacy_Reference_OPTIONAL.md`
- `agentos/**`
- `aos/docs/workflow/**`
- `aos/docs/user-guide/project-map.md`
- `aos/START_HERE.md`
- `aos/templates/**`
- `aos/prompts/**`
- `aos/reports/examples/**`
- CI files
- release files
- merge automation files
- RAG-light files
- SQLite files
- dogfood artifacts

## UNKNOWN
- none

## NOT_RUN
- Task 4: NOT_RUN; out of scope.
- dogfood artifacts: NOT_RUN; out of scope.
- staging: NOT_RUN; forbidden by remediation prompt.
- commit: NOT_RUN; forbidden by remediation prompt.
- push: NOT_RUN; forbidden by remediation prompt.
- merge: NOT_RUN; forbidden by remediation prompt.
- tag: NOT_RUN; forbidden by remediation prompt.
- release: NOT_RUN; forbidden by remediation prompt.

## BLOCKED
- none

## Remaining Gaps
- Human review is required before Task 4 or any commit/push preparation.
- The validator remains optional and is not wired into CI.

## Final Boundary
This remediation stops at `HUMAN_REVIEW_REQUIRED`.
