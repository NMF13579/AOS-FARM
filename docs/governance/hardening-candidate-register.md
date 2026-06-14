# Hardening Candidate Register

*Note: This is a register of candidates. It does NOT constitute execution authorization.*

## Category 1: Validator hardening
```yaml
candidate_id: HC-001
category: Validator hardening
source_evidence: step_10 gap review
problem_statement: Thin Validator Implementation assumes well-formed YAML and only checks structure.
risk_if_ignored: Malformed checkpoints could bypass structural checks or cause false passes.
risk_if_changed: Stricter validation might block legitimate but slightly malformed human approvals.
minimum_risk_profile: MEDIUM_RISK_CONTROLLED
requires_human_checkpoint: true
requires_protected_canonical_change: false
requires_runtime_implementation: true
requires_validator_change: true
requires_ci_change: false
recommended_next_step: Create a parser update for `validate_checkpoint.sh` to check canonical values.
not_authorized_now: true
```

## Category 2: Runtime enforcement preparation
```yaml
candidate_id: HC-002
category: Runtime enforcement preparation
source_evidence: step_11 gap review
problem_statement: Runtime enforcement is planned but not implemented (e.g., git hooks).
risk_if_ignored: Agents or humans could accidentally bypass rules without hard runtime enforcement.
risk_if_changed: Could break local dev workflows if hooks are too strict.
minimum_risk_profile: HIGH_RISK_PROTECTED
requires_human_checkpoint: true
requires_protected_canonical_change: false
requires_runtime_implementation: true
requires_validator_change: false
requires_ci_change: false
recommended_next_step: Implement local pre-push hook as described in Step 11 plan.
not_authorized_now: true
```

## Category 4: Human checkpoint consistency hardening
```yaml
candidate_id: HC-003
category: Human checkpoint consistency hardening
source_evidence: step_8 gap review
problem_statement: Human checkpoints rely entirely on text file updates and agent interpretation.
risk_if_ignored: An agent could hallucinate a PASS if the text is ambiguous.
risk_if_changed: Stricter parsing requires more rigid human input.
minimum_risk_profile: MEDIUM_RISK_CONTROLLED
requires_human_checkpoint: true
requires_protected_canonical_change: false
requires_runtime_implementation: true
requires_validator_change: true
requires_ci_change: false
recommended_next_step: Ensure thin validator checks exact YAML block matching for approvals.
not_authorized_now: true
```
