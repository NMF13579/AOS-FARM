# Roadmap Adjustment Proposal Boundary

## Principle
`Roadmap adjustment proposal ≠ roadmap mutation.`

Any change to the canonical roadmap (`01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`) or control sources requires a separate, explicit Human Checkpoint.

## Allowed Actions under this Boundary
- Proposing future roadmap adjustment candidates.
- Classifying candidates by risk.
- Indicating dependencies between proposed steps.
- Indicating the required human checkpoint for authorization.

## Forbidden Actions under this Boundary
- Modifying `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, or `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
- Modifying the active roadmap directly.
- Declaring a Build Step "complete" beyond its generated Evidence.
- Assigning `LOW_RISK_FAST` to a roadmap mutation.
- Simulating human approval for a roadmap mutation.

## Future Candidates (Proposals)
- **Candidate 1:** Insert a Build Step for "Git Hook Deployment" before proceeding to CI implementations.
  - **Risk:** `HIGH_RISK_PROTECTED`
  - **Dependency:** Step 11 (Runtime Enforcement Planning)
  - **Required Checkpoint:** Yes, explicit roadmap mutation authorization required.
