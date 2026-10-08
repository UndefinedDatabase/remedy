"""F253 S5a — `remedy client order <order> [--json]` reads an order the supervisor started as a
record of its own (DECISION F253 D13).

Every `remedy` call here is a subprocess (the way `tests/cli/test_client_changes_cmd.py` drives
`client changes`), so its `cwd` and its `REMEDY_DATA_DIR` are exactly a real client's. The first
three tests start a stand-in "order" directly through `OrderLauncher`, a small script that prints
one envelope and exits, to exercise the command's answer and its refusal without a real `do run`.
The last test is the one real run the round's block asks for: `OrderLauncher` with its default
prefix starts a real order, through the fake builder and reviewer, against a project `remedy
init` registers — the same registration `tests/cli/test_do_project_repo.py` drives — and the
round's own order (`tests/cli/test_machine_client_contract.py`'s shape) carries a past deadline,
so `remedy do` stops it before any task runs.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.serve_paths import serve_paths
from packages.orchestration.serve_runs import OrderLauncher

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Git identity for the scratch repository the real-run test commits into.
_GIT_IDENTITY = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                 "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
#: A deadline already in the past: the real run's budget stops it before any task runs.
_PAST_DEADLINE = "2000-01-01T00:00:00+00:00"

#: A stand-in for `remedy do run`: prints one envelope naming a mission, then exits 0 at once —
#: enough to drive `client order` against an ENDED order without a real `do run`.
_ENDED_ORDER_CHILD = 'import json; print(json.dumps({"ok": True, "mission_id": "m-stand-in"}))'


def _subprocess_env(data_root: Path) -> dict[str, str]:
    """A fresh copy of `os.environ`, read at call time (R-0803's lesson): never a module-level
    snapshot, which would freeze before a test's own data root is known."""
    return {**os.environ, "PYTHONPATH": str(REPO_ROOT), "REMEDY_DATA_DIR": str(data_root)}


def _remedy(args: list[str], cwd: Path, data_root: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", *args],
        cwd=str(cwd), capture_output=True, text=True, env=_subprocess_env(data_root), timeout=60)
    return result.returncode, result.stdout


def _start_ended_order(data_root: Path) -> str:
    """Start the stand-in order and wait for its end; its order id."""
    launcher = OrderLauncher(serve_paths(data_root),
                             argv_prefix=[sys.executable, "-c", _ENDED_ORDER_CHILD])
    record = launcher.start("do a thing", [])
    launcher.wait(record.order_id, timeout=30)
    return record.order_id


def test_the_answer_names_an_ended_orders_keys_and_values(tmp_path):
    data_root = tmp_path / "data"
    order_id = _start_ended_order(data_root)

    code, out = _remedy(["client", "order", order_id, "--json"], tmp_path, data_root)

    assert code == 0, out
    body = json.loads(out)
    assert body["ok"] is True
    assert body["order_id"] == order_id
    assert body["state"] == "ended"
    assert body["exit_code"] == 0
    assert body["started_at"] and body["ended_at"]
    assert Path(body["order_file"]).name == "order.md"
    assert body["answer"] == {"ok": True, "mission_id": "m-stand-in"}


@pytest.mark.parametrize("bad_id", ["0123456789abcdef", "../x"])
def test_an_unknown_or_path_shaped_id_is_order_not_found(tmp_path, bad_id):
    data_root = tmp_path / "data"

    code, out = _remedy(["client", "order", bad_id, "--json"], tmp_path, data_root)

    assert code == 3, out
    body = json.loads(out)
    assert (body["ok"], body["error"]) == (False, "order_not_found")
    assert bad_id in body["message"]


def test_the_summary_without_json_names_the_state(tmp_path):
    data_root = tmp_path / "data"
    order_id = _start_ended_order(data_root)

    code, out = _remedy(["client", "order", order_id], tmp_path, data_root)

    assert code == 0, out
    assert f"Order {order_id}: ended" in out


def _git_repo(path: Path) -> Path:
    path.mkdir()
    env = {**os.environ, **_GIT_IDENTITY}
    subprocess.run(["git", "init", "-q", str(path)], check=True, env=env)
    (path / "README.md").write_text("# Scratch\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(path), "add", "README.md"], check=True, env=env)
    subprocess.run(["git", "-C", str(path), "commit", "-q", "-m", "init"], check=True, env=env)
    return path.resolve()


def test_a_real_order_reaches_its_mission_and_status_names_it(tmp_path):
    data_root = tmp_path / "data"
    repo = _git_repo(tmp_path / "repo")

    # Register the project (the registration `tests/cli/test_do_project_repo.py` drives).
    code, init_out = _remedy(["init", "--json"], repo, data_root)
    assert code == 0, init_out
    slug = json.loads(init_out)["summary"]["slug"]

    order_text = (f"---\nproject: {slug}\nmax-cost-usd: 1\n---\n"
                 "Add a line saying hello to README.md\n")
    options = ["--no-llm", "--builder-provider=fake", "--reviewer-provider=fake",
              f"--deadline={_PAST_DEADLINE}"]
    launcher = OrderLauncher(serve_paths(data_root))                 # the default prefix
    record = launcher.start(order_text, options)
    exit_code = launcher.wait(record.order_id, timeout=120)
    assert exit_code == 1, "a past deadline stops the run before any task runs"

    code, order_out = _remedy(
        ["client", "order", record.order_id, "--json"], tmp_path, data_root)
    assert code == 0, order_out
    order_body = json.loads(order_out)
    assert order_body["state"] == "ended"
    # The past deadline stops the run before any task runs, so `remedy do`'s own envelope is a
    # refusal (`ok: false`) — the mission and its jobs already exist, which is what this test
    # (and `remedy status --json`, below) holds to the order's own file.
    mission_id = order_body["answer"]["mission_id"]
    assert order_body["answer"]["job_ids"]

    code, status_out = _remedy(["status", "--json"], tmp_path, data_root)
    assert code == 0, status_out
    digest = json.loads(status_out)["client"]
    missions = [m for project in digest["projects"] for m in project["missions"]
               if m["mission_id"] == mission_id]
    assert len(missions) == 1
    assert missions[0]["order_source_path"] == order_body["order_file"]
