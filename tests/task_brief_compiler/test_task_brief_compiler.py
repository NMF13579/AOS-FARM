from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path("aos/tools/optional/task_brief_compiler.py").resolve()
SPEC = importlib.util.spec_from_file_location("aos_task_brief_compiler_core", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

BLOCKED = MODULE.BLOCKED
PASS = MODULE.PASS
compile_task_brief = MODULE.compile_task_brief

FIXTURES = Path("aos/reports/examples/task-brief-compiler/fixtures")
VALID = FIXTURES / "valid"
NEGATIVE = FIXTURES / "negative"


class TaskBriefCompilerTests(unittest.TestCase):
    def test_valid_candidate_and_accept_selection_compiles_draft(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "draft.md"
            result = compile_task_brief(
                VALID / "source-candidate.md",
                VALID / "accepted-selection.md",
                output,
            )
            self.assertEqual(result.final_status, PASS)
            self.assertTrue(output.exists())
            compiled = output.read_text(encoding="utf-8")
        self.assertIn("task_brief_draft_status: DRAFT", compiled)
        self.assertIn("final_status: HUMAN_REVIEW_REQUIRED", compiled)

    def test_compiler_writes_only_explicit_output_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "nested" / "draft.md"
            result = compile_task_brief(
                VALID / "source-candidate.md",
                VALID / "accepted-selection.md",
                output,
            )
            self.assertEqual(result.final_status, PASS)
            self.assertTrue(output.exists())
            self.assertEqual(sorted(output.parent.iterdir()), [output])

    def test_source_candidate_is_not_modified(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "draft.md"
            candidate_before = (VALID / "source-candidate.md").read_text(encoding="utf-8")
            compile_task_brief(VALID / "source-candidate.md", VALID / "accepted-selection.md", output)
            candidate_after = (VALID / "source-candidate.md").read_text(encoding="utf-8")
        self.assertEqual(candidate_before, candidate_after)

    def test_source_selection_is_not_modified(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "draft.md"
            selection_before = (VALID / "accepted-selection.md").read_text(encoding="utf-8")
            compile_task_brief(VALID / "source-candidate.md", VALID / "accepted-selection.md", output)
            selection_after = (VALID / "accepted-selection.md").read_text(encoding="utf-8")
        self.assertEqual(selection_before, selection_after)

    def test_selection_decision_clarify_blocks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "draft.md"
            result = compile_task_brief(VALID / "source-candidate.md", NEGATIVE / "selection-not-accepted.md", output)
        self.assertEqual(result.final_status, BLOCKED)

    def test_selection_decision_defer_blocks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "draft.md"
            selection = Path(tmpdir) / "selection-defer.md"
            text = (VALID / "accepted-selection.md").read_text(encoding="utf-8")
            selection.write_text(text.replace("selection_decision: ACCEPT", "selection_decision: DEFER"), encoding="utf-8")
            result = compile_task_brief(VALID / "source-candidate.md", selection, output)
        self.assertEqual(result.final_status, BLOCKED)

    def test_selection_decision_reject_blocks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "draft.md"
            selection = Path(tmpdir) / "selection-reject.md"
            text = (VALID / "accepted-selection.md").read_text(encoding="utf-8")
            selection.write_text(text.replace("selection_decision: ACCEPT", "selection_decision: REJECT"), encoding="utf-8")
            result = compile_task_brief(VALID / "source-candidate.md", selection, output)
        self.assertEqual(result.final_status, BLOCKED)

    def test_selection_with_execution_authorized_true_blocks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "draft.md"
            result = compile_task_brief(
                VALID / "source-candidate.md",
                NEGATIVE / "selection-authorizes-execution.md",
                output,
            )
        self.assertEqual(result.final_status, BLOCKED)

    def test_candidate_status_not_draft_blocks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            candidate = Path(tmpdir) / "candidate.md"
            output = Path(tmpdir) / "draft.md"
            text = (VALID / "source-candidate.md").read_text(encoding="utf-8")
            candidate.write_text(text.replace("status: DRAFT", "status: READY_FOR_EXECUTION"), encoding="utf-8")
            result = compile_task_brief(candidate, VALID / "accepted-selection.md", output)
        self.assertEqual(result.final_status, BLOCKED)

    def test_missing_required_candidate_fields_block(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            candidate = Path(tmpdir) / "candidate.md"
            output = Path(tmpdir) / "draft.md"
            text = (VALID / "source-candidate.md").read_text(encoding="utf-8")
            candidate.write_text(text.replace("allowed_files: aos/docs/workflow/, aos/templates/task-briefs/\n", ""), encoding="utf-8")
            result = compile_task_brief(candidate, VALID / "accepted-selection.md", output)
        self.assertEqual(result.final_status, BLOCKED)

    def test_generated_draft_keeps_execution_authorized_false(self):
        compiled = self._compile_to_temp()
        self.assertIn("execution_authorized: false", compiled)

    def test_generated_draft_keeps_risk_profile_assigned_by_human_false(self):
        compiled = self._compile_to_temp()
        self.assertIn("risk_profile_assigned_by_human: false", compiled)

    def test_generated_draft_keeps_commit_authorized_false(self):
        compiled = self._compile_to_temp()
        self.assertIn("commit_authorized: false", compiled)

    def test_generated_draft_keeps_push_authorized_false(self):
        compiled = self._compile_to_temp()
        self.assertIn("push_authorized: false", compiled)

    def test_generated_draft_ends_at_human_review_required(self):
        compiled = self._compile_to_temp()
        self.assertIn("final_status: HUMAN_REVIEW_REQUIRED", compiled)

    def test_cli_returns_zero_for_valid_compile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "draft.md"
            process = subprocess.run(
                [
                    sys.executable,
                    "aos/scripts/aos_task_brief_compile.py",
                    "compile",
                    "--candidate",
                    str(VALID / "source-candidate.md"),
                    "--selection",
                    str(VALID / "accepted-selection.md"),
                    "--output",
                    str(output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(process.returncode, 0)
        payload = json.loads(process.stdout)
        self.assertEqual(payload["final_status"], PASS)

    def test_cli_returns_non_zero_for_blocked_compile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "draft.md"
            process = subprocess.run(
                [
                    sys.executable,
                    "aos/scripts/aos_task_brief_compile.py",
                    "compile",
                    "--candidate",
                    str(VALID / "source-candidate.md"),
                    "--selection",
                    str(NEGATIVE / "selection-not-accepted.md"),
                    "--output",
                    str(output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(process.returncode, 0)
        payload = json.loads(process.stdout)
        self.assertEqual(payload["final_status"], BLOCKED)

    def _compile_to_temp(self) -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "draft.md"
            result = compile_task_brief(
                VALID / "source-candidate.md",
                VALID / "accepted-selection.md",
                output,
            )
            self.assertEqual(result.final_status, PASS)
            return output.read_text(encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
