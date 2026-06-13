# Thin Validator Contract

## Статус

```yaml
document_type: thin_validator_contract
project: AOS-1 / AgentOS Next
status: active_baseline
source_pack_role: core_required
language: ru
owner: human
```

## Назначение

Thin Validator — это автоматический скрипт (будет реализован на шаге 10), предназначенный для мгновенной `deterministic` проверки базовых правил безопасности перед тем, как человек приступит к Manual Review.

Валидатор не заменяет человека, но гарантирует, что к человеку не попадут отчеты с очевидными нарушениями `Minimal Safety Floor`.

## Правила Валидации (Validation Checks)

Скрипт должен проверять следующие условия:

1. **Required Fields & Structure**: 
   - Все markdown-файлы в `agentos/reports` и `agentos/tasks` должны содержать блок `Metadata` в формате YAML (или эквивалентном).
   - Обязательные поля: `status`, `risk_profile` (для отчетов), `task`.
2. **Forbidden Claims / Fake Approval Phrases**:
   - Агенту запрещено писать `approved: true`, `decision: APPROVED` или аналогичные фразы в файлах Evidence / Execution Report.
   - Исключением являются файлы `Human Review`, но они должны физически подтверждаться git commit-ом от авторизованного пользователя (в MVP проверяется только отсутствие фраз в отчетах агента).
3. **UNKNOWN/OK Conflict**:
   - Если статус поля или состояние задачи `UNKNOWN`, общий статус валидатора не может быть `PASS` (он должен падать с ошибкой).
4. **NOT_RUN/PASS Conflict**:
   - Поле `validator_status: NOT_RUN` не может сопровождаться фразами о том, что валидация пройдена (`PASS`). Скрипт должен выявлять такие логические противоречия.
5. **Protected Path Change Markers**:
   - Скрипт должен проверять Evidence (дифф/список путей). Если затронуты пути из списка `protected` (например, `agentos/docs/minimal-safety-floor.md`), статус задачи должен строго требовать `HIGH_RISK_PROTECTED` и checkpoint. Если профиль ниже — валидатор падает.
6. **Evidence File Existence**:
   - Если Execution Report переведен в статус `READY_FOR_REVIEW`, скрипт обязан проверить физическое наличие соответствующего `Evidence Report`. Если файла нет — ошибка.

## Non-goals (Чего валидатор не делает)

- Он **не исправляет** ошибки автоматически (no auto-fix).
- Он **не анализирует смысл** текста или качество кода.
- Он **не выполняет** unit-тесты (это задача Code Pipeline).
