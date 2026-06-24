# Commit & Push Approval Workflow

In AOS-FARM, saving work (Commit) and sending work to the main repository (Push) are high-risk actions. They are separated by explicit human checkpoints to prevent accidents.

## Why Commit Requires Authorization
A commit permanently records changes in the local history. Before a commit happens, the agent must present a "Candidate Set" (the exact list of files to be saved) and a proposed commit message. 
- You must review the Candidate Set to ensure the agent didn't sneak in unauthorized changes.
- If you approve, you update the `commit-authorization` checkpoint.

## Why Push Requires Separate Authorization
A push sends your local commits to the remote shared repository (e.g., GitHub). This affects the remote baseline that other users or systems rely on.
- Commit ≠ Push. You might commit locally multiple times but only push once.
- Push ≠ Release. Pushing to a `dev` branch doesn't mean the code is running in production.
- **Evidence does not authorize a push.** Even if the agent provides a perfect report showing local success, it must explicitly ask for Push Authorization.

## What a Human Checkpoint Does
A human checkpoint is a specific Markdown file (located in `reports/human-checkpoints/`). It has explicit fields like `checkpoint_status: PENDING` and `commit_authorized: false`. 
The agent stops and waits for you to manually open this file and change the text to `true` and `APPROVED_FOR_COMMIT`.

## Examples of the Flow
- **Scenario 1**: The agent writes code, runs tests, and says "All tests PASS". 
  - *Result*: The agent stops. It prepares a commit package and waits. PASS but no approval → stop.
- **Scenario 2**: The agent gives you a 5-page report (Evidence) proving the feature works. 
  - *Result*: The agent stops. Evidence exists but no approval → stop.
- **Scenario 3**: You authorize the commit. The agent creates the commit.
  - *Result*: The agent stops again. Commit created but push not authorized → stop.
- **Scenario 4**: You are away from the keyboard. 
  - *Result*: The agent marks its status as `HUMAN_REVIEW_REQUIRED` and goes idle.
