# AOS-FARM.447 Commit Authorization Package

* **stage:** AOS-FARM.447 — Canonical Project Documentation Alignment
* **branch:** build/canonical-project-docs-alignment
* **Risk Profile:** HIGH_RISK_PROTECTED
* **HEAD hash:** 70499854c653c8bf67628e147e077c6355a7775c
* **origin/dev hash:** 70499854c653c8bf67628e147e077c6355a7775c
* **ahead/behind result:** 0 0
* **ls-remote result:** `FAILED` (Network/DNS error: Could not resolve host: github.com)
* **complete changed file list:**
  * `00_AOS_Core_Control.md`
  * `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
  * `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
* **complete report list intended for commit:**
  * `reports/aos-farm-447-0-1-baseline-source-check-report.md`
  * `reports/aos-farm-447-execution-report.md`
  * `reports/aos-farm-447-final-review-report.md`
* **excluded local/untracked files:**
  * All previous/historical `reports/aos-farm-*` untracked files (e.g. 442, 443, 444, 445, 446).
  * All previous/historical `reports/human-checkpoints/*` untracked files.
  * All `tests/*` untracked files.
* **diff --check result:** Clean (no whitespace errors).

## Summaries

* **repository naming alignment summary:** Updated legacy `NMF13579/AOS-1` references to `NMF13579/AOS-FARM` where current active repo is discussed. Added explicit clarification that AgentOS/AOS-1 naming is historical/reference unless human-approved.
* **branch model alignment summary:** `dev` explicitly described as the active controlled integration baseline; `build/` recommended for implementations. Removed old "frozen skeleton" constraints.
* **product folder boundary preservation summary:** `/aos/` and internal `agentos/` layers remain strictly preserved. Legacy AgentOS import explicitly blocked.
* **Local Temporary Workspace Boundary summary:** The `/.aos-tmp/` definition has been added to canonical sources 00, 01, and 02. Expressly forbids Source of Truth, Evidence, approval, and checkpoints inside `/.aos-tmp/`.
* **safety/control semantics review summary:** Escalation to `HUMAN_REVIEW_REQUIRED` or `UNKNOWN_BLOCKED` enforced in `02_AOS_Governance_Control_Module_and_Safety_Rules.md` if protected governance artifacts appear in `/.aos-tmp/`. No safety regressions or weakened PASS semantics.

## Important Authorizations & Limitations

* **Network limitation:** `remote refs/heads/dev` must be rechecked before push authorization when network becomes available.
* **Execution limitation:** Creating this package does **NOT** authorize commit.

## Proposed Commit Message

```text
docs: align canonical project documentation with aos-farm
```

* **final_status:** HUMAN_REVIEW_REQUIRED
