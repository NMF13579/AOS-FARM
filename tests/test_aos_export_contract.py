import unittest
import os
import subprocess
import tempfile
import json

class TestAosExportContract(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        
    def run_cli(self, args):
        cmd = ["python3", "aos/scripts/aos_architecture_document_check.py"] + args
        result = subprocess.run(cmd, capture_output=True, text=True)
        report = {}
        if result.stdout:
            try:
                report = json.loads(result.stdout)
            except json.JSONDecodeError:
                pass
        return result, report

    def _create_fixture(self, content):
        fd, path = tempfile.mkstemp(suffix=".md")
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path

    def _assert_status(self, content, expected_status):
        path = self._create_fixture(content)
        try:
            res, report = self.run_cli(["task-breakdown", "--file", path])
            self.assertEqual(report.get("status"), expected_status, f"Expected {expected_status} but got {report.get('status')} for content:\n{content}\nReport: {report}")
        finally:
            os.remove(path)

    def get_valid_content(self):
        return """
origin_technical_assignment: ref
origin_architecture_brief: ref
origin_adr: ref
origin_pattern: ref
origin_stack_preset: ref
origin_unknown_resolution: ref
origin_conflict_resolution: ref
architecture_decision_evidence: found
human_architecture_checkpoint: reviewed
unresolved_unknowns: none
downstream_scope_boundary: defined
risk_profile_handling: agent suggests
approval_boundary: defined
build_step_boundary: defined

PASS ≠ approval
Evidence ≠ approval
validator PASS ≠ execution authority
Task Brief readiness does not authorize Build Step execution
Agent may suggest Risk Profile but cannot assign LOW_RISK_FAST
AOS-FARM.633 execution is not claimed
"""

    def test_valid_artifact_positive(self):
        # - valid Architecture-to-Task export artifact with architecture decision Evidence
        # - valid artifact with human checkpoint status
        # - valid artifact with UNKNOWN carry-forward
        # - valid artifact preserving approval boundary
        self._assert_status(self.get_valid_content(), "PASS")

    def test_missing_architecture_decision_evidence(self):
        content = self.get_valid_content().replace("architecture_decision_evidence: found", "")
        self._assert_status(content, "UNKNOWN_BLOCKED")

    def test_missing_human_checkpoint(self):
        content = self.get_valid_content().replace("human_architecture_checkpoint: reviewed", "")
        self._assert_status(content, "HUMAN_REVIEW_REQUIRED")

    def test_unknown_silently_dropped(self):
        content = self.get_valid_content().replace("unresolved_unknowns: none", "")
        self._assert_status(content, "UNKNOWN_BLOCKED")

    def test_pass_treated_as_approval(self):
        content = self.get_valid_content() + "\npass is approval\n"
        self._assert_status(content, "FAILED")

    def test_evidence_treated_as_approval(self):
        content = self.get_valid_content() + "\nevidence is approval\n"
        self._assert_status(content, "FAILED")

    def test_validator_pass_execution_authority(self):
        content = self.get_valid_content() + "\nvalidator pass is execution authority\n"
        self._assert_status(content, "FAILED")

    def test_task_brief_readiness_build_step_auth(self):
        content = self.get_valid_content() + "\ntask brief readiness is build step authorization\n"
        self._assert_status(content, "FAILED")

    def test_agent_assigns_low_risk_fast(self):
        content = self.get_valid_content() + "\nagent assigns low_risk_fast\n"
        self._assert_status(content, "FAILED")

    def test_aos_farm_633_execution_claimed(self):
        content = self.get_valid_content() + "\naos-farm.633 execution claimed\n"
        self._assert_status(content, "FAILED")

    def test_lifecycle_promotion_ready_for_execution(self):
        content = self.get_valid_content() + "\nstatus: READY_FOR_EXECUTION\n"
        self._assert_status(content, "BLOCKED")
if __name__ == '__main__':
    unittest.main()
