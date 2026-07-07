# AOS-FARM.629 — Architecture-to-Task Export Plan

This report is planning Evidence.
This report is not canonical workflow documentation.
This report is not a route update.
This report does not change Task Brief requirements.
This report does not authorize implementation.
Any future canonical adoption requires separate human-approved scope.

## 1. Status

* Planning Status: READY_FOR_HUMAN_REVIEW
* Implementation Status: NOT_AUTHORIZED
* Canonical Status: NOT_CANONICAL
* Task Brief Creation Status: NOT_AUTHORIZED
* Build Step Execution Status: NOT_AUTHORIZED
* AOS-FARM.630 Execution: NOT_AUTHORIZED

## 2. Repository State

* branch: build/aos-farm-629-architecture-to-task-export-planning
* HEAD short: e5015e7
* HEAD full: e5015e71efde0e298c2dcdc55705260533678f88
* origin/dev short: e5015e7
* origin/dev full: e5015e71efde0e298c2dcdc55705260533678f88
* origin/main short: 2557721
* origin/main full: 25577219c33fb2a9e91bc188eb660276b21f57e5
* origin/dev...HEAD: 0 0
* expected origin/dev after AOS-FARM.628 short: e5015e7
* expected origin/dev after AOS-FARM.628 full: e5015e71efde0e298c2dcdc55705260533678f88
* tracked worktree: clean
* untracked files: .venv/, aos/reports/dogfood/aos-farm-621-architecture-evidence-packet-dogfood 2.md

## 3. Source Decision

* AOS-FARM.628 checkpoint packet: aos/reports/architecture/aos-farm-628-human-architecture-checkpoint.md
* AOS-FARM.628 decision record: aos/reports/architecture/aos-farm-628-human-architecture-decision-record.md
* checkpoint packet source: immutable baseline SHA
* decision record source: immutable baseline SHA
* immutable baseline SHA: e5015e71efde0e298c2dcdc55705260533678f88
* origin/dev matched immutable baseline: yes
* architecture checkpoint result: ARCHITECTURE_APPROVED
* downstream planning allowed: true
* implementation authorized: false
* release authorized: false
* merge to main authorized: false
* AOS-FARM.630 execution authorized: false
* automatic next-stage start: false

## 4. Source of Truth Boundary

This report is not a canonical Source of Truth.
This report does not change workflow or route files.

## 5. Boundary

* PASS converted to approval: no
* Evidence converted to approval: no
* Architecture approval converted to implementation authorization: no
* downstream planning converted to READY_FOR_EXECUTION: no
* export plan converted to implementation: no
* Task Brief input fields converted to Task Brief creation: no
* Task Brief readiness converted to approval: no
* Task Brief completeness converted to implementation authorization: no
* Architecture-to-Task export completeness converted to READY_FOR_EXECUTION: no
* Task Brief candidate converted to Build Step execution: no
* report treated as canonical Source of Truth: no
* report treated as implementation spec: no
* implementation authorized: no
* release authorized: no
* merge to main authorized: no
* AOS-FARM.630 execution authorized: no
* automatic next-stage start: no
* human approval simulated: no

## 6. Inputs Reviewed

* aos/reports/architecture/aos-farm-628-human-architecture-checkpoint.md
* aos/reports/architecture/aos-farm-628-human-architecture-decision-record.md
* aos/START_HERE.md
* aos/docs/ROUTES.md
* aos/docs/workflow/architecture-input-intake.md
* aos/docs/workflow/architecture-decision-layer.md
* aos/docs/architecture/review/architecture-decision-evidence-packet.md
* aos/docs/architecture/review/human-architecture-checkpoint-template.md

## 7. Architecture Outputs Eligible for Export

* Architecture inputs mapped to Task Brief requirements
* Context references from ADRs
* Downstream constraints specified in architecture reviews

## 8. Evidence-Only Items

* validator output
* architecture Evidence Packet
* checkpoint packet
* agent recommendation
* current baseline rerun
* accepted warning list
* discovery command output
* AOS-FARM.627 missing persisted report gap

## 9. Human Decision-Only Items

* Risk Profile assignment
* architecture approval
* downstream planning permission
* Task Brief approval
* implementation authorization
* commit authorization
* push authorization
* release authorization
* merge to main authorization
* AOS-FARM.630 execution authorization
* retirement or resolution of carry-forward gaps

## 10. Deferred Warnings and Gaps

| Warning / Gap | Source | Carry Forward? | Downstream Impact | Required Handling |
|---|---|---|---|---|
| AOS-FARM.627 persisted validator result file missing | AOS-FARM.628 | yes | Must remain visible until explicitly resolved or retired by human | Do not convert to PASS/Evidence/approval |

## 11. Proposed Architecture-to-Task Export Contract

```yaml
architecture_to_task_export_contract:
  source_inputs:
    - architecture checkpoint packet
    - architecture decision record
    - ADRs and registries
  exported_fields:
    - architecture_context
    - selected_pattern_or_approach
    - constraints
    - non_goals
    - risks
    - accepted_tradeoffs
    - open_questions
    - deferred_items
    - validation_baseline
    - human_decision_reference
  evidence_references:
    - validator results
    - dogfood evidence
  human_decision_references:
    - explicit human architecture approval record
  deferred_warnings:
    - AOS-FARM.627 persisted validator result file missing
  downstream_planning_constraints:
    - scope must not expand without human permission
    - destructive operations forbidden by default
  forbidden_exports:
    - architecture approval as implementation authorization
    - architecture approval as Task Brief approval
    - architecture approval as Build Step approval
    - validator PASS as approval
    - Evidence as approval
    - checkpoint packet as approval
    - recommendation as decision
    - downstream planning allowed as READY_FOR_EXECUTION
    - Task Brief input fields as Task Brief creation
    - Task Brief readiness as approval
    - Task Brief completeness as implementation authorization
    - Architecture-to-Task export completeness as READY_FOR_EXECUTION
    - Task Brief candidate as approved Build Step
    - accepted warning as resolved warning
    - missing report as PASS
    - missing report as Evidence
    - missing report as approval
    - planning report as canonical Source of Truth
    - planning report as route update
    - planning report as workflow update
  required_gates_before_task_execution:
    - Task Brief creation and approval
    - Build Step approval
    - implementation authorization
  required_human_checkpoints:
    - Task Brief approval
    - Build Step authorization
```

## 12. Lifecycle Transition Map

| From State | To State | Allowed? | Required Gate | Forbidden Interpretation |
|---|---|---|---|---|
| ARCHITECTURE_APPROVED | Architecture-to-Task Export Plan | yes | None (Export Planning) | Export Plan \u2260 Canonical docs |
| Architecture-to-Task Export Plan | Task Brief Draft | yes | Human Export Approval | Task Brief Draft \u2260 Execution ready |
| Task Brief input fields | Task Brief creation | no | Human Task Brief Creation Action | Input fields \u2260 Task Brief |
| Task Brief Draft | Task Brief readiness | no | Validator PASS + Human Review | Draft \u2260 Task Brief readiness |
| Task Brief readiness | Build Step planning | no | Human Task Brief Approval | Readiness \u2260 Build Step planning |
| Validator PASS | Task Brief Approval | no | Human Approval Checkpoint | Validator PASS \u2260 Approval |
| Export contract complete | READY_FOR_EXECUTION | no | Implementation Authorization | Export completeness \u2260 Execution |
| AOS-FARM.629 report | Canonical workflow docs | no | Explicit Canonical Update Task | Report \u2260 Workflow update |
| AOS-FARM.629 recommendation | AOS-FARM.630 execution | no | AOS-FARM.630 Authorization | Recommendation \u2260 Execution |

## 13. Task Brief Integration Plan

The architecture-to-task export contract will govern how architecture constraints are passed as read-only references into future Task Briefs.

## 14. Build Step Planning Impact

Build Steps must explicitly cross-reference the required constraints passed through the export contract.

## 15. AOS-FARM.630 Recommendation Candidates

Recommended next stage type: HUMAN_REVIEW_REQUIRED

AOS-FARM.630 should not be selected until this revised AOS-FARM.629 report is reviewed by human.
Do not claim AOS-FARM.630 implementation is authorized.

## 16. AOS-FARM.630 Candidate Classification Rule

* If export contract is clear and human accepts it: IMPLEMENTATION_CANDIDATE
* If export contract has unresolved gaps: REVISION_CANDIDATE
* If implementation would require docs/templates/scripts/tests in one stage: SPLIT_REQUIRED
* If acceptance or safety is unclear: HUMAN_REVIEW_REQUIRED

## 17. Human Review Questions

1. Does the proposed export contract accurately reflect the boundaries for downstream planning?
2. Are there any other forbidden exports that should be explicitly listed?
3. Should AOS-FARM.630 be split into separate documentation and template implementation stages?

## 18. Final Status

* Planning Status: READY_FOR_HUMAN_REVIEW
* Implementation Status: NOT_AUTHORIZED
* Canonical Status: NOT_CANONICAL
* Task Brief Creation Status: NOT_AUTHORIZED
* Build Step Execution Status: NOT_AUTHORIZED
* AOS-FARM.630 Execution: NOT_AUTHORIZED
