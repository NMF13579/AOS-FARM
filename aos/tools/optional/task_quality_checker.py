import json

class TaskQualityChecker:
    def __init__(self, package_path):
        self.package_path = package_path
        with open(self.package_path, 'r') as f:
            self.data = json.load(f)

    def validate(self):
        try:
            outputs = self.data.get("validation_outputs", {})
        except Exception:
            return "BLOCKED"
            
        if outputs.get("forbidden_claims_present", False):
            return "BLOCKED"
            
        if outputs.get("human_review_required", True) is False:
            return "BLOCKED"
            
        for key, value in outputs.items():
            if value in ("NOT_RUN", "UNKNOWN"):
                return "BLOCKED"

        criteria = self.data.get("acceptance_criteria", [])
        evidence_list = self.data.get("evidence", [])
        evidence_map = {e["criterion_id"]: e for e in evidence_list}

        warnings = False

        for crit in criteria:
            cid = crit["id"]
            is_req = crit.get("required", False)
            ev = evidence_map.get(cid)
            
            if not ev:
                if is_req:
                    return "BLOCKED"
                else:
                    return "NOT_ENOUGH_EVIDENCE"
            
            st = ev.get("status")
            if st in ("WARNING", "PASS_WITH_WARNINGS"):
                warnings = True
            elif st != "PASS":
                if is_req:
                    return "BLOCKED"
                else:
                    return "NOT_ENOUGH_EVIDENCE"

        if warnings:
            return "PASS_WITH_WARNINGS"
            
        return "PASS"
