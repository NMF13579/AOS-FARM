# 04 — Шаблоны draft artifacts

**Document status:** ACTIVE_OPERATIONAL_METHOD_COMPONENT  
**Scope:** draft artifact templates only  
**Approval authorized:** false  
**Execution authorized:** false  

---

## 1. Разрешённые draft artifacts

Агент может создавать:

- `problem-interview-report.md`;
- `requirements-checklist-draft.md`;
- `PROJECT_SPEC.draft.md`;
- `REQUIREMENTS.draft.md`;
- preliminary candidate task list только если это явно входит в scope.

Агент не должен создавать:

- canonical `PROJECT_SPEC.md`;
- execution package;
- commit authorization;
- push authorization;
- deploy authorization;
- production use authorization;
- final database schema;
- final architecture decision.

---

## 2. Шаблон PROJECT_SPEC.draft.md

```markdown
---
title: [Project title]
version: 0.1-draft
status: DRAFT
approval_status: NOT_APPROVED
execution_authorized: false
implementation_authorized: false
---

# 1. Source Status
- intake_depth: EXPRESS / FULL / EXISTING_SPEC_REVIEW
- source_input_type: interview / existing_spec / user_vision_only / mixed
- problem_interview_status: COMPLETED / INCOMPLETE / SKIPPED_BY_USER / NOT_REQUIRED
- problem_evidence_level: HIGH / MEDIUM / LOW / UNKNOWN
- data_discovery_depth: FULL / PARTIAL / MINIMAL / MISSING / UNKNOWN
- requirements_confidence: HIGH / MEDIUM / LOW / UNKNOWN

# 2. User Vision
[что пользователь хочет получить, зачем это нужно, как он представляет решение]

# 3. Data Discovery
[Data Inventory, data objects, fields, sensitivity, source, owner]

# 4. Information Flow
[как данные входят, обрабатываются, хранятся и передаются]

# 5. Access / Permissions
[роли и permissions]

# 6. Problem Evidence
[боль, последний конкретный случай, workaround, частота, цена ошибки, цитаты]

# 7. Optional Current Workflow
[текущий workflow, если применимо]

# 8. Requirements Draft
[candidate requirements]

# 9. Implementation Hints
[идеи с NOT_EVALUATED / NEEDS_HUMAN_REVIEW]

# 10. Negative Constraints
[never do, ask first, compliance]

# 11. Acceptance Criteria
[Given-When-Then / Input → Expected Output]

# 12. MVP
[минимальная полезная версия]

# 13. UNKNOWN / Open Questions
[неизвестные вопросы]

# 14. Contradictions
[противоречия или No contradictions detected]

# 15. Human Decisions Required
[решения, требующие Human review]

# 16. Final Status
ready_for_requirements_review: true / true_with_risks / false
ready_for_execution: false
approval_status: NOT_APPROVED
execution_authorized: false
```

---

## 3. Шаблон REQUIREMENTS.draft.md

```markdown
# Functional Requirements

- FR-001: Система ДОЛЖНА [конкретное действие].
  - Source: [source]
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true / false

# Data Requirements

- DATA-001: Система должна хранить [data object].
  - Fields: [fields]
  - Sensitive: yes / no / UNKNOWN
  - Source: [Data Discovery]

# Access Requirements

- ACCESS-001: Роль [X] может [create/read/update/delete/approve] объект [Y].

# Non-Functional Requirements

- NFR-001: Система ДОЛЖНА [quality / constraint].

# Constraints

- CON-001: Система НЕ ДОЛЖНА [forbidden action].

# Security / Privacy

- SEC-001: [security/privacy requirement].

# Acceptance Criteria

- AC-001: GIVEN [condition] WHEN [action] THEN [result].

# Out of Scope

- OOS-001: [excluded item].

# UNKNOWN

- UNK-001: [unknown].
```

---

## 4. Шаблон Traceability Matrix

```markdown
# Traceability Matrix

| Requirement ID | Source | Source Type | Acceptance Criteria | Human Decision Needed |
|---|---|---|---|---|
| FR-001 | Q-003 | quote | AC-001 | no |
| DATA-001 | DATA-OBJECT-001 | data_discovery | AC-002 | yes |
| ACCESS-001 | ACCESS-MATRIX | access_permissions | AC-003 | yes |
| CON-001 | Q-007 | quote | AC-004 | no |
```

Allowed Source Type:

```text
quote
self_report
existing_spec
user_vision
data_discovery
information_flow
access_matrix
implementation_hint
agent_inference
UNKNOWN
```

---

## 5. Шаблон Final Status Block

```yaml
final_status:
  artifact_type: PROJECT_SPEC_DRAFT / REQUIREMENTS_DRAFT / PROBLEM_INTERVIEW_REPORT / REQUIREMENTS_CHECKLIST_DRAFT
  intake_depth: EXPRESS / FULL / EXISTING_SPEC_REVIEW
  problem_interview_status: COMPLETED / INCOMPLETE / SKIPPED_BY_USER / NOT_REQUIRED
  problem_evidence_level: HIGH / MEDIUM / LOW / UNKNOWN
  data_discovery_depth: FULL / PARTIAL / MINIMAL / MISSING / UNKNOWN
  information_flow_status: COMPLETE / PARTIAL / MISSING / UNKNOWN
  access_permissions_status: COMPLETE / PARTIAL / MISSING / NOT_APPLICABLE / UNKNOWN
  requirements_confidence: HIGH / MEDIUM / LOW / UNKNOWN
  unknown_count: [number]
  contradiction_count: [number]
  inference_count: [number]
  implementation_hint_count: [number]
  critical_failure_count: [number]
  ready_for_requirements_review: true / true_with_risks / false
  ready_for_execution: false
  approval_status: NOT_APPROVED
  execution_authorized: false
  implementation_authorized: false
  commit_authorized: false
  push_authorized: false
  deploy_authorized: false
  production_use_authorized: false
```
