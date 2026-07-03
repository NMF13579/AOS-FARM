import json
import os
import shutil
import subprocess
import tempfile
import unittest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DASHBOARD_SCRIPT = os.path.join(PROJECT_ROOT, "aos/scripts/aos_queue_dashboard.py")
NEXT_SELECTION_SCRIPT = os.path.join(PROJECT_ROOT, "aos/scripts/aos_next_task_selection.py")


DONE_TASK = """---
task_id: AOS-FARM-TASK-0001
title: Done task
status: READY_FOR_EXECUTION
queue_mode: MANUAL
queue_position: 1
queue_status: DONE
risk_profile: HIGH_RISK_PROTECTED
approval_status: NOT_REQUESTED
evidence_status: PENDING
---
"""


BACKLOG_TASK = """---
task_id: AOS-FARM-TASK-0002
title: Backlog task
status: DRAFT
queue_mode: MANUAL
queue_position: 2
queue_status: BACKLOG
risk_profile: UNKNOWN_BLOCKED
approval_status: NOT_APPROVED
evidence_status: NOT_RUN
---
"""


class TestAOSLifecycleReconciliation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        os.mkdir(os.path.join(self.temp_dir, "tasks"))
        with open(os.path.join(self.temp_dir, "tasks/AOS-FARM-TASK-0001.md"), "w", encoding="utf-8") as f:
            f.write(DONE_TASK)
        with open(os.path.join(self.temp_dir, "tasks/AOS-FARM-TASK-0002.md"), "w", encoding="utf-8") as f:
            f.write(BACKLOG_TASK)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_dashboard_uses_same_next_candidate_boundary_as_queue_helper(self):
        res = subprocess.run(
            ["python3", DASHBOARD_SCRIPT, "--json"],
            cwd=self.temp_dir,
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        data = json.loads(res.stdout)
        self.assertEqual(data["next_candidate"], "AOS-FARM-TASK-0002")
        self.assertNotEqual(data["next_candidate"], "AOS-FARM-TASK-0001")
        self.assertIn("NEXT != approval", data["boundary_note"])

    def test_next_task_selection_json_reports_read_only_reconciliation(self):
        res = subprocess.run(
            ["python3", NEXT_SELECTION_SCRIPT, "--json"],
            cwd=self.temp_dir,
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        data = json.loads(res.stdout)
        self.assertEqual(data["next_candidate"], "AOS-FARM-TASK-0002")
        self.assertEqual(data["ranked_first_task_id"], "AOS-FARM-TASK-0001")
        self.assertEqual(data["selection_status"], "RECONCILED_WITH_SKIPPED_NON_CANDIDATE")
        self.assertFalse(data["approval_claimed"])
        self.assertFalse(data["execution_authorized"])


if __name__ == "__main__":
    unittest.main()
