"""F200 T002 — the systemd unit and the container entrypoint behave, not just exist.

`scripts/serve/remedy-serve.service` and `scripts/serve/container-entrypoint.sh`
are the lifecycle artifacts named in the feature file's amended Task slicing
(DECISION F200 D1). This module proves their real content: the
unit file's fields a systemd user service needs (``ExecStart`` running `serve
start`, ``KillMode=process`` so a stop or restart never kills the runs the
supervisor started, ``Restart=on-failure`` and ``Type=simple``); and the
entrypoint's actual behaviour, run for real against a stub `remedy` executable
written into ``tmp_path`` — the argument passthrough, the `REMEDY_DATA_DIR`
directory creation, the `exec` replacement (the stub inherits the SAME process
id the entrypoint was started with, proving no wrapping shell is left
running), and the refusal with exit 2 and no stub execution at all when
`REMEDY_DATA_DIR` is unset.
"""
from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
UNIT_FILE = REPO_ROOT / "scripts" / "serve" / "remedy-serve.service"
ENTRYPOINT = REPO_ROOT / "scripts" / "serve" / "container-entrypoint.sh"

#: A minimal stub standing in for the `remedy` console script: it records its
#: own process id, the `REMEDY_DATA_DIR` it was run with and every argument it
#: received, one per line, to the file named by `STUB_OUTPUT`, then exits 0.
_STUB_SOURCE = """#!/usr/bin/env bash
{
  printf '%s\\n' "$$"
  printf '%s\\n' "${REMEDY_DATA_DIR:-}"
  for arg in "$@"; do
    printf '%s\\n' "$arg"
  done
} > "${STUB_OUTPUT}"
"""


def _write_stub(tmp_path: Path) -> Path:
    stub = tmp_path / "remedy-stub.sh"
    stub.write_text(_STUB_SOURCE, encoding="utf-8")
    stub.chmod(0o755)
    return stub


def _parse_unit(text: str) -> dict[str, str]:
    """A naive `key=value` reading of the unit file's body lines."""
    settings: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("["):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        settings[key.strip()] = value.strip()
    return settings


# ---------------------------------------------------------------------------
# The systemd unit
# ---------------------------------------------------------------------------

def test_unit_file_exists_and_parses():
    assert UNIT_FILE.is_file()
    settings = _parse_unit(UNIT_FILE.read_text(encoding="utf-8"))
    assert settings, "the unit file has no key=value settings at all"


def test_unit_exec_start_runs_serve_start():
    settings = _parse_unit(UNIT_FILE.read_text(encoding="utf-8"))
    assert settings["ExecStart"].endswith("serve start")


def test_unit_kill_mode_is_process():
    """KillMode=process: a stop or restart ends only the supervisor, never its runs."""
    settings = _parse_unit(UNIT_FILE.read_text(encoding="utf-8"))
    assert settings["KillMode"] == "process"


def test_unit_restarts_on_failure():
    settings = _parse_unit(UNIT_FILE.read_text(encoding="utf-8"))
    assert settings["Restart"] == "on-failure"


def test_unit_type_is_simple():
    settings = _parse_unit(UNIT_FILE.read_text(encoding="utf-8"))
    assert settings["Type"] == "simple"


# ---------------------------------------------------------------------------
# The container entrypoint
# ---------------------------------------------------------------------------

def test_entrypoint_shell_syntax_is_valid():
    result = subprocess.run(["bash", "-n", str(ENTRYPOINT)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_entrypoint_is_executable_on_disk():
    mode = ENTRYPOINT.stat().st_mode
    assert mode & stat.S_IXUSR, "container-entrypoint.sh is not owner-executable on disk"
    assert os.access(ENTRYPOINT, os.X_OK)


def test_entrypoint_execs_the_stub_with_serve_start_and_extra_args(tmp_path):
    stub = _write_stub(tmp_path)
    stub_output = tmp_path / "stub-output.txt"
    data_dir = tmp_path / "data-root" / "nested"
    env = {**os.environ, "REMEDY_DATA_DIR": str(data_dir), "REMEDY_BIN": str(stub),
           "STUB_OUTPUT": str(stub_output)}

    proc = subprocess.Popen(["bash", str(ENTRYPOINT), "--json"], env=env)
    returncode = proc.wait(timeout=30)

    assert returncode == 0
    assert data_dir.is_dir(), "REMEDY_DATA_DIR was not created"

    lines = stub_output.read_text(encoding="utf-8").splitlines()
    stub_pid, stub_data_dir, *stub_argv = lines
    assert stub_argv == ["serve", "start", "--json"]
    assert stub_data_dir == str(data_dir)
    # Proof of `exec`: the stub ran AS the entrypoint's own process, not as a
    # child of a shell the entrypoint left running.
    assert stub_pid == str(proc.pid)


def test_entrypoint_defaults_remedy_bin_to_plain_remedy_on_path(tmp_path):
    """With no REMEDY_BIN, the entrypoint execs `remedy` resolved on PATH."""
    stub = _write_stub(tmp_path)
    fake_bin_dir = tmp_path / "bin"
    fake_bin_dir.mkdir()
    (fake_bin_dir / "remedy").write_bytes(stub.read_bytes())
    (fake_bin_dir / "remedy").chmod(0o755)
    stub_output = tmp_path / "stub-output.txt"
    data_dir = tmp_path / "data-root"
    env = {**os.environ, "REMEDY_DATA_DIR": str(data_dir),
           "PATH": f"{fake_bin_dir}{os.pathsep}{os.environ.get('PATH', '')}",
           "STUB_OUTPUT": str(stub_output)}
    env.pop("REMEDY_BIN", None)

    proc = subprocess.run(["bash", str(ENTRYPOINT)], env=env)

    assert proc.returncode == 0
    lines = stub_output.read_text(encoding="utf-8").splitlines()
    assert lines[1:] == [str(data_dir), "serve", "start"]


def test_entrypoint_refuses_without_data_dir_and_never_runs_the_stub(tmp_path):
    stub = _write_stub(tmp_path)
    stub_output = tmp_path / "stub-output.txt"
    env = {k: v for k, v in os.environ.items() if k != "REMEDY_DATA_DIR"}
    env["REMEDY_BIN"] = str(stub)
    env["STUB_OUTPUT"] = str(stub_output)

    result = subprocess.run(["bash", str(ENTRYPOINT)], env=env, capture_output=True, text=True,
                             timeout=30)

    assert result.returncode == 2
    assert "REMEDY_DATA_DIR" in result.stderr
    assert not stub_output.exists(), "the stub ran despite REMEDY_DATA_DIR being unset"


def test_entrypoint_and_docs_both_tell_the_operator_to_run_with_an_init_process():
    """DECISION F200 D8: 'the container entrypoint ... expects the container
    to run with an init process.' A requirement an operator never reads is no
    requirement at all, so both of its stated homes must carry it: the
    entrypoint's own header comment, and the built-state page."""
    entrypoint_text = ENTRYPOINT.read_text(encoding="utf-8")
    assert "--init" in entrypoint_text
    assert "docker run --init" in entrypoint_text

    docs_page = REPO_ROOT / "docs" / "system" / "serve-daemon-v1.md"
    docs_text = docs_page.read_text(encoding="utf-8")
    assert "docker run --init" in docs_text


def test_entrypoint_refuses_with_empty_data_dir_too(tmp_path):
    stub = _write_stub(tmp_path)
    stub_output = tmp_path / "stub-output.txt"
    env = {**os.environ, "REMEDY_DATA_DIR": "", "REMEDY_BIN": str(stub),
           "STUB_OUTPUT": str(stub_output)}

    result = subprocess.run(["bash", str(ENTRYPOINT)], env=env, capture_output=True, text=True,
                             timeout=30)

    assert result.returncode == 2
    assert not stub_output.exists()
