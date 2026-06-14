# Documentation Assembly Pipeline MVP

## 1. Overview
The Documentation Assembly Pipeline is the first layer of the Assembly Core. It is responsible for translating raw ideas and requirements into actionable, scoped, and strictly bounded documents ready for the Code Assembly Pipeline.

## 2. Artifact Flow
The MVP pipeline strictly enforces the following linear progression of artifacts:
1. **Idea / Input**: Raw concept or request.
2. **Project Brief**: High-level problem, goal, and constraints.
3. **Specification**: Expected behavior and architecture rules.
4. **Task Brief**: Actionable scope, boundaries, and validation requirements.
5. **Execution Package**: Bundled context for the agent.
6. **Execution Report**: Agent's claim of execution results.
7. **Evidence Report**: Hard proof artifacts.
8. **Human Review Package**: Final bundle for human decision.

## 3. Core Constraints
- **Scope Expansion**: The pipeline must NOT expand the scope beyond what the human explicitly defined.
- **Approvals**: The pipeline does NOT approve. It only structures data. `PASS ≠ approval`.
- **Handling UNKNOWN**: If at any stage information is missing or unclear, the process stops with `UNKNOWN_BLOCKED`.
- **Handling Non-Approval**: If human approval is missing, the process stops with `HUMAN_REVIEW_REQUIRED`.

## 4. Traceability
Each artifact must include source traceability fields (e.g., `prepared_by_task`, `created_for_task`) to maintain an unbroken chain of evidence.
