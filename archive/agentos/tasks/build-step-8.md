# Task Brief: Build Step 8

## Mode

HIGH_RISK_PROTECTED (Определено в Roadmap)

## Repository

AOS-FARM

## Branch

main (или текущая ветка)

## Risk Profile Assignment

- proposed_by_agent: HIGH_RISK_PROTECTED
- assigned_by_human: [Ожидает подтверждения]
- assignment_evidence: Требуется утверждение вместе с запуском этого шага.

## Context

На шаге 7 мы определили теорию проверок (Governance Contract). На шаге 8 мы реализуем эти проверки в виде документальной и логической структуры (Governance / Control Module v1).

## Goal

Реализовать первые control checks как progressive governance.

## Scope

Создать документ-инструкцию `agentos/docs/governance-control-module-v1.md`, описывающий как применять первые 6 гейтов:
- Scope Gate
- Evidence Gate
- Human Review Gate
- False PASS Gate
- Lifecycle Mutation Gate
- Protected/Canonical Gate

Создание `Execution Report` и `Evidence Report` по шагу 8.

## Rules

- Не заменять Human Review скриптами, если скрипты не утверждены явно. На данном этапе проверки выполняются в виде инструкций для агента/человека (policy-based validation).

## Allowed Changes

- `agentos/tasks/build-step-8.md` (этот файл)
- `agentos/docs/governance-control-module-v1.md`
- `agentos/reports/build-step-8/execution-report.md`
- `agentos/reports/build-step-8/evidence-report.md`

## Forbidden Changes

- Физическое изменение корневых файлов CI/CD или хуков git.
- Модификация существующих контрактов из шагов 1-7.

## Validation

- validator_status: NOT_RUN
- Ручная проверка политик (Gates) человеком.

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.
