# AOS-FARM.251 — Thin Task Queue Helper Dogfood Scope & Risk Plan

## 1. Stage Purpose
Dogfood the Thin Task Queue Helper / Dry-Run Runner MVP on a real AOS-FARM task flow. This stage proves that the helper can safely support the manual task queue workflow without becoming an approval authority, execution engine, lifecycle mutator, or autonomous runner.

## 2. Dogfood Scenario
**Target task:** AOS-FARM.259 (Core Working Version Readiness Audit Scope / Risk / Authorization Preparation)
*Note: This target will only be used as a sample input. No actual execution of AOS-FARM.259 will occur during this dogfood.*

## 3. Allowed Scope
- Create dogfood queue item for AOS-FARM.259.
- Run helper in `dry-run`, `validate`, `next-safe-step`, `generate-handoff`, and `generate-verification` modes.
- Confirm detection of required fields, missing approval, and unsafe transitions.
- Confirm helper fails closed on missing approval and unsafe transition.
- Generate dogfood artifacts and execution reports.
- Create human checkpoints.
- Commit/push only after explicit Human authorization.

## 4. Forbidden Operations
- Implementation or execution of AOS-FARM.259 or any queued task.
- Automatic agent launch or autonomous execution.
- Automatic lifecycle mutation.
- Automatic approval.
- Staging/committing/pushing outside of explicitly authorized steps.
- Helper authority expansion.
- SQLite, RAG, or search implementation.
- Destructive operations.
- Modifying protected/canonical source files.

## 5. Risk Profile
**Proposed Risk Profile:** `MEDIUM_RISK_GUIDED`
**Reason:** This stage executes a previously authorized dry-run helper against dogfood fixtures and writes dogfood evidence. It does not execute project tasks, mutate lifecycle automatically, approve, commit, push, or expand helper authority.
**Human assignment required:** The agent must not assign this Risk Profile as human. Human Risk Profile assignment is required before dogfood execution.
