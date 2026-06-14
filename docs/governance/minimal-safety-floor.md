# Minimal Safety Floor

## 1. Purpose
Formalize the always-on Minimal Safety Floor for AOS-FARM / AgentOS Next.

## 2. Always-On Status
The Minimal Safety Floor has been in effect since Build Step 0. This document formalizes its semantics.

## 3. Scope
The Minimal Safety Floor applies to all Documentation Assembly Pipelines, Code Assembly Pipelines, AI agent behaviors, and automated workflows.

## 4. Core Invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- Verification PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- BLOCKED ≠ PASS.

## 5. Approval Boundary
Human approval cannot be simulated.
Human approval cannot be inferred.
Human approval cannot be replaced by agent text.
Scope proposal ≠ execution authorization.

## 6. Evidence Boundary
Evidence is required to substantiate agent claims. Evidence acts as proof of state, not as an authorization to proceed.

## 7. PASS Boundary
PASS indicates a successful validation check. It does not replace human authorization for protected changes or lifecycle mutations.

## 8. UNKNOWN / NOT_RUN Boundary
UNKNOWN status must be treated as BLOCKED or HUMAN_REVIEW_REQUIRED. NOT_RUN must not be treated as a PASS.

## 9. Human Checkpoint Boundary
Checkpoints identify explicit requirements for human decisions. Agent must halt execution until human authorization is given.

## 10. Protected / Canonical Boundary
No protected/canonical change without explicit checkpoint.

## 11. Destructive Operations Boundary
No destructive operation by default.

## 12. Commit / Push / Release Boundary
Execution authorization ≠ commit authorization.
Commit authorization ≠ push authorization.
Push authorization ≠ release authorization.
Remote baseline closure ≠ production use.
No auto-commit.
No auto-push.
No auto-merge.
No release without explicit human authorization.
No production use without explicit human authorization.

## 13. Risk Profile Boundary
Agent may propose Risk Profile, but cannot self-assign LOW_RISK_FAST.

## 14. Agent Behavior Requirements
Scope must not expand without explicit human permission.
Human unavailable for required review/approval/checkpoint/Risk Profile assignment → BLOCKED or HUMAN_REVIEW_REQUIRED.

## 15. Minimal Safety Floor Checklist
Tasks must verify adherence against the `templates/minimal-safety-floor-checklist-template.md`.

## 16. Non-Goals
The Minimal Safety Floor does not provide runtime blocking itself. It establishes the semantic and authorization boundaries that Governance and Runtime Enforcement modules will enforce.

## 17. Final Boundary Statement
Minimal Safety Floor is always-on. It can block execution, but it cannot approve execution. Human approval remains above PASS, Evidence, CI, verification, and agent claims.
