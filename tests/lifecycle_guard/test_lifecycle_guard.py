from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path("aos/tools/optional/lifecycle_guard.py").resolve()
SPEC = importlib.util.spec_from_file_location("aos_lifecycle_guard_core", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

BLOCKED = MODULE.BLOCKED
PASS = MODULE.PASS
validate_commit_checkpoint = MODULE.validate_commit_checkpoint
validate_push_checkpoint = MODULE.validate_push_checkpoint

FIXTURES = Path("aos/reports/examples/lifecycle-guard/fixtures")
VALID = FIXTURES / "valid"
NEGATIVE = FIXTURES / "negative"


class LifecycleGuardTests(unittest.TestCase):
    def test_valid_commit_checkpoint_returns_pass(self):
        result = validate_commit_checkpoint(VALID / "commit-authorized.md")
        self.assertEqual(result.final_status, PASS)

    def test_valid_push_checkpoint_returns_pass(self):
        result = validate_push_checkpoint(VALID / "push-authorized.md")
        self.assertEqual(result.final_status, PASS)

    def test_commit_checkpoint_with_commit_authorized_false_blocks(self):
        result = validate_commit_checkpoint(NEGATIVE / "commit-not-authorized.md")
        self.assertEqual(result.final_status, BLOCKED)

    def test_push_checkpoint_with_push_authorized_false_blocks(self):
        result = validate_push_checkpoint(NEGATIVE / "push-not-authorized.md")
        self.assertEqual(result.final_status, BLOCKED)

    def test_force_push_authorized_true_blocks(self):
        result = validate_push_checkpoint(NEGATIVE / "force-push-claimed.md")
        self.assertEqual(result.final_status, BLOCKED)

    def test_force_push_performed_true_blocks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "push.md"
            text = (VALID / "push-authorized.md").read_text(encoding="utf-8")
            artifact.write_text(text + "\nforce_push_performed: true\n", encoding="utf-8")
            result = validate_push_checkpoint(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_tag_push_authorized_true_blocks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "push.md"
            text = (VALID / "push-authorized.md").read_text(encoding="utf-8")
            artifact.write_text(text.replace("tag_push_authorized: false", "tag_push_authorized: true"), encoding="utf-8")
            result = validate_push_checkpoint(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_merge_authorized_true_blocks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "push.md"
            text = (VALID / "push-authorized.md").read_text(encoding="utf-8")
            artifact.write_text(text.replace("merge_authorized: false", "merge_authorized: true"), encoding="utf-8")
            result = validate_push_checkpoint(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_release_authorized_true_blocks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "push.md"
            text = (VALID / "push-authorized.md").read_text(encoding="utf-8")
            artifact.write_text(text.replace("release_authorized: false", "release_authorized: true"), encoding="utf-8")
            result = validate_push_checkpoint(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_next_task_authorized_true_blocks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "push.md"
            text = (VALID / "push-authorized.md").read_text(encoding="utf-8")
            artifact.write_text(text.replace("next_task_authorized: false", "next_task_authorized: true"), encoding="utf-8")
            result = validate_push_checkpoint(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_next_task_started_true_blocks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "commit.md"
            text = (VALID / "commit-authorized.md").read_text(encoding="utf-8")
            artifact.write_text(text.replace("next_task_started: false", "next_task_started: true"), encoding="utf-8")
            result = validate_commit_checkpoint(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_human_decision_required_true_blocks_when_authorization_expected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "commit.md"
            text = (VALID / "commit-authorized.md").read_text(encoding="utf-8")
            artifact.write_text(text.replace("human_decision_required: false", "human_decision_required: true"), encoding="utf-8")
            result = validate_commit_checkpoint(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_unknown_is_not_ok(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "push.md"
            text = (VALID / "push-authorized.md").read_text(encoding="utf-8")
            artifact.write_text(text + "\nUNKNOWN is OK.\n", encoding="utf-8")
            result = validate_push_checkpoint(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_not_run_is_not_pass(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "push.md"
            text = (VALID / "push-authorized.md").read_text(encoding="utf-8")
            artifact.write_text(text + "\nNOT_RUN is PASS.\n", encoding="utf-8")
            result = validate_push_checkpoint(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_pass_is_not_approval(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "commit.md"
            text = (VALID / "commit-authorized.md").read_text(encoding="utf-8")
            artifact.write_text(text + "\nPASS is approval.\n", encoding="utf-8")
            result = validate_commit_checkpoint(artifact)
        self.assertEqual(result.final_status, BLOCKED)

    def test_textual_negative_boundary_statements_do_not_cause_false_failure(self):
        result = validate_push_checkpoint(VALID / "push-authorized.md")
        self.assertEqual(result.final_status, PASS)

    def test_cli_returns_zero_for_valid_checkpoints(self):
        process = subprocess.run(
            [
                sys.executable,
                "aos/scripts/aos_lifecycle_guard.py",
                "validate-commit-checkpoint",
                "--checkpoint",
                str(VALID / "commit-authorized.md"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(process.returncode, 0)
        payload = json.loads(process.stdout)
        self.assertEqual(payload["final_status"], PASS)

    def test_cli_returns_non_zero_for_blocked_checkpoints(self):
        process = subprocess.run(
            [
                sys.executable,
                "aos/scripts/aos_lifecycle_guard.py",
                "validate-push-checkpoint",
                "--checkpoint",
                str(NEGATIVE / "force-push-claimed.md"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(process.returncode, 0)
        payload = json.loads(process.stdout)
        self.assertEqual(payload["final_status"], BLOCKED)


if __name__ == "__main__":
    unittest.main()
