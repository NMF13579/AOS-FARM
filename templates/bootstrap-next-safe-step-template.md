# Bootstrap Next Safe Step

**AGENT INSTRUCTION**: Use this template to determine and present the safest next step to the user. Do not execute the step until explicitly authorized. 
Remember: `UNKNOWN ≠ OK`, `NOT_RUN ≠ PASS`, `PASS ≠ approval`, `Evidence ≠ approval`.

## Status Verification
- **Current State**: [Brief description]
- **Last Closed Stage**: [ID of the last stage with push/remote closure]
- **Open Work**: [Any uncommitted or unpushed work on the current branch?]
- **Required Sources Available**: [Yes/No - Check `00`, `01`, `02`]
- **Human Approval Status**: [Is there a pending checkpoint blocking continuation?]
- **Known Blockers**: [Any errors, missing approvals, or ambiguity?]

## Proposed Next Action
- **Candidate Next Step**: [e.g., Task ID and description]
- **Risk Profile Proposal**: [e.g., LOW_RISK_FAST, MEDIUM_RISK_GUIDED]
- **Why This Step Is Safe**: [Justification based on scope and boundaries]

## Boundaries
- **What Must Not Be Done**: [Explicit forbidden actions during this step]
- **Stop Condition**: [When should the agent stop and ask for human review?]
