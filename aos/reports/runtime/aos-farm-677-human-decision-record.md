# AOS-FARM.677 Human Architecture, Risk Profile, and Serialization Contract Decision

## 1. Decision Authority
Я, человек-владелец проекта AOS-FARM, принимаю следующие решения для AOS-FARM.677.
Эта запись является human decision для scope, Risk Profile и serialization contract AOS-FARM.677.
Она не является:
1. Commit authorization.
2. Push authorization.
3. Merge authorization.
4. Release authorization.
5. Approval результата implementation.
6. Разрешением начать AOS-FARM.678.

## 2. Risk Profile Assignment
Для AOS-FARM.677 человеком назначается:
`HIGH_RISK_PROTECTED`
- `risk_profile_assigned_by_human: true`
- `risk_profile_assigned_by_agent: false`

Этот Risk Profile применяется только к AOS-FARM.677 и не назначает Risk Profile будущим этапам автоматически.

## 3. Architecture Checkpoint
Человеком разрешён implementation scope AOS-FARM.677:
- Execution Package schema
- strict JSON parser
- RFC 8785 canonical serialization
- package digest
- repository and baseline binding
- capability lifecycle
- session identity and binding
- nonce and expiration
- replay-state interface
- revocation interface
- authorization lineage
- workspace-lock interface
- signing and verification interfaces
- read-only validation CLI
- positive and negative fixtures
- Evidence

Максимально допустимый trust claim:
`DIGEST_BOUND`

Допустимые дополнительные claims:
- `SINGLE_USE_CONTRACT_DEFINED`
- `WORKSPACE_LOCK_INTERFACE_IMPLEMENTED`
- `REPLAY_STATE_INTERFACE_IMPLEMENTED`

Запрещённые claims:
- `SINGLE_USE_ENFORCED`
- `WORKSPACE_CONCURRENCY_ENFORCED`
- `REPLAY_PROTECTION_PRODUCTION_READY`
- `TRUSTED_TIME_ESTABLISHED`
- `SIGNED_SEPARATE_KEY_CUSTODY`
- `ENFORCED_MODE`
- `PRODUCTION_READY`

## 4. Physical Enforcement Boundary
AOS-FARM.677 не реализует:
1. Command Guard.
2. Write Guard.
3. Trusted runner.
4. Filesystem broker.
5. Shell broker.
6. Editor interception.
7. Protected Path enforcement.
8. Local Git Guard.
9. Remote Git Guard.
10. OS-level concurrency enforcement.
11. Container, VM или microVM isolation.
12. Production signing keys.
13. External witness.
14. Trusted time service.
15. Automatic approval.
16. Automatic lifecycle transitions.

Scope не должен расширяться без нового explicit human checkpoint.

## 5. Serialization Contract Decision
Для Execution Package AOS-FARM.677 принят следующий normative contract:
- `serialization_format`: JSON
- `canonical_serialization`: RFC 8785
- `json_parser`: strict
- `duplicate_keys`: rejected
- `floating_point_values`: forbidden
- `nan_and_infinity`: forbidden
- `integer_values`: explicitly bounded
- `unicode_normalization`: forbidden
- `unicode_strings`: preserved without normalization
- `property_ordering`: RFC 8785 UTF-16 code-unit ordering
- `array_order`: preserved
- `canonical_encoding`: UTF-8

### 5.1. Unicode decision
Предыдущее положение AOS-FARM.676:
`unicode_normalization: NFC`
не применяется к Execution Package canonical serialization AOS-FARM.677.
Для AOS-FARM.677 устанавливается:
`unicode_normalization: forbidden`

Причина:
1. RFC 8785 не предусматривает Unicode normalization.
2. Normalization изменяет исходное строковое значение.
3. NFC и NFD representations должны сохраняться как разные JSON strings.
4. Canonicalization должна сериализовать parsed string без семантического изменения.
5. Нормализация до digest может создать неоднозначность и скрыто изменить подписываемый payload.
Это решение является explicit human resolution конфликта между AOS-FARM.676 artifact и RFC 8785 contract.

## 6. Architecture Artifact Handling
Существующий файл:
`aos/docs/runtime/runtime-contracts.md`
содержит конфликтующее значение `unicode_normalization: NFC`.
В рамках AOS-FARM.677 этот файл остаётся protected architecture artifact и не должен изменяться автоматически.
До отдельного разрешения:
1. Implementation AOS-FARM.677 должна следовать настоящему human decision.
2. Конфликт должен быть отражён в Evidence как explicit human override для scope AOS-FARM.677.
3. Агент не должен молча менять AOS-FARM.676 artifact.
4. Агент не должен заявлять, что конфликтующий artifact уже исправлен.
5. Отдельная cross-reference correction может быть выполнена только после отдельного protected-change checkpoint.

## 7. Digest Payload Contract
Для AOS-FARM.677 утверждается:
validated package object
→ create digest payload projection
→ remove package_digest completely
→ remove package_signature completely
→ do not replace removed fields with null
→ canonicalize projected object using RFC 8785
→ encode as UTF-8
→ calculate SHA-256
→ store package_digest in full package object

Нормативная последовательность:
`strip-then-canonicalize`

Запрещено:
`canonicalize-then-strip`

Дополнительные правила:
1. `package_digest` отсутствует в digest payload.
2. `package_signature` отсутствует в digest payload.
3. Отсутствующее field и field со значением null не эквивалентны.
4. Generation и verification используют одинаковую projection.
5. Signature создаётся после digest.
6. Добавление signature не изменяет digest.
7. Digest не является authenticity.

## 8. Implementation File Boundary
Разрешается создание новых файлов только в пределах согласованного implementation scope после повторной baseline verification.
Предварительно разрешённые области:
- `aos/runtime/`
- `aos/scripts/aos_execution_package_validate.py`
- `tests/runtime/`
- `tests/fixtures/runtime/execution_package/`
- `aos/reports/runtime/aos-farm-677-implementation-report.md`
Точный минимальный file inventory должен быть зафиксирован до первой mutation.
Не разрешено изменять core governance files, approval/lifecycle records, registries, workflows и 676 architecture artifacts без отдельного checkpoint.

## 9. Dependency Decision
Для AOS-FARM.677 утверждается:
Python standard library only
Разрешается собственный минимальный in-repository RFC 8785 canonicalizer только для restricted JSON value domain AOS-FARM.677.
Не разрешено без отдельного dependency review добавлять новую dependency, устанавливать packages, или расширять implementation.

## 10. Git Baseline Decision
AOS-FARM.677 не должен реализовываться поверх непроверенной или незавершённой branch AOS-FARM.676.
До создания implementation branch необходимо отдельно закрыть Git boundary AOS-FARM.676 и установить актуальный origin/dev. Настоящее решение не является push authorization для AOS-FARM.676.

## 11. Implementation Authority
После выполнения Git baseline prerequisites разрешается отдельный implementation prompt AOS-FARM.677.
- `implementation_scope_approved_by_human: true`
- `risk_profile_assigned_by_human: true`
- `serialization_contract_approved_by_human: true`
- `digest_contract_approved_by_human: true`
- `protected_change_allowed: false`
- `commit_authorized: false`
- `push_authorized: false`
- `merge_authorized: false`
- `release_authorized: false`
- `next_stage_authorized: false`

Implementation должна остановиться перед commit.
