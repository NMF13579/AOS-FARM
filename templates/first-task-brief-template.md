# First Task Brief Template

## Task Identity
- **Task ID / Name**: [e.g., AOS-FARM-NEW-01 — Problem Intake Draft]
- **Mode**: Documentation-only Implementation
- **Repository**: [Repository Name]
- **Branch**: `build/initial-problem-intake`

## Context
We are starting a new project. We need to define the exact problem and scope before writing any code.

## Goal
Draft the initial Problem Intake and Project Specification documents based on the user's checklist.

## Boundaries
- **Scope**: Documentation generation only.
- **Allowed Files**: `docs/features/*`, `docs/project-status/*`
- **Forbidden Files**: `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`, any `.py`, `.js`, or executable files.

## Rules
- **Required Behavior**: Write the specification, generate a self-verification report, prepare a commit authorization package, and STOP.
- **Non-Goals**: Do not write code. Do not run scanners. Do not commit or push.
- **Validation**: Verify that no forbidden files were touched and no code was generated.

## Deliverables
- **Expected Final Report**: A detailed implementation report proving the scope was respected.

## Safety
- **Stop Rule**: Stop immediately after generating the implementation report and wait for Human Commit Authorization.
