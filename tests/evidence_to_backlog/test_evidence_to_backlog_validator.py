from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path("aos/tools/optional/evidence_to_backlog_validator.py").resolve()
SPEC = importlib.util.spec_from_file_location("aos_evidence_to_backlog_validator_core", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

BLOCKED = MODULE.BLOCKED
HUMAN_REVIEW_REQUIRED = MODULE.HUMAN_REVIEW_REQUIRED
PASS = MODULE.PASS
validate_backlog_item = MODULE.validate_backlog_item
validate_chain = MODULE.validate_chain
validate_lessons = MODULE.validate_lessons
validate_next_task_candidate = MODULE.validate_next_task_candidate
validate_review = MODULE.validate_review

FIXTURES = Path("aos/reports/examples/evidence-to-backlog/fixtures")
VALID = FIXTURES / "valid"
NEGATIVE = FIXTURES / "negative"


class EvidenceToBacklogValidatorTests(unittest.TestCase):
    def test_valid_review_returns_pass(self):
        result = validate_review(VALID / "post-execution-review.md")
        self.assertEqual(result.final_status, PASS)

    def test_valid_lessons_returns_pass(self):
        result = validate_lessons(VALID / "lessons-learned.md")
        self.assertEqual(result.final_status, PASS)

    def test_valid_backlog_item_returns_pass(self):
        result = validate_backlog_item(VALID / "backlog-item.md")
        self.assertEqual(result.final_status, PASS)

    def test_valid_next_task_candidate_returns_pass(self):
        result = validate_next_task_candidate(VALID / "next-task-candidate.md")
        self.assertEqual(result.final_status, PASS)

    def test_valid_chain_returns_pass(self):
        result = validate_chain(
            VALID / "post-execution-review.md",
            VALID / "lessons-learned.md",
            VALID / "backlog-item.md",
            VALID / "next-task-candidate.md",
        )
        self.assertEqual(result.final_status, PASS)

    def test_missing_required_field_returns_blocked(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "review.md"
            source = (VALID / "post-execution-review.md").read_text(encoding="utf-8")
            artifact.write_text(source.replace("source_task_id: AOS-FARM.FIXTURE\n", ""), encoding="utf-8")
            result = validate_review(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_not_run_treated_as_pass_returns_blocked(self):
        result = validate_review(NEGATIVE / "not-run-treated-as-pass.md")
        self.assertEqual(result.final_status, BLOCKED)

    def test_unknown_treated_as_ok_returns_blocked(self):
        result = validate_review(NEGATIVE / "unknown-treated-as-ok.md")
        self.assertEqual(result.final_status, BLOCKED)

    def test_candidate_with_approval_claim_returns_blocked(self):
        result = validate_next_task_candidate(NEGATIVE / "candidate-claims-approval.md")
        self.assertEqual(result.final_status, BLOCKED)

    def test_candidate_with_execution_authorized_true_returns_blocked(self):
        result = validate_next_task_candidate(NEGATIVE / "execution-authorized-inside-candidate.md")
        self.assertEqual(result.final_status, BLOCKED)

    def test_self_assigned_risk_profile_requires_human_review_or_blocks(self):
        result = validate_next_task_candidate(NEGATIVE / "risk-profile-self-assigned.md")
        self.assertIn(result.final_status, {HUMAN_REVIEW_REQUIRED, BLOCKED})

    def test_missing_source_evidence_returns_blocked(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "candidate.md"
            source = (VALID / "next-task-candidate.md").read_text(encoding="utf-8")
            artifact.write_text(source.replace("source_evidence: reports/fixture-evidence.md\n", "source_evidence:\n"), encoding="utf-8")
            result = validate_next_task_candidate(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_validator_does_not_emit_forbidden_status(self):
        result = validate_chain(
            VALID / "post-execution-review.md",
            VALID / "lessons-learned.md",
            VALID / "backlog-item.md",
            VALID / "next-task-candidate.md",
        )
        self.assertNotEqual(result.final_status, "APPROVED")
        self.assertNotIn("APPROVED", MODULE.ALLOWED_STATUSES)

    def test_cli_invalid_arguments_emit_blocked_final_status(self):
        process = subprocess.run(
            [sys.executable, "aos/scripts/aos_evidence_to_backlog.py", "validate-review"],
            check=False,
            capture_output=True,
            text=True,
        )
        combined_output = process.stdout + process.stderr
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("final_status", combined_output)
        self.assertNotIn('"final_status": "APPROVED"', combined_output)
        self.assertNotIn("approval_claimed: true", combined_output)

        json_lines = [
            line for line in combined_output.splitlines() if line.strip().startswith("{")
        ]
        self.assertTrue(json_lines)
        payload = json.loads(json_lines[-1])
        self.assertEqual(payload["final_status"], BLOCKED)
        self.assertFalse(payload["approval_claimed"])


if __name__ == "__main__":
    unittest.main()
