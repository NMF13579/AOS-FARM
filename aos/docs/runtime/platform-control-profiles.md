# Platform Control Profiles

This document defines the platform-specific capabilities, isolation levels, and control profiles for macOS and Linux within the AOS-FARM runtime architecture.

## 1. macOS Platform Profile

- **platform**: macos
- **supported_versions**: macOS 13+ (Ventura or newer)
- **supported_execution_environments**: Local Developer Laptop, Hosted CI macOS Runner
- **initial_execution_mode**: OBSERVE_MODE
- **initial_runner_model**: LOCAL_BROKER_PROCESS
- **initial_isolation_level**: PROCESS_BOUNDARY
- **initial_effective_claim**: POST_ACTION_DETECTION
- **target_execution_mode**: ENFORCED_MODE
- **target_runner_model**: SEPARATE_OS_IDENTITY_BROKER or CONTAINER/VM (via OrbStack/Docker)
- **target_isolation_level**: OS_IDENTITY_BOUNDARY / PLATFORM_BOUNDARY
- **target_claim_ceiling**: BLOCKED_BY_OS_OR_SANDBOX
- **agent_os_identity**: IDE User
- **runner_os_identity**: Separate local service account or isolated VM
- **filesystem_mechanism**: Read-only mounts for agent, writable by runner only (Target)
- **shell_control**: Shell block via broker IPC only in target mode
- **local_git_control**: Git wrapper/hook enforced by OS user permissions
- **residual_bypass_paths**: In initial profile, same-user bypass allows the agent to mutate validation scripts directly or bypass the local broker.

### macOS Constraints
- **Same-user broker**: macOS apps share user permissions. Running an agent inside an IDE gives it access to the user's keychain and home directory.
- **Symlink traversal**: macOS filesystem allows rapid escape unless sandboxed.
- **Container feasibility**: Requires virtualization (e.g., Docker Desktop, OrbStack). Native macOS containers do not exist.

## 2. Linux Platform Profile

- **platform**: linux
- **supported_distributions**: Ubuntu 22.04+, Debian 12+
- **supported_execution_environments**: CI Linux Runner, Local Linux Workstation
- **initial_execution_mode**: OBSERVE_MODE
- **initial_runner_model**: LOCAL_BROKER_PROCESS
- **initial_isolation_level**: PROCESS_BOUNDARY
- **initial_effective_claim**: POST_ACTION_DETECTION
- **target_execution_mode**: ENFORCED_MODE
- **target_runner_model**: SEPARATE_EXECUTION_DOMAIN (User/Mount Namespaces or Rootless Container)
- **target_isolation_level**: PLATFORM_BOUNDARY
- **target_claim_ceiling**: BLOCKED_BY_PLATFORM
- **agent_os_identity**: Unprivileged user
- **runner_os_identity**: Separate user or outer container context
- **filesystem_mechanism**: Read-only bind mounts (`--read-only`) with specific writable volumes for runner
- **shell_control**: Namespace restriction (no direct `/bin/bash` execution allowed for agent container)
- **local_git_control**: Outer container handles git operations
- **residual_bypass_paths**: In target profile, privileged container risks must be mitigated by using rootless containers.

### Linux Constraints
- **Namespaces**: Available but complex to configure per-session without a wrapper like Podman or Docker.
- **Root access**: Agent might utilize `sudo` if passwordless sudo is configured. The agent OS user must strictly have `sudo` removed.

## 3. Platform Comparison Matrix

- **Process isolation**: macOS requires separate OS user or heavy VM. Linux offers lightweight native namespaces.
- **OS-user separation**: Feasible on both, but macOS user switching inside an IDE context is operationally complex.
- **Read-only filesystem**: macOS supports `chflags` or separate users. Linux supports native read-only bind mounts.
- **Network isolation**: macOS native network isolation is poor. Linux network namespaces offer strong isolation.
- **Target profile**: macOS leans towards VM-based isolation (Docker/OrbStack). Linux targets native rootless containers.
- **Maximum honest claim**: Linux can achieve `BLOCKED_BY_PLATFORM` more naturally. macOS native tops out at `BLOCKED_BY_OS_OR_SANDBOX` unless relying on a VM.
- **Residual same-user bypass**: Highly present on both in the initial `LOCAL_BROKER_PROCESS` mode.
