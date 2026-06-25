# Optional Problem Intake Runner

This directory contains the *optional* Python runner for the Problem Intake and Technical Assignment methodology.

**Important Safety and Usage Notes:**
1. **Not Required**: The AOS Consumer Kit does not require you to run these scripts. The entire methodology can be executed manually by passing the prompts and runbooks (in `aos/docs/methodology/problem-intake/runbooks/`) to an LLM of your choice.
2. **Read-Only / Local Only**: This runner does not commit, push, or execute changes against your repository. It only generates drafts for human review.
3. **No Approval Authority**: Evidence ≠ approval. Generating a successful `Problem Intake Summary` using this runner does not grant the agent permission to implement it.
4. **Markdown Dependency**: This runner reads its state logic and algorithms directly from the Markdown runbooks in `aos/docs/methodology/`.

## Usage
`python problem_intake_runner.py`
