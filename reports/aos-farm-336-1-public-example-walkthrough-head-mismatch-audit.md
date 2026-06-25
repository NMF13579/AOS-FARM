---
status: unexpected_head_mismatch_audit
---

# AOS-FARM.336.1 Отчет об аудите несовпадения HEAD и переподготовке пакета авторизации

- **expected old commit SHA**: 4ad5c404af251ff9e246fc0b91e1d3ce3021f062
- **actual HEAD SHA**: 19afa462c688983c4648daf95723de540cc62277
- **origin/dev SHA**: 22137ee01defca59c56d015e58bb86a79ed88ae8
- **ahead/behind state**: dev ahead of origin/dev by 1, behind by 0
- **actual HEAD committed files**:
  - `docs/user-guide/quickstart-example-walkthrough.md`
  - `templates/example-first-controlled-task-brief.md`
  - `reports/aos-farm-334-public-example-walkthrough-report.md`
  - `reports/aos-farm-334-public-example-walkthrough-verification.md`
  - `reports/aos-farm-334-public-example-walkthrough-commit-authorization-package.md`
  - `reports/human-checkpoints/aos-farm-334-public-example-walkthrough-commit-authorization.md`
- **expected six-file set**: (см. список выше, они полностью совпадают)
- **whether actual HEAD matches authorized scope**: Да, актуальный HEAD содержит ровно те же 6 файлов.
- **whether forbidden scope was detected**: Нет, запрещенные изменения отсутствуют.
- **whether push may be re-authorized for actual HEAD**: Да, можно запросить авторизацию push для `19afa462c688983c4648daf95723de540cc62277`.
- **confirmation that push was not performed**: Подтверждаю, пуш НЕ выполнялся.
