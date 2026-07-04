import subprocess
import json
import sys

SCRIPT_PATH = "aos/scripts/aos_remote_closure_check.py"

def test_markdown_output_dev():
    result = subprocess.run([sys.executable, SCRIPT_PATH, "--target", "dev", "--markdown"], capture_output=True, text=True)
    assert result.returncode == 0
    output = result.stdout
    
    assert "Evidence, not approval" in output
    assert "not release authorization" in output
    assert "UNKNOWN is not OK" in output
    assert "NOT_RUN is not PASS" in output
    assert "PASS is not approval" in output
    assert "Target: dev" in output

def test_markdown_output_main():
    result = subprocess.run([sys.executable, SCRIPT_PATH, "--target", "main", "--markdown"], capture_output=True, text=True)
    assert result.returncode == 0
    output = result.stdout
    assert "Target: main" in output

def test_json_output():
    result = subprocess.run([sys.executable, SCRIPT_PATH, "--target", "dev", "--json"], capture_output=True, text=True)
    assert result.returncode == 0
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, "Output is not valid JSON"
        
    required_keys = [
        "schema_version", "generated_at", "project", "target",
        "current_branch", "head_sha", "origin_target_sha",
        "ls_remote_target_sha", "head_equals_origin_target",
        "head_equals_ls_remote_target", "working_tree_clean",
        "origin_main_relation_if_target_dev", "ahead_behind_state",
        "last_commit_subject", "last_commit_changed_files",
        "analysis_status", "warnings", "notes"
    ]
    
    for key in required_keys:
        assert key in data, f"Missing key in JSON output: {key}"
    
    assert data["target"] == "dev"
