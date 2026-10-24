"""The optional container sandbox runner: the same five-dimension profile, compiled onto podman or
docker instead of the tool sandbox (DECISION F162 D7).

Remedy never pulls an image: every run passes `--pull never`, and a missing runtime or a missing
local image refuses rather than reaching the network. No worker Remedy runs today uses this
module — claude-cli keeps its login in the operator's home, and every other process already runs
through the tool sandbox (`tool_sandbox.py`) — so `tests/test_no_orphan_modules.py` carries it as
deliberately unwired until F246's gate plugin run reads a runner choice from configuration
(R-1467).
"""
from __future__ import annotations

import dataclasses
import os
import shutil
import signal
import uuid
from collections.abc import Mapping, Sequence

from packages.orchestration.exec_guard import ExecGuardPolicy, ExecGuardResult, run_guarded
from packages.orchestration.sandbox_profiles import SandboxDimensionEnforcement, SandboxProfile
from packages.orchestration.tool_sandbox import SANDBOX_MISSING, SandboxUnavailable

#: The two container runtimes Remedy recognises, in the order `container_runtime_path` prefers
#: them (DECISION F162 D7 (1)): podman needs no daemon, so it is tried first.
CONTAINER_RUNTIME_NAMES = ("podman", "docker")

#: WHY 30 seconds: `image inspect` and the cleanup `rm -f` are both local daemon queries, never a
#: pull, so they cannot legitimately take longer than this module's other short calls.
_RUNTIME_PROBE_TIMEOUT_SECONDS = 30.0


def container_runtime_path() -> str | None:
    """The first installed runtime of `CONTAINER_RUNTIME_NAMES`, or None if neither is on PATH."""
    for name in CONTAINER_RUNTIME_NAMES:
        found = shutil.which(name)
        if found:
            return found
    return None


def container_image_present(runtime: str, image: str) -> bool:
    """Whether *image* already sits in *runtime*'s local store; Remedy never pulls one itself."""
    result = run_guarded(
        [runtime, "image", "inspect", image],
        ExecGuardPolicy(wall_timeout_seconds=_RUNTIME_PROBE_TIMEOUT_SECONDS))
    return result.returncode == 0


def container_run_argv(
    profile: SandboxProfile, *, runtime: str, image: str, workspace: str,
    argv: Sequence[str], env: Mapping[str, str], name: str,
) -> list[str]:
    """Compile *profile* onto one `<runtime> run` argv; `--pull never` always (DECISION F162 D7 (2))."""
    uid, gid = os.getuid(), os.getgid()
    network = "host" if profile.net.mode == "allowlist" else "none"
    tmp = (f"/tmp:rw,size={profile.tmp_quota_mb}m" if profile.tmp_quota_mb is not None
           else "/tmp:rw")
    out = [
        runtime, "run", "--rm", "--init", "--pull", "never", "--name", name,
        "--read-only", "--user", f"{uid}:{gid}", "--network", network,
        "-v", f"{workspace}:{workspace}:rw", "-w", workspace, "--tmpfs", tmp,
    ]
    if profile.ulimits.cpu_s is not None:
        out += ["--ulimit", f"cpu={profile.ulimits.cpu_s}:{profile.ulimits.cpu_s + 2}"]
    if profile.ulimits.nofile is not None:
        out += ["--ulimit", f"nofile={profile.ulimits.nofile}:{profile.ulimits.nofile}"]
    if profile.ulimits.mem_mb is not None:
        out += ["--memory", f"{profile.ulimits.mem_mb}m",
                "--memory-swap", f"{profile.ulimits.mem_mb}m"]
    combined = {**env, "HOME": "/tmp", "TMPDIR": "/tmp"}
    for key in sorted(combined):
        out += ["-e", f"{key}={combined[key]}"]
    return out + [image, *argv]


# WHY: the one caller that both runs a process in a container and limits its CPU, so a sandboxed
# CPU death's attribution lives here, mirroring run_guarded_with_sandbox_profile's own reasoning
# for the process runner (DECISION F162 D7 (3)).
def run_in_container_with_sandbox_profile(
    argv: Sequence[str], profile: SandboxProfile, *, workspace: str, image: str,
    base: ExecGuardPolicy = ExecGuardPolicy(),
) -> ExecGuardResult:
    """Run *argv* under *profile* inside a container; refuses rather than installing or pulling."""
    runtime = container_runtime_path()
    if runtime is None:
        raise SandboxUnavailable(
            SANDBOX_MISSING, "no container runtime (podman or docker) is installed",
            "install podman or docker, then retry")
    if not container_image_present(runtime, image):
        raise SandboxUnavailable(
            SANDBOX_MISSING, f"the image {image!r} is not present locally; Remedy never pulls one",
            f"pull {image} yourself, then retry")
    name = f"remedy-sbx-{uuid.uuid4().hex[:12]}"
    run_argv = container_run_argv(
        profile, runtime=runtime, image=image, workspace=workspace, argv=argv,
        env=base.env if base.env is not None else {}, name=name)
    policy = ExecGuardPolicy(wall_timeout_seconds=base.wall_timeout_seconds,
                              output_cap_bytes=base.output_cap_bytes, cwd=base.cwd,
                              cancel_check=base.cancel_check)
    result = run_guarded(run_argv, policy)
    if result.tripped_limit in ("wall_timeout", "cancelled"):
        # A killed client can leave its container running; one cleanup call, best effort.
        run_guarded([runtime, "rm", "-f", name],
                    ExecGuardPolicy(wall_timeout_seconds=_RUNTIME_PROBE_TIMEOUT_SECONDS))
    if (result.tripped_limit is None and profile.ulimits.cpu_s is not None
            and result.returncode == 128 + signal.SIGXCPU):
        return dataclasses.replace(result, classification="resource_limit",
                                    tripped_limit="cpu_seconds")
    return result


def _container_enforcement_for_fs_scope(
        profile: SandboxProfile, runtime_available: bool) -> SandboxDimensionEnforcement:
    """fs_scope is enforced only by the container's read-only root plus its one writable mount."""
    if not runtime_available:
        return SandboxDimensionEnforcement(
            "fs_scope", "unenforced", "no container runtime: the container runner refuses to run")
    if "{workspace}" in profile.fs_scope:
        return SandboxDimensionEnforcement(
            "fs_scope", "enforced",
            "the container's root is read-only and the workspace is its one writable mount")
    return SandboxDimensionEnforcement(
        "fs_scope", "unenforced",
        "the container mounts the whole workspace, wider than the declared scope")


def _container_enforcement_for_net(
        profile: SandboxProfile, runtime_available: bool) -> SandboxDimensionEnforcement:
    """deny is enforced by `--network none`; an allowlist shares the host network unfiltered."""
    if not runtime_available:
        return SandboxDimensionEnforcement(
            "net", "unenforced", "no container runtime: the container runner refuses to run")
    if profile.net.mode == "deny":
        return SandboxDimensionEnforcement("net", "enforced", "the container has no network")
    return SandboxDimensionEnforcement(
        "net", "unenforced", "the container shares the host network and hosts are not filtered")


def _container_enforcement_for_ulimit(
        key: str, value: int | None, runtime_available: bool,
        reason: str) -> SandboxDimensionEnforcement:
    """A ulimits key is enforced by the container's own `--ulimit` or cgroup, given a runtime."""
    dimension = f"ulimits.{key}"
    if value is None:
        return SandboxDimensionEnforcement(dimension, "enforced", "nothing to limit")
    if not runtime_available:
        return SandboxDimensionEnforcement(
            dimension, "unenforced", "no container runtime: the container runner refuses to run")
    return SandboxDimensionEnforcement(dimension, "enforced", reason)


def _container_enforcement_for_allowed_binaries(
        value: tuple[str, ...] | None, runtime_available: bool) -> SandboxDimensionEnforcement:
    """No mechanism filters binaries by name inside a container either."""
    if value is None:
        return SandboxDimensionEnforcement("allowed_binaries", "enforced", "nothing to limit")
    if not runtime_available:
        return SandboxDimensionEnforcement(
            "allowed_binaries", "unenforced",
            "no container runtime: the container runner refuses to run")
    return SandboxDimensionEnforcement(
        "allowed_binaries", "unenforced", "binaries are not filtered by name")


def _container_enforcement_for_tmp_quota(
        value: int | None, runtime_available: bool) -> SandboxDimensionEnforcement:
    """A tmp quota is the one dimension the container runner enforces that the process one does not."""
    if value is None:
        return SandboxDimensionEnforcement("tmp_quota_mb", "enforced", "nothing to limit")
    if not runtime_available:
        return SandboxDimensionEnforcement(
            "tmp_quota_mb", "unenforced",
            "no container runtime: the container runner refuses to run")
    return SandboxDimensionEnforcement(
        "tmp_quota_mb", "enforced", "a size-limited /tmp inside the container")


def container_sandbox_enforcement(
        profile: SandboxProfile, *, runtime_available: bool) -> tuple[SandboxDimensionEnforcement, ...]:
    """The per-dimension honesty record for the container runner (DECISION F162 D7 (4))."""
    return (
        _container_enforcement_for_fs_scope(profile, runtime_available),
        _container_enforcement_for_net(profile, runtime_available),
        _container_enforcement_for_ulimit(
            "cpu_s", profile.ulimits.cpu_s, runtime_available, "--ulimit cpu inside the container"),
        _container_enforcement_for_ulimit(
            "mem_mb", profile.ulimits.mem_mb, runtime_available,
            "the container's cgroup memory limit"),
        _container_enforcement_for_ulimit(
            "nofile", profile.ulimits.nofile, runtime_available,
            "--ulimit nofile inside the container"),
        _container_enforcement_for_allowed_binaries(profile.allowed_binaries, runtime_available),
        _container_enforcement_for_tmp_quota(profile.tmp_quota_mb, runtime_available),
    )
