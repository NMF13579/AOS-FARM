# AOS-FARM.675 Divergent Review

## aos/scripts/aos_architecture_document_check 2.py vs aos/scripts/aos_architecture_document_check.py

### Unified Diff
```diff
diff --git a/aos/scripts/aos_architecture_document_check 2.py b/aos/scripts/aos_architecture_document_check.py
index d7c81fb..c9230ac 100644
--- a/aos/scripts/aos_architecture_document_check 2.py	
+++ b/aos/scripts/aos_architecture_document_check.py
@@ -753,7 +753,8 @@ def get_validate_all_report():
         ("evidence", "aos/docs/architecture/review/architecture-decision-evidence-packet.md"),
         ("matrix", "aos/docs/architecture/review/stack-fit-matrix.md"),
         ("matrix", "aos/docs/architecture/review/pattern-fit-matrix.md"),
-        ("criteria", "aos/docs/architecture/review/architecture-decision-criteria.md")
+        ("criteria", "aos/docs/architecture/review/architecture-decision-criteria.md"),
+        ("task-breakdown", "tests/fixtures/architecture/valid_task_breakdown_traced.md")
     ]
 
     registry_files = [
@@ -786,14 +787,6 @@ def get_validate_all_report():
         all_auth.extend(auth_findings)
         all_human_review.extend(human_review_findings)
 
-    checks_report.append({
-        "checker": "task-breakdown",
-        "result": "NOT_RUN",
-        "reason": "checker_not_implemented",
-        "counted_as_pass": False,
-        "blocks_overall_pass": False
-    })
-
     structural_results = run_structural_checks()
     for res in structural_results:
         status = res.get("status")

```

### AST Analysis
- Functions only in duplicate: None
- Functions only in counterpart: None
- Classes only in duplicate: None
- Classes only in counterpart: None
- Test methods only in duplicate: None
- Test methods only in counterpart: None

## aos/scripts/aos_lifecycle_state 2.py vs aos/scripts/aos_lifecycle_state.py

### Unified Diff
```diff
diff --git a/aos/scripts/aos_lifecycle_state 2.py b/aos/scripts/aos_lifecycle_state.py
index e0ac9f0..cb3fc8e 100644
--- a/aos/scripts/aos_lifecycle_state 2.py	
+++ b/aos/scripts/aos_lifecycle_state.py
@@ -22,6 +22,7 @@ VALID_LIFECYCLE_STATES = {
     "HUMAN_REVIEW_REQUIRED",
     "APPROVED",
     "REJECTED",
+    "CLOSED",
     "NEEDS_CHANGES",
     "BLOCKED",
     "UNKNOWN_BLOCKED",

```

### AST Analysis
- Functions only in duplicate: None
- Functions only in counterpart: None
- Classes only in duplicate: None
- Classes only in counterpart: None
- Test methods only in duplicate: None
- Test methods only in counterpart: None

## aos/templates/architecture-brief-template 2.md vs aos/templates/architecture-brief-template.md

### Unified Diff
```diff
diff --git a/aos/templates/architecture-brief-template 2.md b/aos/templates/architecture-brief-template.md
index b93cbce..5118753 100644
--- a/aos/templates/architecture-brief-template 2.md	
+++ b/aos/templates/architecture-brief-template.md
@@ -35,6 +35,42 @@ unknown_records:
 conflict_records: 
 human_checkpoints: 
 
+## How to use this template
+
+Use this template after Architecture Input Intake to draft candidate architecture evidence for human review.
+
+This artifact may summarize selected and rejected candidate options, but it must not approve architecture, assign Risk Profile, authorize implementation, or create an executable Task Brief.
+
+## Required content
+
+- decision question
+- source Technical Assignment reference
+- source Architecture Input Intake reference
+- selected option candidates
+- rejected option candidates
+- assumptions
+- constraints
+- tradeoffs
+- risks
+- unresolved UNKNOWN records
+- conflict records
+- downstream Task Brief impact
+- validation command/output reference
+- human review questions
+- human checkpoints required
+
+## Prohibited claims
+
+- approved: true
+- approval_status: APPROVED
+- status: READY_FOR_EXECUTION
+- execution_authorized: true
+- implementation_authorized: true
+- release_authorized: true
+- risk_profile_assigned_by_agent: true
+- validator PASS means approval
+- no human review required
+
 ## Allowed Statuses
 - DRAFT
 - HUMAN_REVIEW_REQUIRED
@@ -51,3 +87,13 @@ human_checkpoints:
 - Architecture Brief does not authorize commit.
 - Architecture Brief does not authorize push.
 - Architecture Brief does not authorize release.
+
+## Validation
+
+Use validation as Evidence only:
+
+```bash
+python3 aos/scripts/aos_architecture_document_check.py brief --file <path>
+```
+
+Validator PASS is not approval. Validator PASS does not authorize Task Brief execution.

```

### Markdown Analysis
- Headings only in duplicate: None
- Headings only in counterpart: ## Prohibited claims, ## Validation, ## How to use this template, ## Required content
- Unique non-empty paragraphs in duplicate: 0
- Unique non-empty paragraphs in counterpart: 7

## aos/templates/architecture-input-intake-template 2.md vs aos/templates/architecture-input-intake-template.md

### Unified Diff
```diff
diff --git a/aos/templates/architecture-input-intake-template 2.md b/aos/templates/architecture-input-intake-template.md
index 1554591..c3d3e15 100644
--- a/aos/templates/architecture-input-intake-template 2.md	
+++ b/aos/templates/architecture-input-intake-template.md
@@ -34,6 +34,12 @@ unknown_records:
 conflict_records: 
 human_checkpoints: 
 
+## How to use this template
+
+Fill this template after a Technical Assignment exists and before Architecture Decision Layer or Task Breakdown.
+
+This artifact captures inputs and uncertainties. It does not approve architecture, select a stack, assign Risk Profile, create task candidates, create a Task Brief, or authorize execution.
+
 ## Modes
 Supported modes:
 - NO_ARCHITECTURE_INPUT
@@ -43,9 +49,45 @@ Supported modes:
 - REFERENCE_ARCHITECTURE
 - UNKNOWN_BLOCKED
 
+## Required content
+
+- source Technical Assignment reference
+- selected input mode
+- source inputs and external document references
+- explicit constraints
+- explicit assumptions
+- explicit non-goals
+- unresolved UNKNOWN records
+- conflict records
+- downstream Task Brief impact
+- human checkpoints required
+
+## Prohibited claims
+
+- approved: true
+- execution_authorized: true
+- implementation_authorized: true
+- risk_profile_assigned_by_agent: true
+- default_stack_selected: true
+- no human review required
+
 ## Safety Constraints
 - External document is untrusted input.
 - External document is not approval.
 - Stack preset is recommendation, not approval.
 - Reference architecture is reference only.
 - Agent inference never has authority.
+
+## Validation
+
+Use validation as Evidence only:
+
+```bash
+python3 aos/scripts/aos_architecture_document_check.py validate-all --json
+```
+
+Validator PASS is not approval. Validator NOT_RUN is not PASS.
+
+## Human review boundary
+
+If this intake identifies architecture-relevant decisions, unresolved UNKNOWNs, conflicts, or downstream task impact, stop at `HUMAN_REVIEW_REQUIRED` or `UNKNOWN_BLOCKED`.

```

### Markdown Analysis
- Headings only in duplicate: None
- Headings only in counterpart: ## Prohibited claims, ## Required content, ## How to use this template, ## Validation, ## Human review boundary
- Unique non-empty paragraphs in duplicate: 0
- Unique non-empty paragraphs in counterpart: 8

## aos/templates/compact/compact-safe-path-template 2.md vs aos/templates/compact/compact-safe-path-template.md

### Unified Diff
```diff
diff --git a/aos/templates/compact/compact-safe-path-template 2.md b/aos/templates/compact/compact-safe-path-template.md
index 8ac9311..2c4b220 100644
--- a/aos/templates/compact/compact-safe-path-template 2.md	
+++ b/aos/templates/compact/compact-safe-path-template.md
@@ -220,6 +220,13 @@ Checklist:
 - Push authorization does not grant merge.
 - Push authorization does not grant release.
 - Merge authorization does not grant release.
+- Merge authorization is not dev push authorization.
+- Dev push requires separate exact phrase: AOS PUSH DEV OK AOS-FARM.<ID>.
+- Feature branch push authorization is not dev push authorization.
+- Combined local integration + remote write command is forbidden.
+- Post-merge local verification required before dev push.
+- Accepted violation state is not authorization precedent.
+- Merge type must be explicit or default --ff-only.
 - Do not request push authorization in the same block as commit authorization.
 
 ## 16. General Boundary Reminder

```

### Markdown Analysis
- Headings only in duplicate: None
- Headings only in counterpart: None
- Unique non-empty paragraphs in duplicate: 1
- Unique non-empty paragraphs in counterpart: 1

## aos/templates/task-breakdown-from-architecture-template 2.md vs aos/templates/task-breakdown-from-architecture-template.md

### Unified Diff
```diff
diff --git a/aos/templates/task-breakdown-from-architecture-template 2.md b/aos/templates/task-breakdown-from-architecture-template.md
index a9574f4..76dc13d 100644
--- a/aos/templates/task-breakdown-from-architecture-template 2.md	
+++ b/aos/templates/task-breakdown-from-architecture-template.md
@@ -39,6 +39,36 @@ human_checkpoints:
 unknown_records:
 conflict_records:
 
+## How to use this template
+
+Use this template only after the architecture gate is resolved for the Technical Assignment.
+
+If architecture input was required, include the Architecture Brief, architecture decision Evidence, validation status, Human Architecture Checkpoint status, unresolved UNKNOWNs, and downstream scope boundary.
+
+This artifact creates task candidates for review. It does not create an approved Task Brief and does not authorize execution.
+
+## Required content
+
+- source Technical Assignment reference
+- source Architecture Brief reference
+- architecture decision Evidence reference
+- Human Architecture Checkpoint status
+- unresolved UNKNOWNs carried forward
+- conflict resolutions carried forward
+- downstream scope boundary
+- proposed Risk Profile only, not assigned Risk Profile
+- approval boundary
+- build step boundary
+
+## Prohibited claims
+
+- approved: true
+- status: READY_FOR_EXECUTION
+- execution_authorized: true
+- risk_profile_assigned_by_agent: true
+- task brief approved
+- validator PASS means approval
+
 ## Task candidate status values:
 - TASK_CANDIDATE_DRAFT
 - HUMAN_REVIEW_REQUIRED
@@ -51,3 +81,13 @@ conflict_records:
 - Without traceability, a task must not become APPROVED.
 - READY_FOR_QUEUE_REVIEW ≠ APPROVED.
 - READY_FOR_QUEUE_REVIEW ≠ READY_FOR_EXECUTION.
+
+## Validation
+
+Use validation as Evidence only:
+
+```bash
+python3 aos/scripts/aos_architecture_document_check.py task-breakdown --file <path>
+```
+
+Validator PASS is not approval and does not authorize execution.

```

### Markdown Analysis
- Headings only in duplicate: None
- Headings only in counterpart: ## Prohibited claims, ## Validation, ## How to use this template, ## Required content
- Unique non-empty paragraphs in duplicate: 0
- Unique non-empty paragraphs in counterpart: 8

## tests/test_aos_architecture_document_check 2.py vs tests/test_aos_architecture_document_check.py

### Unified Diff
```diff
diff --git a/tests/test_aos_architecture_document_check 2.py b/tests/test_aos_architecture_document_check.py
index 2ff8a81..2bbfd47 100644
--- a/tests/test_aos_architecture_document_check 2.py	
+++ b/tests/test_aos_architecture_document_check.py
@@ -549,12 +549,10 @@ human_weight_required: true
         checks = report.get("checks", [])
         self.assertTrue(len(checks) > 0)
         
-        not_run_checks = [c for c in checks if c.get("result") == "NOT_RUN"]
-        self.assertTrue(len(not_run_checks) > 0)
-        self.assertEqual(not_run_checks[0].get("checker"), "task-breakdown")
-        self.assertEqual(not_run_checks[0].get("reason"), "checker_not_implemented")
-        self.assertFalse(not_run_checks[0].get("counted_as_pass"))
-        self.assertFalse(not_run_checks[0].get("blocks_overall_pass"))
+        task_breakdown_checks = [c for c in checks if c.get("checker") == "task-breakdown"]
+        self.assertTrue(len(task_breakdown_checks) > 0)
+        self.assertEqual(task_breakdown_checks[0].get("result"), "PASS")
+        self.assertEqual(task_breakdown_checks[0].get("file"), "tests/fixtures/architecture/valid_task_breakdown_traced.md")
         
         output_str = json.dumps(report)
         self.assertNotIn('"APPROVED"', output_str)

```

### AST Analysis
- Functions only in duplicate: None
- Functions only in counterpart: None
- Classes only in duplicate: None
- Classes only in counterpart: None
- Test methods only in duplicate: None
- Test methods only in counterpart: None

## tests/test_aos_doctor 2.py vs tests/test_aos_doctor.py

### Unified Diff
```diff
diff --git a/tests/test_aos_doctor 2.py b/tests/test_aos_doctor.py
index 80f5824..45f4ea0 100644
--- a/tests/test_aos_doctor 2.py	
+++ b/tests/test_aos_doctor.py
@@ -1,6 +1,8 @@
 import unittest
 from unittest.mock import patch
 import sys
+import json
+import io
 from pathlib import Path
 
 current_dir = Path(__file__).parent.resolve()
@@ -11,8 +13,7 @@ import aos_doctor
 
 class TestAOSDoctor(unittest.TestCase):
 
-    def test_determine_overall_status_ran_0_tests(self):
-        # A test run with 0 tests is NOT a strong PASS
+    def test_determine_overall_status_ran_0_tests_unittest(self):
         results = [{
             "command": "python3 -m unittest discover -s tests -p test*.py",
             "status": "PASS",
@@ -22,24 +23,114 @@ class TestAOSDoctor(unittest.TestCase):
         overall = aos_doctor.determine_overall_status(results)
         self.assertEqual(overall, "FAILED_OR_BLOCKED")
         self.assertEqual(results[0]["status"], "FAILED")
-        self.assertEqual(results[0]["reason"], "Ran 0 tests is not a strong PASS")
+        self.assertEqual(results[0]["reason"], "0 tests executed is not a strong PASS")
+
+    def test_determine_overall_status_ran_0_tests_pytest(self):
+        results = [{
+            "command": "python3 -m pytest",
+            "status": "PASS",
+            "stdout": "collected 0 items",
+            "stderr": ""
+        }]
+        overall = aos_doctor.determine_overall_status(results)
+        self.assertEqual(overall, "FAILED_OR_BLOCKED")
+        self.assertEqual(results[0]["status"], "FAILED")
+        self.assertEqual(results[0]["reason"], "0 tests executed is not a strong PASS")
 
     def test_determine_overall_status_ran_n_tests(self):
-        # Normal tests PASS
         results = [{
-            "command": "python3 -m unittest discover -s tests -p test*.py",
+            "command": "python3 -m pytest",
             "status": "PASS",
-            "stdout": "Ran 5 tests in 0.010s\nOK",
+            "stdout": "503 passed in 67.97s",
             "stderr": ""
         }]
         overall = aos_doctor.determine_overall_status(results)
         self.assertEqual(overall, "PASS")
 
-    def test_explicit_unittest_discovery_path(self):
-        # Check that COMMANDS_TO_AGGREGATE includes the specific explicit path
+    def test_explicit_pytest_path(self):
         cmds = aos_doctor.COMMANDS_TO_AGGREGATE
-        has_explicit = any(c == ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test*.py"] for c in cmds)
+        has_explicit = any(c == [sys.executable, "-m", "pytest"] for c in cmds)
         self.assertTrue(has_explicit)
 
+    @patch('aos_doctor.subprocess.run')
+    def test_sys_executable_and_no_shell(self, mock_run):
+        for cmd in aos_doctor.COMMANDS_TO_AGGREGATE:
+            self.assertEqual(cmd[0], sys.executable)
+            
+        mock_run.return_value.returncode = 0
+        mock_run.return_value.stdout = ""
+        mock_run.return_value.stderr = ""
+        aos_doctor.run_command(["ls"])
+        mock_run.assert_called_with(["ls"], capture_output=True, text=True, timeout=120)
+
+    @patch('aos_doctor.run_command')
+    def test_missing_pytest_diagnostics(self, mock_run_command):
+        def side_effect(cmd):
+            if cmd == [sys.executable, "-c", "import pytest"]:
+                return {
+                    "command": " ".join(cmd),
+                    "status": "FAILED",
+                    "return_code": 1,
+                    "stdout": "",
+                    "stderr": "Traceback..."
+                }
+            return {
+                "command": " ".join(cmd),
+                "status": "PASS",
+                "return_code": 0,
+                "stdout": "503 passed in 60s" if "-m pytest" in " ".join(cmd) else "",
+                "stderr": ""
+            }
+        
+        mock_run_command.side_effect = side_effect
+        
+        with patch('sys.argv', ['aos_doctor.py', '--json']):
+            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
+                aos_doctor.main()
+                output = json.loads(mock_stdout.getvalue())
+        
+        pytest_check = next(r for r in output["results"] if r["command"] == f"{sys.executable} -c import pytest")
+        self.assertEqual(pytest_check["status"], "FAILED")
+        
+        self.assertIn("pytest", pytest_check["reason"])
+        self.assertIn(sys.executable, pytest_check["reason"])
+        self.assertIn("requirements-dev.txt", pytest_check["reason"])
+        self.assertIn(f"{sys.executable} -m pip install -r requirements-dev.txt", pytest_check["reason"])
+        
+        runner_check = next(r for r in output["results"] if "pytest" in r["command"] and "-m" in r["command"])
+        self.assertEqual(runner_check["status"], "NOT_RUN")
+        self.assertEqual(runner_check["reason"], "Skipped due to missing pytest dependency")
+        
+        self.assertEqual(len(output["results"]), len(aos_doctor.COMMANDS_TO_AGGREGATE))
+        self.assertEqual(output["overall_status"], "FAILED_OR_BLOCKED")
+        
+        pip_cmds = [cmd for cmd in aos_doctor.COMMANDS_TO_AGGREGATE if "pip" in cmd]
+        self.assertEqual(len(pip_cmds), 0)
+
+    @patch('aos_doctor.run_command')
+    def test_available_pytest(self, mock_run_command):
+        def side_effect(cmd):
+            return {
+                "command": " ".join(cmd),
+                "status": "PASS",
+                "return_code": 0,
+                "stdout": "503 passed in 60s" if "-m pytest" in " ".join(cmd) else "",
+                "stderr": ""
+            }
+        mock_run_command.side_effect = side_effect
+        
+        with patch('sys.argv', ['aos_doctor.py', '--json']):
+            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
+                aos_doctor.main()
+                output = json.loads(mock_stdout.getvalue())
+                
+        pytest_check = next(r for r in output["results"] if "import pytest" in r["command"])
+        self.assertEqual(pytest_check["status"], "PASS")
+        
+        runner_check = next(r for r in output["results"] if "-m pytest" in r["command"])
+        self.assertEqual(runner_check["status"], "PASS")
+        
+        self.assertEqual(output["overall_status"], "PASS")
+
 if __name__ == '__main__':
     unittest.main()

```

### AST Analysis
- Functions only in duplicate: test_explicit_unittest_discovery_path, test_determine_overall_status_ran_0_tests
- Functions only in counterpart: test_available_pytest, test_sys_executable_and_no_shell, test_explicit_pytest_path, test_determine_overall_status_ran_0_tests_pytest, test_determine_overall_status_ran_0_tests_unittest, test_missing_pytest_diagnostics, side_effect
- Classes only in duplicate: None
- Classes only in counterpart: None
- Test methods only in duplicate: test_explicit_unittest_discovery_path, test_determine_overall_status_ran_0_tests
- Test methods only in counterpart: test_available_pytest, test_sys_executable_and_no_shell, test_determine_overall_status_ran_0_tests_pytest, test_determine_overall_status_ran_0_tests_unittest, test_missing_pytest_diagnostics, test_explicit_pytest_path

### Special Case Analysis: tests/test_aos_doctor 2.py
4. Assertions in duplicate not in canonical: The duplicate contains a basic assertion `self.assertEqual(results[0]["reason"], "Ran 0 tests is not a strong PASS")`.
5. Covered by canonical test? Yes. The canonical test expands this into `test_determine_overall_status_ran_0_tests_unittest` and `...pytest` with more detailed assertions.
6. Recommendation: DELETE_DUPLICATE_KEEP_CANONICAL
7. Reason: The duplicate is an older version. All functional test coverage is already subsumed by the counterpart in a more robust way.
