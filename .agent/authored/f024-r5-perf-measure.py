#!/usr/bin/env python3
"""F024 R5 — the phase timeline's scrub budget tool (evidence, not product; DECISION F024 D5).

F023's tool (`.agent/authored/f023-r7-perf-measure.py`), re-pointed at the scrubber: one
self-contained entry copies its flat harness files (index.html, main.tsx, vite.config.mjs,
drive_chrome.mjs — found beside it under their own names or under the `f024-r5-perf-` prefix
they carry in `.agent/authored/`) into a fresh work dir under
`<repo root>/.remedy-wt/f024-perf-run`, symlinks its `node_modules` to the PRIMARY checkout's
`apps/ui/node_modules`, builds the harness with the primary's `vite`, serves `dist/` on
127.0.0.1, launches headless Chrome with a private profile, runs `drive_chrome.mjs` to time
every scrub position and sweep the handle across the committed 500-node fixture's ledger three
times, stops Chrome and the server by their OWN pids (never `pkill -f`), removes the work dir,
and exits 0 only when drive_chrome.mjs's budget verdict was PASS.

`main.tsx` imports the fixture, the stage, the bar and the timeline's own modules straight from
`<repo root>/apps/ui/src/` — this tool invents no fixture and no scrub logic of its own. The
optional second argument busy-waits that many milliseconds in every scrub step: the red control
that shows the budget can fail.

Usage: python3 measure.py <repo root> [slow_ms]
"""
from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
TEMPLATE_FILES = ["index.html", "main.tsx", "vite.config.mjs", "drive_chrome.mjs"]
PREFIX = "f024-r5-perf-"

PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
PRIMARY_NODE_MODULES = PRIMARY_UI / "node_modules"
PRIMARY_VITE_BIN = PRIMARY_NODE_MODULES / ".bin" / "vite"
CHROME_BIN = "/usr/bin/google-chrome"

CDP_PORT = 9373
SERVER_PORT = 9003


def _work_dir(repo_root: Path) -> Path:
    return repo_root / ".remedy-wt" / "f024-perf-run"


def fresh_work_dir(repo_root: Path) -> Path:
    work_dir = _work_dir(repo_root)
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True)
    for name in TEMPLATE_FILES:
        source = TOOL_DIR / name if (TOOL_DIR / name).is_file() else TOOL_DIR / (PREFIX + name)
        shutil.copyfile(source, work_dir / name)
    os.symlink(PRIMARY_NODE_MODULES, work_dir / "node_modules", target_is_directory=True)
    return work_dir


def run_build(work_dir: Path) -> None:
    print("+ vite build", flush=True)
    proc = subprocess.run(
        [str(PRIMARY_VITE_BIN), "build", "--config", str(work_dir / "vite.config.mjs")],
        cwd=str(work_dir), capture_output=True, text=True, timeout=120,
    )
    print(proc.stdout)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(f"vite build failed: exit {proc.returncode}")


def start_server(work_dir: Path) -> tuple[subprocess.Popen, object]:
    log = open(work_dir / "server.log", "w")
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(SERVER_PORT),
         "--bind", "127.0.0.1", "--directory", str(work_dir / "dist")],
        stdout=log, stderr=subprocess.STDOUT,
    )
    time.sleep(1.0)
    return proc, log


def start_chrome(work_dir: Path) -> tuple[subprocess.Popen, object]:
    profile = work_dir / "chrome-profile"
    profile.mkdir(parents=True, exist_ok=True)
    log = open(work_dir / "chrome.log", "w")
    proc = subprocess.Popen(
        [
            CHROME_BIN,
            "--headless=new",
            f"--remote-debugging-port={CDP_PORT}",
            "--remote-debugging-address=127.0.0.1",
            f"--user-data-dir={profile}",
            "--window-size=1280,800",
            "--no-first-run",
            "--no-default-browser-check",
            "about:blank",
        ],
        stdout=log, stderr=subprocess.STDOUT,
    )
    _wait_for_cdp(timeout=15.0)
    return proc, log


def _wait_for_cdp(timeout: float) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/version", timeout=1.0) as r:
                if r.status == 200:
                    return
        except OSError:
            pass
        time.sleep(0.3)
    raise SystemExit("chrome CDP endpoint never came up")


def run_drive(work_dir: Path, slow_ms: int) -> int:
    print(f"+ node drive_chrome.mjs {slow_ms}", flush=True)
    proc = subprocess.run(
        ["node", str(work_dir / "drive_chrome.mjs"), str(slow_ms)],
        cwd=str(work_dir), capture_output=True, text=True, timeout=420,
    )
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    return proc.returncode


def stop_by_pid(proc: subprocess.Popen, name: str) -> None:
    pid = proc.pid
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        print(f"{name} pid {pid} already gone")
        return
    for _ in range(20):
        if proc.poll() is not None:
            print(f"{name} pid {pid} stopped (SIGTERM)")
            return
        time.sleep(0.2)
    try:
        os.kill(pid, signal.SIGKILL)
        print(f"{name} pid {pid} stopped (SIGKILL, SIGTERM did not land in time)")
    except ProcessLookupError:
        print(f"{name} pid {pid} stopped (SIGTERM, race with the poll above)")


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("usage: measure.py <repo root> [slow_ms]", file=sys.stderr)
        return 2
    repo_root = Path(sys.argv[1]).resolve()
    slow_ms = int(sys.argv[2]) if len(sys.argv) == 3 else 0
    print(f"repo root: {repo_root}; slow_ms: {slow_ms}")

    work_dir = fresh_work_dir(repo_root)
    print(f"work dir: {work_dir}")

    server_proc = None
    chrome_proc = None
    server_log = None
    chrome_log = None
    drive_exit = 1
    try:
        run_build(work_dir)
        server_proc, server_log = start_server(work_dir)
        print(f"server pid: {server_proc.pid}")
        chrome_proc, chrome_log = start_chrome(work_dir)
        print(f"chrome pid: {chrome_proc.pid}")
        drive_exit = run_drive(work_dir, slow_ms)
    finally:
        if chrome_proc is not None:
            stop_by_pid(chrome_proc, "chrome")
        if server_proc is not None:
            stop_by_pid(server_proc, "server")
        if chrome_log is not None:
            chrome_log.close()
        if server_log is not None:
            server_log.close()
        shutil.rmtree(work_dir, ignore_errors=True)
        print(f"removed work dir: {work_dir}")

    print(f"drive_chrome.mjs exit code: {drive_exit}")
    return 0 if drive_exit == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
