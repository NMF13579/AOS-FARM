import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = PROJECT_ROOT / "aos/scripts/aos_lifecycle_state.py"
FIXTURES = PROJECT_ROOT / "tests/fixtures/lifecycle-state"


class TestAOSLifecycleState(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.tasks_dir = Path(self.temp_dir) / "tasks"
        self.tasks_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def copy_fixture(self, fixture_name, task_name):
        shutil.copyfile(FIXTURES / fixture_name, self.tasks_dir / task_name)

    def run_state(self, *args):
        return subprocess.run(
            ["python3", str(SCRIPT)] + list(args),
            cwd=self.temp_dir,
            capture_output=True,
            text=True,
        )

    def test_skips_done_ranked_first_and_selects_draft_candidate(self):
        self.copy_fixture("done-ranked-first.md", "AOS-FARM-TASK-0001.md")
        self.copy_fixture("draft-unknown-candidate.md", "AOS-FARM-TASK-0002.md")
        res = self.run_state("--json")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        data = json.loads(res.stdout)
        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["current_task"]["id"], "AOS-FARM-TASK-0002")
        self.assertEqual(data["current_task"]["selection_status"], "SELECTED")
        self.assertTrue(any(c["source"] == "ranked_queue" for c in data["conflicts"]))
        self.assertFalse(data["permissions"]["execution_allowed"])
        self.assertFalse(data["permissions"]["commit_allowed"])
        self.assertFalse(data["permissions"]["push_allowed"])

    def test_draft_unknown_candidate_preserves_not_run_and_missing_human_risk(self):
        self.copy_fixture("draft-unknown-candidate.md", "AOS-FARM-TASK-0002.md")
        res = self.run_state("--task", "tasks/AOS-FARM-TASK-0002.md", "--json")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        data = json.loads(res.stdout)
        self.assertEqual(data["current_task"]["id"], "AOS-FARM-TASK-0002")
        self.assertEqual(data["lifecycle"]["state"], "DRAFT")
        self.assertEqual(data["human"]["risk_profile_status"], "UNKNOWN_BLOCKED")
        self.assertEqual(data["evidence"]["validation_status"], "NOT_RUN")
        self.assertEqual(data["evidence"]["evidence_status"], "NOT_RUN")
        self.assertFalse(data["permissions"]["approval_granted"])

    def test_evidence_present_does_not_grant_approval_or_execution(self):
        self.copy_fixture("evidence-present-not-approved.md", "AOS-FARM-TASK-0003.md")
        res = self.run_state("--task", "tasks/AOS-FARM-TASK-0003.md", "--json")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        data = json.loads(res.stdout)
        self.assertEqual(data["evidence"]["evidence_status"], "PRESENT")
        self.assertEqual(data["human"]["acceptance_status"], "NOT_REVIEWED")
        self.assertFalse(data["permissions"]["approval_granted"])
        self.assertFalse(data["permissions"]["execution_allowed"])

    def test_missing_task_is_unknown_blocked(self):
        res = self.run_state("--task", "tasks/AOS-FARM-TASK-9999.md", "--json")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        data = json.loads(res.stdout)
        self.assertEqual(data["current_task"]["selection_status"], "UNKNOWN_BLOCKED")
        self.assertEqual(data["lifecycle"]["state"], "UNKNOWN_BLOCKED")
        self.assertIn("missing_task", data["lifecycle"]["blockers"])

    def test_text_explain_and_consistency_are_read_only(self):
        self.copy_fixture("draft-unknown-candidate.md", "AOS-FARM-TASK-0002.md")
        before = sorted((p.name, p.stat().st_mtime_ns) for p in self.tasks_dir.iterdir())
        text = self.run_state("--text")
        explain = self.run_state("--explain")
        consistency = self.run_state("--check-consistency")
        after = sorted((p.name, p.stat().st_mtime_ns) for p in self.tasks_dir.iterdir())
        self.assertEqual(text.returncode, 0, text.stderr + text.stdout)
        self.assertEqual(explain.returncode, 0, explain.stderr + explain.stdout)
        self.assertEqual(consistency.returncode, 0, consistency.stderr + consistency.stdout)
        self.assertEqual(before, after)
        self.assertIn("Read-only interpreter", text.stdout)
        self.assertIn("does not approve", explain.stdout)


if __name__ == "__main__":
    unittest.main()
