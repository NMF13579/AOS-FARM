task_id: AOS-FARM.438.R3
task_title: Valid Report Fixture Alias Polish
branch: build/controlled-execution-guard-mvp
repo_root: /Users/muhammed/Documents/GitHub/AOS-FARM

missing_fixture_path: aos/reports/examples/controlled-execution-guard/fixtures/valid_report.md
file_added: aos/reports/examples/controlled-execution-guard/fixtures/valid_report.md

commands_run:
  - pwd
  - git rev-parse --show-toplevel
  - git branch --show-current
  - git status -sb
  - find aos/reports/examples/controlled-execution-guard/fixtures -maxdepth 4 -type f | sort
  - sed -n '1,220p' aos/reports/examples/controlled-execution-guard/fixtures/reports/valid_report.md
  - python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report aos/reports/examples/controlled-execution-guard/fixtures/valid_report.md
  - python3 -m unittest discover -s tests/guards -p 'test_controlled_execution_guard.py'
  - python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos precheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml
  - python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report aos/reports/examples/controlled-execution-guard/fixtures/reports/not_run_treated_as_pass_report.md

exact_valid_postcheck_result:
  status: PASS
  exit_code: 0
  summary: postcheck verified evidence boundary disclosures

unittest_result:
  status: PASS
  exit_code: 0
  summary: Ran 18 tests successfully.

valid_precheck_result:
  status: PASS
  exit_code: 0
  summary: controlled execution package satisfies required guard boundaries

r1_negative_report_command_result:
  status: BLOCKED
  exit_code: 1
  summary: NOT_RUN treated as PASS remains blocked

validator_outputs:
  valid_postcheck:
    pass:
      - evidence report contains required execution boundary disclosures
      - commit/push/merge/release remained unperformed
      - human review remains required
  valid_precheck:
    pass:
      - risk profile present: HIGH_RISK_PROTECTED
      - human execution authorization present
      - scope and execution boundaries are fully declared
  r1_negative_postcheck:
    blocked:
      - NOT_RUN treated as PASS
      - same evidence listed as PASS and NOT_RUN: python -m pytest tests/guards/test_controlled_execution_guard.py
    not_run:
      - python -m pytest tests/guards/test_controlled_execution_guard.py

NOT_RUN:
  - none in the executed R3 command set

UNKNOWN:
  - none

BLOCKED:
  - expected negative result: aos/reports/examples/controlled-execution-guard/fixtures/reports/not_run_treated_as_pass_report.md

out_of_scope_findings:
  - none for this narrow correction
  - no active implementation was added outside aos/
  - agentos was untouched
  - pre-existing unrelated dirty state remained untouched

commit_performed: false
push_performed: false
merge_performed: false
release_performed: false
next_task_started: false
approval_claimed: false
human_review_required: true
final_status: HUMAN_REVIEW_REQUIRED
