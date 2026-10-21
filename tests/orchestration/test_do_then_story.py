"""amend1015 Phase 1, Gate 1: one fake `remedy do`, then its run story over the real public API.

Two orders run through the real CLI entry with the fake providers on tiny repositories that hold
only README.md: one ends done, and one whose builder is unavailable ends failed. The failure is
forced by a test-only `sitecustomize.py` on the child's `PYTHONPATH` that gives `FakeProvider` a
builder error by default (DECISION amend1015f D15). Then a real `remedy serve start --json` runs
on the same scratch data root and a client token of the project reads both stories; the done
job's apply through the API lands the change, and a second apply answers 409.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import threading
import time
from collections.abc import Iterator
from dataclasses import dataclass
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.orchestration.client_story_words import STORY_PHRASES, STORY_REASONS, story_problems

pytestmark = pytest.mark.integration

REPO = Path(__file__).resolve().parents[2]
ORDER = "pass die readme an"
GATE_SECONDS = 20.0
START_SECONDS = 15
STOP_SECONDS = 15
JOB_ID = re.compile(r"remedy job apply ([0-9a-f]{16}) --repo")
CLIENT_TOKEN = "story-gate-client-token-0123456789abcdef"
#: The test-only failure: every FakeProvider built in the child has an unavailable builder.
FAILING_SITECUSTOMIZE = '''\
import packages.orchestration.pingpong_provider_fake as _provider

_init = _provider.FakeProvider.__init__


def _failing_init(self, *args, **kwargs):
    kwargs.setdefault("builder_error", "provider_unavailable: forced by the story gate")
    _init(self, *args, **kwargs)


_provider.FakeProvider.__init__ = _failing_init
'''


def _env(data_dir: Path, ceiling: Path, *paths: Path) -> dict[str, str]:
    env = dict(os.environ)
    env.update({"REMEDY_DATA_DIR": str(data_dir), "GIT_CEILING_DIRECTORIES": str(ceiling),
                "PYTHONPATH": os.pathsep.join(str(p) for p in (*paths, REPO)),
                "REMEDY_SERVE_API_PORT": "0"})
    return env


def _cli(*args: str) -> list[str]:
    return [sys.executable, "-m", "apps.cli.grouped", *args]


def _tiny_repo(root: Path, name: str) -> Path:
    repo = root / name
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / "README.md").write_text("# tiny\n")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"],
                   cwd=repo, check=True)
    return repo


def _register(repo: Path, env: dict[str, str], elsewhere: Path) -> str:
    done = subprocess.run(_cli("project", "register", "--repo", str(repo), "--json"),
                          cwd=elsewhere, env=env, capture_output=True, text=True, timeout=30)
    assert done.returncode == 0, done.stdout + done.stderr
    return json.loads(done.stdout)["slug"]


def _do(repo: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        _cli("do", "run", ORDER, "--repo", str(repo), "--builder-provider", "fake",
             "--reviewer-provider", "fake", "--no-ui"),
        cwd=REPO, env=env, capture_output=True, text=True, timeout=GATE_SECONDS)


def _job_ids(data_dir: Path) -> set[str]:
    jobs = data_dir / "jobs"
    return {p.name for p in jobs.iterdir()} if jobs.is_dir() else set()


@dataclass
class Api:
    port: int

    def call(self, method: str, path: str, body: dict | None = None,
             token: str = CLIENT_TOKEN) -> tuple[int, dict]:
        connection = HTTPConnection("127.0.0.1", self.port, timeout=GATE_SECONDS)
        raw = json.dumps(body).encode("utf-8") if body is not None else None
        try:
            connection.request(method, path, body=raw, headers={"Authorization": f"Bearer {token}"})
            response = connection.getresponse()
            return response.status, json.loads(response.read())
        finally:
            connection.close()


@dataclass
class Gate:
    api: Api
    done_job: str
    done_repo: Path
    failed_job: str
    started: float


def _first_line(child: subprocess.Popen) -> str:
    box: list[str] = []
    reader = threading.Thread(target=lambda: box.append(child.stdout.readline()), daemon=True)
    reader.start()
    reader.join(START_SECONDS)
    if reader.is_alive():
        child.kill()
        pytest.fail(f"remedy serve printed no ready line within {START_SECONDS} seconds")
    return box[0] if box else ""


@pytest.fixture(scope="module")
def gate(tmp_path_factory) -> Iterator[Gate]:
    started = time.monotonic()
    root = tmp_path_factory.mktemp("sg")
    data_dir = root / "d"
    env = _env(data_dir, root)
    elsewhere = root / "elsewhere"
    elsewhere.mkdir()
    done_repo, failed_repo = _tiny_repo(root, "done"), _tiny_repo(root, "failed")
    slugs = [_register(done_repo, env, elsewhere), _register(failed_repo, env, elsewhere)]

    run = _do(done_repo, env)
    assert run.returncode == 0, run.stdout + run.stderr
    [done_job] = set(JOB_ID.findall(run.stdout))

    forcing = root / "forcing"
    forcing.mkdir()
    (forcing / "sitecustomize.py").write_text(FAILING_SITECUSTOMIZE)
    before = _job_ids(data_dir)
    failed = _do(failed_repo, _env(data_dir, root, forcing))
    assert failed.returncode == 1, failed.stdout + failed.stderr
    [failed_job] = _job_ids(data_dir) - before

    clients = data_dir / "api" / "clients.json"
    clients.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    clients.write_text(json.dumps({"clients": [{
        "name": "story-gate", "token": CLIENT_TOKEN, "projects": slugs,
        "max_total_tokens": None, "max_provider_calls": None, "may_apply": True}]}))
    os.chmod(clients, 0o600)

    folder = root / "serve"
    folder.mkdir()
    child = subprocess.Popen(_cli("serve", "start", "--json"), cwd=folder, env=env,
                             stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL, text=True)
    try:
        ready = json.loads(_first_line(child) or "null")
        assert ready and ready["ok"] is True, ready
        yield Gate(Api(ready["api_port"]), done_job, done_repo, failed_job, started)
    finally:
        subprocess.run(_cli("serve", "stop", "--json"), cwd=folder, env=env,
                       stdin=subprocess.DEVNULL, capture_output=True, timeout=STOP_SECONDS + 15)
        try:
            child.wait(timeout=STOP_SECONDS)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait(10)
        child.stdout.close()


def _story(gate: Gate, job_id: str) -> dict:
    status, story = gate.api.call("GET", f"/api/v1/jobs/{job_id}/story")
    assert status == 200, story
    assert story_problems(story) == [], story
    assert "$" not in json.dumps(story)
    for step in story["steps"]:
        if step["phrase"] is not None:
            assert step["phrase"]["key"] in STORY_PHRASES
    return story


def test_a_done_run_reads_done_and_its_apply_lands_once(gate: Gate) -> None:
    story = _story(gate, gate.done_job)
    assert _story(gate, gate.done_job) == story  # a read changes nothing, so it repeats

    assert story["state"] == "done"
    [building] = [step for step in story["steps"] if step["id"] == "building"]
    assert [task["status"] for task in building["tasks"]] == ["done"]
    assert story["next"] == {"action": "apply", "route": {
        "method": "POST", "path": f"/api/v1/jobs/{gate.done_job}/apply"}}
    assert story["numbers"]["rounds"] >= 1
    assert story["note_open"] is False

    route = story["next"]["route"]
    status, applied = gate.api.call(route["method"], route["path"], {})
    assert status == 200, applied
    assert (applied["ok"], applied["status"]) == (True, "applied"), applied
    changed = [change["path"] for change in story["changes"]]
    assert changed and all((gate.done_repo / path).is_file() for path in changed)
    status, again = gate.api.call(route["method"], route["path"], {})
    assert status == 409, again
    assert (again["ok"], again["error"]) == (False, "job_already_applied"), again

    after = _story(gate, gate.done_job)
    assert after["state"] == "done_applied"
    assert after["next"] == {"action": "none", "route": None}
    assert time.monotonic() - gate.started < GATE_SECONDS


def test_a_failed_run_reads_failed_and_offers_no_retry(gate: Gate) -> None:
    """amend1015c D3 (R-1331): a run of the failed job through its run route, with a provider
    that works, re-attempts nothing and the job reads failed again, so the story offers none."""
    story = _story(gate, gate.failed_job)

    assert story["state"] == "failed"
    reason = story["state_detail"]["reason"]
    assert reason["key"] in STORY_REASONS
    assert reason == {"key": "provider_unavailable", "args": {"provider": "fake"}}
    assert story["next"] == {"action": "none", "route": None}
    assert story["changes"] == []

    path = f"/api/v1/jobs/{gate.failed_job}/run"
    status, record = gate.api.call("POST", path, {"builder_provider": "fake",
                                                  "reviewer_provider": "fake"})
    assert status == 202, record
    deadline = time.monotonic() + GATE_SECONDS
    while record.get("state") == "running" and time.monotonic() < deadline:
        time.sleep(0.2)
        status, record = gate.api.call("GET", path)
    assert record["state"] == "ended", record
    again = _story(gate, gate.failed_job)
    assert (again["state"], again["next"]["action"]) == ("failed", "none")
    assert time.monotonic() - gate.started < 2 * GATE_SECONDS


def test_an_unknown_token_may_not_read_a_story(gate: Gate) -> None:
    status, body = gate.api.call("GET", f"/api/v1/jobs/{gate.done_job}/story", token="wrong" * 8)
    assert status == 401, body
