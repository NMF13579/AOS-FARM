# Hardening Candidate Register Template

*Note: Template ≠ implementation. Candidate ≠ authorized change.*

```yaml
candidate_id: HC-XXX
category: [Validator hardening | Runtime enforcement | etc]
source_evidence: [Link or reference to evidence]
problem_statement: [What is the gap?]
risk_if_ignored: [Impact of doing nothing]
risk_if_changed: [Impact/Risk of implementing the fix]
minimum_risk_profile: [e.g., HIGH_RISK_PROTECTED]
requires_human_checkpoint: true
requires_protected_canonical_change: [true/false]
requires_runtime_implementation: [true/false]
requires_validator_change: [true/false]
requires_ci_change: [true/false]
recommended_next_step: [Proposed action]
not_authorized_now: true
```
