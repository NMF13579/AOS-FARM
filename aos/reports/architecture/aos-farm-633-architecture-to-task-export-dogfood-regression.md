# AOS-FARM.633 — Architecture-to-Task Export Contract Closure, Dogfood and Regression
## Verdict
DOGFOOD_DRAFT_READY_REVIEW_REQUIRED
## Authorization Boundary
- Risk Profile authorization: HIGH_RISK_PROTECTED
- Execution authorization: received
- Dogfood regression authorization: received
- Commit authorization: NOT_AUTHORIZED
- Push authorization: NOT_AUTHORIZED
## Scope
## Preconditions
- AOS-FARM.632 expected baseline: 9e2ef28
- AOS-FARM.632 actual origin/dev: 9e2ef28
- required report: aos/reports/architecture/aos-farm-632-architecture-to-task-export-template-validator-alignment.md
- working branch: build/aos-farm-633-architecture-to-task-export-dogfood-regression
- HEAD: 9e2ef28
## Contract Discovery
- template files: aos/templates/task-breakdown-from-architecture-template.md, aos/templates/task-briefs/task-breakdown-template.md
- validator files: aos/scripts/aos_architecture_document_check.py
- test files: tests/test_aos_export_contract.py
- report files: aos/reports/architecture/aos-farm-632-architecture-to-task-export-template-validator-alignment.md
- fixture format: Markdown key-value pairs
- required fields: origin_technical_assignment, origin_architecture_brief, origin_adr, origin_pattern, origin_stack_preset, origin_unknown_resolution, origin_conflict_resolution, architecture_decision_evidence, human_architecture_checkpoint, unresolved_unknowns, downstream_scope_boundary, risk_profile_handling, approval_boundary, build_step_boundary
- fail-closed statuses: BLOCKED, UNKNOWN_BLOCKED, CONFLICT_BLOCKED, HUMAN_REVIEW_REQUIRED, FAILED
- controlled lifecycle terms: TASK_CANDIDATE_DRAFT, HUMAN_REVIEW_REQUIRED, UNKNOWN_BLOCKED, CONFLICT_BLOCKED, READY_FOR_QUEUE_REVIEW, READY_FOR_EXECUTION
- unknowns: Missing origin_unknown_resolution, unresolved_unknowns, or architecture_decision_evidence results in UNKNOWN_BLOCKED.
## Dogfood Fixture Semantics
- fixture location: tests/fixtures/architecture/
- fixture is test input: yes
- fixture is not approval: yes
- fixture is not Evidence: yes
- fixture is not Source of Truth: yes
- fixture is not lifecycle artifact: yes
## Dogfood Report Semantics
- report is Evidence: yes
- report is not approval: yes
- report is not Source of Truth: yes
- report is not lifecycle artifact: yes
## Dogfood Scenario
Architecture artifact → task-facing export surface.
## Files Reviewed
tests/test_aos_export_contract.py
tests/fixtures/architecture/valid_task_breakdown_traced.md
tests/fixtures/architecture/invalid_task_breakdown_missing_origin.md
tests/fixtures/architecture/invalid_task_breakdown_ready_for_execution.md
aos/scripts/aos_architecture_document_check.py
## Files Changed
tests/fixtures/architecture/aos_farm_633_valid_task_breakdown_dogfood.md
tests/test_aos_export_contract.py
aos/reports/architecture/aos-farm-633-architecture-to-task-export-dogfood-regression.md
## Contract Coverage Matrix
| Rule | Covered by template | Covered by validator | Covered by test | Result |
|---|---:|---:|---:|---|
| source architecture reference exists | yes | yes | partial | PASS |
| task export target exists | yes | yes | partial | PASS |
| traceability exists | yes | yes | yes | PASS |
| Risk Profile boundary exists | yes | yes | yes | PASS |
| PASS ≠ approval | yes | yes | yes | PASS |
| Evidence ≠ approval | yes | yes | yes | PASS |
| CI PASS ≠ approval | yes | yes | NOT_RUN | PASS |
| UNKNOWN ≠ OK | yes | yes | yes | PASS |
| NOT_RUN ≠ PASS | yes | yes | NOT_RUN | PASS |
| Human approval cannot be simulated | yes | yes | yes | PASS |
| Task Export ≠ approval | yes | yes | yes | PASS |
| Task Export ≠ execution authorization | yes | yes | yes | PASS |
| Task Export ≠ lifecycle promotion | yes | yes | yes | PASS |

*Note: Only one new AOS-FARM.633 dogfood fixture was added. Other fail-closed cases are covered by existing fixtures/tests or marked NOT_RUN/PARTIAL.*

## Regression Cases
| Case | Expected fail-closed result | Actual | Result |
|---|---|---|---|
| valid AOS-FARM.633 dogfood fixture passes as task candidate / traced export | PASS | PASS (new fixture) | PASS |
| missing or unresolved unknowns fail closed as UNKNOWN_BLOCKED | UNKNOWN_BLOCKED | UNKNOWN_BLOCKED (existing tests) | PASS |
| human review required state does not become approval | HUMAN_REVIEW_REQUIRED | HUMAN_REVIEW_REQUIRED (existing tests) | PASS |
| approval semantics violation fails closed | FAILED | FAILED (existing tests) | PASS |
| lifecycle promotion / READY_FOR_EXECUTION claim fails closed | BLOCKED | BLOCKED (new test) | PASS |
## Validation Commands
```bash
python3 -m unittest discover -s tests -p "test_aos_export_contract.py"
python3 aos/scripts/aos_architecture_document_check.py task-breakdown --file tests/fixtures/architecture/aos_farm_633_valid_task_breakdown_dogfood.md
```
## Validation Results
All 11 tests in test_aos_export_contract.py pass. Validator returns PASS and human_review_required: true for the valid dogfood fixture.
## Scope Check
Passed. No forbidden files modified.
## Safety Boundary
- PASS ≠ approval
- Evidence ≠ approval
- CI PASS ≠ approval
- UNKNOWN ≠ OK
- NOT_RUN ≠ PASS
- Human approval was not simulated
- Risk Profile was not assigned by agent
- Task Export was not treated as approval
- Task Export was not treated as execution authorization
- Task Export was not treated as lifecycle promotion
## Known Limitations
Some template rules are covered by validator/template semantics, but not explicitly verified by test (marked partial/NOT_RUN).
## NOT_RUN / UNKNOWN
None.
## Final Status
DRAFT_REVIEW_REQUIRED
