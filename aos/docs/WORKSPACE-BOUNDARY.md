# Workspace Boundary

This document explains the folder boundary model for AOS-FARM consumer usage.

## 1. /aos/
- **Purpose**: AOS core package.
- Contains documentation, scripts, and internal templates.
- **Not for**: Target product code.

## 2. /aos/root/
- **Purpose**: Root-level templates for target repositories.
- Files here (e.g., `AGENTS.md`, `llms.txt`) may map to the target repo root through the installer in the future.
- **Not for**: Active target runtime state. They are templates, not active runtime files by themselves.

## 3. /project/
- **Purpose**: User project documentation workspace.
- Used for requirements, plans, decisions, notes, and task context.
- **Not for**: Default product source code. It should not silently become the product code root.

## 4. /aos-modules/
- **Purpose**: Container for AOS modules/extensions.
- It is a module boundary only, not part of the core package.
- **Not for**: Core package files.

## 5. /aos/prompt-packs/
- **Purpose**: Specific instructions for different agent environments (Prompt Packs).
- **Not for**: General documentation or product code.

## 6. /.aos-tmp/
- **Purpose**: Local temporary scratch workspace only.
- It is ignored by version control and is entirely disposable.
- **Not for**: Evidence, reports, approvals, checkpoints, or canonical files.
- **Source of Truth?**: **No.** `/.aos-tmp/` is never the Source of Truth.

## Folder Boundary Summary

| Folder | Purpose | Allowed examples | Forbidden examples | Source of Truth? |
| --- | --- | --- | --- | --- |
| `/aos/` | AOS core package | docs, scripts, templates | user product code | yes, for AOS package |
| `/aos/root/` | root templates | `AGENTS.md`, `llms.txt` | active target runtime state | yes, as templates |
| `/project/` | project documentation workspace | requirements, plans, decisions | default `src/`, `app/`, `backend/` | yes, for project docs |
| `/aos-modules/` | module container | module docs/packages | core package files | depends on module |
| `/aos/prompt-packs/` | agent instructions | agent-specific prompt guidelines | general documentation | yes, for prompts |
| `/.aos-tmp/` | temporary scratch | transient logs, temporary command output | Evidence, approvals, reports, canonical files | no |

## Where should an agent write?

Rules:
- If it is AOS core documentation, use `/aos/docs/`.
- If it is an installable root template, use `/aos/root/`.
- If it is user project planning/documentation, use `/project/`.
- If it is an AOS module, use `/aos-modules/`.
- If it is temporary scratch output, use `/.aos-tmp/`.
- If it is Evidence/report/approval/checkpoint, do not use `/.aos-tmp/`.
- If the correct location is unclear, stop with `HUMAN_REVIEW_REQUIRED`.

## Important Safety Invariants
- `/project/` is documentation workspace, not default product source root.
- `/.aos-tmp/` is never Source of Truth.
- Reports and Evidence must not be stored in `/.aos-tmp/`.
- Protected/canonical files require human checkpoint.
- PASS/Evidence/self-test do not equal approval.
