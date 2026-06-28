# AOS-FARM.445 Execution Authorization

## Scope
AOS-FARM.445.A — Canonical Clarification Patch

## Decision
APPROVED_FOR_EXECUTION

## Human-assigned Risk Profile
HIGH_RISK_PROTECTED

## Approved Protected/Canonical Changes
Clarification-only changes permitted for:
* 00_AOS_Core_Control.md
* 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
* 02_AOS_Governance_Control_Module_and_Safety_Rules.md

## Approved Clarification Formula
* Product folder AOS = `/aos/`
* `/aos/root/AGENTS.md` = template for target project root `AGENTS.md`
* Root 00/01/02 = AOS-FARM development canonical sources, not consumer runtime prerequisites
* `agentos/` = internal/reference layer, not consumer first-start path
* AgentOS remains reference only and must not be imported into AOS-FARM

## Constraints Acknowledged
* No destructive cleanup.
* No release.
* No commit.
* No push.
* No merge.
* All safety invariants remain enforced.
