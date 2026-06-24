# Agent Tutor Question Routing

If a user asks a question, the Agent Tutor should consult these specific files before answering:

| User Question Type | Target Documentation Source |
|---|---|
| "What is this feature?" | `docs/features/feature-documentation-registry.md` |
| "What already exists?" | `docs/project-status/feature-status-registry.md` |
| "What stages are closed?" | `docs/project-status/stage-registry.md` |
| "How do I start?" | `docs/user-guide/README.md` |
| "Why is approval needed?" | `docs/user-guide/commit-push-approval-workflow.md` |
| "Why is the agent blocked?" | The most recently modified report + human checkpoint |
| "What is the next safe step?" | `docs/project-status/stage-registry.md` + latest closure report |
| "Prepare a prompt for the executor" | Use relevant `templates/` + authorized scope |
