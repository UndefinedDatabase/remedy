"""exec-1017c — `remedy job abandon` and `remedy client cancel-order`, run as a client runs them.

Every `remedy` call is a subprocess with its own `REMEDY_DATA_DIR`, as in
`tests/cli/test_client_order_cmd.py`; an order is started through `OrderLauncher` with a stand-in
child, so the order's process state (running, ended) is real and nothing calls a model.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from packages.orchestration.serve_paths import serve_paths
from packages.orchestration.serve_runs import OrderLauncher

REPO_ROOT = Path(__file__).resolve().parents[2]

_JOB = "# Job: Cancel CLI\n\n## Task 1\nAdd a helper.\n\nAcceptance:\n- it exists\n"

#: A stand-in for `remedy do run` that waits for a release file, so the order reads `running`.
_WAITING_ORDER_CHILD = """\
import json, sys, time
from pathlib import Path
release = Path(sys.argv[3])
print(json.dumps({"ok": True}))
sys.stdout.flush()
deadline = time.monotonic() + 60
while not release.exists() and time.monotonic() < deadline:
    time.sleep(0.01)
"""


def _remedy(args: list[str], cwd: Path, data_root: Path) -> tuple[int, dict]:
    env = {**os.environ, "PYTHONPATH": str(REPO_ROOT), "REMEDY_DATA_DIR": str(data_root)}
    result = subprocess.run([sys.executable, "-m", "apps.cli.main", *args, "--json"], cwd=str(cwd),
                            capture_output=True, text=True, env=env, timeout=60)
    return result.returncode, json.loads(result.stdout)


def _planned_job(tmp_path: Path, data_root: Path, monkeypatch) -> str:
    from packages.orchestration.pingpong_job import parse_job_file

    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
    repo = tmp_path / "repo"
    repo.mkdir()
    return parse_job_file(_JOB, str(repo)).job_id


def test_job_cancel_ends_a_job_that_never_ran_and_a_second_cancel_changes_nothing(tmp_path, monkeypatch):
    data_root = tmp_path / "data"
    job_id = _planned_job(tmp_path, data_root, monkeypatch)

    code, first = _remedy(["job", "abandon", job_id[:8], "--reason", "not wanted"], tmp_path, data_root)
    again_code, again = _remedy(["job", "abandon", job_id], tmp_path, data_root)
    stop_code, stop = _remedy(["job", "stop", job_id], tmp_path, data_root)

    assert code == 0, first
    assert (first["job_id"], first["job_status"], first["cancel_pending"]) == (job_id, "cancelled", False)
    assert first["cancel"]["reason"] == "not wanted" and first["cancel"]["source"] == "cli"
    assert again_code == 0 and again["already_cancelled"] is True
    # A cancelled job never runs again, so no stop is requested for it.
    assert (stop_code, stop["error"]) == (1, "job_not_stoppable")


def test_job_cancel_refuses_an_unknown_and_a_path_shaped_job(tmp_path):
    data_root = tmp_path / "data"
    assert _remedy(["job", "abandon", "ffffffffffffffff"], tmp_path, data_root)[1]["error"] == "job_not_found"
    code, body = _remedy(["job", "abandon", "../x"], tmp_path, data_root)
    assert (code, body["error"]) == (2, "invalid_job_id")


def test_cancel_order_of_a_running_order_reads_cancelling_until_its_process_ends(tmp_path):
    data_root = tmp_path / "data"
    release = tmp_path / "release"
    launcher = OrderLauncher(serve_paths(data_root), argv_prefix=[sys.executable, "-c", _WAITING_ORDER_CHILD])
    record = launcher.start("do a thing", [str(release)])
    try:
        code, answer = _remedy(["client", "cancel-order", record.order_id, "--reason", "wrong"],
                               tmp_path, data_root)
        assert code == 0, answer
        assert (answer["state"], answer["phase"], answer["already_cancelled"]) == (
            "running", "cancelling", False)
        _code, polled = _remedy(["client", "order", record.order_id], tmp_path, data_root)
        assert polled["phase"] == "cancelling" and polled["cancel"]["reason"] == "wrong"
    finally:
        release.touch()
        launcher.wait(record.order_id, timeout=30)

    _code, ended = _remedy(["client", "order", record.order_id], tmp_path, data_root)
    assert (ended["state"], ended["phase"]) == ("ended", "cancelled")
    code, again = _remedy(["client", "cancel-order", record.order_id], tmp_path, data_root)
    assert code == 0 and again["already_cancelled"] is True and again["cancel"]["reason"] == "wrong"


def test_cancel_order_of_an_unknown_order_is_order_not_found(tmp_path):
    code, body = _remedy(["client", "cancel-order", "0123456789abcdef"], tmp_path, tmp_path / "data")
    assert (code, body["error"]) == (3, "order_not_found")
