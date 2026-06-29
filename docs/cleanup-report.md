# Cleanup Report

## Выполненные действия

- Созданы папки: `docs/`, `docs/references/`, `archive/`.
- Конвертированы и перемещены в `docs/` файлы:
  - `Адреса проектов.txt` → `docs/project-pointers.md`
  - `Архитектура.txt` → `docs/architecture-notes.md`
  - `Скелет архитектуры.txt` → `docs/architecture-skeleton.md`
- Оригинальные `.txt` файлы перемещены в `archive/` и удалены из корня.
- Обновлён `README.md` — добавлена секция `## Repository Structure`.
- Созданный ранее `constitution.md` placeholder больше не является активным источником правил; он superseded/removed и заменён текущими canonical control sources: `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.

## Файлы, которые не трогал и почему

- `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`, `03_AOS_Future_and_Legacy_Reference_OPTIONAL.md` — canonical файлы; правило безопасности запрещает их переименование или изменение без явного разрешения Human.
- `llms.txt` — машинно-читаемый контекст; не изменял по условию задачи.
- `.git/` и метаданные репозитория — не изменял.

## Вопросы, требующие решения Human

- Подтвердите, что содержимое `docs/*.md` может оставаться без изменений (только расширено заголовком), или укажите правки.
- Stale item resolved: создание окончательной `constitution.md` больше не требуется; replacement authority — `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
- Разрешаете ли вы запуск `uvx specify init` в этом репозитории для инициализации Spec Kit (раньше команда вызывала интерактивный prompt). По безопасности: я не запускаю `specify init` без явного указания Human.
- Хотите, чтобы я закоммитил и запушил эти изменения или оставить их unstaged?
