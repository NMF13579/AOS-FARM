# DOGFOOD.9 Comparative Audit: SMP Equipment vs RAG Org KB

```yaml
artifact_type: comparative_dogfood_audit
compared_cases:
  - smp-equipment-dogfood-2026-06-19
  - rag-org-kb-dogfood-2026-06-20
artifact_status: DRAFT
approval_status: NOT_APPROVED
execution_status: NOT_AUTHORIZED
ready_for_execution: false
final_process_status: NEEDS_HUMAN_REVIEW
```

## 1. Metadata

- artifact_type: `comparative_dogfood_audit`
- compared_cases:
  - `smp-equipment-dogfood-2026-06-19`
  - `rag-org-kb-dogfood-2026-06-20`
- artifact_status: `DRAFT`
- approval_status: `NOT_APPROVED`
- execution_status: `NOT_AUTHORIZED`
- ready_for_execution: false
- final_process_status: `NEEDS_HUMAN_REVIEW`

## 2. Audit Purpose

This audit compares two Technical Assignment Pipeline V2 dogfood runs to determine what can be safely claimed and what must remain warning, limitation, or recommendation.

This audit is evidence synthesis only. It does not approve either generated specification, does not authorize implementation, does not create a Task Brief, does not authorize release or production use, and does not modify methodology.

## 3. Case Inventory

### Case 1: SMP Equipment

Directory: `agentos/reports/problem-intake/smp-equipment-dogfood-2026-06-19/`

Artifacts found:

- `input.md`
- `problem-interview-report.md`
- `PROJECT_SPEC.draft.md`
- `REQUIREMENTS.draft.md`
- `requirements-checklist-draft.md`
- `problem-intake-run-report.md`
- `documentation-assembly-bridge-output.md`
- `human-review-package.md`
- `validator-report.md`
- `dogfood-audit.md`
- `dogfood-decision.md`

Inventory status: complete for the known SMP dogfood package.

### Case 2: RAG Org KB

Directory: `agentos/reports/problem-intake/rag-org-kb-dogfood-2026-06-20/`

Artifacts found:

- `input.md`
- `problem-interview-report.md`
- `PROJECT_SPEC.draft.md`
- `REQUIREMENTS.draft.md`
- `requirements-checklist-draft.md`
- `problem-intake-run-report.md`
- `implementation-contract-draft.md`
- `unknown-resolution-addendum.md`
- `documentation-assembly-bridge-output.md`
- `human-review-package.md`
- `validator-report.md`
- `dogfood-audit.md`

Inventory status: complete for the known RAG Org KB dogfood package.

## 4. Case 1 Summary: SMP Equipment

Intake route:

- interview-based / problem-interview route;
- richer operational discovery than a direct brief;
- real-world ambulance station equipment accounting/control context.

Domain complexity:

- operational workflow;
- custody and responsibility chain;
- physical inventory;
- equipment state;
- shift handoff;
- paper checklist mismatch;
- audit trail and accountability pressure.

What the pipeline produced well:

- structured input and problem interview report;
- `PROJECT_SPEC.draft.md`;
- `REQUIREMENTS.draft.md`;
- checklist;
- run report;
- bridge output;
- human review package;
- validator evidence;
- dogfood audit;
- decision report accepting the MVP with warnings.

Weak or unresolved areas:

- role, permission, escalation, and exception details remained incomplete;
- significant interaction boundary needed sharper definition;
- reporting and management escalation required deeper requirements pass;
- inter-substation movement exceptions were not fully developed;
- manual structural validation did not prove semantic correctness.

Validation status:

- validation_type: `manual_structural_evidence`;
- validator_command_executed: false;
- audit_status: `PASS_WITH_WARNINGS`.

Audit / decision status:

- `PIPELINE_MVP_STATUS: WORKING_MVP_CONFIRMED`;
- `DOGFOOD_DECISION: ACCEPT_MVP_WITH_WARNINGS`;
- `APPROVAL_STATUS: NOT_APPROVED`;
- `EXECUTION_STATUS: NOT_AUTHORIZED`;
- ready_for_execution: false.

Final dogfood implication:

The SMP case is strong evidence that Technical Assignment Pipeline V2 works as an MVP for an interview-based operational problem-intake flow through Human Review Package level, with warnings.

## 5. Case 2 Summary: RAG Org KB

Intake route:

- direct brief route;
- `problem_interview_status: SKIPPED_BY_USER`;
- accepted for dogfood but lower confidence than interview-based intake.

Domain complexity:

- technical product design;
- organizational knowledge bases;
- document lifecycle;
- metadata extraction;
- Markdown conversion;
- chunking and indexing;
- role-based access;
- future retrieval/chat;
- citation behavior;
- audit and retention.

What the pipeline produced well:

- direct brief input;
- skipped-interview disclosure;
- `PROJECT_SPEC.draft.md`;
- `REQUIREMENTS.draft.md`;
- checklist;
- run report;
- implementation contract draft;
- UNKNOWN resolution addendum;
- bridge output;
- human review package;
- validator report;
- dogfood audit.

Why Engineering Clarification was needed:

- product/discovery drafts described a broad RAG product, but were not enough for agent coding;
- data model, state machine, RBAC, indexing, retrieval, chat answer behavior, error handling, audit, and MVP slice needed engineering-level clarification;
- UNKNOWN resolution was needed to narrow the first implementation slice to `Document pipeline only`;
- without this layer, a coding agent could overbuild full RAG chat or make unapproved backend/security decisions.

Validation status:

- validation_type: `manual_structural_evidence`;
- validator_command_executed: false;
- structural_validation_status: `STRUCTURAL_VALIDATION_PASS_WITH_WARNINGS`.

Audit status:

- audit_status: `DOGFOOD_AUDIT_PASS_WITH_WARNINGS`;
- package_level: `HUMAN_REVIEW_PACKAGE_LEVEL`;
- approval_status: `NOT_APPROVED`;
- execution_status: `NOT_AUTHORIZED`;
- ready_for_execution: false.

Final dogfood implication:

The RAG case is strong evidence that Technical Assignment Pipeline V2 can handle a complex technical product/discovery case through Human Review Package level, but also proves that complex technical domains need an Engineering Clarification / Implementation Contract layer before Task Brief generation.

## 6. Route Comparison

| Dimension | SMP interview-based route | RAG direct brief route |
|---|---|---|
| Discovery depth | Higher, because the agent collected operational detail through interview | Lower, because problem interview was intentionally skipped |
| Product/discovery draft quality | Strong for operational process mapping | Strong for product concept, weaker for validated problem evidence |
| UNKNOWN generated | Operational UNKNOWN around role boundaries, exceptions, reporting, significant interaction | Engineering/product UNKNOWN around data model, parser fidelity, chunking, VectorStore, retention, Task Brief boundary |
| Human Review Package readiness | Reached | Reached |
| Agent coding readiness | Not ready without further scoping | Not ready without engineering clarification and Task Brief |
| Risk of missing engineering constraints | Medium | High without implementation contract |

Conclusion:

The interview-based route is stronger for problem discovery. The direct brief route can still produce useful drafts, but it carries higher risk and needs explicit engineering clarification before implementation planning.

## 7. Domain Complexity Comparison

SMP equipment case:

- best described as operational workflow / custody / inventory domain;
- tested problem interview, responsibility chains, physical asset movement, handoff, exception handling, and audit needs;
- better tested product reasoning around messy real-world process and accountability.

RAG Org KB case:

- best described as technical product / document lifecycle / indexing / retrieval domain;
- tested product-to-engineering translation, domain model, document lifecycle, indexing abstractions, access control, and future RAG behavior;
- exposed deeper engineering gaps than the SMP case.

Comparison:

- SMP better tested interview-based product discovery and operational process modeling.
- RAG better tested implementation-readiness limits and the need for an intermediate engineering layer.
- Both cases tested safety semantics and Human Review Package construction.

## 8. Pipeline Strengths Proven By Both Cases

Together, the two cases show that Technical Assignment Pipeline V2 can:

- turn user input into structured `PROJECT_SPEC` draft artifacts;
- produce `REQUIREMENTS` draft artifacts;
- preserve `DRAFT / NOT_APPROVED / NOT_AUTHORIZED`;
- reach Human Review Package level in at least two different domains;
- surface UNKNOWN instead of hiding it;
- prevent fake execution-ready promotion;
- avoid approval simulation;
- support dogfood evidence creation;
- keep Evidence separate from approval;
- keep Human Review Package separate from implementation authorization.

Strength classification:

- product/discovery draft pipeline: strong evidence;
- Human Review Package construction: strong evidence;
- safety boundary preservation: strong evidence;
- semantic completeness: medium evidence;
- implementation readiness: weak evidence;
- CLI validator automation for extended packages: weak/missing evidence.

## 9. Pipeline Limitations Proven By Dogfood

Observed limitations:

- direct brief route is weaker than interview-based route;
- complex technical domains need engineering clarification;
- current validator coverage is mostly structural/manual for extended dogfood packages;
- run reports may lag behind late dogfood artifacts;
- product requirements are not enough for agent coding;
- Human Review Package is not implementation authorization;
- dogfood evidence does not prove production readiness;
- dogfood evidence does not prove universal domain coverage;
- neither case produced an approved Task Brief;
- neither case executed implementation.

These limitations are acceptable for dogfood evidence, but they must remain visible.

## 10. Engineering Clarification Layer Assessment

Evidence supports formalizing a permanent layer between `REQUIREMENTS` and Task Brief for complex or technical products.

Candidate layer components:

- `Engineering Clarification / Implementation Contract`
- `UNKNOWN Resolution Addendum`
- `Documentation Assembly Bridge Output`
- `Human Review Package before Task Brief`

Evidence from RAG case:

- `implementation-contract-draft.md` clarified entities, state machine, RBAC, indexing, retrieval, chat answer behavior, error handling, audit/retention, and MVP boundary.
- `unknown-resolution-addendum.md` narrowed key implementation-affecting UNKNOWN without turning decisions into approval.
- bridge output connected product/discovery and engineering layers into review-ready evidence.
- human review package captured required human decisions before Task Brief.

Evidence from SMP case:

- interview-based product discovery was strong, but role, permission, exception, and reporting gaps still remained.
- this suggests engineering clarification may also help non-technical operational domains when moving from requirements to implementation scope.

Boundary:

- DOGFOOD.9 may recommend methodology change.
- DOGFOOD.9 must not perform methodology change.
- Methodology recommendation does not equal methodology change.

Recommendation:

Formalize the Engineering Clarification / Implementation Contract layer in a later authorized methodology task, or explicitly defer it with recorded rationale.

## 11. Safety Boundary Comparison

Both cases preserved the required safety boundary:

| Safety invariant | SMP | RAG |
|---|---:|---:|
| No approval claimed | yes | yes |
| No execution authorization claimed | yes | yes |
| No execution-ready promotion claimed | yes | yes |
| No release authorization claimed | yes | yes |
| No production use claimed | yes | yes |
| Human approval not simulated | yes | yes |
| PASS / Evidence not treated as approval | yes | yes |
| Human review package not treated as approval | yes | yes |
| Domain workflow approval not treated as AOS approval | yes | yes |

Safety conclusion:

The strongest shared result is not just artifact generation, but preservation of approval/execution boundaries under two different case types.

## 12. Evidence Quality Assessment

Strong evidence:

- two different domains tested;
- one interview-based operational case;
- one direct-brief technical product case;
- both reached Human Review Package level;
- both preserved `NOT_APPROVED`, `NOT_AUTHORIZED`, and `ready_for_execution: false`;
- both surfaced UNKNOWN and warnings;
- RAG case demonstrated the value of an engineering clarification layer.

Medium evidence:

- product/discovery draft quality across different domains;
- repeatability of artifact chain;
- manual structural validation adequacy for dogfood evidence;
- methodology implication that Engineering Clarification should be formalized.

Weak evidence:

- implementation readiness;
- semantic completeness of requirements;
- role/permission completeness;
- exception handling completeness;
- validator automation coverage for extended packages.

Missing evidence:

- production validation;
- implementation execution;
- approved Task Brief generation;
- CLI validator execution over the full extended packages;
- release readiness;
- universal domain coverage.

Overall evidence quality:

`MEDIUM_TO_STRONG_FOR_PRODUCT_DISCOVERY_PIPELINE_WITH_WARNINGS`

## 13. Conclusions

What can be safely claimed:

- Technical Assignment Pipeline V2 works as a product/discovery draft pipeline with warnings.
- It can reach Human Review Package level in at least two different domains.
- It preserves approval and execution boundaries.
- It supports both interview-based and direct-brief intake, with direct brief carrying lower confidence.
- It surfaces UNKNOWN rather than hiding it.
- It supports dogfood evidence creation.
- Engineering Clarification / Implementation Contract layer is recommended before Task Brief for complex technical domains.

What cannot be claimed:

- not production ready;
- not release ready;
- not universally validated;
- not implementation-ready by default;
- not approved;
- not authorized for execution;
- not validated through full CLI validator coverage for extended packages;
- not sufficient by itself for direct agent coding in complex technical domains.

Safe conclusion:

Technical Assignment Pipeline V2 has enough comparative dogfood evidence to support `WORKS_AS_PRODUCT_DISCOVERY_PIPELINE_WITH_WARNINGS`, while requiring a follow-up methodology decision on whether to formalize the Engineering Clarification / Implementation Contract layer.

## 14. Recommended Next Step

`DOGFOOD.10 — Dogfood Methodology Decision: formalize or defer Engineering Clarification / Implementation Contract layer.`

## 15. Final Comparative Audit Status

```yaml
audit_status: COMPARATIVE_DOGFOOD_AUDIT_PASS_WITH_WARNINGS
evidence_quality: MEDIUM_TO_STRONG_FOR_PRODUCT_DISCOVERY_PIPELINE_WITH_WARNINGS
methodology_recommendation: FORMALIZE_ENGINEERING_CLARIFICATION_LAYER_BEFORE_TASK_BRIEF
approval_status: NOT_APPROVED
execution_status: NOT_AUTHORIZED
ready_for_execution: false
final_process_status: NEEDS_HUMAN_REVIEW
methodology_changed: false
commit_performed: false
push_performed: false
cleanup_performed: false
```
