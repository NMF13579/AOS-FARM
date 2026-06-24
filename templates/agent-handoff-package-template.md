# Agent Handoff Package

- **Handoff ID**: [ID]
- **Target Agent**: [Agent Name/Role]
- **Task ID**: [Task ID]
- **Authorized Target Task**: [Task Name]
- **Human Execution Authorization Reference**: [Path to checkpoint]
- **Risk Profile Assigned By Human**: [Risk Profile]
- **Repository**: [Repo]
- **Branch**: [Branch]

## Scope and Context
- **Context**: [Context]
- **Goal**: [Goal]
- **Scope**: [Exact scope]
- **Allowed Files**: [List]
- **Forbidden Files**: [List]

## Execution Instructions
- **Required Behavior**: [What the agent must do]
- **Non-Goals**: [What the agent must NOT do]
- **Validation**: [How the agent should self-verify]
- **Expected Final Report**: [Path/Format of the expected report]

## Stop Conditions
- **Stop Conditions**: [When the agent must stop immediately]

## Critical Boundaries
- Do not simulate Human approval.
- Do not expand scope.
- Do not commit.
- Do not push.
- Do not treat PASS as approval.
- Do not treat Evidence as approval.
- Do not treat UNKNOWN as OK.
- Do not treat NOT_RUN as PASS.
