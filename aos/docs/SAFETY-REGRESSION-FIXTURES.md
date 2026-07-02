# Safety Regression Fixtures

> **GUIDANCE BOUNDARY:**
> This document is guidance only.

## Purpose
Safety regression fixtures are used to verify that the AOS validation layer correctly identifies and blocks violations of the Minimal Safety Floor. 

These fixtures include negative test cases where an agent or user might incorrectly attempt to use:
- `PASS` as approval
- `CI PASS` as approval
- Evidence claims as approval
- `NOT_RUN` as `PASS`
- `UNKNOWN` as `OK`
- Queue NEXT as execution authorization
- Doctor PASS as authorization
- Dashboard NEXT as authorization
- Prompt pack as Source of Truth
- Task candidate as approval

## Tests
The fixtures are stored in `tests/fixtures/aos-safety-regression/`. The test suite `tests/test_aos_safety_regression.py` validates that `aos_task_document_check.py` successfully blocks these known unsafe patterns.
