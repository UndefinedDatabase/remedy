"""F029 R4 S4 — DECISION F029 D4 (2): the write door's `job.rerun-subtree`,
modelled on the injection class of `test_command_dispatch.py`
(`TestInjectionDispatchEffects`, DECISION F028 D5): the shape checks that run
BEFORE the effect can refuse anything, the 409 `rerun_subtree_command`'s own
refusal gives, and the 200s `needs_confirmation` and `prepared` answer.
"""
from __future__ import annotations

import json
import re
import subprocess
import threading
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import JOB_COMPLETED, parse_job_file, run_job
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput
from tests.ui_server.server_start import wait_for_server_info

CSRF_HEADER = "X-Remedy-CSRF"

JOB_TEXT = """# One-task job

## Task 1 — create task1.txt

Create `task1.txt`.
"""


class _NamedFileBuilder:
    """Fake Builder: writes the file the composed prompt names. Mirrors
    `test_subtree_rerun_prepare.py`'s own copy exactly."""

    def __init__(self, cwd_holder: dict) -> None:
        self._cwd = cwd_holder
        self.calls = 0

    def build(self, prompt, **kw):
        self.calls += 1
        ws = Path(self._cwd["path"])
        name = re.search(r"task\d+\.txt", prompt).group(0)
        (ws / name).write_text(f"{name} attempt {self.calls}\n")
        return BuilderOutput(summary=f"wrote {name}", files_changed=[name], provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok", provider="fake")


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True, check=True)


def _start_ui_server_for_job(job_id: str, tmp_path: Path) -> tuple[int, str]:
    """Mirrors `test_command_dispatch.py`'s own copy exactly (finding R-0701)."""
    import secrets

    from packages.orchestration.ui_server import start_ui_server

    info_file = str(tmp_path / "server_info.json")
    token = secrets.token_urlsafe(16)

    def run():
        try:
            start_ui_server(job_id, host="127.0.0.1", port=0, token=token,
                            open_browser=False, info_file=info_file)
        except (SystemExit, KeyboardInterrupt):
            pass

    t = threading.Thread(target=run, daemon=True)
    t.start()
    return wait_for_server_info(info_file, t)["port"], token


@pytest.fixture
def repo(tmp_path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@e.com")
    _git(r, "config", "user.name", "T")
    _git(r, "config", "commit.gpgsign", "false")
    (r / "base.txt").write_text("base\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


class TestRerunSubtreeDoor:
    """What `job.rerun-subtree` answers through the write door (DECISION F029 D4)."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, repo, tmp_path, monkeypatch):
        from packages.orchestration import worktrees as W

        data_root = tmp_path / "remedy_data"
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
        job = parse_job_file(JOB_TEXT, str(repo))
        holder: dict = {}
        real_create = W.create

        def spy(job_id, r):
            h = real_create(job_id, r)
            holder["path"] = h.path
            return h

        monkeypatch.setattr(W, "create", spy)
        prov = _NamedFileBuilder(holder)
        self.job = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                           builder_name="fake", reviewer_name="fake", max_rounds=1)
        assert self.job.state == JOB_COMPLETED
        self.job_id = str(self.job.job_id)
        self.tmp_path = data_root
        self.control = data_root / "control"

    def _post(self, port, token, nonce, args):
        payload = {"command": "job.rerun-subtree", "client_nonce": nonce, "args": args}
        conn = HTTPConnection("127.0.0.1", port, timeout=10)
        try:
            conn.request("POST", f"/api/jobs/{self.job_id}/commands",
                         body=json.dumps(payload),
                         headers={"Authorization": f"Bearer {token}",
                                  CSRF_HEADER: token,
                                  "Content-Type": "application/json"})
            resp = conn.getresponse()
            return resp.status, json.loads(resp.read())
        finally:
            conn.close()

    def _record_bytes(self) -> bytes:
        from packages.orchestration.data_paths import job_record_path
        return job_record_path(self.job_id).read_bytes()

    def test_needs_confirmation_is_a_200_that_changes_nothing(self):
        before = self._record_bytes()
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-needs-confirmation",
                                  {"task_id": "T001"})

        assert status == 200, body
        assert body["command"] == "job.rerun-subtree"
        assert body["outcome"] == "needs_confirmation"
        assert self._record_bytes() == before

    def test_confirm_cost_prepares_and_answers_200(self):
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-prepared",
                                  {"task_id": "T001", "confirm_cost": True})

        assert status == 200, body
        assert body["outcome"] == "prepared"
        assert body["run_command"] == f"remedy job run {self.job_id}"
        assert self._record_bytes() != b""

    def test_a_refusal_is_a_409_naming_unknown_task(self):
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-refused",
                                  {"task_id": "no-such-task", "confirm_cost": True})

        assert status == 409, body
        assert body["error"].startswith("unknown_task:"), body

    def test_a_non_bool_confirm_cost_is_400_before_the_job_is_read(self):
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-bad-confirm-cost",
                                  {"task_id": "T001", "confirm_cost": "yes"})

        assert status == 400, body
        assert body["field"] == "confirm_cost", body

    def test_a_missing_task_id_is_400_before_the_job_is_read(self):
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = self._post(port, token, "nonce-no-task", {})

        assert status == 400, body
        assert body["field"] == "task_id", body
