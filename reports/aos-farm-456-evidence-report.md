# AOS-FARM.456 — Evidence Report

## Validator execution commands and results:

1. Valid Mapping
`python3 aos/scripts/aos_task_quality_check.py validate-forbidden-evidence --mapping tests/fixtures/forbidden_behavior_evidence_mapping/valid_mapping.json`
Result: `FORBIDDEN_EVIDENCE_MAPPING_VALID_HUMAN_REVIEW_REQUIRED`, exit code 0.

2. Negative Approved Status
`python3 aos/scripts/aos_task_quality_check.py validate-forbidden-evidence --mapping tests/fixtures/forbidden_behavior_evidence_mapping/negative_final_status_approved.json`
Result: `FORBIDDEN_EVIDENCE_MAPPING_BLOCKED`, exit code 1.

3. UNKNOWN Without Human Review
`python3 aos/scripts/aos_task_quality_check.py validate-forbidden-evidence --mapping tests/fixtures/forbidden_behavior_evidence_mapping/negative_unknown_without_human_review.json`
Result: `FORBIDDEN_EVIDENCE_MAPPING_UNKNOWN_BLOCKED`, exit code 1.

## Test Results
`python3 -m unittest discover -s tests -p "*forbidden_behavior*"`
PASS: All tests for the forbidden behavior evidence mapping executed successfully.

`python3 -m unittest discover -s tests -p "*task_quality*"`
PASS: All existing task quality checker tests executed successfully.
