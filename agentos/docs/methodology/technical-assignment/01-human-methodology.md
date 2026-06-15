# 01 — Человекочитаемая методология

**Document status:** ACTIVE_OPERATIONAL_METHOD  
**Methodology ID:** TECHNICAL_ASSIGNMENT_AGENT_WORKFLOW  
**Methodology version:** 1.0  
**Paired machine contract:** `02-agent-contract.yaml`  
**Implementation authorized:** false  
**Execution authorized:** false  

---

## 1. Назначение

Этот документ объясняет методологию создания технического задания с помощью агента.

Документ предназначен для инженера, архитектора или владельца workflow, который проектирует путь от входных данных непрограммиста к структурированным draft artifacts.

Методология фокусируется на:

- User Vision;
- Data Discovery;
- Information Flow;
- Access / Permissions;
- Constraints;
- Acceptance Criteria;
- Human review boundaries;
- отраслевых серых зонах.

---

## 2. Главная идея

Агент не должен заставлять пользователя думать как программист.

Пользователь описывает:

- что хочет получить;
- что должно измениться;
- какие данные существуют;
- кто пользуется системой;
- кто может видеть или менять данные;
- что система никогда не должна делать;
- что будет считаться успехом.

Агент переводит это в структурированные draft artifacts.

---

## 3. AOS boundaries

Агент всегда сохраняет границы:

```text
PASS ≠ approval.
Evidence ≠ approval.
Interview summary ≠ approval.
Requirements Checklist ≠ approval.
PROJECT_SPEC.draft.md ≠ approval.
PROJECT_SPEC.md ≠ approval.
Human review ≠ execution approval.
Human approval cannot be simulated.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
Skeleton ≠ implementation.
User Vision ≠ approved requirement.
Implementation Hint ≠ architecture decision.
Data Discovery ≠ final database schema.
Information Flow ≠ implementation.
Problem Interview completed ≠ implementation authorization.
Problem Interview skipped ≠ BLOCKED.
```

---

## 4. User Vision

User Vision — это то, что пользователь хочет получить и как он представляет решение.

Техническое задание должно включать:

```markdown
# User Vision

## Что пользователь хочет получить
[простое описание]

## Почему это важно
[цель / польза / боль]

## Как пользователь представляет решение
[идеи и предпочтения пользователя]

## Что пользователь считает успехом
[наблюдаемый или измеримый результат]
```

Правила:

- User Vision не является approved requirement.
- User Vision не является approved scope.
- User Vision не является architecture.

---

## 5. Data Discovery

Data Discovery обязателен.

Он собирает:

- data objects;
- example fields;
- кто создаёт данные;
- кто читает данные;
- кто обновляет данные;
- кто удаляет или архивирует данные;
- sensitive data status;
- data lifecycle;
- audit trail needs.

Data Discovery является входом для будущей architecture и database modelling.

Он не является final database schema.

---

## 6. Information Flow

Information Flow описывает, как данные движутся через систему:

```text
source → actor → system action → destination → Human review point → log/audit
```

Нужно зафиксировать:

- источник данных;
- actor;
- destination;
- transformation или action;
- Human review requirement;
- logging requirement.

High-impact actions по умолчанию требуют Human review.

---

## 7. Access / Permissions

Access / Permissions обязателен, если:

- в системе больше одного пользователя;
- есть роли;
- есть sensitive data;
- есть external users;
- важен role-based access.

Workflow должен создать Access Matrix:

```markdown
| Data Object | Create | Read | Update | Delete | Approve |
|---|---|---|---|---|---|
```

Это вход для architecture, а не final authorization implementation.

---

## 8. Optional Current Workflow

Классический As-Is не обязателен.

Current Workflow собирается только если:

- пользователь заменяет существующий workflow;
- есть текущий ручной процесс;
- проект является migration из старой системы;
- проект автоматизирует существующие operations.

Если не применимо:

```yaml
current_workflow_status: NOT_APPLICABLE
current_workflow_required: false
```

---

## 9. Implementation Hints

Implementation Hints полезны, но не являются финальными решениями.

Разрешённые statuses:

```text
USER_MENTIONED
AGENT_INFERENCE
CANDIDATE_REQUIREMENT
NOT_EVALUATED
NEEDS_HUMAN_REVIEW
```

Запрещённые statuses:

```text
APPROVED_REQUIREMENT
SELECTED_STACK
FINAL_ARCHITECTURE
READY_FOR_EXECUTION
STACK_APPROVED
IMPLEMENTATION_CHOICE
```

Правила:

- Implementation Hint не является requirement.
- Implementation Hint не является stack selection.
- Agent inference не является architecture.
- User preference не является approved technical decision.

---

## 10. Problem Interview Status

Problem Interview полезен, но не обязателен.

Если он выполнен, confidence выше.

Если он пропущен, draft всё равно можно создать, но нужно явно показать более низкий confidence.

Обязательная формулировка при skip:

```text
Проблемное интервью было пропущено пользователем.
Это ТЗ основано в основном на видении пользователя, его предпочтениях, описанных данных и подсказках по реализации.
Доказательная база проблемы неполная.
Перед реализацией ключевые предположения нужно проверить человеком.
```

---

## 11. Draft Artifacts

Разрешённые draft artifacts:

- `problem-interview-report.md`;
- `requirements-checklist-draft.md`;
- `PROJECT_SPEC.draft.md`;
- `REQUIREMENTS.draft.md`;
- candidate task list только если это явно входит в scope.

Запрещённые artifacts:

- canonical `PROJECT_SPEC.md`;
- execution package;
- commit authorization;
- push authorization;
- deploy authorization;
- production use authorization;
- final database schema;
- final architecture decision.

---

## 12. Human Review Boundary

Human review требуется перед:

- approval требований;
- final database schema;
- architecture decisions;
- implementation tasks;
- execution package;
- commit;
- push;
- deploy;
- production use.

Ни один artifact из этой методологии не разрешает execution.

---

## 13. Change Control

Если этот документ меняется:

- нужно проверить `02-agent-contract.yaml`;
- нужно вручную пройти `07-consistency-checklist.md`;
- независимые изменения `01` или `02` без consistency review не допускаются.
