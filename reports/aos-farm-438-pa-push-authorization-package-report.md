task_id: AOS-FARM.438.PA
branch: build/controlled-execution-guard-mvp
repo_root: /Users/muhammed/Documents/GitHub/AOS-FARM
commit_sha: 814c20433af68552b0bb3a884381fa7946c37ac3
origin_dev_sha: bb39f6946e3bbf170cb7ab802c1cd711d2da6026
ahead_behind: "0 1"
package_created: reports/aos-farm-438-push-authorization-package.md
checkpoint_template_created: reports/human-checkpoints/aos-farm-438-push-authorization.md
push_command_candidate: git push origin HEAD:dev

commands_run:
  - pwd
  - git rev-parse --show-toplevel
  - git branch --show-current
  - git status -sb
  - git rev-parse HEAD
  - git show -s --format='%H%n%s' HEAD
  - git rev-parse origin/dev
  - git rev-list --left-right --count origin/dev...HEAD
  - git fetch origin
  - git ls-remote origin refs/heads/dev
  - git show --name-status --oneline --no-renames HEAD
  - git diff-tree --no-commit-id --name-only -r HEAD | sort
  - git status --short
  - git ls-files --others --exclude-standard | sort
  - python3 -m unittest discover -s tests/guards -p 'test_controlled_execution_guard.py'
  - python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos precheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml
  - python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report aos/reports/examples/controlled-execution-guard/fixtures/valid_report.md
  - python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report aos/reports/examples/controlled-execution-guard/fixtures/reports/not_run_treated_as_pass_report.md

validation_results:
  unittest: PASS
  valid_precheck: PASS
  valid_postcheck: PASS
  negative_not_run_treated_as_pass: BLOCKED
  head_commit_matches_expected: PASS
  ahead_behind_matches_expected: PASS
  remote_baseline_still_one_commit_behind: PASS
  commit_content_matches_verified_scope: PASS

NOT_RUN:
  - none in the executed AOS-FARM.438.PA package command set

UNKNOWN:
  - none

BLOCKED:
  - expected negative result for not_run_treated_as_pass_report.md

excluded_out_of_scope_state:
  - pre-existing deletions under agentos/reports/problem-intake/... remain local and uncommitted
  - unrelated untracked reports/* outside AOS-FARM.438 remain local and uncommitted
  - commit authorization package artifacts remain local and uncommitted
  - push authorization package artifacts from this task remain local and uncommitted until a separate human-authorized commit step exists

push_performed: false
merge_performed: false
release_performed: false
next_task_started: false
approval_claimed: false
human_push_decision_required: true
final_status: HUMAN_PUSH_DECISION_REQUIRED
