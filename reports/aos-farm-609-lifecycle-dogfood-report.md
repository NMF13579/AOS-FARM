# AOS-FARM.609 — Full Lifecycle Dogfood Audit Report

## Executive Summary

This audit is report-only and does not approve, execute, commit, push, merge, or mutate lifecycle state.

Proposed Risk Profile only:

```yaml
risk_profile_proposal: MEDIUM_RISK_GUIDED
final_assignment_by_human_required: true
```

Most recent fully reconstructable end-to-end lifecycle from available repository evidence:

```text
AOS-FARM.505 / AOS-FARM-DRAFT-CANDIDATE-0004
-> AOS-FARM.507
-> AOS-FARM.509 / tasks/AOS-FARM-TASK-0509.md
-> AOS-FARM.511
-> AOS-FARM.512
-> AOS-FARM.541
-> AOS-FARM.542
-> AOS-FARM.543
-> AOS-FARM.544
-> AOS-FARM.545
-> AOS-FARM.546
-> AOS-FARM.547
-> AOS-FARM.548
```

This chain is the best dogfood target because it is the latest evidence trail that covers task candidate selection, task drafting, human execution gate, execution, execution review, commit review, human commit, push review, human push, remote closure, and final acceptance-style review.

Later chains were also inspected:
- `AOS-FARM.564` through `AOS-FARM.570`: narrower follow-on lifecycle for queue remediation and dual-remote closure.
- `AOS-FARM.588` through `AOS-FARM.596`: later product and merge-related lifecycle evidence, but less clean as a single task lifecycle.
- `AOS-FARM.607`: recent implementation evidence, but not a completed full lifecycle.

Final verdict:

```text
The lifecycle is usable and safety-preserving, but high-friction, report-heavy, and partially duplicated.
It succeeds technically more often than it succeeds as a compact human workflow.
```

## Source / Authority Boundary

Required authority sources were read in order:
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

Authority rules preserved:
- PASS is not approval.
- Evidence is not approval.
- CI PASS is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Human approval cannot be simulated.
- Commit authorization is not push authorization.
- Push authorization is not release authorization.

## Evidence Base

Primary lifecycle evidence:
- `reports/aos-farm-505-draft-task-candidates.md`
- `reports/aos-farm-507-planning-cycle-final-review-package.md`
- `reports/aos-farm-509-candidate-0004-promotion-task-draft-report.md`
- `tasks/AOS-FARM-TASK-0509.md`
- `reports/aos-farm-511-task-0509-risk-profile-execution-gate-report.md`
- `reports/aos-farm-512-task-0509-execution-report.md`
- `reports/aos-farm-541-third-pass-active-package-closure-review-retake.md`
- `reports/aos-farm-542-commit-authorization-review-third-pass-active-package.md`
- `reports/aos-farm-543-human-commit-authorization-and-commit-execution-report.md`
- `reports/aos-farm-544-push-authorization-review-third-pass-active-package.md`
- `reports/aos-farm-545-human-push-authorization-and-push-execution-report.md`
- `reports/aos-farm-546-post-push-remote-closure-review.md`
- `reports/aos-farm-547-third-pass-final-local-remote-closure-report.md`
- `reports/aos-farm-548-third-pass-final-stage-acceptance-review.md`

Follow-on evidence used for friction and architecture:
- `reports/aos-farm-564-active-manual-queue-lifecycle-remediation-report.md`
- `reports/aos-farm-565-queue-next-candidate-status-semantics-fix-report.md`
- `reports/aos-farm-566-combined-564-565-commit-authorization-package.md`
- `reports/aos-farm-568-push-authorization-review.md`
- `reports/aos-farm-570-push-execution-and-remote-closure-report.md`
- `reports/aos-farm-594-post-main-merge-final-closure-review.md`
- `reports/aos-farm-595-consumer-guidance-polish-closure-report.md`
- `reports/aos-farm-596-human-review-package.md`
- `reports/aos-farm-607-lifecycle-state-reconciliation-final-report.md`

## Baseline State

Collection time baseline:

```text
git branch --show-current
work/aos-farm-601-code-execution-alignment

git rev-parse HEAD
25577219c33fb2a9e91bc188eb660276b21f57e5

git rev-parse origin/dev
25577219c33fb2a9e91bc188eb660276b21f57e5

git rev-parse origin/main
25577219c33fb2a9e91bc188eb660276b21f57e5

git ls-remote origin refs/heads/dev
25577219c33fb2a9e91bc188eb660276b21f57e5 refs/heads/dev

git ls-remote origin refs/heads/main
25577219c33fb2a9e91bc188eb660276b21f57e5 refs/heads/main

git rev-list --left-right --count origin/dev...HEAD
0 0

git rev-list --left-right --count origin/main...HEAD
0 0

git rev-list --left-right --count origin/main...origin/dev
0 0

git status -sb
## work/aos-farm-601-code-execution-alignment

git status --short --untracked-files=all
[empty]
```

Baseline interpretation:
- The active branch at audit time is not `dev`; it is `work/aos-farm-601-code-execution-alignment`.
- `HEAD`, `origin/dev`, and `origin/main` are all equal at `25577219c33fb2a9e91bc188eb660276b21f57e5`.
- Working tree was clean before AOS-FARM.609 report creation.
- `git fetch origin` required elevated Git metadata access because `.git/FETCH_HEAD` is not writable in the default sandbox.

## Reconstructed Lifecycle Map

Target chain audited:
- Candidate 0004 / Task 0509 path, plus package-level commit/push/closure stages.

| Expected Node | Actual Step | Artifact | Decision maker | Mandatory | Technical | Exists due to non-optimized process? | Evidence path |
|---|---|---|---|---|---|---|---|
| Task Candidate | Draft Task Candidate creation | AOS-FARM.505 candidate 0004 | agent, then human review pending | yes | mostly documentation | yes | `reports/aos-farm-505-draft-task-candidates.md` |
| Human Review Preparation | Planning cycle final review package | AOS-FARM.507 | agent prepared, human pending | yes | partly | yes | `reports/aos-farm-507-planning-cycle-final-review-package.md` |
| Clarification | Pre-existing duplicate task cleanup boundary review | AOS-FARM.508 | agent | no | yes | yes | `reports/aos-farm-508-pre-existing-untracked-task-duplicate-cleanup-review.md` |
| Clarification Review | Task draft creation for selected candidate | AOS-FARM.509 | agent | yes | yes | yes | `reports/aos-farm-509-candidate-0004-promotion-task-draft-report.md` |
| Execution Authorization Review | Task draft plus human gate preparation | collapsed into 509 and 511 | human + agent | yes | yes | yes | `reports/aos-farm-509-candidate-0004-promotion-task-draft-report.md`, `reports/aos-farm-511-task-0509-risk-profile-execution-gate-report.md` |
| Execution Authorization | Human assigns Risk Profile and execution | AOS-FARM.511 | human | yes | partly | no | `reports/aos-farm-511-task-0509-risk-profile-execution-gate-report.md` |
| Execution | Task execution | AOS-FARM.512 | agent | yes | yes | no | `reports/aos-farm-512-task-0509-execution-report.md` |
| Execution Review | Package closure review retake | AOS-FARM.541 | agent review for human | yes | yes | yes | `reports/aos-farm-541-third-pass-active-package-closure-review-retake.md` |
| Commit Authorization Review | Commit review | AOS-FARM.542 | agent review for human | yes | yes | yes | `reports/aos-farm-542-commit-authorization-review-third-pass-active-package.md` |
| Commit Authorization | Human commit authorization | embedded in AOS-FARM.543 | human | yes | no | no | `reports/aos-farm-543-human-commit-authorization-and-commit-execution-report.md` |
| Commit | Local commit execution | AOS-FARM.543 | git after human authorization | yes | yes | no | `reports/aos-farm-543-human-commit-authorization-and-commit-execution-report.md` |
| Push Authorization Review | Push review | AOS-FARM.544 | agent review for human | yes | yes | yes | `reports/aos-farm-544-push-authorization-review-third-pass-active-package.md` |
| Push Authorization | Human push authorization | embedded in AOS-FARM.545 | human | yes | no | no | `reports/aos-farm-545-human-push-authorization-and-push-execution-report.md` |
| Push | Push execution to `origin/dev` | AOS-FARM.545 | git after human authorization | yes | yes | no | `reports/aos-farm-545-human-push-authorization-and-push-execution-report.md` |
| Remote Closure | Post-push and final closure review | AOS-FARM.546, .547, .548 | agent review plus git evidence | yes | yes | yes | `reports/aos-farm-546-post-push-remote-closure-review.md`, `reports/aos-farm-547-third-pass-final-local-remote-closure-report.md`, `reports/aos-farm-548-third-pass-final-stage-acceptance-review.md` |

Reconstruction note:
- The lifecycle exists, but several expected nodes are split or collapsed across multiple reports.
- Exact separate artifacts for "Clarification" and "Clarification Review" are only partially reconstructable; therefore those mappings are best-effort and should be treated as partially inferred from artifact sequence.

## Cost Audit

Counts are exact only where the repository artifacts explicitly state them.
Prompt and response counts are not recorded in repo artifacts, so those cells are `UNKNOWN`.

| Step | Prompts | Human decisions | Git commands | Validation commands | Changed files | Reports | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| Task Candidate | UNKNOWN | approximate_from_available_evidence: 1 review gate pending | UNKNOWN | approximate_from_available_evidence | approximate_from_available_evidence | 6 | planning cycle produced `502` through `507`; assistant responses UNKNOWN |
| Human Review Preparation | UNKNOWN | 1 pending package review | UNKNOWN | approximate_from_available_evidence | 1 | 1 | `507`; report-only |
| Clarification | UNKNOWN | 0 | UNKNOWN | UNKNOWN | 0 | 1 | `508`; boundary cleanup review |
| Clarification Review / Task Draft | UNKNOWN | 1 promotion decision pending | UNKNOWN | at least 1 | 2 | 1 | `509` creates task file plus report |
| Execution Authorization | UNKNOWN | 1 | UNKNOWN | at least 1 | 1 | 1 | `511`; task metadata gate |
| Execution | UNKNOWN | 0 | at least 2 | at least 1 | 2 | 1 | `512`; one output artifact plus report |
| Execution Review | UNKNOWN | 0 | approximate_from_available_evidence | at least 4 | package-wide | 1 | `541`; package closure retake |
| Commit Authorization Review | UNKNOWN | 1 recommended | approximate_from_available_evidence | at least 4 | 0 | 1 | `542`; review only |
| Commit Authorization + Commit | UNKNOWN | 1 | at least 2 | at least 4 | package-wide commit payload | 1 | `543`; human decision embedded, commit result partly deferred to runtime output |
| Push Authorization Review | UNKNOWN | 1 recommended | at least 5 | at least 4 | 0 | 1 | `544`; review only |
| Push Authorization + Push | UNKNOWN | 1 | at least 5 | at least 4 | 0 | 1 | `545`; actual push to `origin/dev` |
| Remote Closure | UNKNOWN | 0 | at least 6 | at least 4 | 0 | 3 | `546`, `547`, `548`; repeated sync checks and acceptance-style review |

Cost observations:
- The process preserves authority boundaries well.
- The process also rechecks the same git facts multiple times across adjacent stages.
- The report count is high relative to the payload size of a single task.

## Friction Audit

id: FRICTION-001
phase: Task Candidate to Task Draft
finding: Candidate selection, draft promotion, and human checkpoint intent are split across too many report artifacts before any real work starts.
evidence: `AOS-FARM.505`, `AOS-FARM.507`, `AOS-FARM.509`
impact: High cognitive load before execution; hard for a non-programmer to know which artifact is the live one.
safety_risk: Medium because confusion can lead to accidental task promotion assumptions.
suggested_direction: Keep the boundaries, but collapse planning handoff into one canonical candidate-to-task conversion package.

id: FRICTION-002
phase: Execution Authorization
finding: Human authorization is preserved correctly, but the review package and authorization artifact are partly fused and partly separate across tasks.
evidence: `AOS-FARM.509`, `AOS-FARM.511`
impact: Human must infer whether they are reviewing, authorizing, or both.
safety_risk: Medium due to decision-boundary ambiguity.
suggested_direction: Standardize one exact pre-execution packet with explicit `review_only` and one exact authorization witness.

id: FRICTION-003
phase: Execution Review
finding: Execution review for the package happened much later and after multiple sibling tasks, not immediately after each task.
evidence: `AOS-FARM.512` followed by package reviews `541`, `542`
impact: Hard to mentally connect one execution artifact to one later commit/push decision.
safety_risk: Low to medium.
suggested_direction: Generate package index manifests automatically so later reviews can point to exact task-to-commit lineage.

id: FRICTION-004
phase: Commit / Push Review
finding: Commit authorization review, commit execution report, push authorization review, push execution report, post-push closure review, and final acceptance review all repeat similar git and validation facts.
evidence: `AOS-FARM.542` to `AOS-FARM.548`
impact: Heavy manual reading cost; duplicated commands; long prompts and long reports.
safety_risk: Low for safety, high for fatigue.
suggested_direction: Auto-assemble a bounded evidence bundle once, then reuse it across commit and push checkpoints.

id: FRICTION-005
phase: Remote Closure
finding: There are three closure-style reports after push for the same remote state.
evidence: `AOS-FARM.546`, `AOS-FARM.547`, `AOS-FARM.548`
impact: Human re-confirms already-known information.
safety_risk: Low.
suggested_direction: Reduce to one mandatory remote closure verification plus one optional acceptance review only when a separate human decision is truly needed.

id: FRICTION-006
phase: Queue / Lifecycle Semantics
finding: Queue helper, dashboard, validator, and lifecycle status later drifted enough to require `AOS-FARM.564`, `AOS-FARM.565`, and `AOS-FARM.607`.
evidence: `AOS-FARM.564`, `AOS-FARM.565`, `AOS-FARM.607`
impact: Human cannot trust a single derived state view.
safety_risk: High because a done task can still look like the next active task.
suggested_direction: Introduce one read-only lifecycle reconciler as the authoritative derived state engine for queue/dashboard/review tooling.

id: FRICTION-007
phase: Terminology
finding: `READY_FOR_EXECUTION`, `READY_FOR_HANDOFF`, `READY_FOR_HUMAN_REVIEW`, acceptance review, and closure review are all meaningful but hard to parse without an internal map.
evidence: `AOS-FARM.507`, `AOS-FARM.541`, `AOS-FARM.548`, `AOS-FARM.607`
impact: High friction for new or occasional users.
safety_risk: Medium because semantic misunderstanding can be mistaken for permission.
suggested_direction: Publish one compact lifecycle legend and require each report to link to the exact legend row it is using.

## Architecture Audit

id: ARCH-001
area: Derived state
finding: Queue helper, queue dashboard, and later lifecycle reconciler each compute "what is next" differently.
evidence: `AOS-FARM.565`, `AOS-FARM.607`
source_of_truth_risk: High; multiple derived views compete.
safety_risk: High; a `DONE` task was still surfaced as next.
user_friction: High.
recommended_fix: One shared read-only lifecycle state library consumed by queue, dashboard, validator, and review tooling.
priority: CRITICAL

id: ARCH-002
area: Reports as state memory
finding: The lifecycle is reconstructable mainly because reports are rich, but that also makes reports function like hidden operational memory.
evidence: `AOS-FARM.541` through `AOS-FARM.548`, `AOS-FARM.564` through `AOS-FARM.570`
source_of_truth_risk: Medium to high.
safety_risk: Medium.
user_friction: High.
recommended_fix: Introduce a small machine-readable lifecycle index per active package while keeping reports human-readable.
priority: IMPORTANT

id: ARCH-003
area: Review package assembly
finding: Human authorization stages depend on repeated manual assembly of the same file sets, command outputs, and boundary statements.
evidence: `AOS-FARM.542`, `AOS-FARM.544`, `AOS-FARM.568`
source_of_truth_risk: Medium.
safety_risk: Low to medium.
user_friction: High.
recommended_fix: Create a review package assembler that never authorizes anything, but prebuilds exact evidence packs.
priority: IMPORTANT

id: ARCH-004
area: Acceptance semantics
finding: Acceptance-style review appears after remote closure, but approval semantics remain intentionally false. This is safe but semantically noisy.
evidence: `AOS-FARM.548`
source_of_truth_risk: Medium.
safety_risk: Medium because "acceptance" sounds stronger than "review".
user_friction: Medium.
recommended_fix: Rename acceptance-style stages to explicit non-approval language unless a true human approval record exists.
priority: IMPORTANT

id: ARCH-005
area: Human checkpoint modeling
finding: Human decisions are sometimes separate files, sometimes embedded in reports, and sometimes only described textually.
evidence: `AOS-FARM.511`, `AOS-FARM.543`, `AOS-FARM.545`
source_of_truth_risk: Medium.
safety_risk: Medium.
user_friction: Medium.
recommended_fix: Standardize human decision witness format across execution, commit, and push.
priority: IMPORTANT

id: ARCH-006
area: Queue maturity
finding: Placeholder queue fields remained in real tasks long enough to require later remediation.
evidence: `AOS-FARM.541`, `AOS-FARM.564`, `AOS-FARM.565`
source_of_truth_risk: Medium.
safety_risk: Medium.
user_friction: Medium.
recommended_fix: Add guardrails for impossible queue combinations and surface them early in review packages.
priority: IMPORTANT

id: ARCH-007
area: Second Source of Truth boundary
finding: `.aos-tmp` is repeatedly discussed as not Source of Truth, which suggests the boundary is understood but operationally fragile.
evidence: `AOS-FARM.507`, `AOS-FARM.607`
source_of_truth_risk: Medium.
safety_risk: Medium.
user_friction: Low.
recommended_fix: Keep strict wording and add automated scanners for forbidden report/evidence/checkpoint placement.
priority: NICE_TO_HAVE

## Key Risks

- The biggest real risk is not unsafe automation; it is mismatched derived state across queue, dashboard, validator, and reports.
- The biggest human-factor risk is semantic overload: too many report types that all mean "not approval".
- The biggest cost risk is repeated manual review of identical git and validation evidence after commit and after push.
- The biggest architecture risk is treating reports as the only practical way to reconstruct lifecycle history.

## Final Verdict

```text
AOS-FARM.609 VERDICT:
SAFE BUT HEAVY
```

The audited lifecycle demonstrates strong safety instincts and good fail-closed behavior. It does not collapse approval boundaries, and the later remediation work shows the system can detect and repair drift.

The main dogfood result is that the lifecycle is still too expensive to operate manually. It needs consolidation of derived-state logic, compression of repeated review packaging, and a simpler human-facing map of stage semantics.
