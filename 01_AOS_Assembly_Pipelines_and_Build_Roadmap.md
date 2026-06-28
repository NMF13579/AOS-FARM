# 01 — AOS Assembly Pipelines and Build Roadmap

## Статус

```yaml
document_type: assembly_pipelines_and_build_roadmap
project: AOS-FARM
status: active_assembly_pipeline_and_build_order
source_pack_role: core_required
language: ru
version: v5.4-final-min
pack_date: "2026-06-10"
owner: human / NMF13579
authorized_to_modify: human only
```

## Назначение

Этот документ определяет:

```text
Documentation Assembly Pipeline
Code Assembly Pipeline
Build Step roadmap
daily workflow
role matrix
first dogfood flow
```

Он не определяет detailed governance/control gates. Это зона документа:

```text
02_AOS_Governance_Control_Module_and_Safety_Rules.md
```

## Главная формула

```text
Documentation Assembly Pipeline задаёт рамки.
Code Assembly Pipeline строит код внутри этих рамок.
Minimal Safety Floor действует с первого дня.
Governance / Control Module усиливает контроль отдельно.
```

## Product Folder Boundaries

Следующие границы структуры проекта строго определены:

```text
Product folder AOS = /aos/
/aos/root/AGENTS.md = template for target project root AGENTS.md
Root 00/01/02 = AOS-FARM development canonical sources, not consumer runtime prerequisites.
agentos/ = internal/reference layer, not consumer first-start path.
legacy AgentOS = must not be imported into AOS-FARM and may be used only as reference.
```

## Local Temporary Workspace Boundary

AOS-FARM repo and target projects use root-level `/.aos-tmp/` for temporary command outputs, scratch logs, and local disposable intermediate files.

The `/.aos-tmp/` directory is:
* local-only
* ignored by git
* disposable
* not Source of Truth
* not Evidence storage
* not approval storage
* not checkpoint storage
* not canonical documentation storage

Evidence, reports, approvals, checkpoints, protected/canonical files, and lifecycle artifacts must never be stored in `/.aos-tmp/`.
Temporary command outputs must not be written into repo root or inside `/aos/`.

## Assembly Core

Assembly Core состоит из двух pipeline:

```text
Documentation Assembly Pipeline
Code Assembly Pipeline
```

Оба pipeline работают под `Minimal Safety Floor`.

Assembly Core не должен:

```text
approve
симулировать human approval
мутировать lifecycle сам
расширять scope
делать commit/merge/release без явного human authorization
обходить Minimal Safety Floor
```

## Documentation Assembly Pipeline

Documentation Assembly Pipeline — первый слой сборки.

Он отвечает за:

```text
Idea
→ Project Brief
→ Specification
→ Task Brief
→ Execution Package
→ Execution Report
→ Evidence Report
→ Human Review Package
```

Назначение:

```text
превратить идею в понятные документы, scope, задачу, Evidence и review package
```

Он не пишет код сам по себе.

Он не approve.

## Code Assembly Pipeline

Code Assembly Pipeline — второй слой сборки.

Он работает только после появления scoped task.

Поток:

```text
Task Brief
→ scoped code change
→ diff
→ checks / tests
→ Execution Report
→ Evidence Report
→ Human Review
```

Назначение:

```text
собрать кодовое изменение строго в рамках Task Brief
```

Он не может расширять scope, даже если это кажется полезным.

Если scope недостаточен:

```text
HUMAN_REVIEW_REQUIRED
```

или:

```text
UNKNOWN_BLOCKED
```

## Minimal Safety Floor in Both Pipelines

Оба pipeline всегда обязаны соблюдать:

```text
PASS ≠ approval
Evidence ≠ approval
CI PASS ≠ approval
UNKNOWN ≠ OK
NOT_RUN ≠ PASS
Human approval cannot be simulated
Scope must not expand without human permission
Protected/canonical changes require human checkpoint
Destructive operations are forbidden by default
Agent cannot self-assign LOW_RISK_FAST
```

## Роли артефактов

| Артефакт | Что делает | Что не делает |
|---|---|---|
| Idea | фиксирует намерение | не является scope |
| Project Brief | описывает проблему, цель, ограничения | не является task approval |
| Specification | описывает expected behavior | не разрешает execution |
| Task Brief | задаёт scope, allowed/forbidden changes и validation | не является approval |
| Execution Package | даёт агенту рабочий контекст | не даёт merge/approval permission |
| Code Diff | показывает proposed implementation | не является approval |
| Execution Report | фиксирует agent claim | не является proof сам по себе |
| Evidence Report | фиксирует proof artifacts | не является approval |
| Human Review | оценивает result и Evidence | не является автоматической lifecycle mutation |
| Human Approval | scoped human decision | не создаётся агентом |

## Assembly / Control / Human

| Слой | Простыми словами | Пример |
|---|---|---|
| Documentation Assembly Pipeline | собирает документы | brief, spec, task, evidence |
| Code Assembly Pipeline | собирает scoped code change | diff, checks, report |
| Minimal Safety Floor | не даёт системе врать | PASS ≠ approval, UNKNOWN ≠ OK |
| Governance / Control Module | проверяет и блокирует риски | scope gate, evidence gate, false PASS gate |
| Human Decision | принимает решение | approve, reject, request changes |

## Human Availability Rule

Если required human review, approval, checkpoint или Risk Profile assignment недоступны:

```text
status: BLOCKED
```

или:

```text
status: HUMAN_REVIEW_REQUIRED
```

Агент не продолжает через предположение.

## Минимальный MVP-проход

```text
1. Idea
2. Project Brief
3. Specification
4. Task Brief
5. Human assigns Risk Profile
6. Agent executes only scoped task
7. Code Diff if code was changed
8. Execution Report
9. Evidence Report
10. Human Review
11. Human Approval / Rejection
```

Если на любом шаге появляется unknown:

```text
UNKNOWN_BLOCKED
```

или:

```text
HUMAN_REVIEW_REQUIRED
```

## Типовые статусы

| Status | Значение |
|---|---|
| DRAFT | черновик |
| READY_FOR_REVIEW | можно проверять |
| READY_FOR_EXECUTION | готово к выполнению, если нет blockers |
| EXECUTION_REPORTED | агент отчитался |
| EVIDENCE_RECORDED | Evidence приложен |
| HUMAN_REVIEW_REQUIRED | нужен человек |
| APPROVED | человек явно approve |
| REJECTED | человек reject |
| BLOCKED | продолжать нельзя |
| UNKNOWN_BLOCKED | неизвестность блокирует |

## Build Step Roadmap

## Build Step 0 — Strategy Lock

Цель:

```text
зафиксировать final assembly-first strategy и сохранить dev skeleton baseline
```

Outputs:

```text
Strategy Lock
branch strategy
old milestone-heavy plan marked as reference only
```

Non-goals:

```text
no runtime
no cleanup
no implementation
no protected changes
no stage execution
```

## Build Step 1 — Documentation Assembly Pipeline Skeleton

Цель:

```text
зафиксировать минимальную структуру Documentation Assembly Pipeline
```

Outputs:

```text
artifact flow map
document sequence
status model
required templates list
```

Non-goals:

```text
no code execution
no runtime
no full governance module
```

## Build Step 2 — Documentation Assembly Pipeline MVP

Цель:

```text
собрать usable flow от Idea до Human Review Package
```

Outputs:

```text
Project Brief template
Specification template
Task Brief template
Execution Report template
Evidence Report template
Human Review template
```

## Build Step 3 — Minimal Safety Floor Formalization

Цель:

```text
формально закрепить always-on safety semantics для documentation и code flows
```

Must include:

```text
PASS ≠ approval
Evidence ≠ approval
CI PASS ≠ approval
UNKNOWN ≠ OK
NOT_RUN ≠ PASS
no fake human approval
no auto-merge
no auto-commit
no lifecycle mutation without rule
no protected/canonical change without checkpoint
```

Важно:

```text
Minimal Safety Floor действует с Build Step 0.
Build Step 3 только формализует и проверяет его, а не включает впервые.
```

## Build Step 4 — Code Assembly Pipeline Contract

Цель:

```text
определить как Task Brief превращается в scoped code change
```

Outputs:

```text
code execution package contract
diff/evidence expectations
allowed/forbidden change handling
manual review requirement
```

Non-goals:

```text
no runtime enforcement yet
no broad validator suite
no automatic merge
```

## Build Step 5 — Code Assembly Pipeline MVP

Цель:

```text
собрать первый минимальный кодовый flow
```

Flow:

```text
Task Brief
→ scoped code change
→ diff
→ checks/tests if available
→ Execution Report
→ Evidence Report
→ Human Review
```

Before validator implementation:

```text
manual human review is mandatory
validator_status: NOT_RUN
NOT_RUN must not be treated as PASS
Evidence required
```

## Build Step 6 — First Dogfood Trial

Цель:

```text
прогнать один реальный low-risk internal task через documentation и code pipelines
```

Rules:

```text
low-risk only
human-assigned profile only
no protected/canonical change
no destructive operation
no auto-approval
no merge
Evidence required
human review required
```

## Build Step 7 — Governance / Control Module Contract

Цель:

```text
определить Governance / Control Module как отдельный progressive governance module
```

Outputs:

```text
module boundary
gate list
risk profile relation
non-bypass rules
```

## Build Step 8 — Governance / Control Module v1

Цель:

```text
реализовать первые control checks как progressive governance
```

Initial gates:

```text
Scope Gate
Evidence Gate
Human Review Gate
False PASS Gate
Lifecycle Mutation Gate
Protected/Canonical Gate
```

## Build Step 9 — Thin Validator Contract

Цель:

```text
определить один быстрый validator для стабильных deterministic checks
```

Checks:

```text
required fields
markdown/yaml structure
forbidden claims
fake approval phrases
UNKNOWN/OK conflict
NOT_RUN/PASS conflict
protected path change markers
evidence file existence when required
```

## Build Step 10 — Thin Validator Implementation

Цель:

```text
реализовать один быстрый validator для заданных deterministic checks
```

Граница:

```text
One validator first.
No broad script suite.
No runtime enforcement yet.
No auto-fix by default.
```

## Build Step 11 — Runtime Enforcement Planning

Цель:

```text
спланировать future Runtime Enforcement без внедрения раньше времени
```

Potential future components:

```text
command allowlist
write allowlist
protected path guard
commit/push guard
audit log
token scope policy
sandbox execution
```

## Build Step 12 — Hardening From Evidence

Цель:

```text
определить hardening priorities на основе dogfood Evidence
```

Potential outputs:

```text
missing guardrails list
validator gaps
template improvements
false PASS risks
runtime enforcement candidates
roadmap adjustments
```

## Как завести новый проект

```text
1. Создай Project Brief.
2. Опиши проблему, пользователя, цель и ограничения.
3. Не называй это approval.
4. Перейди к Specification.
5. Если scope неясен — UNKNOWN_BLOCKED.
```

## Как описать feature

```text
1. Создай feature note или spec draft.
2. Попроси AI помочь структурировать.
3. Human назначает Risk Profile.
4. Если это просто идея — LOW_RISK_FAST возможен только если human явно назначил этот Risk Profile.
5. Если это меняет roadmap/architecture/runtime — минимум HIGH_RISK_PROTECTED.
```

## Как поручить task агенту

```text
1. Создай Task Brief.
2. Укажи Goal.
3. Укажи Scope.
4. Укажи Allowed Changes.
5. Укажи Forbidden Changes.
6. Укажи Validation.
7. Укажи Expected Final Report.
8. Human назначает Risk Profile.
9. Только после этого можно обсуждать execution.
```

## Можно ли выполнять?

Проверь:

```text
есть ли clear scope?
есть ли allowed/forbidden changes?
назначен ли Risk Profile человеком?
есть ли validation или явно указан validator_status: NOT_RUN?
не затрагиваются ли protected/canonical files?
нет ли destructive operations?
нет ли UNKNOWN?
```

Если ответ на любой пункт неизвестен:

```text
UNKNOWN_BLOCKED
```

или:

```text
HUMAN_REVIEW_REQUIRED
```

## Первые практические tasks

| Task | Build Step | Цель | Минимальный Risk Profile |
|---|---|---|---|
| Task 0 | 0 | Strategy Lock | HIGH_RISK_PROTECTED |
| Task 1 | 1 | Documentation Assembly Pipeline Skeleton | MEDIUM_RISK_GUIDED |
| Task 2 | 2 | Documentation Assembly Pipeline MVP | MEDIUM_RISK_GUIDED |
| Task 3 | 3 | Minimal Safety Floor Formalization | HIGH_RISK_PROTECTED |
| Task 4 | 4 | Code Assembly Pipeline Contract | MEDIUM_RISK_GUIDED |
| Task 5 | 5 | Code Assembly Pipeline MVP | MEDIUM_RISK_GUIDED |
| Task 6 | 6 | First Dogfood Trial | LOW_RISK_FAST или MEDIUM_RISK_GUIDED, human-assigned |
| Task 7 | 7 | Governance / Control Module Contract | HIGH_RISK_PROTECTED |

## Финальная граница

Этот документ объясняет assembly pipelines, build roadmap и daily workflow.

Он не является approval.

Он не авторизует execution.

Он не ослабляет Minimal Safety Floor.

Для safety/control conflicts `02_AOS_Governance_Control_Module_and_Safety_Rules.md` имеет domain authority, если `00_AOS_Core_Control.md` явно не говорит иначе.
