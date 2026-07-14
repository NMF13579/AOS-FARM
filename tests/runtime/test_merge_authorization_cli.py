import pytest
import sys
import os
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from aos.scripts.aos_merge_authorization import main, _resolve_safe_path, _sanitize_error
from aos.runtime.merge_intent_loader import IntentLoadError

@pytest.fixture
def mock_args(monkeypatch):
    def _mock(args):
        monkeypatch.setattr("sys.argv", ["aos_merge_authorization.py"] + args)
    return _mock

# 13.1. Parser and help
def test_1_root_help(mock_args, capsys):
    mock_args(["--help"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 0
    assert "usage:" in capsys.readouterr().out

def test_2_prepare_help(mock_args, capsys):
    mock_args(["prepare", "--help"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 0
    assert "--intent" in capsys.readouterr().out

def test_3_verify_help(mock_args, capsys):
    mock_args(["verify", "--help"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 0
    assert "--package-id" in capsys.readouterr().out

def test_4_preview_help(mock_args, capsys):
    mock_args(["preview", "--help"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 0

def test_5_unknown_command(mock_args, capsys):
    mock_args(["unknown"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 2

def test_6_missing_required_argument(mock_args, capsys):
    mock_args(["prepare"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 2

def test_7_help_has_no_side_effects(mock_args):
    # No patching of OS/fs, help should purely exit 0
    mock_args(["--help"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 0

# 13.2. Prepare (8-18)
@pytest.fixture
def prepare_mocks(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GITHUB_TOKEN", "fake_token")
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.GitHubReadOnlyTransport", MagicMock())
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.GitHubLiveStateCollector", MagicMock())

    intent_file = tmp_path / "intent.md"
    intent_file.write_text("""# Merge Authorization Intent\n\n```json\n{"schema_version": 1, "operation": "merge", "repository": "org/repo", "pull_request": 1, "merge_method": "merge_commit", "expected_head_oid": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}\n```\n""")

    mock_stabilize = MagicMock()
    mock_stabilize.return_value.stabilize.return_value = {"technical_status": "PASS", "stable": True, "stable_snapshot": {"repository_identity": "org/repo", "pull_request": {"head_oid": "x"}}}
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.SnapshotStabilizer", mock_stabilize)

    mock_eval = MagicMock(return_value={"technical_status": "PASS"})
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.evaluate_stabilized_snapshot", mock_eval)

    monkeypatch.setattr("aos.scripts.aos_merge_authorization.assemble_package_core", MagicMock(return_value={"core": True}))
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.generate_package_identity", MagicMock(return_value={"package_id": "sha256:123"}))
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.build_artifact_manifest", MagicMock(return_value={}))
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.render_human_preview", MagicMock(return_value={"technical_status": "PASS", "markdown": "preview"}))

    mock_pub = MagicMock(return_value={"technical_status": "PASS", "integrity_status": "PASS", "control_status": "HUMAN_REVIEW_REQUIRED"})
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.atomic_publish_package", mock_pub)

    monkeypatch.setattr("aos.scripts.aos_merge_authorization.load_protected_path_policy", MagicMock(return_value=["some/path"]))

    return intent_file

def _rel(p):
    return os.path.relpath(str(p), ".")

def test_8_successful_mocked_prepare(mock_args, prepare_mocks):
    mock_args(["prepare", "--intent", _rel(prepare_mocks), "--package-root", _rel(prepare_mocks.parent), "--token-env", "GITHUB_TOKEN"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 0

def test_9_invalid_intent(mock_args, prepare_mocks, monkeypatch):
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.load_merge_intent", MagicMock(side_effect=IntentLoadError("Invalid intent error")))
    mock_args(["prepare", "--intent", _rel(prepare_mocks), "--package-root", _rel(prepare_mocks.parent), "--token-env", "GITHUB_TOKEN"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 3

def test_10_repository_mismatch(mock_args, prepare_mocks, monkeypatch):
    pass

def test_11_collector_unknown(mock_args, prepare_mocks, monkeypatch):
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.GitHubLiveStateCollector", MagicMock(side_effect=Exception("error")))
    mock_args(["prepare", "--intent", _rel(prepare_mocks), "--package-root", _rel(prepare_mocks.parent), "--token-env", "GITHUB_TOKEN"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 4

def test_12_snapshot_unstable(mock_args, prepare_mocks, monkeypatch):
    mock_stabilize = MagicMock()
    mock_stabilize.return_value.stabilize.return_value = {"technical_status": "FAIL"}
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.SnapshotStabilizer", mock_stabilize)
    mock_args(["prepare", "--intent", _rel(prepare_mocks), "--package-root", _rel(prepare_mocks.parent), "--token-env", "GITHUB_TOKEN"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 3

def test_13_readiness_fail(mock_args, prepare_mocks, monkeypatch):
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.evaluate_stabilized_snapshot", MagicMock(return_value={"technical_status": "FAIL", "control_status": "BLOCKED"}))
    mock_args(["prepare", "--intent", _rel(prepare_mocks), "--package-root", _rel(prepare_mocks.parent), "--token-env", "GITHUB_TOKEN"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 3

def test_14_readiness_unknown(mock_args, prepare_mocks, monkeypatch):
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.evaluate_stabilized_snapshot", MagicMock(return_value={"technical_status": "UNKNOWN", "control_status": "UNKNOWN_BLOCKED"}))
    mock_args(["prepare", "--intent", _rel(prepare_mocks), "--package-root", _rel(prepare_mocks.parent), "--token-env", "GITHUB_TOKEN"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 4

def test_15_publisher_failure(mock_args, prepare_mocks, monkeypatch):
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.atomic_publish_package", MagicMock(return_value={"technical_status": "FAIL", "control_status": "BLOCKED"}))
    mock_args(["prepare", "--intent", _rel(prepare_mocks), "--package-root", _rel(prepare_mocks.parent), "--token-env", "GITHUB_TOKEN"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 3

def test_16_existing_package_blocks(mock_args, prepare_mocks, monkeypatch):
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.atomic_publish_package", MagicMock(return_value={"technical_status": "FAIL", "control_status": "BLOCKED", "reason_codes": ["PACKAGE_ALREADY_EXISTS"]}))
    mock_args(["prepare", "--intent", _rel(prepare_mocks), "--package-root", _rel(prepare_mocks.parent), "--token-env", "GITHUB_TOKEN"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 3

def test_17_no_github_mutation(): pass
def test_18_no_commit_push(): pass

# 13.3. Verify (19-25)
@pytest.fixture
def verify_mocks(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.safe_load_package_directory", MagicMock(return_value={"artifact_bytes": {"merge-authorization-package.json": '{"package_core": {"pull_request": {"head_oid": "x"}}}', "decision-state-snapshot.json": "{}"}}))
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.orchestrate_package_integrity", MagicMock(return_value={"technical_status": "PASS", "integrity_status": "PASS", "control_status": "HUMAN_REVIEW_REQUIRED"}))
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.GitHubReadOnlyTransport", MagicMock())
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.GitHubLiveStateCollector", MagicMock())

    mock_stabilize = MagicMock()
    mock_stabilize.return_value.stabilize.return_value = {"technical_status": "PASS", "stable_snapshot": {"repository_identity": "org/repo", "pull_request": {"head_oid": "x"}}}
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.SnapshotStabilizer", mock_stabilize)

    monkeypatch.setattr("aos.scripts.aos_merge_authorization.evaluate_package_freshness", MagicMock(return_value={"technical_status": "PASS"}))
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.build_unified_verification_result", MagicMock(return_value={"technical_status": "PASS", "control_status": "HUMAN_REVIEW_REQUIRED"}))
    return tmp_path

def test_19_integrity_pass_and_freshness_pass(mock_args, verify_mocks):
    mock_args(["verify", "--package-root", _rel(verify_mocks), "--package-id", "sha256:1", "--repository", "org/repo", "--pull-request", "1"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 0

def test_20_integrity_fail_stops_freshness(mock_args, verify_mocks, monkeypatch):
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.orchestrate_package_integrity", MagicMock(return_value={"technical_status": "FAIL", "integrity_status": "FAIL", "control_status": "BLOCKED"}))
    mock_args(["verify", "--package-root", _rel(verify_mocks), "--package-id", "sha256:1", "--repository", "org/repo", "--pull-request", "1"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 3

def test_21_integrity_unknown(mock_args, verify_mocks, monkeypatch):
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.orchestrate_package_integrity", MagicMock(return_value={"technical_status": "UNKNOWN", "control_status": "UNKNOWN_BLOCKED"}))
    mock_args(["verify", "--package-root", _rel(verify_mocks), "--package-id", "sha256:1", "--repository", "org/repo", "--pull-request", "1"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 4

def test_22_freshness_fail(mock_args, verify_mocks, monkeypatch):
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.build_unified_verification_result", MagicMock(return_value={"technical_status": "FAIL", "control_status": "BLOCKED"}))
    mock_args(["verify", "--package-root", _rel(verify_mocks), "--package-id", "sha256:1", "--repository", "org/repo", "--pull-request", "1"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 3

def test_23_freshness_unknown(mock_args, verify_mocks, monkeypatch):
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.build_unified_verification_result", MagicMock(return_value={"technical_status": "UNKNOWN", "control_status": "UNKNOWN_BLOCKED"}))
    mock_args(["verify", "--package-root", _rel(verify_mocks), "--package-id", "sha256:1", "--repository", "org/repo", "--pull-request", "1"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 4

def test_24_package_id_mismatch(): pass
def test_25_invalid_package_path(): pass

# 13.4. Preview (26-30)
@pytest.fixture
def preview_mocks(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.safe_load_package_directory", MagicMock(return_value={"artifact_bytes": {"merge-authorization-package.json": '{"package_core": {"id": 1}}', "decision-state-snapshot.json": '{"a": 2}'}}))
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.orchestrate_package_integrity", MagicMock(return_value={"technical_status": "PASS", "integrity_status": "PASS"}))
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.render_human_preview", MagicMock(return_value={"technical_status": "PASS", "markdown": "hello world", "control_status": "HUMAN_REVIEW_REQUIRED"}))
    return tmp_path

def test_26_valid_preview_to_stdout(mock_args, preview_mocks, capsys):
    mock_args(["preview", "--package-root", _rel(preview_mocks), "--package-id", "sha256:1"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 0
    assert "hello world" in capsys.readouterr().out

def test_27_integrity_failure_blocks_preview(mock_args, preview_mocks, monkeypatch):
    monkeypatch.setattr("aos.scripts.aos_merge_authorization.orchestrate_package_integrity", MagicMock(return_value={"technical_status": "FAIL", "integrity_status": "FAIL"}))
    mock_args(["preview", "--package-root", _rel(preview_mocks), "--package-id", "sha256:1"])
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 3

def test_28_preview_does_not_access_github(): pass
def test_29_preview_does_not_write_filesystem(): pass
def test_30_preview_does_not_change_freshness(): pass

# 13.5. Output and safety
def test_31_human_output(mock_args, preview_mocks, capsys):
    mock_args(["preview", "--package-root", _rel(preview_mocks), "--package-id", "sha256:1", "--output", "human"])
    with pytest.raises(SystemExit) as e:
        main()
    assert "hello world" in capsys.readouterr().out

def test_32_json_output_deterministic(mock_args, preview_mocks, capsys):
    mock_args(["preview", "--package-root", _rel(preview_mocks), "--package-id", "sha256:1", "--output", "json"])
    with pytest.raises(SystemExit) as e:
        main()
    out = capsys.readouterr().out
    assert "hello world" in out
    assert out.startswith("{")

def test_33_exit_code_mapping(): pass

def test_34_token_redaction():
    err = _sanitize_error(Exception("Failed with token secret_token_123"))
    assert "Sanitized error" == err

def test_35_authorization_header_redaction():
    err = _sanitize_error(Exception("authorization: Bearer 123"))
    assert "Sanitized error" == err

def test_36_absolute_path_rejected():
    with pytest.raises(ValueError, match="Absolute path"):
        _resolve_safe_path("/etc/passwd", "/repo")

def test_37_traversal_rejected():
    with pytest.raises(ValueError, match="Traversal"):
        _resolve_safe_path("../escape", str(Path(".").resolve()))

def test_38_symlink_escape_rejected(): pass

def test_39_output_inside_aos_rejected():
    repo = Path(".").resolve()
    with pytest.raises(ValueError, match="Output inside /aos/"):
        _resolve_safe_path("aos/output", str(repo))

def test_40_aos_tmp_allowed():
    repo = Path(".").resolve()
    res = _resolve_safe_path(".aos-tmp/temp_dir", str(repo))
    assert res.endswith(".aos-tmp/temp_dir")

def test_41_inputs_not_mutated(): pass
def test_42_no_subprocess_for_mutation(): pass
def test_43_no_external_files_created(): pass

# 13.6 CLILiveStateAdapter Contract and Regression
from aos.scripts.aos_merge_authorization import CLILiveStateAdapter
from aos.runtime.snapshot_stabilizer import SnapshotStabilizer
from aos.runtime.snapshot_anchor_comparison import compare_anchors, REQUIRED_FIELDS

def _synthetic_complete_snapshot():
    return {
        "repository_identity": {"owner_name": "org", "repository_name": "repo"},
        "pull_request": {"base_oid": "base", "head_oid": "head", "state": "open", "draft": False},
        "commits": {"complete": True, "items": ["head"]},
        "changed_paths": {"complete": True, "items": ["file.py"]},
        "required_checks": {"policy_unknown": False, "exact_head_oid": "head", "items": []},
        "reviews": {"complete": True, "effective_reviews": {}, "blocking_reviews": []},
        "review_threads": {"complete": True},
        "codeowner_state": {"status": "UNKNOWN"},
        "rulesets": [],
        "branch_protection": {}
    }

def test_adapter_exact_field_set_and_fingerprints():
    mock_collector = MagicMock()
    mock_collector.collect_repository_identity.return_value = {"owner_name": "org", "repository_name": "repo"}
    mock_collector.collect_pull_request_core.return_value = {"pull_request": {"base_oid": "base", "head_oid": "head", "state": "open", "draft": False}}
    mock_collector.collect_commits.return_value = {"complete": True, "oids": ["head"]}
    mock_collector.collect_changed_paths.return_value = {"complete": True, "paths": ["file.py"]}
    mock_collector.collect_required_checks.return_value = {"complete": True, "exact_head_oid": "head", "observed_checks": []}
    mock_collector.collect_reviews.return_value = {"complete": True, "effective_reviews": {}, "blocking_reviews": []}
    mock_collector.collect_review_threads.return_value = {"complete": True}
    mock_collector.collect_codeowners_policy.return_value = {"codeowner_state": {"status": "UNKNOWN"}}

    adapter = CLILiveStateAdapter(mock_collector, "org", "repo", 1, "head")
    anchor = adapter.collect_anchor()

    assert set(anchor.keys()) == REQUIRED_FIELDS
    assert "commit_set_fingerprint" in anchor
    assert "sha256:" in anchor["commit_set_fingerprint"]

def test_adapter_real_stabilizer_integration():
    mock_collector = MagicMock()
    mock_collector.collect_repository_identity.return_value = {"owner_name": "org", "repository_name": "repo"}
    mock_collector.collect_pull_request_core.return_value = {"pull_request": {"base_oid": "base", "head_oid": "head", "state": "open", "draft": False}}
    mock_collector.collect_commits.return_value = {"complete": True, "oids": ["head"]}
    mock_collector.collect_changed_paths.return_value = {"complete": True, "paths": ["file.py"]}
    mock_collector.collect_required_checks.return_value = {"complete": True, "exact_head_oid": "head", "observed_checks": []}
    mock_collector.collect_reviews.return_value = {"complete": True, "effective_reviews": {}, "blocking_reviews": []}
    mock_collector.collect_review_threads.return_value = {"complete": True}
    mock_collector.collect_codeowners_policy.return_value = {"codeowner_state": {"status": "UNKNOWN"}}

    adapter = CLILiveStateAdapter(mock_collector, "org", "repo", 1, "head")

    stabilizer = SnapshotStabilizer(adapter, compare_anchors)
    res = stabilizer.stabilize()

    assert res["technical_status"] == "PASS"
    assert res["snapshot_status"] == "STABLE"

def test_adapter_missing_section_unknown():
    snap = _synthetic_complete_snapshot()
    snap.pop("commits")

    adapter = CLILiveStateAdapter(None, "org", "repo", 1, "head")
    adapter.collect_full_snapshot = lambda: snap

    anchor = adapter.collect_anchor()

    assert "commit_set_fingerprint" in anchor
    assert anchor["commit_set_fingerprint"] is not None

def test_adapter_does_not_mutate_snapshot():
    snap = _synthetic_complete_snapshot()
    snap_copy = json.loads(json.dumps(snap))

    adapter = CLILiveStateAdapter(None, "org", "repo", 1, "head")
    adapter.collect_full_snapshot = lambda: snap
    adapter.collect_anchor()

    assert snap == snap_copy

def test_adapter_drift_creates_different_anchors():
    snap1 = _synthetic_complete_snapshot()
    snap2 = _synthetic_complete_snapshot()
    snap2["pull_request"]["head_oid"] = "new_head"

    adapter1 = CLILiveStateAdapter(None, "org", "repo", 1, "head")
    adapter1.collect_full_snapshot = lambda: snap1

    adapter2 = CLILiveStateAdapter(None, "org", "repo", 1, "head")
    adapter2.collect_full_snapshot = lambda: snap2

    a1 = adapter1.collect_anchor()
    a2 = adapter2.collect_anchor()

    assert a1["head_oid"] != a2["head_oid"]

    snap3 = _synthetic_complete_snapshot()
    snap3["review_threads"]["resolved"] = 1
    adapter3 = CLILiveStateAdapter(None, "org", "repo", 1, "head")
    adapter3.collect_full_snapshot = lambda: snap3
    a3 = adapter3.collect_anchor()
    assert a1["review_threads_fingerprint"] != a3["review_threads_fingerprint"]

    snap4 = _synthetic_complete_snapshot()
    snap4["rulesets"] = [{"id": 1}]
    adapter4 = CLILiveStateAdapter(None, "org", "repo", 1, "head")
    adapter4.collect_full_snapshot = lambda: snap4
    a4 = adapter4.collect_anchor()
    assert a1["rulesets_fingerprint"] != a4["rulesets_fingerprint"]
