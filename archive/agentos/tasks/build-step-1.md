# Task Brief: Build Step 1

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

Мы успешно завершили Strategy Lock (Build Step 0). Теперь мы переходим к шагу 1: созданию костяка конвейера документации (Documentation Assembly Pipeline Skeleton). Это первый слой сборки, определяющий, как абстрактная идея превращается в конкретную задачу и набор отчетов.

## Goal

Зафиксировать минимальную структуру Documentation Assembly Pipeline.

## Scope

- Создание документа `agentos/docs/documentation-pipeline-skeleton.md`.
- Определение `artifact flow map`.
- Определение `document sequence`.
- Фиксация `status model`.
- Формирование списка необходимых шаблонов (required templates list).
- Создание `Execution Report` и `Evidence Report` по факту выполнения шага 1.

## Rules

- Не генерировать сами шаблоны на этом шаге (это задача Build Step 2).
- Не включать Governance/Control Module.
- Не пытаться выполнить код или создать исполняемые модули.

## Allowed Changes

- `agentos/tasks/build-step-1.md` (этот файл)
- `agentos/docs/documentation-pipeline-skeleton.md`
- `agentos/reports/build-step-1/execution-report.md`
- `agentos/reports/build-step-1/evidence-report.md`

## Forbidden Changes

- Создание самих шаблонов (будут созданы на Build Step 2).
- Модификация файлов из шага 0 (`strategy-lock.md`).

## Required Behavior / Content

- Зафиксировать структуру: Idea → Project Brief → Specification → Task Brief → Execution/Evidence Report → Human Review Package.
- Зафиксировать статусы (DRAFT, READY_FOR_REVIEW и т.д.).

## Non-Goals

- no code execution
- no runtime
- no full governance module

## Validation

- validator_status: NOT_RUN
- Ручная проверка файлов человеком (Human Review Gate).

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.

## Final Boundary Rule

No approval, no lifecycle mutation, no next-stage start unless explicitly authorized by Human.
