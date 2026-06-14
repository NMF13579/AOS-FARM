# Governance / Control Module Contract

## 1. Purpose
This contract establishes the definitive rules for AgentOS governance, risk management, and the control module, ensuring absolute safety boundaries and human oversight.

## 2. Authority and Source Precedence
Source precedence: `00_AOS_Core_Control.md` > `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` > `02_AOS_Governance_Control_Module_and_Safety_Rules.md`. 
Domain authority: `01` governs the roadmap and daily workflow; `02` governs safety, gates, and approval boundaries.

## 3. Module Boundary
The control module dictates all lifecycle phases of an agent execution, ensuring safety checkpoints cannot be bypassed.

## 4. Non-Authority Boundary
This contract does not grant approval. It does not authorize execution, commit, push, release, or production use.

## 5. Governance / Control Module Inputs
Authorized human checkpoints, repository artifacts, verified git state, and control module configuration documents.

## 6. Governance / Control Module Outputs
Deterministic verification states, blocking indicators, or read-only execution reports.

## 7. Gate List
- source availability gate
- source precedence gate
- scope boundary gate
- risk profile gate
- human checkpoint gate
- approval boundary gate
- evidence boundary gate
- PASS semantics gate
- UNKNOWN / NOT_RUN gate
- protected/canonical change gate
- destructive operation gate
- lifecycle mutation gate
- runtime implementation gate
- validator implementation gate
- CI workflow gate
- commit gate
- push gate
- release gate
- production use gate
- controller loop stop gate

## 8. Gate Semantics
Gates enforce mechanical blocking of unauthorized states or boundary violations prior to any operation phase.

## 9. Risk Profile Relation
- **LOW_RISK_FAST:** Automatically or lightly gated execution for non-sensitive changes. Cannot be self-assigned by the agent.
- **MEDIUM_RISK_GUIDED:** Requires bounded execution, verified human checkpoints before execution and push.
- **HIGH_RISK_PROTECTED:** Explicitly controls governance rules, safety bounds, validators, or destructive changes.

## 10. Human Checkpoint Boundary
Checkpoints strictly record explicit human decisions. Human approval cannot be simulated.

## 11. PASS / Evidence / Approval Boundary
PASS ≠ approval. Evidence ≠ approval. CI PASS ≠ approval.

## 12. UNKNOWN / NOT_RUN / BLOCKED Semantics
UNKNOWN ≠ OK. NOT_RUN ≠ PASS. BLOCKED ≠ PASS.

## 13. Protected / Canonical Change Boundary
Protected/canonical changes require an explicit human checkpoint.

## 14. Destructive Operation Boundary
Destructive operations are forbidden by default.

## 15. Lifecycle Boundary
Transitions between execution, commit, push, and release strictly demand explicit human lifecycle checkpoints.

## 16. Non-Bypass Rules
Scope must not expand without explicit human permission. Checkpoints must not be simulated or bypassed.

## 17. Controller Loop Relation
The Controller Loop evaluates next safe tasks based on evidence without auto-approving blocked gates.

## 18. Validator / Runtime Relation
This contract defines documentation rules. It does not implement runtime enforcement or validators.

## 19. CI Relation
This contract defines boundaries but does not modify CI workflows.

## 20. Forbidden Claims
The contract does not claim: runtime enforcement is implemented, validator is implemented, CI gate is active, production use is authorized, release is authorized, commit is authorized, push is authorized, PASS grants approval, Evidence grants approval, CI PASS grants approval, agent can simulate human approval, agent can assign Risk Profile as human, agent can assign LOW_RISK_FAST.

## 21. Required Evidence
Verifiable git state, file contents, and human checkpoints must perfectly reflect constraints.

## 22. Fail-Closed Rules
Any ambiguity, unknown state, missing evidence, or human unavailability for a required review/checkpoint/Risk Profile assignment dictates a fail-closed status: BLOCKED or HUMAN_REVIEW_REQUIRED.

## 23. Out-of-Scope Items
Implementing the runtime verification engine or validators.

## 24. Future Implementation Notes
Validators and runtime checks will mechanize these boundaries in future dedicated steps.

## 25. Final Invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- BLOCKED ≠ PASS.
- Human approval cannot be simulated.
- Skeleton ≠ implementation.
- Scope must not expand without explicit human permission.
- Protected/canonical changes require human checkpoint.
- Destructive operations are forbidden by default.
- Minimal Safety Floor is always-on.
- Human unavailable for required review/approval/checkpoint/Risk Profile assignment → BLOCKED or HUMAN_REVIEW_REQUIRED.
- Agent may propose Risk Profile, but may not assign LOW_RISK_FAST.
