# AOS-FARM.503 External Best Practices Reference

```yaml
report_id: AOS-FARM.503
cycle: AOS-FARM-CYCLE-0001
source_type: EXTERNAL_REFERENCE_ONLY
source_of_truth: false
may_override_00_01_02: false
may_authorize_execution: false
may_grant_approval: false
status: NOT_RUN_EXTERNAL_REFERENCE
approval_granted: false
execution_authorized: false
```

## External Search Prompt

Created at:

```text
.aos-tmp/cycles/AOS-FARM-CYCLE-0001/prompts/02-perplexity-best-practices-prompt.md
```

The prompt asks for best practices on product onboarding, project intake, requirements traceability, problem interview to specification, specification to implementation plan, task decomposition, task queue acceptance, AI coding agent safety, code review gates, Evidence and validation reports, and human approval workflows.

## Perplexity Output Status

```text
PERPLEXITY_OUTPUT_NOT_PROVIDED
NOT_RUN_EXTERNAL_REFERENCE
```

No Perplexity output was provided in this task, and this agent did not browse Perplexity. This does not block the planning cycle, but it must not be treated as PASS.

## Placeholder For Future External Findings

When external output is provided later, it may be summarized here only as external reference. It must remain subordinate to `00`, `01`, and `02`, and it must not authorize execution, approval, task promotion, Risk Profile assignment, commit, push, merge, release, or protected/canonical mutation.

## Best-Practice Themes To Compare Later

- Clear first-run onboarding path with a small number of mandatory entrypoints.
- Read-only project discovery before technical planning.
- One-question-at-a-time problem interview when requirements are vague.
- Explicit traceability from problem statement to Technical Assignment to each task candidate.
- Manual queue acceptance before task execution.
- Separate execution, Evidence, human review, commit, push, merge, and release gates.
- Human-only approval and Risk Profile assignment.
- Deterministic validators for structure and forbidden claims, with validator PASS never treated as approval.

## Boundary Statement

External references are not Source of Truth, not Evidence, and not approval. Missing external output is `NOT_RUN_EXTERNAL_REFERENCE`, not PASS.
