# Education Intake Extension

**Domain:** education  
**Extension status:** ACTIVE_DOMAIN_EXTENSION  
**Extends:** technical-assignment-agent-workflow  
**May override core:** false  
**May weaken core:** false  
**Execution authorized:** false  

---

## 1. Когда использовать

Использовать extension, если проект затрагивает:

- students;
- teachers;
- courses;
- learning materials;
- assignments;
- grading;
- progress tracking;
- parents;
- schools;
- children’s data;
- online learning.

---

## 2. Серые зоны

Образовательные проекты требуют внимания к:

- student privacy;
- minors’ data;
- grading responsibility;
- teacher authority;
- parent access;
- content safety;
- academic integrity;
- progress interpretation;
- accessibility.

---

## 3. Domain-Specific Questions

1. Кто learners?
2. Есть ли minors?
3. Кто создаёт learning materials?
4. Кто может видеть student progress?
5. Кто может grade?
6. Может ли система recommend learning paths?
7. Какие outputs требуют teacher approval?
8. Могут ли parents видеть данные?
9. Какие данные нужно скрыть от students или parents?
10. Что должно логироваться?

---

## 4. Education Data Discovery

Возможные data objects:

- Student;
- Teacher;
- Parent;
- Course;
- Lesson;
- Assignment;
- Grade;
- Progress Record;
- Learning Material;
- Feedback;
- Audit Log.

---

## 5. Access / Permissions

Типичные roles:

- Student;
- Teacher;
- Parent;
- School Admin;
- Content Creator;
- System.

Sensitive permissions:

- grading;
- viewing private student data;
- changing progress records;
- publishing content;
- messaging students;
- parent access.

---

## 6. Negative Constraints

Система не должна:

- expose student private data unauthorized users;
- allow automated final grading without authorized review;
- modify grades without audit trail;
- show unsafe content;
- treat AI feedback as teacher approval;
- bypass teacher review where required.

---

## 7. Acceptance Criteria

Acceptance Criteria должны включать:

- role-based access check;
- grading audit trail;
- teacher review for high-impact outputs;
- student privacy check;
- parent visibility boundaries;
- content safety review.

---

## 8. Human Decisions Required

- Может ли система grade automatically?
- Какие outputs требуют teacher approval?
- Что могут видеть parents?
- Какие student data являются sensitive?
- Какие content safety rules применяются?
- Какой audit trail обязателен?

---

## 9. Final Status

```yaml
extension_applied: true
domain: education
domain_review_required: true
student_privacy_review_required: true
execution_authorized: false
```
