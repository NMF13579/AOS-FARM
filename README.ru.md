<div align="center">
  <h1>AOS-FARM</h1>
  <p><b>Создавайте с AI-агентами быстрее — не теряя человеческого контроля.</b></p>

  [![Install / First Run](https://img.shields.io/badge/Install_/_First_Run-000000?style=for-the-badge&logo=github&logoColor=white)](docs/user-guide/installation-clone-first-run-guide.md)
  [![Quickstart](https://img.shields.io/badge/Quickstart-000000?style=for-the-badge&logo=rocket&logoColor=white)](docs/user-guide/quickstart.md)
  [![Templates](https://img.shields.io/badge/Templates-000000?style=for-the-badge&logo=files&logoColor=white)](templates/)
  [![Project Map](https://img.shields.io/badge/Project_Map-000000?style=for-the-badge&logo=map&logoColor=white)](docs/user-guide/project-map.md)
  [![Safety](https://img.shields.io/badge/Safety-000000?style=for-the-badge&logo=shield&logoColor=white)](docs/governance/minimal-safety-floor.md)
  [![English](https://img.shields.io/badge/English-000000?style=for-the-badge)](README.md)
</div>

---

AOS-FARM — это Markdown-first фреймворк для безопасных AI-проектов и vibe-coding. Он помогает превращать идеи в контролируемые задачи (Task Brief), собирать доказательства (Evidence), устанавливать чекпоинты (Human Checkpoints) и создавать процессы, полностью подконтрольные человеку.

## ⚠️ Какую боль решает?
AI-агенты работают быстро, но создают риски:
- скрыто расширяют scope;
- путают PASS (успешный тест) с approval (одобрением человека);
- считают отчеты принятыми решениями;
- пушат опасные изменения lifecycle до того, как человек их поймет;
- смешивают Evidence, validation и approval.

AOS-FARM добавляет **строгие границы процесса** (controlled workflow boundaries), чтобы человек всегда сохранял полный контроль (Source of Truth).

## 🎯 Для кого это?
- vibe-coders;
- не-программистов, создающих продукты с помощью AI-агентов;
- соло-фаундеров;
- product owners;
- пользователей GPT / Codex / Cursor / Antigravity / Claude Code;
- команд, которым нужны легковесные, подконтрольные человеку AI-процессы.

**Не для:**
- полностью автономного деплоя в продакшен;
- замены человеческого ревью (human review);
- слепых auto-merge / auto-release процессов.

## ⚙️ Как работает
1. **Idea**
2. **Task Brief**
3. **Scope + Forbidden Changes**
4. **Dry Run / Evidence**
5. **Human Checkpoint**
6. **Controlled Execution**
7. **Verification**
8. **Commit / Push** (только после явного human authorization)

## ⏱️ Первые 10 минут
1. Склонируйте репозиторий.
2. Откройте его в IDE.
3. Прочитайте [Quickstart](docs/user-guide/quickstart.md).
4. Откройте [Project Map](docs/user-guide/project-map.md).
5. Откройте [Installation / First Run Guide](docs/user-guide/installation-clone-first-run-guide.md).
6. Выберите шаблон из папки [templates](templates/).
7. Попросите GPT или агента IDE выступить в роли AOS-FARM Tutor.
8. Сначала запустите только dry-run (прогон без изменений).
9. Остановитесь до commit / push, если нет явного human authorization.

## 🎓 Tutor Mode
Отправьте этот промпт вашему AI-ассистенту для безопасного старта:
```text
Act as AOS-FARM Tutor.
Guide me through my first dry-run.
Do not execute, stage, commit, push, merge, release, or approve anything.
Explain each approval boundary before risky steps.
```

## 🛡️ Границы безопасности (Safety boundaries)
AOS-FARM требует соблюдать строгий Minimal Safety Floor с первого дня:
- **PASS ≠ approval**
- **Evidence ≠ approval**
- **CI PASS ≠ approval**
- **UNKNOWN ≠ OK** (если состояние неизвестно — это BLOCKED)
- **NOT_RUN ≠ PASS**
- **Human approval cannot be simulated** (агент не может подделать решение человека)
- **Destructive operations are forbidden by default**

## 🚫 Что AOS-FARM не делает
AOS-FARM **не выполняет автоматически**:
- approve задач;
- запуск агентов (runner);
- stage изменений;
- commit;
- push;
- merge;
- создание релизов;
- заявление о готовности к продакшену (production readiness);
- замену суждений человека.

## 🗺️ Карта документации

| Документ | Назначение |
|----------|------------|
| [Installation / First Run](docs/user-guide/installation-clone-first-run-guide.md) | Безопасный старт и установка |
| [Quickstart](docs/user-guide/quickstart.md) | Верхнеуровневый обзор системы |
| [Project Map](docs/user-guide/project-map.md) | Навигация по файлам |
| [Glossary](docs/user-guide/glossary.md) | Важные термины |
| [Walkthrough](docs/user-guide/quickstart-example-walkthrough.md) | Пример контролируемой задачи |
| [Templates](templates/) | Шаблоны задач (Task Brief) и чекпоинтов |
| [Approval Boundary](docs/governance/pass-evidence-approval-boundary.md) | Почему PASS — это не approval |
| [Minimal Safety Floor](docs/governance/minimal-safety-floor.md) | Базовые правила безопасности |

## 📊 Текущий статус проекта
- **Public onboarding**: в процессе подготовки
- **Template trial**: в процессе подготовки
- **Production readiness**: не заявлена (not claimed)
- **Release approval**: не выдано (not granted)
- **Runner**: отложен (deferred)
- **Human approval required for lifecycle actions**
