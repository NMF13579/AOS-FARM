# Code Execution Package Template

## Overview
```yaml
task_id: [TASK_ID]
source_task_brief: [PATH_TO_BRIEF]
```

## Scope
```yaml
authorized_scope: [DESCRIPTION]
allowed_files: []
forbidden_files: []
allowed_actions: []
forbidden_actions: []
```

## Requirements
```yaml
required_preflight: []
required_validation: []
expected_evidence: []
```

## Boundaries & Status
```yaml
approval_boundaries: [BOUNDARIES]
final_status_values: []
```

## Invariants Reminder
- PASS ≠ approval.
- Evidence ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
