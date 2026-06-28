# Lessons Learned: AOS-FARM.448

## Controlled Execution Dogfood Insights
- The transition from Task Queue to Controlled Execution requires strict tracking of YAML schema versions for both the Execution Package and the Evidence Report.
- Human Authorization must explicitly provide `HIGH_RISK_PROTECTED` via the human placeholder, rather than the agent generating it directly.
- `scopecheck` correctly identifies the exact bounded files and prevents creation/modification of anything outside the authorized `changed-files` list.
- `postcheck` strongly relies on a rigid YAML evidence structure embedded within the Evidence Report, ensuring that execution boundaries like `commit_performed` are explicitly stated as `false`.

*Note: Lessons Learned ≠ approval.*
