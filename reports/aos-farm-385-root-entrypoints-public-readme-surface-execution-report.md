# AOS-FARM-385 Root Entrypoints and Public README Surface Execution Report

## Execution Details
- **Task**: AOS-FARM.385 — Controlled Root Entrypoints and Public README Surface Update
- **Target File Set**: Derived from `aos-farm-383-root-entrypoints-public-readme-surface-authorization-package.md`
- **Execution Mode**: STRICT ALLOWLIST
- **Risk Profile**: HIGH_RISK_PROTECTED

## Created / Rewritten Paths
The following root files were updated to present AOS-FARM as a public Consumer Kit:

### Rewritten
- `README.md`: Replaced old internal Build Steps roadmap with a clean, public-facing summary of the AOS framework, its fail-closed philosophy, and explicit instructions to look in the `aos/` directory for installation.
- `README.ru.md`: Symmetrically translated the new `README.md` into Russian.

### Modified
- `AGENTS.md`: Appended the `## AOS Consumer Kit Reference` block instructing agents to consult `aos/AGENT_CONTEXT.md` and `aos/START_HERE.md` for Consumer product information. Crucially, the internal core controls (`00/01/02/03`) remain untouched and explicitly protected.

## Boundary Verification
- [x] Did NOT create `llms.txt`.
- [x] Did NOT modify existing legacy `docs/`, `templates/`, or `agentos/` folders.
- [x] Did NOT modify internal core control files (`00/01/02/03`).
- [x] Did NOT modify `aos/` kit files.
- [x] Did NOT stage, commit, or push.
- [x] Did NOT add any active runners, CI hooks, DB/RAG dependencies, or Spec Kit components.

## Next Steps
Root entrypoint update is complete. The modified files await post-execution verification before final stage validation.

## Final Status
**AOS_FARM_385_ROOT_ENTRYPOINTS_PUBLIC_README_SURFACE_EXECUTION_COMPLETE**
