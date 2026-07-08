# AOS-FARM.640 — Terminal State Semantics Design

## 1. Stage title

AOS-FARM.640 — Task Readiness Terminal State Semantics and Legacy Blocker Exclusion Design

## 2. Purpose

Define a safe future design for excluding terminal and legacy task records from the active readiness gate without misreporting them as `PASS`, without weakening `task --validate-all`, and without hiding non-conforming task files from audit output.

## 3. Source review

Required canonical sources were reviewed before design conclusions:

- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

Source control conclusions applied here:

- `PASS` does not equal approval.
- Evidence does not equal approval.
- Human approval cannot be simulated.
- Unknown or ambiguous state must fail closed.
- Lifecycle-adjacent control surfaces require human checkpointing.

## 4. Prompt 1 baseline validation

Prompt 1 established the following baseline:

- branch: `build/aos-farm-640-terminal-state-semantics-design`
- baseline `HEAD`: `e7ef25508f9d9b61fdae64ffe80fc1dfd7054d88`
- `origin/dev`: `e7ef25508f9d9b61fdae64ffe80fc1dfd7054d88`
- `origin/main`: `e77d8011b84946340e428db2c7547f0285be0713`
- `origin/dev...HEAD`: `0 0`

Baseline validation from Prompt 1:

| Command | Result | Exit | Interpretation |
|---|---:|---:|---|
| `python3 aos/scripts/aos_validate.py --json` | `UNKNOWN_BLOCKED` | `0` | Expected aggregate fail-closed result because readiness failed. |
| `python3 aos/scripts/aos_task_document_check.py task --readiness-all` | `FAILED` | `1` | Expected; same four readiness blockers remained. |
| `python3 aos/scripts/aos_task_document_check.py task --validate-all` | `PASS` | `0` | Expected; task documents remained structurally valid. |
| `python3 aos/scripts/aos_architecture_document_check.py validate-all --json` | `PASS` | `0` | Expected. |
| `python3 -m unittest discover -s tests` | `PASS` | `0` | Expected. |
| `git diff --check` | `PASS` | `0` | Expected. |

## 5. AOS-FARM.638/639 context

AOS-FARM.638 and AOS-FARM.639 established that the current system has real readiness blockers that cannot be legally closed under current schema and validator semantics.

Key preserved facts:

- `task --readiness-all` currently evaluates every `tasks/*.md`.
- `REJECTED` and `CLOSED` do not create readiness exclusion.
- `RETIRED` and `SUPERSEDED` are not legal task-header statuses.
- `AOS-FARM.463` cannot become readiness-clean without task-id migration or schema/validator evolution.
- Human risk assignment alone does not close a readiness blocker.

## 6. Current validator behavior summary

The current readiness implementation has these decisive properties:

- `task --validate-all` discovers every `tasks/*.md` document and must keep doing so.
- `task --readiness-all` also discovers every `tasks/*.md` document and currently treats every discovered task as part of readiness evaluation.
- `check_task_readiness` validates `task_id` format before any terminal-state interpretation.
- The only readiness success result today is `READY_FOR_HANDOFF`.
- Current readiness outputs otherwise resolve to `BLOCKED` or `HUMAN_REVIEW_REQUIRED`, with aggregate command exit `1` if any task is not `READY_FOR_HANDOFF`.

## 7. Current lifecycle/readiness mismatch

Current project semantics mix several distinct concerns inside one readiness path:

- lifecycle state
- readiness result
- validation result
- approval state
- execution authorization
- legacy-task compatibility

This causes two problems:

1. Terminal task concepts are not represented as readiness exclusions.
2. Legacy invalid tasks remain permanently mixed into active readiness output with no explicit quarantine model.

## 8. Schema/helper mismatch around CLOSED

Current task header schema and task validator accept `CLOSED` as a legal status.

Current `aos_lifecycle_state.py` `VALID_LIFECYCLE_STATES` does not include `CLOSED`.

This is a real design mismatch because:

- the schema says `CLOSED` is legal;
- readiness does not exclude it;
- lifecycle helper cannot represent it directly as a valid lifecycle state.

Any future implementation must reconcile this mismatch explicitly rather than relying on implied behavior.

## 9. Required separation of concepts

Future design must keep the following concepts separate:

### 9.1 Lifecycle status

Task-header state such as `DRAFT`, `HUMAN_REVIEW_REQUIRED`, `REJECTED`, `CLOSED`.

### 9.2 Readiness result

Readiness-only evaluation result such as:

- `READY_FOR_HANDOFF`
- `BLOCKED`
- `HUMAN_REVIEW_REQUIRED`
- `EXCLUDED_TERMINAL`
- `EXCLUDED_LEGACY`

### 9.3 Validation result

Structural/schema/document result such as task document validity and malformed witness detection.

### 9.4 Approval state

Human approval state only. Never inferred from validation or readiness.

### 9.5 Execution authorization

Human authorization boundary only. Never inferred from lifecycle or readiness.

### 9.6 Exclusion classification

A distinct audit classification proving why a task is excluded from active readiness counting without claiming that the task passed readiness.

## 10. Risk and authority boundary

- Risk Profile recommendation: `HIGH_RISK_PROTECTED`
- Risk Profile assignment: `HUMAN_REQUIRED_NOT_ASSIGNED_BY_AGENT`

This design concerns future validator semantics, lifecycle-adjacent semantics, and possible canonical witness storage. That is protected work.

Implementation-ready design is not implementation authorization.

AOS-FARM.640 may recommend future implementation.

AOS-FARM.640 does not authorize implementation.

Any future exclusion registry or manifest is a canonical or lifecycle-adjacent control surface and requires a separate human checkpoint before creation or use.

## 11. Design options

### 11.1 Task-header-only witness

Description:

- Store terminal and legacy exclusion witness fields directly in each task header.

Advantages:

- Per-task evidence is colocated with the affected task.
- No second canonical surface is needed for basic witness lookup.
- Audit traceability is straightforward.

Disadvantages:

- Invalid legacy task ids may block before witness fields are trusted unless check order changes carefully.
- Task files become the only exclusion witness surface, which is fragile for malformed legacy documents.
- Some exclusion cases may require references to replacement/dependency evidence outside the task file.

### 11.2 Separate exclusion registry / manifest

Description:

- Store exclusions in a separate canonical registry or manifest, leaving task headers mostly unchanged.

Advantages:

- Can quarantine malformed legacy tasks even when the task header itself is invalid.
- Can centralize dependency and supersession checks.

Disadvantages:

- Creates a new canonical control surface immediately.
- Higher risk of drift between task file and registry.
- Easier to misuse for broad or bulk exclusions.
- Requires explicit human checkpoint before creation or use.

### 11.3 Hybrid model

Description:

- Use per-task witness in task header for normal terminal exclusions.
- Allow a separate human-gated exclusion registry only for legacy/non-conforming cases where task-header-only witness is insufficient.

Advantages:

- Preserves per-task locality for standard terminal cases.
- Provides a controlled path for malformed legacy ids.
- Minimizes need for registry while keeping one available for exceptional quarantine cases.

Disadvantages:

- More complex than single-surface models.
- Requires explicit rule ordering so registry does not become a blanket bypass.

## 12. Rejected unsafe options

Rejected as unsafe:

- Treat `REJECTED` as implicit readiness pass.
- Treat `CLOSED` as implicit readiness pass.
- Treat excluded tasks as `READY_FOR_HANDOFF`.
- Hide excluded tasks from output.
- Skip malformed legacy tasks silently.
- Allow wildcard, pattern, directory, or blanket exclusion.
- Allow registry-only exclusion without per-task witness details.
- Allow agent-assigned exclusion witness.
- Allow invalid legacy task ids to become valid by omission.

## 13. Recommended model

Recommended direction: hybrid terminal/legacy exclusion model.

Core rules:

- `task --validate-all` must still discover every `tasks/*.md`.
- `task --readiness-all` should evaluate active tasks for `READY_FOR_HANDOFF`.
- Valid terminal exclusions should be classified as `EXCLUDED_TERMINAL`, not `PASS`.
- Valid legacy exclusions should be classified as `EXCLUDED_LEGACY`, not `PASS`.
- Malformed or unsupported exclusions remain `BLOCKED` or `UNKNOWN_BLOCKED`.
- No excluded task disappears from audit output.

## 14. Exclusion witness location decision

Decision:

- Normal terminal exclusions: task-header witness in the affected task document.
- Legacy invalid-id exclusions: separate human-gated exclusion registry or manifest, because malformed legacy ids may fail before task-header witness can be trusted safely.

Reason:

- Standard terminal cases should remain local and auditable per task.
- Legacy malformed cases require a quarantine surface that can reference a non-conforming task without pretending the task header is already valid.
- Registry use must be exceptional, explicit, per-task, and human-gated.

## 15. Validator check order decision

Decision:

- `task --validate-all` keeps strict full discovery and strict malformed detection first.
- Future readiness flow should first determine whether a task is active candidate, terminal-excludable with valid witness, or legacy-excludable with valid quarantine witness.
- For normal active tasks, existing structural and readiness checks remain strict.
- For invalid legacy ids, readiness may consult the separate legacy witness only after full-document discovery but before counting the task as active readiness blocker.

Reason:

- Full discovery must remain intact.
- Invalid ids must not be silently accepted as valid.
- Legacy quarantine must be explicit and separate from normal readiness success.

## 16. CLOSED subtype decision

Decision:

Future `CLOSED` semantics must not be monolithic. If `CLOSED` remains legal, a subtype field is required, such as:

- `closure_type: completed`
- `closure_type: rejected`
- `closure_type: retired`
- `closure_type: superseded`

Rules:

- `CLOSED` without valid subtype remains blocked.
- `CLOSED` does not imply approval.
- `CLOSED completed` does not imply approval unless explicit approval exists separately.
- `CLOSED rejected`, `CLOSED retired`, and `CLOSED superseded` are candidate terminal exclusions only if valid witness is present.

## 17. REJECTED semantics

Decision:

- `REJECTED` remains a lifecycle or header state, not a readiness pass.
- `REJECTED` without human witness remains blocked.
- `REJECTED` with valid human witness and no active dependency conflict may be classified as `EXCLUDED_TERMINAL`.

Reason:

- Rejection is a decision outcome, not readiness success.
- It should remove the task from active readiness counting only when the rejection witness is explicit and auditable.

## 18. Dependency/supersession integrity rules

Future exclusion integrity rules must include:

- no self-supersession;
- no circular supersession;
- `superseded_by` must point to an existing valid task reference;
- active downstream dependency may block exclusion unless replacement mapping is explicit;
- rejected/completed terminal exclusion must not strand active dependents without audit-visible disposition;
- legacy quarantine cannot be used to bypass unresolved dependency graph problems.

## 19. Invalid legacy task id handling

`AOS-FARM.463` demonstrates the required rule:

- invalid legacy ids must not be silently accepted as valid task ids;
- invalid legacy ids must remain visible in audit output;
- invalid legacy ids may become `EXCLUDED_LEGACY` only through explicit per-task quarantine witness;
- without valid witness, invalid legacy ids remain readiness blockers.

## 20. Proposed future validator semantics

Future high-level semantics:

1. Discover every `tasks/*.md`.
2. Validate each task structurally for `task --validate-all`.
3. For readiness, classify each discovered file into one of:
   - active readiness candidate
   - terminal exclusion candidate
   - legacy exclusion candidate
   - malformed/unsupported exclusion
4. Apply strict witness validation.
5. Emit separate counts and per-task audit records.
6. Return `PASS` only if all active tasks are readiness-clean and no malformed exclusions exist.

Readiness-specific meaning:

- `READY_FOR_HANDOFF`: active task passed readiness.
- `EXCLUDED_TERMINAL`: excluded from active readiness counting, not pass.
- `EXCLUDED_LEGACY`: excluded from active readiness counting, not pass.
- `BLOCKED` / `UNKNOWN_BLOCKED`: exclusion unsupported, malformed, or unresolved.

## 21. Proposed future schema fields if needed

If task-header witness is implemented for normal terminal exclusions, possible future fields:

```yaml
closure_type: completed|rejected|retired|superseded
terminal_reason: <short controlled reason>
terminal_decision_ref: <human checkpoint or decision artifact ref>
terminal_decision_date: YYYY-MM-DD
readiness_exclusion_requested: true|false
readiness_exclusion_class: terminal
superseded_by: <task id when closure_type is superseded>
```

Constraints:

- No new field should imply approval.
- No field should imply readiness pass.
- Unsupported or partial field sets remain blocked.

## 22. Proposed future registry/manifest fields if needed

If a separate registry is created for legacy cases, possible future fields:

```yaml
task_ref: AOS-FARM.463
classification: EXCLUDED_LEGACY
reason: invalid_legacy_task_id
decision_by: human
decision_ref: <human checkpoint ref>
decision_date: YYYY-MM-DD
dependency_review: pass|blocked
replacement_task: <optional task id>
source: registry
not_pass: true
```

Registry rules:

- one entry per task only;
- no wildcard entries;
- no directory entries;
- no regex entries;
- no blanket project-wide exclusions.

## 23. Future JSON/audit output contract

Proposed future JSON/audit shape:

```json
{
  "status": "PASS_OR_UNKNOWN_BLOCKED_OR_BLOCKED",
  "active_ready_count": 0,
  "active_blocked_count": 0,
  "active_human_review_required_count": 0,
  "excluded_terminal_count": 0,
  "excluded_legacy_count": 0,
  "malformed_exclusion_count": 0,
  "unresolved_legacy_count": 0,
  "exclusions": [
    {
      "task_ref": "AOS-FARM.463",
      "classification": "EXCLUDED_LEGACY",
      "reason": "invalid_legacy_task_id",
      "decision_by": "human",
      "decision_ref": "example-human-checkpoint-ref",
      "decision_date": "2026-07-08",
      "source": "registry",
      "not_pass": true
    }
  ]
}
```

Required audit properties:

- count active blockers;
- count active ready tasks;
- count terminal exclusions;
- count legacy exclusions;
- list every exclusion;
- list malformed exclusions;
- expose witness source;
- expose reason/ref/date;
- mark exclusions as not pass;
- preserve `PASS ≠ approval` language in human-readable output.

## 24. No mass exclusion rule

Future implementation must reject:

- wildcard exclusion;
- pattern-level exclusion;
- directory-level exclusion;
- blanket or bulk exclusion without per-task witness.

Every exclusion must be individually witnessed, individually audited, and individually reported.

## 25. Safety invariants

This design preserves the following invariants:

- This report is Evidence, not approval.
- PASS is validation only, not approval.
- Evidence is not approval.
- CI PASS is not approval.
- Excluded terminal task is not PASS.
- Excluded legacy task is not PASS.
- `EXCLUDED_TERMINAL` is not `READY_FOR_HANDOFF`.
- `EXCLUDED_LEGACY` is not `READY_FOR_HANDOFF`.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- No release is authorized.
- No merge to main is authorized.
- No blocker is closed by this report.
- No implementation is authorized by this report.
- Human approval cannot be simulated.

## 26. Test plan

Future implementation test plan must include at least:

1. Active `DRAFT` task with `UNKNOWN_BLOCKED` risk remains blocker.
2. Active task with `NOT_RUN` validator remains blocker.
3. `REJECTED` task without human witness remains blocker.
4. `REJECTED` task with valid human witness and no active dependency is `EXCLUDED_TERMINAL`, not `PASS`.
5. `CLOSED` task without `closure_type` remains blocker.
6. `CLOSED` task with `closure_type: rejected` requires rejection witness.
7. `CLOSED` task with `closure_type: completed` must not imply approval unless explicit approval exists.
8. `CLOSED` task with invalid or unknown `closure_type` remains blocker.
9. `SUPERSEDED` task requires valid `superseded_by`.
10. `SUPERSEDED` task with missing target remains blocker.
11. Circular supersession is rejected.
12. Self-supersession is rejected.
13. `RETIRED` task requires human witness.
14. Invalid legacy id task is not silently accepted.
15. Invalid legacy id with valid quarantine witness becomes `EXCLUDED_LEGACY`, not `PASS`.
16. Invalid legacy id without registry witness remains blocker.
17. `task --validate-all` still discovers every `tasks/*.md`.
18. `task --validate-all` still detects malformed docs.
19. `task --readiness-all` lists exclusions separately.
20. `aos_validate.py --json` exposes exclusion counters.
21. `aos_validate.py --json` does not report `PASS` if exclusions are malformed.
22. `PASS ≠ approval` language is preserved.
23. `NOT_RUN ≠ PASS` remains enforced.
24. Agent Risk Profile assignment is rejected.
25. Excluded terminal task is not counted as active ready.
26. Excluded legacy task is not counted as active ready.
27. Active downstream dependency prevents exclusion unless replacement is recorded.
28. Wildcard exclusion is rejected.
29. Directory-level exclusion is rejected.
30. Pattern-level exclusion is rejected.
31. Blanket or bulk exclusion without per-task witness is rejected.

## 27. Future implementation task recommendation

Recommended downstream tasks:

1. Separate protected implementation task for readiness exclusion semantics.
2. Separate schema/helper reconciliation task for `CLOSED` and subtype semantics.
3. Separate legacy quarantine task for known malformed ids such as `AOS-FARM.463`.
4. Separate test implementation task covering exclusion classification and audit output.
5. Separate human-checkpoint task before any registry or manifest is created.

## 28. Explicit non-goals

Non-goals of AOS-FARM.640:

- implement validator changes;
- edit task files;
- rename `AOS-FARM.463`;
- add terminal statuses now;
- modify current lifecycle definitions now;
- change current `task --readiness-all`;
- change validator exit codes;
- close readiness blockers;
- create actual exclusion registry or manifest;
- authorize implementation;
- authorize commit, push, merge, release, or deployment.

## 29. Final statement

This report is Evidence, not approval.
