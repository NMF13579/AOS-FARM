# UNKNOWN Resolution Addendum Template

```yaml
artifact_type: unknown_resolution_addendum
artifact_status: DRAFT
approval_status: NOT_APPROVED
execution_status: NOT_AUTHORIZED
source_contract: "[path]"
```

## 1. Purpose

Record human decisions or additional evidence that resolve specific UNKNOWN items from an Implementation Contract.

This addendum is Evidence. It is not approval and does not authorize implementation.

## 2. UNKNOWN Item

- UNKNOWN id:
- UNKNOWN statement:
- source location:
- related contract section:

## 3. Why It Blocks Implementation Readiness

Explain the engineering decision that cannot be safely made while this item remains UNKNOWN.

## 4. Resolution Options

| Option | Description | Impact | Risk |
|---|---|---|---|
| A | | | |
| B | | | |

## 5. Human Decision Required

- decision owner:
- exact decision needed:
- decision deadline, if any:
- evidence required:

## 6. Human Decision Recorded

```yaml
human_decision: MISSING
decision_evidence: MISSING
approval_status: NOT_APPROVED
```

## 7. Impact on Scope / Risk

- scope impact:
- risk impact:
- Risk Profile change needed:
- protected/canonical impact:
- validation impact:

## 8. Updated Contract Section

State the replacement or addition to the Implementation Contract.

## 9. Unresolved UNKNOWN Handling

If unresolved, status must remain:

```text
UNKNOWN_BLOCKED
```

or:

```text
HUMAN_REVIEW_REQUIRED
```

Do not treat unresolved UNKNOWN as OK.

## 10. Safety Boundary

- This addendum does not approve implementation.
- This addendum does not authorize execution.
- Evidence does not equal approval.
- `UNKNOWN` does not equal OK.
- Human approval cannot be simulated.
