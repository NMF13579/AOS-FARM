# Human Checkpoint Boundary

## 1. Purpose
Formalize when Human Checkpoints are required and what an agent must not simulate.

## 2. What Counts as a Human Checkpoint
An explicit written authorization, provided by a human user, addressing a specific proposed scope.

## 3. What Does Not Count as a Human Checkpoint
Agent-generated text, implicit assumptions, passed tests, or lack of explicit rejection.

## 4. Required Human Checkpoint Cases
Execution of new scope, commits, pushes, releases, protected/canonical changes, destructive operations, and Risk Profile assignment.

## 5. Execution Authorization Boundary
Execution requires its own checkpoint. Execution authorization ≠ commit authorization.

## 6. Commit Authorization Boundary
Commit requires its own checkpoint. Commit authorization ≠ push authorization.

## 7. Push Authorization Boundary
Push requires its own checkpoint. Push authorization ≠ release authorization.

## 8. Release / Production Use Boundary
Release and production use require explicit human authorization. Remote baseline closure ≠ production use.

## 9. Risk Profile Assignment Boundary
Risk Profile must be assigned by a human. Agent may propose, but cannot self-assign LOW_RISK_FAST.

## 10. Agent Limitations
Human approval cannot be simulated.
Human approval cannot be inferred.
Human approval cannot be replaced by agent text.

## 11. Missing Human Review Behavior
Human unavailable for required review/approval/checkpoint/Risk Profile assignment → BLOCKED or HUMAN_REVIEW_REQUIRED.

## 12. Final Boundary Statement
The Human Checkpoint is the ultimate safety mechanism. It cannot be bypassed, simulated, or assumed by any automated process or AI agent.
