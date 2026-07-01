# Task Brief: Build Step 3

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

После создания шаблонов (Step 2) нам необходимо формально закрепить фундамент безопасности конвейеров: `Minimal Safety Floor`. Этот документ будет диктовать жесткие правила для агента и людей, предотвращая нарушения.

## Goal

Формально закрепить always-on safety semantics для documentation и code flows.

## Scope

- Создание документа `agentos/docs/minimal-safety-floor.md`.
- Создание `Execution Report` и `Evidence Report` по факту выполнения шага 3.

## Rules

Must include (Обязательно включить в документ):
- PASS ≠ approval
- Evidence ≠ approval
- CI PASS ≠ approval
- UNKNOWN ≠ OK
- NOT_RUN ≠ PASS
- no fake human approval
- no auto-merge
- no auto-commit
- no lifecycle mutation without rule
- no protected/canonical change without checkpoint

## Allowed Changes

- `agentos/tasks/build-step-3.md` (этот файл)
- `agentos/docs/minimal-safety-floor.md`
- `agentos/reports/build-step-3/execution-report.md`
- `agentos/reports/build-step-3/evidence-report.md`

## Forbidden Changes

- Модификация шаблонов из шага 2.
- Исполнение кода.

## Validation

- validator_status: NOT_RUN
- Ручная проверка текста документа человеком.

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.
