# AOS-FARM.452 Task Brief

## Metadata
**task_id**: AOS-FARM.452
**task_title**: First Controlled Code Work Dogfood through AOS-FARM.451 Execution Corridor
**risk_profile_proposal**: HIGH_RISK_PROTECTED
**status**: AOS_FARM_452_TASK_BRIEF_CREATED_EXECUTION_AUTHORIZATION_REQUIRED
**stop_before_commit**: true
**stop_before_push**: true
**stop_before_release**: true

## 1. Problem
We need to dogfood the newly established AOS-FARM.451 Execution Corridor (task-to-code execution bridge) by performing a controlled code work operation on a high-risk validator.

## 2. Goal
Perform the first controlled code work dogfooding through the AOS-FARM.451 Execution Corridor without violating any safety invariant, executing a scoped change on the code quality control validator.

## 3. Scope
The scope is strictly limited to making code changes inside the `aos_code_quality_control.py` validator and its associated tests and fixtures. Generating the required evidence and reports for human review.

## 4. Allowed files
- aos/scripts/aos_code_quality_control.py
- tests/test_aos_code_quality_control.py
- tests/fixtures/code_quality_control/
- reports/aos-farm-452-*.md

## 5. Forbidden files
- 00_AOS_Core_Control.md
- 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
- 02_AOS_Governance_Control_Module_and_Safety_Rules.md
- aos/root/AGENTS.md
- README.md
- START_HERE*

## 6. Required tests
- `python3 -m unittest tests/test_aos_code_quality_control.py` must pass for all fixtures.

## 7. Required checks
- `git diff --check` must be clean.
- Protected/canonical diff must be empty.

## 8. Acceptance criteria
- Code changes correctly implement the scoped logic inside allowed files.
- Tests pass.
- Invariants are preserved.
- No forbidden files modified.
- Validator does not emit false `APPROVED` states.

## 9. Evidence required
- Diff of the code changes.
- Output of the test execution.
- Human Review Report clearly indicating the required execution authorization bounds.

## 10. Out of scope
- Autonomous runner execution.
- Lifecycle mutation automation.
- Any change to control / safety documentation.
- Execution without human authorization.

## 11. Required invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Task Queue position ≠ execution authorization.
- Task Brief ≠ execution authorization.
- Execution Package valid ≠ approval.
- Code Quality reported ≠ approval.
- Commit authorization ≠ push authorization.
- Push authorization ≠ release authorization.

## 12. Human authorization boundary
- Task Brief does not authorize execution.
- Task Brief does not authorize commit.
- Task Brief does not authorize push.
- Task Brief does not authorize release.
- Human approval cannot be simulated.
- Risk Profile is proposed, not self-assigned by the agent.

**Risk Profile proposal**: HIGH_RISK_PROTECTED
**Reason**: Задача потенциально затрагивает validator/control logic: `aos/scripts/aos_code_quality_control.py`, `tests/test_aos_code_quality_control.py`, `tests/fixtures/code_quality_control/`.
Validator интерпретирует boundaries: PASS / Evidence / approval / UNKNOWN / NOT_RUN / commit / push / release / human review status.

## 13. Stop conditions
- Stop before commit.
- Stop before push.
- Stop before release.
