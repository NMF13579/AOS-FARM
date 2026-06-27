---
task_id: AOS-FARM.444
stage: fixtures
title: AOS-FARM.444.8 Fixtures Report
---

Created test fixtures for read-only checker:
- tests/fixtures/result_acceptance/positive/accept_result_pass.json
- tests/fixtures/result_acceptance/positive/accept_result_with_warnings.json
- tests/fixtures/result_acceptance/warning/accept_not_enough_evidence_with_acknowledgement.json
- tests/fixtures/result_acceptance/negative/missing_human_decision.json
- tests/fixtures/result_acceptance/negative/unknown_human_decision.json
- tests/fixtures/result_acceptance/negative/accept_blocked_task_quality.json
- tests/fixtures/result_acceptance/negative/accept_unknown_required_field.json
- tests/fixtures/result_acceptance/negative/accept_not_run_required_check.json
- tests/fixtures/result_acceptance/negative/needs_changes_without_follow_up.json
- tests/fixtures/result_acceptance/negative/reject_without_reason.json
- tests/fixtures/result_acceptance/negative/commit_authorized_true.json
- tests/fixtures/result_acceptance/negative/push_authorized_true.json
- tests/fixtures/result_acceptance/negative/next_task_started_true.json
- tests/fixtures/result_acceptance/negative/lifecycle_mutation_true.json
- tests/fixtures/result_acceptance/malformed/invalid_json.json
