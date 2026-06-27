from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path("aos/tools/optional/project_state_scanner.py").resolve()
SPEC = importlib.util.spec_from_file_location("aos_project_state_scanner_core", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

scan_project_state = MODULE.scan_project_state
UNKNOWN_BLOCKED = MODULE.UNKNOWN_BLOCKED


class ProjectStateScannerTests(unittest.TestCase):
    def test_scanner_returns_git_state_from_mocked_read_only_commands(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "reports").mkdir()
            (root / "reports" / "aos-farm-441-8-lifecycle-guard-mvp-report.md").write_text("x", encoding="utf-8")
            state = scan_project_state(project_root=root, run_command=self._mock_commands())
        self.assertEqual(state["branch"], "build/deterministic-control-helpers-mvp")
        self.assertEqual(state["head"], "abc123")
        self.assertEqual(state["origin_dev"], "def456")
        self.assertEqual(state["ahead_behind"], "0\t0")

    def test_scanner_returns_unknown_blocked_when_origin_dev_unavailable(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "reports").mkdir()
            state = scan_project_state(project_root=root, run_command=self._mock_commands(origin_available=False))
        self.assertIsNone(state["origin_dev"])
        self.assertEqual(state["remote_probe_status"], UNKNOWN_BLOCKED)

    def test_scanner_does_not_infer_approval_from_pass(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._make_minimal_project(tmpdir)
            candidate = root / "aos" / "reports" / "examples" / "task-brief-compiler" / "fixtures" / "valid" / "source-candidate.md"
            candidate.parent.mkdir(parents=True)
            candidate.write_text("status: DRAFT\ncandidate_goal: x\n", encoding="utf-8")
            draft = root / "reports" / "aos-farm-441-7-dogfood-task-brief-draft.md"
            draft.write_text(
                "source_candidate: aos/reports/examples/task-brief-compiler/fixtures/valid/source-candidate.md\n"
                "final_status: HUMAN_REVIEW_REQUIRED\nPASS is not approval.\n",
                encoding="utf-8",
            )
            state = scan_project_state(project_root=root, run_command=self._mock_commands())
        self.assertFalse(state["execution_authorized"])

    def test_scanner_does_not_infer_approval_from_evidence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._make_minimal_project(tmpdir)
            state = scan_project_state(project_root=root, run_command=self._mock_commands())
        self.assertFalse(state["commit_authorized"])

    def test_scanner_does_not_treat_unknown_as_ok(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._make_minimal_project(tmpdir)
            state = scan_project_state(project_root=root, run_command=self._mock_commands(origin_available=False))
        self.assertEqual(state["remote_probe_status"], UNKNOWN_BLOCKED)

    def test_scanner_does_not_treat_not_run_as_pass(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._make_minimal_project(tmpdir)
            state = scan_project_state(project_root=root, run_command=self._mock_commands())
        self.assertFalse(state["push_authorized"])

    def test_scanner_keeps_execution_authorized_false_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._make_minimal_project(tmpdir)
            state = scan_project_state(project_root=root, run_command=self._mock_commands())
        self.assertFalse(state["execution_authorized"])

    def test_scanner_keeps_commit_authorized_false_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._make_minimal_project(tmpdir)
            state = scan_project_state(project_root=root, run_command=self._mock_commands())
        self.assertFalse(state["commit_authorized"])

    def test_scanner_keeps_push_authorized_false_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._make_minimal_project(tmpdir)
            state = scan_project_state(project_root=root, run_command=self._mock_commands())
        self.assertFalse(state["push_authorized"])

    def test_scanner_reports_next_required_action_conservatively(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._make_minimal_project(tmpdir)
            candidate = root / "aos" / "reports" / "examples" / "task-brief-compiler" / "fixtures" / "valid" / "source-candidate.md"
            candidate.parent.mkdir(parents=True)
            candidate.write_text("status: DRAFT\ncandidate_goal: x\n", encoding="utf-8")
            draft = root / "reports" / "aos-farm-441-7-dogfood-task-brief-draft.md"
            draft.write_text(
                "source_candidate: aos/reports/examples/task-brief-compiler/fixtures/valid/source-candidate.md\n"
                "final_status: HUMAN_REVIEW_REQUIRED\n",
                encoding="utf-8",
            )
            state = scan_project_state(project_root=root, run_command=self._mock_commands())
        self.assertEqual(state["next_required_action"], "HUMAN_REVIEW_TASK_BRIEF_DRAFT")

    def test_scanner_does_not_mutate_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._make_minimal_project(tmpdir)
            before = sorted(str(path.relative_to(root)) for path in root.rglob("*"))
            scan_project_state(project_root=root, run_command=self._mock_commands())
            after = sorted(str(path.relative_to(root)) for path in root.rglob("*"))
        self.assertEqual(before, after)

    def test_cli_returns_json_machine_readable_output(self):
        process = subprocess.run(
            [sys.executable, "aos/scripts/aos_status.py", "status"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(process.returncode, 0)
        payload = json.loads(process.stdout)
        self.assertIn("branch", payload)
        self.assertIn("execution_authorized", payload)

    def test_cli_json_flag_returns_json_machine_readable_output(self):
        process = subprocess.run(
            [sys.executable, "aos/scripts/aos_status.py", "status", "--json"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(process.returncode, 0)
        payload = json.loads(process.stdout)
        self.assertIn("next_required_action", payload)

    def _mock_commands(self, origin_available: bool = True):
        results = {
            ("git", "branch", "--show-current"): "build/deterministic-control-helpers-mvp",
            ("git", "rev-parse", "HEAD"): "abc123",
            ("git", "rev-list", "--left-right", "--count", "origin/dev...HEAD"): "0\t0",
        }
        if origin_available:
            results[("git", "rev-parse", "origin/dev")] = "def456"

        def runner(command):
            key = tuple(command)
            if key not in results:
                raise RuntimeError("unavailable")
            return results[key]

        return runner

    def _make_minimal_project(self, tmpdir: str) -> Path:
        root = Path(tmpdir)
        (root / "reports").mkdir()
        (root / "aos").mkdir()
        (root / "reports" / "aos-farm-441-8-lifecycle-guard-mvp-report.md").write_text("x", encoding="utf-8")
        return root


if __name__ == "__main__":
    unittest.main()
