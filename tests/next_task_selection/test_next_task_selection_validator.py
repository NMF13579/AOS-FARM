from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path("aos/tools/optional/next_task_selection_validator.py").resolve()
SPEC = importlib.util.spec_from_file_location("aos_next_task_selection_validator_core", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

BLOCKED = MODULE.BLOCKED
PASS = MODULE.PASS
validate_selection = MODULE.validate_selection

FIXTURES = Path("aos/reports/examples/next-task-selection/fixtures")
VALID = FIXTURES / "valid"
NEGATIVE = FIXTURES / "negative"


class NextTaskSelectionValidatorTests(unittest.TestCase):
    def test_valid_accept_fixture(self):
        result = validate_selection(VALID / "selection-accept.md")
        self.assertEqual(result.final_status, PASS)

    def test_valid_clarify_fixture(self):
        result = validate_selection(VALID / "selection-clarify.md")
        self.assertEqual(result.final_status, PASS)

    def test_valid_defer_fixture(self):
        result = validate_selection(VALID / "selection-defer.md")
        self.assertEqual(result.final_status, PASS)

    def test_valid_reject_fixture(self):
        result = validate_selection(VALID / "selection-reject.md")
        self.assertEqual(result.final_status, PASS)

    def test_invalid_execution_authorized_true(self):
        result = validate_selection(NEGATIVE / "selection-authorizes-execution.md")
        self.assertEqual(result.final_status, BLOCKED)

    def test_invalid_task_brief_authorized_true(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "selection.md"
            text = (VALID / "selection-accept.md").read_text(encoding="utf-8")
            artifact.write_text(
                text.replace("task_brief_authorized: false", "task_brief_authorized: true"),
                encoding="utf-8",
            )
            result = validate_selection(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_invalid_next_task_started_true(self):
        result = validate_selection(NEGATIVE / "selection-starts-next-task.md")
        self.assertEqual(result.final_status, BLOCKED)

    def test_invalid_risk_profile_assigned_by_agent(self):
        result = validate_selection(NEGATIVE / "selection-assigns-risk-profile-without-human.md")
        self.assertEqual(result.final_status, BLOCKED)

    def test_invalid_final_status_approved(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "selection.md"
            text = (VALID / "selection-accept.md").read_text(encoding="utf-8")
            artifact.write_text(
                text.replace(
                    "final_status: HUMAN_REVIEW_REQUIRED",
                    "final_status: APPROVED",
                ),
                encoding="utf-8",
            )
            result = validate_selection(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_unknown_is_not_ok(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "selection.md"
            text = (VALID / "selection-accept.md").read_text(encoding="utf-8")
            artifact.write_text(text + "\nUNKNOWN is OK.\n", encoding="utf-8")
            result = validate_selection(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_not_run_is_not_pass(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "selection.md"
            text = (VALID / "selection-accept.md").read_text(encoding="utf-8")
            artifact.write_text(text + "\nNOT_RUN is PASS.\n", encoding="utf-8")
            result = validate_selection(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_pass_is_not_approval(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "selection.md"
            text = (VALID / "selection-accept.md").read_text(encoding="utf-8")
            artifact.write_text(text + "\nPASS is approval.\n", encoding="utf-8")
            result = validate_selection(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_textual_negative_boundary_statements_do_not_cause_false_failure(self):
        result = validate_selection(VALID / "selection-accept.md")
        self.assertEqual(result.final_status, PASS)

    def test_cli_returns_non_zero_for_blocked_artifacts(self):
        process = subprocess.run(
            [
                sys.executable,
                "aos/scripts/aos_next_task_selection.py",
                "validate-selection",
                "--selection",
                str(NEGATIVE / "selection-claims-approval.md"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(process.returncode, 0)
        payload = json.loads(process.stdout)
        self.assertEqual(payload["final_status"], BLOCKED)

    def test_cli_returns_zero_for_valid_artifacts(self):
        process = subprocess.run(
            [
                sys.executable,
                "aos/scripts/aos_next_task_selection.py",
                "validate-selection",
                "--selection",
                str(VALID / "selection-clarify.md"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(process.returncode, 0)
        payload = json.loads(process.stdout)
        self.assertEqual(payload["final_status"], PASS)


if __name__ == "__main__":
    unittest.main()
