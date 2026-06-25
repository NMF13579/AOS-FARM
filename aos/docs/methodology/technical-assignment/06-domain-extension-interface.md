# 06 — Интерфейс Domain Extension

**Document status:** ACTIVE_OPERATIONAL_METHOD_COMPONENT  
**Scope:** правила отраслевых intake extensions  
**Execution authorized:** false  

---

## 1. Назначение

Domain Extensions позволяют специалистам закрывать отраслевые серые зоны без переписывания core technical assignment workflow.

Примеры:

- медицина;
- строительство;
- образование;
- финансы;
- право;
- государственный сектор.

---

## 2. Extension Policy

Domain Extension может добавлять:

- domain-specific questions;
- required data fields;
- domain-specific constraints;
- safety gates;
- Human review requirements;
- Acceptance Criteria;
- domain-specific UNKNOWN list;
- domain-specific specialist decisions.

Domain Extension не может:

- override core;
- weaken core;
- authorize execution;
- authorize implementation;
- assign Risk Profile;
- select stack;
- finalize database schema;
- remove Human review;
- simulate Human approval.

Policy:

```yaml
domain_extension_policy:
  may_add_questions: true
  may_add_required_data_fields: true
  may_add_constraints: true
  may_add_safety_gates: true
  may_add_human_review_requirements: true

  may_override_core: false
  may_weaken_core: false
  may_authorize_execution: false
  may_authorize_implementation: false
  may_assign_risk_profile: false
  may_select_stack: false
  may_finalize_database_schema: false

  if_conflict_with_core:
    status: HUMAN_REVIEW_REQUIRED
    execution_authorized: false
```

---

## 3. Шаблон Extension

```markdown
# [Domain] Intake Extension

## 1. Extension Status
- domain: [domain]
- extension_status: ACTIVE_DOMAIN_EXTENSION
- extends: technical-assignment-agent-workflow
- may_override_core: false
- may_weaken_core: false
- execution_authorized: false

## 2. When to Use This Extension
[когда подключать]

## 3. Domain-Specific Grey Zones
[серые зоны отрасли]

## 4. Domain-Specific Questions
[вопросы для специалиста]

## 5. Domain-Specific Data Discovery
[data objects, fields, sensitivity, lifecycle]

## 6. Domain-Specific Access / Permissions
[roles, permissions, approval points]

## 7. Domain-Specific Negative Constraints
[never do, ask first, compliance]

## 8. Domain-Specific Acceptance Criteria
[как проверять]

## 9. Domain-Specific Human Decisions Required
[решения, требующие specialist review]

## 10. Extension Final Status
- extension_applied: true / false
- unresolved_domain_risks_count: [number]
- domain_review_required: true / false
- execution_authorized: false
```

---

## 4. Activation Rule

Domain Extension нужно подключать, если:

- пользователь назвал отрасль;
- появились domain-specific data;
- система влияет на domain-specific safety, compliance, money, legal, clinical, construction, educational или professional outcomes;
- агент не уверен, применяются ли отраслевые правила.

Если непонятно:

```yaml
domain_extension_status: UNKNOWN
domain_review_required: true
execution_authorized: false
```
