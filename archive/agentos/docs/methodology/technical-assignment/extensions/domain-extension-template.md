# [Domain] Intake Extension

**Domain:** [domain-name]  
**Extension status:** DRAFT_DOMAIN_EXTENSION  
**Extends:** technical-assignment-agent-workflow  
**May override core:** false  
**May weaken core:** false  
**Execution authorized:** false  

---

## 1. Когда использовать

[Опишите, когда этот domain extension должен подключаться.]

---

## 2. Серые зоны отрасли

[Опишите domain-specific grey zones, которые core workflow не закрывает достаточно глубоко.]

---

## 3. Domain-Specific Questions

1. [Вопрос специалисту]
2. [Вопрос специалисту]
3. [Вопрос специалисту]

---

## 4. Domain-Specific Data Discovery

Возможные data objects:

- [Data Object]
- [Data Object]
- [Data Object]

Для каждого объекта указать:

- sensitivity;
- owner;
- source;
- access roles;
- lifecycle;
- audit requirement;
- Human review requirement.

---

## 5. Domain-Specific Access / Permissions

Типичные roles:

- [Role]
- [Role]
- [Role]

Sensitive actions:

- [Action requiring approval]
- [Action requiring audit]
- [Action forbidden by default]

---

## 6. Domain-Specific Negative Constraints

Система не должна:

- [forbidden action];
- [forbidden action];
- [forbidden action].

---

## 7. Domain-Specific Acceptance Criteria

Acceptance Criteria должны включать:

- [check];
- [check];
- [check].

---

## 8. Human Decisions Required

- [decision]
- [decision]
- [decision]

---

## 9. Final Status

```yaml
extension_applied: true / false
domain: [domain-name]
domain_review_required: true
unresolved_domain_risks_count: [number]
execution_authorized: false
implementation_authorized: false
```
