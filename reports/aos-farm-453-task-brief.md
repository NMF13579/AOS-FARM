# AOS-FARM.453 - Add Overengineering Review Gate to Code Execution Corridor

## Metadata
- **task_id**: AOS-FARM.453
- **task_title**: Add Overengineering Review Gate to Code Execution Corridor
- **risk_profile_proposal**: HIGH_RISK_PROTECTED
- **status**: AOS_FARM_453_TASK_BRIEF_CREATED_EXECUTION_AUTHORIZATION_REQUIRED
- **stop_before_commit**: true
- **stop_before_push**: true
- **stop_before_release**: true

## Problem
A small code task can drift into unnecessary architectural changes, validator semantics changes, or complex abstractions without explicit human review (as seen in AOS-FARM.452).

## Goal
Add a lightweight, declarative Overengineering Review Gate inside the Code Execution Corridor to catch scope drift, future-only code, and unauthorized abstractions before human review, without automatically blocking or mutating lifecycle.

## Scope
Add `overengineering_controls` section to Code Execution Package template and `Overengineering / Complexity Review` section to Code Quality Review template. Update the validator to report these controls without changing approval semantics.

## Allowed files
- aos/templates/code-execution-package-template.md
- aos/templates/code-quality-review-template.md
- aos/scripts/aos_code_quality_control.py
- tests/test_aos_code_quality_control.py
- tests/fixtures/code_quality_control/
- reports/aos-farm-453-*.md

## Forbidden files
- 00_AOS_Core_Control.md
- 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
- 02_AOS_Governance_Control_Module_and_Safety_Rules.md
- aos/root/AGENTS.md
- README.md
- START_HERE*
- .github/workflows/

## Required tests
- python3 -m unittest -v tests/test_aos_code_quality_control.py

## Required checks
- git diff --check
- git diff --stat
- git diff --name-status
- protected/canonical diff check
- validator validate-package check
- validator summarize check

## Acceptance criteria
See AOS-FARM.453 instructions for full Human Review readiness.

## Evidence required
- Precheck baseline report
- Validator outputs
- Code Quality Review
- Dogfood/Evidence reports

## Out of scope
- CI integration
- Radon/lizard integration
- Hard block by line count
- Automatic split implementation
- Dashboard output
- Approval/commit/push automation
- Canonical governance updates

## Required invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Task Brief ≠ execution authorization.
- Execution Package valid ≠ approval.
- Code Quality reported ≠ approval.
- Complexity warning ≠ approval.
- Complexity warning ≠ automatic rejection.
- Commit authorization ≠ push authorization.
- Push authorization ≠ release authorization.
- Validator does not emit APPROVED, READY_FOR_RELEASE, READY_FOR_MERGE, READY_FOR_COMMIT, READY_FOR_PUSH, PASS-as-approval.

## Human authorization boundary
- Task Brief does not authorize execution.
- Task Brief does not authorize commit.
- Task Brief does not authorize push.
- Task Brief does not authorize release.
- Risk Profile is proposed, not self-assigned by the agent.

## Stop conditions
- Wait for Explicit Human Authorization before creating the Code Execution Package.
- Stop before commit.
- Stop before push.
- Stop before release.
