# Valid Controlled Execution Evidence Report Fixture

```yaml
task_id: AOS-FARM.438
branch: build/controlled-execution-guard-mvp
changed_files:
  - aos/tools/optional/controlled_execution_guard.py
diff_summary: minimal controlled execution guard MVP files added under aos
commands_run:
  - python3 -m unittest discover -s tests/guards -p 'test_controlled_execution_guard.py'
validation_results:
  commands_run:
    - command: python3 -m unittest discover -s tests/guards -p 'test_controlled_execution_guard.py'
      result: PASS
      exit_code: 0
pass:
  - controlled execution guard tests passed
not_run: []
unknown: []
blocked: []
out_of_scope_changes: []
forbidden_actions_not_performed:
  - commit
  - push
  - merge
  - release
commit_performed: false
push_performed: false
merge_performed: false
release_performed: false
next_task_started: false
approval_claimed: false
human_review_required: true
next_safe_step: human review of execution and evidence reports
```
