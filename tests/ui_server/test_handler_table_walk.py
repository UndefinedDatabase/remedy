"""R-0804: every cockpit read endpoint answers 200 for a job the real job path created.

The operator's tests.md run of 2026-09-05 crashed the brain endpoint for a ping-pong
job with an ``AttributeError`` (no attribute ``inputs``) raised through the cockpit's
task adapter. That adapter is deleted; this walk keeps the property. The job is made by
``parse_job_file`` + ``run_job`` with the fake provider named, so each task gets its
own ``FakeProvider`` and runs two rounds. The endpoint set is read from
``ui_server.py`` itself, so an endpoint added later is walked without editing here.
"""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

import pytest

from packages.orchestration.ui_server import _RemedyHandler

_UI_SERVER = (Path(__file__).resolve().parents[2]
              / "packages" / "orchestration" / "ui_server.py")

_TWO_TASK_JOB = """# Job: two tasks for the handler walk

## Task 1
Update docs/README.md.

Acceptance:
- done

## Task 2
Update docs/README.md again.

Acceptance:
- done
"""


def _do_get(tree: ast.Module) -> ast.FunctionDef:
    [cls] = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "_RemedyHandler"]
    [fn] = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "do_GET"]
    return fn


def _job_endpoints() -> set[str]:
    """The ``/api/jobs/<id>/<endpoint>`` names do_GET routes, read from the source.

    Two sources, both inside do_GET: the string keys of the ``handlers = {...}``
    dict literal, and the strings compared against the name ``endpoint``
    (``events-since`` is routed by its own ``if endpoint == "events-since"``
    branch because it reads a ``cursor`` query parameter the dict's one-argument
    handlers do not take).
    """
    fn = _do_get(ast.parse(_UI_SERVER.read_text(encoding="utf-8")))
    names: set[str] = set()
    for node in ast.walk(fn):
        if (isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict)
                and [getattr(t, "id", None) for t in node.targets] == ["handlers"]):
            names |= {k.value for k in node.value.keys
                      if isinstance(k, ast.Constant) and isinstance(k.value, str)}
        if (isinstance(node, ast.Compare) and isinstance(node.left, ast.Name)
                and node.left.id == "endpoint"):
            names |= {c.value for c in node.comparators
                      if isinstance(c, ast.Constant) and isinstance(c.value, str)}
    return names


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True, check=True)


@pytest.fixture
def fake_two_task_job(tmp_path, monkeypatch) -> str:
    """A two-task job run to completion by ``run_job`` with the fake provider."""
    from packages.orchestration.pingpong_job import parse_job_file, run_job
    from packages.orchestration.pingpong_loop import load_run

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.chdir(tmp_path)
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@e.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "config", "commit.gpgsign", "false")
    (repo / "README.md").write_text("# Demo\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "init")

    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    result = run_job(job.job_id, builder_name="fake", reviewer_name="fake")

    assert len(result.tasks) == 2
    assert [len(load_run(t.run_id)["rounds"]) for t in result.tasks] == [2, 2]
    return str(result.job_id)


def _get(job_id: str, endpoint: str) -> int:
    handler = _RemedyHandler.__new__(_RemedyHandler)
    handler.server_token = "tok"
    handler.target_job_id = job_id
    handler.app_html = ""
    captured: dict = {}
    handler._send_json = lambda code, data: captured.update(code=code)  # type: ignore[method-assign]
    handler.path = f"/api/jobs/{job_id}/{endpoint}?token=tok"
    handler.do_GET()
    return captured["code"]


def test_the_endpoint_set_is_read_from_the_source():
    endpoints = _job_endpoints()
    assert endpoints, "no endpoint was derived from do_GET"
    assert {"brain", "brain-view-model", "events-since"} <= endpoints


def test_every_cockpit_read_endpoint_answers_200_for_a_fake_job(fake_two_task_job):
    failures: dict[str, str] = {}
    for endpoint in sorted(_job_endpoints()):
        try:
            code = _get(fake_two_task_job, endpoint)
        except Exception as exc:  # the defect raised out of do_GET
            failures[endpoint] = f"{type(exc).__name__}: {exc}"
            continue
        if code != 200:
            failures[endpoint] = f"HTTP {code}"
    assert not failures, f"cockpit endpoints failed for a fake ping-pong job: {failures}"
