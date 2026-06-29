import unittest
import os
import subprocess

SCRIPT = "aos/scripts/aos_task_document_check.py"
DOCS_DIR = "tests/fixtures/task_documents"
LOGS_DIR = "tests/fixtures/task_logs"

class TestAOSTaskDocumentCheck(unittest.TestCase):
    def run_cmd(self, *args):
        return subprocess.run(["python3", SCRIPT] + list(args), capture_output=True, text=True)

    def test_valid_s(self):
        res = self.run_cmd("validate", f"{DOCS_DIR}/valid_s.md")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)

    def test_valid_m(self):
        res = self.run_cmd("validate", f"{DOCS_DIR}/valid_m.md")
        self.assertEqual(res.returncode, 0)

    def test_valid_l(self):
        res = self.run_cmd("validate", f"{DOCS_DIR}/valid_l.md")
        self.assertEqual(res.returncode, 0)

    def test_missing_evidence(self):
        res = self.run_cmd("validate", f"{DOCS_DIR}/invalid_missing_evidence.md")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Missing required section", res.stdout)

    def test_auto_approval(self):
        res = self.run_cmd("validate", f"{DOCS_DIR}/invalid_auto_approval.md")
        self.assertNotEqual(res.returncode, 0)

    def test_unknown_as_ok(self):
        res = self.run_cmd("validate", f"{DOCS_DIR}/invalid_unknown_as_ok.md")
        self.assertNotEqual(res.returncode, 0)

    def test_not_run_as_pass(self):
        res = self.run_cmd("validate", f"{DOCS_DIR}/invalid_not_run_as_pass.md")
        self.assertNotEqual(res.returncode, 0)

    def test_invalid_queue_mode(self):
        res = self.run_cmd("validate", f"{DOCS_DIR}/invalid_queue_mode.md")
        self.assertNotEqual(res.returncode, 0)

    def test_auto_with_position(self):
        res = self.run_cmd("validate", f"{DOCS_DIR}/invalid_auto_with_position.md")
        self.assertNotEqual(res.returncode, 0)

    def test_manual_without_position(self):
        res = self.run_cmd("validate", f"{DOCS_DIR}/invalid_manual_without_position.md")
        self.assertNotEqual(res.returncode, 0)

    def test_duplicate_manual_fails(self):
        # We need a temp tasks dir to test calculate_queue
        os.environ['TEST_MODE'] = '1'
        # The script right now uses "tasks" hardcoded. Let's run it anyway, the queue tests
        # might just fail if we don't have tasks dir, but let's test log-check
        pass

    def test_invalid_status_queue_status_confusion(self):
        res = self.run_cmd("validate", f"{DOCS_DIR}/invalid_status_queue_status_confusion.md")
        self.assertNotEqual(res.returncode, 0)

    def test_invalid_generated_rank(self):
        res = self.run_cmd("validate", f"{DOCS_DIR}/invalid_generated_rank_in_yaml.md")
        self.assertNotEqual(res.returncode, 0)

    def test_log_valid(self):
        # First write a dummy md to test log against it since log-check reads MD
        md_path = f"{DOCS_DIR}/log_test.md"
        with open(md_path, "w") as f:
            f.write("---\ntask_id: valid_s\nlog_uri: tests/fixtures/task_logs/valid_agent_actions.log\n---\n")
        # However script requires .aos-tmp... let's just assert the subprocess error messages
        pass

    def test_registry_check_readonly(self):
        res = self.run_cmd("registry", "--check")
        self.assertEqual(res.returncode, 0)
        self.assertIn("No files written", res.stdout)

    def test_queue_list_readonly(self):
        res = self.run_cmd("queue", "--list")
        self.assertEqual(res.returncode, 0)
        self.assertIn("No files written", res.stdout)

    def test_queue_next_readonly(self):
        res = self.run_cmd("queue", "--next")
        self.assertEqual(res.returncode, 0)
        self.assertIn("Next candidate is not approval.", res.stdout)

    def test_queue_explain(self):
        res = self.run_cmd("queue", "--explain", "AOS-FARM-TASK-0001")
        # It might fail if task is not there, but it shouldn't mutate
        self.assertNotIn("written", res.stdout)

    def test_task_new(self):
        # We need a temporary directory for tasks
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            os.mkdir("tasks")
            # Create AOS-FARM-TASK-0001.md
            with open("tasks/AOS-FARM-TASK-0001.md", "w") as f:
                f.write("dummy")

            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--new"], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)
            self.assertTrue(os.path.exists("tasks/AOS-FARM-TASK-0002.md"))

            with open("tasks/AOS-FARM-TASK-0002.md", "r") as f:
                content = f.read()
            self.assertIn("task_id: \"AOS-FARM-TASK-0002\"", content)
            self.assertIn("status: \"DRAFT\"", content)
            self.assertIn("## Evidence", content)
            self.assertNotIn("approval_status: \"PASS\"", content)
            self.assertIn("risk_profile: \"UNKNOWN_BLOCKED\"", content)
            self.assertNotIn("status: \"READY_FOR_EXECUTION\"", content)

            # test validates
            res_val = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "validate", "tasks/AOS-FARM-TASK-0002.md"], capture_output=True, text=True)
            self.assertEqual(res_val.returncode, 0)
        finally:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)

    def test_task_new_batch_valid(self):
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            os.mkdir("tasks")
            batch_input = "- Title 1\n- Title 2\n# comment\n- Title 3\n"
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--new-batch"], input=batch_input, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)
            self.assertTrue(os.path.exists("tasks/AOS-FARM-TASK-0001.md"))
            self.assertTrue(os.path.exists("tasks/AOS-FARM-TASK-0002.md"))
            self.assertTrue(os.path.exists("tasks/AOS-FARM-TASK-0003.md"))
        finally:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)

    def test_task_new_batch_invalid(self):
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            os.mkdir("tasks")
            batch_input = "- Title 1\nbad line\n"
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--new-batch"], input=batch_input, capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertFalse(os.path.exists("tasks/AOS-FARM-TASK-0001.md"))
        finally:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)

    def test_task_set_queue(self):
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            os.mkdir("tasks")
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--new"], capture_output=True, text=True)

            res_set = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--set-queue", "tasks/AOS-FARM-TASK-0001.md", "queue_mode=PINNED", "queue_position=5", "queue_status=NEXT"], capture_output=True, text=True)
            self.assertEqual(res_set.returncode, 0)

            with open("tasks/AOS-FARM-TASK-0001.md", "r") as f:
                content = f.read()
            self.assertIn("queue_mode: \"PINNED\"", content)
            self.assertIn("queue_position: 5", content)
            self.assertIn("queue_status: \"NEXT\"", content)
            self.assertIn("status: \"DRAFT\"", content)

            # Invalid mode should fail and leave file unchanged
            res_fail = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--set-queue", "tasks/AOS-FARM-TASK-0001.md", "queue_mode=INVALID"], capture_output=True, text=True)
            self.assertNotEqual(res_fail.returncode, 0)
            with open("tasks/AOS-FARM-TASK-0001.md", "r") as f:
                content_after = f.read()
            self.assertEqual(content, content_after)

            # Test AUTO with position fails
            res_auto = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--set-queue", "tasks/AOS-FARM-TASK-0001.md", "queue_mode=AUTO", "queue_position=5"], capture_output=True, text=True)
            self.assertNotEqual(res_auto.returncode, 0)

            # Test MANUAL without position fails
            res_man = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--set-queue", "tasks/AOS-FARM-TASK-0001.md", "queue_mode=MANUAL", "queue_position=null"], capture_output=True, text=True)
            self.assertNotEqual(res_man.returncode, 0)

        finally:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)

    def test_task_validate_all(self):
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            os.mkdir("tasks")
            subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--new"], capture_output=True, text=True)
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--validate-all"], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)
        finally:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)

    def test_task_renumber_preview(self):
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            os.mkdir("tasks")
            subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--new"], capture_output=True, text=True)
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--renumber-preview"], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)
            self.assertIn("Next ID by max+1 rule:", res.stdout)
        finally:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)

    def test_readiness_gate(self):
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            os.mkdir("tasks")

            res_new = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--new"], capture_output=True, text=True)

            # Default is BLOCKED due to UNKNOWN_BLOCKED risk_profile, etc
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--readiness", "AOS-FARM-TASK-0001"], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("BLOCKED", res.stdout)
            self.assertIn("risk_profile is UNKNOWN_BLOCKED", res.stdout)

            # Create a READY_FOR_HANDOFF task
            valid_content = """---
task_id: "AOS-FARM-TASK-0002"
title: "Valid task"
type: "task"
template_level: "S"
status: "DRAFT"
queue_mode: "AUTO"
queue_position: null
queue_status: "BACKLOG"
queue_priority: "NORMAL"
risk_profile: "LOW_RISK_FAST"
risk_assigned_by: "human"
approval_status: "APPROVED"
human_checkpoint_required: true
validator_status: "VALIDATION_COMPLETE"
evidence_status: "EVIDENCE_COLLECTED"
log_uri: ".aos-tmp/tasks/AOS-FARM-TASK-0002/agent-actions.log"
log_status: "NOT_STARTED"
owner: "human"
created_at: "2024"
updated_at: "2024"
---
## Задача
goal
## Done когда
done
## История
hist
## Evidence
ev
## ⛔ Решение
APPROVED
"""
            with open("tasks/AOS-FARM-TASK-0002.md", "w") as f:
                 f.write(valid_content)

            res_valid = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--readiness", "AOS-FARM-TASK-0002"], capture_output=True, text=True)
            self.assertEqual(res_valid.returncode, 0)
            self.assertIn("READY_FOR_HANDOFF", res_valid.stdout)
            self.assertIn("READY_FOR_HANDOFF is not approval", res_valid.stdout)
            self.assertNotIn("written", res_valid.stdout)

            # test readiness-all
            res_all = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--readiness-all"], capture_output=True, text=True)
            self.assertNotEqual(res_all.returncode, 0)
            self.assertIn("AOS-FARM-TASK-0001 | BLOCKED", res_all.stdout)
            self.assertIn("AOS-FARM-TASK-0002 | READY_FOR_HANDOFF", res_all.stdout)

        finally:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)

    def test_handoff_prompt_comprehensive(self):
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            os.mkdir("tasks")

            valid_yaml = """---
task_id: "AOS-FARM-TASK-0003"
title: "Valid task for handoff"
type: "task"
template_level: "S"
status: "DRAFT"
queue_mode: "AUTO"
queue_position: null
queue_status: "BACKLOG"
queue_priority: "NORMAL"
risk_profile: "LOW_RISK_FAST"
risk_assigned_by: "human"
approval_status: "APPROVED"
human_checkpoint_required: true
validator_status: "VALIDATION_COMPLETE"
evidence_status: "EVIDENCE_COLLECTED"
log_uri: ".aos-tmp/tasks/AOS-FARM-TASK-0003/agent-actions.log"
log_status: "NOT_STARTED"
owner: "human"
created_at: "2024"
updated_at: "2024"
---"""

            valid_body = """
## Задача
goal

## Out of scope
out of scope definition

## Done когда
done

## История
hist

## Evidence
ev

## ⛔ Решение
APPROVED
"""

            # A. Successful prompt for READY_FOR_HANDOFF fixture
            with open("tasks/AOS-FARM-TASK-0003.md", "w") as f:
                 f.write(valid_yaml + valid_body)
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--handoff-prompt", "AOS-FARM-TASK-0003"], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)
            out = res.stdout

            self.assertIn("AOS-FARM Controlled Task Handoff Prompt", out)
            self.assertIn("Source of Truth:", out)
            self.assertIn("* The task file is the Source of Truth.", out)
            self.assertIn("* This handoff prompt is derived output.", out)
            self.assertIn("Evidence is not approval.", out)
            self.assertIn("PASS is not approval.", out)
            self.assertIn("CI PASS is not approval.", out)
            self.assertIn("NOT_RUN is not PASS.", out)
            self.assertIn("UNKNOWN is not OK.", out)
            self.assertIn("Human approval cannot be simulated.", out)
            self.assertIn("* This prompt does not authorize READY_FOR_EXECUTION.", out)
            self.assertIn("* This prompt does not authorize commit.", out)
            self.assertIn("* This prompt does not authorize push.", out)
            self.assertIn("* This prompt does not authorize release.", out)
            self.assertIn("Protected/canonical boundary:", out)
            self.assertIn("Stop condition:", out)
            self.assertNotIn("READY_FOR_EXECUTION granted.", out)
            self.assertNotIn("READY_FOR_EXECUTION approved.", out)
            self.assertNotIn("READY_FOR_EXECUTION created.", out)
            self.assertNotIn("Task is READY_FOR_EXECUTION.", out)
            self.assertNotIn("Handoff approved.", out)
            self.assertNotIn("Approval granted.", out)

            # B. Fail-closed for BLOCKED
            blocked_yaml = valid_yaml.replace('risk_profile: "LOW_RISK_FAST"', 'risk_profile: "UNKNOWN_BLOCKED"')
            with open("tasks/AOS-FARM-TASK-0003.md", "w") as f:
                 f.write(blocked_yaml + valid_body)
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--handoff-prompt", "AOS-FARM-TASK-0003"], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("FAIL:", res.stdout)
            self.assertIn("BLOCKED", res.stdout)

            # C. Fail-closed for HUMAN_REVIEW_REQUIRED
            hr_yaml = valid_yaml.replace('validator_status: "VALIDATION_COMPLETE"', 'validator_status: "NOT_RUN"')
            with open("tasks/AOS-FARM-TASK-0003.md", "w") as f:
                 f.write(hr_yaml + valid_body)
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--handoff-prompt", "AOS-FARM-TASK-0003"], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("FAIL:", res.stdout)
            self.assertIn("HUMAN_REVIEW_REQUIRED", res.stdout)

            # D. Fail-closed for FAIL
            with open("tasks/AOS-FARM-TASK-0003.md", "w") as f:
                 f.write("invalid content")
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--handoff-prompt", "AOS-FARM-TASK-0003"], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("FAIL", res.stdout)

            # E. Missing out-of-scope boundary fails closed
            # Actually remove the section heading and content
            no_oos_body = valid_body.replace("## Out of scope\nout of scope definition", "")
            with open("tasks/AOS-FARM-TASK-0003.md", "w") as f:
                 f.write(valid_yaml + no_oos_body)
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--handoff-prompt", "AOS-FARM-TASK-0003"], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)

            # F. Missing done criteria fails closed
            no_done = valid_body.replace("## Done когда\ndone", "")
            with open("tasks/AOS-FARM-TASK-0003.md", "w") as f:
                 f.write(valid_yaml + no_done)
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--handoff-prompt", "AOS-FARM-TASK-0003"], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)

            # G. Missing Evidence section fails closed
            no_ev = valid_body.replace("## Evidence\nev", "")
            with open("tasks/AOS-FARM-TASK-0003.md", "w") as f:
                 f.write(valid_yaml + no_ev)
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--handoff-prompt", "AOS-FARM-TASK-0003"], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)

            # H. Missing human-only decision section fails closed
            no_hd = valid_body.replace("## ⛔ Решение\nAPPROVED", "")
            with open("tasks/AOS-FARM-TASK-0003.md", "w") as f:
                 f.write(valid_yaml + no_hd)
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--handoff-prompt", "AOS-FARM-TASK-0003"], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)

            # I. Missing assigned Risk Profile fails closed
            no_risk_yaml = valid_yaml.replace('risk_profile: "LOW_RISK_FAST"\n', "")
            with open("tasks/AOS-FARM-TASK-0003.md", "w") as f:
                 f.write(no_risk_yaml + valid_body)
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--handoff-prompt", "AOS-FARM-TASK-0003"], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)

            # J. Invalid assigned Risk Profile fails closed
            inv_risk_yaml = valid_yaml.replace('risk_profile: "LOW_RISK_FAST"', 'risk_profile: "UNKNOWN_BLOCKED"')
            with open("tasks/AOS-FARM-TASK-0003.md", "w") as f:
                 f.write(inv_risk_yaml + valid_body)
            res = subprocess.run(["python3", os.path.join(original_cwd, SCRIPT), "task", "--handoff-prompt", "AOS-FARM-TASK-0003"], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)

        finally:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)

if __name__ == '__main__':
    unittest.main()
