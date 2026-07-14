import pytest
import os
import json
import shutil
from pathlib import Path
from unittest.mock import MagicMock

from aos.scripts.aos_merge_authorization import cmd_prepare, cmd_verify, cmd_preview
import aos.scripts.aos_merge_authorization
from tests.runtime.merge_authorization_fixture_factory import ready_intent

class FakeTransport:
    def request_rest(self, path):
        if path == "/repos/org/repo":
            return {
                "owner": {"login": "org"},
                "name": "repo",
                "node_id": "R_kgDO",
                "default_branch": "main",
                "visibility": "private"
            }
        if path == "/repos/org/repo/pulls/1":
            return {
                "number": 1,
                "state": "open",
                "draft": False,
                "base": {"ref": "main", "sha": "b"*40, "repo": {"node_id": "R_kgDO"}},
                "head": {"ref": "feature", "sha": "a"*40, "repo": {"node_id": "R_kgDO"}},
                "mergeable_state": "clean"
            }
        if path.startswith("/repos/org/repo/pulls/1/commits"):
            return [{"sha": "a"*40, "parents": [{"sha": "b"*40}]}]
        if path.startswith("/repos/org/repo/pulls/1/files"):
            return [{"filename": "src/main.py"}]
        if path.startswith(f"/repos/org/repo/commits/{'a'*40}/check-runs"):
            return {"check_runs": [{"name": "test", "status": "completed", "conclusion": "success"}]}
        if path.startswith("/repos/org/repo/pulls/1/reviews"):
            return [{"state": "APPROVED", "author_association": "MEMBER", "user": {"login": "user1"}}]
        raise Exception(f"Unhandled REST path: {path}")

    def request_graphql(self, query_name, variables):
        if query_name == "review_threads":
            return {"repository": {"pullRequest": {"reviewThreads": {"nodes": []}}}}
        raise Exception(f"Unhandled GraphQL query: {query_name}")

class Args:
    pass

@pytest.fixture
def integration_env(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GITHUB_TOKEN", "fake_token")
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.GitHubReadOnlyTransport", FakeTransport)
    
    intent_path = tmp_path / "intent.md"
    intent = ready_intent()
    intent_path.write_text(f"# Merge Authorization Intent\n\n```json\n{json.dumps(intent)}\n```")
    
    pkg_root = tmp_path / ".aos-tmp"
    pkg_root.mkdir()
    
    return intent_path, pkg_root

def test_prepare_integration(integration_env):
    intent_path, pkg_root = integration_env
    args = Args()
    args.intent = "intent.md"
    args.package_root = ".aos-tmp"
    args.token_env = "GITHUB_TOKEN"
    
    res = cmd_prepare(args)
    assert res.get("technical_status") == "PASS"
    assert res.get("integrity_status") == "PASS"
    assert res.get("freshness_status") == "NOT_RUN"
    assert res.get("control_status") == "HUMAN_REVIEW_REQUIRED"
    assert res.get("approval_granted") is False
    assert res.get("execution_authorized") is False

def test_verify_integration(integration_env):
    intent_path, pkg_root = integration_env
    args = Args()
    args.intent = "intent.md"
    args.package_root = ".aos-tmp"
    args.token_env = "GITHUB_TOKEN"
    cmd_prepare(args)
    
    dirs = list(pkg_root.glob("sha256-*"))
    assert len(dirs) == 1
    pkg_id = "sha256:" + dirs[0].name.split("-")[1]
    
    v_args = Args()
    v_args.package_root = ".aos-tmp"
    v_args.package_id = pkg_id
    v_args.repository = "org/repo"
    v_args.pull_request = "1"
    
    res = cmd_verify(v_args)
    assert res.get("technical_status") == "PASS"
    assert res.get("integrity_status") == "PASS"
    assert res.get("freshness_status") == "PASS"
    assert res.get("control_status") == "HUMAN_REVIEW_REQUIRED"

def test_preview_integration(integration_env, monkeypatch):
    intent_path, pkg_root = integration_env
    args = Args()
    args.intent = "intent.md"
    args.package_root = ".aos-tmp"
    args.token_env = "GITHUB_TOKEN"
    cmd_prepare(args)
    
    dirs = list(pkg_root.glob("sha256-*"))
    pkg_id = "sha256:" + dirs[0].name.split("-")[1]
    
    p_args = Args()
    p_args.package_root = ".aos-tmp"
    p_args.package_id = pkg_id
    
    # preview should NOT access GitHub, so we block it
    import aos.scripts.aos_merge_authorization
    monkeypatch.setattr(aos.scripts.aos_merge_authorization, 'GitHubReadOnlyTransport', MagicMock(side_effect=Exception("Network accessed in preview")))
    
    res = cmd_preview(p_args)
    assert res.get("technical_status") == "PASS"
    assert res.get("approval_granted") is False
    assert res.get("execution_authorized") is False
    assert "markdown" in res

def test_negative_head_drift(integration_env, monkeypatch):
    intent_path, pkg_root = integration_env
    args = Args()
    args.intent = "intent.md"
    args.package_root = ".aos-tmp"
    args.token_env = "GITHUB_TOKEN"
    cmd_prepare(args)
    
    dirs = list(pkg_root.glob("sha256-*"))
    pkg_id = "sha256:" + dirs[0].name.split("-")[1]
    
    class FakeTransportDrift(FakeTransport):
        def request_rest(self, path):
            if path == "/repos/org/repo/pulls/1":
                d = super().request_rest(path)
                d["head"]["sha"] = "c" * 40
                return d
            return super().request_rest(path)
            
    import aos.scripts.aos_merge_authorization
    monkeypatch.setattr(aos.scripts.aos_merge_authorization, 'GitHubReadOnlyTransport', FakeTransportDrift)
    
    v_args = Args()
    v_args.package_root = ".aos-tmp"
    v_args.package_id = pkg_id
    v_args.repository = "org/repo"
    v_args.pull_request = "1"
    
    res = cmd_verify(v_args)
    assert res.get("freshness_status") == "FAIL"

def test_negative_incomplete_state(integration_env):
    intent_path, pkg_root = integration_env
    args = Args()
    args.intent = "intent.md"
    args.package_root = ".aos-tmp"
    args.token_env = "GITHUB_TOKEN"
    cmd_prepare(args)
    
    dirs = list(pkg_root.glob("sha256-*"))
    pkg_id = "sha256:" + dirs[0].name.split("-")[1]
    
    class FakeTransportUnknown(FakeTransport):
        def request_rest(self, path):
            raise Exception("Timeout")
            
    import aos.scripts.aos_merge_authorization
    aos.scripts.aos_merge_authorization.GitHubReadOnlyTransport = FakeTransportUnknown
    
    v_args = Args()
    v_args.package_root = ".aos-tmp"
    v_args.package_id = pkg_id
    v_args.repository = "org/repo"
    v_args.pull_request = "1"
    
    res = cmd_verify(v_args)
    assert res.get("freshness_status") == "UNKNOWN"

def test_negative_required_check_failure(integration_env, monkeypatch):
    intent_path, pkg_root = integration_env
    
    class FakeTransportFailCheck(FakeTransport):
        def request_rest(self, path):
            if "check-runs" in path:
                return {"check_runs": [{"name": "test", "status": "completed", "conclusion": "failure"}]}
            return super().request_rest(path)
            
    import aos.scripts.aos_merge_authorization
    monkeypatch.setattr(aos.scripts.aos_merge_authorization, 'GitHubReadOnlyTransport', FakeTransportFailCheck)
    
    args = Args()
    args.intent = "intent.md"
    args.package_root = ".aos-tmp"
    args.token_env = "GITHUB_TOKEN"
    res = cmd_prepare(args)
    assert res.get("technical_status") == "FAIL"
    assert res.get("control_status") == "BLOCKED"

def test_negative_unresolved_thread(integration_env, monkeypatch):
    intent_path, pkg_root = integration_env
    
    class FakeTransportThread(FakeTransport):
        def request_graphql(self, query_name, variables):
            if query_name == "review_threads":
                return {"repository": {"pullRequest": {"reviewThreads": {"nodes": [{"isResolved": False}]}}}}
            return super().request_graphql(query_name, variables)
            
    import aos.scripts.aos_merge_authorization
    monkeypatch.setattr(aos.scripts.aos_merge_authorization, 'GitHubReadOnlyTransport', FakeTransportThread)
    
    args = Args()
    args.intent = "intent.md"
    args.package_root = ".aos-tmp"
    args.token_env = "GITHUB_TOKEN"
    res = cmd_prepare(args)
    assert res.get("technical_status") == "FAIL"
    assert res.get("control_status") == "BLOCKED"

def test_negative_unknown_ruleset(integration_env, monkeypatch):
    intent_path, pkg_root = integration_env
    
    class FakeTransportRuleset(FakeTransport):
        def request_rest(self, path):
            if path == "/repos/org/repo":
                return {"status": "UNKNOWN", "error_code": "API_ERROR"}
            return super().request_rest(path)
            
    import aos.scripts.aos_merge_authorization
    monkeypatch.setattr(aos.scripts.aos_merge_authorization, 'GitHubReadOnlyTransport', FakeTransportRuleset)
    
    args = Args()
    args.intent = "intent.md"
    args.package_root = ".aos-tmp"
    args.token_env = "GITHUB_TOKEN"
    res = cmd_prepare(args)
    assert res.get("technical_status") == "FAIL"
    assert res.get("control_status") == "BLOCKED"

def test_negative_extra_package_file(integration_env):
    intent_path, pkg_root = integration_env
    args = Args()
    args.intent = "intent.md"
    args.package_root = ".aos-tmp"
    args.token_env = "GITHUB_TOKEN"
    cmd_prepare(args)
    
    dirs = list(pkg_root.glob("sha256-*"))
    pkg_id = "sha256:" + dirs[0].name.split("-")[1]
    
    with open(dirs[0] / "extra.txt", "w") as f:
        f.write("extra")
        
    v_args = Args()
    v_args.package_root = ".aos-tmp"
    v_args.package_id = pkg_id
    v_args.repository = "org/repo"
    v_args.pull_request = "1"
    res = cmd_verify(v_args)
    assert res.get("technical_status") == "FAIL"
    assert res.get("integrity_status") == "NOT_RUN"
    assert res.get("control_status") == "BLOCKED"
    assert "PACKAGE_ARTIFACT_SET_MISMATCH" in res.get("reason_codes", [])

def test_negative_repeated_publication(integration_env):
    intent_path, pkg_root = integration_env
    args = Args()
    args.intent = "intent.md"
    args.package_root = ".aos-tmp"
    args.token_env = "GITHUB_TOKEN"
    cmd_prepare(args)
    
    res = cmd_prepare(args)
    assert res.get("technical_status") == "FAIL"
    assert res.get("control_status") == "BLOCKED"
    assert "PACKAGE_ALREADY_EXISTS" in res.get("reason_codes", [])

def test_negative_invalid_intent(integration_env):
    intent_path, pkg_root = integration_env
    intent_path.write_text("invalid")
    args = Args()
    args.intent = "intent.md"
    args.package_root = ".aos-tmp"
    args.token_env = "GITHUB_TOKEN"
    res = cmd_prepare(args)
    assert res.get("technical_status") == "FAIL"
    assert res.get("control_status") == "BLOCKED"
    assert "MERGE_INTENT_INVALID" in res.get("reason_codes", [])

def test_negative_missing_policy(integration_env, monkeypatch):
    intent_path, pkg_root = integration_env
    
    # Break the policy loading
    def fake_load(*args, **kwargs):
        from aos.runtime.protected_path_policy import PolicyLoadError
        raise PolicyLoadError("broken")
        
    import aos.scripts.aos_merge_authorization
    monkeypatch.setattr(aos.scripts.aos_merge_authorization, "load_protected_path_policy", fake_load)
    
    args = Args()
    args.intent = "intent.md"
    args.package_root = ".aos-tmp"
    args.token_env = "GITHUB_TOKEN"
    res = cmd_prepare(args)
    assert res.get("technical_status") == "UNKNOWN"
    assert res.get("control_status") == "UNKNOWN_BLOCKED"
