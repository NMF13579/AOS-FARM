# Code Assembly Pipeline Contract

## Статус

```yaml
document_type: code_pipeline_contract
project: AOS-1 / AgentOS Next
status: active_baseline
source_pack_role: core_required
language: ru
owner: human
```

## Назначение

Code Assembly Pipeline — это второй слой сборки. Он отвечает за превращение `Task Brief` (из Documentation Pipeline) в конкретное изменение кода (`scoped code change`). 

Данный контракт определяет правила работы агента внутри этого конвейера до момента появления полноценного `Runtime Enforcement`.

## 1. Code Execution Package Contract

Для начала изменения кода агент должен получить `Task Brief` (статус задачи: `READY_FOR_EXECUTION` или одобрено человеком). 

Агент работает **только** в рамках `Allowed Changes`, указанных в Task Brief.
Если для выполнения задачи необходимо затронуть другие пути или файлы, это расценивается как `Scope Expansion`. 
Агент **обязан остановиться** и запросить разрешение человека (`HUMAN_REVIEW_REQUIRED`).

## 2. Diff & Evidence Expectations

По завершении изменения кода агент обязан предоставить `Evidence Report`.

Доказательства (Evidence) должны включать:
- Список измененных путей (сравнение с `Allowed Changes`).
- `git diff` или аналогичный вывод, явно демонстрирующий изменения.
- Логи сборки/тестов, если они были указаны в разделе `Validation` Task Brief.

Отсутствие Evidence (или его неполнота) приводит к автоматическому переходу задачи в статус `BLOCKED`.

## 3. Allowed / Forbidden Change Handling

**Поведение при попытке нарушить Scope:**
- Если агент пытается модифицировать файл из `Forbidden Changes`, он должен прервать операцию (перевести статус в `BLOCKED` и уведомить человека).
- Если изменение требуется, но оно не указано ни в `Allowed`, ни в `Forbidden` (серая зона), это трактуется как `UNKNOWN_BLOCKED`. Требуется явное решение человека для расширения Scope.

**Destructive Operations:**
Удаление файлов, переименование, перезапись истории (force-push) запрещены по умолчанию, если профиль риска задачи не равен `DESTRUCTIVE_OR_CANONICAL` и явно не авторизован человеком.

## 4. Manual Review Requirement

До момента реализации физического валидатора (Validator Script) и CI Quality Gates:
**Каждое изменение кода требует ручной проверки (Manual Human Review).**

Статус `NOT_RUN` (если автоматическая валидация недоступна) **не может** рассматриваться как `PASS`. 
Агент может формировать `Execution Report`, но итоговое решение о слиянии (merge) принимает только человек.
