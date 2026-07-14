import json
import os

base_dir = "/Users/muhammed/Documents/GitHub/AOS-FARM/tests/fixtures/runtime/execution_package"

def write(path, data):
    p = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        json.dump(data, f, indent=4)

# Replay fixtures
for state in ["UNSEEN", "RESERVED", "CONSUMED", "REVOKED", "CONFLICT", "UNKNOWN", "NOT_CHECKED"]:
    name = f"replay-{state.lower().replace('_', '-')}.json"
    if state == "UNSEEN":
        name = "valid-replay-record.json"
    
    write(f"replay/{name}", {
        "replay_key": "a" * 64,
        "package_id": "pkg_1",
        "package_digest": "b" * 64,
        "authorization_id": "auth_1",
        "nonce": "n1_abcde",
        "session_id": "sess_1_valid",
        "record_state": state,
        "recorded_at": "2026-07-10T12:00:00Z",
        "source_type": "EXPLICIT_VALIDATION_INPUT"
    })

# Workspace Lock fixtures
for state in ["ABSENT", "PRESENT_SELF", "PRESENT_OTHER", "STALE", "CONFLICT", "UNKNOWN", "NOT_CHECKED"]:
    write(f"workspace/workspace-lock-{state.lower().replace('_', '-')}.json", {
        "workspace_instance_id": "ws_1",
        "session_id": "sess_1_valid",
        "package_id": "pkg_1",
        "package_digest": "b" * 64,
        "authorization_id": "auth_1",
        "lock_id": "lock_123",
        "lock_state": state,
        "created_at": "2026-07-10T12:00:00Z",
        "expires_at": "2026-07-10T13:00:00Z",
        "source_type": "EXPLICIT_VALIDATION_INPUT"
    })

# Session mismatch fixtures
write("session/unit/session-authorization-mismatch.json", {
    "schema_version": 1,
    "session_id": "sess_1_valid",
    "session_state": "PENDING",
    "session_revision": 1,
    "created_at": "2026-07-10T12:00:00Z",
    "updated_at": "2026-07-10T12:00:00Z",
    "package_id": "pkg_1",
    "package_digest": "a" * 64,
    "authorization_id": "auth_MISMATCH",
    "baseline_head": "0123456789abcdef0123456789abcdef01234567",
    "nonce": "n1_abcde",
    "workspace_instance_id": "ws_1",
    "resume_allowed": True,
    "session_identity_source": "EXPLICIT_VALIDATION_INPUT",
    "parent_session_id": None
})

write("session/unit/session-platform-mismatch.json", {
    "schema_version": 1,
    "session_id": "sess_1_valid",
    "session_state": "PENDING",
    "session_revision": 1,
    "created_at": "2026-07-10T12:00:00Z",
    "updated_at": "2026-07-10T12:00:00Z",
    "package_id": "pkg_1",
    "package_digest": "a" * 64,
    "authorization_id": "auth_1",
    "baseline_head": "0123456789abcdef0123456789abcdef01234567",
    "nonce": "n1_abcde",
    "workspace_instance_id": "ws_1",
    "resume_allowed": True,
    "session_identity_source": "EXPLICIT_VALIDATION_INPUT",
    "parent_session_id": None
})

# Full valid execution package with session
write("session/integration/full-valid-execution-package-with-session.json", {
    "schema_version": 1,
    "package_id": "aos.farm.integration",
    "authorization_id": "AUTH-100",
    "format_version": "1.0",
    "created_at": "2026-07-10T10:00:00Z",
    "expires_at": "2026-07-10T22:00:00Z",
    "repository_binding": {
        "repository_id": "NMF13579/AOS-FARM",
        "remote_identity": "origin",
        "branch": "build/aos-farm-677-execution-package-foundation",
        "baseline_head": "9defceec6dda20f3e6ee16683e5cb7ff12c3bfa8"
    },
    "platform_binding": {
        "platform_profile": "macos_aarch64",
        "execution_environment_id": "local_dev",
        "execution_mode": "interactive"
    },
    "required_checks": {
        "strict_schema": True,
        "clean_workspace": False,
        "tracked_clean": False
    },
    "capability_lifecycle": {
        "status": "ISSUED",
        "valid_from": "2026-07-10T10:00:00Z",
        "valid_until": "2026-07-10T22:00:00Z",
        "single_use": True
    },
    "session": {
        "schema_version": 1,
        "session_id": "sess_integration_01",
        "session_state": "PENDING",
        "session_revision": 1,
        "created_at": "2026-07-10T10:00:00Z",
        "updated_at": "2026-07-10T10:00:00Z",
        "package_id": "aos.farm.integration",
        "package_digest": "db8fa43977c08a476db8a10e53ef4dd6992ce3bd4fc760195e86d061ea33de20",
        "authorization_id": "AUTH-100",
        "baseline_head": "9defceec6dda20f3e6ee16683e5cb7ff12c3bfa8",
        "nonce": "nonce-12345",
        "workspace_instance_id": "ws-test-01",
        "resume_allowed": False,
        "session_identity_source": "EXPLICIT_VALIDATION_INPUT",
        "parent_session_id": None
    }
})

print("Generated 17 fixtures successfully.")
