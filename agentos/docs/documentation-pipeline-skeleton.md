# Documentation Assembly Pipeline Skeleton

## Статус

```yaml
document_type: pipeline_skeleton
project: AOS-1 / AgentOS Next
status: active_baseline
source_pack_role: core_required
language: ru
owner: human
```

## 1. Artifact Flow Map & Document Sequence

Конвейер документации переводит абстрактную идею в строго заданную задачу и завершается формированием пакета для проверки человеком.

```text
1. Idea / Feature Draft (Неструктурированный замысел)
   ↓
2. Project Brief (Описание проблемы, пользователя, цели и ограничений)
   ↓
3. Specification (Expected behavior, технические рамки)
   ↓
4. Task Brief (Строгий Scope, Allowed/Forbidden Changes, Validation Rules, Risk Profile)
   ↓
[EXECUTION / КОДОВЫЙ КОНВЕЙЕР ИДЕТ ЗДЕСЬ, ЕСЛИ ПРИМЕНИМО]
   ↓
5. Execution Report (Отчет агента о проделанной работе)
   ↓
6. Evidence Report (Доказательства: логи, диффы, статус валидатора)
   ↓
7. Human Review Package (Сборка для окончательного принятия решения человеком)
```

## 2. Status Model

Любая задача или документ внутри конвейера может находиться в одном из следующих состояний:

| Status | Значение |
|---|---|
| `DRAFT` | Черновик, в процессе подготовки. |
| `READY_FOR_REVIEW` | Документ готов, ожидается проверка человеком. |
| `READY_FOR_EXECUTION` | Задача утверждена и может быть взята в работу агентом (нет blockers). |
| `EXECUTION_REPORTED` | Агент выполнил задачу и отчитался. |
| `EVIDENCE_RECORDED` | Доказательства приложены к отчету. |
| `HUMAN_REVIEW_REQUIRED` | Требуется вмешательство/решение человека (Safety Floor Gate). |
| `APPROVED` | Явное одобрение человеком (переход на следующий шаг). |
| `REJECTED` | Отклонено человеком. |
| `BLOCKED` | Продолжать выполнение нельзя (нехватка данных/допусков). |
| `UNKNOWN_BLOCKED` | Неопределенность блокирует дальнейшие действия. |

## 3. Required Templates List

Для того чтобы Documentation Assembly Pipeline мог функционировать, в рамках **Build Step 2** необходимо будет создать следующие шаблоны (templates):

1. **Project Brief Template** (`agentos/templates/project-brief.md`)
2. **Specification Template** (`agentos/templates/specification.md`)
3. **Task Brief Template** (`agentos/templates/task-brief.md`)
4. **Execution Report Template** (`agentos/templates/execution-report.md`)
5. **Evidence Report Template** (`agentos/templates/evidence-report.md`)
6. **Human Review Template** (`agentos/templates/human-review.md`)

## Границы ответственности
Данный скелет не реализует сами шаблоны и не исполняет код. Он лишь задает структурную основу для сборки документов в AOS-1.
