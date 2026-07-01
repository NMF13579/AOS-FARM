# Medical Intake Extension

**Domain:** medicine / healthcare  
**Extension status:** ACTIVE_DOMAIN_EXTENSION  
**Extends:** technical-assignment-agent-workflow  
**May override core:** false  
**May weaken core:** false  
**Execution authorized:** false  

---

## 1. Когда использовать

Использовать extension, если проект затрагивает:

- пациентов;
- medical records;
- appointments;
- symptoms;
- diagnosis support;
- treatment support;
- clinic workflow;
- doctor/patient communication;
- health data;
- medical documents;
- clinical safety.

---

## 2. Серые зоны

Медицинские проекты требуют дополнительной проверки:

- patient safety;
- clinical responsibility;
- privacy;
- consent;
- medical secrecy;
- audit trail;
- access to patient data;
- automated triage;
- diagnosis или treatment suggestions;
- communication with patients.

---

## 3. Domain-Specific Questions

1. Система обрабатывает patient data?
2. Система влияет на clinical decisions?
3. Система создаёт advice, который видит пациент?
4. Система summarises symptoms или complaints?
5. Система предлагает diagnosis, treatment, priority или urgency?
6. Кто должен review outputs перед patient-facing use?
7. Какие данные запрещено хранить?
8. Какие действия всегда требуют doctor approval?
9. Что должно логироваться?
10. Какие compliance или clinic policy применяются?

---

## 4. Medical Data Discovery

Возможные data objects:

- Patient;
- Appointment;
- Complaint;
- Symptom;
- Medical Document;
- Doctor Note;
- Notification;
- Consent;
- Audit Log.

Для каждого объекта нужно указать:

- sensitive data status;
- owner/controller;
- permitted readers;
- permitted editors;
- retention;
- audit requirement;
- consent requirement.

---

## 5. Access / Permissions

Access Matrix обязателен.

Типичные roles:

- Doctor;
- Nurse;
- Admin;
- Patient;
- Clinic Manager;
- System.

Audit Log должен быть read-only или append-only.

---

## 6. Negative Constraints

Система не должна:

- autonomously diagnose;
- autonomously prescribe treatment;
- hide uncertainty;
- показывать patient data unauthorized users;
- delete audit logs;
- отправлять patient-facing medical messages без required review;
- make clinical decisions without Human review.

---

## 7. Acceptance Criteria

Acceptance Criteria должны включать:

- clinical safety review;
- privacy review;
- role-based access check;
- audit log check;
- Human review check для patient-impacting outputs.

---

## 8. Human Decisions Required

- Может ли output быть patient-facing?
- Какие outputs требуют doctor approval?
- Какие patient data можно хранить?
- Какая retention policy применяется?
- Какие compliance rules применяются?
- Какой audit trail обязателен?

---

## 9. Final Status

```yaml
extension_applied: true
domain: medical
domain_review_required: true
clinical_safety_review_required: true
privacy_review_required: true
execution_authorized: false
```
