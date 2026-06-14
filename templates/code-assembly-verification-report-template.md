# Code Assembly Verification Report Template

## Verification Items
```yaml
preconditions: [STATUS]
scope_compliance: [STATUS]
diff_evidence: [STATUS]
test_evidence: [STATUS]
unknown_not_run_semantics: [STATUS]
unauthorized_change_check: [STATUS]
```

## Boundaries
```yaml
approval_boundary: "Verification PASS ≠ approval. Manual review remains required."
```

## Final Status
```yaml
final_status: [STATUS]
```

## Invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
