# AOS-FARM.446 Execution Report

**Stage**: AOS-FARM.446 — Local Temporary Workspace Policy
**Branch**: build/local-temporary-workspace-policy
**Risk Profile**: MEDIUM_RISK_GUIDED

## Files Modified/Created
- `[NEW]` `.gitignore` (in repository root)
- `[NEW]` `docs/development/local-temporary-workspace.md`
- `[NEW]` `aos/root/.gitignore.template`
- `[MODIFY]` `aos/root/AGENTS.md`
- `[MODIFY]` `aos/INSTALL.md`
- `[MODIFY]` `aos/ADOPTION.md`
- `[MODIFY]` `aos/docs/workflow/consumer-runtime-handoff.md`

## Exact `.gitignore` Rule Added
```gitignore
/.aos-tmp/
```

## Product-Folder Guidance Summary
- **Template Provided:** A standard `.gitignore.template` has been added to `aos/root/` for consumer projects that don't already have one.
- **Rule Enforcement:** `aos/root/AGENTS.md` now explicitly restricts target projects to use `/.aos-tmp/` for temporary command outputs and logs.
- **Installation/Adoption Guidance:** `aos/INSTALL.md` and `aos/ADOPTION.md` now explicitly instruct consumers to ignore `/.aos-tmp/` in their root `.gitignore`.
- **Handoff Contract Clarification:** `aos/docs/workflow/consumer-runtime-handoff.md` strictly clarifies that `.aos-tmp/` must remain outside the `aos/` product folder, and must never contain Evidence, reports, or approval checkpoints.

## Verification Command Outputs
- `git status --short`: (Truncated to changed tracked files)
  ```
   M aos/ADOPTION.md
   M aos/INSTALL.md
   M aos/docs/workflow/consumer-runtime-handoff.md
   M aos/root/AGENTS.md
  ```
- `git diff --check`: (No output, confirming no trailing whitespace errors in tracked files)
- `git diff --name-only`: 
  ```
  aos/ADOPTION.md
  aos/INSTALL.md
  aos/docs/workflow/consumer-runtime-handoff.md
  aos/root/AGENTS.md
  ```
- `git check-ignore .aos-tmp/example.log`: 
  ```
  .aos-tmp/example.log
  ```
- `grep -R ".aos-tmp" ...`: 
  ```
  .gitignore:/.aos-tmp/
  docs/development/local-temporary-workspace.md:This policy governs the usage of the local temporary workspace `.aos-tmp/` within the AOS-FARM repository and target consumer projects.
  ...
  aos/root/.gitignore.template:/.aos-tmp/
  aos/root/AGENTS.md:- Target projects must use a local-only `/.aos-tmp/` directory in their project root...
  ```

## Dogfood Result
The dogfood test successfully demonstrated that generating a mock `.aos-tmp/status.log` is fully ignored by Git (`git status --short` did not list it, and `git check-ignore` correctly matched it). The file was then successfully cleaned up.

## Confirmations
- **No `.aos-tmp/` contents staged/committed**: Confirmed.
- **No reports moved/deleted**: Confirmed.
- **No broad cleanup introduced**: Confirmed.

**Final Status**: HUMAN_REVIEW_REQUIRED
