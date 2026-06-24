# Task Status Transition Contract

## Allowed Transitions
Transitions require specific events or checkpoints.
- `DRAFT` → `READY_FOR_REVIEW`
- `READY_FOR_REVIEW` → `READY_FOR_EXECUTION`
- `READY_FOR_EXECUTION` → `HUMAN_REVIEW_REQUIRED`
- `HUMAN_REVIEW_REQUIRED` → `EXECUTION_AUTHORIZED` (only after Human execution checkpoint)
- `EXECUTION_AUTHORIZED` → `IN_PROGRESS`
- `IN_PROGRESS` → `RESULT_REPORTED`
- `RESULT_REPORTED` → `VERIFICATION_PENDING`
- `VERIFICATION_PENDING` → `VERIFIED` or `BLOCKED`
- `VERIFIED` → `COMMIT_AUTHORIZATION_PENDING`
- `COMMIT_AUTHORIZATION_PENDING` → `COMMITTED` (only after Human Commit Authorization)
- `COMMITTED` → `PUSH_AUTHORIZATION_PENDING`
- `PUSH_AUTHORIZATION_PENDING` → `PUSHED` (only after Human Push Authorization)
- `PUSHED` → `CLOSED` (after remote baseline closure report)

## Forbidden Transitions
- `DRAFT` → `IN_PROGRESS` without authorization.
- `READY_FOR_EXECUTION` → `IN_PROGRESS` without Human checkpoint.
- `VERIFIED` → `COMMITTED` without Human Commit Authorization.
- `COMMITTED` → `PUSHED` without Human Push Authorization.
- `UNKNOWN_BLOCKED` → `VERIFIED` without evidence.
- `NOT_RUN` → `PASS`.
- `PASS` → `approval` (PASS never equates to approval).
- `Evidence` → `approval`.
