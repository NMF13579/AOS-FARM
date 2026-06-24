# Bootstrap Human Checkpoint

**CRITICAL INVARIANT**: Human approval cannot be simulated. The agent may propose a Risk Profile but cannot assign it as a human.

## Checkpoint Identity
- **Checkpoint ID**: [e.g., aos-farm-01-human-checkpoint]
- **Target Task**: [e.g., AOS-FARM-NEW-01]

## Human Decision Record
**Instructions for Human**: Change these fields to explicitly authorize the agent's next step.
- `checkpoint_status`: PENDING
- `execution_authorized`: false
- `commit_authorized`: false
- `push_authorized`: false
- `release_authorized`: false
- `production_use_authorized`: false
- `risk_profile_assigned_by_human`: PENDING

## Scope Constraints
- **Authorized Scope**: [Explicit list of allowed files/actions]
- **Forbidden Scope**: [Explicit list of forbidden files/actions]

## Notes
[Any specific instructions or constraints for the agent during this authorized execution]
