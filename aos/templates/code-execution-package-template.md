# Code Execution Package

## 1. Task Brief Reference
- **Task ID**: [insert task ID]
- **Risk Profile**: [insert explicitly assigned risk profile]

## 2. Execution Claims
- [ ] Claim: Execution matches Task Brief scope exactly. No scope expansion occurred.
- [ ] Claim: No protected/canonical files modified (unless explicitly authorized).
- [ ] Claim: No approval is simulated. 

## 3. Changed Files
```yaml
changes:
  - file_path: ""
    change_type: "MODIFY / ADD / DELETE"
```

## 4. Overengineering Controls
```yaml
overengineering_controls:
  expected_change_size: small
  max_touched_files_soft:
  max_new_files_soft:
  max_added_lines_soft:
  max_new_dependencies: 0
  max_new_classes_soft:
  max_new_functions_soft:
  architecture_change_allowed: false
  future_only_code_allowed: false
  scope_expansion_allowed: false
  validator_semantics_change_allowed: false
  validator_reporting_extension_allowed: false
  lifecycle_semantics_change_allowed: false
  protected_canonical_change_allowed: false
  compression_review_required: true
  simpler_alternative_required: true
```

## 4. Evidence
- [ ] Diff included or linked.
- [ ] Relevant tests executed and outputs provided.
- [ ] All validators passed.

*Note: Evidence ≠ approval. CI PASS ≠ approval.*

## 5. Quality Control Status
`CODE_QUALITY_REPORTED_HUMAN_REVIEW_REQUIRED` (or `CODE_QUALITY_BLOCKED`)
