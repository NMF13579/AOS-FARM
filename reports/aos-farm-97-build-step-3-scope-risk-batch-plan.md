# AOS-FARM.97 — Build Step 3 Scope / Risk / Batch Plan

## 1. Summary

```yaml
task_id: AOS-FARM.97
task_name: "Build Step 3 Scope, Risk, Batch Plan, and Execution Authorization Preparation"
report_date: "2026-06-14"
report_type: planning_and_authorization_preparation
mode: planning_only
implementation_performed: false
commit_performed: false
push_performed: false
```

This report defines the full scope of Build Step 3 — Minimal Safety Floor Formalization,
groups Step 3 tasks at the maximum safe boundary, proposes one large docs/templates-only
execution batch, prepares the execution authorization package for that batch, and creates
a pending Human Execution Checkpoint.

This report does NOT authorize execution. It does NOT authorize commit. It does NOT authorize push.
Human approval cannot be simulated.

---

## 2. Preconditions Checked

| Precondition | Required | Actual | Result |
|---|---|---|---|
| Current branch | dev | dev | ✅ PASS |
| HEAD SHA | 1ef2f3a034b07888b158243ed8127a438589dd61 | 1ef2f3a034b07888b158243ed8127a438589dd61 | ✅ PASS |
| origin/dev SHA | 1ef2f3a034b07888b158243ed8127a438589dd61 | 1ef2f3a034b07888b158243ed8127a438589dd61 | ✅ PASS |
| dev ahead origin/dev | 0 | 0 | ✅ PASS |
| Remote baseline closed | true | true | ✅ PASS |
| AOS-FARM.96.17 closure report exists | true | true | ✅ PASS |
| Working tree staged files | 0 | 0 | ✅ PASS |

**Precondition summary: ALL PASSED. No blockers.**

---

## 3. Required Sources Availability

| Source | Required | Available | Result |
|---|---|---|---|
| 00_AOS_Core_Control.md | true | true | ✅ PRESENT |
| 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md | true | true | ✅ PRESENT |
| 02_AOS_Governance_Control_Module_and_Safety_Rules.md | true | true | ✅ PRESENT |

**All three required sources confirmed available and read.**

Source precedence applied:

```text
00_AOS_Core_Control.md = highest canonical project control source
01_AOS_Assembly_Pipelines_and_Build_Roadmap.md = authority for Assembly Pipelines, Build Step roadmap
02_AOS_Governance_Control_Module_and_Safety_Rules.md = authority for safety, Risk Profiles, gates,
  approval boundary, lifecycle boundary, protected/canonical rules, destructive operations,
  UNKNOWN/NOT_RUN/PASS semantics
```

No source conflicts detected.

---

## 4. Current Git Baseline

```yaml
current_branch: dev
head_sha: "1ef2f3a034b07888b158243ed8127a438589dd61"
origin_dev_sha: "1ef2f3a034b07888b158243ed8127a438589dd61"
head_equals_origin_dev: true
dev_ahead_origin_dev_by: 0
staged_files: 0
remote_baseline_closed: true
```

Working tree status at time of this report: untracked files only (post-push evidence artifacts and
older deferred housekeeping — classified in AOS-FARM.96.17, no action taken here).

---

## 5. Step 2 Closure Dependency

```yaml
closure_report: reports/aos-farm-96-17-build-step-2-post-push-remote-baseline-closure.md
closure_report_exists: true
closure_final_status: AOS_FARM_96_17_BUILD_STEP_2_REMOTE_BASELINE_CLOSED
build_step_2_committed: true
build_step_2_pushed: true
remote_baseline_closed: true
may_start_build_step_3_planning_stream: true
```

AOS-FARM.96.17 confirmed Step 2 fully complete and remote baseline closed.
Step 3 planning is explicitly permitted by AOS-FARM.96.17.

---

## 6. Build Step 3 Objective

**Build Step 3 Name:** Minimal Safety Floor Formalization

**Authority source:** `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` — Build Step 3 definition.

```text
Build Step 3 — Minimal Safety Floor Formalization

Goal:
  формально закрепить always-on safety semantics для documentation и code flows

Must include:
  PASS ≠ approval
  Evidence ≠ approval
  CI PASS ≠ approval
  UNKNOWN ≠ OK
  NOT_RUN ≠ PASS
  no fake human approval
  no auto-merge
  no auto-commit
  no lifecycle mutation without rule
  no protected/canonical change without checkpoint

Important:
  Minimal Safety Floor действует с Build Step 0.
  Build Step 3 только формализует и проверяет его, а не включает впервые.
```

Build Step 3 is the formal documentation and template layer that records, for the repository,
the always-on safety semantics that have governed the project since Build Step 0. It does not
introduce new runtime enforcement. It does not create validators. It does not create CI workflows.

**Minimum Risk Profile for Task 3 (per 01 Roadmap table):**

```text
Task 3 | Build Step 3 | Minimal Safety Floor Formalization | HIGH_RISK_PROTECTED
```

> Note: The 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md table lists HIGH_RISK_PROTECTED as
> the minimum profile for Task 3. However, the Batch 1 proposed scope is limited to
> docs/templates/reports only — no protected/canonical files modified, no validators,
> no runtime enforcement. The agent proposes MEDIUM_RISK_GUIDED for the docs-only batch;
> the human must assign the final profile. If the human assigns HIGH_RISK_PROTECTED, that
> governs execution and the checkpoint must be updated accordingly.

---

## 7. Minimal Safety Floor Semantics

These invariants are always-on and must be included in all Step 3 formalization artifacts.
They are sourced from `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`,
and `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.

```text
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
Verification PASS ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
BLOCKED ≠ PASS.
Human approval cannot be simulated.
Human approval cannot be inferred.
Human approval cannot be replaced by agent text.
Scope proposal ≠ execution authorization.
Execution authorization ≠ commit authorization.
Commit authorization ≠ push authorization.
Push authorization ≠ release authorization.
Remote baseline closure ≠ production use.
No auto-commit.
No auto-push.
No auto-merge.
No release without explicit human authorization.
No production use without explicit human authorization.
No protected/canonical change without explicit checkpoint.
No destructive operation by default.
Scope must not expand without explicit human permission.
Agent may propose Risk Profile, but cannot self-assign LOW_RISK_FAST.
Human unavailable for required review/approval/checkpoint/Risk Profile assignment → BLOCKED or HUMAN_REVIEW_REQUIRED.
```

---

## 8. Upper Safety Boundary Grouping Rule

**Rule (per task instructions):**

> If the batch is docs/templates/reports only, does not modify protected/canonical files, does not
> create runtime/validator/CI implementation, and does not require destructive operations, then
> the batch should be grouped into one large bounded execution batch.

**Forbidden splitting rule:**

> Do not split Step 3 into many tiny tasks only for process ceremony.

**Required split rule:**

> Protected/canonical changes, CI/workflow changes, runtime implementation, validator implementation,
> scripts, or destructive operations must be separated into their own future checkpoint and must not
> be included in the first docs/templates-only Step 3 batch.

**Application to Step 3:**

The proposed Batch 1 scope (10 docs/templates/reports files) meets all conditions for grouping
into one large bounded execution batch:

- ✅ docs/templates/reports only
- ✅ does not modify protected/canonical sources (00, 01, 02)
- ✅ does not create runtime enforcement
- ✅ does not create validators
- ✅ does not create CI workflows or scripts
- ✅ does not perform destructive operations

**Decision: Group all 10 proposed outputs into one Batch 1.**

---

## 9. Proposed Step 3 Batch Strategy

```text
AOS-FARM.97 — Step 3 Scope, Risk, Batch Plan, and Execution Authorization Preparation  [THIS TASK]
AOS-FARM.98 — Human Execution Authorization for Step 3 Batch 1
AOS-FARM.99 — Controlled Execution: Step 3 Minimal Safety Floor Docs/Templates Batch
AOS-FARM.100 — Post-Execution Verification for Step 3 Batch 1
AOS-FARM.101 — Final Step 3 Verification
AOS-FARM.102 — Final Step 3 Commit Authorization Preparation
AOS-FARM.103 — Human Commit Authorization
AOS-FARM.104 — Controlled Final Step 3 Commit Execution
AOS-FARM.105 — Final Step 3 Push Authorization Preparation
AOS-FARM.106 — Human Push Authorization
AOS-FARM.107 — Controlled Final Step 3 Push Execution
AOS-FARM.108 — Post-Push Remote Baseline Closure
```

```yaml
proposed_batch_count: 12
commit_push_timing: "After AOS-FARM.101 Final Step 3 Verification — not after AOS-FARM.99"
no_commit_after_batch_execution: true
no_push_after_batch_execution: true
final_commit_and_push_after_final_verification_only: true
```

**Important commit/push boundary:**

```text
There must be no commit/push after AOS-FARM.99.
Commit/push happens only after final Step 3 verification (AOS-FARM.101).
```

---

## 10. Proposed Step 3 Batch 1 Artifact Set

**Target task:** AOS-FARM.99 — Controlled Execution: Step 3 Minimal Safety Floor Docs/Templates Batch

| # | Proposed Output File | Purpose |
|---|---|---|
| 1 | docs/governance/minimal-safety-floor.md | Formal document: always-on safety invariants |
| 2 | docs/governance/pass-evidence-approval-boundary.md | Formal document: PASS/Evidence/approval boundary |
| 3 | docs/governance/unknown-not-run-pass-semantics.md | Formal document: UNKNOWN/NOT_RUN/PASS semantics |
| 4 | docs/governance/human-checkpoint-boundary.md | Formal document: human checkpoint boundary |
| 5 | templates/minimal-safety-floor-checklist-template.md | Template: safety floor verification checklist |
| 6 | templates/safety-gate-matrix-template.md | Template: safety gate matrix |
| 7 | templates/human-approval-boundary-template.md | Template: human approval boundary |
| 8 | templates/unknown-not-run-pass-semantics-template.md | Template: UNKNOWN/NOT_RUN/PASS template |
| 9 | templates/step-safety-verification-report-template.md | Template: step safety verification report |
| 10 | reports/aos-farm-minimal-safety-floor-formalization-report.md | Report: formalization summary |

```yaml
proposed_output_count: 10
```

---

## 11. Existing Path / Conflict Check

| Path | Status | Action |
|---|---|---|
| docs/governance/minimal-safety-floor.md | CLEAR | Safe to create in AOS-FARM.99 |
| docs/governance/pass-evidence-approval-boundary.md | CLEAR | Safe to create in AOS-FARM.99 |
| docs/governance/unknown-not-run-pass-semantics.md | CLEAR | Safe to create in AOS-FARM.99 |
| docs/governance/human-checkpoint-boundary.md | CLEAR | Safe to create in AOS-FARM.99 |
| templates/minimal-safety-floor-checklist-template.md | CLEAR | Safe to create in AOS-FARM.99 |
| templates/safety-gate-matrix-template.md | CLEAR | Safe to create in AOS-FARM.99 |
| templates/human-approval-boundary-template.md | CLEAR | Safe to create in AOS-FARM.99 |
| templates/unknown-not-run-pass-semantics-template.md | CLEAR | Safe to create in AOS-FARM.99 |
| templates/step-safety-verification-report-template.md | CLEAR | Safe to create in AOS-FARM.99 |
| reports/aos-farm-minimal-safety-floor-formalization-report.md | CLEAR | Safe to create in AOS-FARM.99 |

```yaml
path_conflict_count: 0
path_conflict_requiring_human_review: false
all_paths_clear: true
```

No path conflicts detected. All 10 proposed outputs are clear for future creation in AOS-FARM.99
(subject to human execution authorization).

---

## 12. Proposed Risk Profile

```yaml
agent_risk_profile_assignment_performed: false
human_risk_profile_assignment_required: true
agent_proposed_risk_profile: MEDIUM_RISK_GUIDED
human_assigned_risk_profile: PENDING_HUMAN_ASSIGNMENT
```

**Risk reasoning:**

```text
- The proposed Step 3 Batch 1 is docs/templates/reports only.
- It formalizes safety semantics already in effect since Build Step 0.
- It does not modify protected/canonical sources (00_AOS_Core_Control.md, 01, 02).
- It does not create runtime enforcement.
- It does not create validators.
- It does not create CI workflows.
- It does not perform destructive operations.
- Because it affects safety semantics documentation, it is not LOW_RISK_FAST.
- Suggested profile is MEDIUM_RISK_GUIDED, pending human assignment.
- Note: 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md Task 3 table entry lists HIGH_RISK_PROTECTED
  as minimum. Human must review and assign the final profile for AOS-FARM.99.
- Agent may NOT self-assign LOW_RISK_FAST (prohibited by 02 and 00).
- If human assigns HIGH_RISK_PROTECTED, the checkpoint and authorization package must be updated.
```

---

## 13. Required Human Checkpoints

| Checkpoint | Purpose | Status |
|---|---|---|
| AOS-FARM.97 Human Checkpoint (this task creates it) | Pending execution authorization for Batch 1 | PENDING_HUMAN_REVIEW |
| AOS-FARM.98 Human Execution Authorization | Explicit human go/no-go for AOS-FARM.99 | NOT_YET_CREATED |
| AOS-FARM.103 Human Commit Authorization | Explicit human commit authorization | NOT_YET_CREATED |
| AOS-FARM.106 Human Push Authorization | Explicit human push authorization | NOT_YET_CREATED |

```yaml
human_checkpoint_required_before_execution: true
human_checkpoint_required_before_commit: true
human_checkpoint_required_before_push: true
checkpoint_may_be_simulated: false
checkpoint_may_be_inferred: false
checkpoint_may_be_replaced_by_agent_text: false
```

---

## 14. Forbidden Scope

The following actions are FORBIDDEN in AOS-FARM.97 and in AOS-FARM.99 (Batch 1):

```text
modify 00_AOS_Core_Control.md
modify 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
modify 02_AOS_Governance_Control_Module_and_Safety_Rules.md
modify any protected/canonical file
create Step 3 implementation artifacts (runtime enforcement, validators, CI workflows)
create any of the 10 proposed Batch 1 output files (reserved for AOS-FARM.99)
stage files
commit
push
merge
release
enable production use
run Spec Kit commands
add Spec Kit dependency
create runtime enforcement
create validator implementation
create CI workflow
delete files
move files
rename files
archive files
simulate approval
assign LOW_RISK_FAST without explicit human instruction
claim PASS as approval
claim Evidence as approval
claim CI PASS as approval
expand scope beyond the 10 proposed Batch 1 output files without explicit human permission
```

---

## 15. Verification Plan

**After AOS-FARM.99 execution (Batch 1), verify:**

```bash
# File existence checks
test -f docs/governance/minimal-safety-floor.md && echo "EXISTS: minimal-safety-floor.md"
test -f docs/governance/pass-evidence-approval-boundary.md && echo "EXISTS: pass-evidence-approval-boundary.md"
test -f docs/governance/unknown-not-run-pass-semantics.md && echo "EXISTS: unknown-not-run-pass-semantics.md"
test -f docs/governance/human-checkpoint-boundary.md && echo "EXISTS: human-checkpoint-boundary.md"
test -f templates/minimal-safety-floor-checklist-template.md && echo "EXISTS: minimal-safety-floor-checklist-template.md"
test -f templates/safety-gate-matrix-template.md && echo "EXISTS: safety-gate-matrix-template.md"
test -f templates/human-approval-boundary-template.md && echo "EXISTS: human-approval-boundary-template.md"
test -f templates/unknown-not-run-pass-semantics-template.md && echo "EXISTS: unknown-not-run-pass-semantics-template.md"
test -f templates/step-safety-verification-report-template.md && echo "EXISTS: step-safety-verification-report-template.md"
test -f reports/aos-farm-minimal-safety-floor-formalization-report.md && echo "EXISTS: formalization-report.md"

# Git state — no commit should have occurred
git status --short
git rev-parse HEAD
git rev-parse origin/dev

# Semantic invariant checks in produced docs
grep -R "PASS ≠ approval" docs/governance/
grep -R "Evidence ≠ approval" docs/governance/
grep -R "CI PASS ≠ approval" docs/governance/
grep -R "UNKNOWN ≠ OK" docs/governance/
grep -R "NOT_RUN ≠ PASS" docs/governance/
grep -R "Human approval cannot be simulated" docs/governance/
```

**Protected source integrity checks:**

```bash
# Confirm no protected/canonical sources were modified
git diff HEAD -- 00_AOS_Core_Control.md
git diff HEAD -- 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
git diff HEAD -- 02_AOS_Governance_Control_Module_and_Safety_Rules.md
```

---

## 16. Final Step 3 Commit / Push Strategy

```text
AOS-FARM.99 — Controlled Execution: creates the 10 Batch 1 output files. No commit.
AOS-FARM.100 — Post-Execution Verification. No commit.
AOS-FARM.101 — Final Step 3 Verification. No commit.
AOS-FARM.102 — Final Step 3 Commit Authorization Preparation. Prepares commit package. No commit.
AOS-FARM.103 — Human Commit Authorization. Human approves commit. No commit until human authorizes.
AOS-FARM.104 — Controlled Final Step 3 Commit Execution. Commit performed after human authorization.
AOS-FARM.105 — Final Step 3 Push Authorization Preparation. Prepares push package. No push.
AOS-FARM.106 — Human Push Authorization. Human approves push. No push until human authorizes.
AOS-FARM.107 — Controlled Final Step 3 Push Execution. Push performed after human authorization.
AOS-FARM.108 — Post-Push Remote Baseline Closure. Closure report.
```

```yaml
commit_after_aos_farm_99: false
commit_after_batch_execution: false
commit_authorized_now: false
push_authorized_now: false
one_final_commit_for_all_step_3: true
one_final_push_for_all_step_3: true
final_commit_gate: "AOS-FARM.103 Human Commit Authorization"
final_push_gate: "AOS-FARM.106 Human Push Authorization"
```

---

## 17. Deferred Housekeeping Boundary

The following untracked files from AOS-FARM.96.17 are not in scope for Step 3:

```text
reports/aos-farm-84-commit-post-push-remote-baseline-closure.md
reports/aos-farm-84-commit-push-authorization-package.md
reports/aos-farm-85-88-evidence-artifacts-commit-authorization-package.md
reports/aos-farm-96-14-final-build-step-2-push-authorization-package.md
reports/aos-farm-96-17-build-step-2-post-push-remote-baseline-closure.md
reports/aos-farm-build-step-2-planning-artifacts-push-authorization-package.md
reports/aos-farm-post-skeleton-push-authorization-package.md
reports/human-checkpoints/aos-farm-84-commit-push-authorization.md
reports/human-checkpoints/aos-farm-85-88-evidence-artifacts-commit-authorization.md
reports/human-checkpoints/aos-farm-96-14-final-build-step-2-push-authorization.md
reports/human-checkpoints/aos-farm-build-step-2-planning-artifacts-push-authorization.md
reports/human-checkpoints/aos-farm-post-skeleton-push-authorization.md
reports/human-checkpoints/aos-farm-push-evidence-push-authorization.md
reports/human-checkpoints/aos-farm-push-evidence-working-tree-addendum.md
```

Also not in scope for Step 3 (AOS-FARM.97 planning files, will be untracked until Step 3 commit):

```text
reports/aos-farm-97-build-step-3-scope-risk-batch-plan.md  (this file)
reports/aos-farm-97-step-3-batch-1-execution-authorization-package.md
reports/human-checkpoints/aos-farm-97-step-3-batch-1-execution-authorization.md
```

Deferred housekeeping classification: unchanged from AOS-FARM.96.17. No action taken.
These files remain untracked and uncommitted. Human must authorize any changes to this boundary.

---

## 18. Next Recommended Task

```text
AOS-FARM.98 — Human Execution Authorization for Step 3 Batch 1
```

Human must review:
1. The Step 3 batch plan (this report).
2. The Step 3 Batch 1 execution authorization package.
3. The pending Human Checkpoint at `reports/human-checkpoints/aos-farm-97-step-3-batch-1-execution-authorization.md`.
4. Assign a Risk Profile for AOS-FARM.99 (proposed: MEDIUM_RISK_GUIDED; minimum per roadmap: HIGH_RISK_PROTECTED).
5. Provide explicit written execution authorization (or rejection) for AOS-FARM.99.

No execution may proceed until AOS-FARM.98 human authorization is complete.

---

## 19. Final Status

```yaml
task_id: AOS-FARM.97
report_type: planning_and_authorization_preparation

closure_report_96_17_existed: true
current_branch: "dev"
head_sha: "1ef2f3a034b07888b158243ed8127a438589dd61"
origin_dev_sha: "1ef2f3a034b07888b158243ed8127a438589dd61"
dev_ahead_origin_dev_by: 0
remote_baseline_closed: true

required_sources_present: true
source_00_present: true
source_01_present: true
source_02_present: true

files_created_by_aos_farm_97:
  - reports/aos-farm-97-build-step-3-scope-risk-batch-plan.md
  - reports/aos-farm-97-step-3-batch-1-execution-authorization-package.md
  - reports/human-checkpoints/aos-farm-97-step-3-batch-1-execution-authorization.md

proposed_step_3_batch_count: 12
proposed_step_3_batch_1_output_count: 10
path_conflict_count: 0
path_conflict_requiring_human_review: false

agent_proposed_risk_profile: MEDIUM_RISK_GUIDED
human_risk_profile_assignment_required: true
human_assigned_risk_profile: PENDING_HUMAN_ASSIGNMENT
agent_risk_profile_assignment_performed: false

execution_authorized_now: false
commit_authorized_now: false
push_authorized_now: false
release_authorized_now: false
production_use_authorized_now: false

implementation_artifacts_created: false
protected_canonical_files_modified: false
staging_performed: false
commit_performed: false
push_performed: false
merge_performed: false
release_performed: false
destructive_operations_performed: false
spec_kit_commands_run: false

blocking_issue_count: 0
warning_count: 0

recommended_next_task: "AOS-FARM.98 — Human Execution Authorization for Step 3 Batch 1"

FINAL_STATUS: AOS_FARM_97_BUILD_STEP_3_SCOPE_RISK_BATCH_PLAN_CREATED
```
