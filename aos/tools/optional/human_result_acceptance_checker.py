import json
import os

class HumanResultAcceptanceChecker:
    def __init__(self):
        pass

    def validate(self, decision_path: str) -> dict:
        if not os.path.exists(decision_path):
            return {
                "status": "BLOCKED",
                "reason": f"Decision file not found: {decision_path}"
            }

        try:
            with open(decision_path, "r", encoding="utf-8") as f:
                decision = json.load(f)
        except json.JSONDecodeError:
            return {
                "status": "BLOCKED",
                "reason": "Invalid JSON in decision file."
            }

        return self._validate_data(decision)

    def _validate_data(self, decision: dict) -> dict:
        # Check all required fields
        required_fields = [
            "task_id", "task_title", "task_quality_package_path",
            "task_quality_result_path", "task_quality_status",
            "acceptance_summary_path", "human_decision", "human_decision_reason",
            "result_accepted_by_human", "human_acknowledges_known_limits",
            "commit_authorized", "push_authorized", "merge_authorized",
            "release_authorized", "next_task_started", "lifecycle_mutation_authorized"
        ]

        for field in required_fields:
            if field not in decision:
                return {"status": "BLOCKED", "reason": f"missing required field: {field}"}

        human_decision = decision.get("human_decision")
        if human_decision not in ["ACCEPT_RESULT", "NEEDS_CHANGES", "REJECT_RESULT"]:
            return {"status": "BLOCKED", "reason": "unknown human_decision"}

        # Forbidden boundaries
        for field in [
            "commit_authorized", "push_authorized", "merge_authorized",
            "release_authorized", "next_task_started", "lifecycle_mutation_authorized",
            "auto_approval_claim", "auto_closure_claim"
        ]:
            if decision.get(field) is True:
                return {"status": "BLOCKED", "reason": f"{field} is true"}

        if human_decision == "ACCEPT_RESULT":
            if decision.get("result_accepted_by_human") is not True:
                return {"status": "BLOCKED", "reason": "ACCEPT_RESULT without result_accepted_by_human: true"}

            tq_status = decision.get("task_quality_status")
            if tq_status == "BLOCKED":
                return {"status": "BLOCKED", "reason": "ACCEPT_RESULT with BLOCKED Task Quality status"}

            # Check for UNKNOWN or NOT_RUN in stringified decision
            decision_str = str(decision)
            if "UNKNOWN" in decision_str:
                return {"status": "BLOCKED", "reason": "ACCEPT_RESULT with UNKNOWN required fields"}

            if "NOT_RUN" in decision_str:
                return {"status": "BLOCKED", "reason": "ACCEPT_RESULT with NOT_RUN required checks"}

            if tq_status == "NOT_ENOUGH_EVIDENCE":
                if decision.get("human_acknowledges_known_limits") is True:
                    return {"status": "PASS_WITH_WARNINGS", "reason": "ACCEPT_RESULT with NOT_ENOUGH_EVIDENCE and explicit acknowledgement"}
                else:
                    return {"status": "BLOCKED", "reason": "ACCEPT_RESULT with NOT_ENOUGH_EVIDENCE but without acknowledgement"}

            if tq_status == "PASS_WITH_WARNINGS":
                return {"status": "PASS_WITH_WARNINGS", "reason": "Task quality passed with warnings"}

            return {"status": "PASS", "reason": "Result accepted successfully."}

        elif human_decision == "NEEDS_CHANGES":
            if not decision.get("follow_up_task_candidate"):
                return {"status": "BLOCKED", "reason": "NEEDS_CHANGES without follow_up_task_candidate"}
            return {"status": "PASS", "reason": "Follow-up required correctly configured."}

        elif human_decision == "REJECT_RESULT":
            if not decision.get("human_decision_reason"):
                return {"status": "BLOCKED", "reason": "REJECT_RESULT without human_decision_reason"}
            return {"status": "PASS", "reason": "Result rejected with reason."}

        return {"status": "NOT_ENOUGH_EVIDENCE", "reason": "Unhandled state"}
