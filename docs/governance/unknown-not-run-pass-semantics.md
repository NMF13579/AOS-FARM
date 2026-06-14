# UNKNOWN / NOT_RUN / PASS Semantics

## 1. Purpose
Formalize UNKNOWN, NOT_RUN, BLOCKED, PASS, and PASS_WITH_WARNINGS semantics.

## 2. Status Vocabulary
Define strict mappings to prevent "fail-open" behaviors.

## 3. UNKNOWN Semantics
UNKNOWN indicates missing data, ambiguity, or an untested state.
UNKNOWN ≠ OK.

## 4. NOT_RUN Semantics
NOT_RUN indicates a check was explicitly skipped or not executed.
NOT_RUN ≠ PASS.

## 5. BLOCKED Semantics
BLOCKED indicates an invariant failure, missing required input, or required human intervention.
BLOCKED ≠ PASS.

## 6. PASS Semantics
PASS indicates a fully completed check with no errors.

## 7. PASS_WITH_WARNINGS Semantics
PASS_WITH_WARNINGS indicates a check completed with non-blocking issues.

## 8. Invalid Status Conversions
UNKNOWN cannot be treated as LOW_RISK or OK.
NOT_RUN cannot be used as evidence of success.

## 9. Required Fail-Closed Behavior
If an agent cannot determine a status, it must fail-closed (BLOCKED or HUMAN_REVIEW_REQUIRED).

## 10. Final Boundary Statement
Strict status semantics ensure agents cannot interpret ambiguity or missing checks as permission to proceed.
