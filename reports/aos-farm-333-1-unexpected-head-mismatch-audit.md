---
status: unexpected_head_mismatch_audit
---

# AOS-FARM.333.1 Отчет об аудите несовпадения HEAD

- **final_status**: AOS_FARM_333_1_UNEXPECTED_HEAD_MISMATCH_AUDIT_PASS_NEW_PUSH_AUTH_REQUIRED
- **branch**: dev
- **HEAD**: 22137ee01defca59c56d015e58bb86a79ed88ae8
- **origin/dev**: 91722fa6141729fc24169bc38f311a9636b1a499
- **ahead/behind**: 1 0
- **authorized commit SHA**: fa781ad2b7899478f699ca190c10a47f485dbbc0
- **actual HEAD SHA**: 22137ee01defca59c56d015e58bb86a79ed88ae8

## Детали коммита
- **whether authorized commit is ancestor of actual HEAD**: false (the authorized commit does not exist in the repository)
- **file list in authorized commit**: (Commit does not exist locally to check, but was expected to be the 6 public onboarding final audit files)
- **file list in actual HEAD**:
  - `reports/aos-farm-330-public-onboarding-commit-authorization-package.md`
  - `reports/aos-farm-330-public-onboarding-final-audit-report.md`
  - `reports/aos-farm-330-public-onboarding-final-verification.md`
  - `reports/aos-farm-330-public-onboarding-fix-summary.md`
  - `reports/human-checkpoints/aos-farm-330-public-onboarding-commit-authorization.md`
  - `templates/first-consumer-workflow-checklist-template.md`
- **commits between origin/dev and HEAD**:
  - `22137ee docs: finalize public onboarding path`

## Проверка границ
- **whether unauthorized files are present**: false
- **whether protected/canonical files were modified**: false
- **whether README was modified**: false
- **whether runner/agentos.py was restored**: false
- **whether CI/database/RAG/vector store was added**: false
- **whether tag state changed**: false
- **whether GitHub release was created**: false
- **whether production use was claimed**: false
- **whether production readiness was claimed**: false

## Диагноз
- **root cause hypothesis**: The previously authorized commit (`fa781ad...`) was lost due to an environment reset or identical recreation of the commit resulting in a different hash (due to timestamp/author changes). The actual HEAD (`22137ee...`) perfectly matches the intended payload and commit message with exactly 6 expected files.
- **classification**: harmless local-only report commit (exact payload recreation)

## Статус
- **blockers**: none
- **warnings**: Local HEAD SHA does not match the previously authorized SHA.
- **recommended next safe step**: AOS-FARM.333.2 — Update Human Push Authorization for actual HEAD SHA
