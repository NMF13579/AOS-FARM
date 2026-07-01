# Hardening Priorities (Based on Evidence)

## Статус

```yaml
document_type: hardening_priorities
project: AOS-1 / AgentOS Next
status: active_baseline
source_pack_role: core_required
language: ru
owner: human
```

## Назначение

На основе пройденных этапов с 0 по 11 (включая тренировочный запуск Dogfood), этот документ определяет приоритеты для дальнейшего усиления системы (Hardening).

## 1. Missing Guardrails List (Отсутствующие ограждения)

- **Отсутствует физическая блокировка коммитов:** Сейчас мы опираемся на контракт. Если агент (или человек) сделает `git push --force` в обход правил, система это не заблокирует физически.
- **Отсутствует изоляция песочницы (Sandbox):** Команды `run_command` всё ещё имеют полный доступ ко всему окружению пользователя, что представляет риск.

## 2. Validator Gaps (Пробелы в валидаторе)

- **Отсутствие кросс-файловой аналитики:** Наш скрипт `thin_validator.py` проверяет каждый файл изолированно. Он не может проверить, что Evidence Report действительно соответствует Execution Report и Task Brief (сравнение содержимого diff с Allowed Changes).
- **Слепота к реальному Git-статусу:** Валидатор читает только Markdown. Он не делает `git diff` для верификации того, что агент действительно не трогал другие файлы.

## 3. Template Improvements (Улучшения шаблонов)

- В `Evidence Report` необходимо добавить обязательное поле для вставки вывода `git status` и хеша коммита (если коммит был), чтобы Evidence был более надежным.
- В `Task Brief` добавить явное поле `Sandbox Mode`, чтобы агент четко знал, какие папки открыты на чтение, а какие — на запись.

## 4. Roadmap Adjustments (Дальнейшие шаги)

На основе этого анализа предлагается включить следующие шаги в будущий Roadmap:
1. **Build Step 13**: Интеграция `thin_validator.py` в локальный `pre-commit` хук.
2. **Build Step 14**: Разработка скрипта `Scope Validator`, который будет физически сверять `git diff` с полем `Allowed Changes` из Task Brief.
3. **Build Step 15**: Изоляция `run_command` (Runtime Enforcement Implementation).

На этом базовая загрузка архитектуры AOS-1 считается успешно завершенной.
