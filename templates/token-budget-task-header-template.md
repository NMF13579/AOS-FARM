# Token-Budget Task Header

- **task_size:** [small | medium | large]
- **preferred_model_tier:** [cheap | standard | expensive]
- **escalation_model_tier:** [standard | expensive]
- **context_policy:** [exact_files_only | bounded_source_pack | broad_review]
- **max_context_behavior:** [Drop old logs / Summarize / Stop]
- **stop_before_limit:** `true`
- **handoff_required_if_interrupted:** `true`
- **do_not_start_commit_if_near_limit:** `true`
- **do_not_start_push_if_near_limit:** `true`

**expensive_model_required_if:**
- protected/canonical changes requested
- Governance / Control Module interpretation needed
- validator/runtime/CI design required
- approval boundary ambiguity detected
- source conflict encountered
- UNKNOWN / NOT_RUN / PASS semantics resolution required
