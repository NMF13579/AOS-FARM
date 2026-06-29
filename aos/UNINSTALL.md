# AOS Uninstall Guide

## Manual Uninstall Guidance
To uninstall the AOS consumer package, you must manually delete the `/aos/` directory and remove AOS references from `llms.txt` and `AGENTS.md`.

## Review Before Removal
- Ensure no active tasks are depending on `aos/schemas/`.
- Verify that custom tools or hooks are not pointing to `aos/tools/`.

## Removal Rules
- **No automatic destructive cleanup**: Scripts must not automatically remove the package.
- **What may be removed**: The `/aos/` folder.
- **What must be checked before removal**: Uncommitted work or custom templates saved inside `/aos/`.
- **Human approval required**: Destructive operations (including deletion of the `/aos/` directory) require explicit human authorization.
