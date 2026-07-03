# AOS-FARM.602 — Untracked Reports Triage Manifest

```yaml
document_type: untracked_reports_triage_manifest
task_id: AOS-FARM.602
subtask_id: AOS-FARM.602.1C
baseline: origin/dev == 24fa9f4e9246f9b1f287e4dec46e76a4f2d8d65a
branch_policy_exception: true
branch_policy_exception_reason: human owner has no terminal access; environment could not create branch; current branch equals origin/dev and tracked worktree is clean
status: DRAFT
approval_status: NOT_APPROVED
commit_authorized: false
push_authorized: false
release_authorized: false
destructive_cleanup_authorized: false
```

## 1. Purpose
Index the 105 pre-existing untracked root-level reports and propose preservation handling without modifying the original artifacts.

## 2. Safety Boundaries
This manifest is a review artifact only. It does not authorize preservation, deletion, commit, push, release, cleanup, or modification of any existing report/checkpoint file.

## 3. Branch Policy Exception
This manifest was created on `work/aos-farm-601-code-execution-alignment` only because branch creation was unavailable in the environment while `HEAD == origin/dev`, tracked files were clean, and untracked scope was limited to root-level `reports/`.

## 4. Inventory Summary
- Total untracked root-level reports before manifest: 105
- Files under `reports/human-checkpoints/`: 24
- Distinct task IDs represented: 39
- Note: the `39` count preserves the `AOS-FARM.602.0` inventory convention and includes one non-task-ID bucket represented by `NO_TASK_ID`.
- Files without obvious task ID: 1

## 5. Category Counts
- `human_checkpoint`: 24
- `commit_authorization_or_commit_report`: 16
- `push_authorization_or_push_report`: 47
- `execution_report`: 1
- `audit_or_review`: 8
- `closure_report`: 3
- `planning_or_package`: 3
- `duplicate_or_superseded_candidate`: 3
- `unknown_report_type`: 0

## 6. Preservation Recommendation Counts
- `PRESERVE_HIGH_VALUE`: 91
- `PRESERVE_OPTIONAL`: 11
- `SUPERSEDED_CANDIDATE`: 3
- `UNKNOWN_NEEDS_HUMAN_REVIEW`: 0

## 7. Task ID Grouping Summary
Top task IDs by file count:
- `AOS-FARM.438`: 9
- `AOS-FARM.439.P1`: 8
- `AOS-FARM.439.P2`: 8
- `AOS-FARM.442`: 6
- `AOS-FARM.445`: 6
- `AOS-FARM.443`: 5
- `AOS-FARM.444`: 5
- `AOS-FARM.440`: 4
- `AOS-FARM.441`: 4
- `AOS-FARM.446`: 4

Likely already closed or pushed stages:
- `AOS-FARM.369`
- `AOS-FARM.408`
- `AOS-FARM.419`
- `AOS-FARM.431`
- `AOS-FARM.438`
- `AOS-FARM.439.P1`
- `AOS-FARM.439.P2`
- `AOS-FARM.440`
- `AOS-FARM.441`
- `AOS-FARM.442`
- `AOS-FARM.443`
- `AOS-FARM.444`
- `AOS-FARM.445`
- `AOS-FARM.446`
- `AOS-FARM.447`
- `AOS-FARM.448`
- `AOS-FARM.449`
- `AOS-FARM.450`
- `AOS-FARM.451`
- `AOS-FARM.452`
- `AOS-FARM.453`
- `AOS-FARM.570`

Likely incomplete or non-closed stages:
- `AOS-FARM.367`
- `AOS-FARM.389`
- `AOS-FARM.407`
- `AOS-FARM.413`
- `AOS-FARM.415`
- `AOS-FARM.418`
- `AOS-FARM.430`
- `AOS-FARM.433`
- `AOS-FARM.434`

## 8. High-Value Preservation Candidates
Representative high-value groups:
- all files under `reports/human-checkpoints/`
- all `remote-baseline-closure-report` and `push-execution-report` files
- all `commit-execution-report` files
- all `stage-closure-summary` files
- authorization packages and final closure artifacts tied to completed tasks

High-value candidate count: 91

## 9. Optional Preservation Candidates
Optional candidate count: 11

Optional examples:
- `reports/aos-farm-354-deep-comprehensive-current-state-audit.md`
- `reports/aos-farm-361-spec-kit-and-recurring-warnings-inventory-audit.md`
- `reports/aos-farm-415-consumer-runtime-handoff-remediation-authorization-package.md`
- `reports/aos-farm-432-ta-to-task-brief-assembly-post-stage-audit.md`
- `reports/aos-farm-438-post-commit-verification-report.md`
- `reports/aos-farm-440-post-commit-verification-report.md`
- `reports/aos-farm-441-post-commit-verification-report.md`
- `reports/aos-farm-445-L-hash-reconciliation-report.md`
- `reports/aos-farm-469-product-boundary-stabilization-remediation-plan.md`
- `reports/aos-farm-469a-scope-tightening-addendum.md`

## 10. Superseded Candidates
Superseded candidate count: 3

- `reports/aos-farm-439-p1-post-commit-verification-report.md`
- `reports/aos-farm-439-p2-post-commit-verification-report.md`
- `reports/aos-farm-445-P1-local-temp-log-cleanup-report.md`

## 11. Files Without Obvious Task ID
- `reports/aos-farm-full-read-only-deep-audit-report.md`

## 12. Known Unknowns
- Classification is filename-first with targeted header checks for ambiguous files only.
- Closed vs incomplete stage grouping is inferred from artifact names such as `remote-baseline-closure`, `push-execution`, and authorization-package patterns.
- No deletion recommendation is made in this manifest.

## 13. Recommended Next Decision
Recommended next step: human review this manifest, then choose between preserving all historical evidence/checkpoints in a separate commit or preserving only the highest-value subset.

## 14. Full File Manifest
The table below enumerates all 105 pre-existing untracked report/checkpoint files.

## 15. Full File Manifest Table
| # | Path | Task ID | Category | Preservation Recommendation | Confidence | Rationale | Proposed Next Action |
|---:|---|---|---|---|---|---|---|
| 1 | `reports/aos-farm-354-deep-comprehensive-current-state-audit.md` | `AOS-FARM.354` | `audit_or_review` | `PRESERVE_OPTIONAL` | `HIGH_FILENAME` | audit or review artifact from filename | `REVIEW_BEFORE_PRESERVATION` |
| 2 | `reports/aos-farm-361-spec-kit-and-recurring-warnings-inventory-audit.md` | `AOS-FARM.361` | `audit_or_review` | `PRESERVE_OPTIONAL` | `HIGH_FILENAME` | audit or review artifact from filename | `REVIEW_BEFORE_PRESERVATION` |
| 3 | `reports/aos-farm-367-cleanup-commit-push-authorization-package.md` | `AOS-FARM.367` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 4 | `reports/aos-farm-369-cleanup-push-remote-baseline-closure.md` | `AOS-FARM.369` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 5 | `reports/aos-farm-389-final-aos-consumer-kit-commit-execution-report.md` | `AOS-FARM.389` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 6 | `reports/aos-farm-389-final-aos-consumer-kit-push-authorization-package.md` | `AOS-FARM.389` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 7 | `reports/aos-farm-407-combined-push-authorization-package.md` | `AOS-FARM.407` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 8 | `reports/aos-farm-408-combined-push-remote-baseline-closure.md` | `AOS-FARM.408` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 9 | `reports/aos-farm-413-consumer-entry-flow-blocking-remediation-push-authorization-package.md` | `AOS-FARM.413` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 10 | `reports/aos-farm-415-consumer-runtime-handoff-remediation-authorization-package.md` | `AOS-FARM.415` | `planning_or_package` | `PRESERVE_OPTIONAL` | `HIGH_FILENAME` | planning or package artifact from filename | `KEEP_LOCAL_PENDING_REVIEW` |
| 11 | `reports/aos-farm-418-consumer-runtime-handoff-remediation-push-authorization-package.md` | `AOS-FARM.418` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 12 | `reports/aos-farm-419-consumer-runtime-handoff-remediation-push-execution-report.md` | `AOS-FARM.419` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 13 | `reports/aos-farm-429-ta-to-task-brief-assembly-layer-evidence-tail-commit-execution-report.md` | `AOS-FARM.429` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 14 | `reports/aos-farm-430-evidence-tail-push-authorization-package.md` | `AOS-FARM.430` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 15 | `reports/aos-farm-431-ta-to-task-brief-assembly-layer-evidence-tail-push-execution-report.md` | `AOS-FARM.431` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 16 | `reports/aos-farm-432-ta-to-task-brief-assembly-post-stage-audit.md` | `AOS-FARM.432` | `audit_or_review` | `PRESERVE_OPTIONAL` | `HIGH_FILENAME` | audit or review artifact from filename | `REVIEW_BEFORE_PRESERVATION` |
| 17 | `reports/aos-farm-433-first-controlled-task-execution-flow-push-authorization-package.md` | `AOS-FARM.433` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 18 | `reports/aos-farm-434-first-controlled-execution-bridge-mvp-push-authorization-package.md` | `AOS-FARM.434` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 19 | `reports/aos-farm-438-c-commit-authorization-package-report.md` | `AOS-FARM.438` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 20 | `reports/aos-farm-438-commit-authorization-package.md` | `AOS-FARM.438` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 21 | `reports/aos-farm-438-pa-push-authorization-package-report.md` | `AOS-FARM.438` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 22 | `reports/aos-farm-438-post-commit-verification-report.md` | `AOS-FARM.438` | `audit_or_review` | `PRESERVE_OPTIONAL` | `HIGH_FILENAME` | audit or review artifact from filename | `REVIEW_BEFORE_PRESERVATION` |
| 23 | `reports/aos-farm-438-push-authorization-package.md` | `AOS-FARM.438` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 24 | `reports/aos-farm-438-remote-baseline-closure-report.md` | `AOS-FARM.438` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 25 | `reports/aos-farm-439-controlled-execution-guard-integration-review.md` | `AOS-FARM.439` | `execution_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | execution artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 26 | `reports/aos-farm-439-p1-c-commit-authorization-package-report.md` | `AOS-FARM.439.P1` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 27 | `reports/aos-farm-439-p1-commit-authorization-package.md` | `AOS-FARM.439.P1` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 28 | `reports/aos-farm-439-p1-pa-push-authorization-package-report.md` | `AOS-FARM.439.P1` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 29 | `reports/aos-farm-439-p1-post-commit-verification-report.md` | `AOS-FARM.439.P1` | `duplicate_or_superseded_candidate` | `SUPERSEDED_CANDIDATE` | `HIGH_FILENAME` | post-commit verification appears superseded by remote closure artifacts | `SUPERSEDED_REVIEW_REQUIRED` |
| 30 | `reports/aos-farm-439-p1-push-authorization-package.md` | `AOS-FARM.439.P1` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 31 | `reports/aos-farm-439-p1-remote-baseline-closure-report.md` | `AOS-FARM.439.P1` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 32 | `reports/aos-farm-439-p2-c-commit-authorization-package-report.md` | `AOS-FARM.439.P2` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 33 | `reports/aos-farm-439-p2-commit-authorization-package.md` | `AOS-FARM.439.P2` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 34 | `reports/aos-farm-439-p2-pa-push-authorization-package-report.md` | `AOS-FARM.439.P2` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 35 | `reports/aos-farm-439-p2-post-commit-verification-report.md` | `AOS-FARM.439.P2` | `duplicate_or_superseded_candidate` | `SUPERSEDED_CANDIDATE` | `HIGH_FILENAME` | post-commit verification appears superseded by remote closure artifacts | `SUPERSEDED_REVIEW_REQUIRED` |
| 36 | `reports/aos-farm-439-p2-push-authorization-package.md` | `AOS-FARM.439.P2` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 37 | `reports/aos-farm-439-p2-remote-baseline-closure-report.md` | `AOS-FARM.439.P2` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 38 | `reports/aos-farm-440-post-commit-verification-report.md` | `AOS-FARM.440` | `audit_or_review` | `PRESERVE_OPTIONAL` | `HIGH_FILENAME` | audit or review artifact from filename | `REVIEW_BEFORE_PRESERVATION` |
| 39 | `reports/aos-farm-440-push-authorization-package.md` | `AOS-FARM.440` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 40 | `reports/aos-farm-440-remote-baseline-closure-report.md` | `AOS-FARM.440` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 41 | `reports/aos-farm-441-post-commit-verification-report.md` | `AOS-FARM.441` | `audit_or_review` | `PRESERVE_OPTIONAL` | `HIGH_FILENAME` | audit or review artifact from filename | `REVIEW_BEFORE_PRESERVATION` |
| 42 | `reports/aos-farm-441-push-authorization-package.md` | `AOS-FARM.441` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 43 | `reports/aos-farm-441-remote-baseline-closure-report.md` | `AOS-FARM.441` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 44 | `reports/aos-farm-442-commit-execution-report.md` | `AOS-FARM.442` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 45 | `reports/aos-farm-442-push-authorization-package.md` | `AOS-FARM.442` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 46 | `reports/aos-farm-442-push-execution-report.md` | `AOS-FARM.442` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 47 | `reports/aos-farm-442-remote-baseline-closure-report.md` | `AOS-FARM.442` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 48 | `reports/aos-farm-442-stage-closure-summary.md` | `AOS-FARM.442` | `closure_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | closure or final artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 49 | `reports/aos-farm-443-push-authorization-package.md` | `AOS-FARM.443` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 50 | `reports/aos-farm-443-push-execution-report.md` | `AOS-FARM.443` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 51 | `reports/aos-farm-443-remote-baseline-closure-report.md` | `AOS-FARM.443` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 52 | `reports/aos-farm-443-stage-closure-summary.md` | `AOS-FARM.443` | `closure_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | closure or final artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 53 | `reports/aos-farm-444-push-authorization-package.md` | `AOS-FARM.444` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 54 | `reports/aos-farm-444-push-execution-report.md` | `AOS-FARM.444` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 55 | `reports/aos-farm-444-remote-baseline-closure-report.md` | `AOS-FARM.444` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 56 | `reports/aos-farm-444-stage-closure-summary.md` | `AOS-FARM.444` | `closure_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | closure or final artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 57 | `reports/aos-farm-445-L-hash-reconciliation-report.md` | `AOS-FARM.445` | `audit_or_review` | `PRESERVE_OPTIONAL` | `HIGH_HEADER` | hash reconciliation report for push package typo investigation | `REVIEW_BEFORE_PRESERVATION` |
| 58 | `reports/aos-farm-445-P1-local-temp-log-cleanup-report.md` | `AOS-FARM.445` | `duplicate_or_superseded_candidate` | `SUPERSEDED_CANDIDATE` | `HIGH_FILENAME` | cleanup side-report appears superseded by main execution and closure artifacts | `SUPERSEDED_REVIEW_REQUIRED` |
| 59 | `reports/aos-farm-445-commit-execution-report.md` | `AOS-FARM.445` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 60 | `reports/aos-farm-445-push-execution-report.md` | `AOS-FARM.445` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 61 | `reports/aos-farm-445-remote-baseline-closure-report.md` | `AOS-FARM.445` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 62 | `reports/aos-farm-446-commit-execution-report.md` | `AOS-FARM.446` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 63 | `reports/aos-farm-446-push-execution-report.md` | `AOS-FARM.446` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 64 | `reports/aos-farm-446-remote-baseline-closure-report.md` | `AOS-FARM.446` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 65 | `reports/aos-farm-447-commit-execution-report.md` | `AOS-FARM.447` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 66 | `reports/aos-farm-447-push-execution-report.md` | `AOS-FARM.447` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 67 | `reports/aos-farm-447-remote-baseline-closure-report.md` | `AOS-FARM.447` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 68 | `reports/aos-farm-448-remote-baseline-closure-report.md` | `AOS-FARM.448` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 69 | `reports/aos-farm-449-remote-baseline-closure-report.md` | `AOS-FARM.449` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 70 | `reports/aos-farm-450-commit-report.md` | `AOS-FARM.450` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 71 | `reports/aos-farm-450-remote-baseline-closure-report.md` | `AOS-FARM.450` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 72 | `reports/aos-farm-451-commit-report.md` | `AOS-FARM.451` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 73 | `reports/aos-farm-451-remote-baseline-closure-report.md` | `AOS-FARM.451` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 74 | `reports/aos-farm-452-commit-report.md` | `AOS-FARM.452` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 75 | `reports/aos-farm-452-remote-baseline-closure-report.md` | `AOS-FARM.452` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 76 | `reports/aos-farm-453-commit-report.md` | `AOS-FARM.453` | `commit_authorization_or_commit_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | commit-stage artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 77 | `reports/aos-farm-453-remote-baseline-closure-report.md` | `AOS-FARM.453` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 78 | `reports/aos-farm-469-product-boundary-stabilization-remediation-plan.md` | `AOS-FARM.469` | `planning_or_package` | `PRESERVE_OPTIONAL` | `HIGH_FILENAME` | planning or package artifact from filename | `KEEP_LOCAL_PENDING_REVIEW` |
| 79 | `reports/aos-farm-469a-scope-tightening-addendum.md` | `AOS-FARM.469A` | `planning_or_package` | `PRESERVE_OPTIONAL` | `HIGH_HEADER` | scope-tightening addendum for later product-boundary task | `KEEP_LOCAL_PENDING_REVIEW` |
| 80 | `reports/aos-farm-570-push-execution-and-remote-closure-report.md` | `AOS-FARM.570` | `push_authorization_or_push_report` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | push or remote-closure artifact from filename | `COMMIT_AS_HISTORICAL_EVIDENCE_CANDIDATE` |
| 81 | `reports/aos-farm-full-read-only-deep-audit-report.md` | `NO_TASK_ID` | `audit_or_review` | `PRESERVE_OPTIONAL` | `HIGH_HEADER` | full read-only deep audit without obvious numbered task id | `REVIEW_BEFORE_PRESERVATION` |
| 82 | `reports/human-checkpoints/aos-farm-367-cleanup-commit-push-authorization.md` | `AOS-FARM.367` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 83 | `reports/human-checkpoints/aos-farm-389-final-aos-consumer-kit-push-authorization.md` | `AOS-FARM.389` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 84 | `reports/human-checkpoints/aos-farm-407-combined-push-authorization.md` | `AOS-FARM.407` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 85 | `reports/human-checkpoints/aos-farm-413-consumer-entry-flow-blocking-remediation-push-authorization.md` | `AOS-FARM.413` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 86 | `reports/human-checkpoints/aos-farm-415-consumer-runtime-handoff-remediation-authorization.md` | `AOS-FARM.415` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 87 | `reports/human-checkpoints/aos-farm-418-consumer-runtime-handoff-remediation-push-authorization.md` | `AOS-FARM.418` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 88 | `reports/human-checkpoints/aos-farm-430-evidence-tail-push-authorization.md` | `AOS-FARM.430` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 89 | `reports/human-checkpoints/aos-farm-433-first-controlled-task-execution-flow-push-authorization.md` | `AOS-FARM.433` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 90 | `reports/human-checkpoints/aos-farm-434-first-controlled-execution-bridge-mvp-push-authorization.md` | `AOS-FARM.434` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 91 | `reports/human-checkpoints/aos-farm-438-commit-authorization.md` | `AOS-FARM.438` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 92 | `reports/human-checkpoints/aos-farm-438-controlled-execution-authorization.md` | `AOS-FARM.438` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 93 | `reports/human-checkpoints/aos-farm-438-push-authorization.md` | `AOS-FARM.438` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 94 | `reports/human-checkpoints/aos-farm-439-p1-commit-authorization.md` | `AOS-FARM.439.P1` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 95 | `reports/human-checkpoints/aos-farm-439-p1-push-authorization.md` | `AOS-FARM.439.P1` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 96 | `reports/human-checkpoints/aos-farm-439-p2-commit-authorization.md` | `AOS-FARM.439.P2` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 97 | `reports/human-checkpoints/aos-farm-439-p2-push-authorization.md` | `AOS-FARM.439.P2` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 98 | `reports/human-checkpoints/aos-farm-440-push-authorization.md` | `AOS-FARM.440` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 99 | `reports/human-checkpoints/aos-farm-441-push-authorization.md` | `AOS-FARM.441` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 100 | `reports/human-checkpoints/aos-farm-442-push-authorization.md` | `AOS-FARM.442` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 101 | `reports/human-checkpoints/aos-farm-443-push-authorization.md` | `AOS-FARM.443` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 102 | `reports/human-checkpoints/aos-farm-444-push-authorization.md` | `AOS-FARM.444` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 103 | `reports/human-checkpoints/aos-farm-445-push-authorization-package.md` | `AOS-FARM.445` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 104 | `reports/human-checkpoints/aos-farm-446-push-authorization-package.md` | `AOS-FARM.446` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
| 105 | `reports/human-checkpoints/aos-farm-447-push-authorization-package.md` | `AOS-FARM.447` | `human_checkpoint` | `PRESERVE_HIGH_VALUE` | `HIGH_FILENAME` | human checkpoint path and authorization naming | `COMMIT_AS_HUMAN_CHECKPOINT_CANDIDATE` |
