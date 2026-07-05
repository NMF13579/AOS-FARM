# AOS-FARM.620 — Registry Baseline Repair Dogfood Report

## 1. Status
```yaml
task_id: AOS-FARM.620
stage: Registry Baseline Repair and Architecture Blocker Cleanup
risk_profile: HIGH_RISK_PROTECTED
report_type: dogfood
status: PASS
approval_status: NOT_APPROVED
human_review_required: true
```

## 2. Scope

In scope:

* Repair architecture registry validation blocker.
* Preserve fail-closed ACTIVE / PROPOSED semantics.
* Add validator semantics coverage.
* Keep registry PASS separate from approval.

Out of scope:

* Human approval.
* Canonical promotion.
* Default stack selection.
* Implementation authorization.
* Execution authorization.
* Release authorization.
* AOS-FARM.621.

## 3. Blocker found

Blocker id: REGISTRY_ACTIVE_FALSE_POSITIVE

Summary:

* The validator treated prose text containing the word ACTIVE as an ACTIVE registry entry.
* The triggering text was documentation prose, not a real registry entry.
* No actual ACTIVE registry entries were found.
* Existing registry entries were PROPOSED.

Root cause:

* ACTIVE detection was too broad.
* A broad word regex matched ACTIVE in documentation prose.

## 4. Repair applied

Repair type: PATCH_VALIDATOR_FALSE_POSITIVE_NARROWLY

Applied behavior:

* Prose text containing ACTIVE is ignored.
* Real status: ACTIVE is still detected.
* Real - status: ACTIVE is still detected.
* ACTIVE without checkpoint remains BLOCKED.
* ACTIVE with checkpoint remains HUMAN_REVIEW_REQUIRED unless an explicit human design decision changes that.
* PROPOSED entries pass.
* APPROVED / execution / release / default stack authority remains blocked.

Changed files:

* aos/scripts/aos_architecture_document_check.py
* tests/test_aos_architecture_document_check.py
* aos/reports/dogfood/aos-farm-620-registry-baseline-repair-dogfood.md

## 5. Additional semantic gap found

During semantics tests, default_stack: true was found not to be blocked.

Repair:

* Added default_stack: true to the positive authority checks.
* Added test coverage proving default_stack: true is BLOCKED.

Reason:

* Selecting a default stack is an architecture decision.
* A validator PASS must not select or imply a default stack.

## 6. Registry state

Registry state after repair:

* registry --validate: PASS
* Registry entries remain PROPOSED.
* No registry entry was promoted to ACTIVE.
* No default stack was selected.
* No approval record was created.
* No checkpoint marker was added.
* No implementation was authorized.
* No execution was authorized.
* No release was authorized.

## 7. Validation evidence

Commands run:

```bash
python3 aos/scripts/aos_architecture_document_check.py registry --validate
python3 -m py_compile aos/scripts/aos_architecture_document_check.py
python3 -m unittest tests/test_aos_architecture_document_check.py
```

Expected result:

* registry --validate: PASS
* py_compile: OK
* scoped unittest: OK

## 8. Boundary statements

Mandatory boundaries:

* Registry PASS ≠ approval.
* Registry repair ≠ approval.
* Evidence ≠ approval.
* CI PASS ≠ approval.
* ACTIVE without checkpoint is BLOCKED.
* Human approval cannot be simulated.
* PROPOSED ≠ ACTIVE.
* NOT_APPROVED ≠ approval.
* No default stack was selected.
* No implementation was authorized.
* No execution was authorized.
* No release was authorized.

## 9. Safety verification

Confirmed:

* No 00_AOS_Core_Control.md change.
* No 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md change.
* No 02_AOS_Governance_Control_Module_and_Safety_Rules.md change.
* No /aos/root/AGENTS.md change.
* No agentos/ change.
* No installer apply logic change.
* No fake approval.
* No fake checkpoint.
* No ACTIVE promotion.
* No canonical promotion.
* No release.
* AOS-FARM.621 was not started.

## 10. Conclusion

AOS-FARM.620 repaired the architecture registry validation baseline without simulating approval or expanding execution authority.

The registry baseline now validates as PASS, but this PASS is validation only.

It is not approval, not implementation authorization, not execution authorization, not release authorization, and not default stack selection.
