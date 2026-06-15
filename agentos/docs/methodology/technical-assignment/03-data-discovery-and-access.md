# 03 — Data Discovery и Access / Permissions

**Document status:** ACTIVE_OPERATIONAL_METHOD_COMPONENT  
**Scope:** universal data intake, Information Flow, Access / Permissions  
**Final database schema authorized:** false  
**Implementation authorized:** false  
**Execution authorized:** false  

---

## 1. Назначение

Этот документ описывает, как агент собирает информацию о данных для технического задания.

Он помогает подготовить входные данные для будущих:

- conceptual data model;
- database schema draft;
- access model;
- data lifecycle;
- Information Flow;
- security requirements.

Документ не создаёт final database schema.

---

## 2. Вопросы Data Discovery

Агент спрашивает простым языком:

1. Что система должна помнить?
2. Какие основные объекты или записи будут в системе?
3. Какие данные нужно хранить по каждому объекту?
4. Кто создаёт данные?
5. Кто может видеть данные?
6. Кто может менять данные?
7. Кто может удалять или архивировать данные?
8. Кто должен подтверждать важные изменения?
9. Откуда данные появляются?
10. Куда данные должны передаваться?
11. Какие данные являются sensitive data?
12. Какие данные нельзя потерять?
13. Нужно ли хранить историю изменений?
14. Нужно ли логировать действия?
15. Есть ли данные, которые система не должна видеть или хранить?

---

## 3. Шаблон Data Inventory

```markdown
# Data Inventory

| Data Object | Description | Example Fields | Sensitive? | Source | Owner | Notes |
|---|---|---|---|---|---|---|
| [object] | [meaning] | [fields] | yes / no / UNKNOWN | [source] | [owner] | [notes] |
```

Для каждого data object нужно собрать:

- название объекта;
- смысл объекта;
- example fields;
- sensitivity;
- source;
- owner или controller, если известен;
- create/read/update/delete context;
- audit trail need;
- retention, если известен.

---

## 4. Шаблон Information Flow

```markdown
# Information Flow

| Step | Data | Source | Actor | Destination | Human Review Needed | Logging Needed |
|---|---|---|---|---|---|---|
| 1 | [data] | [source] | Human / System | [destination] | yes / no / UNKNOWN | yes / no / UNKNOWN |
```

High-impact actions по умолчанию получают:

```text
Human Review Needed: yes
```

Агент не может снять это значение без Human review.

---

## 5. Шаблон Access Matrix

```markdown
# Access Matrix

| Data Object | Create | Read | Update | Delete | Approve |
|---|---|---|---|---|---|
| [object] | [role] | [role] | [role] | [role / forbidden] | [role / not applicable] |
```

Access / Permissions обязателен при:

- multi-user system;
- sensitive data;
- external users;
- role-based access;
- domain-specific legal или professional boundaries.

---

## 6. Шаблон Data Lifecycle

```markdown
# Data Lifecycle

| Data Object | Created By | Created When | Updated By | Archived / Deleted By | Retention | Audit Required |
|---|---|---|---|---|---|---|
| [object] | [role] | [event] | [role] | [role / forbidden] | [period / UNKNOWN] | yes / no / UNKNOWN |
```

Если объект содержит sensitive data, lifecycle не может оставаться полностью UNKNOWN перед implementation.

---

## 7. Boundaries

```text
Data Discovery ≠ final database schema.
Information Flow ≠ implementation.
Access Matrix ≠ final authorization model.
Data Lifecycle ≠ migration plan.
```

Все эти элементы являются входом для Architecture / Data Model Plan.
