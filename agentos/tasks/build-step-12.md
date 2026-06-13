# Task Brief: Build Step 12

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

Это финальный шаг базовой сборки. Мы построили pipelines, safety rules, validator и спланировали runtime enforcement. Теперь нам нужно подвести итоги (Hardening from Evidence), проанализировав весь процесс (включая Dogfood trial), чтобы определить, где мы должны усилить систему в будущем.

## Goal

Определить hardening priorities (приоритеты усиления безопасности) на основе собранного опыта (Evidence).

## Scope

Создать документ `agentos/docs/hardening-priorities.md`, который зафиксирует:
- missing guardrails list (чего сейчас не хватает).
- validator gaps (что валидатор еще не умеет ловить).
- template improvements (что улучшить в шаблонах).
- roadmap adjustments (какие шаги нужны дальше).

Создать финальные `Execution Report` и `Evidence Report` по шагу 12.

## Rules

- Только анализ и планирование. Без изменения самих шаблонов и скриптов в рамках этого шага.

## Allowed Changes

- `agentos/tasks/build-step-12.md` (этот файл)
- `agentos/docs/hardening-priorities.md`
- `agentos/reports/build-step-12/execution-report.md`
- `agentos/reports/build-step-12/evidence-report.md`

## Forbidden Changes

- Удаление старых отчетов.
- Изменение текущего скрипта валидатора.

## Validation

- validator_status: NOT_RUN
- Ручная проверка приоритетов человеком.

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.
