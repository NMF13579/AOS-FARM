# Thin Validator Contract

## 1. Overview
The Thin Validator is a fast, deterministic checker designed to enforce minimum safety constraints and validate that all preconditions are met before any execution, commit, or lifecycle mutation is allowed. This document defines the *contract* for the validator. The actual implementation will follow in Build Step 10.

## 2. Required Inputs
- Target files/scope to be checked.
- Human Authorization Checkpoints.
- Task definitions and risk profiles.

## 3. Required Outputs
- Structured Result output indicating `PASS` or `FAIL`.
- Explicit findings documenting any violations.
- A final Execution Report for the validation run.

## 4. Allowed Statuses
- `PASS`: All checks succeeded.
- `FAIL`: One or more checks failed.
- `BLOCKED`: The validator encountered a fatal error preventing execution.
- `UNKNOWN`: The validator could not conclusively determine the state.

## 5. BLOCKED States
A state is strictly BLOCKED if:
- Required inputs are missing.
- Execution syntax is invalid or unsupported.
- A check crashes or times out.
- The state violates protected rules.

## 6. UNKNOWN_BLOCKED States
If a check returns an ambiguous status or fails to explicitly return `PASS` or `FAIL`, it is treated as `UNKNOWN`. According to AOS-FARM invariant rules, `UNKNOWN` ≠ `OK`, and therefore an `UNKNOWN` state immediately forces a transition to a `BLOCKED` state.

## 7. Forbidden Claims (Invariants)
- `PASS` ≠ approval
- `Evidence` ≠ approval
- `CI PASS` ≠ approval
- `UNKNOWN` ≠ OK
- `NOT_RUN` ≠ PASS
- Validator result ≠ human approval
- Validator PASS ≠ commit/push/release authorization

## 8. Evidence vs Approval Boundary
The output of the validator, even if it is a complete `PASS`, is solely *evidence*. It proves that technical constraints are met, but it does NOT grant authorization. Human approval is an explicit, separate action.

## 9. Human Checkpoint Boundary
The validator cannot simulate human interaction. If a check requires human judgment or a human signature, the validator must fail-closed if that explicitly-formed checkpoint is absent.

## 10. Handoff to Step 10 Implementation
This contract acts as the blueprint. Build Step 10 will translate these invariants, inputs, and outputs into an executable script/program that strictly adheres to this contract without adding hidden features.
