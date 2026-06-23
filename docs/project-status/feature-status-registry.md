# Feature Status Registry

| Feature ID | Feature Name | Feature Type | Status | Introduced By Stage | Related Docs | Related Templates | Related Scripts | Related Reports | Related Commit | User Entry Point | Approval Boundary | Known Limitations | Not Implemented | Last Updated |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | Governance Control Module | Core | IMPLEMENTED | UNKNOWN | `02_AOS_Governance_Control_Module_and_Safety_Rules.md` | `human-approval-boundary-template.md` | None | UNKNOWN | UNKNOWN | Checkpoints | Protected | Manual compliance | Automated enforcement | 2026-06-23 |
| F-002 | Document Pipeline | Tooling | IMPLEMENTED | AOS-FARM.202 | `docs/features/` | None | `document_pipeline.py` | AOS-FARM.195, 202 | `e80746f3` | Python Script | Guided | Local only | RAG / Chat | 2026-06-23 |
| F-003 | Manual Feature Registry | Docs | IMPLEMENTED | AOS-FARM.210 | `docs/features/README.md` | `feature-documentation-template.md` | None | AOS-FARM.210 | `63c19b1a` | `README.md` | Guided | Manual only | Auto-scanners | 2026-06-23 |
| F-004 | Stage Status Registry | Docs | IMPLEMENTED | AOS-FARM.217 | `docs/project-status/README.md` | `stage-status-record-template.md` | None | AOS-FARM.217 | UNKNOWN | `README.md` | Guided | Manual only | CI Integration | 2026-06-23 |

*(Note: UNKNOWN and NOT_RUN are strictly preserved and must not be converted to OK or PASS without evidence.)*
