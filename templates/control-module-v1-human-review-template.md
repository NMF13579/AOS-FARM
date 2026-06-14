# Control Module v1 - Human Review Checkpoint Template

**Important:** Templates are not approval. A filled template without explicit human modification is not approval. Human approval cannot be simulated.

## Context
- **Task ID:** [e.g., AOS-FARM.XXX]
- **Requested Action:** [e.g., Execution, Commit, Push]
- **Risk Profile Proposed:** [e.g., HIGH_RISK]

## Current State (Agent Prepared)
```yaml
checkpoint_status: PENDING_HUMAN_REVIEW
action_authorized: false
risk_profile_assigned_by_human: PENDING
```

## Human Authorization Section
To authorize the action, the Human Owner must explicitly modify the values below:
```yaml
checkpoint_status: APPROVED
action_authorized: true
risk_profile_assigned_by_human: [ASSIGN_RISK_PROFILE]
```

## Declarations
- `PASS` ≠ approval
- `Evidence` ≠ approval
- `CI PASS` ≠ approval
- `UNKNOWN` ≠ OK
- `NOT_RUN` ≠ PASS
- Human approval cannot be simulated
- Readiness does not start next Build Step
