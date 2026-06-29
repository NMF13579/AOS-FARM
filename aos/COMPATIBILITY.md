# AOS Package Compatibility

## Supported Target Repo Assumptions
- Standard Git repository.
- Markdown support.

## Usage
- Docs-only/manual-first usage is fully supported and recommended as the default.

## Optional Helper Requirements
- Python 3.10+ required if utilizing scripts in `aos/tools/optional/`.

## Unsupported Cases
- Environments without local file system access.
- Fully autonomous execution without human-in-the-loop checkpoints.

## Dependency Boundaries
- The AOS package relies on no external proprietary databases. It relies solely on local filesystem state and standard Git operations.
