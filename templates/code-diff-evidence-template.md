# Code Diff Evidence Template

## Diff Data
```yaml
changed_files: []
diff_summary: [SUMMARY]
```

## Test Data
```yaml
test_commands: []
test_results: []
not_run_items: []
unknown_items: []
```

## Limitations & Boundaries
```yaml
evidence_limitations: [LIMITATIONS]
approval_boundary: "Diff is Evidence, not approval. Test output is Evidence, not approval. Manual review remains required."
```

## Invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
