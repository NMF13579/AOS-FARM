# NOT_RUN Treated As PASS Report Fixture

```yaml
task_id: AOS-FARM.438
branch: build/controlled-execution-guard-mvp
changed_files:
  - aos/tools/optional/controlled_execution_guard.py
diff_summary: contradictory validation disclosure
commands_run: []
validation_results:
  not_run_is_pass: true
pass:
  - python -m pytest tests/guards/test_controlled_execution_guard.py
not_run:
  - python -m pytest tests/guards/test_controlled_execution_guard.py
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
next_safe_step: human review
```
