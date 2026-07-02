# Agentic Operating System (AOS-FARM)

**Надежный фреймворк для безопасной разработки с AI-агентами.**
**The secure framework for AI-driven software development.**

AOS-FARM помогает безопасно работать с AI-помощниками (агентами). Он не дает агенту делать скрытые действия, менять важные файлы без спроса или выдавать успешные тесты за ваше одобрение.

## Навигация / Navigation

* [Начать на русском](aos/docs/START-RU.md)
* Start in English *(planned)*
* [Установка](aos/docs/INSTALL.md)
* [Первое ознакомление](aos/docs/TUTOR.md)
* Собрать ТЗ *(planned)*
* Пройти problem interview *(planned)*
* Запустить self-test *(planned)*
* [Для агента / AGENTS.md](aos/root/AGENTS.md)
* [Документация AOS](aos/docs/ROUTES.md)

---

## Core Philosophy / Философия безопасности
1. **Fail-Closed by Default**: Если что-то непонятно, агент обязан остановиться и спросить.
2. **PASS ≠ Approval**: Успешный тест не означает, что код можно отправлять в проект.
3. **No Simulated Approval**: Агенту строго запрещено симулировать одобрение от лица человека.
4. **Deferred Commits**: Все коммиты делаются только по явной команде пользователя.

*Note: README.md в этом репозитории является навигационной страницей. При установке AOS-FARM в целевой проект, установщик не будет молча перезаписывать ваш README.md.*
