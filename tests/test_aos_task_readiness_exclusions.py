import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = PROJECT_ROOT / "aos/scripts/aos_task_document_check.py"


def build_task(task_id, **overrides):
    data = {
        "task_id": task_id,
        "title": "Fixture task",
        "type": "task",
        "template_level": "S",
        "status": "DRAFT",
        "queue_mode": "AUTO",
        "queue_position": "null",
        "queue_status": "BACKLOG",
        "queue_priority": "NORMAL",
        "risk_profile": "LOW_RISK_FAST",
        "risk_assigned_by": "human",
        "approval_status": "APPROVED",
        "human_checkpoint_required": "true",
        "validator_status": "VALIDATION_COMPLETE",
        "evidence_status": "EVIDENCE_COLLECTED",
        "log_uri": f".aos-tmp/tasks/{task_id}/agent-actions.log",
        "log_status": "NOT_STARTED",
        "owner": "human",
        "created_at": "2026-07-08",
        "updated_at": "2026-07-08",
    }
    data.update(overrides)

    lines = ["---"]
    for key, value in data.items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif value == "null":
            rendered = "null"
        elif isinstance(value, int):
            rendered = str(value)
        else:
            rendered = f"\"{value}\""
        lines.append(f"{key}: {rendered}")
    lines.append("---")
    lines.append("## Задача")
    lines.append("goal")
    lines.append("")
    lines.append("## Done когда")
    lines.append("done")
    lines.append("")
    lines.append("## История")
    lines.append("history")
    lines.append("")
    lines.append("## Evidence")
    lines.append("evidence")
    lines.append("")
    lines.append("## ⛔ Решение")
    lines.append("APPROVED")
    lines.append("")
    return "\n".join(lines)


class TestAOSTaskReadinessExclusions(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.tasks_dir = Path(self.temp_dir) / "tasks"
        self.tasks_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def write_task(self, filename, content):
        (self.tasks_dir / filename).write_text(content, encoding="utf-8")

    def run_cmd(self, *args):
        return subprocess.run(
            ["python3", str(SCRIPT)] + list(args),
            cwd=self.temp_dir,
            capture_output=True,
            text=True,
        )

    def readiness_json(self):
        res = self.run_cmd("task", "--readiness-all", "--json")
        return res, json.loads(res.stdout)

    def test_rejected_task_with_explicit_witness_is_excluded_terminal_not_pass(self):
        self.write_task(
            "AOS-FARM-TASK-1001.md",
            build_task(
                "AOS-FARM-TASK-1001",
                status="REJECTED",
                readiness_exclusion_task_id="AOS-FARM-TASK-1001",
                readiness_exclusion_type="TERMINAL",
                readiness_exclusion_reason="human rejected task",
                readiness_exclusion_source_evidence="reports/human-checkpoints/example.md",
                readiness_exclusion_human_checkpoint="reports/human-checkpoints/example.md",
                readiness_exclusion_applies_to_readiness=True,
                readiness_exclusion_approval_granted=False,
                readiness_exclusion_created_in_stage="AOS-FARM.642",
                readiness_exclusion_review_required=False,
                approval_status="REJECTED",
            ),
        )
        res = self.run_cmd("task", "--readiness", "AOS-FARM-TASK-1001")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        self.assertIn("Readiness: EXCLUDED_TERMINAL", res.stdout)
        self.assertIn("EXCLUDED_TERMINAL is not PASS", res.stdout)
        self.assertNotIn("Readiness: READY_FOR_HANDOFF", res.stdout)

    def test_invalid_legacy_task_with_explicit_witness_is_excluded_legacy(self):
        self.write_task(
            "AOS-FARM.463.md",
            build_task(
                "AOS-FARM.463",
                readiness_exclusion_task_id="AOS-FARM.463",
                readiness_exclusion_type="LEGACY",
                readiness_exclusion_reason="legacy invalid task id retained for audit",
                readiness_exclusion_source_evidence="reports/human-checkpoints/example-legacy.md",
                readiness_exclusion_human_checkpoint="reports/human-checkpoints/example-legacy.md",
                readiness_exclusion_applies_to_readiness=True,
                readiness_exclusion_approval_granted=False,
                readiness_exclusion_created_in_stage="AOS-FARM.642",
                readiness_exclusion_review_required=False,
            ),
        )
        self.write_task("AOS-FARM-TASK-2000.md", build_task("AOS-FARM-TASK-2000"))
        res_validate = self.run_cmd("task", "--validate-all")
        self.assertEqual(res_validate.returncode, 0, res_validate.stderr + res_validate.stdout)
        res = self.run_cmd("task", "--readiness-all")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        self.assertIn("AOS-FARM.463 | EXCLUDED_LEGACY", res.stdout)
        self.assertIn("AOS-FARM-TASK-2000 | READY_FOR_HANDOFF", res.stdout)
        self.assertIn("excluded_legacy_count: 1", res.stdout)
        self.assertIn("EXCLUDED_LEGACY is not PASS", res.stdout)

    def test_malformed_exclusion_blocks_readiness(self):
        self.write_task(
            "AOS-FARM-TASK-1002.md",
            build_task(
                "AOS-FARM-TASK-1002",
                status="REJECTED",
                readiness_exclusion_task_id="AOS-FARM-TASK-1002",
                readiness_exclusion_type="TERMINAL",
                readiness_exclusion_reason="missing witness should fail closed",
                readiness_exclusion_source_evidence="reports/human-checkpoints/example.md",
                readiness_exclusion_human_checkpoint="HUMAN_REVIEW_REQUIRED",
                readiness_exclusion_applies_to_readiness=True,
                readiness_exclusion_approval_granted=False,
                readiness_exclusion_created_in_stage="AOS-FARM.642",
                readiness_exclusion_review_required=False,
                approval_status="REJECTED",
            ),
        )
        res = self.run_cmd("task", "--readiness-all")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("AOS-FARM-TASK-1002 | MALFORMED_EXCLUSION", res.stdout)
        self.assertIn("malformed_exclusion_count: 1", res.stdout)
        self.assertIn("MALFORMED_EXCLUSION is blocker state", res.stdout)

    def test_readiness_json_includes_typed_gate_provenance(self):
        self.write_task("AOS-FARM-TASK-2100.md", build_task("AOS-FARM-TASK-2100"))
        res, data = self.readiness_json()
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        entry = data["tasks"][0]

        self.assertIn("gate_provenance", entry)
        self.assertIn("authorization_boundary", entry)
        self.assertEqual(
            set(entry["gate_provenance"].keys()),
            {
                "risk_profile_status",
                "risk_profile_assigned_by",
                "human_witness_status",
                "validation_status",
                "evidence_status",
                "approval_status",
                "has_blocking_unknown",
                "has_required_human_review",
            },
        )
        self.assertEqual(
            set(entry["authorization_boundary"].keys()),
            {
                "handoff_allowed",
                "execution_authorized",
                "commit_authorized",
                "push_authorized",
                "merge_authorized",
                "release_authorized",
            },
        )

    def test_readiness_json_includes_status_taxonomy_fields(self):
        self.write_task("AOS-FARM-TASK-2110.md", build_task("AOS-FARM-TASK-2110"))
        res, data = self.readiness_json()
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        entry = data["tasks"][0]

        for key in [
            "raw_status",
            "raw_readiness",
            "raw_exit_code",
            "structural_status",
            "semantic_status",
            "effective_status",
            "process_exit_status",
            "exit_code",
            "normalization_reason",
        ]:
            self.assertIn(key, entry)
        self.assertEqual(entry["raw_status"], "READY_FOR_HANDOFF")
        self.assertEqual(entry["raw_readiness"], "READY_FOR_HANDOFF")
        self.assertEqual(entry["structural_status"], "PASS")
        self.assertEqual(entry["semantic_status"], "PASS")
        self.assertEqual(entry["effective_status"], "PASS")
        self.assertEqual(entry["process_exit_status"], "NOT_RUN")
        self.assertIsNone(entry["exit_code"])
        self.assertFalse(entry["authorization_boundary"]["execution_authorized"])

    def test_semantic_human_review_required_is_not_generic_fail(self):
        self.write_task(
            "AOS-FARM-TASK-2111.md",
            build_task("AOS-FARM-TASK-2111", validator_status="NOT_RUN", approval_status="NOT_APPROVED"),
        )
        res, data = self.readiness_json()
        self.assertNotEqual(res.returncode, 0)
        self.assertEqual(data["status"], "HUMAN_REVIEW_REQUIRED")
        entry = data["active_blockers"][0]

        self.assertEqual(entry["raw_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(entry["structural_status"], "PASS")
        self.assertEqual(entry["semantic_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(entry["effective_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertNotEqual(entry["effective_status"], "PASS")
        self.assertEqual(entry["primary_blocker_category"], "not_run_required_check")
        categories = {item["category"] for item in entry["blocker_categories"]}
        self.assertIn("not_run_required_check", categories)
        self.assertIn("requires_validation_run", categories)
        self.assertIn("human_review_required", categories)
        self.assertEqual(entry["next_required_action"], "requires human decision; not resolved by agent")

    def test_ready_raw_status_can_normalize_to_semantic_human_review(self):
        self.write_task(
            "AOS-FARM-TASK-2112.md",
            build_task(
                "AOS-FARM-TASK-2112",
                validator_status="PENDING",
                evidence_status="EVIDENCE_COLLECTED",
            ),
        )
        res, data = self.readiness_json()
        self.assertNotEqual(res.returncode, 0)
        entry = data["active_blockers"][0]

        self.assertEqual(entry["raw_status"], "READY_FOR_HANDOFF")
        self.assertEqual(entry["raw_readiness"], "READY_FOR_HANDOFF")
        self.assertEqual(entry["structural_status"], "PASS")
        self.assertEqual(entry["semantic_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(entry["effective_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertIn("required validation/Evidence/approval boundary", entry["normalization_reason"])
        categories = {item["category"] for item in entry["blocker_categories"]}
        self.assertIn("not_run_required_check", categories)

    def test_structural_fail_remains_fail_not_human_review_required(self):
        self.write_task("AOS-FARM-TASK-2113.md", "---\ntask_id: \"AOS-FARM-TASK-2113\"\n---\n")
        res, data = self.readiness_json()
        self.assertNotEqual(res.returncode, 0)
        entry = data["active_blockers"][0]

        self.assertEqual(entry["raw_status"], "BLOCKED")
        self.assertEqual(entry["structural_status"], "FAIL")
        self.assertEqual(entry["semantic_status"], "BLOCKED")
        self.assertEqual(entry["effective_status"], "BLOCKED")
        self.assertNotEqual(entry["semantic_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(entry["primary_blocker_category"], "true_structural_failure")
        categories = {item["category"] for item in entry["blocker_categories"]}
        self.assertIn("requires_task_doc_fix", categories)

    def test_malformed_exclusion_is_unknown_not_human_review_required(self):
        self.write_task(
            "AOS-FARM-TASK-2114.md",
            build_task(
                "AOS-FARM-TASK-2114",
                status="REJECTED",
                readiness_exclusion_task_id="AOS-FARM-TASK-2114",
                readiness_exclusion_type="TERMINAL",
                readiness_exclusion_reason="missing witness should fail closed",
                readiness_exclusion_source_evidence="reports/human-checkpoints/example.md",
                readiness_exclusion_human_checkpoint="HUMAN_REVIEW_REQUIRED",
                readiness_exclusion_applies_to_readiness=True,
                readiness_exclusion_approval_granted=False,
                readiness_exclusion_created_in_stage="AOS-FARM.648",
                readiness_exclusion_review_required=False,
                approval_status="REJECTED",
            ),
        )
        res, data = self.readiness_json()
        self.assertNotEqual(res.returncode, 0)
        entry = data["malformed_exclusions"][0]

        self.assertEqual(entry["raw_status"], "MALFORMED_EXCLUSION")
        self.assertEqual(entry["structural_status"], "UNKNOWN_BLOCKED")
        self.assertEqual(entry["semantic_status"], "UNKNOWN_BLOCKED")
        self.assertEqual(entry["effective_status"], "UNKNOWN_BLOCKED")
        self.assertNotEqual(entry["semantic_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(entry["primary_blocker_category"], "malformed_or_unparseable_status")

    def test_readiness_inventory_and_resolution_boundary_are_reported(self):
        self.write_task(
            "AOS-FARM-TASK-2115.md",
            build_task("AOS-FARM-TASK-2115", validator_status="NOT_RUN"),
        )
        self.write_task("AOS-FARM-TASK-2116.md", build_task("AOS-FARM-TASK-2116"))
        res, data = self.readiness_json()
        self.assertNotEqual(res.returncode, 0)

        inventory = data["readiness_inventory"]
        self.assertEqual(inventory["active_ready_count"], 1)
        self.assertEqual(inventory["active_human_review_required_count"], 1)
        self.assertEqual(inventory["active_unknown_blocked_count"], 0)
        self.assertEqual(inventory["active_structural_fail_count"], 0)
        self.assertIn("blocker_resolution_boundary", data)
        self.assertTrue(all(value == "none" for value in data["blocker_resolution_boundary"].values()))

    def test_readiness_json_authorization_booleans_default_false(self):
        self.write_task("AOS-FARM-TASK-2101.md", build_task("AOS-FARM-TASK-2101"))
        res, data = self.readiness_json()
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        boundary = data["tasks"][0]["authorization_boundary"]

        self.assertTrue(boundary["handoff_allowed"])
        self.assertFalse(boundary["execution_authorized"])
        self.assertFalse(boundary["commit_authorized"])
        self.assertFalse(boundary["push_authorized"])
        self.assertFalse(boundary["merge_authorized"])
        self.assertFalse(boundary["release_authorized"])

    def test_missing_risk_profile_does_not_authorize_execution(self):
        self.write_task(
            "AOS-FARM-TASK-2102.md",
            build_task("AOS-FARM-TASK-2102", risk_profile=""),
        )
        res, data = self.readiness_json()
        self.assertNotEqual(res.returncode, 0)
        entry = data["tasks"][0]

        self.assertEqual(entry["readiness"], "BLOCKED")
        self.assertEqual(entry["gate_provenance"]["risk_profile_status"], "missing")
        self.assertFalse(entry["authorization_boundary"]["execution_authorized"])

    def test_missing_human_witness_does_not_authorize_execution_when_required(self):
        self.write_task(
            "AOS-FARM-TASK-2103.md",
            build_task("AOS-FARM-TASK-2103", risk_assigned_by="none"),
        )
        res, data = self.readiness_json()
        self.assertNotEqual(res.returncode, 0)
        entry = data["tasks"][0]

        self.assertEqual(entry["readiness"], "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(entry["gate_provenance"]["human_witness_status"], "missing")
        self.assertTrue(entry["gate_provenance"]["has_required_human_review"])
        self.assertFalse(entry["authorization_boundary"]["execution_authorized"])

    def test_not_run_is_represented_as_not_run_not_pass(self):
        self.write_task(
            "AOS-FARM-TASK-2104.md",
            build_task("AOS-FARM-TASK-2104", validator_status="NOT_RUN"),
        )
        res, data = self.readiness_json()
        self.assertNotEqual(res.returncode, 0)
        provenance = data["tasks"][0]["gate_provenance"]

        self.assertEqual(provenance["validation_status"], "NOT_RUN")
        self.assertNotEqual(provenance["validation_status"], "PASS")
        self.assertTrue(provenance["has_required_human_review"])

    def test_unknown_is_represented_as_blocking(self):
        self.write_task(
            "AOS-FARM-TASK-2105.md",
            build_task("AOS-FARM-TASK-2105", risk_profile="UNKNOWN_BLOCKED"),
        )
        res, data = self.readiness_json()
        self.assertNotEqual(res.returncode, 0)
        provenance = data["tasks"][0]["gate_provenance"]

        self.assertEqual(provenance["risk_profile_status"], "unknown")
        self.assertTrue(provenance["has_blocking_unknown"])
        self.assertFalse(data["tasks"][0]["authorization_boundary"]["execution_authorized"])

    def test_human_review_required_remains_non_pass(self):
        self.write_task(
            "AOS-FARM-TASK-2106.md",
            build_task("AOS-FARM-TASK-2106", evidence_status="NOT_RUN"),
        )
        res, data = self.readiness_json()
        self.assertNotEqual(res.returncode, 0)
        entry = data["tasks"][0]

        self.assertEqual(entry["readiness"], "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(entry["gate_provenance"]["evidence_status"], "missing")
        self.assertTrue(entry["gate_provenance"]["has_required_human_review"])
        self.assertNotEqual(entry["readiness"], "PASS")

    def test_closed_completed_terminal_exclusion_is_rejected_fail_closed(self):
        self.write_task(
            "AOS-FARM-TASK-1007.md",
            build_task(
                "AOS-FARM-TASK-1007",
                status="CLOSED",
                closure_type="COMPLETED",
                readiness_exclusion_task_id="AOS-FARM-TASK-1007",
                readiness_exclusion_type="TERMINAL",
                readiness_exclusion_reason="completed is not a terminal exclusion subtype",
                readiness_exclusion_source_evidence="reports/human-checkpoints/example.md",
                readiness_exclusion_human_checkpoint="reports/human-checkpoints/example.md",
                readiness_exclusion_applies_to_readiness=True,
                readiness_exclusion_approval_granted=False,
                readiness_exclusion_created_in_stage="AOS-FARM.643",
                readiness_exclusion_review_required=False,
            ),
        )
        res = self.run_cmd("task", "--readiness", "AOS-FARM-TASK-1007")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Readiness: MALFORMED_EXCLUSION", res.stdout)
        self.assertIn("CLOSED terminal exclusion requires closure_type", res.stdout)

    def test_missing_readiness_exclusion_type_fails_closed(self):
        self.write_task(
            "AOS-FARM-TASK-1008.md",
            build_task(
                "AOS-FARM-TASK-1008",
                status="REJECTED",
                readiness_exclusion_task_id="AOS-FARM-TASK-1008",
                readiness_exclusion_reason="missing type should fail closed",
                readiness_exclusion_source_evidence="reports/human-checkpoints/example.md",
                readiness_exclusion_human_checkpoint="reports/human-checkpoints/example.md",
                readiness_exclusion_applies_to_readiness=True,
                readiness_exclusion_approval_granted=False,
                readiness_exclusion_created_in_stage="AOS-FARM.644",
                readiness_exclusion_review_required=False,
                approval_status="REJECTED",
            ),
        )
        res = self.run_cmd("task", "--readiness", "AOS-FARM-TASK-1008")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Readiness: MALFORMED_EXCLUSION", res.stdout)
        self.assertIn("readiness_exclusion_type must be one of", res.stdout)

    def test_invalid_readiness_exclusion_type_fails_closed(self):
        self.write_task(
            "AOS-FARM-TASK-1009.md",
            build_task(
                "AOS-FARM-TASK-1009",
                status="REJECTED",
                readiness_exclusion_task_id="AOS-FARM-TASK-1009",
                readiness_exclusion_type="ACTIVE",
                readiness_exclusion_reason="invalid type should fail closed",
                readiness_exclusion_source_evidence="reports/human-checkpoints/example.md",
                readiness_exclusion_human_checkpoint="reports/human-checkpoints/example.md",
                readiness_exclusion_applies_to_readiness=True,
                readiness_exclusion_approval_granted=False,
                readiness_exclusion_created_in_stage="AOS-FARM.644",
                readiness_exclusion_review_required=False,
                approval_status="REJECTED",
            ),
        )
        res = self.run_cmd("task", "--readiness", "AOS-FARM-TASK-1009")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Readiness: MALFORMED_EXCLUSION", res.stdout)
        self.assertIn("readiness_exclusion_type must be one of", res.stdout)

    def test_wildcard_mass_and_blanket_exclusions_are_rejected(self):
        cases = [
            ("AOS-FARM-TASK-*", "Wildcard exclusion is forbidden"),
            ("AOS-FARM-TASK-1003,AOS-FARM-TASK-1004", "Mass or blanket exclusion is forbidden"),
            ("ALL", "Blanket exclusion is forbidden"),
        ]
        for target, reason in cases:
            with self.subTest(target=target):
                shutil.rmtree(self.tasks_dir)
                self.tasks_dir.mkdir()
                self.write_task(
                    "AOS-FARM-TASK-1003.md",
                    build_task(
                        "AOS-FARM-TASK-1003",
                        status="REJECTED",
                        readiness_exclusion_task_id=target,
                        readiness_exclusion_type="TERMINAL",
                        readiness_exclusion_reason="invalid scope",
                        readiness_exclusion_source_evidence="reports/human-checkpoints/example.md",
                        readiness_exclusion_human_checkpoint="reports/human-checkpoints/example.md",
                        readiness_exclusion_applies_to_readiness=True,
                        readiness_exclusion_approval_granted=False,
                        readiness_exclusion_created_in_stage="AOS-FARM.642",
                        readiness_exclusion_review_required=False,
                        approval_status="REJECTED",
                    ),
                )
                res = self.run_cmd("task", "--readiness", "AOS-FARM-TASK-1003")
                self.assertNotEqual(res.returncode, 0)
                self.assertIn("MALFORMED_EXCLUSION", res.stdout)
                self.assertIn(reason, res.stdout)

    def test_closed_and_rejected_alone_are_not_escape_hatches(self):
        self.write_task(
            "AOS-FARM-TASK-1004.md",
            build_task("AOS-FARM-TASK-1004", status="CLOSED", approval_status="NOT_APPROVED"),
        )
        self.write_task(
            "AOS-FARM-TASK-1005.md",
            build_task("AOS-FARM-TASK-1005", status="REJECTED", approval_status="REJECTED"),
        )
        res = self.run_cmd("task", "--readiness-all")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("AOS-FARM-TASK-1004 | BLOCKED", res.stdout)
        self.assertIn("AOS-FARM-TASK-1005 | BLOCKED", res.stdout)
        self.assertNotIn("AOS-FARM-TASK-1004 | EXCLUDED_TERMINAL", res.stdout)
        self.assertNotIn("AOS-FARM-TASK-1005 | EXCLUDED_TERMINAL", res.stdout)

    def test_invalid_task_id_without_witness_stays_blocked(self):
        self.write_task("AOS-FARM.463.md", build_task("AOS-FARM.463"))
        res = self.run_cmd("task", "--readiness", "AOS-FARM.463")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Invalid task_id format: AOS-FARM.463", res.stdout)
        self.assertNotIn("EXCLUDED_LEGACY", res.stdout)

    def test_not_run_and_evidence_not_approval_remain_fail_closed(self):
        self.write_task(
            "AOS-FARM-TASK-1006.md",
            build_task(
                "AOS-FARM-TASK-1006",
                validator_status="NOT_RUN",
                evidence_status="EVIDENCE_COLLECTED",
                approval_status="NOT_APPROVED",
            ),
        )
        res = self.run_cmd("task", "--readiness", "AOS-FARM-TASK-1006")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("validator_status is NOT_RUN", res.stdout)
        self.assertIn("approval_status is NOT_APPROVED", res.stdout)

    def test_missing_risk_profile_stays_fail_closed(self):
        self.write_task(
            "AOS-FARM-TASK-1010.md",
            build_task("AOS-FARM-TASK-1010", risk_profile=""),
        )
        res = self.run_cmd("task", "--readiness", "AOS-FARM-TASK-1010")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Readiness: BLOCKED", res.stdout)
        self.assertIn("risk_profile is missing", res.stdout)

    def test_agent_assigned_risk_profile_does_not_satisfy_human_assignment(self):
        self.write_task(
            "AOS-FARM-TASK-1011.md",
            build_task(
                "AOS-FARM-TASK-1011",
                risk_profile="HIGH_RISK_PROTECTED",
                risk_assigned_by="agent",
            ),
        )
        res = self.run_cmd("task", "--readiness", "AOS-FARM-TASK-1011")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Readiness: BLOCKED", res.stdout)
        self.assertIn("risk_assigned_by: agent is forbidden (agent/self)", res.stdout)

    def test_missing_human_witness_field_fails_closed(self):
        self.write_task(
            "AOS-FARM-TASK-1012.md",
            build_task(
                "AOS-FARM-TASK-1012",
                status="REJECTED",
                readiness_exclusion_task_id="AOS-FARM-TASK-1012",
                readiness_exclusion_type="TERMINAL",
                readiness_exclusion_reason="missing checkpoint should fail closed",
                readiness_exclusion_source_evidence="reports/human-checkpoints/example.md",
                readiness_exclusion_applies_to_readiness=True,
                readiness_exclusion_approval_granted=False,
                readiness_exclusion_created_in_stage="AOS-FARM.644",
                readiness_exclusion_review_required=False,
                approval_status="REJECTED",
            ),
        )
        res = self.run_cmd("task", "--readiness", "AOS-FARM-TASK-1012")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Readiness: MALFORMED_EXCLUSION", res.stdout)
        self.assertIn("Missing exclusion witness fields", res.stdout)

    def test_unknown_blocked_does_not_pass_aggregate_readiness(self):
        self.write_task("AOS-FARM-TASK-1013.md", build_task("AOS-FARM-TASK-1013", risk_profile="UNKNOWN_BLOCKED"))
        self.write_task("AOS-FARM-TASK-1014.md", build_task("AOS-FARM-TASK-1014"))
        res = self.run_cmd("task", "--readiness-all")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("AOS-FARM-TASK-1013 | BLOCKED", res.stdout)
        self.assertIn("active_blocked_count: 1", res.stdout)
        self.assertIn("AOS-FARM-TASK-1014 | READY_FOR_HANDOFF", res.stdout)

    def test_not_run_does_not_pass_aggregate_readiness(self):
        self.write_task(
            "AOS-FARM-TASK-1015.md",
            build_task("AOS-FARM-TASK-1015", validator_status="NOT_RUN"),
        )
        self.write_task("AOS-FARM-TASK-1016.md", build_task("AOS-FARM-TASK-1016"))
        res = self.run_cmd("task", "--readiness-all")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("AOS-FARM-TASK-1015 | HUMAN_REVIEW_REQUIRED", res.stdout)
        self.assertIn("active_human_review_required_count: 1", res.stdout)
        self.assertIn("AOS-FARM-TASK-1016 | READY_FOR_HANDOFF", res.stdout)


if __name__ == "__main__":
    unittest.main()
