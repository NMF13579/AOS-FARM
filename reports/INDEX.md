---
derived_navigation_artifact: true
manual_snapshot: true
source_of_truth: false
approval_authority: false
lifecycle_authority: false
evidence_authority: false
complete_history_claim: false
snapshot_date: "2026-07-02"
maintained_by: human (manual update)
---

# reports/INDEX.md — Manual Navigation Snapshot

> **IMPORTANT BOUNDARY:**
> `reports/INDEX.md` is a **manual derived navigation snapshot**.
> It is **not** a registry.
> It is **not** complete unless explicitly stated and verified.
> It must **not** be used as Source of Truth for approval, lifecycle,
> Evidence, or closure.
> Canonical governance remains in `00_AOS_Core_Control.md`, `01`, and `02`.
> This document is guidance and navigation only.

---

## Purpose

This index provides a manually maintained snapshot of known report files in the
`reports/` directory. It helps users and agents quickly locate relevant reports
without scanning the full directory.

It is a navigation aid only. It does not reflect the complete history of all
reports. It does not confirm Evidence, approval, or lifecycle status of any
report listed.

---

## How to Use This Index

1. Use this index to find a report by category or stage number.
2. Open the report file directly to read its content and status.
3. Do not treat a report's presence in this index as confirmation of any
   approval, Evidence acceptance, or lifecycle transition.
4. If a report is missing from this index, it may still exist in `reports/`.
   Run `find reports -type f -name "*.md" | sort` to see all files.

---

## How to Regenerate / Update This Index

This index is **manually maintained**. To update it:

1. Run: `find reports -maxdepth 2 -type f -name "*.md" | sort`
2. Categorize new files into the appropriate section below.
3. Update `snapshot_date` in the front matter.
4. Mark `complete_history_claim: false` unless you have explicitly verified
   every report in the directory.

Do not rewrite old reports. Do not change old reports' meaning. Do not use
automated tooling to overwrite this index without human review.

---

## Limitations

```text
- This index is a point-in-time snapshot only.
- Many untracked reports exist that are not yet committed to the repository.
- The presence of a report here does not mean it was approved or accepted.
- The absence of a report here does not mean it does not exist.
- Evidence and approval records in reports must be verified in the report files
  themselves, not from this index.
```

---

## Latest Known Closure Reports

These reports record post-push remote baseline verification after authorized
push operations.

| File | Stage / Task | Notes |
|---|---|---|
| `reports/ta-35-dev-push-and-remote-baseline-closure.md` | TA-34/35 | Dev integration push closure |
| `reports/ta-32-evidence-tail-push-and-working-branch-closure.md` | TA-31/32 | Evidence tail push closure |
| `reports/ta-28-technical-assignment-pipeline-v2-working-branch-push-closure.md` | TA-27/28 | Pipeline v2 push closure |
| `reports/aos-farm-570-push-execution-and-remote-closure-report.md` | AOS-FARM.570 | Most recent push closure (untracked) |

---

## Human Checkpoint Reports

These reports record explicit human authorization decisions.

### Tracked (committed)

| File | Decision Type |
|---|---|
| `reports/human-checkpoints/aos-farm-commit-authorization.md` | Commit |
| `reports/human-checkpoints/aos-farm-push-authorization.md` | Push |
| `reports/human-checkpoints/aos-farm-dev-to-main-merge-approval.md` | Merge |
| `reports/human-checkpoints/aos-farm-first-controlled-implementation-authorization.md` | Execution |
| `reports/human-checkpoints/aos-farm-implementation-readiness-authorization.md` | Execution readiness |
| `reports/human-checkpoints/aos-farm-documentation-assembly-mvp-execution-authorization.md` | Execution |
| `reports/human-checkpoints/ta-21-technical-assignment-execution-authorization.md` | Execution |
| `reports/human-checkpoints/ta-34-dev-integration-push-authorization.md` | Push |

### Untracked (known, not yet committed)

A large number of human checkpoint files exist in `reports/human-checkpoints/`
that are untracked. Notable recent ones include:

```text
reports/human-checkpoints/aos-farm-438-commit-authorization.md
reports/human-checkpoints/aos-farm-438-push-authorization.md
reports/human-checkpoints/aos-farm-440-push-authorization.md
reports/human-checkpoints/aos-farm-441-push-authorization.md
reports/human-checkpoints/aos-farm-442-push-authorization.md
reports/human-checkpoints/aos-farm-443-push-authorization.md
reports/human-checkpoints/aos-farm-444-push-authorization.md
reports/human-checkpoints/aos-farm-445-push-authorization-package.md
reports/human-checkpoints/aos-farm-446-push-authorization-package.md
reports/human-checkpoints/aos-farm-447-push-authorization-package.md
```

Run `git status --short --untracked-files=all | grep human-checkpoints` to see
the current full list.

---

## Execution Reports

These reports record what an agent did during an authorized execution.

| File | Stage / Task | Notes |
|---|---|---|
| `reports/aos-farm-128-multi-environment-ide-controller-token-routing-implementation-report.md` | AOS-FARM.128 | Multi-env controller |
| `reports/aos-farm-135-build-step-6-dogfood-evidence-report.md` | Build Step 6 | First dogfood Evidence |
| `reports/aos-farm-429-ta-to-task-brief-assembly-layer-evidence-tail-commit-execution-report.md` | AOS-FARM.429 | TA-to-brief assembly |
| `reports/aos-farm-438-c-commit-authorization-package-report.md` | AOS-FARM.438 | Commit package |
| `reports/aos-farm-445-commit-execution-report.md` | AOS-FARM.445 | Commit execution |
| `reports/aos-farm-446-commit-execution-report.md` | AOS-FARM.446 | Commit execution |
| `reports/aos-farm-447-commit-execution-report.md` | AOS-FARM.447 | Commit execution |
| `reports/aos-farm-571-user-agent-tutor-feature-hardening-execution-report.md` | AOS-FARM.571 | Current stage (untracked) |

---

## Evidence Reports

Evidence reports are collected during task execution to support human review.
They are records only — not approval.

| File | Stage / Task |
|---|---|
| `reports/aos-farm-135-build-step-6-dogfood-evidence-report.md` | Build Step 6 |
| `reports/ta-25-technical-assignment-fixture-dogfood-final-audit.md` | TA-25 |
| `reports/aos-farm-432-ta-to-task-brief-assembly-post-stage-audit.md` | AOS-FARM.432 |
| `reports/aos-farm-439-controlled-execution-guard-integration-review.md` | AOS-FARM.439 |

---

## Audit / Review Reports

| File | Type |
|---|---|
| `reports/aos-farm-122-deep-step-5-audit.md` | Deep audit |
| `reports/aos-farm-354-deep-comprehensive-current-state-audit.md` | Full state audit (untracked) |
| `reports/aos-farm-361-spec-kit-and-recurring-warnings-inventory-audit.md` | Spec kit audit (untracked) |
| `reports/aos-farm-full-read-only-deep-audit-report.md` | Read-only deep audit (untracked) |

---

## Current Stage Reports

| File | Type | Status |
|---|---|---|
| `reports/aos-farm-571-user-agent-tutor-feature-hardening-execution-report.md` | Execution report | Untracked, created this stage |
| `reports/aos-farm-571-user-agent-tutor-feature-hardening-final-review-package.md` | Final review package | Untracked, created this stage |

---

## Unknown or Uncategorized Reports

A number of reports exist in `reports/` that have not been fully categorized
in this snapshot. These include push authorization packages, commit packages,
and remote baseline closure reports numbered 438–570. Run:

```bash
find reports -maxdepth 1 -type f -name "*.md" | sort
find reports -maxdepth 1 -name "*.md" | wc -l
```

to see the complete current count and list.

---

*This index is a manual derived navigation snapshot. It is not Source of Truth
for approval, lifecycle, Evidence, or closure. Canonical governance in 00/01/02
always takes precedence.*
