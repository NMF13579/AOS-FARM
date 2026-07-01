# Task Brief (Dogfood Trial)

## Mode

LOW_RISK_FAST

## Repository

AOS-FARM

## Branch

main

## Risk Profile Assignment

- proposed_by_agent: LOW_RISK_FAST
- assigned_by_human: LOW_RISK_FAST (Разрешено заранее в рамках Build Step 6)
- assignment_evidence: Явное разрешение в Task Brief Build Step 6.

## Context

Проверка работоспособности пайплайна (Dogfood).

## Goal

Создать файл `.dogfood-test`.

## Scope

Добавление одного файла в корень.

## Rules

- PASS ≠ approval

## Allowed Changes

- `/.dogfood-test`
- `agentos/reports/build-step-6/dogfood/*`

## Forbidden Changes

- Любые другие файлы в репозитории.

## Required Behavior / Content

Файл должен содержать строку "AOS-1 Dogfood Trial".

## Non-Goals

- Выполнение сложного кода.

## Validation

- validator_status: NOT_RUN
- Ручная проверка наличия файла.

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.
