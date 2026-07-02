# Task Intake Wizard

> **GUIDANCE BOUNDARY:**
> This document is guidance only.
> It does not grant approval, execution permission, commit permission,
> push permission, merge permission, release permission, or lifecycle mutation
> permission.

---

## Purpose

The Task Intake Wizard provides a structured routing layer to classify incoming raw ideas and determine the correct next step. It ensures that ideas are appropriately scoped, refined, and evaluated before becoming task candidates.

This is a documentation and prompt alignment layer, not an executable script.

## Intake Statuses

During the intake process, an idea must be classified into one of the following exact statuses:
- `NEEDS_PROBLEM_INTERVIEW`
- `NEEDS_TZ`
- `TOO_BROAD`
- `TOO_SMALL`
- `DUPLICATE_OR_OVERLAP`
- `BLOCKED`
- `READY_FOR_TASK_CANDIDATE`
- `HUMAN_REVIEW_REQUIRED`

## Medical-Domain Fast-Exit

A critical part of the intake wizard is identifying medical-domain requests.

**If request touches clinical decisions, patient data, diagnosis, treatment, triage, medical recommendations, regulated health workflows, or clinical decision support:**
- **status:** `HUMAN_REVIEW_REQUIRED`
- **normal intake flow:** stopped
- **reason:** medical-domain boundary requires separate architecture

This is an always-on mandatory check for all intake activities.
