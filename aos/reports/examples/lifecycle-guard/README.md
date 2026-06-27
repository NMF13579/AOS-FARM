# Lifecycle Guard Examples

These fixtures show review-only human checkpoint artifacts for commit and push
authorization validation.

The lifecycle guard validates checkpoint semantics only. It does not perform
git operations, does not authorize merge or release, and does not start the
next task.

## Included Fixtures

- `fixtures/valid/commit-authorized.md`
- `fixtures/valid/push-authorized.md`
- `fixtures/negative/commit-not-authorized.md`
- `fixtures/negative/push-not-authorized.md`
- `fixtures/negative/force-push-claimed.md`

## Safety Notes

- PASS is validation result only.
- PASS does not authorize commit.
- PASS does not authorize push.
- PASS does not authorize merge.
- PASS does not authorize release.
- PASS does not start the next task.
- Evidence is not approval.
- CI PASS is not approval.
- Human approval cannot be simulated.
