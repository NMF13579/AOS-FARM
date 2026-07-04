# AOS-FARM.611 — Process Friction Backlog
## 1. Scope
This backlog is Evidence/input for future human decision. It is not an approval, nor is it a roadmap mutation.

## 2. Friction Items

### FRICTION-611-01 — Shallow Handoff "What Was Done"
```yaml
id: FRICTION-611-01
severity: LOW
source_pass: 611.1
finding: The handoff script natively scrapes programmatic activity for "What Was Done", resulting in "Collected handoff summary" rather than a broader context summary.
evidence: "What Was Done: - Collected handoff summary" output in 611.1.
impact: Mild context loss across session boundaries for complex tasks.
proposed_follow_up: Add an optional argument to the script to accept a user-defined context string, or tune the prompt.
suggested_stage: 612_polishing_candidate
requires_human_decision: true
```

### FRICTION-611-02 — Untracked File Diff Visibility
```yaml
id: FRICTION-611-02
severity: LOW
source_pass: 611.2
finding: The review package `--files` scope correctly loads report file names, but because they are untracked, they don't show up in the standard git Diff Summary.
evidence: Empty diff summary in 611.2 for explicitly scoped `reports/aos-farm-611-1...` file.
impact: Potential user confusion over missing file content in the review package.
proposed_follow_up: Minor script update to inject `git diff --no-index /dev/null <file>` for untracked scoped files.
suggested_stage: 612_polishing_candidate
requires_human_decision: true
```

## 3. Severity Summary
* LOW: 2
* MEDIUM: 0
* HIGH: 0
* UNKNOWN_BLOCKED: 0

## 4. Recommended Handling
defer_to_612

## 5. Boundary Notes
* backlog is not approval
* backlog is not execution authorization
* backlog is not roadmap mutation
