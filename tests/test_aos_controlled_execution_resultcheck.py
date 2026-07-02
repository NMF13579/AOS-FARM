import unittest
import json
import tempfile
from pathlib import Path
import shutil

from aos.tools.optional.controlled_execution_guard import (
    resultcheck,
    GuardResult,
    RESULT_VERIFICATION_READY_FOR_HUMAN_REVIEW,
    RESULT_VERIFICATION_READY_WITH_LIMITATIONS,
    RESULT_VERIFICATION_NOT_READY,
    RESULT_VERIFICATION_BLOCKED,
    UNKNOWN_BLOCKED
)

class TestControlledExecutionResultCheck(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="aos_resultcheck_test_")
        self.temp_path = Path(self.temp_dir)
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        
    def write_json(self, name: str, data: dict) -> Path:
        p = self.temp_path / name
        p.write_text(json.dumps(data))
        return p
        
    def create_clean_session_record(self, overrides=None):
        data = {
            "task_id": "TASK-123",
            "request_id": "REQ-123",
            "preconditions_id": "PRE-123",
            "boundary_id": "BOUND-123",
            "handoff_to_result_verification_required": True
        }
        if overrides:
            data.update(overrides)
        return self.write_json("session_record.json", data)
        
    def create_clean_result_package(self, overrides=None):
        data = {
            "task_id": "TASK-123",
            "request_id": "REQ-123",
            "boundary_id": "BOUND-123",
            "result_package_id": "RES-123",
            "changed_files": ["foo.py"],
            "commands_run": ["echo 1"],
            "validation_results": {"tests": "pass"},
            "not_run": [],
            "known_unknowns": [],
            "blockers": [],
            "evidence_summary": "All good",
            "human_review_required": True,
            "approval_status": "PENDING_HUMAN_REVIEW"
        }
        if overrides:
            data.update(overrides)
        return self.write_json("result_package.json", data)

    def test_clean_result_package(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package()
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_READY_FOR_HUMAN_REVIEW)

    def test_clean_result_package_with_not_run(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package({"not_run": ["pytest"]})
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_READY_WITH_LIMITATIONS)
        self.assertIn("pytest", res.not_run_items)

    def test_missing_session_record(self):
        rp = self.create_clean_result_package()
        res = resultcheck("does-not-exist.json", rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_BLOCKED)
        self.assertIn("not found", res.blocked_items[0])

    def test_missing_result_package(self):
        sr = self.create_clean_session_record()
        res = resultcheck(sr, "does-not-exist.json", project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_BLOCKED)
        self.assertIn("not found", res.blocked_items[0])

    def test_malformed_json(self):
        sr = self.create_clean_session_record()
        p = self.temp_path / "bad.json"
        p.write_text("{bad json")
        res = resultcheck(sr, p, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, UNKNOWN_BLOCKED)
        self.assertIn("malformed", res.unknown_items[0])

    def test_task_id_mismatch(self):
        sr = self.create_clean_session_record({"task_id": "TASK-123"})
        rp = self.create_clean_result_package({"task_id": "TASK-456"})
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_BLOCKED)
        self.assertTrue(any("task_id mismatch" in b for b in res.blocked_items))

    def test_missing_result_package_id(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package({"result_package_id": None})
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_NOT_READY)

    def test_missing_changed_files(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package()
        rp_data = json.loads(rp.read_text())
        del rp_data["changed_files"]
        rp.write_text(json.dumps(rp_data))
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_NOT_READY)

    def test_missing_validation_results(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package()
        rp_data = json.loads(rp.read_text())
        del rp_data["validation_results"]
        rp.write_text(json.dumps(rp_data))
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_NOT_READY)

    def test_known_unknowns_unresolved(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package({"known_unknowns": ["something"]})
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_NOT_READY)

    def test_blockers_non_empty(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package({"blockers": ["something"]})
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_BLOCKED)

    def test_approval_status_approved(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package({"approval_status": "APPROVED"})
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_BLOCKED)

    def test_result_verified_true(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package({"result_verified": True})
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_BLOCKED)

    def test_task_completed_true(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package({"task_completed": True})
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_BLOCKED)

    def test_ready_to_merge_raw_text(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package({"evidence_summary": "I am ready to merge this code"})
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_BLOCKED)

    def test_negative_boundary_statements_false(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package({"approval_claimed": False})
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_READY_FOR_HUMAN_REVIEW)

    def test_missing_human_review_required(self):
        sr = self.create_clean_session_record()
        rp = self.create_clean_result_package({"human_review_required": False})
        res = resultcheck(sr, rp, project_root=self.temp_path, aos_root=self.temp_path)
        self.assertEqual(res.status, RESULT_VERIFICATION_NOT_READY)

if __name__ == '__main__':
    unittest.main()
