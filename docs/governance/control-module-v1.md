# Governance / Control Module v1

## 1. Purpose
The Governance / Control Module v1 establishes a documentation and operational control-check layer for the AOS-FARM environment. It enforces formal gates and prevents execution without explicit authorization.

## 2. Non-authority boundary
This module provides a mechanism for checking state and presenting information to the Human Owner. It DOES NOT possess the authority to approve executions, commits, pushes, releases, or any lifecycle mutations.

## 3. Relation to Minimal Safety Floor
The Control Module v1 implements the Minimal Safety Floor defined in `02_AOS_Governance_Control_Module_and_Safety_Rules.md`, acting as the operational layer for its semantics.

## 4. Relation to Step 7 Contract
This module builds upon the thin contract established in Build Step 7, formalizing the gate execution model and required artifacts for verifying that the contract is upheld.

## 5. Gate execution model
Gates are executed sequentially and evaluated strictly. A failure or unknown result in any gate halts the execution and transitions to a `BLOCKED` or `HUMAN_REVIEW_REQUIRED` state. Gates cannot be bypassed by automated agents.

## 6. Required inputs
- Defined scope and Risk Profile
- Explicit human checkpoints
- Previous gate results and execution reports

## 7. Required outputs
- Checklists
- Gate Result records
- Execution Reports
- Human Review Checkpoints

## 8. BLOCKED states
A state becomes `BLOCKED` if:
- Required inputs are missing.
- Scope boundary is breached.
- A destructive operation is detected without specific authorization.

## 9. HUMAN_REVIEW_REQUIRED states
A state becomes `HUMAN_REVIEW_REQUIRED` when:
- Evaluating a `HIGH_RISK` or `HIGH_RISK_PROTECTED` execution.
- Lifecycle mutations are proposed.
- Protected/canonical rules are modified.
- Resolution of `BLOCKED` or `UNKNOWN` conditions is needed.

## 10. UNKNOWN_BLOCKED states
Any state or check result that cannot be conclusively evaluated as `PASS` or `FAIL` must be treated as `UNKNOWN`, which immediately transitions to a `BLOCKED` condition.

## 11. Human checkpoint boundary
The Human Owner is the sole authority. The checkpoint boundary clearly delineates agent preparation (read-only, planning) from execution and lifecycle mutations.

## 12. Forbidden interpretations (Mandatory Formulas)
- `PASS` ≠ approval
- `Evidence` ≠ approval
- `CI PASS` ≠ approval
- `UNKNOWN` ≠ OK
- `NOT_RUN` ≠ PASS
- Human approval cannot be simulated
- Readiness does not start next Build Step
