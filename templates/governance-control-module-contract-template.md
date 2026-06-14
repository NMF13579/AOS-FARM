# Governance / Control Module Contract Template

This contract does not grant approval.
This contract does not authorize execution.
This contract does not authorize commit.
This contract does not authorize push.
This contract does not authorize release.
This contract does not authorize production use.
Human approval remains required where required by governance rules.

## 1. Module Purpose
[Define the core goal of this governance module]

## 2. Source Authority
[State primary sources of truth and their precedence]

## 3. Module Boundary
[Define exact bounds of control and lifecycle limits]

## 4. Non-Authority Boundary
[Explicitly disclaim approval/authorization grants]

## 5. Inputs
[List required inputs e.g., git state, checkpoints]

## 6. Outputs
[List deterministically produced outputs]

## 7. Gate List
[List all required lifecycle and safety gates]

## 8. Gate Matrix Reference
[Link or refer to the gate matrix defining rules]

## 9. Risk Profile Relation
[Map Risk Profiles to safety bounds and human requirements]

## 10. Human Checkpoint Boundary
[Define rules protecting checkpoints from simulation]

## 11. PASS / Evidence / Approval Boundary
[Define exact semantics: PASS != approval, Evidence != approval]

## 12. UNKNOWN / NOT_RUN / BLOCKED Semantics
[Define fail-closed rules: UNKNOWN != OK, NOT_RUN != PASS]

## 13. Protected / Canonical Change Rules
[Rules for modifying canonical sources]

## 14. Destructive Operation Rules
[Rules governing and forbidding destructive changes]

## 15. Lifecycle Mutation Rules
[Rules for state transitions across environments]

## 16. Non-Bypass Rules
[Rules that cannot be structurally circumvented]

## 17. Forbidden Claims
[List of claims the implementation must not make]

## 18. Required Evidence
[The exact proof necessary to pass gates]

## 19. Fail-Closed Rules
[Conditions triggering immediate BLOCKED status]

## 20. Final Invariants
[Always-on invariants including minimal safety floor]
