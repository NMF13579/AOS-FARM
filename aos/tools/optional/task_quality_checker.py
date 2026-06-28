import json

class TaskQualityChecker:
    def __init__(self, package_path):
        self.package_path = package_path
        with open(self.package_path, 'r') as f:
            self.data = json.load(f)

    def validate(self):
        # 1. Missing required fields check
        required_fields = [
            "contract_version", "package_type", "task_id", "task_title",
            "task_brief_path", "acceptance_criteria_path", "evidence_matrix_path",
            "expected_artifacts", "actual_artifacts", "changed_files",
            "validation_outputs", "known_limitations", "warnings", "blockers",
            "human_review_required", "non_authority_boundary"
        ]

        for field in required_fields:
            if field not in self.data:
                return "BLOCKED"

        # 2. non_authority_boundary logic is implicitly handled by the required fields check above

        # 3. Check human_review_required
        if self.data.get("human_review_required", True) is False:
            return "BLOCKED"

        outputs = self.data.get("validation_outputs", {})
        if outputs.get("human_review_required") is False:
            return "BLOCKED"

        # 4. Check forbidden claims
        if outputs.get("forbidden_claims_present", False):
            return "BLOCKED"

        # 5. Check NOT_RUN / UNKNOWN in validation_outputs
        for key, value in outputs.items():
            if value in ("NOT_RUN", "UNKNOWN"):
                return "BLOCKED"

        # 6. Check evidence
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
