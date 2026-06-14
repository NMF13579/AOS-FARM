# Controller Loop Handoff Protocol

## 1. Purpose
Reduce manual relay between ChatGPT and the IDE agent by defining a machine-readable task-to-task handoff protocol.

## 2. Problem Statement
The user currently manually transfers outputs. Architect/Auditor Mode improves single-task self-checking but lacks task-to-task automation.

## 3. Authority and Source Precedence
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

## 4. Operating Formula
Task completion requires a machine-readable final report routing and a next-action handoff file to inform the next agent session.

## 5. Handoff Flow
Task execution
→ final report
→ next-action handoff file
→ Controller reads handoff
→ Controller determines safe next task
→ if human checkpoint is required, stop and request human approval
→ if authorization already exists, continue only within authorized scope

## 6. Task Final Report Requirement
Tasks must produce a final report defining execution state, issues, and routing recommendation.

## 7. Next-Action Handoff Requirement
Tasks must produce a dedicated handoff file if a subsequent action is intended.

## 8. Controller Read Step
The new session must read the handoff file before executing the next task.

## 9. Safe Next Task Selection
Next task depends on handoff status and approval boundaries.

## 10. Human Checkpoint Boundary
If the next action requires protected/canonical changes, commit, push, release, or execution authorization, human checkpoint is mandatory.

## 11. Approval Boundary
Human approval cannot be simulated.

## 12. Risk Profile Boundary
Risk Profile cannot be assigned by agent as human.

## 13. Commit / Push Boundary
Protocol does not authorize commit or push.

## 14. Runtime Boundary
Controller Loop Handoff Protocol is not runtime enforcement yet.

## 15. Validator Boundary
Does not implement deterministic validator logic.

## 16. UNKNOWN / NOT_RUN Boundary
UNKNOWN ≠ OK
NOT_RUN ≠ PASS

## 17. PASS / Evidence / CI PASS Boundary
PASS ≠ approval
Evidence ≠ approval
CI PASS ≠ approval

## 18. Manual Relay Reduction
Reduces manual relay by standardizing machine-readable next-action handoff.

## 19. Machine-Readable Handoff Fields
Defines YAML schema for handoff status, branches, scopes, and warnings.

## 20. Allowed Next Action Types
Lists specific verification, execution, and authorization action types.

## 21. Blocked / Human Review Routing
BLOCKED or UNKNOWN must route to blocked or human review.

## 22. Relationship to Architect/Auditor Mode
Relies on Architect/Auditor verification before issuing handoff.

## 23. Relationship to IDE Architect Controller Mode
Mechanizes the Controller's routing decision step.

## 24. Relationship to Governance / Control Module
Enforces the safety gates structurally across sessions.

## 25. Future Runtime Extension
Will evolve into deterministic automated loop.

## 26. Examples
Task completes → creates handoff recommending commit authorization → stops.

## 27. Final Invariants
Controller Loop Handoff Protocol is not runtime enforcement yet.
Controller Loop Handoff Protocol is not autonomous approval.
Controller Loop Handoff Protocol does not bypass human checkpoints.
Controller Loop Handoff Protocol does not authorize commit or push.
Controller Loop Handoff Protocol reduces manual relay by standardizing machine-readable next-action handoff.
PASS ≠ approval
Evidence ≠ approval
CI PASS ≠ approval
UNKNOWN ≠ OK
NOT_RUN ≠ PASS
Human approval cannot be simulated
Risk Profile cannot be assigned by agent as human
Scope must not expand without explicit human permission
Protected/canonical changes require human checkpoint
Destructive operations are forbidden by default
