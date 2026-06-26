# AOS-FARM.438.P1 Active AOS Bundle Correction Report

```yaml
task_id: AOS-FARM.438.P1
task_title: Move Controlled Execution Guard MVP into active aos bundle
branch: build/controlled-execution-guard-mvp
risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by: human
initial_finding: implementation was placed outside the active aos bundle
active_runtime_target: aos
legacy_runtime_target: agentos
commit_performed: false
push_performed: false
merge_performed: false
release_performed: false
next_task_started: false
approval_claimed: false
human_review_required: true
final_status: HUMAN_REVIEW_REQUIRED
```

## Correction Summary

- AOS-FARM.438 reached Evidence boundary, but human review found that the implementation lived in the wrong product zone.
- The active runtime implementation was recreated under `aos/`:
  - `aos/tools/optional/controlled_execution_guard.py`
  - `aos/scripts/aos_controlled_execution_guard.py`
  - `aos/docs/controlled-execution-guard-mvp.md`
  - `aos/reports/examples/controlled-execution-guard/...`
- Development-only validation remained in `tests/guards/test_controlled_execution_guard.py`.

## Misplaced Files Handling

- Removed after safe migration:
  - `agentos/guards/__init__.py`
  - `agentos/guards/controlled_execution_guard.py`
  - `scripts/aos_controlled_execution_guard.py`
  - `tests/fixtures/controlled_execution/*`
  - `docs/assembly/controlled-execution-guard-mvp.md`
- Retained with reason:
  - `tests/guards/test_controlled_execution_guard.py` remains a dev harness, not active runtime product code.

## Boundary Notes

- `agentos/` remains archive / legacy.
- `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`, and `03_AOS_Future_and_Legacy_Reference_OPTIONAL.md` remain AOS-FARM development sources only.
- The runtime guard does not require those files inside `aos/` or inside a user project.
