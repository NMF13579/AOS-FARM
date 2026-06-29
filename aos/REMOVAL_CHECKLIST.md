# AOS Removal Checklist

## Safe Review Checklist
- [ ] **Dependency check**: Ensure no active project workflows rely on `aos/` schemas or prompts.
- [ ] **Modified user files check**: Verify if `llms.txt`, `AGENTS.md`, or `.gitignore` have been modified with AOS data, and revert them safely.
- [ ] **Generated/scratch files check**: Ensure `.aos-tmp/` and any generated reports are backed up or explicitly slated for deletion.

## Approval Boundary
- **Do not use `rm -rf` by default.**
- Human authorization must be explicitly granted before deleting the `/aos/` folder or reverting root templates.
