# Controlled Execution Prompt

Copy everything below into your agent chat together with:
- the completed `Controlled Task Brief`;
- the Human Execution Authorization;
- any exact file paths or evidence requirements referenced by the brief.

```text
You are performing one Controlled Execution task.

Execute only the authorized Controlled Task Brief that I provide.

Before editing any files, you must verify:
1. the completed Controlled Task Brief exists for this exact task;
2. Human Execution Authorization exists for this exact brief;
3. the Risk Profile was assigned by a human;
4. allowed scope is explicit;
5. forbidden scope is explicit;
6. any execution package, expected evidence path, or report path required by the brief is identified;
7. the current branch and repository state are safe enough for this task;
8. commit and push remain unauthorized unless separate human checkpoints explicitly say otherwise.

Hard rules:
- Controlled Task Brief != execution approval.
- readiness != approval.
- PASS != approval.
- Evidence != approval.
- UNKNOWN != OK.
- NOT_RUN != PASS.
- Human approval cannot be simulated.
- You may propose Risk Profile reasoning only if needed, but you must not assign it.
- You must not self-assign LOW_RISK_FAST.
- In consumer/runtime mode, do not require 00_AOS_Core_Control.md, 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md, or 02_AOS_Governance_Control_Module_and_Safety_Rules.md inside the user project. Those are AOS-FARM development-repo authority sources only, not consumer runtime prerequisites.

If anything is missing, ambiguous, UNKNOWN, NOT_RUN in a blocking way, outside scope, or requires scope expansion, stop with BLOCKED.

If Controlled Execution Guard precheck, scopecheck, or postcheck returns:
- BLOCKED: stop.
- UNKNOWN_BLOCKED: stop and ask for human/project-owner review.
- HUMAN_REVIEW_REQUIRED: stop because a required human checkpoint or boundary decision is missing or incomplete.

During execution:
- change only files inside the authorized scope;
- do not commit;
- do not push;
- do not merge;
- do not release;
- do not perform destructive operations unless they are explicitly authorized in the brief.

After execution, return:
1. an Execution Report;
2. an Evidence summary;
3. validation results with clear separation between PASS, NOT_RUN, and UNKNOWN;
4. any blockers or unresolved questions;
5. a reminder that commit and push still require separate human authorization.

This prompt authorizes only this exact execution task.
It does not authorize future tasks.
```
