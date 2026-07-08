# AOS-FARM.640 — Legacy Blocker Exclusion Decision Record

## 1. Decision problem

Record the decision framework for how future terminal and legacy exclusion semantics should treat the current readiness blockers without closing them in AOS-FARM.640.

## 2. Why AOS-FARM.639 could not resolve blockers

AOS-FARM.639 could not legally resolve the blockers because the current system has no safe exclusion model.

Current constraints:

- `task --readiness-all` inspects every `tasks/*.md`.
- `REJECTED` and `CLOSED` do not bypass readiness checks.
- `RETIRED` and `SUPERSEDED` are not legal task-header statuses.
- `AOS-FARM.463` fails `task_id` validation before any hypothetical terminal handling.
- Current readiness has no `EXCLUDED_TERMINAL` or `EXCLUDED_LEGACY` concept.

## 3. Current blocker table

| Blocker id | Current issue | Proposed future treatment | Closed in 640 |
|---|---|---|---:|
| AOS-FARM-TASK-0001 | `risk_profile: UNKNOWN_BLOCKED`, `approval_status: NOT_APPROVED`, `execution_authorized` not true, `validator_status: NOT_RUN`, `evidence_status: NOT_RUN` | Remain active blocker unless future human decision plus future implementation produce either real active readiness work or valid terminal witness. | no |
| AOS-FARM-TASK-060101 | Human-assigned `HIGH_RISK_PROTECTED`, but still `NOT_APPROVED`, not execution-authorized, `validator_status: NOT_RUN`, `evidence_status: NOT_RUN` | Remain active blocker unless future human decision and future implemented semantics classify it through a witnessed terminal disposition. | no |
| AOS-FARM-TASK-060102 | `risk_profile: UNKNOWN_BLOCKED`, `risk_assigned_by: none`, `approval_status: NOT_APPROVED`, `validator_status: NOT_RUN`, `evidence_status: NOT_RUN` | Remain active blocker; human risk assignment alone is not closure. Future terminal exclusion is possible only with explicit witnessed disposition. | no |
| AOS-FARM.463 | Invalid legacy `task_id`, `risk_assigned_by: none`, `approval_status: NOT_APPROVED`, `validator_status: NOT_RUN`, `evidence_status: NOT_RUN` | Candidate for future `EXCLUDED_LEGACY` only through explicit quarantine witness after separate implementation. | no |

## 4. Treatment of each current blocker

### 4.1 AOS-FARM-TASK-0001

Current state is ordinary active-task blockage, not legacy formatting failure.

Future treatment:

- remain active unless normal task remediation occurs; or
- become `EXCLUDED_TERMINAL` only if future human witness explicitly records a terminal disposition and dependency review passes.

### 4.2 AOS-FARM-TASK-060101

Current state proves that human-assigned risk alone does not equal readiness.

Future treatment:

- remain active unless future execution/evidence work occurs; or
- become `EXCLUDED_TERMINAL` only through explicit terminal witness with no approval simulation.

### 4.3 AOS-FARM-TASK-060102

Current state proves that fixing only one component, such as risk assignment, does not close readiness.

Future treatment:

- remain active blocker by default;
- future human risk assignment can remove only the risk ambiguity component;
- terminal exclusion requires separate explicit witnessed disposition.

### 4.4 AOS-FARM.463

Current state is special because it is both active-blocked and structurally non-conforming.

Future treatment:

- must not be silently accepted as a valid task id;
- must stay visible in audit output;
- may become `EXCLUDED_LEGACY` only through explicit per-task quarantine witness;
- otherwise remains blocker.

## 5. Special handling for AOS-FARM.463

`AOS-FARM.463` requires dedicated legacy handling because:

- `task_id` format is invalid under current validator rules;
- filename matching and readiness rules are built around `AOS-FARM-TASK-\d+`;
- task-header-only exclusion is not sufficient if validator trust depends on already-valid identity.

Decision:

- future model should allow a registry or manifest witness for malformed legacy ids only;
- this does not normalize the id;
- this does not rename the file;
- this does not convert the task to pass;
- this does not close the blocker in AOS-FARM.640.

## 6. Proposed terminal exclusion model

Future terminal exclusion model:

- applies to otherwise identifiable task records with supported terminal witness;
- excludes them from active readiness counting only;
- emits `EXCLUDED_TERMINAL`;
- never emits `PASS` because of exclusion alone;
- preserves per-task listing in human and JSON output.

Supported future witness examples:

- rejected with human decision reference;
- closed-rejected with subtype and decision reference;
- closed-retired with human witness;
- closed-superseded with valid replacement reference.

## 7. Proposed legacy exclusion model

Future legacy exclusion model:

- applies to malformed legacy records such as invalid historical task ids;
- requires explicit per-task quarantine witness;
- emits `EXCLUDED_LEGACY`;
- never treats malformed identity as valid identity;
- keeps the task visible in audit output.

## 8. Human checkpoint requirements

All future exclusion use requires human checkpointing.

Minimum expectations:

- human decision maker;
- decision reference;
- decision date;
- exclusion reason;
- dependency or replacement review result;
- explicit `not_pass: true` semantics.

Agent-assigned exclusion witness is forbidden.

## 9. Witness-location decision

Decision:

- normal terminal witness should live in the task header;
- malformed legacy witness should live in a separate human-gated registry or manifest.

Reason:

- normal terminal state is most safely audited near the task itself;
- malformed legacy records need a quarantine surface that does not depend on already-valid task identity parsing.

## 10. Validator check order decision

Decision:

- future `task --validate-all` remains full-discovery and strict;
- future readiness classification evaluates all discovered tasks, then distinguishes:
  - active tasks,
  - valid terminal exclusions,
  - valid legacy exclusions,
  - malformed exclusions.

Reason:

- no discovered task may disappear;
- invalid legacy tasks must remain visible even if excluded from active readiness counting;
- malformed exclusion claims must fail closed.

## 11. Dependency and supersession rules

Future rules must require:

- valid target for `superseded_by`;
- no self-supersession;
- no circular supersession;
- no exclusion if active downstream dependency would be stranded without replacement mapping;
- explicit dependency review in witness output.

## 12. Risks

Primary risks:

- accidental weakening of readiness semantics;
- accidental conversion of terminal exclusion into implicit pass;
- registry drift or blanket exclusion misuse;
- silent acceptance of malformed legacy ids;
- dependency graph corruption through unsafe supersession.

Mitigation:

- per-task witness only;
- explicit `EXCLUDED_TERMINAL` and `EXCLUDED_LEGACY` states;
- strict malformed exclusion reporting;
- no wildcard or bulk exclusion;
- protected implementation stage with human checkpoint.

## 13. Non-goals

This decision record does not:

- implement validator changes;
- change current schema;
- edit current task files;
- rename `AOS-FARM.463`;
- close any blocker;
- authorize implementation;
- create an exclusion registry now.

## 14. Rejected alternatives

Rejected:

- treat `REJECTED` as automatic pass;
- treat `CLOSED` as automatic pass;
- use only a registry for all exclusions;
- use only task-header witness for malformed legacy ids;
- omit excluded tasks from output;
- accept bulk exclusions.

## 15. Downstream tasks required

Recommended downstream tasks:

1. Protected implementation task for hybrid exclusion semantics.
2. Schema/helper reconciliation task for `CLOSED` and subtype semantics.
3. Legacy quarantine implementation task for malformed ids.
4. Dedicated test implementation task for exclusion cases.
5. Human checkpoint task before any registry or manifest is created.

## 16. Required common safety statements

- This report is Evidence, not approval.
- PASS is validation only, not approval.
- Evidence is not approval.
- CI PASS is not approval.
- Excluded terminal task is not PASS.
- Excluded legacy task is not PASS.
- `EXCLUDED_TERMINAL` is not `READY_FOR_HANDOFF`.
- `EXCLUDED_LEGACY` is not `READY_FOR_HANDOFF`.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- No release is authorized.
- No merge to main is authorized.
- No blocker is closed by this report.
- No implementation is authorized by this report.
- Human approval cannot be simulated.

## 17. Conclusion

No blocker is closed by AOS-FARM.640.

This decision record is Evidence, not approval.
