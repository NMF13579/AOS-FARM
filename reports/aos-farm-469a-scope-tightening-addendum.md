# AOS-FARM.469A — Scope Tightening Addendum for Product Boundary Implementation

## 1. Baseline
- origin/main: 9fc5c78abaf13ed328b190a8a38dbdec78b8fa97
- origin/dev: d1144379990acc70bd3198aa31efbc92fc4ebf38
- main...dev: 0 90
- local status: dev branch, dirty working tree with untracked files
- mode: READ-ONLY REVIEW + PLANNING REPORT UPDATE ONLY

## 2. Verdict
- AOS-FARM.469 status: ACCEPT_WITH_MODIFICATION
- AOS-FARM.470 authorization status: NOT AUTHORIZED (REQUIRES_HUMAN_DECISION)
- reason: The scope defined in 469 was dangerously broad (allowed `aos/**`, `AGENTS.md`, `README.md` entirely) and used incorrect decision language. This addendum tightens the boundaries for a safe handoff.

## 3. Problems found in 469 handoff
List:
- broad `aos/**`: Allowed full write access to the entire `aos` directory, which could lead to unintended modifications of stable files.
- root README/AGENTS risk: Permitting edits to these files creates a risk of canonical governance modification.
- Required decision: ACCEPT: The phrase "ACCEPT" was used as a generic classification, implying automatic approval for execution, violating the invariant that execution requires human authorization.
- [CLASSIFICATION] placeholders: Used as a formatting tag instead of reflecting actual safety decisions (e.g., [REJECT], [REQUIRES_HUMAN_DECISION]).
- .aos-tmp ambiguity: Did not restrict the use of `.aos-tmp` as temporary, disposable scratch space.
- tests/fixtures move ambiguity: Recommended moving examples to `tests/fixtures/` without explicitly granting scope access to `tests/fixtures/`.

## 4. Corrected allowed files for 470
Exact list only:
- `llms.txt`
- `aos/SELF_TEST.md`
- `aos/MANIFEST.md`
- `aos/VERSION.md`
- `aos/COMPATIBILITY.md`
- `aos/CHANGELOG.md`
- `aos/UNINSTALL.md`
- `aos/REMOVAL_CHECKLIST.md`
- `aos/prompts/problem-intake.md`
- `aos/tools/README.md`
- `aos/tools/dry-run-only/README.md`
- `aos/tools/optional/problem-intake-runner/problem_intake_runner.py`
- `aos/schemas/task-quality-check-package.schema.json`
- `aos/reports/examples/`
- `aos/examples/`

## 5. Corrected forbidden files for 470
Exact list:
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
- `AGENTS.md`
- `README.md`
- `constitution.md`
- `.github/`
- `docs/`
- `specs/`
- `tasks/`
- `reports/` except the 469A addendum itself (`reports/aos-farm-469a-scope-tightening-addendum.md`)
- `aos/AGENT_CONTEXT.md` unless explicitly authorized
- `aos/START_HERE.md` unless explicitly authorized
- `aos/root/AGENTS.md` unless explicitly authorized
- `aos/docs/governance/`
- `aos/docs/workflow/`
- `aos/templates/`
- `aos/scripts/` except explicitly allowed runner file above
- any file not listed in allowed files

## 6. Corrected decision wording
Show replacements:
- Replace “Required decision: ACCEPT” with one of:
  - Required decision: implementation authorization required
  - Required decision: human checkpoint required
  - Required decision: none for planning; implementation remains unauthorized
  - Required decision: REQUIRES_HUMAN_DECISION
- Replace “[CLASSIFICATION]” with:
  - [REJECT] for blockers
  - [ACCEPT_WITH_MODIFICATION] for fixable findings
  - [REQUIRES_HUMAN_DECISION] for protected drift/human choices

## 7. .aos-tmp boundary
Explain exact boundary:
- `.aos-tmp` is local-only, ignored, disposable scratch space.
- `.aos-tmp` is not the Source of Truth.
- Do not store Evidence, approvals, checkpoints, reports, or canonical outputs in `.aos-tmp`.
- Runner defaults may use `.aos-tmp` only if outputs are temporary drafts and non-authoritative.

## 8. reports/examples boundary
Explain allowed and forbidden action:
- Do not authorize moving files to `tests/fixtures` in 470 unless `tests/fixtures` is explicitly added to the allowed scope by a human.
- For 470, the preferred actions are:
  - sanitize/genericize in place inside `aos/reports/examples`, or
  - create generic examples under `aos/examples`, or
  - mark the move to `tests/fixtures` as PARKING_LOT / REQUIRES_HUMAN_DECISION.

## 9. Human checkpoints required before 470
List decisions:
- Review and authorize this tightened allowed file scope.
- Approve the target location for sanitized examples (in-place vs generic `aos/examples` vs deferred move to `tests/fixtures`).
- Authorize execution for 470 based on this addendum.

## 10. Final handoff decision
AOS-FARM.470 READY: CONDITIONAL
MERGE TECHNICAL READINESS: NO
MERGE GOVERNANCE DECISION: REQUIRES_HUMAN_DECISION
