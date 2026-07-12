import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


from aos.runtime.simple_control_planning import bind_payload


SCRIPT_ABS = Path("aos/scripts/aos_control_surface.py").resolve()


def git(cwd, *args):
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=True,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
    ).stdout.strip()


class TestSimpleControlGit(unittest.TestCase):
    def make_repo(self, with_remote=False):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name) / "repo"
        root.mkdir()
        git(root, "init", "-b", "build/test")
        git(root, "config", "user.email", "aos@example.invalid")
        git(root, "config", "user.name", "AOS Test")
        (root / "README.md").write_text("base\n", encoding="utf-8")
        git(root, "add", "--", "README.md")
        git(root, "commit", "-m", "base")
        remote = None
        if with_remote:
            remote = Path(tmp.name) / "remote.git"
            git(Path(tmp.name), "init", "--bare", "-b", "build/test", str(remote))
            git(root, "remote", "add", "origin", str(remote))
            git(root, "push", "origin", "HEAD:refs/heads/build/test")
        return tmp, root, remote

    def repo_binding(self, root):
        return {
            "repository": "SANDBOX/AOS-FARM",
            "branch": git(root, "branch", "--show-current"),
            "head": git(root, "rev-parse", "HEAD"),
        }

    def write_candidate(self, root, path="candidate.txt", content="candidate\n"):
        target = root / path
        target.write_text(content, encoding="utf-8")
        return path

    def make_manifest(self, root, paths):
        from aos.runtime.simple_control_git import create_candidate_manifest

        return create_candidate_manifest(root, paths, "AOS-FARM.681.8", self.repo_binding(root))

    def make_commit_request(self, manifest, root, operation_id="op-commit"):
        from aos.runtime.simple_control_git import create_commit_request

        return create_commit_request(
            manifest,
            operation_id,
            "AOS-FARM.681.8 controlled commit",
            "Sandbox validation only.",
            self.repo_binding(root),
        )

    def make_commit_witness(self, manifest, request):
        from aos.runtime.simple_control_git import create_commit_witness

        preview = {"preview_binding": bind_payload({"request": request["request_binding"], "manifest": manifest["candidate_binding"]})}
        return create_commit_witness(manifest, request, preview, "human-owner")

    def test_candidate_manifest_accepts_exact_files_and_blocks_bad_paths(self):
        from aos.runtime.simple_control_git import GitControlError, create_candidate_manifest

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            git(root, "init", "-b", "build/test")
            git(root, "config", "user.email", "aos@example.invalid")
            git(root, "config", "user.name", "AOS Test")
            (root / "file.txt").write_text("x", encoding="utf-8")
            manifest = create_candidate_manifest(root, ["file.txt"], "task", {"repository": "sandbox", "branch": "build/test", "head": "0"})
            self.assertEqual(manifest["files"][0]["relative_path"], "file.txt")
            self.assertEqual(manifest["files"][0]["expected_state"], "UNTRACKED")
            for bad in ["/tmp/x", "../x", "dir", "link"]:
                if bad == "dir":
                    (root / "dir").mkdir()
                if bad == "link":
                    (root / "link").symlink_to(root / "file.txt")
                with self.assertRaises(GitControlError, msg=bad):
                    create_candidate_manifest(root, [bad], "task", {"repository": "sandbox", "branch": "build/test", "head": "0"})
            with self.assertRaises(GitControlError):
                create_candidate_manifest(root, ["file.txt", "file.txt"], "task", {"repository": "sandbox", "branch": "build/test", "head": "0"})

    def test_commit_witness_validation_and_non_grants(self):
        from aos.runtime.simple_control_git import GitControlError, validate_commit_witness

        tmp, root, _remote = self.make_repo()
        with tmp:
            self.write_candidate(root)
            manifest = self.make_manifest(root, ["candidate.txt"])
            request = self.make_commit_request(manifest, root)
            witness = self.make_commit_witness(manifest, request)
            self.assertTrue(validate_commit_witness(witness, manifest, request))
            self.assertNotIn("push", witness["grants"])
            for override in [
                {"decision_type": "PUSH_AUTHORIZATION"},
                {"candidate_manifest_binding": "wrong"},
                {"commit_request_binding": "wrong"},
                {"repository_baseline_binding": {"repository": "wrong"}},
                {"actor_reference": ""},
                {"consumed_at": "2026-07-13T00:00:00Z"},
                {"grants": ["stage_exact_candidate_manifest", "create_one_ordinary_commit", "push"]},
            ]:
                bad = dict(witness, **override)
                with self.assertRaises(GitControlError, msg=str(override)):
                    validate_commit_witness(bad, manifest, request)

    def test_controlled_commit_stages_exact_manifest_and_creates_one_commit(self):
        from aos.runtime.simple_control_git import apply_commit

        tmp, root, _remote = self.make_repo()
        with tmp:
            self.write_candidate(root, "candidate.txt", "candidate\n")
            (root / "noise.txt").write_text("noise\n", encoding="utf-8")
            manifest = self.make_manifest(root, ["candidate.txt"])
            request = self.make_commit_request(manifest, root)
            witness = self.make_commit_witness(manifest, request)
            before = git(root, "rev-parse", "HEAD")
            result = apply_commit(root, manifest, request, witness)
            after = git(root, "rev-parse", "HEAD")
            self.assertEqual(result["commit_state"], "COMMIT_COMPLETED")
            self.assertNotEqual(before, after)
            self.assertEqual(git(root, "rev-parse", f"{after}^"), before)
            self.assertEqual(git(root, "diff", "--cached", "--name-only"), "")
            self.assertEqual(git(root, "status", "--short", "--", "noise.txt"), "?? noise.txt")
            self.assertFalse(result["push_performed"])
            self.assertFalse(result["approval_granted"])

    def test_preexisting_staged_path_blocks_without_reset(self):
        from aos.runtime.simple_control_git import GitControlError, apply_commit

        tmp, root, _remote = self.make_repo()
        with tmp:
            self.write_candidate(root, "candidate.txt")
            (root / "staged.txt").write_text("staged\n", encoding="utf-8")
            git(root, "add", "--", "staged.txt")
            manifest = self.make_manifest(root, ["candidate.txt"])
            request = self.make_commit_request(manifest, root)
            with self.assertRaises(GitControlError):
                apply_commit(root, manifest, request, self.make_commit_witness(manifest, request))
            self.assertEqual(git(root, "diff", "--cached", "--name-only"), "staged.txt")

    def test_commit_idempotency_reconciles_completed_commit(self):
        from aos.runtime.simple_control_git import apply_commit

        tmp, root, _remote = self.make_repo()
        with tmp:
            self.write_candidate(root)
            manifest = self.make_manifest(root, ["candidate.txt"])
            request = self.make_commit_request(manifest, root)
            witness = self.make_commit_witness(manifest, request)
            first = apply_commit(root, manifest, request, witness)
            second = apply_commit(root, manifest, request, witness)
            self.assertEqual(second["reconciliation_result"], "COMMIT_ALREADY_COMPLETED_VERIFIED")
            self.assertEqual(second["commit_oid"], first["commit_oid"])
            self.assertFalse(second["side_effect_repeated"])

    def test_push_to_local_bare_build_branch_and_idempotency(self):
        from aos.runtime.simple_control_git import (
            apply_commit,
            apply_push,
            create_push_request,
            create_push_witness,
            observe_remote_ref,
        )

        tmp, root, remote = self.make_repo(with_remote=True)
        with tmp:
            self.write_candidate(root)
            manifest = self.make_manifest(root, ["candidate.txt"])
            request = self.make_commit_request(manifest, root)
            commit_result = apply_commit(root, manifest, request, self.make_commit_witness(manifest, request))
            remote_before = observe_remote_ref(root, "origin", "refs/heads/build/test")
            push_request = create_push_request(root, "push-op", "AOS-FARM.681.8", commit_result, "origin", "refs/heads/build/test", remote_before)
            witness = create_push_witness(push_request, "human-owner")
            result = apply_push(root, push_request, witness)
            self.assertEqual(result["push_state"], "PUSH_COMPLETED")
            self.assertEqual(observe_remote_ref(root, "origin", "refs/heads/build/test"), commit_result["commit_oid"])
            self.assertFalse(result["integration_performed"])
            retry = apply_push(root, push_request, witness)
            self.assertEqual(retry["reconciliation_result"], "PUSH_ALREADY_COMPLETED_VERIFIED")
            self.assertFalse(retry["side_effect_repeated"])
            self.assertTrue(str(remote).endswith("remote.git"))

    def test_push_policy_blocks_non_build_and_force(self):
        from aos.runtime.simple_control_git import GitControlError, validate_build_ref

        for bad in ["refs/heads/dev", "refs/heads/main", "refs/tags/v1", "refs/heads/build/*", ":refs/heads/build/test"]:
            with self.assertRaises(GitControlError, msg=bad):
                validate_build_ref(bad)

    def test_active_repository_git_write_guard(self):
        from aos.runtime.simple_control_git import GitControlError, active_repository_root, apply_commit

        tmp, root, _remote = self.make_repo()
        with tmp:
            self.write_candidate(root)
            manifest = self.make_manifest(root, ["candidate.txt"])
            request = self.make_commit_request(manifest, root)
            with self.assertRaises(GitControlError):
                apply_commit(active_repository_root(), manifest, request, self.make_commit_witness(manifest, request))

    def test_cli_commit_apply_uses_temporary_repository(self):
        tmp, root, _remote = self.make_repo()
        with tmp:
            self.write_candidate(root)
            manifest = self.make_manifest(root, ["candidate.txt"])
            request = self.make_commit_request(manifest, root)
            witness = self.make_commit_witness(manifest, request)
            result = subprocess.run(
                [
                    "python3",
                    "-B",
                    str(SCRIPT_ABS),
                    "--json",
                    "/commit",
                    "--apply",
                    "--candidate-manifest-json",
                    json.dumps(manifest),
                    "--commit-request-json",
                    json.dumps(request),
                    "--commit-witness-json",
                    json.dumps(witness),
                ],
                cwd=root,
                capture_output=True,
                text=True,
            )
            data = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(data["resolved_command_id"], "COMMIT")
            self.assertEqual(data["result"]["commit_state"], "COMMIT_COMPLETED")
            self.assertFalse(data["result"]["push_performed"])


if __name__ == "__main__":
    unittest.main()
