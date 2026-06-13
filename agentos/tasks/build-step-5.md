# Task Brief: Build Step 5

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

Мы определили `Code Assembly Pipeline Contract` (Step 4). Теперь нам нужно собрать первый минимальный кодовый флоу в действии, но пока без автоматических валидаторов. Это **Code Assembly Pipeline MVP**.

## Goal

Собрать первый минимальный кодовый flow (задокументировать или инициализировать процессы для кодовых изменений).

## Scope

В рамках AOS-1 MVP кодового конвейера представляет собой документальное описание того, как мы применяем созданный в Step 4 контракт на практике. 
- Создание `agentos/docs/code-pipeline-mvp.md` (инструкция по прохождению кодового конвейера).
- Создание `Execution Report` и `Evidence Report` по факту выполнения шага 5.

## Rules

- Сохранять Manual Review (validator_status: NOT_RUN).
- Никакого автоматического мержа.

## Allowed Changes

- `agentos/tasks/build-step-5.md` (этот файл)
- `agentos/docs/code-pipeline-mvp.md`
- `agentos/reports/build-step-5/execution-report.md`
- `agentos/reports/build-step-5/evidence-report.md`

## Forbidden Changes

- Модификация `code-pipeline-contract.md` или `minimal-safety-floor.md`.

## Validation

- validator_status: NOT_RUN
- Ручная проверка флоу человеком.

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.
