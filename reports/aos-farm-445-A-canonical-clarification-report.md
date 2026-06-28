# AOS-FARM.445.A Canonical Clarification Report

## Task Context
AOS-FARM.445.A — Canonical Clarification Patch
Authorized Risk Profile: HIGH_RISK_PROTECTED

## Objective
Apply clarification-only changes to the core canonical sources to explicitly define product folder boundaries.

## Changes Applied

A new section `## Product Folder Boundaries` was added to each of the three canonical sources, containing the exact required clarification formula.

### Affected Files
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

### Exact Formula Injected
```text
Product folder AOS = /aos/
/aos/root/AGENTS.md = template for target project root AGENTS.md
Root 00/01/02 = AOS-FARM development canonical sources, not consumer runtime prerequisites.
agentos/ = internal/reference layer, not consumer first-start path.
AgentOS = remains reference only and must not be imported into AOS-FARM.
```

## Evidence (Git Diff)

```diff
diff --git a/00_AOS_Core_Control.md b/00_AOS_Core_Control.md
index 3ca7ff6..3dca433 100644
--- a/00_AOS_Core_Control.md
+++ b/00_AOS_Core_Control.md
@@ -375,6 +375,18 @@ generic RAG database
 multi-agent framework first
 ```
 
+## Product Folder Boundaries
+
+Следующие границы структуры проекта строго определены:
+
+```text
+Product folder AOS = /aos/
+/aos/root/AGENTS.md = template for target project root AGENTS.md
+Root 00/01/02 = AOS-FARM development canonical sources, not consumer runtime prerequisites.
+agentos/ = internal/reference layer, not consumer first-start path.
+AgentOS = remains reference only and must not be imported into AOS-FARM.
+```
+
 ## Layer Model
 
 ```text
diff --git a/01_AOS_Assembly_Pipelines_and_Build_Roadmap.md b/01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
index e2b9deb..990772f 100644
--- a/01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
+++ b/01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
@@ -42,6 +42,18 @@ Minimal Safety Floor действует с первого дня.
 Governance / Control Module усиливает контроль отдельно.
 ```
 
+## Product Folder Boundaries
+
+Следующие границы структуры проекта строго определены:
+
+```text
+Product folder AOS = /aos/
+/aos/root/AGENTS.md = template for target project root AGENTS.md
+Root 00/01/02 = AOS-FARM development canonical sources, not consumer runtime prerequisites.
+agentos/ = internal/reference layer, not consumer first-start path.
+AgentOS = remains reference only and must not be imported into AOS-FARM.
+```
+
 ## Assembly Core
 
 Assembly Core состоит из двух pipeline:
diff --git a/02_AOS_Governance_Control_Module_and_Safety_Rules.md b/02_AOS_Governance_Control_Module_and_Safety_Rules.md
index c19aa37..ad25dc2 100644
--- a/02_AOS_Governance_Control_Module_and_Safety_Rules.md
+++ b/02_AOS_Governance_Control_Module_and_Safety_Rules.md
@@ -46,6 +46,18 @@ Governance / Control Module adds progressive governance.
 Runtime Enforcement physically blocks forbidden actions later.
 ```
 
+## Product Folder Boundaries
+
+Следующие границы структуры проекта строго определены:
+
+```text
+Product folder AOS = /aos/
+/aos/root/AGENTS.md = template for target project root AGENTS.md
+Root 00/01/02 = AOS-FARM development canonical sources, not consumer runtime prerequisites.
+agentos/ = internal/reference layer, not consumer first-start path.
+AgentOS = remains reference only and must not be imported into AOS-FARM.
+```
+
 ## Minimal Safety Floor
 
 Minimal Safety Floor обязателен с первого дня, даже если полноценный Governance / Control Module ещё не реализован.
```

## Execution Constraints Verification
- [x] No work outside AOS-FARM.445.A started.
- [x] Canonical docs were NOT rewritten (only appended targeted clarification).
- [x] Safety semantics were NOT weakened.
- [x] No runner/auto-execution introduced.
- [x] No SQLite/RAG-light introduced.
- [x] No destructive cleanup performed.
- [x] No release, commit, push, or merge executed.

## Status
Current Status: `HUMAN_REVIEW_REQUIRED`
