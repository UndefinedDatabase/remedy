#!/usr/bin/env python3
"""F042 R6's live render run (evidence, not product): the multi-project cockpit in a real browser
against the REAL UI server and REAL jobs (DECISION F042 D6).

One entry, `<prefix>measure.py <repo root>`, where <prefix> is whatever this file's name carries
before `measure.py`. It makes a fresh work dir `<repo root>/.remedy-wt/f042-r6-live-run` with a
data root of its own; registers two projects, `alpha` and `beta`, by `remedy init` in two git
folders; plans two jobs in alpha and one in beta with `remedy do --no-llm --plan-only`, and runs
alpha's first to its end on the fake providers (no network, no model); builds the cockpit with the
primary checkout's `vite` binary inside `<repo root>/apps/ui`, so the page is this tree's own
code; starts `start_ui_server` in a child process on 127.0.0.1 port 9010 with
`REMEDY_UI_NO_AUTO_BUILD=1`; launches `/usr/bin/google-chrome --headless=new` at 1440 by 900 with
a private profile and CDP on port 9372; runs its sibling `drive.mjs` with the run's facts in a
JSON file; stops Chrome and the server by their OWN recorded pids (never `pkill -f`), removes the
work dir, and exits 0 only when drive.mjs reported every check passing.

Usage: python3 <prefix>measure.py <repo root>
"""
from __future__ import annotations

import json
import os
import secrets
import shutil
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
PREFIX = Path(__file__).name[: -len("measure.py")]
PRIMARY_VITE = Path("/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vite")
CHROME_BIN = "/usr/bin/google-chrome"
CDP_PORT = 9372
SERVER_PORT = 9010
ORDER = "fix src/main.py and update README.md"
SERVE = ("import sys\n"
         "from packages.orchestration.ui_server import start_ui_server\n"
         "start_ui_server(sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]), token=sys.argv[3],\n"
         "                open_browser=False, info_file=sys.argv[4])\n")


def git_folder(path: Path) -> Path:
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(path), "commit", "--allow-empty", "-m", "init", "-q"], check=True,
                   capture_output=True, env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                                             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})
    return path


def cli(args: list[str], cwd: Path, env: dict[str, str]) -> str:
    proc = subprocess.run([sys.executable, "-m", "apps.cli.main", *args], cwd=str(cwd), env=env,
                          stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=180)
    if proc.returncode != 0:
        raise SystemExit(f"remedy {' '.join(args)} failed: exit {proc.returncode}\n{proc.stderr[-2000:]}")
    return proc.stdout


def wait_for(path: Path, timeout: float) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.is_file():
            try:
                return json.loads(path.read_text())
            except json.JSONDecodeError:
                pass
        time.sleep(0.3)
    raise SystemExit(f"{path} never appeared")


def wait_for_cdp(timeout: float) -> None:
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


def stop_by_pid(proc: subprocess.Popen, name: str) -> None:
    try:
        os.kill(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        print(f"{name} pid {proc.pid} already gone")
        return
    for _ in range(25):
        if proc.poll() is not None:
            print(f"{name} pid {proc.pid} stopped (SIGTERM)")
            return
        time.sleep(0.2)
    try:
        os.kill(proc.pid, signal.SIGKILL)
        print(f"{name} pid {proc.pid} stopped (SIGKILL)")
    except ProcessLookupError:
        print(f"{name} pid {proc.pid} stopped (SIGTERM, race)")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: measure.py <repo root>", file=sys.stderr)
        return 2
    repo_root = Path(sys.argv[1]).resolve()
    work = repo_root / ".remedy-wt" / "f042-r6-live-run"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    shutil.copy(TOOL_DIR / f"{PREFIX}drive.mjs", work / "drive.mjs")
    env = {**os.environ, "PYTHONPATH": str(repo_root), "REMEDY_DATA_DIR": str(work / "data"),
           "REMEDY_UI_NO_AUTO_BUILD": "1"}
    env.pop("REMEDY_PROJECT", None)
    server = chrome = None
    logs = []
    drive_exit = 1
    try:
        jobs: dict[str, list[str]] = {}
        for slug, count in (("alpha", 2), ("beta", 1)):
            folder = git_folder(work / slug)
            cli(["init"], folder, env)
            jobs[slug] = [json.loads(cli(["do", ORDER, "--no-llm", "--plan-only", "--json"], folder, env))["job_ids"][0]
                          for _ in range(count)]
        cli(["job", "run", jobs["alpha"][0], "--builder-provider", "fake", "--reviewer-provider", "fake", "--json"],
            work / "alpha", env)
        print(f"jobs: {json.dumps(jobs)}")
        build = subprocess.run([str(PRIMARY_VITE), "build"], cwd=str(repo_root / "apps" / "ui"),
                               capture_output=True, text=True, timeout=240)
        print(f"vite build exit {build.returncode}")
        if build.returncode != 0:
            print(build.stdout[-2000:], build.stderr[-2000:])
            return 1
        token = secrets.token_urlsafe(16)
        info = work / "server_info.json"
        server_log = open(work / "server.log", "w")
        logs.append(server_log)
        server = subprocess.Popen([sys.executable, "-c", SERVE, jobs["alpha"][0], str(SERVER_PORT), token, str(info)],
                                  cwd=str(repo_root), env=env, stdout=server_log, stderr=subprocess.STDOUT)
        print(f"server pid: {server.pid}, port {wait_for(info, 60.0)['port']}")
        facts = work / "live.json"
        facts.write_text(json.dumps({"base": f"http://127.0.0.1:{SERVER_PORT}/", "token": token, "jobs": jobs}))
        profile = work / "chrome-profile"
        profile.mkdir()
        chrome_log = open(work / "chrome.log", "w")
        logs.append(chrome_log)
        chrome = subprocess.Popen([CHROME_BIN, "--headless=new", f"--remote-debugging-port={CDP_PORT}",
                                   "--remote-debugging-address=127.0.0.1", f"--user-data-dir={profile}",
                                   "--window-size=1440,900", "--no-first-run", "--no-default-browser-check",
                                   "about:blank"], stdout=chrome_log, stderr=subprocess.STDOUT)
        wait_for_cdp(20.0)
        print(f"chrome pid: {chrome.pid}")
        drive = subprocess.run(["node", str(work / "drive.mjs"), str(facts)], cwd=str(work), capture_output=True,
                               text=True, timeout=300)
        print(drive.stdout)
        if drive.stderr:
            print(drive.stderr, file=sys.stderr)
        drive_exit = drive.returncode
    finally:
        if chrome is not None:
            stop_by_pid(chrome, "chrome")
        if server is not None:
            stop_by_pid(server, "server")
        for log in logs:
            log.close()
        shutil.rmtree(work, ignore_errors=True)
        print(f"removed work dir: {work}")
    print(f"drive.mjs exit code: {drive_exit}")
    return 0 if drive_exit == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
