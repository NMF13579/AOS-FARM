# Task Brief: Build Step 9

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

Мы формализовали шлюзы контроля (Gates). Чтобы ускорить процесс, нам нужен автоматический скрипт — тонкий валидатор (Thin Validator), который будет мгновенно проверять детерминированные вещи (формат, наличие фраз-маркеров) до того, как человек приступит к проверке. Сначала нужно определить контракт этого валидатора.

## Goal

Определить один быстрый validator для стабильных deterministic checks (Thin Validator Contract).

## Scope

Создать `agentos/docs/thin-validator-contract.md`. В нем описать правила валидации:
- required fields
- markdown/yaml structure
- forbidden claims
- fake approval phrases
- UNKNOWN/OK conflict
- NOT_RUN/PASS conflict
- protected path change markers
- evidence file existence when required

Создание `Execution Report` и `Evidence Report` по шагу 9.

## Rules

- Только один валидатор. Никаких сложных suite.
- Без автоматического исправления (no auto-fix by default).

## Allowed Changes

- `agentos/tasks/build-step-9.md` (этот файл)
- `agentos/docs/thin-validator-contract.md`
- `agentos/reports/build-step-9/execution-report.md`
- `agentos/reports/build-step-9/evidence-report.md`

## Forbidden Changes

- Написание самого скрипта валидатора (это будет на шаге 10).

## Validation

- validator_status: NOT_RUN
- Ручная проверка контракта валидатора человеком.

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.
