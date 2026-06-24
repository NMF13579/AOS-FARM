# Task Queue Helper Output

- **Helper Mode**: [Mode]
- **Target Task**: [Task ID]
- **Input File**: [Path]

## Validations
- **Required Fields Present**: [List]
- **Missing Fields**: [List]
- **Approval Status Summary**: [execution_authorized: true/false, commit_authorized: true/false, push_authorized: true/false]
- **Unsafe Transition Detected**: [Yes/No]

## Semantic Checks
- **UNKNOWN Status**: [Present/Absent]
- **NOT_RUN Status**: [Present/Absent]

## Outcome
- **Recommended Next Safe Step**: [Next Step]
- **Final Helper Status**: [HELPER_DRY_RUN_PASS | HELPER_BLOCKED_MISSING_APPROVAL | HELPER_BLOCKED_UNSAFE_TRANSITION | HELPER_UNKNOWN_BLOCKED]

*Note: HELPER_DRY_RUN_PASS ≠ approval.*
