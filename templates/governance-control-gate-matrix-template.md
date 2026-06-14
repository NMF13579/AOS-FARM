# Governance Control Gate Matrix Template

| gate_id | gate_name | gate_purpose | required_inputs | required_evidence | PASS_condition | PASS_WITH_WARNINGS_condition | BLOCKED_condition | UNKNOWN_condition | NOT_RUN_condition | Risk_Profile_relation | human_checkpoint_required | approval_required | forbidden_bypass | failure_status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G01 | source availability gate | | | | | | | | | | | | | | |
| G02 | source precedence gate | | | | | | | | | | | | | | |
| G03 | scope boundary gate | | | | | | | | | | | | | | |
| G04 | risk profile gate | | | | | | | | | | | | | | |
| G05 | human checkpoint gate | | | | | | | | | | | | | | |
| G06 | approval boundary gate | | | | | | | | | | | | | | |
| G07 | evidence boundary gate | | | | | | | | | | | | | | |
| G08 | PASS semantics gate | | | | | | | | | | | | | | |
| G09 | UNKNOWN / NOT_RUN gate | | | | | | | | | | | | | | |
| G10 | protected/canonical change gate | | | | | | | | | | | | | | |
| G11 | destructive operation gate | | | | | | | | | | | | | | |
| G12 | lifecycle mutation gate | | | | | | | | | | | | | | |
| G13 | runtime implementation gate | | | | | | | | | | | | | | |
| G14 | validator implementation gate | | | | | | | | | | | | | | |
| G15 | CI workflow gate | | | | | | | | | | | | | | |
| G16 | commit gate | | | | | | | | | | | | | | |
| G17 | push gate | | | | | | | | | | | | | | |
| G18 | release gate | | | | | | | | | | | | | | |
| G19 | production use gate | | | | | | | | | | | | | | |
| G20 | controller loop stop gate | | | | | | | | | | | | | | |

## Critical Boundary Invariants
- PASS ≠ approval
- Evidence ≠ approval
- CI PASS ≠ approval
- UNKNOWN ≠ OK
- NOT_RUN ≠ PASS
- Human approval cannot be simulated
