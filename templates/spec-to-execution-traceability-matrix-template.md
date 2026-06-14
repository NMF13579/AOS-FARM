# Spec-to-Execution Traceability Matrix

## Matrix

| requirement_id | source_reference | spec_section | plan_section | task_id | output_artifact | verification_evidence | status | unknowns | human_review_required |
|---|---|---|---|---|---|---|---|---|---|
| [ID] | [Source] | [Spec] | [Plan] | [Task] | [Artifact] | [Evidence] | [TRACEABLE | PARTIAL | MISSING | UNKNOWN_BLOCKED | HUMAN_REVIEW_REQUIRED] | [List unknowns] | [Yes/No] |

## AOS Invariants
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
Verification PASS ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
Human approval cannot be simulated.
Execution authorization preparation ≠ execution authorization.
Execution authorization ≠ commit authorization.
Commit authorization ≠ push authorization.
Spec Kit pattern reference ≠ Spec Kit dependency.
Spec Kit guidance ≠ AOS governance authority.
Documentation output ≠ approval.
Documentation output ≠ release.
