from typing import Callable, Any, Dict

class SnapshotStabilizer:
    def __init__(self, collector: Any, compare_anchors_func: Callable):
        self.collector = collector
        self.compare_anchors = compare_anchors_func
        self.maximum_attempts = 2

    def stabilize(self) -> Dict[str, Any]:
        result = {
            "schema_version": 1,
            "maximum_attempts": self.maximum_attempts,
            "attempts_used": 0,
            "first_comparison": None,
            "second_comparison": None
        }

        def execute_attempt():
            try:
                first_anchor = self.collector.collect_anchor()
                full_snapshot = self.collector.collect_full_snapshot()
                revalidation_anchor = self.collector.collect_anchor()
            except Exception:
                return None, None, None, {"stable": False, "technical_status": "UNKNOWN", "reason_code": "SNAPSHOT_COLLECTION_UNAVAILABLE"}

            comparison = self.compare_anchors(first_anchor, revalidation_anchor)
            return first_anchor, full_snapshot, revalidation_anchor, comparison

        # ATTEMPT 1
        result["attempts_used"] = 1
        _, full_snapshot, _, comp1 = execute_attempt()
        result["first_comparison"] = comp1

        if comp1.get("stable"):
            result["snapshot_status"] = "STABLE"
            result["technical_status"] = "PASS"
            result["control_status"] = "HUMAN_REVIEW_REQUIRED"
            result["reason_code"] = None
            result["stable_snapshot"] = full_snapshot
            return result

        if comp1.get("technical_status") == "UNKNOWN":
            result["snapshot_status"] = "UNSTABLE"
            result["technical_status"] = "UNKNOWN"
            result["control_status"] = "UNKNOWN_BLOCKED"
            result["reason_code"] = comp1.get("reason_code")
            return result

        # ATTEMPT 2
        result["attempts_used"] = 2
        _, full_snapshot2, _, comp2 = execute_attempt()
        result["second_comparison"] = comp2

        if comp2.get("stable"):
            result["snapshot_status"] = "STABLE_AFTER_RETRY"
            result["technical_status"] = "PASS"
            result["control_status"] = "HUMAN_REVIEW_REQUIRED"
            result["reason_code"] = None
            result["stable_snapshot"] = full_snapshot2
            return result

        if comp2.get("technical_status") == "UNKNOWN":
            result["snapshot_status"] = "UNSTABLE"
            result["technical_status"] = "UNKNOWN"
            result["control_status"] = "UNKNOWN_BLOCKED"
            result["reason_code"] = comp2.get("reason_code")
            return result

        # Unstable twice
        result["snapshot_status"] = "UNSTABLE"
        result["technical_status"] = "FAIL"
        result["control_status"] = "BLOCKED"
        result["reason_code"] = "LIVE_STATE_UNSTABLE"
        return result
