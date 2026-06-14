# PASS / Evidence / Approval Boundary

## 1. Purpose
Clarify the separation between PASS, Evidence, CI PASS, Verification PASS, and human approval.

## 2. PASS Is a Validation Result
PASS means a specific condition was met during an automated or manual check. PASS ≠ approval.

## 3. Evidence Is a Supporting Artifact
Evidence means artifacts exist showing the results of work. Evidence ≠ approval.

## 4. CI PASS Is Not Human Approval
A successful Continuous Integration pipeline run means automated tests passed. CI PASS ≠ approval.

## 5. Verification PASS Is Not Human Approval
Passing a verification check verifies state, but does not grant permission to mutate lifecycle. Verification PASS ≠ approval.

## 6. Human Approval Requirements
Only an explicit, intentional human decision can serve as approval.

## 7. Forbidden Substitutions
Human approval cannot be simulated.
Human approval cannot be inferred.
Human approval cannot be replaced by agent text.

## 8. Valid Decision Chain
Action -> Verification -> Evidence -> Human Review -> Human Approval -> Execution/Commit

## 9. Invalid Decision Chains
Action -> Verification PASS -> Execution (Invalid)
Action -> Evidence Exists -> Execution (Invalid)

## 10. Final Boundary Statement
The lines between passing tests, generating evidence, and receiving human authorization are strictly separated. No amount of successful verification can substitute for human approval.
