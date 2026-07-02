# Agentic Operating System (AOS-FARM)

**Надежный фреймворк для безопасной разработки с AI-агентами.**
**The secure framework for AI-driven software development.**

AOS-FARM помогает безопасно работать с AI-помощниками (агентами). Он не дает агенту делать скрытые действия, менять важные файлы без спроса или выдавать успешные тесты за ваше одобрение.

*Note: Этот README.md служит исключительно для навигации (README is navigation only). Этот файл не предоставляет никаких execution authorization. Он не заявляет о production readiness или runtime readiness.*

## 🇷🇺 Русскоязычный вход
Первичная документация и пути инициализации сделаны с приоритетом русского языка (Russian first-class entry).

## ⏱️ Первые 5 минут
* Если вы впервые здесь: [Начать](aos/docs/START-RU.md)
* Если вы хотите настроить агента: [Для агента](aos/root/AGENTS.md)
* Если нужно обучение: [Tutor](aos/docs/TUTOR.md)

## Навигация / Navigation

* [Начать](aos/docs/START-RU.md)
* [Установка](aos/docs/INSTALL.md)
* [Проверить проект](aos/docs/SELF-TEST.md)
* [AOS Doctor](aos/scripts/aos_doctor.py)
* [Queue Dashboard](aos/scripts/aos_queue_dashboard.py)
* [Tutor](aos/docs/TUTOR.md)
* [Tutor Scenarios](aos/docs/TUTOR-SCENARIOS.md)
* [Prompt Packs](aos/prompt-packs/README.md)
* [Для агента](aos/root/AGENTS.md)
* [Safe Commands](aos/docs/FIRST-SAFE-COMMANDS.md)
* [Authorization Commands](aos/docs/AUTHORIZATION-COMMANDS.md)
* [Workspace Boundary](aos/docs/WORKSPACE-BOUNDARY.md)

---

## Core Philosophy / Философия безопасности
1. **Fail-Closed by Default**: Если что-то непонятно, агент обязан остановиться и спросить.
2. **PASS ≠ Approval**: Никакой успешный тест (включая CI PASS) не означает одобрение.
3. **Evidence ≠ approval**: Наличие отчетов/артефактов об успехе не заменяет команду человека.
4. **Self-test PASS ≠ approval**: Пройденный `self-test` не даёт никаких разрешений на действия агента.
5. **Doctor PASS ≠ approval**: Успешная проверка Доктора не авторизует коммиты, пуши или релизы.
6. **Queue Dashboard output ≠ approval**: Очередь или статус `NEXT` не дают разрешений агенту.
7. **Commit/Push require exact commands**: Для сохранения или отправки кода человек обязан сказать точную команду (например, `AOS COMMIT OK`, `AOS PUSH OK`). Никаких deferred commits без прямого разрешения.
