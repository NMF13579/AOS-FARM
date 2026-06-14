# AOS-FARM Task Verification Checker Contract

## 1. Purpose
Compare an agent task report against repo evidence, expected task spec, allowed files, required files, git state, checkpoint state, and authorization boundaries.

## 2. Non-authority Boundary
The checker must not produce:
- approval
- execution authorization
- commit authorization
- push authorization
- release authorization
- production authorization
- human decision

## 3. Input Model
Dictates expected repo state, task scope, allowed/forbidden files, required files, and required boolean states via a deterministic template schema.

## 4. Evidence Model
Reconstructs truth purely from git state, file system state, and checkpoint file parsing, treating agent task reports as claims rather than ground truth.

## 5. Verification Model
Strictly compares the Input Model against the Evidence Model. Any deviation or ambiguity fails closed.

## 6. Output Model
Emits a standard structured YAML/Markdown report detailing individual checks, overall verification status, and final recommendation.

## 7. PASS Semantics
Verification successfully confirmed all expected constraints and boundaries. PASS ≠ approval.

## 8. PASS_WITH_WARNINGS Semantics
Verification succeeded but encountered non-blocking anomalies. Does not lower safety requirements.

## 9. BLOCKED Semantics
Verification failed due to a constraint violation, unauthorized modification, or broken boundary.

## 10. UNKNOWN Semantics
Verification cannot be completed due to missing evidence or unparseable state. UNKNOWN ≠ OK.

## 11. Authorization Boundary
The checker verifies if an authorization state exists in the repository, but it can never grant authorization itself.

## 12. Human Checkpoint Boundary
The checker can read human checkpoints but cannot write, simulate, or bypass them. Human approval cannot be simulated.

## 13. Risk Profile Boundary
The checker observes the assigned Risk Profile but cannot assign or alter it.

## 14. File Scope Verification
Compares exactly allowed created/modified files against the working tree and commit history. Checks for forbidden files.

## 15. Git State Verification
Verifies branch name, HEAD hash, origin/dev hash, and remote baseline closure (ahead/behind counts).

## 16. Required Source Verification
Ensures fundamental control files (00_AOS_Core_Control.md, 01, 02, AGENTS.md) are present and unmodified unless explicitly authorized.

## 17. Forbidden Operation Verification
Verifies that no unauthorized git operations (stage, commit, push), CI modifications, runtime implementations, or validator implementations occurred.

## 18. Checkpoint State Verification
Ensures the state inside human checkpoints exactly matches expected values (e.g., PENDING_HUMAN_DECISION).

## 19. Claim-vs-evidence Comparison
Validates that the agent report (claim) exactly reflects the repository reality (evidence).

## 20. Fail-closed Rules
Fail closed if any evidence is missing, any constraint is broken, any unauthorized file is seen, or any verification check resolves to UNKNOWN or BLOCKED.

## 21. Exit Code Recommendation
Future implementations should use exit code 0 for PASS or PASS_WITH_WARNINGS, and non-zero (e.g., 1) for BLOCKED or UNKNOWN.

## 22. Future Implementation Constraints
Future implementation must require a separate human-authorized task, preferably under Thin Validator Contract / Thin Validator Implementation.
