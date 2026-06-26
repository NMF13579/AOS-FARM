# Approval Claimed Fixture

```yaml
task_id: AOS-FARM.438
branch: build/controlled-execution-guard-mvp
changed_files:
  - aos/tools/optional/controlled_execution_guard.py
diff_summary: invalid approval claim
commands_run:
  - python3 aos/scripts/aos_controlled_execution_guard.py postcheck --project-root . --aos-root aos --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report bad.md
validation_results:
  commands_run:
    - command: python3 aos/scripts/aos_controlled_execution_guard.py postcheck --project-root . --aos-root aos --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report bad.md
      result: PASS
      exit_code: 0
pass:
  - validator output captured
not_run: []
unknown: []
blocked: []
out_of_scope_changes: []
forbidden_actions_not_performed:
  - commit
  - push
commit_performed: false
push_performed: false
merge_performed: false
release_performed: false
next_task_started: false
approval_claimed: false
human_review_required: true
approved: true
next_safe_step: none
```
