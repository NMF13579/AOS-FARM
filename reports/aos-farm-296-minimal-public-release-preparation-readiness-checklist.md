# AOS-FARM.296 — Minimal Public Release Preparation Readiness Checklist

## Goal
Verify that all preconditions for a minimal public release are met, and gather the evidence required for a final Human Release Decision.

## Checklist Items

- [ ] **README Entrypoint Check**: The `README.md` must clearly point to the file-based bootstrap workflow and must not reference the deleted `agentos/agentos.py start` script.
- [ ] **User Guide Check**: `docs/user-guide/README.md`, `bootstrap-agent-workflow.md`, and `agent-tutor-mode.md` must accurately reflect the dogfood-verified state.
- [ ] **Template Duplicate Check**: Confirm 0 duplicate files (`* 2.md`) exist in the `templates/` directory.
- [ ] **Safety Invariant Check**: The repository must comply with the Minimal Safety Floor and all core governance files (`00`, `01`, `02`) must be intact.
- [ ] **Release Boundary Check**: Verify that no unauthorized script execution logic or unapproved runners are present.
- [ ] **Evidence-Tail Check**: Ensure that all preparation and verification artifacts (including this checklist) are documented and staged for final commit.

## Human Release Decision Placeholder
- `release_decision_ready`: false
- `human_release_authorization_provided`: false
- `release_tag_authorized`: pending
- `release_notes`: pending
