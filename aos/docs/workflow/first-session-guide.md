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
- **Format it:** Ensure it matches the structure found in `aos/templates/task-briefs/problem-intake-template.md`. Save this locally (e.g., `problem-intake-summary.md`).
- **Safety Note:** This document is just evidence. It is **not** an approval to begin writing code.

### 3. Build the Technical Assignment
Now that the problem is defined, you must translate it into technical boundaries.
- **Copy this prompt:** Open `aos/prompts/technical-assignment-builder.md` and copy its contents.
- **Paste it with context:** Paste the prompt into your agent, along with the `problem-intake-summary.md` you saved in Step 2.
- **What happens:** The agent will define strict boundaries. It will explicitly list what is **in-scope**, what is **out-of-scope**, and exactly which files will be modified.
- **Save the output:** Capture this output into a document based on `aos/templates/task-briefs/technical-assignment-template.md`.

### 4. Proceed to Execution
With a bounded Technical Assignment in hand, you are now ready to create a `controlled-task-brief` and authorize the agent to begin actual implementation.

---

## Important Clarifications

### Is the Python Runner Required?
**No.** There is a Python runner located in `aos/tools/optional/problem-intake-runner/`, but it is completely optional. It exists for advanced, guided execution in local environments. The markdown-only chat workflow described above is fully functional and recommended for your first session.

### What is Approval?
AOS operates on strict fail-closed security invariants:
- **PASS ≠ Approval:** Just because an agent completes an interview or finishes a script without errors does not mean it has permission to execute code.
- **Evidence ≠ Approval:** Generating these intake documents provides *evidence* of planning, but you must still explicitly authorize the agent to act on them.
- Only a human can grant the agent permission to edit protected files, commit, push, or deploy.
