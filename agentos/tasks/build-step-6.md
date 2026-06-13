# Task Brief: Build Step 6

## Mode

MEDIUM_RISK_GUIDED (Определено в Roadmap)

## Repository

AOS-FARM

## Branch

main (или текущая ветка)

## Risk Profile Assignment

- proposed_by_agent: MEDIUM_RISK_GUIDED
- assigned_by_human: [Ожидает подтверждения]
- assignment_evidence: Требуется утверждение вместе с запуском этого шага.

## Context

Мы собрали `Documentation Assembly Pipeline` и `Code Assembly Pipeline`. Пришло время проверить их работу на практике (First Dogfood Trial).

## Goal

Прогнать один реальный low-risk internal task через конвейеры документации и кода.

## Scope

- Сгенерировать тренировочную задачу (например: "Создать пустой файл `.dogfood-test` в корне проекта").
- Провести задачу через все шаблоны от Project Brief до Evidence Report.
- Все тестовые артефакты сохранить в `agentos/reports/build-step-6/dogfood/`.
- Подготовить `Execution Report` и `Evidence Report` по факту выполнения шага 6.

## Rules

- low-risk only
- no protected/canonical change (кроме добавления тестового файла).
- no destructive operation
- no auto-approval
- no merge
- Evidence required
- human review required

## Allowed Changes

- `agentos/tasks/build-step-6.md` (этот файл)
- `agentos/reports/build-step-6/dogfood/*` (все артефакты догфуда)
- Корневой файл `.dogfood-test` (или аналогичный).
- `agentos/reports/build-step-6/execution-report.md`
- `agentos/reports/build-step-6/evidence-report.md`

## Forbidden Changes

- Модификация любых других файлов в репозитории.

## Validation

- validator_status: NOT_RUN
- Ручная проверка флоу человеком.

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.
