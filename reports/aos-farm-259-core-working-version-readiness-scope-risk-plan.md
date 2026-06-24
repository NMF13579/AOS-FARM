# AOS-FARM.259 — Core Working Version Readiness Scope & Risk Plan

## 1. Stage Purpose
Perform a controlled readiness audit to determine whether the current AOS-FARM core can be treated as a Core Working Version / Release Candidate. This stage verifies if the core layers work together as a usable GitHub template/workflow system for a non-programmer.

## 2. Allowed Scope
- Conduct read-only readiness audit of core artifacts and user journeys.
- Generate readiness audit reports and gap registers if needed.
- Create status documentation (`docs/project-status/core-working-version-readiness.md`) only if readiness criteria are met.
- Verify warning regarding `Used tool: schedule` as a non-blocking anomaly.

## 3. Forbidden Operations
- Implementation of any new features or runner expansion.
- Autonomous execution or automatic lifecycle mutation.
- Automatic approval or stage progression.
- SQLite, RAG, search, or CI implementations.
- GitHub releases or tag creation.
- Destructive operations or modifications to protected/canonical sources.

## 4. Risk Profile
**Proposed Risk Profile:** `MEDIUM_RISK_GUIDED`
**Reason:** This stage audits already-created core workflow artifacts and generates reports. It strictly forbids changes to protected sources, approval semantics, lifecycle rules, CI, SQLite/RAG, and release/production state.
**Human assignment required:** The agent must not assign this Risk Profile as human. Human Risk Profile assignment is required before execution.
