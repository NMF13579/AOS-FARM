import json
import subprocess
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, str(Path(__file__).parent.parent / "aos" / "scripts"))
import aos_duplicate_workspace_check as checker

@pytest.fixture
def temp_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    tracked = set()
    untracked = set()
    staged = set()
    return repo, tracked, untracked, staged

def run_checker(repo, tracked, untracked, staged, json_mode=True):
    with patch("aos_duplicate_workspace_check.get_repo_root", return_value=repo), \
         patch("aos_duplicate_workspace_check.get_git_state", return_value=(tracked, untracked, staged)), \
         patch("sys.argv", ["aos_duplicate_workspace_check.py"] + (["--json"] if json_mode else [])):
        try:
            with patch("sys.stdout") as mock_stdout:
                checker.main()
        except SystemExit as e:
            if json_mode:
                output = "".join(call[0][0] for call in mock_stdout.write.call_args_list)
                return e.code, json.loads(output)
            output = "".join(call[0][0] for call in mock_stdout.write.call_args_list)
            return e.code, output
    return None, None

def test_clean_workspace(temp_repo):
    repo, tr, untr, stg = temp_repo
    (repo / "file.py").write_text("hello")
    (repo / "version2.py").write_text("hello")
    (repo / "final-report.md").write_text("hello")
    
    code, out = run_checker(repo, tr, untr, stg)
    assert code == 0
    assert out["final_status"] == "PASS"
    assert out["repository_root"] == "."
    assert out["summary"]["suspicious_count"] == 0

def test_exact_duplicates(temp_repo):
    repo, tr, untr, stg = temp_repo
    
    (repo / "file.py").write_text("hello")
    (repo / "file 2.py").write_text("hello")
    (repo / "file (1).md").write_text("hello")
    (repo / "file.md").write_text("hello")
    (repo / "file copy.json").write_text("{}")
    (repo / "file.json").write_text("{}")
    
    code, out = run_checker(repo, tr, untr, stg)
    assert code == 1
    assert out["final_status"] == "FAILED_OR_BLOCKED"
    assert out["summary"]["exact_duplicate_count"] == 3

def test_divergent_and_conflicted_copy(temp_repo):
    repo, tr, untr, stg = temp_repo
    (repo / "file.md").write_text("canonical")
    (repo / "file conflicted copy.md").write_text("conflict")
    
    code, out = run_checker(repo, tr, untr, stg)
    assert code == 2
    assert out["final_status"] == "HUMAN_REVIEW_REQUIRED"
    assert out["summary"]["content_diverged_count"] == 1
    assert out["items"][0]["classification"] == "CONTENT_DIVERGED"

def test_orphan_pair(temp_repo):
    repo, tr, untr, stg = temp_repo
    (repo / "orphan copy.txt").write_text("hello")
    
    code, out = run_checker(repo, tr, untr, stg)
    assert code == 3
    assert out["final_status"] == "UNKNOWN_BLOCKED"
    assert out["summary"]["orphan_count"] == 1

def test_git_tracked_untracked_staged(temp_repo):
    repo, tr, untr, stg = temp_repo
    (repo / "f.txt").write_text("x")
    (repo / "f copy.txt").write_text("x")
    (repo / "g.txt").write_text("x")
    (repo / "g copy.txt").write_text("x")
    (repo / "h.txt").write_text("x")
    (repo / "h copy.txt").write_text("x")
    
    tr.add("f copy.txt")
    untr.add("g copy.txt")
    stg.add("h copy.txt")
    
    code, out = run_checker(repo, tr, untr, stg)
    assert out["summary"]["tracked_duplicate_count"] == 1
    assert out["summary"]["untracked_duplicate_count"] == 1
    assert out["summary"]["staged_duplicate_count"] == 1

def test_nested_duplicate(temp_repo):
    repo, tr, untr, stg = temp_repo
    nested = repo / "d1" / "d2"
    nested.mkdir(parents=True)
    (nested / "f.txt").write_text("x")
    (nested / "f copy.txt").write_text("x")
    
    code, out = run_checker(repo, tr, untr, stg)
    assert code == 1
    assert out["summary"]["exact_duplicate_count"] == 1
    assert out["items"][0]["duplicate_path"] == str(Path("d1/d2/f copy.txt"))

def test_deterministic_item_ordering(temp_repo):
    repo, tr, untr, stg = temp_repo
    names = ["z", "a", "m"]
    for n in names:
        (repo / f"{n}.txt").write_text("x")
        (repo / f"{n} copy.txt").write_text("x")
        
    code, out = run_checker(repo, tr, untr, stg)
    paths = [item["duplicate_path"] for item in out["items"]]
    assert paths == ["a copy.txt", "m copy.txt", "z copy.txt"]

def test_external_symlink(temp_repo, tmp_path):
    repo, tr, untr, stg = temp_repo
    external = tmp_path / "ext.txt"
    external.write_text("x")
    (repo / "f.txt").write_text("x")
    os.symlink(external, repo / "f copy.txt")
    
    code, out = run_checker(repo, tr, untr, stg)
    assert code == 3
    assert out["summary"]["ambiguous_count"] == 1

def test_unreadable_file(temp_repo):
    repo, tr, untr, stg = temp_repo
    (repo / "f.txt").write_text("x")
    (repo / "f copy.txt").write_text("x")
    
    with patch("aos_duplicate_workspace_check.get_sha256", side_effect=PermissionError("Access denied")):
        code, out = run_checker(repo, tr, untr, stg)
        assert code == 3
        assert out["summary"]["ambiguous_count"] == 1
        assert "errors" in out and len(out["errors"]) > 0

def test_git_command_failure(temp_repo):
    repo, tr, untr, stg = temp_repo
    with patch("aos_duplicate_workspace_check.get_repo_root", return_value=repo), \
         patch("aos_duplicate_workspace_check.get_git_state", return_value=(None, None, None)), \
         patch("sys.argv", ["aos_duplicate_workspace_check.py", "--json"]):
        try:
            with patch("sys.stdout") as mock_stdout:
                checker.main()
        except SystemExit as e:
            assert e.code == 3
            output = "".join(call[0][0] for call in mock_stdout.write.call_args_list)
            out = json.loads(output)
            assert out["final_status"] == "UNKNOWN_BLOCKED"
            assert not out["scan_complete"]

def test_scan_failure(temp_repo):
    repo, tr, untr, stg = temp_repo
    with patch("os.walk", side_effect=Exception("Disk error")):
        code, out = run_checker(repo, tr, untr, stg)
        assert code == 3
        assert out["final_status"] == "UNKNOWN_BLOCKED"
        assert not out["scan_complete"]

def test_help_no_scan(temp_repo):
    repo, tr, untr, stg = temp_repo
    with patch("sys.argv", ["aos_duplicate_workspace_check.py", "--help"]), \
         patch("sys.stdout"):
        try:
            checker.main()
        except SystemExit as e:
            assert e.code == 0

def test_human_readable_output(temp_repo):
    repo, tr, untr, stg = temp_repo
    (repo / "f.txt").write_text("x")
    (repo / "f copy.txt").write_text("x")
    code, out = run_checker(repo, tr, untr, stg, json_mode=False)
    assert "Final Status: FAILED_OR_BLOCKED" in out
    assert "Exact Duplicate Count: 1" in out

def test_no_filesystem_writes(temp_repo):
    repo, tr, untr, stg = temp_repo
    (repo / "f.txt").write_text("x")
    (repo / "f copy.txt").write_text("x")
    before = list(repo.rglob("*"))
    run_checker(repo, tr, untr, stg)
    after = list(repo.rglob("*"))
    assert before == after
