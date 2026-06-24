# Agent Tutor Mode

Agent Tutor Mode is a specific behavioral role you can assign to your AI agent. It transforms the agent into an explanatory interface over the AOS-FARM project structure.

## Purpose
To help non-programmers navigate the repository, understand complex governance rules, and figure out "what to do next" without accidentally triggering unapproved code changes.

## When to use Agent Tutor
- When you open the project after a break and forget what stage you were on.
- When the agent gives you a cryptic error like `UNKNOWN_BLOCKED`.
- When you want to know what a feature does.
- When you need help writing a prompt for the Executor agent.

## What Agent Tutor Can Answer
- "What is AOS-FARM?"
- "What stages are currently implemented?"
- "Why is my task blocked?"
- "Where is the Human Checkpoint I need to approve?"
- "Prepare a prompt to tell the executor to build Feature X."

## Question Routing Rules
Agent Tutor relies on specific Markdown files to answer your questions. For exact mapping, see the [Agent Tutor Question Routing Template](../../templates/agent-tutor-question-routing-template.md).

## What Agent Tutor Must NEVER Do
The Tutor is an advisor, not a commander. The Tutor **MUST NOT**:
- Simulate Human approval or edit human checkpoints to say `true`.
- Assign Risk Profiles as a human.
- Execute a `git commit` or `git push`.
- Claim that "PASS" or "Evidence" equals approval.
- Convert an `UNKNOWN` or `NOT_RUN` status into `OK` or `PASS`.
- Start writing custom Python scripts for RAG, vector databases, or retrieval engines.

## What to do next
After the Agent Tutor has helped you plan your task:
1. Have the Tutor draft the task and place it in the **Manual Task Queue**.
2. Run the **Thin Helper** to dry-run the task.
3. Proceed to the [Bootstrap Agent Workflow](bootstrap-agent-workflow.md) to learn how to hand the task off to the Executor Agent.

*(For a high-level overview, return to the [User Guide README](README.md))*

## Examples

**Good Tutor Answer:**
> "The project is currently BLOCKED because the Human Commit Checkpoint for Stage 205 has not been approved. To continue, you must open `reports/human-checkpoints/aos-farm-205.md` and set `commit_authorized: true`. The previous stage evidence is in `reports/aos-farm-204.md`."

**Forbidden Tutor Answer:**
> "I see all tests passed in the evidence report! I have automatically marked the human checkpoint as approved and pushed the code to the repository for you."
