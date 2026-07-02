import unittest
import tempfile
import json
from pathlib import Path
from aos.tools.optional.controlled_execution_guard import (
    sessioncheck,
    SESSION_CONSISTENCY_PASS,
    SESSION_CONSISTENCY_BLOCKED,
    SESSION_CONSISTENCY_NOT_READY,
    UNKNOWN_BLOCKED
)

class TestControlledExecutionSessionCheck(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name).resolve()
        
    def tearDown(self):
        self.temp_dir.cleanup()
        
    def write_json(self, name, content):
        p = self.temp_path / f"{name}.json"
        p.write_text(json.dumps(content, indent=2))
        return p
        
    def default_artifacts(self):
        req = {"task_id": "T1", "request_id": "R1"}
        prec = {"task_id": "T1", "request_id": "R1", "preconditions_id": "P1"}
        bound = {"task_id": "T1", "request_id": "R1", "boundary_id": "B1"}
        rec = {
            "task_id": "T1",
            "request_id": "R1",
            "preconditions_id": "P1",
            "boundary_id": "B1",
            "handoff_to_result_verification_required": True,
            "approval_claimed": False
        }
        return req, prec, bound, rec
        
    def run_check(self, req, prec, bound, rec):
        rp = self.write_json("request", req)
        pp = self.write_json("preconditions", prec)
        bp = self.write_json("boundary", bound)
        recp = self.write_json("record", rec)
        # Using self.temp_path as project_root to pass path safety checks
        return sessioncheck(rp, pp, bp, recp, project_root=self.temp_path, aos_root=Path("aos").resolve())

    def test_clean_session(self):
        req, prec, bound, rec = self.default_artifacts()
        res = self.run_check(req, prec, bound, rec)
        self.assertEqual(res.status, SESSION_CONSISTENCY_PASS)
        
    def test_missing_artifact(self):
        req, prec, bound, rec = self.default_artifacts()
        rp = self.write_json("request", req)
        pp = self.write_json("preconditions", prec)
        bp = self.write_json("boundary", bound)
        missing_recp = self.temp_path / "missing_record.json"
        res = sessioncheck(rp, pp, bp, missing_recp, project_root=self.temp_path, aos_root=Path("aos").resolve())
        self.assertEqual(res.status, SESSION_CONSISTENCY_BLOCKED)
        
    def test_malformed_json(self):
        req, prec, bound, rec = self.default_artifacts()
        rp = self.write_json("request", req)
        pp = self.write_json("preconditions", prec)
        bp = self.write_json("boundary", bound)
        recp = self.temp_path / "record.json"
        recp.write_text("{ malformed }")
        res = sessioncheck(rp, pp, bp, recp, project_root=self.temp_path, aos_root=Path("aos").resolve())
        self.assertIn(res.status, (SESSION_CONSISTENCY_BLOCKED, UNKNOWN_BLOCKED))
        
    def test_task_id_mismatch(self):
        req, prec, bound, rec = self.default_artifacts()
        rec["task_id"] = "T2"
        res = self.run_check(req, prec, bound, rec)
        self.assertEqual(res.status, SESSION_CONSISTENCY_BLOCKED)
        
    def test_request_id_mismatch(self):
        req, prec, bound, rec = self.default_artifacts()
        prec["request_id"] = "R2"
        res = self.run_check(req, prec, bound, rec)
        self.assertEqual(res.status, SESSION_CONSISTENCY_BLOCKED)
        
    def test_preconditions_id_mismatch(self):
        req, prec, bound, rec = self.default_artifacts()
        rec["preconditions_id"] = "P2"
        res = self.run_check(req, prec, bound, rec)
        self.assertEqual(res.status, SESSION_CONSISTENCY_BLOCKED)
        
    def test_boundary_id_mismatch(self):
        req, prec, bound, rec = self.default_artifacts()
        rec["boundary_id"] = "B2"
        res = self.run_check(req, prec, bound, rec)
        self.assertEqual(res.status, SESSION_CONSISTENCY_BLOCKED)
        
    def test_task_completion_claimed(self):
        req, prec, bound, rec = self.default_artifacts()
        rec["task_completion_claimed"] = True
        res = self.run_check(req, prec, bound, rec)
        self.assertEqual(res.status, SESSION_CONSISTENCY_BLOCKED)
        
    def test_result_verification_claimed(self):
        req, prec, bound, rec = self.default_artifacts()
        rec["result_verification_claimed"] = True
        res = self.run_check(req, prec, bound, rec)
        self.assertEqual(res.status, SESSION_CONSISTENCY_BLOCKED)
        
    def test_approval_claimed(self):
        req, prec, bound, rec = self.default_artifacts()
        rec["approval_claimed"] = True
        res = self.run_check(req, prec, bound, rec)
        self.assertEqual(res.status, SESSION_CONSISTENCY_BLOCKED)
        
    def test_commit_performed(self):
        req, prec, bound, rec = self.default_artifacts()
        rec["commit_performed"] = True
        res = self.run_check(req, prec, bound, rec)
        self.assertEqual(res.status, SESSION_CONSISTENCY_BLOCKED)
        
    def test_raw_unsafe_claim_ready_to_merge(self):
        req, prec, bound, rec = self.default_artifacts()
        rec["some_notes"] = "ready to merge"
        res = self.run_check(req, prec, bound, rec)
        self.assertEqual(res.status, SESSION_CONSISTENCY_BLOCKED)
        
    def test_missing_handoff_marker(self):
        req, prec, bound, rec = self.default_artifacts()
        rec.pop("handoff_to_result_verification_required", None)
        rec.pop("human_review_required", None)
        res = self.run_check(req, prec, bound, rec)
        self.assertEqual(res.status, SESSION_CONSISTENCY_NOT_READY)
        
    def test_negative_boundary_statements_false(self):
        req, prec, bound, rec = self.default_artifacts()
        rec["approval_claimed"] = False
        rec["task_completion_claimed"] = False
        res = self.run_check(req, prec, bound, rec)
        self.assertEqual(res.status, SESSION_CONSISTENCY_PASS)

if __name__ == "__main__":
    unittest.main()
