# Task Brief: Build Step 7

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

Мы убедились, что базовые конвейеры работают (Step 6). Теперь нам нужно определить `Governance / Control Module`, который будет проверять и блокировать риски поверх базовых конвейеров в виде прогрессивных шлюзов.

## Goal

Определить Governance / Control Module как отдельный progressive governance module (Создать Контракт).

## Scope

Создание документа `agentos/docs/governance-control-module-contract.md`, который будет включать:
- module boundary
- gate list (Scope Gate, Evidence Gate и т.д.)
- risk profile relation
- non-bypass rules

Создание `Execution Report` и `Evidence Report` по шагу 7.

## Rules

- Должно опираться на `Minimal Safety Floor`.
- Строгий запрет на автоматическое исполнение (это контракт, а не реализация).

## Allowed Changes

- `agentos/tasks/build-step-7.md` (этот файл)
- `agentos/docs/governance-control-module-contract.md`
- `agentos/reports/build-step-7/execution-report.md`
- `agentos/reports/build-step-7/evidence-report.md`

## Forbidden Changes

- Модификация `minimal-safety-floor.md`.

## Validation

- validator_status: NOT_RUN
- Ручная проверка контракта человеком.

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.
