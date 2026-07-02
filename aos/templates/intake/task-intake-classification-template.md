# Task Intake Classification

## Overview
Use this template to classify a raw idea into an actionable intake status.

## Raw Idea
[Insert raw idea description here]

## Classification Status
[Select exactly one:]
- NEEDS_PROBLEM_INTERVIEW
- NEEDS_TZ
- TOO_BROAD
- TOO_SMALL
- DUPLICATE_OR_OVERLAP
- BLOCKED
- READY_FOR_TASK_CANDIDATE
- HUMAN_REVIEW_REQUIRED

## Medical-Domain Check
Does the request touch clinical decisions, patient data, diagnosis, treatment, triage, medical recommendations, regulated health workflows, or clinical decision support?

[If Yes:]
- **status:** HUMAN_REVIEW_REQUIRED
- **normal intake flow:** stopped
- **reason:** medical-domain boundary requires separate architecture

## Next Steps
[Explain next steps based on classification status]
