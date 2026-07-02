# Практические сценарии (Tutor Scenarios)

Здесь собраны частые вопросы начинающих пользователей при работе с AOS-FARM и четкие ответы, как правильно себя вести.

---

## 1. Я впервые открыл проект — что делать?
**Scenario:** Вы открыли новый репозиторий, где уже установлен AOS-FARM.
**User question:** Что мне делать в первую очередь?
**Plain answer:** Ознакомьтесь с правилами навигации.
**What this means:** Вы должны понять, где что лежит, и не пытаться сразу писать код.
**Next safe action:** Прочитайте `START-RU.md`, `FIRST-START.md` и запустите AOS Doctor (`python3 aos/scripts/aos_doctor.py`), чтобы осмотреться.
**Forbidden actions:** Писать код, менять конфигурации, запускать агентов на исполнение задач без авторизации.
**Boundary:** Чтение документации не дает execution authorization.

---

## 2. У меня есть готовое ТЗ — куда его положить?
**Scenario:** У вас уже есть техническое задание (ТЗ) на задачу.
**User question:** Куда мне сохранить файл с ТЗ?
**Plain answer:** В папку `/project/`.
**What this means:** `/project/` — это документационное пространство (workspace), где живут требования и планы.
**Next safe action:** Создайте файл с ТЗ в `/project/` и попросите агента проверить его (сделать review).
**Forbidden actions:** Класть ТЗ в `/aos/`, в `/.aos-tmp/` или смешивать с исходным кодом продукта.
**Boundary:** Наличие ТЗ в `/project/` не дает агенту автоматического разрешения (approval) начинать работу над кодом.

---

## 3. У меня только идея — как начать problem intake?
**Scenario:** Есть только идея, нет готового ТЗ.
**User question:** С чего начать формулировать задачу?
**Plain answer:** Начните с создания драфта в `/project/`.
**What this means:** Вы можете попросить агента помочь вам описать идею, сформулировать цели и ограничения.
**Next safe action:** Назначьте `LOW_RISK_FAST` и попросите агента написать Project Brief.
**Forbidden actions:** Просить агента "сделать всё сразу" (expand scope), минуя этап проектирования.
**Boundary:** Это процесс создания документации, а не execution approval.

---

## 4. Self-test PASS — можно ли запускать агента?
**Scenario:** Агент запустил `aos_consumer_self_test.py` и получил PASS.
**User question:** Можно ли агенту начинать писать код?
**Plain answer:** Нет, нельзя.
**What this means:** Self-test проверяет только целостность инфраструктуры AOS, а не дает команду на старт работы.
**Next safe action:** Человек должен явно авторизовать выполнение конкретной задачи.
**Forbidden actions:** Автоматически запускать (auto-execution) или считать self-test за разрешение.
**Boundary:** Self-test PASS ≠ approval.

---

## 5. Doctor PASS — можно ли выполнять задачу?
**Scenario:** `aos_doctor.py` отработал без ошибок.
**User question:** Если Доктор говорит PASS, значит ли это, что задача разрешена?
**Plain answer:** Нет.
**What this means:** AOS Doctor просто агрегирует статус проверок (read-only validation). Он ничего не разрешает.
**Next safe action:** Изучите результаты Доктора, затем дайте агенту точную команду на выполнение задачи.
**Forbidden actions:** Считать вывод AOS Doctor за execution authorization или lifecycle mutation.
**Boundary:** Doctor PASS ≠ approval. Doctor не является Source of Truth.

---

## 6. Queue next показал задачу — можно ли выполнять?
**Scenario:** Вызван `aos_queue_dashboard.py`, и он показал кандидата в NEXT.
**User question:** Означает ли статус NEXT в очереди, что агент может сам начать работу?
**Plain answer:** Нет, агент должен ждать вашу команду.
**What this means:** Очередь показывает, какая задача следующая по плану, но не дает старт.
**Next safe action:** Проверьте, есть ли blockers и missing human decisions, и дайте явную авторизацию агенту.
**Forbidden actions:** Агенту запрещено начинать работу (auto-execution) просто потому, что задача NEXT.
**Boundary:** Queue NEXT ≠ execution authorization. Dashboard — это только view, не Source of Truth.

---

## 7. Validator PASS — можно ли commit?
**Scenario:** Агент написал код, запустил скрипты валидации и они показали PASS.
**User question:** Агент спрашивает, можно ли ему сделать commit. Что делать?
**Plain answer:** Изучите код (diff), и если вы согласны, дайте точную команду.
**What this means:** Успешная проверка скриптом не значит, что код решает вашу задачу так, как вы хотели.
**Next safe action:** Напишите `AOS COMMIT OK`, если полностью согласны с изменениями.
**Forbidden actions:** Агенту запрещено делать commit самостоятельно. Человеку нельзя использовать размытые слова ("давай", "сохраняй").
**Boundary:** Validator PASS ≠ commit authorization.

---

## 8. CI PASS — можно ли merge/release?
**Scenario:** Задача выполнена, автотесты (CI) на сервере прошли успешно.
**User question:** Можно ли теперь сливать код (merge) или делать релиз?
**Plain answer:** Только если вы сами это подтвердите.
**What this means:** CI-сервер проверяет техническое качество, но не бизнес-логику и не риски релиза.
**Next safe action:** Внимательно просмотрите pull request и дайте явную авторизацию на merge.
**Forbidden actions:** Настраивать авто-merge для AI-изменений.
**Boundary:** CI PASS ≠ approval. CI PASS ≠ merge/release permission.

---

## 9. Агент просит разрешение на commit — что написать?
**Scenario:** Агент подготовил Evidence и ждет вашей команды.
**User question:** Что именно мне нужно напечатать?
**Plain answer:** Нужно написать `AOS COMMIT OK`.
**What this means:** Вы берете на себя ответственность за предложенные изменения (diff) в рамках этой задачи.
**Next safe action:** Скопируйте и отправьте `AOS COMMIT OK`.
**Forbidden actions:** Симуляция одобрения (No fake approval) агентом от лица человека. Использование слов "ок", "коммить", "сохрани".
**Boundary:** Human approval cannot be simulated.

---

## 10. Агент просит push — что написать?
**Scenario:** Коммит успешно создан, агент просит отправить код на сервер.
**User question:** Как дать разрешение на отправку?
**Plain answer:** Напишите `AOS PUSH OK`.
**What this means:** Вы разрешаете отправку зафиксированного состояния (коммита) в удаленный репозиторий.
**Next safe action:** Убедитесь, что коммит авторизован, и отправьте `AOS PUSH OK`.
**Forbidden actions:** Агенту запрещено делать push без этой точной команды.
**Boundary:** Commit authorization ≠ push authorization.

---

## 11. Почему UNKNOWN_BLOCKED — это нормально?
**Scenario:** Агент остановился со статусом `UNKNOWN_BLOCKED`.
**User question:** Является ли это поломкой?
**Plain answer:** Нет, это штатная работа системы безопасности.
**What this means:** Когда система сталкивается с неясностью (unknown route, missing status, unclear scope), она "падает в безопасность" (fail-closed).
**Next safe action:** Вмешайтесь и явно разрешите проблему или уточните scope.
**Forbidden actions:** Обходить (bypass) статус или превращать UNKNOWN в PASS.
**Boundary:** UNKNOWN ≠ OK.

---

## 12. Где хранить Evidence?
**Scenario:** Агент сгенерировал отчет с результатами работы (Evidence).
**User question:** Куда сохранить этот артефакт?
**Plain answer:** Сохраните его в папку `reports/` или `aos/reports/` (в зависимости от проекта), но точно не в `/.aos-tmp/`.
**What this means:** `/.aos-tmp/` — это папка для временного мусора. Отчеты должны оставаться в истории проекта.
**Next safe action:** Создайте Markdown-файл с Evidence в рабочей документационной папке.
**Forbidden actions:** Сохранять Evidence в `/.aos-tmp/` или считать наличие Evidence как approval.
**Boundary:** Evidence ≠ approval. `/.aos-tmp/` ≠ Source of Truth.

---

## 13. Почему нельзя писать код в /project/?
**Scenario:** Вы просите агента реализовать фичу.
**User question:** Почему агент отказывается писать исходный код внутри `/project/`?
**Plain answer:** Потому что `/project/` предназначена только для документации.
**What this means:** Разделение рабочего пространства — ключевой принцип AOS-FARM. Документация не смешивается с кодом.
**Next safe action:** Укажите агенту пути к директориям вашего исходного кода продукта (например, `src/`, `backend/`).
**Forbidden actions:** Превращать `/project/` в default product source root.
**Boundary:** Workspace boundary.

---

## 14. Что делать, если агент хочет расширить scope?
**Scenario:** Агент предлагает попутно отрефакторить соседний файл или добавить функцию "заодно".
**User question:** Можно ли согласиться на лету?
**Plain answer:** Нет, без явного изменения ТЗ и Risk Profile этого делать нельзя.
**What this means:** Расширение scope "на лету" разрушает контроль и может привести к поломкам.
**Next safe action:** Если изменение нужно, обновите Task Brief, переназначьте Risk Profile (human checkpoint) и только потом разрешите.
**Forbidden actions:** Неявное, скрытое расширение scope.
**Boundary:** Do not expand scope without explicit human permission.

---

## 15. Что делать, если protected/canonical files затронуты?
**Scenario:** Задача требует изменения правил (например, файлов в папке `aos/` или `00_AOS_Core_Control.md`).
**User question:** Как это правильно сделать?
**Plain answer:** Требуется Risk Profile `HIGH_RISK_PROTECTED` и отдельный human checkpoint.
**What this means:** Эти файлы контролируют саму безопасность. Их изменение — самая рискованная операция.
**Next safe action:** Подготовьте четкий план изменения, подтвердите его с человеком и только после этого приступайте к редактированию.
**Forbidden actions:** Делать такие изменения попутно, скрытно, или без отдельного подтверждения.
**Boundary:** Do not modify protected/canonical files without human checkpoint.
