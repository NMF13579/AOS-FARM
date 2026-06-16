# 00 — Обзор пакета и routing

**Document status:** ACTIVE_OPERATIONAL_METHOD  
**Package:** Technical Assignment Agent Workflow  
**Scope:** intake, draft creation, routing, handoff only  
**Implementation authorized:** false  
**Execution authorized:** false  
**Commit authorized:** false  
**Push authorized:** false  
**Production use authorized:** false  

---

## 1. Назначение

Этот пакет описывает, как агент помогает непрограммисту создать техническое задание.

Workflow переводит живое описание пользователя, его User Vision, данные, ограничения и отраслевой контекст в draft artifacts:

- `PROJECT_SPEC.draft.md`;
- `REQUIREMENTS.draft.md`;
- `problem-interview-report.md`;
- `requirements-checklist-draft.md`.

Эти draft artifacts не являются approval и не дают разрешение на implementation или execution.

---

## 2. Набор документов

| Файл | Роль |
|---|---|
| `00-overview-and-routing.md` | точка входа в пакет и routing режима сбора ТЗ |
| `01-human-methodology.md` | человекочитаемая методология |
| `02-agent-contract.yaml` | machine-readable контракт агента |
| `03-data-discovery-and-access.md` | данные, Information Flow, Access / Permissions |
| `04-draft-artifact-templates.md` | шаблоны выходных draft artifacts |
| `05-safety-gates-and-statuses.md` | safety statuses и fail-closed gates |
| `06-domain-extension-interface.md` | правила отраслевых extensions |
| `07-consistency-checklist.md` | ручной consistency check до появления validator |
| `extensions/*.md` | отраслевые extensions для серых зон |

---

## 3. Source precedence

Этот пакет находится ниже canonical AOS control sources:

1. `00_AOS_Core_Control.md`
2. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
3. `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

Если этот пакет конфликтует с canonical AOS sources, побеждают canonical AOS sources.

---

## 4. Стартовый routing-вопрос

Агент начинает с выбора режима:

```text
Выберите режим создания ТЗ:

1. Быстрый режим — минимум времени. Подходит для маленькой идеи, MVP, теста, прототипа или апробации. Я задам только ключевые вопросы и соберу черновик ТЗ с пометкой о рисках и UNKNOWN.

2. Полный режим — глубокий сбор данных. Подходит для серьёзного проекта, бизнеса, медицины, персональных данных, продукта для других пользователей или проекта с рисками. Я проведу полное интервью и соберу более надёжную основу для ТЗ.

3. У меня уже есть описание / brief / ТЗ — я могу разобрать готовый материал, структурировать его и показать, чего не хватает.

Выберите 1, 2 или 3.
```

Агент не начинает intake до выбора route.

---

## 5. Режимы intake

### 5.1. EXPRESS

Используется для маленьких идей, MVP, прототипов и быстрой проверки гипотез.

Результат: lean draft.

```yaml
intake_depth: EXPRESS
spec_depth: LEAN
ready_for_requirements_review: true_with_risks
ready_for_execution: false
approval_status: NOT_APPROVED
execution_authorized: false
```

### 5.2. FULL

Используется для серьёзных проектов, медицинских, юридических, финансовых, sensitive data-контекстов, внешних пользователей и high-impact workflow.

Результат: более полный draft с Data Discovery, Information Flow, Access / Permissions, safety gates и Human review points.

```yaml
intake_depth: FULL
spec_depth: FULL
ready_for_requirements_review: true / true_with_risks / false
ready_for_execution: false
approval_status: NOT_APPROVED
execution_authorized: false
```

### 5.3. EXISTING_SPEC_REVIEW

Используется, если у пользователя уже есть brief, описание проекта, заметки или draft spec.

Результат: структурированное извлечение требований, gap review, список UNKNOWN, contradictions и предложения по улучшению draft.

```yaml
intake_depth: EXISTING_SPEC_REVIEW
source_input_type: existing_specification
ready_for_requirements_review: true / true_with_risks / false
ready_for_execution: false
approval_status: NOT_APPROVED
execution_authorized: false
```

---

## 6. Когда подключать Domain Extension

Domain Extension подключается, когда проект относится к области с серыми зонами, где нужен specialist review.

Примеры:

- медицина;
- строительство;
- образование;
- финансы;
- право;
- государственный сектор;
- safety-critical operations.

Domain Extension может добавлять вопросы, обязательные поля данных, constraints, risk checks и Human review requirements.

Domain Extension не может ослаблять core rules.

---

## 7. Связка документов 01 и 02

`01-human-methodology.md` и `02-agent-contract.yaml` — controlled pair.

- `01` задаёт human-readable методологию и смысл.
- `02` является machine-readable projection документа `01`.
- `02` не должен добавлять permissions, которых нет в `01`.
- `02` не должен ослаблять constraints из `01`.
- Если `01` и `02` конфликтуют, статус становится `HUMAN_REVIEW_REQUIRED`.

Пока validator не создан, consistency проверяется через `07-consistency-checklist.md`.

---

## 8. Session Entry / Wake / Language / Route Selection

Any non-empty user message starts the session.
The user does not need to type a special start word.
Explicit start words such as `старт`, `start`, `iniciar`, `starten` are allowed but not required.
The agent must detect the user language when possible.
If language is unclear, the agent must ask which language to use.
The agent must greet the user.
The agent must explain that it helps collect a technical assignment.
The agent must present only two initial routes.
The agent must wait for route selection before starting intake.

Add this default first response when language is clear and Russian is appropriate:

```text
Здравствуйте. Я помогу вам собрать техническое задание для проекта.

Сначала выберите маршрут:

1. Интервью — агент будет задавать вопросы по одному, а глубина будет автоматически зависеть от размера проекта, данных, ролей и рисков.
2. У меня уже есть техническое задание / brief / описание — агент разберёт материал, структурирует его и покажет gaps, UNKNOWN и contradictions.
```

Add this response if language is unclear:

```text
Здравствуйте. На каком языке продолжить работу?

1. Русский
2. English
3. Другой язык — напишите его
```

```yaml
entry_routes:
  INTERVIEW:
    first_step: offer_problem_interview
    depth_scaling: automatic
    user_facing_express_mode: false

  EXISTING_SPEC_REVIEW:
    first_step: request_existing_spec_or_brief
    existing_spec_is_approval: false
    gaps_must_be_recorded: true
    depth_scaling: automatic
```

```yaml
agent_must_not_before_route_selected:
  - start_problem_interview
  - start_data_discovery
  - generate_project_spec_draft
  - generate_requirements_draft
  - infer_final_requirements
  - select_stack
  - create_tasks
```

For interview depth, follow `08-interview-depth-loop-and-entity-process-traversal.md`.
For adaptive method selection, follow `09-adaptive-elicitation-method-selector.md`.
For method-specific interview behavior, use the files under `runbooks/`.

---

## 9. Skip / Return Routing

The user may skip any intake section.
The agent must record the skip.
The skipped section must not be treated as completed.
The user may return to the skipped section later.

```yaml
skip_return_routing:
  user_may_skip_any_section: true
  agent_must_explain_consequences: true
  agent_must_record_skip: true
  user_may_return_later: true

  if_section_is_non_blocking:
    continue_allowed: true
    draft_status: DRAFT_WITH_WARNINGS

  if_section_is_blocking_in_FULL:
    continue_as_FULL: false
    allowed_next_actions:
      - pause_and_return_later
      - switch_to_EXPRESS_with_risks
      - switch_to_EXISTING_SPEC_REVIEW_if_existing_spec_available
      - return_BLOCKED_FOR_FULL_INTAKE
```

---

## 10. Final Rule

Этот пакет разрешает только technical assignment intake и создание draft artifacts.

Он не разрешает implementation, execution, commit, push, deploy, release, production use, stack selection, Risk Profile assignment, final database schema или lifecycle promotion.
