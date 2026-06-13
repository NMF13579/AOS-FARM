# Task Brief: Build Step 2

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

На шаге 1 мы создали скелет `Documentation Assembly Pipeline Skeleton`, в котором перечислили все необходимые шаблоны. Теперь нам нужно реализовать их физически.

## Goal

Собрать usable flow от Idea до Human Review Package (создать реальные шаблоны).

## Scope

Создание следующих шаблонов в директории `agentos/templates/`:
- `project-brief.md`
- `specification.md`
- `task-brief.md`
- `execution-report.md`
- `evidence-report.md`
- `human-review.md`

Создание `Execution Report` и `Evidence Report` по факту выполнения шага 2.

## Rules

- Сохранять формат YAML/Markdown.
- Шаблоны должны строго соответствовать правилу "PASS ≠ approval".

## Allowed Changes

- `agentos/tasks/build-step-2.md` (этот файл)
- Все файлы `.md` в папке `agentos/templates/`
- `agentos/reports/build-step-2/`

## Forbidden Changes

- Модификация файлов из шагов 0 и 1.
- Исполнение кода.

## Validation

- validator_status: NOT_RUN
- Ручная проверка структуры шаблонов.

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.
