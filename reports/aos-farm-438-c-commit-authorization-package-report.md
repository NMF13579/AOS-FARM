task_id: AOS-FARM.438.C
branch: build/controlled-execution-guard-mvp
repo_root: /Users/muhammed/Documents/GitHub/AOS-FARM
package_created: reports/aos-farm-438-commit-authorization-package.md
checkpoint_template_created: reports/human-checkpoints/aos-farm-438-commit-authorization.md

exact_commit_scope:
  - aos/tools/optional/controlled_execution_guard.py
  - aos/scripts/aos_controlled_execution_guard.py
  - aos/docs/controlled-execution-guard-mvp.md
  - aos/reports/examples/controlled-execution-guard/fixtures/*
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

excluded_out_of_scope_files:
  - pre-existing deletions under agentos/reports/problem-intake/...
  - unrelated untracked reports outside reports/aos-farm-438*.md
  - any other pre-existing dirty/untracked files not created by AOS-FARM.438

commands_run:
  - pwd
  - git rev-parse --show-toplevel
  - git branch --show-current
  - git status -sb
  - git rev-parse HEAD
  - git rev-parse origin/dev
  - git rev-list --left-right --count origin/dev...HEAD
  - git status --short
  - git ls-files --others --exclude-standard | sort
  - test ! -e agentos/guards && echo "OK: no agentos/guards" || find agentos/guards -maxdepth 3 -type f -print
  - grep -RIn "agentos" aos/tools/optional aos/scripts aos/docs/controlled-execution-guard-mvp.md tests/guards/test_controlled_execution_guard.py reports/aos-farm-438*.md 2>/dev/null || true
  - grep -RIn "00_AOS_Core_Control\\|01_AOS_Assembly\\|02_AOS_Governance\\|03_AOS_Future" aos/tools/optional aos/scripts aos/docs/controlled-execution-guard-mvp.md aos/reports/examples/controlled-execution-guard tests/guards/test_controlled_execution_guard.py 2>/dev/null || true
  - python3 -m unittest discover -s tests/guards -p 'test_controlled_execution_guard.py'
  - python3 -m pytest tests/guards/test_controlled_execution_guard.py
  - python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos precheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml
  - python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report aos/reports/examples/controlled-execution-guard/fixtures/valid_report.md
  - python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report reports/aos-farm-438-controlled-execution-guard-evidence-report.md
  - python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report aos/reports/examples/controlled-execution-guard/fixtures/reports/not_run_treated_as_pass_report.md
  - negative precheck commands for missing_human_authorization, missing_risk_profile, risk_profile_not_human_assigned, unknown_scope, approval_claimed, commit_claimed, push_claimed
  - python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos scopecheck --package aos/reports/examples/controlled-execution-guard/fixtures/changed_file_outside_scope.yaml --changed-files aos/reports/examples/controlled-execution-guard/fixtures/changed_file_outside_scope.yaml

validation_results:
  unittest: PASS
  valid_precheck: PASS
  valid_postcheck: PASS
  real_evidence_postcheck: PASS
  negative_not_run_treated_as_pass: BLOCKED
  missing_human_authorization: BLOCKED
  missing_risk_profile: HUMAN_REVIEW_REQUIRED
  risk_profile_not_human_assigned: HUMAN_REVIEW_REQUIRED
  unknown_scope: UNKNOWN_BLOCKED
  approval_claimed: BLOCKED
  commit_claimed: BLOCKED
  push_claimed: BLOCKED
  changed_file_outside_scope: BLOCKED

NOT_RUN:
  - python3 -m pytest tests/guards/test_controlled_execution_guard.py because pytest module was unavailable

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

commit_performed: false
push_performed: false
merge_performed: false
release_performed: false
next_task_started: false
approval_claimed: false
human_review_required: true
final_status: HUMAN_COMMIT_DECISION_REQUIRED
