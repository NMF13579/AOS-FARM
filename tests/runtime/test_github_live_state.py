import json
import pytest
from unittest.mock import MagicMock
from aos.runtime.github_live_state import GitHubLiveStateCollector
from aos.runtime.github_readonly_transport import GitHubReadOnlyTransport, GitHubTransportError

def test_collect_repository_identity():
    mock_transport = MagicMock()
    mock_transport.request_rest.return_value = {
        "owner": {"login": "owner"},
        "name": "repo",
        "node_id": "MDQ6",
        "default_branch": "main",
        "visibility": "public"
    }
    
    collector = GitHubLiveStateCollector(transport=mock_transport)
    result = collector.collect_repository_identity("owner", "repo")
    
    assert result["owner_name"] == "owner"
    assert result["repository_name"] == "repo"
    assert result["repository_node_id"] == "MDQ6"
    assert result["default_branch"] == "main"
    assert result["visibility"] == "public"
    mock_transport.request_rest.assert_called_with("/repos/owner/repo")

def test_collect_pull_request_core_unknown_head():
    mock_transport = MagicMock()
    # Missing head.repo
    mock_transport.request_rest.return_value = {
        "base": {"repo": {"node_id": "BASE"}},
        "head": {"repo": None}
    }
    
    collector = GitHubLiveStateCollector(transport=mock_transport)
    result = collector.collect_pull_request_core("owner", "repo", 123)
    
    assert result["status"] == "UNKNOWN"
    assert result["error_code"] == "HEAD_REPOSITORY_IDENTITY_UNKNOWN"

def test_collect_commits_pagination():
    mock_transport = MagicMock()
    # Return two pages of commits, then empty
    mock_transport.request_rest.side_effect = [
        [{"sha": "abc"}] * 100, # Page 1
        [{"sha": "def"}] * 50,  # Page 2
        []                      # Page 3
    ]
    
    collector = GitHubLiveStateCollector(transport=mock_transport)
    result = collector.collect_commits("owner", "repo", 123)
    
    assert result["status"] == "PASS"
    assert result["complete"] is True
    assert result["count"] == 2 # "abc" and "def", since duplicates are filtered out
    assert result["oids"] == ["abc", "def"]
    assert result["pages_fetched"] == 2

def test_collect_commits_limit_reached():
    mock_transport = MagicMock()
    # Return 10 full pages to reach limit
    def mock_req(path):
        return [{"sha": f"commit_{i}"} for i in range(100)]
    mock_transport.request_rest.side_effect = mock_req
    
    collector = GitHubLiveStateCollector(transport=mock_transport)
    # Default max_pages is 10, max_commits is 250
    result = collector.collect_commits("owner", "repo", 123)
    
    assert result["status"] == "UNKNOWN"
    assert result["truncated"] is True
    assert result["error_code"] == "COLLECTION_LIMIT_REACHED"

def test_collect_changed_paths():
    mock_transport = MagicMock()
    mock_transport.request_rest.side_effect = [
        [{"filename": "a.txt"}, {"filename": "b/c.txt"}],
        []
    ]
    
    collector = GitHubLiveStateCollector(transport=mock_transport)
    result = collector.collect_changed_paths("owner", "repo", 123)
    
    assert result["status"] == "PASS"
    assert result["complete"] is True
    assert result["paths"] == ["a.txt", "b/c.txt"]

def test_collect_required_checks():
    mock_transport = MagicMock()
    mock_transport.request_rest.return_value = {
        "check_runs": [
            {"name": "test1", "status": "completed", "conclusion": "success"},
            {"name": "test2", "status": "completed", "conclusion": "failure"},
            {"name": "test3", "status": "in_progress"}
        ]
    }
    
    collector = GitHubLiveStateCollector(transport=mock_transport)
    result = collector.collect_required_checks("owner", "repo", "headoid")
    
    assert result["exact_head_oid"] == "headoid"
    assert len(result["pending_required_checks"]) == 1
    assert len(result["failing_required_checks"]) == 1
    assert result["pending_required_checks"][0]["name"] == "test3"
    assert result["failing_required_checks"][0]["name"] == "test2"
    
def test_unexpected_network_call_fails():
    # Because of fail_on_network fixture, this is guaranteed
    pass

import urllib.request
import socket
import builtins
import subprocess
import pathlib

@pytest.fixture(autouse=True)
def fail_on_network(monkeypatch):
    def block_network(*args, **kwargs):
        raise AssertionError("unexpected live network call")
    monkeypatch.setattr(urllib.request, "urlopen", block_network)
    monkeypatch.setattr(socket, "socket", block_network)

@pytest.fixture(autouse=True)
def fail_on_side_effects(monkeypatch):
    def block_action(*args, **kwargs):
        raise AssertionError("unexpected filesystem or subprocess call")
    
    # We shouldn't block builtins.open completely as pytest needs it, 
    # but we can wrap it to block 'w', 'a' modes
    original_open = builtins.open
    def secure_open(file, mode='r', *args, **kwargs):
        if 'w' in mode or 'a' in mode or '+' in mode:
            block_action()
        return original_open(file, mode, *args, **kwargs)
    monkeypatch.setattr(builtins, "open", secure_open)
    
    monkeypatch.setattr(pathlib.Path, "write_text", block_action)
    monkeypatch.setattr(pathlib.Path, "write_bytes", block_action)
    monkeypatch.setattr(subprocess, "run", block_action)
    monkeypatch.setattr(subprocess, "Popen", block_action)
    monkeypatch.setattr(subprocess, "call", block_action)

