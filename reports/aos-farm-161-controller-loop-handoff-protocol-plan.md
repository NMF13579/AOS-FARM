# Controller Loop Handoff Protocol Plan

## Scope
Minimal implementation scope for future AOS-FARM.163. The protocol must reduce manual relay by requiring every controlled task to produce a machine-readable next-action handoff.

## Allowed Files
The future implementation may create/modify only these files:
- docs/operations/controller-loop-handoff-protocol.md
- templates/controller-loop-next-action-handoff-template.md
- templates/controller-loop-final-report-routing-template.md
- reports/aos-farm-163-controller-loop-handoff-protocol-execution-report.md

## Handoff Flow
Task execution
→ final report
→ next-action handoff file
→ Controller reads handoff
→ Controller determines safe next task
→ if human checkpoint is required, stop and request human approval
→ if authorization already exists, continue only within authorized scope

## Invariants Preserved
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

## Protocol Status
Controller Loop Handoff Protocol is not runtime enforcement yet.
Controller Loop Handoff Protocol is not autonomous approval.
Controller Loop Handoff Protocol does not bypass human checkpoints.
Controller Loop Handoff Protocol does not authorize commit or push.
Controller Loop Handoff Protocol reduces manual relay by standardizing machine-readable next-action handoff.
