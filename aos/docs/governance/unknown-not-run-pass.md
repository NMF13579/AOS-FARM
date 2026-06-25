# Strict Failure Semantics

AOS enforces fail-closed semantics to prevent runaway AI execution.

## UNKNOWN ≠ OK
If an agent cannot verify a file's state, cannot find a required source, or receives an ambiguous response, it must treat the situation as blocked. It cannot assume "it's probably fine."

## NOT_RUN ≠ PASS
If a required validation step, preflight check, or test is skipped or fails to execute, the result is considered a failure. The agent cannot proceed under the assumption that an un-run test implies a passing state.
