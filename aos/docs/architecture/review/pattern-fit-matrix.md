---
task_id: AOS-FARM.621
document_type: pattern_fit_matrix
matrix_status: INCOMPLETE_WEIGHTS
approval_status: NOT_REQUESTED
human_weight_required: true
human_review_required: true
active_patterns_selected: false
---

# Pattern Fit Matrix

This matrix compares existing AOS and architecture patterns as candidate-only evidence.
It does not select active patterns and does not authorize implementation.

## Pattern candidates

| Pattern | Candidate notes |
|---|---|
| AOS-PATTERN-001 Markdown-first Governance | Strong alignment with existing AOS source-of-truth model. |
| AOS-PATTERN-002 Human-Gated Pipeline | Strong alignment with approval and authorization boundaries. |
| AOS-PATTERN-003 Template + Validator | Strong alignment with repeatable lifecycle checks. |
| AOS-PATTERN-004 Candidate → Approved Queue | Strong alignment with candidate lifecycle separation. |
| AOS-PATTERN-005 Local Scratch Boundary | Strong alignment with non-canonical working space discipline. |
| AOS-PATTERN-006 Product Folder Boundary | Strong alignment with project isolation. |
| AOS-PATTERN-007 Read-only Dashboard | Useful for visibility without mutation authority. |
| AOS-PATTERN-008 Safe-Create Installer | Strong alignment with installer safety boundary. |
| AOS-PATTERN-009 Tutor-Guided Workflow | Useful for non-programmer workflows; requires scope control. |
| ARCH-PATTERN-001 Layered Architecture | Common baseline; fit depends on project complexity. |
| ARCH-PATTERN-002 Modular Monolith | Useful for bounded complexity without service sprawl. |
| ARCH-PATTERN-003 Event-Driven Architecture | Useful for asynchronous flows; higher reasoning burden. |
| ARCH-PATTERN-004 Microservices | Usually high operational burden; requires strong justification. |
| ARCH-PATTERN-005 Hexagonal / Ports and Adapters | Useful for boundary discipline and testability. |
| ARCH-PATTERN-006 CQRS | Useful for read/write separation; may overfit simple projects. |
| ARCH-PATTERN-007 Serverless | Useful for managed runtime; external authority and platform coupling require review. |

## Criteria weights

| Criterion | Weight | Human weight required | Evidence source |
|---|---|---|---|
| Markdown-first compatibility | UNASSIGNED_BY_HUMAN | true | ADR-0001 |
| Validator-first lifecycle | UNASSIGNED_BY_HUMAN | true | ADR-0002 |
| Human-gated approval | UNASSIGNED_BY_HUMAN | true | ADR-0005 |
| Local-first operation | UNASSIGNED_BY_HUMAN | true | registry / project constraint |
| Non-programmer usability | UNASSIGNED_BY_HUMAN | true | project constraint |
| Safe installer boundary | UNASSIGNED_BY_HUMAN | true | ADR-0004 |
| Low operational burden | UNASSIGNED_BY_HUMAN | true | project constraint |
| Extensibility | UNASSIGNED_BY_HUMAN | true | registry |
| Fail-closed semantics | UNASSIGNED_BY_HUMAN | true | project constraint |
| Minimal runtime authority | UNASSIGNED_BY_HUMAN | true | ADR-0003 / project constraint |
| No autonomous runner by default | UNASSIGNED_BY_HUMAN | true | ADR-0003 |
| Product folder boundary preservation | UNASSIGNED_BY_HUMAN | true | project constraint |

## Candidate observations

| Criterion | Stronger observed candidates | Review caution |
|---|---|---|
| Markdown-first compatibility | AOS-PATTERN-001, AOS-PATTERN-003, AOS-PATTERN-004 | General architecture patterns need mapping into Markdown governance. |
| Validator-first lifecycle | AOS-PATTERN-003, AOS-PATTERN-007, ARCH-PATTERN-005 | Validation depth remains limited until a future validator stage. |
| Human-gated approval | AOS-PATTERN-002, AOS-PATTERN-004 | Human checkpoint answers are not present in this draft. |
| Local-first operation | AOS-PATTERN-001, AOS-PATTERN-005, AOS-PATTERN-006 | Serverless, bot, and SaaS-oriented patterns need extra authority review. |
| Non-programmer usability | AOS-PATTERN-007, AOS-PATTERN-009 | Guided UX must not imply delegated approval. |
| Safe installer boundary | AOS-PATTERN-008 | Installer behavior needs exact scope in a later stage. |
| Low operational burden | AOS-PATTERN-001, AOS-PATTERN-003, ARCH-PATTERN-002 | Microservices and event-driven designs may add burden. |
| Extensibility | AOS-PATTERN-003, ARCH-PATTERN-002, ARCH-PATTERN-005 | Extensibility must not expand scope without authorization. |
| Fail-closed semantics | AOS-PATTERN-002, AOS-PATTERN-003, AOS-PATTERN-004 | Future validation should guard against marker drift. |
| Minimal runtime authority | AOS-PATTERN-005, AOS-PATTERN-007, ARCH-PATTERN-002 | Runtime integrations require separate human review. |
| No autonomous runner by default | AOS-PATTERN-002, AOS-PATTERN-004 | Event-driven or bot designs must preserve manual gates. |
| Product folder boundary preservation | AOS-PATTERN-006, ARCH-PATTERN-005 | Boundary ownership must be explicit before implementation planning. |

## Tradeoffs and rationale

- AOS-native patterns are closer to the current lifecycle and should be reviewed first as governance candidates.
- General architecture patterns may be useful once project scope is known, but they need human weighting and contextual constraints.
- High-distribution patterns such as microservices, serverless, and event-driven architecture carry additional operational and authority concerns.
- No pattern is promoted by this matrix.
