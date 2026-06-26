# First Session Guide

Welcome to your first session using the AOS Consumer Kit. This guide will walk you through the correct path to start your project safely and effectively. 

AOS is methodology-first. You will interact with an AI agent (like ChatGPT, Claude, or a local agent) by providing it with carefully crafted prompts.

## The Workflow: 5-Minute Overview

### 1. Initialize the Problem Intake Agent
Your very first step is to explain your idea. Do not write any code.
- **Copy this prompt:** Open `aos/prompts/problem-intake.md` and copy its entire contents.
- **Paste it:** Paste the prompt into your AI agent's chat interface.
- **What happens:** The agent will greet you and ask if you want to proceed with an interview or review an existing brief.
- **The Process:** If you choose the interview, the agent will ask you **one question at a time**. It does this to uncover the *real* problem, your users, constraints, and gray areas. Answer naturally.

### 2. Capture the Problem Intake Summary
Once the interview is complete, the agent will produce a structured summary.
- **Save the output:** Copy the agent's final summary.
- **Format it:** Ensure it matches the structure found in `aos/templates/task-briefs/problem-intake-template.md`. Save this locally (e.g., `aos/reports/problem-intake/<project-or-feature-name>.md`).
- **Safety Note:** This document is just evidence. It is **not** an approval to begin writing code.

### 3. Build the Technical Assignment (The Handoff)
Now that the problem is defined, you must translate it into technical boundaries.
- **Open Builder:** Open `aos/prompts/technical-assignment-builder.md` and copy its contents.
- **Paste Intake Output:** Paste the prompt into your agent, along with the full contents of the Problem Intake document you just saved.
- **Save TA Output:** The agent will define strict boundaries. Capture this output and save it locally (e.g., `aos/reports/technical-assignments/<project-or-feature-name>.md`).
- **Safety Note:** Do not start implementation until you pass a human review and approval checkpoint.

### 4. Build the Task Breakdown and Queue
A Technical Assignment is too broad for an AI to implement all at once. You must break it down.
- **Which prompt do I copy next?** Open `aos/prompts/task-brief-builder.md` and copy its contents.
- **What input do I paste with it?** Paste the prompt and the full `Technical Assignment` document from Step 3.
- **What output should I expect?** The agent will generate a `Task Breakdown` and a manual `Task Queue`. The agent will explicitly tell you it will not write code yet.

### 5. Human Task Review
You must manually review the generated task queue.
- **What do I need to review manually?** Ensure every task draft traces directly back to your Technical Assignment. The agent is not authorized to invent new features. Check the proposed priorities and dependencies.
- **What does approval mean here?** Moving a task to `READY_FOR_EXECUTION_AUTHORIZATION` means it's a good plan, but it is **still not authorized** for implementation.
- **How do I know which task is next?** Select a task (or a batch of tasks) from the queue that has no blocked dependencies.

### 6. Proceed to Controlled Execution
Now you can create a specific, execution-ready brief for your chosen task.
- **Create the brief:** Use `aos/templates/task-briefs/controlled-task-brief-template.md` to define the exact constraints for the selected task.
- **When can the agent start writing code?** Only after you have explicitly given the agent the filled-out `controlled-task-brief` and explicitly granted **Execution Authorization**.
- **What should I read next?** Open `aos/docs/workflow/first-controlled-execution.md`. It explains the first safe bridge from `Controlled Task Brief` to `Human Execution Authorization`, `Controlled Execution`, and `Evidence Review`.

---

## Important Clarifications

### Is the Python Runner Required?
**No.** There is a Python runner located in `aos/tools/optional/problem-intake-runner/`, but it is completely optional. It exists for advanced, guided execution in local environments. The markdown-only chat workflow described above is fully functional and recommended for your first session.

### What is Approval?
AOS operates on strict fail-closed security invariants:
- **PASS ≠ Approval:** Just because an agent completes an interview or finishes a script without errors does not mean it has permission to execute code.
- **Evidence ≠ Approval:** Generating these intake documents provides *evidence* of planning, but you must still explicitly authorize the agent to act on them.
- Only a human can grant the agent permission to edit protected files, commit, push, or deploy.
