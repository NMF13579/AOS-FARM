# Post-Execution Verification

- **Verification ID**: [ID]
- **Target Task ID**: [Task ID]
- **Target Execution Report**: [Reference]
- **Verifier**: [Agent/Human]
- **Verification Mode**: Read-only verification

## Checks
- **Required Sources Checked**: [List `00`, `01`, `02`]
- **Expected Files**: [List]
- **Actual Files**: [List]
- **Unauthorized Files**: [List]

## Validations
- **Scope Compliance**: [Pass/Fail]
- **Forbidden Operation Check**: [Pass/Fail]
- **Approval Boundary Check**: [Pass/Fail]
- **UNKNOWN Check**: [List explicitly]
- **NOT_RUN Check**: [List explicitly]
- **Evidence Check**: [Pass/Fail]
- **Commit/Push Check**: [Pass/Fail - verify no unauthorized commits]

## Findings
- **Blocking Issues**: [List]
- **Warnings**: [List]

## Outcome
- **Verification Result**: [VERIFICATION_PASS | VERIFICATION_PASS_WITH_WARNINGS | VERIFICATION_BLOCKED | UNKNOWN_BLOCKED]
- **Next Safe Step**: [Wait for Human Commit Authorization or Fix Issues]

*Note: VERIFICATION_PASS ≠ approval. VERIFICATION_PASS_WITH_WARNINGS ≠ approval.*
