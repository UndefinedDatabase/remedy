"""Pins DECISION F162 D7: the optional container sandbox runner.

F162 round 7 C2 pins the pure compiler (`container_run_argv`), the runtime lookup, the refusal
shapes and the enforcement record — none of it starting a real container. F162 round 7 C3 adds
the fixture processes D3 (5) shares with the process runner, run for real against a local
`python:3.12-slim`.
"""
from __future__ import annotations

import os
import signal

import pytest

import packages.orchestration.sandbox_container as SC
from packages.orchestration.exec_guard import ExecGuardResult
from packages.orchestration.sandbox_container import (
    CONTAINER_RUNTIME_NAMES,
    container_run_argv,
    container_sandbox_enforcement,
    run_in_container_with_sandbox_profile,
)
from packages.orchestration.sandbox_profiles import (
    SANDBOX_ENFORCEMENT_KEYS,
    SandboxDimensionEnforcement,
    get_sandbox_profile,
)
from packages.orchestration.tool_sandbox import SANDBOX_MISSING, SandboxUnavailable

# ---------------------------------------------------------------------------
# F162 round 7 C2: the compiler, the runtime lookup, the refusal and the record.
# ---------------------------------------------------------------------------


def test_container_run_argv_for_strict_equals_the_literal(tmp_path):
    uid, gid = os.getuid(), os.getgid()
    workspace = str(tmp_path)
    argv = container_run_argv(
        get_sandbox_profile("strict"), runtime="docker", image="python:3.12-slim",
        workspace=workspace, argv=["python3", "-c", "pass"], env={"PATH": "/usr/bin"},
        name="remedy-sbx-test")
    assert argv == [
        "docker", "run", "--rm", "--init", "--pull", "never", "--name", "remedy-sbx-test",
        "--read-only", "--user", f"{uid}:{gid}", "--network", "none",
        "-v", f"{workspace}:{workspace}:rw", "-w", workspace, "--tmpfs", "/tmp:rw,size=64m",
        "--ulimit", "cpu=600:602", "--ulimit", "nofile=256:256",
        "--memory", "2048m", "--memory-swap", "2048m",
        "-e", "HOME=/tmp", "-e", "PATH=/usr/bin", "-e", "TMPDIR=/tmp",
        "python:3.12-slim", "python3", "-c", "pass",
    ]


def test_container_run_argv_for_standard_equals_the_literal(tmp_path):
    uid, gid = os.getuid(), os.getgid()
    workspace = str(tmp_path)
    argv = container_run_argv(
        get_sandbox_profile("standard"), runtime="docker", image="python:3.12-slim",
        workspace=workspace, argv=["python3", "-c", "pass"], env={"PATH": "/usr/bin"},
        name="remedy-sbx-test")
    assert argv == [
        "docker", "run", "--rm", "--init", "--pull", "never", "--name", "remedy-sbx-test",
        "--read-only", "--user", f"{uid}:{gid}", "--network", "none",
        "-v", f"{workspace}:{workspace}:rw", "-w", workspace, "--tmpfs", "/tmp:rw,size=512m",
        "--ulimit", "cpu=1800:1802", "--ulimit", "nofile=1024:1024",
        "-e", "HOME=/tmp", "-e", "PATH=/usr/bin", "-e", "TMPDIR=/tmp",
        "python:3.12-slim", "python3", "-c", "pass",
    ]


def test_container_run_argv_for_net_local_equals_the_literal(tmp_path):
    uid, gid = os.getuid(), os.getgid()
    workspace = str(tmp_path)
    argv = container_run_argv(
        get_sandbox_profile("net-local"), runtime="docker", image="python:3.12-slim",
        workspace=workspace, argv=["python3", "-c", "pass"], env={"PATH": "/usr/bin"},
        name="remedy-sbx-test")
    assert argv == [
        "docker", "run", "--rm", "--init", "--pull", "never", "--name", "remedy-sbx-test",
        "--read-only", "--user", f"{uid}:{gid}", "--network", "host",
        "-v", f"{workspace}:{workspace}:rw", "-w", workspace, "--tmpfs", "/tmp:rw,size=512m",
        "--ulimit", "cpu=1800:1802", "--ulimit", "nofile=1024:1024",
        "-e", "HOME=/tmp", "-e", "PATH=/usr/bin", "-e", "TMPDIR=/tmp",
        "python:3.12-slim", "python3", "-c", "pass",
    ]


def test_container_runtime_path_answers_podman_before_docker(monkeypatch):
    assert CONTAINER_RUNTIME_NAMES == ("podman", "docker")
    monkeypatch.setattr(SC.shutil, "which",
                         lambda name: f"/usr/bin/{name}" if name in ("podman", "docker") else None)
    assert SC.container_runtime_path() == "/usr/bin/podman"


def test_container_runtime_path_answers_docker_when_podman_is_absent(monkeypatch):
    monkeypatch.setattr(SC.shutil, "which", lambda name: "/usr/bin/docker" if name == "docker" else None)
    assert SC.container_runtime_path() == "/usr/bin/docker"


def test_container_runtime_path_answers_none_when_neither_is_found(monkeypatch):
    monkeypatch.setattr(SC.shutil, "which", lambda name: None)
    assert SC.container_runtime_path() is None


def _stub_result(returncode: int | None, tripped_limit: str | None = None,
                  classification: str = "failed") -> ExecGuardResult:
    return ExecGuardResult(
        returncode=returncode, term_signal=None, stdout=b"", stderr=b"", stdout_truncated=False,
        stderr_truncated=False, stdout_bytes_seen=0, stderr_bytes_seen=0, streams_complete=True,
        wall_seconds=0.0, cpu_seconds_used=0.0, classification=classification,
        tripped_limit=tripped_limit, limits_enforced=(), limits_unsupported=())


def test_the_runner_refuses_with_sandbox_missing_when_no_runtime_is_installed(tmp_path, monkeypatch):
    monkeypatch.setattr(SC, "container_runtime_path", lambda: None)

    def _no_run(argv, policy):
        raise AssertionError("nothing should run without a runtime")

    monkeypatch.setattr(SC, "run_guarded", _no_run)
    with pytest.raises(SandboxUnavailable) as excinfo:
        run_in_container_with_sandbox_profile(
            ["x"], get_sandbox_profile("strict"), workspace=str(tmp_path), image="python:3.12-slim")
    assert excinfo.value.state == SANDBOX_MISSING


def test_the_runner_refuses_naming_the_image_when_it_is_not_present_locally(tmp_path, monkeypatch):
    monkeypatch.setattr(SC, "container_runtime_path", lambda: "/usr/bin/docker")
    monkeypatch.setattr(SC, "container_image_present", lambda runtime, image: False)

    def _no_run(argv, policy):
        raise AssertionError("nothing should run for an absent image")

    monkeypatch.setattr(SC, "run_guarded", _no_run)
    with pytest.raises(SandboxUnavailable) as excinfo:
        run_in_container_with_sandbox_profile(
            ["x"], get_sandbox_profile("strict"), workspace=str(tmp_path), image="python:3.12-slim")
    assert excinfo.value.state == SANDBOX_MISSING
    assert "python:3.12-slim" in str(excinfo.value)
    assert "never pulls" in str(excinfo.value)


def test_the_runner_attributes_a_152_exit_as_resource_limit_cpu_seconds(tmp_path, monkeypatch):
    monkeypatch.setattr(SC, "container_runtime_path", lambda: "/usr/bin/docker")
    monkeypatch.setattr(SC, "container_image_present", lambda runtime, image: True)
    cpu_result = _stub_result(128 + signal.SIGXCPU)
    monkeypatch.setattr(SC, "run_guarded", lambda argv, policy: cpu_result)
    attributed = run_in_container_with_sandbox_profile(
        ["x"], get_sandbox_profile("strict"), workspace=str(tmp_path), image="python:3.12-slim")
    assert attributed is not cpu_result
    assert attributed.classification == "resource_limit"
    assert attributed.tripped_limit == "cpu_seconds"


def test_the_runner_leaves_a_137_exit_unchanged(tmp_path, monkeypatch):
    monkeypatch.setattr(SC, "container_runtime_path", lambda: "/usr/bin/docker")
    monkeypatch.setattr(SC, "container_image_present", lambda runtime, image: True)
    killed_result = _stub_result(137)
    monkeypatch.setattr(SC, "run_guarded", lambda argv, policy: killed_result)
    unchanged = run_in_container_with_sandbox_profile(
        ["x"], get_sandbox_profile("strict"), workspace=str(tmp_path), image="python:3.12-slim")
    assert unchanged is killed_result


def test_a_wall_timeout_makes_exactly_one_further_rm_f_call(tmp_path, monkeypatch):
    monkeypatch.setattr(SC, "container_runtime_path", lambda: "/usr/bin/docker")
    monkeypatch.setattr(SC, "container_image_present", lambda runtime, image: True)
    calls: list[list[str]] = []
    timeout_result = _stub_result(None, tripped_limit="wall_timeout")

    def _record(argv, policy):
        calls.append(list(argv))
        return timeout_result

    monkeypatch.setattr(SC, "run_guarded", _record)
    run_in_container_with_sandbox_profile(
        ["x"], get_sandbox_profile("strict"), workspace=str(tmp_path), image="python:3.12-slim")
    assert len(calls) == 2
    name = calls[0][calls[0].index("--name") + 1]
    assert calls[1] == ["/usr/bin/docker", "rm", "-f", name]


def test_a_cancelled_result_also_makes_one_rm_f_call(tmp_path, monkeypatch):
    monkeypatch.setattr(SC, "container_runtime_path", lambda: "/usr/bin/docker")
    monkeypatch.setattr(SC, "container_image_present", lambda runtime, image: True)
    calls: list[list[str]] = []
    cancelled_result = _stub_result(None, tripped_limit="cancelled")

    def _record(argv, policy):
        calls.append(list(argv))
        return cancelled_result

    monkeypatch.setattr(SC, "run_guarded", _record)
    run_in_container_with_sandbox_profile(
        ["x"], get_sandbox_profile("strict"), workspace=str(tmp_path), image="python:3.12-slim")
    assert len(calls) == 2
    assert calls[1][1:3] == ["rm", "-f"]


#: One (profile, runtime_available, expected states) row per built-in of DECISION F162 D7 (4).
_CONTAINER_ENFORCEMENT_TABLE_CASES = (
    ("strict", True, (
        ("fs_scope", "enforced"), ("net", "enforced"), ("ulimits.cpu_s", "enforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "enforced"),
        ("allowed_binaries", "unenforced"), ("tmp_quota_mb", "enforced"),
    )),
    ("strict", False, (
        ("fs_scope", "unenforced"), ("net", "unenforced"), ("ulimits.cpu_s", "unenforced"),
        ("ulimits.mem_mb", "unenforced"), ("ulimits.nofile", "unenforced"),
        ("allowed_binaries", "unenforced"), ("tmp_quota_mb", "unenforced"),
    )),
    ("standard", True, (
        ("fs_scope", "enforced"), ("net", "enforced"), ("ulimits.cpu_s", "enforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "enforced"),
        ("allowed_binaries", "enforced"), ("tmp_quota_mb", "enforced"),
    )),
    ("standard", False, (
        ("fs_scope", "unenforced"), ("net", "unenforced"), ("ulimits.cpu_s", "unenforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "unenforced"),
        ("allowed_binaries", "enforced"), ("tmp_quota_mb", "unenforced"),
    )),
    ("net-local", True, (
        ("fs_scope", "enforced"), ("net", "unenforced"), ("ulimits.cpu_s", "enforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "enforced"),
        ("allowed_binaries", "enforced"), ("tmp_quota_mb", "enforced"),
    )),
    ("net-local", False, (
        ("fs_scope", "unenforced"), ("net", "unenforced"), ("ulimits.cpu_s", "unenforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "unenforced"),
        ("allowed_binaries", "enforced"), ("tmp_quota_mb", "unenforced"),
    )),
)


@pytest.mark.parametrize(
    "profile_name,runtime_available,expected", _CONTAINER_ENFORCEMENT_TABLE_CASES,
    ids=[f"{c[0]}-{c[1]}" for c in _CONTAINER_ENFORCEMENT_TABLE_CASES])
def test_container_sandbox_enforcement_key_state_table(profile_name, runtime_available, expected):
    profile = get_sandbox_profile(profile_name)
    record = container_sandbox_enforcement(profile, runtime_available=runtime_available)
    assert tuple(e.key for e in record) == SANDBOX_ENFORCEMENT_KEYS
    assert tuple((e.key, e.state) for e in record) == expected


def test_container_sandbox_enforcement_full_tuple_for_strict_with_a_runtime():
    record = container_sandbox_enforcement(get_sandbox_profile("strict"), runtime_available=True)
    assert record == (
        SandboxDimensionEnforcement(
            "fs_scope", "enforced",
            "the container's root is read-only and the workspace is its one writable mount"),
        SandboxDimensionEnforcement("net", "enforced", "the container has no network"),
        SandboxDimensionEnforcement(
            "ulimits.cpu_s", "enforced", "--ulimit cpu inside the container"),
        SandboxDimensionEnforcement(
            "ulimits.mem_mb", "enforced", "the container's cgroup memory limit"),
        SandboxDimensionEnforcement(
            "ulimits.nofile", "enforced", "--ulimit nofile inside the container"),
        SandboxDimensionEnforcement(
            "allowed_binaries", "unenforced", "binaries are not filtered by name"),
        SandboxDimensionEnforcement(
            "tmp_quota_mb", "enforced", "a size-limited /tmp inside the container"),
    )
