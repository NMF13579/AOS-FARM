# Baseline Audit and Design Alignment (AOS-FARM.596)

## Gate 0 — Baseline Audit

- **Branch**: `build/aos-farm-596`
- **HEAD**: `ebc7fb103340e5f8ec5d9d27f6f4eb966da5b1d6`
- **origin/dev**: `ebc7fb103340e5f8ec5d9d27f6f4eb966da5b1d6`
- **origin/main**: `ccea6196b507e459c0c103069a1ba7ef2ae08557`
- **Ahead/Behind against origin/dev**: `0 / 0`
- **origin/main...origin/dev divergence**: `0 / 1`
- **Working Tree Status**: Clean (no tracked files modified)
- **Untracked File Status**: Unrelated old reports exist, but no dirty tracking files.
- **Required Source Availability**: Readable (`00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`)
- **Protected/Canonical Dirty Status**: Clean

**Decision**: Continue

### Approval Status Fields
```yaml
approval_claimed: false
commit_authorized: false
push_authorized: false
release_authorized: false
```

## Gate 1 — Design Alignment (Implementation Map)

### 1. Unified AOS Validate
- **Files**: `aos/scripts/aos_validate.py`, `aos/docs/VALIDATION.md`, `README.md`, `aos/docs/ROUTES.md`, `aos/docs/FIRST-SAFE-COMMANDS.md`
- **Tests**: `tests/test_aos_validate.py`
- **Validation**: `python3 -m py_compile aos/scripts/aos_validate.py`, `python3 aos/scripts/aos_validate.py all`

### 2. Safety Regression Fixtures
- **Files**: `aos/docs/SAFETY-REGRESSION-FIXTURES.md`
- **Tests**: `tests/test_aos_safety_regression.py`, `tests/fixtures/aos-safety-regression/*`
- **Validation**: `python3 -m unittest discover`

### 3. Task Intake Wizard Routing Layer
- **Files**: `aos/docs/TASK-INTAKE-WIZARD.md`, `aos/templates/intake/task-intake-classification-template.md`, `aos/templates/task-candidates/task-candidate-template.md`, `aos/START_HERE.md`, `aos/prompts/problem-intake.md`, `aos/prompts/technical-assignment-builder.md`, `aos/prompts/task-brief-builder.md`, `README.md`, `aos/docs/ROUTES.md`
- **Tests**: N/A (Documentation/Template alignment)
- **Validation**: Manual structure verification.

### 4. Review & Handoff Package Generator
- **Files**: `aos/scripts/aos_review_package.py`, `aos/docs/REVIEW-HANDOFF-PACKAGE.md`, `aos/templates/reports/review-handoff-package-template.md`
- **Tests**: `tests/test_aos_review_package.py`
- **Validation**: `python3 -m py_compile aos/scripts/aos_review_package.py`, `python3 aos/scripts/aos_review_package.py --since origin/dev`

### 5. Lessons Learned / Incident Memory
- **Files**: `aos/docs/LESSONS-LEARNED.md`, `aos/templates/lessons/lesson-entry-template.md`
- **Tests**: `tests/test_lessons_learned_docs.py`
- **Validation**: `python3 -m unittest discover`

### Explicit Out-of-Scope Confirmations
- No root 00/01/02 changes
- No staging/
- No /aos/staging/
- No script for Task Intake Wizard
- No queue mutation
- No task creation
- No approval/lifecycle semantics changes
- No Risk Profile assignment
- No validator behavior change in `aos_task_document_check.py`
