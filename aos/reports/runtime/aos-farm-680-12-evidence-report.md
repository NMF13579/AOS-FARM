# AOS-FARM.680.12 — Workspace Binding Test Determinism Evidence Report

## 1. Verdict

Status at this checkpoint: pre-freeze validation complete, freeze pending.

This report records a narrow test-fixture correction for `AOS-FARM.680.12`.
The authorized goal is to remove environment dependence from
`tests/runtime/test_workspace_binding.py` without changing runtime semantics.

## 2. Parent Commit

- branch: `build/aos-farm-680-candidate-freeze`
- baseline commit: `1caac06c1bd3ad96bfcfdb8433bd208aabb75dc4`
- baseline parent: `5edc6a58acd6d44e7f5ee78772baaeaa6dd7b677`

## 3. Post-Push Failure

- failing test from AOS-FARM.680.11:
  `tests/runtime/test_workspace_binding.py::test_validate_workspace_state_binding`
- clean-clone full pytest result:
  - command: `.venv/bin/python -m pytest`
  - exit code: `1`
  - passed: `653`
  - failed: `1`
  - interpretation: environment-sensitive test fixture caused post-push closure failure

## 4. Root Cause

Classification accepted by human:

- `classification: NONDETERMINISTIC_TEST_FIXTURE`
- `runtime_regression_proven: false`
- `test_environment_dependency_proven: true`

Observed cause:

1. the old test used real repository state;
2. it implicitly expected untracked inventory;
3. active repository had large untracked inventory;
4. disposable clean clone did not;
5. one assertion locked the test to only one valid environment.

## 5. Runtime Semantics

- runtime files changed: `false`
- runtime semantics changed: `false`
- correction boundary: test fixture only

`validate_workspace_state_binding` semantics remain:

1. clean workspace without required untracked permission may pass;
2. untracked inventory without permission blocks;
3. untracked inventory with `required_checks.tracked_clean=true` passes;
4. staged or unstaged tracked changes block;
5. missing `baseline_state` fails closed;
6. PASS is technical only and is not approval.

## 6. Test Defect Classification

- defect type: nondeterministic fixture
- production runtime defect: not proven
- environment dependency: proven
- authorized repair shape: deterministic boundary mocking at `aos.runtime.package_binding.bind_repository`

## 7. Authorized Scope

Allowed candidate files:

1. `tests/runtime/test_workspace_binding.py`
2. `aos/reports/runtime/aos-farm-680-12-evidence-report.md`

Expected candidate count: `2`

## 8. Files Changed

1. `tests/runtime/test_workspace_binding.py`
2. `aos/reports/runtime/aos-farm-680-12-evidence-report.md`

## 9. Files Not Changed

Confirmed not changed:

1. `aos/runtime/workspace_binding.py`
2. `aos/runtime/package_binding.py`
3. `aos/scripts/aos_conditional_scope_check.py`
4. `aos/scripts/aos_validate.py`
5. `aos/schemas/aos_build_step_scope_contract.schema.json`
6. `aos/templates/execution-artifacts/aos-build-step-scope-contract-template.json`
7. `tests/scripts/test_aos_conditional_scope_check.py`
8. `tests/test_aos_validate.py`
9. `aos/reports/runtime/aos-farm-680-evidence-report.md`
10. `aos/reports/runtime/aos-farm-679-evidence-report.md`
11. `00_AOS_Core_Control.md`
12. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
13. `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
14. `AGENTS.md`
15. `.gitignore`

## 10. Deterministic Fixture Design

The corrected test no longer depends on active repository untracked inventory.

Design used:

1. keep `validate_workspace_state_binding` unmodified;
2. monkeypatch `aos.runtime.package_binding.bind_repository`;
3. feed deterministic `baseline_state` payloads into the validator;
4. assert mapping from `baseline_state` to validator result;
5. preserve separate fail-closed checks for invalid repository root and binding exceptions.

## 11. Test Cases

Deterministic state matrix implemented:

1. clean state without `required_checks` -> `PASS`
2. untracked inventory without permission -> `BLOCKED / UNTRACKED_INVENTORY_PRESENT`
3. untracked inventory with `tracked_clean` permission -> `PASS`
4. staged tracked change -> `BLOCKED / DIRTY_TRACKED_STATE`
5. unstaged tracked change -> `BLOCKED / DIRTY_TRACKED_STATE`
6. missing `baseline_state` result -> `UNKNOWN_BLOCKED / MISSING_REPOSITORY_STATE_CHECK`
7. missing unrelated binding field while `baseline_state` is present -> baseline state still governs result
8. wrong `baseline_head` type -> `UNKNOWN_BLOCKED / BINDING_EXCEPTION`
9. wrong package type -> `UNKNOWN_BLOCKED / BINDING_EXCEPTION`
10. input package immutability preserved
11. `PASS != APPROVED`

## 12. Targeted Validation

1. command: `.venv/bin/python -m pytest tests/runtime/test_workspace_binding.py -vv`
   - exit code: `0`
   - passed: `33`
   - failed: `0`
   - interpretation: deterministic workspace-binding coverage passes

2. command: `.venv/bin/python -m pytest tests/scripts/test_aos_conditional_scope_check.py`
   - exit code: `0`
   - passed: `31`
   - failed: `0`
   - interpretation: conditional scope checker regression coverage preserved

3. command: `.venv/bin/python -m pytest tests/test_aos_validate.py`
   - exit code: `0`
   - passed: `37`
   - failed: `0`
   - interpretation: aggregate validator regression coverage preserved

4. command: `git diff --check`
   - exit code: `0`
   - passed: `n/a`
   - failed: `0`
   - interpretation: no whitespace or patch-format issues

## 13. Active Repository Full Pytest

Initial exact command:

- command: `.venv/bin/python -m pytest`
- exit code: `0`
- passed: `663`
- failed: `0`
- interpretation: active repository no longer depends on pre-existing untracked inventory for workspace-binding outcome

## 14. Disposable Clean Clone Full Pytest

Clean clone location:

- `/private/tmp/aos-farm-68012-clean-hrktlB/repo`

Validation results:

1. command: `/Users/muhammed/Documents/GitHub/AOS-FARM/.venv/bin/python -m pytest tests/runtime/test_workspace_binding.py`
   - exit code: `0`
   - passed: `33`
   - failed: `0`
   - interpretation: deterministic workspace-binding cases pass in clean clone

2. command: `/Users/muhammed/Documents/GitHub/AOS-FARM/.venv/bin/python -m pytest`
   - exit code: `0`
   - passed: `663`
   - failed: `0`
   - interpretation: full clean-clone validation matches active repository outcome

3. command: `git diff --check`
   - exit code: `0`
   - passed: `n/a`
   - failed: `0`
   - interpretation: clean clone candidate diff has no patch-format issues

## 15. Aggregate Validation

1. command: `.venv/bin/python aos/scripts/aos_validate.py all --json`
   - exit code: `0`
   - passed: `n/a`
   - failed: `0`
   - interpretation: aggregate status remains advisory human boundary only

Observed aggregate summary:

- `overall_status: HUMAN_REVIEW_REQUIRED`
- `approval_granted: false`
- `execution_authorized: false`
- advisories:
  - `aos_install.py --dry-run -> HUMAN_REVIEW_REQUIRED`
  - `aos_next_task_selection.py -> HUMAN_REVIEW_REQUIRED`

## 16. Temporary Contract Boundary

Temporary contract created:

- path: `/private/tmp/AOS-FARM.680.12/freeze-contract.json`
- tracked template changed: `false`
- task id: `AOS-FARM.680.12`
- baseline head: `1caac06c1bd3ad96bfcfdb8433bd208aabb75dc4`
- branch: `build/aos-farm-680-candidate-freeze`
- commit message: `test: make workspace binding validation deterministic`
- candidate files:
  1. `tests/runtime/test_workspace_binding.py`
  2. `aos/reports/runtime/aos-farm-680-12-evidence-report.md`

## 17. Root Canonical Audit

- protected/canonical files changed: `false`
- historical evidence rewritten: `false`

## 18. Known Limitations

1. this report is pre-freeze and does not contain final tree OID;
2. commit authorization is not granted;
3. push authorization is not granted;
4. merge authorization is not granted;
5. release authorization is not granted;
6. default AOS-FARM.680 tracked contract remains a previous candidate artifact and is not repurposed for this repair candidate;
7. this evidence intentionally omits final tree OID and any authorization artifact;
8. repair-candidate freeze and verify-freeze remain pending at this checkpoint.

## 19. NOT_RUN

1. repair-candidate freeze
2. verify-freeze

## 20. UNKNOWN

unknown_items: []

## 21. Commit State

- commit created in AOS-FARM: `false`
- commit authorized: `false`

## 22. Push State

- push executed: `false`
- push authorized: `false`
- merge authorized: `false`
- release authorized: `false`

## 23. Required Human Action

After final clean-clone validation and repair-candidate freeze, a separate human checkpoint is still required before any commit, push, merge, or release.
