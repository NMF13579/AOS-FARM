# Minimal Safety Floor Checklist Template

## 1. Task Identity
- Task ID: 
- Task Name: 

## 2. Required Sources Checked
- 00_AOS_Core_Control.md: 
- 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md: 
- 02_AOS_Governance_Control_Module_and_Safety_Rules.md: 

## 3. Approval Boundary Checks
- PASS ≠ approval.
- CI PASS ≠ approval.
- Verification PASS ≠ approval.
- Human approval cannot be simulated.

## 4. Evidence Boundary Checks
- Evidence ≠ approval.

## 5. PASS Boundary Checks
- PASS claimed as approval: false

## 6. UNKNOWN / NOT_RUN Checks
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.

## 7. Human Checkpoint Checks
- Explicit human checkpoints verified where required.

## 8. Protected / Canonical Checks
- Protected / Canonical change explicitly authorized.

## 9. Destructive Operation Checks
- Destructive operation explicitly authorized.

## 10. Commit / Push / Release Checks
- Execution authorization ≠ commit authorization.
- Commit authorization ≠ push authorization.
- Push authorization ≠ release authorization.

## 11. Risk Profile Checks
- Human assigned Risk Profile verified.

## 12. Final Checklist Result

```yaml
required_sources_available: unknown
pass_claimed_as_approval: false
evidence_claimed_as_approval: false
ci_pass_claimed_as_approval: false
verification_pass_claimed_as_approval: false
unknown_treated_as_ok: false
not_run_treated_as_pass: false
human_approval_simulated: false
protected_canonical_change_detected: unknown
destructive_operation_detected: false
commit_authorized: false
push_authorized: false
release_authorized: false
production_use_authorized: false
agent_risk_profile_assignment_performed: false
human_risk_profile_assignment_required: unknown
final_checklist_result: UNKNOWN
```
