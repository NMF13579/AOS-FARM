# AOS-FARM Dev to Main Merge Report

```yaml
task_id: AOS-FARM.8
task_name: Execute Authorized Dev-to-Main Documentation Merge
repository: NMF13579/AOS-FARM
source_branch: dev
target_branch: main
mode: authorized_documentation_merge_execution

merge_authorization:
  approval_artifact: reports/human-checkpoints/aos-farm-dev-to-main-merge-approval.md
  docs_activation_approval_artifact: reports/human-checkpoints/aos-farm-docs-activation-approval.md
  reviewed_source_head_sha: 63be83360cdaeb29bcfd6dd2336a18bb188fddf9
  authorization_commit_sha: a1dcb6a23eef9d22f1d18ee8f936d0a0e189e8ad
  actual_origin_dev_sha_before_merge: a1dcb6a23eef9d22f1d18ee8f936d0a0e189e8ad
  actual_origin_main_sha_before_merge: 66171599af06bdb985fd40c915f5cd7e163eba9e
  merge_base_sha_before_merge: 12988f1e48b4a0e22643e53d9e1b47dc06073953

self_inclusion_delta:
  allowed: true
  allowed_files:
    - reports/aos-farm-dev-main-divergence-review.md
    - reports/human-checkpoints/aos-farm-dev-to-main-merge-approval.md
    - reports/aos-farm-setup-report.md

merge_execution:
  merge_performed: true
  merge_method: no_ff_merge
  merge_commit_sha: 2baa94baa8829de09a7cf89b88be11933091acdd
  pushed_to_origin_main: true
  origin_main_sha_after_push: d8d61e48206c2f676977ae7edf51049acf6f1ac2

boundaries:
  implementation_authorized: false
  speckit_implement_authorized: false
  release_authorized: false
  production_use_authorized: false
  workflow_created: false
  ci_activated: false
  branch_protection_changed: false

final_status: AOS_FARM_8_MERGE_PUSHED_TO_MAIN
```
