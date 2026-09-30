"""Test-load governor: the worker cap, the CPU priority and the one-line run record.

Operator amendment amend0930-test-load (2026-09-30). ``tests/conftest.py`` wires these helpers
into every pytest run of this repository, however it is started, so a limit placed here cannot
be missed the way a limit in ``scripts/remedy_pytest.sh`` would be.

A cap lowers the heat at any one moment; it does not lower the electricity used, because the
same work only takes longer. The record written here is how that work is measured.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

#: Parallel workers a run may start when ``REMEDY_TEST_MAX_WORKERS`` is unset or not a number.
DEFAULT_MAX_WORKERS = 6
#: Niceness a run lowers itself to when ``REMEDY_TEST_NICE`` is unset or not a number.
DEFAULT_NICE = 10
#: The run record is cut to its newer half when it grows past this many bytes.
LOAD_LOG_LIMIT_BYTES = 5 * 1024 * 1024
#: The command line is shortened to this many characters in the record.
LOAD_LOG_COMMAND_CHARS = 300


def _whole_number(raw: str | None, default: int) -> int:
    try:
        return max(0, int(raw.strip())) if raw and raw.strip() else default
    except ValueError:
        return default


def worker_cap(environ=None) -> int:
    """The worker cap; 0 means "no cap"."""
    env = os.environ if environ is None else environ
    return _whole_number(env.get("REMEDY_TEST_MAX_WORKERS"), DEFAULT_MAX_WORKERS)


def auto_worker_count(cpus: int | None = None, environ=None) -> int:
    """What ``-n auto`` and ``-n logical`` resolve to: the smaller of the cap and the CPU count."""
    machine = cpus if cpus is not None else (os.cpu_count() or 1)
    cap = worker_cap(environ)
    return machine if cap == 0 else max(1, min(cap, machine))


def clamped_worker_count(asked, environ=None):
    """The worker count an explicit ``-n N`` really gets; anything that is not a number stays as is."""
    cap = worker_cap(environ)
    if cap and isinstance(asked, int) and asked > cap:
        return cap
    return asked


def cap_notice(asked: int, cap: int) -> str:
    return (f"remedy tests: -n {asked} is above the worker cap, running {cap} workers "
            f"(REMEDY_TEST_MAX_WORKERS)")


def lower_priority(environ=None) -> int | None:
    """Lower this process to the wanted niceness; never raise priority, ignore an OSError.

    Returns the niceness after the call, or None when it could not be read.
    """
    env = os.environ if environ is None else environ
    wanted = _whole_number(env.get("REMEDY_TEST_NICE"), DEFAULT_NICE)
    try:
        current = os.nice(0)
        if wanted and current < wanted:
            current = os.nice(wanted - current)
        return current
    except OSError:
        return None


def load_log_path(environ=None, home: Path | None = None) -> Path | None:
    """Where the run record goes, or None for "nowhere".

    ``REMEDY_TEST_LOAD_LOG`` set to a path wins; set and empty means nothing; unset means
    ``~/.remedy-loop/test_load.jsonl`` when that folder exists.
    """
    env = os.environ if environ is None else environ
    if "REMEDY_TEST_LOAD_LOG" in env:
        raw = env["REMEDY_TEST_LOAD_LOG"].strip()
        return Path(raw) if raw else None
    folder = (home or Path.home()) / ".remedy-loop"
    return folder / "test_load.jsonl" if folder.is_dir() else None


def _cpu_seconds() -> float:
    t = os.times()
    return t.user + t.system + t.children_user + t.children_system


def note_start() -> dict:
    """The reading taken when a run starts."""
    return {"wall": time.monotonic(), "cpu": _cpu_seconds()}


def build_record(start: dict, collected: int, exit_status: int, workers: int, command: str) -> dict:
    return {
        "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "command": command[:LOAD_LOG_COMMAND_CHARS],
        "collected": collected,
        "exit_status": exit_status,
        "wall_seconds": round(time.monotonic() - start["wall"], 2),
        "cpu_seconds": round(_cpu_seconds() - start["cpu"], 2),
        "workers": workers,
    }


def keep_newer_half(path: Path, limit: int = LOAD_LOG_LIMIT_BYTES) -> None:
    """Cut a record file above ``limit`` bytes to its newer half, on a line boundary."""
    if path.stat().st_size <= limit:
        return
    data = path.read_bytes()
    tail = data[len(data) // 2:]
    cut = tail.find(b"\n")
    path.write_bytes(tail[cut + 1:] if cut >= 0 else b"")


def append_record(path: Path, record: dict, limit: int = LOAD_LOG_LIMIT_BYTES) -> bool:
    """Append one JSON line; a failed write never fails a test run."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            keep_newer_half(path, limit)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
        return True
    except OSError:
        return False


# F293 T003: a test run that leaves a process behind fails (R-1118). The run's controller puts a
# mark into its own environment before any worker starts, so every process the run starts carries
# it unless something strips the environment; the runtime server's child spawn does exactly that,
# so a process is also the run's when its working folder or an argument lies in the run's
# temporary folder. The name does not start with ``REMEDY_``, because every run's input snapshot
# records each ``REMEDY_`` variable and a mark that changes per run must not reach it.

#: The environment variable that carries the run's mark.
RUN_MARK_VARIABLE = "PYTEST_REMEDY_RUN_MARK"
#: Seconds a process found at the end of a run gets to finish exiting before it counts as left.
LEFTOVER_GRACE_SECONDS = 3.0


def new_run_mark() -> str:
    return uuid.uuid4().hex


def _inside(text: str, folders: list[str]) -> bool:
    return any(text == folder or folder + os.sep in text for folder in folders)


def leftover_processes(mark: str, folders) -> list:
    """This user's processes, other than this one and its parents, that belong to the run.

    A process belongs to the run when its environment carries ``mark``, or when its working
    folder or one of its arguments lies inside one of ``folders``. A zombie has already ended.
    """
    import psutil

    folder_texts = [str(folder) for folder in folders if folder]
    me = psutil.Process()
    skip = {me.pid, *(parent.pid for parent in me.parents())}
    uid = os.getuid()
    found = []
    for proc in psutil.process_iter(["pid", "uids", "status", "cmdline", "cwd", "environ"], ad_value=None):
        info = proc.info
        if info["pid"] in skip or info["uids"] is None or info["uids"].real != uid:
            continue
        if info["status"] == psutil.STATUS_ZOMBIE:
            continue
        marked = (info["environ"] or {}).get(RUN_MARK_VARIABLE) == mark
        placed = bool(folder_texts) and (
            _inside(info["cwd"] or "", folder_texts)
            or any(_inside(arg, folder_texts) for arg in info["cmdline"] or ()))
        if marked or placed:
            found.append(proc)
    return found


def end_processes(procs, grace: float = LEFTOVER_GRACE_SECONDS) -> list[str]:
    """Give ``procs`` ``grace`` seconds to exit, then end the rest; describe each one ended."""
    import psutil

    _gone, alive = psutil.wait_procs(procs, timeout=grace)
    ended = []
    for proc in alive:
        try:
            ended.append(f"pid {proc.pid}: {' '.join(proc.cmdline())[:LOAD_LOG_COMMAND_CHARS]}")
            proc.terminate()
        except psutil.Error:
            continue
    _gone, stubborn = psutil.wait_procs(alive, timeout=grace)
    for proc in stubborn:
        try:
            proc.kill()
        except psutil.Error:
            continue
    return ended


def leftover_notice(ended: list[str]) -> str:
    return (f"remedy tests: the run left {len(ended)} process(es) behind, now ended "
            f"(F293 T003): " + "; ".join(ended))
