# Governance / Control Module Contract

## Статус

```yaml
document_type: governance_module_contract
project: AOS-1 / AgentOS Next
status: active_baseline
source_pack_role: core_required
language: ru
owner: human
```

## Назначение

Данный документ определяет `Governance / Control Module` как прогрессивный модуль управления. Он не собирает проект, а выполняет функции проверки, блокировки и разделения заявлений агента (claims) от реальных решений (decisions).

Модуль добавляет проверки (Gates) поверх `Documentation Assembly Pipeline` и `Code Assembly Pipeline`.

## 1. Module Boundary (Границы ответственности)

Governance / Control Module не должен:
- Инициировать одобрение (approve) от лица человека.
- Заменять человеческое решение.
- Самостоятельно мутировать жизненный цикл (например, переводить задачу в статус `READY_FOR_EXECUTION` без проверки).
- Автоматически запускать следующий Build Step.
- Расширять Scope.
- Скрыто включать или отключать проверки (gates).

## 2. Gate List (Список шлюзов)

Модуль включает следующие контрольные шлюзы, которые будут реализованы в v1:

1. **Scope Gate**: Проверяет, что явный Scope существует, и нет скрытого его расширения (Allowed/Forbidden Changes описаны). Если scope неизвестен — `UNKNOWN_BLOCKED`.
2. **Evidence Gate**: Проверяет наличие Evidence Report. Отсутствие доказательств — `BLOCKED`.
3. **False PASS Gate**: Убеждается, что не сработали ложные допущения (`PASS ≠ approval`, `UNKNOWN ≠ OK`).
4. **Human Review Gate**: Проверяет, что там, где требуется решение человека (Risk Profile assignment, Approval), оно было явно получено. Отсутствие — `HUMAN_REVIEW_REQUIRED` или `BLOCKED`.
5. **Lifecycle Mutation Gate**: Блокирует автоматическую смену статуса без явного правила.
6. **Protected/Canonical Gate**: Защищает важные файлы. Если статус файла неизвестен — `UNKNOWN_BLOCKED`.

## 3. Risk Profile Relation

Risk Profile (профиль риска) назначается только человеком или явно разрешенным детерминированным классификатором.
- Агент может только *предложить* Risk Profile.
- Агент не имеет права самовольно назначать `LOW_RISK_FAST`.
- Если профиль не назначен или неизвестен: `UNKNOWN_BLOCKED` или `HUMAN_REVIEW_REQUIRED`.

## 4. Non-bypass Rules

Правила `Minimal Safety Floor` не могут быть отключены через Governance Module.
UNKNOWN-статус не может трактоваться как низкий риск (UNKNOWN cannot be LOW).
Если требуется человеческое решение, а человек недоступен, задача замораживается (`BLOCKED`).
