# Manual Code Review Checkpoint Template

## 1. Checkpoint Status
```yaml
checkpoint_status: PENDING_HUMAN_REVIEW
human_review_completed: false
approval_recorded: false
commit_authorized: false
push_authorized: false
release_authorized: false
production_use_authorized: false
```

## 2. Invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
