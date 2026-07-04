import subprocess
import json
import sys

SCRIPT_PATH = "aos/scripts/aos_baseline_summary.py"

def test_markdown_output():
    result = subprocess.run([sys.executable, SCRIPT_PATH, "--markdown"], capture_output=True, text=True)
    assert result.returncode == 0
    output = result.stdout
    
    assert "PASS is not approval" in output
    assert "UNKNOWN is not OK" in output
    assert "No commit was performed" in output
    assert "No push was performed" in output

def test_json_output():
    result = subprocess.run([sys.executable, SCRIPT_PATH, "--json"], capture_output=True, text=True)
    assert result.returncode == 0
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, "Output is not valid JSON"
        
    required_keys = [
        "schema_version", "generated_at", "project", "target_branch",
        "current_branch", "head_sha", "origin_dev_sha", "origin_main_sha",
        "ls_remote_dev_sha", "ls_remote_main_sha", "origin_dev_head_ahead_behind",
        "origin_main_head_ahead_behind", "origin_main_origin_dev_ahead_behind",
        "working_tree_summary", "working_tree_clean", "staged_files_count",
        "modified_files_count", "untracked_files_count", "untracked_files_summary",
        "last_commit_subject", "last_commit_changed_files", "analysis_status",
        "warnings", "notes"
    ]
    
    for key in required_keys:
        assert key in data, f"Missing key in JSON output: {key}"

def test_safety_notes_in_markdown():
    result = subprocess.run([sys.executable, SCRIPT_PATH, "--markdown"], capture_output=True, text=True)
    output = result.stdout
    
    safety_notes = [
        "Generated baseline summary is not Source of Truth.",
        "Generated baseline summary is not approval.",
        "Baseline Evidence is not approval.",
        "UNKNOWN is not OK.",
        "NOT_RUN is not PASS.",
        "PASS is not approval.",
        "No commit was performed.",
        "No push was performed."
    ]
    
    for note in safety_notes:
        assert note in output, f"Missing safety note in Markdown output: {note}"
