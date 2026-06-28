# Controlled Task Brief: AOS-FARM.448

**task_id:** AOS-FARM.448
**goal:** Dogfood one complete controlled task lifecycle.
**scope:** Dogfood preparation and execution of one complete controlled task lifecycle including registry, brief, guard precheck, scopecheck, execution report, evidence, postcheck, backlog loop, and next task candidate.

## Scope Boundaries

**allowed_files:**
- `reports/aos-farm-448-*`
- `reports/human-checkpoints/aos-farm-448-*`
- Working branch: `build/first-controlled-task-lifecycle-dogfood`

**allowed_changes:**
- Creation of lifecycle artifacts, execution reports, and evidence records strictly limited to the `AOS-FARM.448` identity.

**forbidden_files:**
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
- `03_AOS_Future_and_Legacy_Reference_OPTIONAL.md`
- `04_AOS_Model_Routing_and_Task_Decomposition_Research.md`
- Any `/aos/` docs unless explicitly authorized.
- Any canonical or protected files.

**forbidden_changes:**
- No runner building.
- No RAG building.
- No SQLite building.
- No vector DB adding.
- No SaaS adding.
- No CI adding.
- No commits.
- No pushes.
- No merges.
- No releases.
- No starting AOS-FARM.449.
- No cleaning, deleting, resetting, rebasing, or forcing anything without human authorization.

## Execution Plan

**validation_plan:**
- Verify baseline is safe.
- Read and adhere to required canonical sources.
- Execute steps sequentially and report on each lifecycle boundary.

**expected_evidence:**
- `Execution Report` demonstrating adherence to scope boundaries.
- `Evidence Report / Evidence Review`.
- Validation artifacts for `scopecheck` and `postcheck`.

## Safety Semantics

**unknowns:**
- Unforeseen issues in `Controlled Execution Guard` execution are marked as UNKNOWN.

**not_run_policy:**
- If any boundary is exceeded or validation fails, STOP immediately. `NOT_RUN ≠ PASS`.

**final_status:** READY_FOR_HUMAN_REVIEW
