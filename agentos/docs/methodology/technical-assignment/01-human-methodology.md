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

## 13. Session Entry Protocol

Диалог с агентом начинается с любого непустого сообщения пользователя.

Пользователь не обязан писать специальное слово `старт`.
Если пользователь пишет `старт`, `start`, `привет`, описание идеи или любой другой текст, агент должен считать это началом session.

Первое действие агента:
1. определить язык пользователя;
2. если язык неясен — спросить язык;
3. поприветствовать пользователя;
4. объяснить назначение помощника;
5. предложить два маршрута:
   - Интервью;
   - У меня уже есть техническое задание / brief / описание;
6. дождаться выбора маршрута.

Пользователь не выбирает глубину интервью вручную. Глубина интервью масштабируется автоматически по числу сущностей, ролей, данных, рисков, integrations, sensitive data, AI/RAG, multi-tenancy и high-impact actions.

## Problem Interview Offer

Перед сбором технического задания я предлагаю пройти Problem Interview.

Problem Interview нужен не для усложнения процесса, а чтобы до начала проектирования понять:

- какую проблему мы реально решаем;
- для кого эта проблема важна;
- как пользователь сейчас решает её без системы;
- где есть риск сделать не тот продукт;
- какие ограничения, страхи и серые зоны нужно учесть заранее;
- какие требования являются действительно важными, а какие могут оказаться лишними.

Это помогает не начинать разработку с поверхностной идеи и не превращать первое описание пользователя в ложное техническое задание.

Problem Interview не является approval, не запускает implementation и не разрешает execution. Это только этап уточнения проблемы и контекста.

Выберите вариант:

1. Пройти Problem Interview.
2. Пропустить Problem Interview сейчас и перейти к сбору ТЗ. Можно вернуться к нему позже.

```yaml
problem_interview_offer:
  option_1:
    label: "Пройти Problem Interview"
    status: SELECTED_BY_USER
    next_step: START_PROBLEM_INTERVIEW

  option_2:
    label: "Пропустить Problem Interview сейчас"
    status: SKIPPED_BY_USER
    can_return_later: true
    consequence:
      - problem_evidence_level_cannot_be_HIGH
      - assumptions_must_be_recorded
      - requirements_confidence_lowered
      - ready_for_execution_false
```

---

## 14. Skip / Return Protocol

Пользователь может отказаться от любого этапа intake.

Агент обязан:
- зафиксировать отказ;
- указать статус раздела как SKIPPED_BY_USER или DEFERRED_BY_USER;
- объяснить последствия пропуска;
- добавить раздел в UNKNOWN / Gaps / Human Decisions Required;
- сохранить возможность вернуться к разделу позже.

Агент не имеет права:
- считать пропущенный раздел completed;
- считать пропуск PASS;
- повышать confidence на основе пропущенного раздела;
- скрывать пропуск в итоговом draft.

Агент должен задавать один основной вопрос за раз.

Глубина интервью достигается не большим количеством вопросов в одном сообщении, а последовательными короткими шагами и проверкой полноты после каждого ответа.

Методика интервью выбирается не пользователем вручную, а через Adaptive Elicitation Method Selector.

Агент определяет сигналы из ответов пользователя, предлагает подходящую методику, кратко объясняет зачем она нужна, и при необходимости ждёт подтверждение пользователя.

Методика интервью является вспомогательным runbook, а не approval и не execution authorization.

Full interview depth rules are defined in `08-interview-depth-loop-and-entity-process-traversal.md`.
Adaptive method selection is defined in `09-adaptive-elicitation-method-selector.md`.
Specific interview methods are defined in `runbooks/`.

Если пользователь возвращается к пропущенному разделу, агент должен:
- открыть именно этот раздел;
- сохранить предыдущие ответы;
- дозаполнить только недостающие поля;
- обновить section_status;
- пересчитать confidence;
- обновить UNKNOWN / risks / Human Decisions Required;
- не стирать историю пропуска.

Интервью не должно превращаться в допрос.

Агент обязан периодически подводить мини-итоги, показывать что уже собрано, какие UNKNOWN остались, и почему следующий блок вопросов нужен.

Если пользователь устал, отвечает односложно или часто пропускает вопросы, агент должен предложить паузу, зафиксировать Return Points и продолжить позже.

Если пользователь сразу называет решение, технологию или цифру, агент не должен считать это готовым требованием. Сначала он уточняет проблему, которую это решение должно закрыть.

Если в проекте много сущностей, агент не должен одинаково глубоко разбирать каждую мелкую сущность. Полный Entity-Process Traversal применяется к core/risk entities, а справочники и low-risk lookup entities проходят lightweight traversal.

---

## 15. Edge Case Elicitation

The agent must not rely only on the standard happy path.
The agent must actively ask about exceptions, anomalies, hardest cases, seasonal/end-of-period cases, peak-load cases, and hidden approval flows when the project has workflow, data, access, operational, medical, legal, financial, or multi-user risk.

Примеры вопросов:
- Расскажите о последнем разе, когда процесс пошёл не так.
- Что происходит, когда стандартный процесс нарушается?
- Что происходит в конце месяца, квартала, смены или отчётного периода?
- Что происходит при пиковой нагрузке?
- Кто подключается, когда что-то идёт не по стандарту?
- Кто ещё должен это согласовать, кроме вас?
- Назовите самый сложный случай из практики.
- Какая ошибка сломает процесс первой?

---

## 16. Depth Probing for Low-Confidence Answers

```yaml
depth_probing_protocol:
  if_answer_is_generic_or_low_confidence:
    agent_must:
      - ask_one_follow_up_question
      - or_record_UNKNOWN
      - or_record_LOW_confidence
      - or_trigger_relevant_runbook
    agent_must_not:
      - force_five_whys_every_time
      - convert_low_confidence_answer_to_requirement
      - assign_HIGH_confidence_from_generic_answer
```

Invariants:
- Generic answer ≠ completed requirement.
- Low-confidence answer ≠ approved requirement.
- Follow-up question ≠ interrogation.
- Depth probing ≠ approval.

---

## 17. Change Control

Если этот документ меняется:

- нужно проверить `02-agent-contract.yaml`;
- нужно вручную пройти `07-consistency-checklist.md`;
- независимые изменения `01` или `02` без consistency review не допускаются.
