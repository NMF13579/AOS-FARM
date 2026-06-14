# Mandatory Pre-Final Architect/Auditor Self-Verification

## Self-Verification Checklist
- [ ] Bounded Self-Correction
- [ ] Read-Only Verification Exception
- [ ] Human Checkpoint Exception
- [ ] Commit/Push Exception
- [ ] Fail-Closed Conditions
- [ ] Forbidden Claims
- [ ] Expected Report Fields

```yaml
architect_auditor_pass_required: true
self_verification_required: true
bounded_self_correction_allowed: true
self_correction_scope: exact_allowed_files_only
scope_expansion_allowed: false
approval_simulation_allowed: false
UNKNOWN_treated_as_OK: false
NOT_RUN_treated_as_PASS: false
human_approval_required_when_applicable: true
```
