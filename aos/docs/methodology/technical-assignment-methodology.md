# Technical Assignment Methodology

The Technical Assignment (TA) is the critical boundary between abstract business requirements (Problem Intake) and concrete execution.

## 1. The Bridge from Intake
The TA Builder takes the structured data from the Problem Intake Summary and translates it into strict technical boundaries.
- **Grey-Zone Discovery**: Identifying implicit assumptions in the intake and explicitly addressing them before execution.
- **Contradiction Capture**: Resolving conflicting requirements.

## 2. Bounding Scope
A core principle of AOS is that scope must not expand without explicit human permission. The TA enforces this by defining:
- **In-Scope**: The explicit boundaries of what will be built.
- **Non-Goals (Out-of-Scope)**: What explicitly will *not* be built. This is the primary defense against scope creep.

## 3. Acceptance Criteria and Evidence
- **Success Criteria**: Concrete, testable states that define when the work is complete.
- **Validation**: Defining how the task will be proven safe.
- **Evidence ≠ Approval**: The TA methodology enforces that even if evidence passes and CI passes, only explicit human authorization can approve a commit or destructive action.

## 4. TA Routing and Readiness
- The TA must list all required files and target artifacts.
- **Readiness vs. Approval**: A "READY" TA simply means it is structurally sound enough to generate a Task Brief. It does NOT authorize execution.
- **Handoff**: The finalized TA acts as the direct input for creating a `Controlled Task Brief`.
