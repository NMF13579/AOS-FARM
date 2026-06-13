---
feature: example-feature-001
owner: human / NMF13579
---

# Acceptance Criteria

1. `specs/example-feature/spec.md` exists and contains YAML frontmatter keys: `id`, `author`, `owner`, `status`, `requires_human_approval`.
2. `specs/example-feature/tasks.md` exists and lists at least one task with `preconditions` and `postconditions`.
3. `specs/example-feature/acceptance.md` exists and documents runnable checks.
4. `scripts/validate-spec.sh` exists, is executable, and exits `0` when the above are satisfied.

Run locally to validate:

```sh
sh scripts/validate-spec.sh specs/example-feature
```
