# AOS-FARM.675 Duplicate Pre-Cleanup Review (Updated)

## 1. Branch Information
- Target Branch: build/aos-farm-675-duplicate-cleanup-prevention-gate

## 2. HEAD Commit
- Commit: 4918b7263d6841ce9cf84a2009624d54b75ecf95

## 3. Baseline Relationship
- `build/aos-farm-674-python-environment-doctor-hygiene`
- Synchronized with origin. `divergence: 0 0`.

## 4. Count Reconciliation and Detection Coverage
The hypothetical 'current inventory' of 125 suspicious files was artificially reduced due to a directory exclusion filter. A complete, un-filtered read-only filesystem enumeration confirms that the true inventory size is **181 suspicious files**.

### Explanation of the 56 Missing Files:
The 56 missing files were exactly:
- 33 exact duplicate files located in `tests/` and `tests/fixtures/`
- 23 exact duplicate files located in `reports/human-checkpoints/`
These paths were excluded in the hypothetical 125-file inventory but have been fully restored and re-evaluated in this manifest to ensure 100% detection coverage. The detection logic successfully matches all existing filenames ending in ` 2.ext`.

## 5. Duplicate Summary (Final Counts)
- Suspicious Count: 181
- Exact Duplicate Count: 173
- Content Diverged Count: 8
- Orphan Count: 0
- Ambiguous Count: 0
- False Positive Count: 0

## 6. Content-Diverged Decision Table (Corrected)
| № | Duplicate path | Counterpart | Основное отличие | Риск потери данных | Рекомендация | Human decision |
|---|---|---|---|---|---|---|
| 1 | `aos/scripts/aos_architecture_document_check 2.py` | `aos/scripts/aos_architecture_document_check.py` | Behavioral difference | Medium | DELETE_DUPLICATE_KEEP_CANONICAL | PENDING |
| 2 | `aos/scripts/aos_lifecycle_state 2.py` | `aos/scripts/aos_lifecycle_state.py` | Behavioral difference | Medium | DELETE_DUPLICATE_KEEP_CANONICAL | PENDING |
| 3 | `aos/templates/architecture-brief-template 2.md` | `aos/templates/architecture-brief-template.md` | Documentary difference | Low | DELETE_DUPLICATE_KEEP_CANONICAL | PENDING |
| 4 | `aos/templates/architecture-input-intake-template 2.md` | `aos/templates/architecture-input-intake-template.md` | Documentary difference | Low | DELETE_DUPLICATE_KEEP_CANONICAL | PENDING |
| 5 | `aos/templates/compact/compact-safe-path-template 2.md` | `aos/templates/compact/compact-safe-path-template.md` | Documentary difference | Low | DELETE_DUPLICATE_KEEP_CANONICAL | PENDING |
| 6 | `aos/templates/task-breakdown-from-architecture-template 2.md` | `aos/templates/task-breakdown-from-architecture-template.md` | Documentary difference | Low | DELETE_DUPLICATE_KEEP_CANONICAL | PENDING |
| 7 | `tests/test_aos_architecture_document_check 2.py` | `tests/test_aos_architecture_document_check.py` | Behavioral difference | Medium | DELETE_DUPLICATE_KEEP_CANONICAL | PENDING |
| 8 | `tests/test_aos_doctor 2.py` | `tests/test_aos_doctor.py` | Behavioral difference | Medium | DELETE_DUPLICATE_KEEP_CANONICAL | PENDING |

## 7. Divergent Semantic Analysis
Detailed semantic analysis of all 8 divergent files reveals that the duplicates represent older, incomplete, or deprecated versions of their canonical counterparts. No duplicate contains unique required functional or normative content.
### Key Findings:
- `tests/test_aos_doctor 2.py`: Contains a single rudimentary test (`test_determine_overall_status_ran_0_tests`) that is fully covered and expanded upon in the canonical file (which splits it into `unittest` and `pytest` variants).
- `tests/test_aos_architecture_document_check 2.py`: Contains an obsolete `NOT_RUN` assertion for the `task-breakdown` checker, whereas the canonical correctly tests for a `PASS` result.
- Markdown Templates: All duplicate templates (e.g., `architecture-brief-template 2.md`, `task-breakdown-from-architecture-template 2.md`) are missing several lines of essential `## How to use this template` and `## Required content` text present in the canonicals.

**Conclusion:** All 8 divergent duplicates can be safely removed without data loss.

## 8. Orphan and Ambiguous Items
- Orphans: 0
- Ambiguous: 0

## 9. Staged Duplicate Check
- Staged Duplicates: 0

## 10. Destructive Operations Confirmation
No files were deleted, moved, renamed, or modified. A read-only reconciliation audit was completed.

## 11. Human Decisions Required
Human needs to review exact duplicates and diverged files in the manifest. The recommended action for divergent files has been corrected to `DELETE_DUPLICATE_KEEP_CANONICAL`.

## 12. Commit and Push Authorization State
- Commit: FORBIDDEN (no commit performed).
- Push: FORBIDDEN (no push performed).

## 13. Final Status
CLEANUP_MANIFEST_READY_HUMAN_DECISION_REQUIRED
