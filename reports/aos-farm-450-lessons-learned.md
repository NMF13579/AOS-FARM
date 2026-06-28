# AOS-FARM.450 Lessons Learned

* Explicit fields in JSON (e.g., `approval_required`, `commit_authorized: false`) are highly effective at making safety boundaries undeniable for consuming agents.
* Reusing the same underlying dictionary structure across subcommands while selectively overriding the `candidate_only` or similar fields simplifies maintaining invariants.
