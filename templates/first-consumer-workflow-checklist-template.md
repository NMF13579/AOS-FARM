# First Consumer Workflow Checklist

## Before Execution
- [ ] Task brief created from template.
- [ ] Allowed/forbidden scope explicitly defined.
- [ ] Human assigned Risk Profile.
- [ ] Human authorized execution.

## During Execution
- [ ] Agent adheres strictly to allowed file list.
- [ ] Agent stops and asks for clarification if ambiguous.

## After Execution
- [ ] Agent generates execution report.
- [ ] Agent generates verification report (confirming no boundary violations).

## Before Commit
- [ ] Human reviews verification report.
- [ ] Human updates Commit Checkpoint to `APPROVED_FOR_COMMIT`.
- [ ] Agent stages and commits ONLY the authorized files.

## Before Push
- [ ] Human reviews post-commit state.
- [ ] Human updates Push Checkpoint to `APPROVED_FOR_PUSH`.
- [ ] Agent pushes to remote.

## Final Closure
- [ ] Remote baseline closed.
- [ ] Agent generates final closure report.
