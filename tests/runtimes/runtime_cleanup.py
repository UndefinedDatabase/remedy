"""The cleanup contract every F007 subprocess proof file lives by.

A test that leaks a supervisor leaves a live log pump, a bound port, an unreaped child
and a runtime directory behind. One of those is a nuisance; a hundred of them are why the
COMPLETE files did not reach a final summary in the external review environment — a
machine roughly six times slower than ours, on which the old per-test cleanup (a full
process-table walk with a `cwd()` syscall for every process on the box) was itself a
significant part of the runtime.

So cleanup is now REGISTERED, not searched for:

* every helper that starts a runtime records the pids it was told about — supervisor, app
  and, for a state-corrupting test, the pids it can no longer read back out of
  runtime.json;
* teardown stops exactly those process groups, reaps our own children, and deletes only
  this test's own runtime control files;
* a cheap verification (command lines only — no syscall per process) proves nothing of
  this test survived, and FAILS FAST with the process table instead of letting the file
  hang until somebody's global timeout;
* one scan per FILE, not per test, then proves that nothing from this run's pytest
  basetemp is still alive.

Nothing outside the test's own temporary directory is ever inspected, and nothing outside
its own registered process groups is ever signalled.
"""
from __future__ import annotations

import contextlib
import os
from pathlib import Path

import psutil

from packages.runtimes import dev_server as DS

#: Control files a test's runtime directory may contain. Only these are removed, and only
#: under the test's own data root.
RUNTIME_CONTROL_FILES = (
    "runtime.json", "runtime.log", "runtime.handshake.json", "runtime.spec.json",
    "runtime.stop", "runtime.stop.invalid", "runtime.log_failure.json",
)

#: How long a stopped process group gets before it is reported as a survivor.
STOP_GRACE_S = 5.0


def alive(pid: int) -> bool:
    if not pid:
        return False
    try:
        proc = psutil.Process(int(pid))
        return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False
    except psutil.Error:
        return True


def _describe(pid: int) -> str:
    with contextlib.suppress(psutil.Error):
        proc = psutil.Process(pid)
        return f"{pid} {' '.join(proc.cmdline())[:90]}"
    return f"{pid} <gone>"


class RuntimeRegistry:
    """Everything one test started, remembered out of band.

    Out of band matters: a test that deliberately corrupts or rewrites runtime.json can no
    longer learn its own pids from it, and a supervisor whose recorded identity was
    mutated is exactly the one `runtime stop` will (correctly) refuse to touch. The
    registry is how such a test still cleans up after itself.
    """

    def __init__(self, tmp_path: Path):
        self.tmp_path = Path(tmp_path)
        self.pids: set[int] = set()
        self.data_roots: set[Path] = set()
        self.projects: set[Path] = set()
        self.procs: list = []                # subprocess.Popen objects we own directly

    # -- recording ---------------------------------------------------------

    def track(self, *pids: int) -> None:
        for pid in pids:
            if pid:
                self.pids.add(int(pid))

    def track_proc(self, proc) -> None:
        self.procs.append(proc)
        self.track(proc.pid)

    def observe(self, payload: dict | None, project=None, data_root=None) -> None:
        """Record whatever a CLI payload told us about live processes."""
        if project is not None:
            self.projects.add(Path(project))
        if data_root is not None:
            self.data_roots.add(Path(data_root))
        if not isinstance(payload, dict):
            return
        for key in ("pid", "supervisor_pid"):
            with contextlib.suppress(TypeError, ValueError):
                self.track(int(payload.get(key) or 0))
        for pid in payload.get("survivors") or []:
            with contextlib.suppress(TypeError, ValueError):
                self.track(int(pid))

    # -- teardown ----------------------------------------------------------

    def _family(self, pid: int) -> list[int]:
        kids: list[int] = []
        with contextlib.suppress(psutil.Error):
            kids = [child.pid for child in psutil.Process(pid).children(recursive=True)]
        return kids

    def stop_everything(self) -> list[int]:
        """Stop exactly the process groups this test owns. Returns the survivors."""
        targets: list[int] = []
        for pid in sorted(self.pids):
            if alive(pid):
                targets.extend(self._family(pid))
                targets.append(pid)

        for pid in targets:
            with contextlib.suppress(Exception):
                DS.stop_process_tree(pid, grace=1.0)

        for proc in self.procs:               # close pipes, reap our direct children
            with contextlib.suppress(Exception):
                proc.kill()
            for stream in (proc.stdout, proc.stderr, proc.stdin):
                with contextlib.suppress(Exception):
                    if stream is not None:
                        stream.close()
            with contextlib.suppress(Exception):
                proc.wait(timeout=STOP_GRACE_S)

        while True:                           # no zombie children of the test process
            try:
                pid, _status = os.waitpid(-1, os.WNOHANG)
            except (ChildProcessError, OSError):
                break
            if pid == 0:
                break

        return sorted({pid for pid in targets if alive(pid)})

    def remove_control_files(self) -> None:
        """Delete this test's own runtime control files — nothing else, nowhere else."""
        for data_root in self.data_roots:
            projects = self.projects or {self.tmp_path / "proj"}
            for project in projects:
                with contextlib.suppress(Exception):
                    old = os.environ.get("REMEDY_DATA_DIR")
                    os.environ["REMEDY_DATA_DIR"] = str(data_root)
                    try:
                        rdir = DS.runtime_dir(project)
                    finally:
                        if old is None:
                            os.environ.pop("REMEDY_DATA_DIR", None)
                        else:
                            os.environ["REMEDY_DATA_DIR"] = old
                    for name in RUNTIME_CONTROL_FILES:
                        with contextlib.suppress(OSError):
                            (rdir / name).unlink()

    def survivors_in_tmp(self) -> list[str]:
        """Anything still alive that this test's tmp_path can be traced to.

        Command lines only: `process_iter(["pid", "cmdline"])` reads one file per process,
        while asking every process on the box for its cwd is a syscall per process and was
        itself a measurable part of the suite's runtime on a slow host. The supervisor
        carries `--repo <tmp>/proj` in its argv, and the application is registered from the
        serve payload, so nothing is missed.
        """
        root = str(self.tmp_path)
        mine = {os.getpid(), *(p.pid for p in psutil.Process().parents())}
        found: list[str] = []
        for proc in psutil.process_iter(["pid", "cmdline"]):
            if proc.pid in mine:
                continue
            with contextlib.suppress(psutil.Error):
                cmdline = " ".join(proc.info["cmdline"] or [])
                if root in cmdline:
                    found.append(f"{proc.pid} {cmdline[:90]}")
        for pid in sorted(self.pids):
            if alive(pid):
                found.append(_describe(pid))
        return sorted(set(found))


def basetemp_survivors(basetemp: Path) -> list[str]:
    """Every runtime process from THIS pytest run that is somehow still alive.

    Run once per file, not per test. Scoped to this run's basetemp: a leak from another
    suite is not swept up here, and nothing outside /tmp/pytest-* is ever looked at.
    """
    root = str(basetemp)
    mine = {os.getpid(), *(p.pid for p in psutil.Process().parents())}
    found: list[str] = []
    for proc in psutil.process_iter(["pid", "cmdline"]):
        if proc.pid in mine:
            continue
        with contextlib.suppress(psutil.Error):
            cmdline = " ".join(proc.info["cmdline"] or [])
            if not cmdline:
                continue
            if root in cmdline:
                found.append(f"{proc.pid} {cmdline[:90]}")
                continue
            if "server.py" in cmdline or "runtime_supervisor" in cmdline:
                with contextlib.suppress(psutil.Error):
                    if root in proc.cwd():
                        found.append(f"{proc.pid} {cmdline[:90]}")
    return sorted(set(found))
