---
feature: example-feature-001
owner: human / NMF13579
version: 0.1
---

# Tasks for Example Feature

1. Draft spec (atomic) — `specs/example-feature/spec.md`
   - owner: human / NMF13579
   - estimate: 0.5h
   - preconditions: none
   - postconditions: `spec.md` exists with required frontmatter

2. Create tasks file — `specs/example-feature/tasks.md`
   - owner: agent
   - estimate: 0.5h
   - preconditions: `spec.md` exists
   - postconditions: `tasks.md` exists and lists atomic tasks

3. Create acceptance criteria — `specs/example-feature/acceptance.md`
   - owner: agent
   - estimate: 0.5h
   - preconditions: `spec.md` and `tasks.md` exist
   - postconditions: `acceptance.md` contains runnable checks

4. Add validator script — `scripts/validate-spec.sh`
   - owner: agent
   - estimate: 0.5h
   - preconditions: all spec files exist
   - postconditions: script passes the checks listed in `acceptance.md`

5. Human review checkpoint
   - owner: human / NMF13579
   - action: review `acceptance.md` and run `scripts/validate-spec.sh`
   - decision: mark spec `status: approved` or provide feedback
