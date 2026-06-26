# Post-Execution Verification Checklist

- [ ] Ensure `git status` shows only authorized modified paths.
- [ ] Ensure `git diff --cached` is empty (if commit was deferred).
- [ ] Ensure `AGENTS.md` and `aos/config` are untouched.
- [ ] Ensure the work stayed inside the exact authorized scope.
- [ ] Record any `NOT_RUN` checks explicitly.
- [ ] Record any `UNKNOWN` items explicitly.
- [ ] Remember that verification is not commit approval.
