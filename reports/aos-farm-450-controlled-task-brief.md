# AOS-FARM.450 Controlled Task Brief

* objective: Add or stabilize deterministic parseable JSON output for Task Queue Helper subcommands.
* branch policy: Execute on build/first-controlled-code-change-dogfood. No direct pushes to dev.
* scope: Add or stabilize deterministic parseable JSON output for validate, show-current, show-next, summary.
* out-of-scope: Modifying protected/canonical files, executing AOS-FARM.451, performing code changes in PREP.
* allowed files for future EXEC phase: 
  - aos/scripts/aos_task_queue_helper.py
  - tests/test_aos_task_queue_helper.py
  - tests/fixtures/task_queue_*.yaml
  - reports/aos-farm-450-*.md
  - reports/aos-farm-450-changed-files.yaml

* conditionally allowed if needed:
  - aos/tools/optional/task_registry_validator.py

  Prefer not to modify aos/tools/optional/task_registry_validator.py unless the helper delegates JSON behavior or validation boundary there.

* forbidden files:
  - 00_AOS_Core_Control.md
  - 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
  - 02_AOS_Governance_Control_Module_and_Safety_Rules.md
  - README.md
  - START_HERE*
  - /aos/root/AGENTS.md

* safety invariants: PASS != approval, Evidence != approval, CI PASS != approval, UNKNOWN != OK, NOT_RUN != PASS, Human approval cannot be simulated, Agent cannot self-assign Risk Profile.
* expected implementation target for future EXEC phase: Add or stabilize deterministic parseable JSON output for:
  - validate
  - show-current
  - show-next
  - summary

* expected tests for future EXEC phase: Update or add tests verifying the JSON output for all subcommands.
* explicit stop before execution: STOP -> HUMAN_REVIEW_REQUIRED before moving to EXEC phase.

This PREP-FIX does not authorize execution.
AOS-FARM.450.EXEC still requires explicit human authorization.
Commit is not authorized.
Push is not authorized.
Release is not authorized.
AOS-FARM.451 is not authorized.
