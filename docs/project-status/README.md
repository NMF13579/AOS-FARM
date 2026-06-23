# AOS-FARM Project Status

## Purpose
This directory (`docs/project-status/`) contains the lightweight, human-readable stage and feature status registry for the AOS-FARM project. It provides a simple project-status layer to help a non-programmer understand what stages exist, their current status, and what features have been implemented.

## Components
- **Stage Registry** (`stage-registry.md`): Tracks the high-level execution stages of the project.
- **Feature Status Registry** (`feature-status-registry.md`): Tracks the status of specific features and capabilities.

## Relationship to docs/features
The `docs/features/` directory holds the documentation explaining *how* to use the features. The `docs/project-status/` directory holds the *current status* of those features and the execution stages that built them.

## Policy
- **Manual Updates Only**: The registries are updated manually. There are NO automated repo scanners or status detectors.
- **Not an Approval Authority**: This registry records status but DOES NOT grant approval.
- **Not Source of Truth**: This registry does not override canonical project sources (`00`, `01`, `02`).
- **UNKNOWN and NOT_RUN**: These states must be preserved. If evidence is missing or a check was not run, the registry must reflect `UNKNOWN` or `NOT_RUN`, not `PASS` or `OK`.
