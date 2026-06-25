# Human Checkpoint Structure

A standard human checkpoint ensures decisions are documented and verifiable.

## Checkpoint Components
1. **Target Task**: The specific execution or commit being authorized.
2. **Constraints**: Clear rules the agent must follow during execution.
3. **Risk Profile**: The impact classification (must be assigned by the human).
4. **Decision Block**: An explicit set of checkboxes (`APPROVED`, `REJECTED`, `CHANGES REQUESTED`).
5. **Signature**: A marker indicating who authorized it and when.

Agents must read the filled checkpoint file before proceeding to verify the `[x] APPROVED` status.
