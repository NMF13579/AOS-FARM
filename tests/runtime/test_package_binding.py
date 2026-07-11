import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from aos.runtime.package_binding import (
    normalize_remote_url,
    aggregate_binding_results,
    bind_platform,
    bind_repository,
    AOSBindingError,
    _get_baseline_state
)

def test_normalize_remote_url():
    expected = "github.com/nmf13579/aos-farm"
    assert normalize_remote_url("git@github.com:NMF13579/AOS-FARM.git") == "github.com/NMF13579/AOS-FARM"
    assert normalize_remote_url("ssh://git@github.com/nmf13579/aos-farm.git") == expected
    assert normalize_remote_url("https://github.com/nmf13579/aos-farm.git") == expected
    assert normalize_remote_url("https://github.com/nmf13579/aos-farm") == expected

def test_normalize_remote_url_rejection():
    with pytest.raises(AOSBindingError) as exc:
        normalize_remote_url("file:///tmp/repo.git")
    assert "LOCAL_REMOTE_BLOCKED" in str(exc.value)

    with pytest.raises(AOSBindingError) as exc:
        normalize_remote_url("../repo.git")
    assert "LOCAL_REMOTE_BLOCKED" in str(exc.value)

    with pytest.raises(AOSBindingError) as exc:
        normalize_remote_url("/tmp/repo")
    assert "LOCAL_REMOTE_BLOCKED" in str(exc.value)

def test_aggregate_binding_results():
    assert aggregate_binding_results([
        {"status": "PASS"},
        {"status": "PASS"}
    ])["status"] == "PASS"

    assert aggregate_binding_results([
        {"status": "PASS"},
        {"status": "FAIL"}
    ])["status"] == "FAIL"

    assert aggregate_binding_results([
        {"status": "FAIL"},
        {"status": "BLOCKED"}
    ])["status"] == "BLOCKED"

    assert aggregate_binding_results([
        {"status": "BLOCKED"},
        {"status": "UNKNOWN_BLOCKED"}
    ])["status"] == "UNKNOWN_BLOCKED"
    
    res = aggregate_binding_results([
        {"check": "a", "status": "NOT_RUN"},
        {"check": "b", "status": "PASS"}
    ], required_checks={"a"})
    assert res["status"] == "UNKNOWN_BLOCKED"

def test_bind_platform():
    package = {
        "platform_profile": "mac_m1",
        "execution_environment_id": "env_1",
        "execution_mode": "strict"
    }
    
    res = bind_platform(package, "mac_m1", "env_1", "strict")
    assert all(r["status"] == "PASS" for r in res)
    
    res_mismatch = bind_platform(package, "mac_intel", "env_1", "strict")
    for r in res_mismatch:
        if r["check"] == "platform_profile":
            assert r["status"] == "BLOCKED"
            assert r["error_code"] == "PLATFORM_PROFILE_MISMATCH"

def test_bind_repository_mocked(monkeypatch):
    import aos.runtime.package_binding as pb
    
    def mock_run_git(args, cwd):
        if args == ["rev-parse", "--show-toplevel"]:
            return cwd
        if args == ["remote"]:
            return "origin"
        if args == ["remote", "get-url", "origin"]:
            return "https://github.com/test/repo.git"
        if args == ["branch", "--show-current"]:
            return "main"
        if args == ["rev-parse", "HEAD"]:
            return "a" * 40
        if args == ["status", "--porcelain=v1"]:
            return ""
        raise pb.AOSBindingError("mock error")
        
    monkeypatch.setattr(pb, "_run_git", mock_run_git)
    monkeypatch.setattr(pb.Path, "exists", lambda self: True)
    monkeypatch.setattr(pb.Path, "is_dir", lambda self: True)
    monkeypatch.setattr(pb.Path, "resolve", lambda self: self)
    
    package = {
        "remote_identity": "github.com/test/repo",
        "branch": "main",
        "baseline_head": "a" * 40
    }
    
    res = pb.bind_repository(package, "/dummy")
    for r in res:
        assert r["status"] == "PASS"

    package_mismatch = {
        "remote_identity": "github.com/wrong/repo",
        "branch": "dev",
        "baseline_head": "b" * 40
    }
    res_mismatch = pb.bind_repository(package_mismatch, "/dummy")
    
    for r in res_mismatch:
        if r["check"] == "baseline_state":
            assert r["status"] == "PASS"
        else:
            assert r["status"] == "BLOCKED"

def test_git_unmerged_state(monkeypatch):
    import aos.runtime.package_binding as pb
    def mock_run_git(args, cwd):
        if args == ["status", "--porcelain=v1"]:
            return "UU file.txt"
        return ""
    monkeypatch.setattr(pb, "_run_git", mock_run_git)
    
    with pytest.raises(AOSBindingError) as exc:
        pb._get_baseline_state("/dummy")
    assert "UNMERGED_STATE_BLOCKED" in str(exc.value)

def test_git_detached_head_blocks(monkeypatch):
    import aos.runtime.package_binding as pb
    def mock_run_git(args, cwd):
        if args == ["rev-parse", "--show-toplevel"]:
            return cwd
        if args == ["remote"]: return "origin"
        if args == ["remote", "get-url", "origin"]: return "https://github.com/test/repo.git"
        if args == ["branch", "--show-current"]:
            return "" # Detached HEAD empty string from git
        if args == ["rev-parse", "HEAD"]: return "a"*40
        if args == ["status", "--porcelain=v1"]: return ""
        return ""
    monkeypatch.setattr(pb, "_run_git", mock_run_git)
    monkeypatch.setattr(pb.Path, "exists", lambda self: True)
    monkeypatch.setattr(pb.Path, "is_dir", lambda self: True)
    monkeypatch.setattr(pb.Path, "resolve", lambda self: self)
    
    package = {
        "remote_identity": "github.com/test/repo",
        "branch": "main",
        "baseline_head": "a" * 40
    }
    res = pb.bind_repository(package, "/dummy")
    for r in res:
        if r["check"] == "branch":
            assert r["status"] == "BLOCKED"
            assert r["error_code"] == "DETACHED_HEAD_BLOCKED"
