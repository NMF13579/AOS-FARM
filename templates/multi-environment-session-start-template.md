# Multi-Environment Session Start Template

**Required Commands to Run:**
```bash
git rev-parse --abbrev-ref HEAD
git status --short
git status -sb
git rev-parse HEAD
git rev-parse origin/dev
git rev-list --count origin/dev..HEAD
git rev-list --count HEAD..origin/dev
git rev-list --left-right --count origin/dev...HEAD
ls -l 00_AOS_Core_Control.md 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md 02_AOS_Governance_Control_Module_and_Safety_Rules.md
```

## Session Start Report
- **environment:** [Antigravity / VS Code / Codex CLI / ChatGPT]
- **current_branch:** [Branch name]
- **HEAD:** [Commit SHA]
- **origin_dev:** [Commit SHA]
- **local_ahead_origin_dev_by:** [Count]
- **origin_dev_ahead_local_by:** [Count]
- **left_right_ahead_behind_summary:** [e.g., 0 0]
- **working_tree_status:** [Clean / Dirty (List staged/modified files)]
- **required_sources_available:** [true / false]
- **latest_known_task:** [Task ID]
- **next_safe_task:** [Action needed to continue safely]
- **human_action_required:** [true / false]
- **active_authorization_state:** [Execution / Commit / Push / None]
- **session_limit_risk:** [Low / High]
- **recommended_model_tier:** [Cheap / Standard / Expensive]
- **handoff_required:** [true / false]
