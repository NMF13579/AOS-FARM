# AOS-FARM.439 — Controlled Execution Guard Integration Review / User Workflow Fit
## Status
task_id: AOS-FARM.439
task_title: Controlled Execution Guard Integration Review / User Workflow Fit
branch: build/controlled-execution-guard-mvp
repo_root: /Users/muhammed/Documents/GitHub/AOS-FARM
base_commit: 814c20433af68552b0bb3a884381fa7946c37ac3
origin_dev: 814c20433af68552b0bb3a884381fa7946c37ac3
ahead_behind: 0 0
risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by: human
review_type: read_only_integration_review
final_status: USER_WORKFLOW_FIT_BLOCKED

## Scope
reviewed_files:
  - README.md
  - aos/START_HERE.md
  - aos/AGENT_CONTEXT.md
  - aos/docs/controlled-execution-guard-mvp.md
  - aos/docs/user-guide/quickstart.md
  - aos/docs/user-guide/project-map.md
  - aos/docs/workflow/README.md
  - aos/docs/workflow/controlled-task-workflow.md
  - aos/docs/workflow/consumer-runtime-handoff.md
  - aos/docs/workflow/first-controlled-execution.md
  - aos/docs/workflow/first-session-guide.md
  - aos/docs/workflow/technical-assignment-to-task-brief.md
  - aos/docs/workflow/commit-push-workflow.md
  - aos/prompts/controlled-execution.md
  - aos/templates/README.md
  - aos/templates/task-briefs/README.md
  - aos/templates/task-briefs/controlled-task-brief-template.md
  - aos/templates/checkpoints/human-execution-authorization-template.md
  - aos/templates/reports/README.md
  - aos/templates/reports/execution-report-template.md
  - aos/templates/reports/evidence-review-template.md
  - aos/templates/authorization/README.md
  - aos/reports/examples/README.md
  - aos/scripts/aos_controlled_execution_guard.py
  - aos/tools/optional/controlled_execution_guard.py
  - reports/aos-farm-438-controlled-execution-guard-execution-report.md
  - reports/aos-farm-438-controlled-execution-guard-evidence-report.md
  - reports/aos-farm-438-r4-final-commit-readiness-recheck-report.md
  - tests/guards/test_controlled_execution_guard.py
excluded_files:
  - agentos/**
  - canonical development sources were not modified and were used only for control authority
  - pre-existing unrelated dirty state
forbidden_operations_observed:
  - none

## Baseline
remote_baseline_status: closed
head_sha: 814c20433af68552b0bb3a884381fa7946c37ac3
origin_dev_sha: 814c20433af68552b0bb3a884381fa7946c37ac3
remote_ref_sha: 814c20433af68552b0bb3a884381fa7946c37ac3
ahead_behind: 0 0

## Source Availability
00_AOS_Core_Control.md: present
01_AOS_Assembly_Pipelines_and_Build_Roadmap.md: present
02_AOS_Governance_Control_Module_and_Safety_Rules.md: present

## User Workflow Map
current_observed_path:
  - README.md points users directly to aos/START_HERE.md
  - aos/START_HERE.md routes to first-session guide, TA builder, task brief builder, then first-controlled-execution
  - first-controlled-execution explains Controlled Task Brief, Human Execution Authorization, Controlled Execution prompt, Evidence Review, and separate commit/push decisions
  - controlled-execution-guard-mvp.md exists as a standalone guard doc with commands
expected_path:
  - README
  - START_HERE
  - aos/START_HERE
  - Problem Intake
  - Technical Assignment
  - Controlled Task Brief
  - Human Execution Authorization
  - Controlled Execution Guard
  - Execution Report
  - Evidence Review
  - commit/push gates
missing_links:
  - no root START_HERE.md entrypoint exists, so the requested README -> START_HERE -> aos/START_HERE path is broken
  - first-controlled-execution does not explicitly insert Controlled Execution Guard precheck/scopecheck/postcheck as part of the safe runtime path
  - templates do not point users from Task Brief or Human Execution Authorization into the guard workflow
  - examples index does not point users to aos/reports/examples/controlled-execution-guard
ambiguous_links:
  - quickstart compresses the workflow to "Define the Task -> Authorize Execution -> Execute -> Verify", which hides Problem Intake -> TA -> Task Breakdown -> Controlled Task Brief sequencing
  - project map refers to aos/examples/ but discoverable examples actually live under aos/reports/examples/

## Controlled Execution Guard Placement
pre_execution_position: documented only in aos/docs/controlled-execution-guard-mvp.md, not clearly inserted into the main user workflow before execution starts
human_execution_authorization_position: clear in first-controlled-execution and controlled-task-workflow
precheck_position: not clearly placed in the main workflow docs after Human Execution Authorization and before agent execution
scopecheck_position: not clearly placed between execution and evidence review / scope verification in the main workflow docs
postcheck_position: documented in the guard doc, but not linked as a standard step before Evidence Review
evidence_review_position: clear in first-controlled-execution and evidence review template
commit_gate_position: clear and explicitly separate
push_gate_position: clear and explicitly separate

## Command Discoverability
precheck_command_found: yes, in aos/docs/controlled-execution-guard-mvp.md
scopecheck_command_found: yes, in aos/docs/controlled-execution-guard-mvp.md
postcheck_command_found: yes, in aos/docs/controlled-execution-guard-mvp.md
examples_found:
  - aos/reports/examples/controlled-execution-guard/fixtures/*
discoverability_assessment: Commands exist, but they are discoverable mainly from the standalone guard doc. The primary execution workflow docs, prompts, and templates do not route the user to those commands at the moment they should be used.

## Template / Prompt Linkage
controlled_task_brief_template: present, but does not tell the user to prepare or reference a guard package/check path
human_execution_authorization_template: present, but does not mention guard precheck usage after authorization
execution_package_template: missing as a dedicated user-facing template
execution_report_template: present, but does not include guard output fields or explicit pre/scope/post check references
evidence_report_template: missing as a dedicated template; only evidence-review-template exists
commit_authorization_template: present as package/checkpoint templates
push_authorization_template: present as package/checkpoint templates
gaps:
  - no dedicated Execution Package template
  - no dedicated Evidence Report template matching guard postcheck inputs
  - no template fields that connect Task Brief / Human Execution Authorization / Execution Report / Evidence Review to guard artifacts
  - prompts do not point back to the guard doc or examples

## Non-Programmer Usability
can_user_start_without_internal_knowledge: partially
can_user_identify_next_step: partially
can_user_understand_stop_conditions: partially
can_user_understand_PASS_boundary: yes
can_user_understand_BLOCKED_boundary: partially
assessment: A non-programmer can follow the high-level markdown flow, but still needs hidden expert knowledge to discover where the guard belongs, which commands to run, and what to do with HUMAN_REVIEW_REQUIRED / UNKNOWN_BLOCKED outcomes. The current quickstart and workflow chain are not yet self-sufficient for the new guard.

## Safety Semantics
PASS_not_approval: preserved in README, START_HERE, workflow docs, templates, and guard doc
Evidence_not_approval: preserved
CI_PASS_not_approval: preserved
UNKNOWN_not_OK: preserved
NOT_RUN_not_PASS: preserved
human_approval_not_simulated: preserved
commit_gate_separate: preserved
push_gate_separate: preserved
assessment: The core safety semantics are consistently preserved in user-facing docs. The main issue is integration and routing, not safety philosophy drift.

## Gaps
### GAP-439-001
severity: BLOCKING
surface: prompts
description: aos/prompts/controlled-execution.md tells the agent to verify 00_AOS_Core_Control.md, 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md, and 02_AOS_Governance_Control_Module_and_Safety_Rules.md before execution.
user_impact: In a real consumer project that only embeds the transferable aos/ bundle, those AOS-FARM development sources do not exist and must not be required. A non-programmer following the prompt literally will hit a false prerequisite or conclude they must copy internal development sources into the user project.
recommended_fix: Rewrite the controlled-execution prompt so consumer/runtime mode verifies the user-facing aos/ workflow artifacts and human authorization artifacts instead of requiring 00/01/02. Keep any AOS-FARM-only source checks explicitly confined to development-repo workflows.
requires_protected_or_canonical_change: false
requires_human_checkpoint: false
suggested_next_task: AOS-FARM.439.P1

### GAP-439-002
severity: HIGH
surface: aos docs
description: first-controlled-execution.md and controlled-task-workflow.md do not explicitly place guard precheck, scopecheck, and postcheck between Human Execution Authorization, execution, Evidence Review, and commit/push gates.
user_impact: The guard exists, but users are not clearly told when to run it. This leaves the integration dependent on hidden expert knowledge and makes the new MVP feel optional in practice instead of intentionally positioned.
recommended_fix: Insert an explicit Controlled Execution Guard step into the first-controlled-execution and controlled-task workflow docs, including when to run precheck, when scopecheck is expected, and when postcheck should happen relative to Evidence Review.
requires_protected_or_canonical_change: false
requires_human_checkpoint: false
suggested_next_task: AOS-FARM.439.P1

### GAP-439-003
severity: HIGH
surface: README
description: The requested entry chain README -> START_HERE -> aos/START_HERE is not intact because there is no root START_HERE.md, and quickstart/user-guide docs compress the workflow in ways that bypass Problem Intake -> Technical Assignment -> Task Breakdown -> Controlled Task Brief sequencing.
user_impact: A new user can start, but the first-hop routing is inconsistent. Some docs correctly teach the full methodology chain while quickstart-style docs imply a simplified "create a task brief and execute" path.
recommended_fix: Normalize the entry chain and align quickstart/project-map copy with the actual methodology-first path so users are routed through Intake -> TA -> Task Breakdown before Controlled Execution.
requires_protected_or_canonical_change: false
requires_human_checkpoint: false
suggested_next_task: AOS-FARM.439.P1

### GAP-439-004
severity: MEDIUM
surface: templates
description: The current templates do not provide a dedicated Execution Package template or a dedicated Evidence Report template aligned to the guard inputs, and existing execution/evidence templates do not reference guard artifacts.
user_impact: A user can proceed, but artifact creation is inconsistent. Non-programmers may not know what package/report structure the guard expects without reverse-engineering fixtures or implementation tests.
recommended_fix: Add or update templates so Controlled Task Brief, Human Execution Authorization, Execution Report, and Evidence Review include explicit guard-related fields and example paths.
requires_protected_or_canonical_change: false
requires_human_checkpoint: false
suggested_next_task: AOS-FARM.439.P2

### GAP-439-005
severity: MEDIUM
surface: examples
description: aos/reports/examples/README.md is not an example index and does not explain the controlled execution guard fixtures. Workflow docs also do not link to these examples.
user_impact: The example assets exist but are not discoverable to a non-programmer. Users are unlikely to find valid_package.yaml / valid_report.md without manual searching.
recommended_fix: Replace the generic examples README with a real example index and link it from the guard doc and first-controlled-execution workflow.
requires_protected_or_canonical_change: false
requires_human_checkpoint: false
suggested_next_task: AOS-FARM.439.P2

### GAP-439-006
severity: MEDIUM
surface: prompts
description: The controlled execution prompt explains BLOCKED behavior but does not teach the user what to do when the guard returns HUMAN_REVIEW_REQUIRED or UNKNOWN_BLOCKED.
user_impact: Non-programmers can see the status, but may not know whether to revise the brief, add human authorization, or stop and request a narrower task.
recommended_fix: Add a short response-handling table for PASS, BLOCKED, HUMAN_REVIEW_REQUIRED, UNKNOWN_BLOCKED, and NOT_RUN in the prompt or first-controlled-execution guide.
requires_protected_or_canonical_change: false
requires_human_checkpoint: false
suggested_next_task: AOS-FARM.439.P2

## Recommended Next Task
recommended_task_id: AOS-FARM.439.P1
recommended_task_title: Controlled Execution Guard User Workflow Integration Hardening
recommended_task_type: docs-prompts-templates integration fix
risk_profile_recommendation: HIGH_RISK_PROTECTED
scope:
  - user-facing workflow docs under aos/docs/workflow and aos/docs/user-guide
  - aos/prompts/controlled-execution.md
  - relevant aos/templates for task brief, human execution authorization, execution report, evidence review, and optional new execution package/evidence report templates
  - example index linkage under aos/reports/examples
non_goals:
  - no runtime code changes to the guard itself
  - no canonical development source changes
  - no commit/push automation changes
  - no agentos activation

## Commands Run
- git fetch origin
- pwd
- git rev-parse --show-toplevel
- git branch --show-current
- git status -sb
- git status --short
- git rev-parse HEAD
- git rev-parse origin/dev
- git rev-list --left-right --count origin/dev...HEAD
- git ls-remote origin refs/heads/dev
- ls -la README.md START_HERE.md aos/START_HERE.md aos/AGENT_CONTEXT.md 2>/dev/null || true
- find aos/docs -maxdepth 4 -type f | sort
- find aos/templates -maxdepth 5 -type f | sort
- find aos/prompts -maxdepth 5 -type f | sort
- find aos/scripts aos/tools -maxdepth 5 -type f | sort
- grep discovery for controlled execution / authorization / evidence terms across reviewed surfaces
- targeted reads of README, aos/START_HERE.md, aos/AGENT_CONTEXT.md, workflow docs, controlled-execution prompt, guard doc, and key templates

## NOT_RUN
- none

## UNKNOWN
- none

## BLOCKED
- GAP-439-001

## Final Decision
final_status: USER_WORKFLOW_FIT_BLOCKED
commit_performed: false
push_performed: false
merge_performed: false
release_performed: false
next_task_started: false
approval_claimed: false
human_review_required: true
