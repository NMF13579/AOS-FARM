# Evidence-based Hardening

## 1. What is Evidence-based Hardening?
Evidence-based hardening is the process of reviewing Evidence collected from previous Build Steps (artifacts, logs, state files) to identify gaps, weaknesses, and potential security or control boundaries that need reinforcement. This process results in "hardening candidates" rather than immediate implementations.

## 2. Invariants & Formulas
The following formulas are absolute and must be preserved:

- `PASS ≠ approval`
- `Evidence ≠ approval`
- `CI PASS ≠ approval`
- `UNKNOWN ≠ OK`
- `NOT_RUN ≠ PASS`
- `No blocker ≠ approval` (Absence of a blocker does not mean we are ready for release)
- `Hardening candidate ≠ authorized change`
- `Roadmap proposal ≠ roadmap mutation`
- `Human approval cannot be simulated`

## 3. Why Evidence ≠ Approval
Evidence is purely a factual record of what happened (e.g., "the script ran and returned 0"). It lacks the semantic context of intent, risk assessment, and organizational authorization. Therefore, collecting Evidence does not substitute for Human Approval.

## 4. Why PASS ≠ Approval
A "PASS" status means a technical check (validator, script, linter) succeeded against its programmed rules. It does not mean the change is safe, architecturally sound, or authorized for production.

## 5. Why CI PASS ≠ Approval
Continuous Integration (CI) passing only validates that code compiles and tests run successfully. It cannot validate business logic risk, governance compliance, or the necessity of a change. CI PASS is a prerequisite for review, not the review itself.

## 6. How Hardening Candidates Emerge from Evidence
When Evidence is reviewed, we look for:
- Manual steps that could be automated but aren't yet.
- Areas where a validator checks syntax but misses semantics.
- Processes where human error could bypass a control.
These observations become "Hardening Candidates", which are recorded for future planning.

## 7. Why Hardening Proposal ≠ Authorization
A proposal merely identifies a gap and suggests a fix. It does not carry the authority to implement the fix. Implementation requires a separate, explicit Human Checkpoint.
