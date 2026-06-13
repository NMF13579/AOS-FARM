---
id: example-feature-001
author: agent
owner: human / NMF13579
status: draft
requires_human_approval: true
reference: https://github.com/NMF13579/AgentOS
---

# Example Feature: Documentation Assembly Baseline

Purpose: provide a minimal, machine-readable example spec to demonstrate the full
spec → tasks → acceptance flow for agents. This is a non-destructive, doc-only
feature intended as reference and template for future feature specs.

Scope:
- Create a `specs/example-feature/tasks.md` listing atomic tasks.
- Provide `acceptance.md` with runnable checks.
- Add a validation script `scripts/validate-spec.sh` that verifies presence and
  required frontmatter keys.

Out of scope:
- Any code changes outside repository documentation and scaffolding.
- Creating or modifying canonical files `00_`, `01_`, `02_`.

Constraints:
- This spec requires a human owner to mark `status: approved` before agent may
  perform any operations that would change canonical or protected files.

Deliverables:
- `specs/example-feature/spec.md` (this file)
- `specs/example-feature/tasks.md`
- `specs/example-feature/acceptance.md`
- `scripts/validate-spec.sh`

Human checkpoints:
- Owner reviews and marks `status: approved` in this spec before agent executes tasks.
