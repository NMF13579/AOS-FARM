# Deferred Commit & Push Strategy

AOS decouples task execution from git lifecycle events.

## Execution is Local
When an agent completes a task, it leaves the files in the local worktree (untracked or modified). It does not automatically stage or commit them.

## Commit Authorization
Multiple local tasks can be batched together. Once a logical milestone is reached, a specific Commit Authorization Checkpoint is prepared. The human reviews the overall diff and authorizes the commit.

## Push Authorization
Similarly, pushing to a remote repository is a separate authorized event, preventing accidental deployment of unverified AI-generated code.
