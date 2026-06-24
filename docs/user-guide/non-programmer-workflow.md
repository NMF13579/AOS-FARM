# Non-Programmer Workflow

Building software with AOS-FARM is designed to be simple and safe for non-programmers. The process relies on explicit steps where the AI does the heavy lifting, but you control the flow.

## The Journey of a Feature

1. **Idea / Problem**: You start with a goal or a problem you want to solve.
2. **Problem Intake & Spec**: You and the agent use templates to define a clear `PROJECT_SPEC` and `REQUIREMENTS`.
3. **Engineering Clarification**: The agent asks clarifying questions until a concrete Implementation Contract is agreed upon.
4. **Task Brief**: The agent proposes a plan (a Task Brief).
5. **Code Assembly Boundary**: This is where planning stops and coding begins.
6. **Controlled Implementation Slice**: The agent writes the code in a restricted scope (a "slice").
7. **Verification**: The agent verifies its own work and creates a report.
8. **Human Approval**: You review the report and explicitly approve the execution, commit, or push.
9. **Documentation & Registry Update**: The agent updates `docs/features/` and `docs/project-status/` to reflect the new capabilities.

## Understanding the Terminology

To stay safe, you must understand four critical rules about what the AI tells you:

- **PASS ≠ Approval**: If an agent says a test "passed", it just means the code ran without errors. It **does not** mean you have approved the change to be permanently saved.
- **Evidence ≠ Approval**: If an agent provides a detailed report (evidence), it proves what it did, but it **does not** grant itself permission to move forward.
- **UNKNOWN ≠ OK**: If the agent doesn't know the status of a file or feature, it must stay "UNKNOWN". It cannot guess or assume it is "OK".
- **NOT_RUN ≠ PASS**: If a check was skipped or not run, the agent cannot pretend it passed.
