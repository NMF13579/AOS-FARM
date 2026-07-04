import subprocess
import json
import sys
import os

SCRIPT_PATH = "aos/scripts/aos_handoff_summary.py"

def test_markdown_output():
    result = subprocess.run([sys.executable, SCRIPT_PATH, "--markdown"], capture_output=True, text=True)
    assert result.returncode == 0
    output = result.stdout
    
    assert "Generated handoff summary is not approval" in output
    assert "Not Source of Truth" in output
    assert "UNKNOWN is not OK" in output
    assert "NOT_RUN is not PASS" in output
    assert "PASS is not approval" in output

def test_default_output():
    result = subprocess.run([sys.executable, SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0
    output = result.stdout
    
    assert "Generated handoff summary is not approval" in output
    assert "Not Source of Truth" in output

def test_json_output():
    result = subprocess.run([sys.executable, SCRIPT_PATH, "--json"], capture_output=True, text=True)
    assert result.returncode == 0
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, "Output is not valid JSON"

def test_write_outside_reports():
    result = subprocess.run([sys.executable, SCRIPT_PATH, "--write", "/tmp/invalid_path.md"], capture_output=True, text=True)
    assert result.returncode == 0
    output = result.stdout
    
    assert "analysis_status: BLOCKED" in output
    assert "output path outside reports/" in output
