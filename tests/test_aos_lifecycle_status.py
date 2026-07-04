import subprocess
import json
import sys

SCRIPT_PATH = "aos/scripts/aos_lifecycle_status.py"

def test_markdown_output():
    result = subprocess.run([sys.executable, SCRIPT_PATH, "--markdown"], capture_output=True, text=True)
    assert result.returncode == 0
    output = result.stdout
    
    assert "Generated status summary is not approval." in output
    assert "UNKNOWN is not OK" in output
    assert "NOT_RUN is not PASS" in output
    assert "PASS is not approval" in output

def test_json_output():
    result = subprocess.run([sys.executable, SCRIPT_PATH, "--json"], capture_output=True, text=True)
    assert result.returncode == 0
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, "Output is not valid JSON"
        
    required_keys = [
        "schema_version", "generated_at", "project", "branch",
        "head", "origin_dev", "origin_main", "working_tree",
        "detected_task", "detected_lifecycle_phase", "last_completed_task",
        "last_remote_closure", "analysis_status", "evidence",
        "missing_evidence", "open_unknowns", "warnings",
        "next_required_human_checkpoint", "allowed_next_actions",
        "forbidden_actions", "source_of_truth_note", "approval_note", "notes"
    ]
    
    for key in required_keys:
        assert key in data, f"Missing key in JSON output: {key}"

def test_next_guidance_output():
    result = subprocess.run([sys.executable, SCRIPT_PATH, "--next"], capture_output=True, text=True)
    assert result.returncode == 0
    output = result.stdout
    
    assert "Action executed: no" in output
    assert "Next safe checkpoint is guidance only" in output
    assert "It is not authorization" in output
