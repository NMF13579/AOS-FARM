# Allowed and Forbidden Code Change Template

## Allowed
- [ALLOWED_ACTION_1]

## Forbidden
- [FORBIDDEN_ACTION_1]

## Policy
```yaml
requires_human_checkpoint: true
blocked_by_default: true
```

## Invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
