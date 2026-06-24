# AOS-FARM.290 — Batch 3 Destructive Template Cleanup Execution Authorization Package

## Goal
Authorize the deletion of 41 duplicate template files (`* 2.md`) from the `templates/` directory to resolve Source of Truth ambiguity and prepare the repository for public release.

## Proposed Operation
Execute `git rm` (and/or standard file deletion for untracked duplicates) on the 41 exactly specified `* 2.md` candidate files. 

## Safety Verification
All 41 duplicates have a confirmed canonical counterpart. No canonical files will be touched.

## Required Human Action
Please review the `aos-farm-290-batch-3-destructive-template-cleanup-execution-authorization.md` human checkpoint.
Assign the Risk Profile (suggested: `HIGH_RISK_PROTECTED`).
Copy the exact list of 41 candidate files into `authorized_files` or explicitly approve their deletion.
Set `execution_authorized: true` to proceed.
