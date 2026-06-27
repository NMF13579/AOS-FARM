import unittest
import os
import sys
import json
import subprocess
import shutil
import tempfile
from pathlib import Path

# Setup paths
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from aos.tools.optional import task_registry_validator

VALID_REGISTRY = """
schema_version: 1
tasks:
  - task_id: AOS-FARM.100
    title: Task 100
    registry_status: CLOSED
    execution_authorized: true
  - task_id: AOS-FARM.101
    title: Task 101
    registry_status: SELECTED
    depends_on:
      - AOS-FARM.100
    execution_authorized: true
    risk_profile_assigned_by_human: true
    risk_profile: HIGH
  - task_id: AOS-FARM.102
    title: Task 102
    registry_status: QUEUED
    execution_authorized: false
  - task_id: AOS-FARM.103
    title: Blocked Task
    registry_status: BLOCKED
    execution_authorized: false
  - task_id: AOS-FARM.104
    title: Deferred Task
    registry_status: DEFERRED
    execution_authorized: false
  - task_id: AOS-FARM.105
    title: Replaced Task
    registry_status: REPLACED
    execution_authorized: false
"""

VALID_QUEUE = """
schema_version: 1
queue_revision: 2026-01-01
queue_items:
  - queue_item_id: Q1
    queue_order: "001"
    task_id: AOS-FARM.101
  - queue_item_id: Q2
    queue_order: "002"
    task_id: AOS-FARM.102
  - queue_item_id: Q3
    queue_order: "003"
    task_id: AOS-FARM.103
  - queue_item_id: Q4
    queue_order: "004"
    task_id: AOS-FARM.104
  - queue_item_id: Q5
    queue_order: "005"
    task_id: AOS-FARM.105
"""

class TestValidator(unittest.TestCase):
    def test_valid_pass(self):
        res = task_registry_validator.validate_registry_queue(VALID_REGISTRY, VALID_QUEUE)
        self.assertTrue(res["ok"])
        self.assertEqual(res["final_status"], "PASS")

    def test_duplicate_task_id(self):
        reg = VALID_REGISTRY + "\n  - task_id: AOS-FARM.101\n"
        res = task_registry_validator.validate_registry_queue(reg, VALID_QUEUE)
        self.assertFalse(res["ok"])
        self.assertEqual(res["final_status"], "BLOCKED")
        self.assertTrue(any("Duplicate task_id" in e for e in res["errors"]))

    def test_duplicate_queue_item_id(self):
        q = VALID_QUEUE + "\n  - queue_item_id: Q1\n    queue_order: 006\n    task_id: AOS-FARM.102"
        res = task_registry_validator.validate_registry_queue(VALID_REGISTRY, q)
        self.assertFalse(res["ok"])
        self.assertTrue(any("Duplicate queue_item_id" in e for e in res["errors"]))

    def test_duplicate_queue_order(self):
        q = VALID_QUEUE + "\n  - queue_item_id: Q6\n    queue_order: '001'\n    task_id: AOS-FARM.102"
        res = task_registry_validator.validate_registry_queue(VALID_REGISTRY, q)
        self.assertFalse(res["ok"])
        self.assertTrue(any("Duplicate queue_order" in e for e in res["errors"]))

    def test_queue_task_missing_in_registry(self):
        q = VALID_QUEUE + "\n  - queue_item_id: Q6\n    queue_order: '006'\n    task_id: MISSING"
        res = task_registry_validator.validate_registry_queue(VALID_REGISTRY, q)
        self.assertFalse(res["ok"])
        self.assertTrue(any("not found in registry" in e for e in res["errors"]))

    def test_dependency_missing(self):
        reg = VALID_REGISTRY + "\n  - task_id: AOS-FARM.106\n    depends_on: [MISSING]"
        res = task_registry_validator.validate_registry_queue(reg, VALID_QUEUE)
        self.assertFalse(res["ok"])
        self.assertTrue(any("depends on missing" in e for e in res["errors"]))

    def test_blocked_deferred_replaced_closed_not_selected(self):
        res = task_registry_validator.select_next_task(VALID_REGISTRY, VALID_QUEUE)
        self.assertEqual(res["task"]["task_id"], "AOS-FARM.101")

    def test_show_next_selects_first_eligible(self):
        res = task_registry_validator.select_next_task(VALID_REGISTRY, VALID_QUEUE)
        self.assertEqual(res["task"]["task_id"], "AOS-FARM.101")

    def test_ready_for_execution_without_risk_profile(self):
        reg = VALID_REGISTRY + "\n  - task_id: AOS-FARM.106\n    registry_status: READY_FOR_EXECUTION\n    execution_authorized: true\n    risk_profile_assigned_by_human: true"
        res = task_registry_validator.validate_registry_queue(reg, VALID_QUEUE)
        self.assertFalse(res["ok"])
        self.assertTrue(any("Risk Profile missing" in e for e in res["errors"]))

    def test_ready_for_execution_without_human_risk_profile(self):
        reg = VALID_REGISTRY + "\n  - task_id: AOS-FARM.106\n    registry_status: READY_FOR_EXECUTION\n    risk_profile: HIGH\n    execution_authorized: true"
        res = task_registry_validator.validate_registry_queue(reg, VALID_QUEUE)
        self.assertFalse(res["ok"])
        self.assertTrue(any("risk_profile_assigned_by_human is false" in e for e in res["errors"]))

    def test_ready_for_execution_without_execution_authorized(self):
        reg = VALID_REGISTRY + "\n  - task_id: AOS-FARM.106\n    registry_status: READY_FOR_EXECUTION\n    risk_profile: HIGH\n    risk_profile_assigned_by_human: true"
        res = task_registry_validator.validate_registry_queue(reg, VALID_QUEUE)
        self.assertFalse(res["ok"])
        self.assertTrue(any("execution_authorized is false" in e for e in res["errors"]))

    def test_pass_evidence_unknown_not_run_not_approval(self):
        reg = VALID_REGISTRY + "\n  - task_id: AOS-FARM.106\n    final_status: PASS\n    execution_authorized: true"
        res = task_registry_validator.validate_registry_queue(reg, VALID_QUEUE)
        self.assertTrue(any("does not imply approval" in w for w in res["warnings"]))

    def test_metadata_no_authority(self):
        reg = VALID_REGISTRY + "\n  - task_id: AOS-FARM.106\n    source_hash: XYZ\n    indexed_at: 2026\n    registry_status: CANDIDATE\n    execution_authorized: false"
        res = task_registry_validator.validate_registry_queue(reg, VALID_QUEUE)
        self.assertTrue(res["ok"])


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.cli_path = project_root / "aos" / "scripts" / "aos_tasks.py"
        self.reg_path = project_root / "aos" / "reports" / "examples" / "task-registry" / "task-registry-example.md"
        self.queue_path = project_root / "aos" / "reports" / "examples" / "task-registry" / "task-queue-example.md"

    def test_no_mutation(self):
        reg_stat = os.stat(self.reg_path)
        q_stat = os.stat(self.queue_path)

        cmd = [sys.executable, str(self.cli_path), "validate", "--registry", str(self.reg_path), "--queue", str(self.queue_path)]
        subprocess.run(cmd, capture_output=True, check=True)

        new_reg_stat = os.stat(self.reg_path)
        new_q_stat = os.stat(self.queue_path)
        
        self.assertEqual(reg_stat.st_mtime, new_reg_stat.st_mtime)
        self.assertEqual(q_stat.st_mtime, new_q_stat.st_mtime)
        
    def test_cli_summary(self):
        cmd = [sys.executable, str(self.cli_path), "summary", "--registry", str(self.reg_path), "--queue", str(self.queue_path)]
        res = subprocess.run(cmd, capture_output=True, check=True, text=True)
        data = json.loads(res.stdout)
        self.assertIn("total_tasks", data)
        self.assertIn("queued", data)
        
    def test_cli_show_current(self):
        cmd = [sys.executable, str(self.cli_path), "show-current", "--registry", str(self.reg_path), "--queue", str(self.queue_path)]
        res = subprocess.run(cmd, capture_output=True, check=True, text=True)
        data = json.loads(res.stdout)
        self.assertIn("selected_task_id", data)
        
    def test_cli_show_next(self):
        cmd = [sys.executable, str(self.cli_path), "show-next", "--registry", str(self.reg_path), "--queue", str(self.queue_path)]
        res = subprocess.run(cmd, capture_output=True, check=True, text=True)
        data = json.loads(res.stdout)
        self.assertIn("selected_task_id", data)

if __name__ == "__main__":
    unittest.main()
