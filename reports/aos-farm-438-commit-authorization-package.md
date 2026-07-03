task_id: AOS-FARM.438.C
source_task_id: AOS-FARM.438
branch: build/controlled-execution-guard-mvp
repo_root: /Users/muhammed/Documents/GitHub/AOS-FARM
base_branch: origin/dev
risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by: human
readiness_source: AOS-FARM.438.R4
readiness_status: READY_FOR_HUMAN_COMMIT_REVIEW

exact_commit_scope:
  - aos/tools/optional/controlled_execution_guard.py
  - aos/scripts/aos_controlled_execution_guard.py
  - aos/docs/controlled-execution-guard-mvp.md
  - aos/reports/examples/controlled-execution-guard/fixtures/approval_claimed.yaml
  - aos/reports/examples/controlled-execution-guard/fixtures/changed_file_outside_scope.yaml
  - aos/reports/examples/controlled-execution-guard/fixtures/commit_claimed.yaml
  - aos/reports/examples/controlled-execution-guard/fixtures/missing_authorized_files.yaml
  - aos/reports/examples/controlled-execution-guard/fixtures/missing_evidence.yaml
  - aos/reports/examples/controlled-execution-guard/fixtures/missing_human_authorization.yaml
  - aos/reports/examples/controlled-execution-guard/fixtures/missing_risk_profile.yaml
  - aos/reports/examples/controlled-execution-guard/fixtures/not_run_treated_as_pass.yaml
  - aos/reports/examples/controlled-execution-guard/fixtures/push_claimed.yaml
  - aos/reports/examples/controlled-execution-guard/fixtures/risk_profile_not_human_assigned.yaml
  - aos/reports/examples/controlled-execution-guard/fixtures/unknown_scope.yaml
  - aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml
  - aos/reports/examples/controlled-execution-guard/fixtures/valid_report.md
  - aos/reports/examples/controlled-execution-guard/fixtures/reports/approval_claimed_report.md
  - aos/reports/examples/controlled-execution-guard/fixtures/reports/missing_evidence_report.md
  - aos/reports/examples/controlled-execution-guard/fixtures/reports/not_run_treated_as_pass.md
  - aos/reports/examples/controlled-execution-guard/fixtures/reports/not_run_treated_as_pass_report.md
  - aos/reports/examples/controlled-execution-guard/fixtures/reports/valid_report.md
  - aos/reports/human-checkpoints/examples/aos-farm-438-controlled-execution-authorization-example.md
  - tests/guards/test_controlled_execution_guard.py
  - reports/aos-farm-438-controlled-execution-guard-execution-report.md
  - reports/aos-farm-438-controlled-execution-guard-evidence-report.md
  - reports/aos-farm-438-p1-active-aos-bundle-correction-report.md
  - reports/aos-farm-438-r-corrected-guard-review-report.md
  - reports/aos-farm-438-r1-fixture-naming-polish-report.md
  - reports/aos-farm-438-r2-final-commit-readiness-recheck-report.md
  - reports/aos-farm-438-r3-valid-report-fixture-alias-polish-report.md
  - reports/aos-farm-438-r4-final-commit-readiness-recheck-report.md

excluded_out_of_scope_state:
  - pre-existing deletions under agentos/reports/problem-intake/... are unrelated and excluded from commit scope
  - unrelated untracked reports outside reports/aos-farm-438*.md are excluded from commit scope
  - any other pre-existing dirty or untracked files not listed in exact_commit_scope are excluded
  - directory-level git status aggregates such as aos/scripts/ and tests/guards/ are not separate commit-scope artifacts beyond the exact files listed above

validation_summary:
  unittest:
    command: python3 -m unittest discover -s tests/guards -p 'test_controlled_execution_guard.py'
    result: PASS
    exit_code: 0
    summary: Ran 18 tests successfully.
  valid_precheck:
    command: python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos precheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml
    result: PASS
    exit_code: 0
  valid_postcheck:
    command: python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report aos/reports/examples/controlled-execution-guard/fixtures/valid_report.md
    result: PASS
    exit_code: 0
  real_evidence_postcheck:
    command: python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report reports/aos-farm-438-controlled-execution-guard-evidence-report.md
    result: PASS
    exit_code: 0
  negative_not_run_treated_as_pass:
    command: python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report aos/reports/examples/controlled-execution-guard/fixtures/reports/not_run_treated_as_pass_report.md
    result: BLOCKED
    exit_code: 1
  negative_prechecks:
    - fixture: missing_human_authorization.yaml
      result: BLOCKED
    - fixture: missing_risk_profile.yaml
      result: HUMAN_REVIEW_REQUIRED
    - fixture: risk_profile_not_human_assigned.yaml
      result: HUMAN_REVIEW_REQUIRED
    - fixture: unknown_scope.yaml
      result: UNKNOWN_BLOCKED
    - fixture: approval_claimed.yaml
      result: BLOCKED
    - fixture: commit_claimed.yaml
      result: BLOCKED
    - fixture: push_claimed.yaml
      result: BLOCKED
    - fixture: changed_file_outside_scope.yaml
      result: BLOCKED

NOT_RUN:
  - python3 -m pytest tests/guards/test_controlled_execution_guard.py because pytest module was unavailable
  - reports/aos-farm-438-controlled-execution-guard-evidence-report.md still records python -m pytest as NOT_RUN because python command was unavailable in that earlier evidence context

UNKNOWN:
  - unknown_scope.yaml returned UNKNOWN_BLOCKED as expected
  - missing_risk_profile.yaml returned HUMAN_REVIEW_REQUIRED as expected

BLOCKED:
  - missing_human_authorization.yaml blocked as expected
  - approval_claimed.yaml blocked as expected
  - commit_claimed.yaml blocked as expected
  - push_claimed.yaml blocked as expected
  - changed_file_outside_scope.yaml blocked as expected
  - not_run_treated_as_pass_report.md blocked as expected

commit_message_proposal: feat: add controlled execution guard MVP
commit_allowed_now: false
push_allowed_now: false
merge_allowed_now: false
release_allowed_now: false
next_task_allowed_now: false
human_decision_required: true

notes:
  - This package does not authorize commit.
  - This package does not authorize push.
  - Human approval is required before commit execution.
  - PASS is not approval.
  - Evidence is not approval.
  - CI PASS is not approval.
