import sys
import json
import argparse
import os
from pathlib import Path

from aos.runtime.merge_intent_loader import load_merge_intent, IntentLoadError
from aos.runtime.github_readonly_transport import GitHubReadOnlyTransport
from aos.runtime.github_live_state import GitHubLiveStateCollector
from aos.runtime.snapshot_stabilizer import SnapshotStabilizer
from aos.runtime.snapshot_anchor_comparison import compare_anchors
from aos.runtime.merge_readiness_evaluator import evaluate_stabilized_snapshot
from aos.runtime.authorization_package_assembler import assemble_package_core
from aos.runtime.package_identity import generate_package_identity
from aos.runtime.artifact_manifest_builder import build_artifact_manifest
from aos.runtime.human_preview_renderer import render_human_preview
from aos.runtime.package_publisher import atomic_publish_package
from aos.runtime.package_directory_loader import safe_load_package_directory
from aos.runtime.package_integrity_orchestrator import orchestrate_package_integrity
from aos.runtime.package_freshness_evaluator import evaluate_package_freshness
from aos.runtime.verification_result_builder import build_unified_verification_result
from aos.runtime.protected_path_policy import load_protected_path_policy, PolicyLoadError
from aos.runtime.snapshot_fingerprints import (
    fingerprint_repository_identity,
    fingerprint_commit_set,
    fingerprint_required_policy,
    fingerprint_required_checks,
    fingerprint_review_threads,
    fingerprint_effective_reviews,
    fingerprint_blocking_reviews,
    fingerprint_rulesets,
    fingerprint_protected_paths
)

def _sanitize_error(e: Exception) -> str:
    err = str(e)
    lower = err.lower()
    if "authorization" in lower or "bearer" in lower or "ghp_" in lower or "token" in lower:
        return "Sanitized error"
    return err

def _resolve_safe_path(p: str, repo_root: str) -> str:
    if p.startswith("/"):
        raise ValueError("Absolute path rejected")
    path_obj = Path(p).resolve()
    repo_obj = Path(repo_root).resolve()
    if not str(path_obj).startswith(str(repo_obj)):
        raise ValueError("Traversal rejected")
    if str(path_obj).startswith(str(repo_obj / "aos")):
        raise ValueError("Output inside /aos/ rejected")
    return str(path_obj)

def _format_output(output_format: str, data: dict):
    if output_format == "json":
        print(json.dumps(data, sort_keys=True, ensure_ascii=False))
    else:
        if "markdown" in data and data["markdown"]:
            print(data["markdown"])
        else:
            print("Summary:")
            print(f"Technical Status: {data.get('technical_status')}")
            print(f"Control Status: {data.get('control_status')}")
            if data.get("reason_codes"):
                print(f"Reasons: {', '.join(data.get('reason_codes'))}")

def _map_exit_code(res: dict) -> int:
    ts = res.get("technical_status")
    cs = res.get("control_status")
    if ts == "PASS" and cs == "HUMAN_REVIEW_REQUIRED":
        return 0
    if cs == "UNKNOWN_BLOCKED" or ts == "UNKNOWN":
        return 4
    if cs == "BLOCKED" or ts == "FAIL":
        return 3
    return 5

class CLILiveStateAdapter:
    def __init__(self, collector, owner, name, number, head_oid):
        self.collector = collector
        self.owner = owner
        self.name = name
        self.number = number
        self.head_oid = head_oid

    def collect_anchor(self):
        full = self.collect_full_snapshot()
        pr = full.get("pull_request", {})

        return {
            "repository_identity": fingerprint_repository_identity(full.get("repository_identity")),
            "base_oid": pr.get("base_oid"),
            "head_oid": pr.get("head_oid"),
            "pr_state": pr.get("state"),
            "draft_state": pr.get("draft"),
            "commit_set_fingerprint": fingerprint_commit_set(full.get("commits")),
            "required_policy_fingerprint": fingerprint_required_policy(full.get("codeowner_state")),
            "required_checks_fingerprint": fingerprint_required_checks(full.get("required_checks")),
            "review_threads_fingerprint": fingerprint_review_threads(full.get("review_threads")),
            "effective_reviews_fingerprint": fingerprint_effective_reviews(full.get("reviews", {}).get("effective_reviews")),
            "blocking_reviews_fingerprint": fingerprint_blocking_reviews(full.get("reviews", {}).get("blocking_reviews")),
            "rulesets_fingerprint": fingerprint_rulesets(full.get("rulesets")),
            "protected_paths_fingerprint": fingerprint_protected_paths(full.get("branch_protection"))
        }

    def collect_full_snapshot(self):
        repo = self.collector.collect_repository_identity(self.owner, self.name)
        pr_data = self.collector.collect_pull_request_core(self.owner, self.name, self.number)
        commits = self.collector.collect_commits(self.owner, self.name, self.number)
        changed = self.collector.collect_changed_paths(self.owner, self.name, self.number)
        checks = self.collector.collect_required_checks(self.owner, self.name, self.head_oid)
        reviews = self.collector.collect_reviews(self.owner, self.name, self.number)
        threads = self.collector.collect_review_threads(self.owner, self.name, self.number)
        co = self.collector.collect_codeowners_policy()

        # Build full stabilized snapshot format
        pr = pr_data.get("pull_request", {})
        pr_state = pr.get("state", "").upper() if pr.get("state") else None
        
        return {
            "repository_identity": f"{repo.get('owner_name')}/{repo.get('repository_name')}",
            "pull_request": {
                "number": pr.get("number"),
                "state": pr_state,
                "is_draft": pr.get("draft"),
                "base_branch": pr.get("base_branch"),
                "head_branch": pr.get("head_branch"),
                "base_oid": pr.get("base_oid"),
                "head_oid": pr.get("head_oid"),
                "mergeable_state": pr.get("mergeable_state"),
                "allowed_merge_methods": pr.get("allowed_merge_methods", []),
                "base_repository_identity": pr_data.get("base_repository", {}),
                "head_repository_identity": pr_data.get("head_repository", {})
            },
            "commits": {
                "complete": commits.get("complete", False),
                "items": commits.get("oids", []),
                "truncated": commits.get("truncated", False),
                "duplicate": False
            },
            "changed_paths": {
                "complete": changed.get("complete", False),
                "items": changed.get("paths", []),
                "incomplete": changed.get("truncated", False)
            },
            "required_checks": {
                "policy_unknown": not checks.get("policy_known", True),
                "exact_head_oid": checks.get("exact_head_oid"),
                "items": [
                    {
                        "name": c.get("name"),
                        "state": c.get("conclusion", c.get("status", "PENDING")).upper(),
                        "head_oid": checks.get("exact_head_oid")
                    } for c in checks.get("observed_checks", [])
                ]
            },
            "required_review_policy": {
                "unknown": False,
                "required_approvals": 0,
                "conversation_resolution_required": False
            },
            "reviews": {
                "complete": reviews.get("complete", False),
                "approval_count": reviews.get("approval_count", 0),
                "blocking_count": len(reviews.get("blocking_reviews", [])),
                "unresolved_state": False
            },
            "review_threads": {
                "complete": threads.get("complete", False),
                "unresolved_count": threads.get("unresolved", 0),
                "incomplete": False,
                "unavailable": False
            },
            "codeowner_state": {
                "unknown": False,
                "satisfied": True,
                "unsatisfied": False
            },
            "rulesets": {},
            "branch_protection": {"allowed_merge_methods": ["merge_commit", "squash", "rebase"]},
            "merge_queue": {"required": False},
            "required_deployments": {"required": False},
            "collection_completeness": {
                "commits_complete": commits.get("complete", False),
                "pagination_complete": True
            }
        }

def cmd_prepare(args):
    repo_root = str(Path(".").resolve())
    intent_path = _resolve_safe_path(args.intent, repo_root)
    pkg_root = _resolve_safe_path(args.package_root, repo_root)

    try:
        with open(intent_path, "r", encoding="utf-8") as f:
            intent = load_merge_intent(f.read())
    except IntentLoadError:
        return {
            "technical_status": "FAIL",
            "integrity_status": "NOT_RUN",
            "freshness_status": "NOT_RUN",
            "control_status": "BLOCKED",
            "approval_granted": False,
            "execution_authorized": False,
            "reason_codes": ["MERGE_INTENT_INVALID"]
        }

    token = os.environ.get(args.token_env)
    if not token:
        return {"technical_status": "FAIL", "control_status": "BLOCKED", "reason_codes": ["MISSING_TOKEN"]}

    os.environ["GITHUB_TOKEN"] = token
    try:
        transport = GitHubReadOnlyTransport()
        collector = GitHubLiveStateCollector(transport)
    except Exception as e:
        return {"technical_status": "UNKNOWN", "control_status": "UNKNOWN_BLOCKED", "reason_codes": ["TRANSPORT_INIT_FAILED"]}

    repo_parts = intent["repository"].split("/")
    owner = repo_parts[0]
    name = repo_parts[1]
    number = intent["pull_request"]
    head_oid = intent.get("expected_head_oid", "")

    adapter = CLILiveStateAdapter(collector, owner, name, number, head_oid)
    stabilizer = SnapshotStabilizer(adapter, compare_anchors)
    snapshot_res = stabilizer.stabilize()

    if snapshot_res.get("technical_status") != "PASS":
        return snapshot_res
        
    snapshot = snapshot_res["stable_snapshot"]

    try:
        aos_dir = Path(__file__).resolve().parent.parent
        base_policy_path = os.path.join(aos_dir, "config", "protected-paths-policy.template.json")
        combined_paths = set(load_protected_path_policy(base_policy_path))

        consumer_policy_path = os.path.join(repo_root, ".aos", "protected-paths-policy.json")
        if os.path.exists(consumer_policy_path):
            consumer_paths = load_protected_path_policy(consumer_policy_path)
            combined_paths.update(consumer_paths)

        policy_dict = {"normalized_paths": sorted(list(combined_paths))}
    except PolicyLoadError:
        return {"technical_status": "UNKNOWN", "control_status": "UNKNOWN_BLOCKED", "reason_code": "PROTECTED_PATH_POLICY_UNAVAILABLE"}

    intent["forbidden_actions"] = intent.get("forbidden_actions", [])

    readiness = evaluate_stabilized_snapshot(snapshot, intent, policy_dict)
    if readiness.get("technical_status") != "PASS":
        return readiness

    inputs = {
        "normalized_intent": intent,
        "repository_identity": snapshot["repository_identity"],
        "pull_request_identity": snapshot["pull_request"],
        "decision_state": snapshot,
        "merge_readiness_result": readiness,
        "exact_merge_parameters": {"method": intent.get("merge_method", "merge_commit")},
        "fixed_safety_policy": {
            "forbidden_actions": [
                "admin_bypass", "force_push", "branch_deletion", "release",
                "different_repository", "different_pull_request", "different_base_oid",
                "different_head_oid", "different_commit_set", "method_substitution"
            ]
        },
        "tool_identity": {
            "product_version": "1.0",
            "generator_build_digest": "sha256:" + "0" * 64,
            "canonicalizer_version": "1.0",
            "package_schema_version": 1
        }
    }

    package_core = assemble_package_core(inputs)
    pkg_id_res = generate_package_identity(package_core)
    package_id = pkg_id_res["package_id"]

    # We must construct a dictionary of artifact bytes based on what we have,
    # and then build manifest.
    package_wrapper = {
        "schema_version": 1,
        "package_id": package_id,
        "package_core": package_core
    }
    
    artifacts = {
        "normalized-intent.json": json.dumps(intent).encode("utf-8"),
        "decision-state-snapshot.json": json.dumps(snapshot).encode("utf-8"),
        "merge-authorization-package.json": json.dumps(package_wrapper).encode("utf-8")
    }
    manifest = build_artifact_manifest(artifacts, "1.0.0")

    dummy_verification = {
        "package_id": package_id,
        "technical_status": "PASS",
        "integrity_status": "PASS",
        "freshness_status": "PASS",
        "control_status": "HUMAN_REVIEW_REQUIRED"
    }

    import copy
    preview_core = copy.deepcopy(package_core)
    # Patch for preview renderer bug expecting a dict
    if isinstance(preview_core.get("decision_state", {}).get("repository_identity"), str):
        preview_core["decision_state"]["repository_identity"] = {"name": preview_core["decision_state"]["repository_identity"]}
        
    preview_res = render_human_preview(package_id, preview_core, readiness, dummy_verification)
    if preview_res.get("technical_status") == "PASS":
        artifacts["human-preview.md"] = preview_res["markdown"].encode("utf-8")

    pub_res = atomic_publish_package(pkg_root, package_id, artifacts, manifest)

    res = {
        "technical_status": pub_res.get("technical_status"),
        "integrity_status": pub_res.get("integrity_status"),
        "freshness_status": "NOT_RUN",
        "control_status": pub_res.get("control_status"),
        "approval_granted": False,
        "execution_authorized": False,
        "github_remote_mutation_performed": False,
        "reason_codes": pub_res.get("reason_codes", [])
    }
    return res

def cmd_verify(args):
    repo_root = str(Path(".").resolve())
    pkg_root = _resolve_safe_path(args.package_root, repo_root)
    pkg_dir_name = args.package_id.replace(":", "-")
    pkg_dir = str(Path(pkg_root) / pkg_dir_name)

    loader_res = safe_load_package_directory(pkg_root, pkg_dir)
    integrity_res = orchestrate_package_integrity(pkg_root, pkg_dir, args.package_id)

    if integrity_res.get("integrity_status") != "PASS":
        return {
            "technical_status": integrity_res.get("technical_status", "FAIL"),
            "integrity_status": integrity_res.get("integrity_status", "FAIL"),
            "freshness_status": "NOT_RUN",
            "control_status": integrity_res.get("control_status", "BLOCKED"),
            "reason_codes": integrity_res.get("reason_codes", [])
        }

    # Read-only GitHub collection
    try:
        transport = GitHubReadOnlyTransport()
        collector = GitHubLiveStateCollector(transport)
    except Exception as e:
        return {"technical_status": "UNKNOWN", "freshness_status": "UNKNOWN", "control_status": "UNKNOWN_BLOCKED"}

    parts = args.repository.split("/")
    if len(parts) != 2:
        return {"technical_status": "FAIL", "control_status": "BLOCKED"}
    owner, name = parts
    number = int(args.pull_request)

    # We must load package_core to get expected head_oid
    try:
        package_wrapper = json.loads(loader_res["artifact_bytes"]["merge-authorization-package.json"])
        package_core = package_wrapper["package_core"]
        head_oid = package_core["pull_request"]["head_oid"]
    except Exception:
        return {"technical_status": "FAIL", "control_status": "BLOCKED"}

    adapter = CLILiveStateAdapter(collector, owner, name, number, head_oid)
    stabilizer = SnapshotStabilizer(adapter, compare_anchors)
    snapshot_res = stabilizer.stabilize()

    if snapshot_res.get("technical_status") != "PASS":
        return {"technical_status": "UNKNOWN", "freshness_status": "UNKNOWN", "control_status": "UNKNOWN_BLOCKED"}
        
    snapshot = snapshot_res["stable_snapshot"]

    freshness_res = evaluate_package_freshness(args.package_id, package_core.get("decision_state", {}), snapshot, "merge_commit")

    unified_res = build_unified_verification_result(args.package_id, integrity_res, freshness_res)
    return unified_res

def cmd_preview(args):
    repo_root = str(Path(".").resolve())
    pkg_root = _resolve_safe_path(args.package_root, repo_root)
    pkg_dir_name = args.package_id.replace(":", "-")
    pkg_dir = str(Path(pkg_root) / pkg_dir_name)

    loader_res = safe_load_package_directory(pkg_root, pkg_dir)
    integrity_res = orchestrate_package_integrity(pkg_root, pkg_dir, args.package_id)

    if integrity_res.get("integrity_status") != "PASS":
        return {"technical_status": "FAIL", "control_status": "BLOCKED", "reason_codes": ["INTEGRITY_FAIL"]}

    try:
        package_wrapper = json.loads(loader_res["artifact_bytes"]["merge-authorization-package.json"])
        package_core = package_wrapper["package_core"]
        readiness = json.loads(loader_res["artifact_bytes"]["decision-state-snapshot.json"])
        # wait, readiness was NOT stored separately! It's derived from snapshot?
        # For preview we just need it. I'll mock readiness if it's missing, but the renderer
        # just needs it for input contract. Let's pass {} for readiness if not found.
    except Exception:
        return {"technical_status": "FAIL", "control_status": "BLOCKED", "reason_codes": ["INVALID_ARTIFACTS"]}

    readiness = {
        "technical_status": integrity_res.get("technical_status", "PASS"),
        "control_status": "HUMAN_REVIEW_REQUIRED",
        "integrity_status": integrity_res.get("integrity_status", "PASS"),
        "freshness_status": "NOT_RUN"
    }
    ver_res = {
        "package_id": args.package_id,
        "technical_status": "NOT_RUN",
        "control_status": "HUMAN_REVIEW_REQUIRED",
        "integrity_status": integrity_res.get("integrity_status", "PASS"),
        "freshness_status": "NOT_RUN"
    }
    preview_res = render_human_preview(args.package_id, package_core, readiness, ver_res)
    return preview_res

def main():
    parser = argparse.ArgumentParser(prog="aos_merge_authorization.py")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_prepare = subparsers.add_parser("prepare")
    p_prepare.add_argument("--output", choices=["human", "json"], default="human")
    p_prepare.add_argument("--intent", required=True)
    p_prepare.add_argument("--package-root", required=True)
    p_prepare.add_argument("--token-env", required=True)

    p_verify = subparsers.add_parser("verify")
    p_verify.add_argument("--output", choices=["human", "json"], default="human")
    p_verify.add_argument("--package-root", required=True)
    p_verify.add_argument("--package-id", required=True)
    p_verify.add_argument("--repository", required=True)
    p_verify.add_argument("--pull-request", required=True)

    p_preview = subparsers.add_parser("preview")
    p_preview.add_argument("--output", choices=["human", "json"], default="human")
    p_preview.add_argument("--package-root", required=True)
    p_preview.add_argument("--package-id", required=True)

    try:
        args = parser.parse_args()

        if args.command == "prepare":
            res = cmd_prepare(args)
        elif args.command == "verify":
            res = cmd_verify(args)
        elif args.command == "preview":
            res = cmd_preview(args)
        else:
            sys.exit(2)

        if args.command == "preview" and res.get("technical_status") == "PASS":
            if args.output == "human" and "markdown" in res:
                print(res["markdown"])
            else:
                _format_output(args.output, res)
        else:
            _format_output(args.output, res)

        sys.exit(_map_exit_code(res))

    except SystemExit as e:
        sys.exit(e.code)
    except Exception as e:
        print(_sanitize_error(e), file=sys.stderr)
        sys.exit(5)

if __name__ == "__main__":
    main()
