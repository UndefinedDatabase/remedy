"""S7b — F295's gate path and four of F304's five paths, driven through a real supervisor over
HTTP alone (DECISION F253 D19).

`tests/cli/test_machine_client_contract.py` (F295's gate test) and
`tests/cli/test_machine_client_paths.py` (F304's second gate test) drive a machine client's work
through the command line. Every operation they use now has a route of the public HTTP API, so this
file drives the same paths the way a client's own test would: each test starts `remedy serve start
--json` as a child process on a scratch data root, with `REMEDY_SERVE_API_PORT` set to `0`, reads
the port from the first line the child prints and the token from `serve/serve.token`, and stops it
with `remedy serve stop`. The repositories are registered with `remedy project register --repo`, as
an operator does before a client starts; everything after that goes to `127.0.0.1` at the port
with the token. Every order is sent with `no_llm` and both providers `fake`, and every run names
both providers `fake`, so no model is called.

The four paths of F304 driven here are the apply with its history and a push, the order of two
jobs, the order naming its project, and the decline. The fifth, one order file started twice, is
absent on purpose: a client sends an order's text, not a file, and two orders sent over HTTP never
share a file, so `order_already_running` has no HTTP form (R-1207, DECISION F253 D19 (4)).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from http.client import HTTPConnection
from pathlib import Path
from typing import Any
from urllib.parse import quote

import pytest

from tests.cli.test_machine_client_contract import (
    _GIT_IDENTITY,
    LATER_DEADLINE,
    PAST_DEADLINE,
    _digest_job,
    _scratch_repo,
)
from tests.cli.test_machine_client_paths import _bare_upstream, _git

REPO_ROOT = Path(__file__).resolve().parents[2]

#: How long the child may take to print its ready line, and to end after `remedy serve stop`.
START_SECONDS = 30
STOP_SECONDS = 30
#: How long a poll of an order or of the digest waits for what it expects.
POLL_SECONDS = 180

#: What every order carries: no model, the fake builder and the fake reviewer.
ORDER_FLAGS = {"no_llm": True, "builder_provider": "fake", "reviewer_provider": "fake"}
#: What every run carries.
RUN_BODY = {"builder_provider": "fake", "reviewer_provider": "fake"}


def _environment(data_root: Path, **more: str) -> dict[str, str]:
    """The environment a client's child process runs in, read when it is needed.

    `PYTHONPATH` names this checkout, because the children run from folders of their own and
    `python -m apps.cli.main` must run this checkout's code wherever it is started.
    """
    code_path = os.pathsep.join(
        part for part in (str(REPO_ROOT), os.environ.get("PYTHONPATH", "")) if part)
    return {**os.environ, **_GIT_IDENTITY, "REMEDY_DATA_DIR": str(data_root),
            "PYTHONPATH": code_path, **more}


def _remedy_command(*args: str) -> list[str]:
    return [sys.executable, "-m", "apps.cli.main", *args]


def _first_line(child: subprocess.Popen) -> str:
    """The first line the child prints, read within START_SECONDS; the child is killed if none."""
    box: list[str] = []
    reader = threading.Thread(target=lambda: box.append(child.stdout.readline()), daemon=True)
    reader.start()
    reader.join(START_SECONDS)
    if reader.is_alive():
        child.kill()
        reader.join(10)
        pytest.fail(f"the supervisor printed no ready line within {START_SECONDS} seconds")
    return box[0] if box else ""


def _poll(what: str, read, done, seconds: float = POLL_SECONDS) -> Any:
    """READ until DONE accepts what it returns, and return that; fail after SECONDS."""
    deadline = time.monotonic() + seconds
    reading = None
    while time.monotonic() < deadline:
        reading = read()
        if done(reading):
            return reading
        time.sleep(0.2)
    pytest.fail(f"{what} did not happen within {seconds:g} seconds; last reading: {reading}")


@dataclass
class Supervisor:
    """A running `remedy serve start` and what a client of its port needs."""

    port: int
    token: str
    env: dict[str, str]
    folder: Path

    def request(self, method: str, path: str, body: dict | None = None) -> tuple[int, dict]:
        connection = HTTPConnection("127.0.0.1", self.port, timeout=POLL_SECONDS)
        headers = {"Authorization": f"Bearer {self.token}"}
        raw = json.dumps(body).encode("utf-8") if body is not None else None
        try:
            connection.request(method, path, body=raw, headers=headers)
            response = connection.getresponse()
            return response.status, json.loads(response.read())
        finally:
            connection.close()

    def get(self, path: str) -> tuple[int, dict]:
        return self.request("GET", path)

    def post(self, path: str, body: dict) -> tuple[int, dict]:
        return self.request("POST", path, body)

    def digest(self) -> dict:
        status, digest = self.get("/api/v1/digest")
        assert status == 200, digest
        return digest

    def register(self, repo: Path) -> tuple[dict, Path]:
        """Register REPO as a project from a folder that is no repository; the answer, the folder."""
        elsewhere = self.folder / "elsewhere"
        elsewhere.mkdir()
        done = subprocess.run(
            _remedy_command("project", "register", "--repo", str(repo), "--json"),
            cwd=str(elsewhere), env=self.env, stdin=subprocess.DEVNULL, capture_output=True,
            text=True, timeout=60)
        assert done.returncode == 0, done.stdout + done.stderr
        return json.loads(done.stdout), elsewhere

    def send_order(self, slug: str, text: str = "Add a line saying hello to README.md",
                   **more: Any) -> dict:
        """Send an order of project SLUG with a cost cap; the 202 answer's record."""
        order = f"---\nproject: {slug}\nmax-cost-usd: 1\n---\n{text}\n"
        status, created = self.post("/api/v1/orders", {"order": order, **ORDER_FLAGS, **more})
        assert status == 202, created
        assert created["state"] == "running"
        return created

    def ended_order(self, created: dict) -> dict:
        """Poll the order of the 202 answer CREATED until it is no longer running."""
        def read() -> dict:
            status, polled = self.get(f"/api/v1/orders/{created['order_id']}")
            assert status == 200, polled
            return polled

        polled = _poll("the order's end", read, lambda order: order["state"] != "running")
        assert polled["state"] == "ended", polled
        return polled

    def completed_job(self, job_id: str) -> dict:
        """Follow the digest until the job is completed and waits for its apply."""
        def read() -> dict:
            return _digest_job(self.digest(), job_id)

        return _poll(f"job {job_id} to complete", read,
                     lambda job: job["state"] == "completed" and job["waits_for_apply"] is True)

    def start_run(self, job_id: str) -> dict:
        status, record = self.post(f"/api/v1/jobs/{job_id}/run", RUN_BODY)
        assert status == 202, record
        assert record["job_id"] == job_id
        return record

    def apply(self, job_id: str, **flags: Any) -> dict:
        status, applied = self.post(f"/api/v1/jobs/{job_id}/apply", flags)
        assert status == 200, applied
        assert (applied["ok"], applied["status"]) == (True, "applied"), applied
        return applied


@pytest.fixture
def supervisor(tmp_path_factory, tmp_path):
    """`remedy serve start --json` running as a child process on a scratch data root, stopped with
    `remedy serve stop` when the test ends, green or red, and killed only if it outlives that."""
    data_root = tmp_path_factory.mktemp("gp")
    env = _environment(data_root, REMEDY_SERVE_API_PORT="0")
    folder = tmp_path / "supervisor-folder"
    folder.mkdir()
    errors = (folder / "serve.err").open("w", encoding="utf-8")
    child = subprocess.Popen(
        _remedy_command("serve", "start", "--json"), cwd=str(folder), env=env,
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=errors, text=True)
    try:
        ready = json.loads(_first_line(child) or "null")
        assert ready and ready["ok"] is True, (ready, (folder / "serve.err").read_text())
        token = (data_root / "serve" / "serve.token").read_text(encoding="utf-8").strip()
        yield Supervisor(port=ready["api_port"], token=token, env=env, folder=folder)
    finally:
        try:
            subprocess.run(_remedy_command("serve", "stop", "--json"), cwd=str(folder), env=env,
                           stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=STOP_SECONDS + 30)
        finally:
            try:
                child.wait(timeout=STOP_SECONDS)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait(10)
            child.stdout.close()
            errors.close()


def _repository(tmp_path: Path) -> Path:
    """A scratch repository with one passing test, as F304's `_client` makes one: the planner's
    blocking criterion runs pytest over `tests`, so a repository without a test fails it."""
    repo = _scratch_repo(tmp_path)
    (repo / "tests").mkdir()
    (repo / "tests" / "test_readme.py").write_text(
        "from pathlib import Path\n\n\ndef test_the_readme_exists():\n"
        "    assert Path('README.md').is_file()\n", encoding="utf-8")
    _git(repo, "add", "tests")
    _git(repo, "commit", "-q", "-m", "Add a test")
    return repo


def test_f295s_gate_path_runs_from_the_order_to_the_proof_over_http_alone(supervisor, tmp_path):
    repo = _repository(tmp_path)
    registered, _elsewhere = supervisor.register(repo)

    # 1. Propose: the deadline has passed, so the budget stops the run before any task runs.
    created = supervisor.send_order(registered["slug"], deadline=PAST_DEADLINE)
    ended = supervisor.ended_order(created)
    assert ended["exit_code"] == 1, ended
    done = ended["answer"]
    assert len(done["job_ids"]) == 1
    [job_id] = done["job_ids"]

    # 2. Read: the digest names the mission, the job stopped, the budget and the remainder.
    digest = supervisor.digest()
    assert digest["version"] == 1
    missions = [m for project in digest["projects"] for m in project["missions"]
                if m["mission_id"] == done["mission_id"]]
    assert len(missions) == 1
    assert missions[0]["job_ids"] == [job_id]
    job = _digest_job(digest, job_id)
    assert job["mission_id"] == done["mission_id"]
    assert job["state"] == "stopped"
    assert set(job["cost"]) == {"basis", "value_usd"}
    assert Path(job["evidence"]["run_manifest_path"]).is_file()
    budget = [d for d in digest["decisions"]
              if d["job_id"] == job_id and d["type"] == "token_budget"]
    assert len(budget) == 1
    assert budget[0]["options"] == ["extend", "abandon"]
    remainder = [d for d in digest["decisions"]
                 if d["job_id"] == job_id and d["type"] == "task_decision"]
    assert len(remainder) == 1
    assert job_id not in digest["awaiting_apply"]

    # 3. Answer: the budget decision, extended past the deadline that stopped it.
    status, answered = supervisor.post(
        f"/api/v1/jobs/{job_id}/decisions/{quote(budget[0]['decision_id'], safe='')}",
        {"reason": "extend", "answer": [f"deadline={LATER_DEADLINE}"]})
    assert status == 200, answered
    assert answered["outcome"] == "extended"
    assert answered["closed_decisions"] == [remainder[0]["decision_id"]]
    assert answered["budgets"]["max_cost_usd"] == 1.0

    # 4. Run: the answered job's run is started, and the digest is followed to its end.
    supervisor.start_run(job_id)
    supervisor.completed_job(job_id)
    digest = supervisor.digest()
    assert job_id in digest["awaiting_apply"]
    assert not [d for d in digest["decisions"] if d["job_id"] == job_id]

    # 5. Approve and apply: the reviewed result lands in the repository.
    applied = supervisor.apply(job_id)
    assert applied["files_applied"]
    for path in applied["files_applied"]:
        assert (repo / path).is_file(), path

    # 6. The proof names the apply that was approved, and calls nothing verified.
    status, proof = supervisor.get(f"/api/v1/jobs/{job_id}/proof")
    assert status == 200, proof
    assert [record["job_apply_id"] for record in proof["job_applies"]] == [applied["job_apply_id"]]
    assert proof["job_applies"][0]["status"] == "applied"
    assert proof["job_applies"][0]["files_applied"] == applied["files_applied"]
    assert proof["overall_status"] != "verified"

    # 7. The digest no longer lists the job as waiting for its apply.
    digest = supervisor.digest()
    assert _digest_job(digest, job_id)["waits_for_apply"] is False
    assert job_id not in digest["awaiting_apply"]


def test_a_result_is_applied_with_its_history_and_pushed_to_the_upstream_over_http(
        supervisor, tmp_path):
    repo = _repository(tmp_path)
    upstream = _bare_upstream(repo, tmp_path)
    branch = _git(repo, "symbolic-ref", "--short", "HEAD")
    registered, _elsewhere = supervisor.register(repo)

    ended = supervisor.ended_order(supervisor.send_order(registered["slug"]))
    assert ended["exit_code"] == 0, ended
    [job_id] = ended["answer"]["job_ids"]

    applied = supervisor.apply(job_id, commit_with_history=True, push=True)

    head = _git(repo, "rev-parse", "HEAD")
    assert applied["commit_sha"] == applied["merge_commit"] == head
    assert applied["target_branch"] == branch
    assert (applied["pushed"], applied["push_remote"], applied["push_ref"]) == (
        True, "origin", f"refs/heads/{branch}")
    assert _git(upstream, "rev-parse", f"refs/heads/{branch}") == head
    assert _digest_job(supervisor.digest(), job_id)["waits_for_apply"] is False


def test_an_order_of_two_jobs_is_driven_to_its_end_from_the_answers_alone_over_http(
        supervisor, tmp_path):
    repo = _repository(tmp_path)
    registered, _elsewhere = supervisor.register(repo)

    ended = supervisor.ended_order(supervisor.send_order(registered["slug"], force_mission=True))
    assert ended["exit_code"] == 0, ended
    first, second = ended["answer"]["job_ids"]
    assert ended["answer"]["waiting_job_ids"] == [second]

    # The first job ran. Each later job runs on what the one before it committed, so the client
    # applies and commits the first, runs the second, and applies and commits that one too.
    applied_first = supervisor.apply(first, commit_auto=True)
    supervisor.start_run(second)
    supervisor.completed_job(second)
    applied_second = supervisor.apply(second, commit_auto=True)

    assert _git(repo, "rev-parse", "HEAD") == applied_second["commit_sha"]
    assert _git(repo, "rev-parse", "HEAD~1") == applied_first["commit_sha"]
    digest = supervisor.digest()
    assert [_digest_job(digest, job_id)["state"] for job_id in (first, second)] == [
        "completed", "completed"]
    assert digest["awaiting_apply"] == []


def test_an_order_naming_its_project_is_applied_in_that_projects_repository_over_http(
        supervisor, tmp_path):
    repo = _repository(tmp_path)
    registered, elsewhere = supervisor.register(repo)

    ended = supervisor.ended_order(supervisor.send_order(registered["slug"]))
    assert ended["exit_code"] == 0, ended
    [job_id] = ended["answer"]["job_ids"]
    assert _digest_job(supervisor.digest(), job_id)["project_id"] == registered["project_id"]

    supervisor.apply(job_id)

    assert (repo / "docs" / "README.md").is_file()
    assert list(elsewhere.iterdir()) == []


def test_a_completed_result_is_declined_over_http_and_waits_for_nothing(supervisor, tmp_path):
    repo = _repository(tmp_path)
    registered, _elsewhere = supervisor.register(repo)
    ended = supervisor.ended_order(supervisor.send_order(registered["slug"]))
    assert ended["exit_code"] == 0, ended
    [job_id] = ended["answer"]["job_ids"]
    assert supervisor.digest()["awaiting_apply"] == [job_id]

    status, declined = supervisor.post(f"/api/v1/jobs/{job_id}/decline", {"reason": "not wanted"})

    assert status == 200, declined
    assert (declined["ok"], declined["reason"]) == (True, "not wanted"), declined
    digest = supervisor.digest()
    job = _digest_job(digest, job_id)
    assert (job["state"], job["waits_for_apply"]) == ("completed", False)
    assert digest["awaiting_apply"] == []
    # Nothing was applied: the repository is as the client left it.
    assert not (repo / "docs" / "README.md").exists()
