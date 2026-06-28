# AOS-FARM.450 Helper Preflight Report

* branch used for preflight: build/first-controlled-code-change-dogfood
* helper help output summary: Script accepts --registry and --queue arguments and subcommands validate, summary, show-current, show-next
* available subcommands: validate, summary, show-current, show-next
* actual registry/queue discovery result: Real project-wide queue and registry files were not found directly
* whether real files were available: NO
* whether fixtures were used: YES
* commands run:
  - python3 aos/scripts/aos_task_queue_helper.py validate --registry <file> --queue <file>
  - python3 aos/scripts/aos_task_queue_helper.py show-current --registry <file> --queue <file>
  - python3 aos/scripts/aos_task_queue_helper.py show-next --registry <file> --queue <file>
  - python3 aos/scripts/aos_task_queue_helper.py summary --registry <file> --queue <file>
* outputs summary: Successfully executed and returned JSON output for all subcommands
* warnings: show-summary subcommand was invalid, actual command is summary.
* NOT_AVAILABLE != PASS
* NOT_RUN != PASS
