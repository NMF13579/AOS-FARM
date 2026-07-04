import subprocess
import json
import sys

SCRIPT_PATH = "aos/scripts/aos_review_package.py"

def run_script(*args):
    cmd = [sys.executable, SCRIPT_PATH] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True)

def test_human_review_mode():
    result = run_script("--mode", "human-review", "--task-id", "TEST", "--target-branch", "dev")
    assert result.returncode == 0
    
    assert "Review package is not approval" in result.stdout
    assert "Commit authorization is not push authorization" in result.stdout
    assert "Push authorization is not release authorization" in result.stdout
    assert "UNKNOWN is not OK" in result.stdout
    assert "NOT_RUN is not PASS" in result.stdout
    assert "PASS is not approval" in result.stdout

def test_commit_authorization_mode():
    result = run_script("--mode", "commit-authorization", "--task-id", "TEST", "--target-branch", "dev")
    assert result.returncode == 0
    assert "**Mode:** commit-authorization" in result.stdout

def test_push_authorization_mode():
    result = run_script("--mode", "push-authorization", "--task-id", "TEST", "--target-branch", "dev")
    assert result.returncode == 0
    assert "**Mode:** push-authorization" in result.stdout

def test_remote_closure_mode():
    result = run_script("--mode", "remote-closure", "--task-id", "TEST", "--target-branch", "dev")
    assert result.returncode == 0
    assert "**Mode:** remote-closure" in result.stdout

def test_json_output():
    result = run_script("--mode", "human-review", "--task-id", "TEST", "--target-branch", "dev", "--format", "json")
    assert result.returncode == 0
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, "Output is not valid JSON"
        
    assert data["mode"] == "human-review"
    assert data["task"] == "TEST"
