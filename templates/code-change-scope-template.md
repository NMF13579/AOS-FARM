# Code Change Scope Template

## Scope Definition
```yaml
in_scope_files: []
out_of_scope_files: []
allowed_change_types: []
forbidden_change_types: []
```

## Policies
```yaml
scope_expansion_policy: "Task Brief scope must not expand without explicit human permission."
protected_canonical_policy: "Requires elevated human authorization."
```

## Invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
