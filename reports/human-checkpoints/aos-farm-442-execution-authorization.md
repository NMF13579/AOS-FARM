checkpoint_id: AOS-FARM.442-EXECUTION-AUTHORIZATION
task_id: AOS-FARM.442
task_title: Task Registry and Queue Contract MVP
branch: build/task-registry-queue-contract-mvp
human_decision: APPROVED_FOR_EXECUTION
risk_profile_assigned_by_human: true
risk_profile: HIGH_RISK_PROTECTED
execution_authorized_by_human: true
execution_authorized: true
allowed_scope:
  - Task Registry contract
  - Task Queue contract
  - Workflow / State Machine contract
  - templates
  - examples
  - read-only validator
  - read-only inspection CLI
  - tests
  - dogfood
  - reports
  - future SQLite/RAG-light compatibility fields only
forbidden_scope:
  - runner
  - auto execution
  - auto approval
  - agent Risk Profile assignment
  - commit automation
  - push automation
  - lifecycle mutation without rule
  - protected/canonical source changes
  - agentos/**
  - .github/**
  - release/**
  - SQLite implementation
  - RAG-light implementation
  - dirty boundary cleanup
  - AOS-FARM.441 closure report commit
implementation_started: false
commit_authorized: false
push_authorized: false
next_allowed_step: AOS-FARM.442.5 Registry and Queue Contract Docs
final_status: APPROVED_FOR_EXECUTION
