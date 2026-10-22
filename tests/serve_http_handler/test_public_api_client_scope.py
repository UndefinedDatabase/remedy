"""A client token reads and acts only on the jobs of its own projects (amend1015c D2).

Operator order amend1015-final-closure, Phase A5/A6: a project-scoped client token must not read
or act on another project's jobs on any route that names one, nor see them in the digest or in
what changed. The story, the logs and the four writes were already held to a client's projects
(their tests are in `test_public_api.py`); this file holds the routes the check found open: the
proof, the run poll, the order poll, the digest and the changes, and the diff of DECISION
amend1015c D5.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from uuid import uuid4

from packages.orchestration import public_api

TOKEN = "client-scope-test-token-0123456789abcdef"


def _project(tmp_path: Path, name: str):
    from packages.orchestration.project_registry import register_project_repo

    repo = tmp_path / name
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    return register_project_repo(name, repo)


def _job(project_id: str, repo: Path, *, title: str = "scope-job") -> str:
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

    job = JobPlan(job_title=title, user_prompt="Scope prompt", tasks=[TaskEntry(title="t")],
                  repo_path=str(repo), project_id=project_id)
    save_job_plan(job)
    return str(job.job_id)


def _client(*projects: str):
    from packages.orchestration.api_clients import ApiClient

    return ApiClient(name="scoped-bot", token=TOKEN, projects=tuple(projects),
                     max_total_tokens=None, max_provider_calls=None, may_apply=True)


def _two_projects(tmp_path: Path):
    mine, theirs = _project(tmp_path, "scope-mine"), _project(tmp_path, "scope-theirs")
    own = _job(str(mine.id), tmp_path / "scope-mine", title="own-job")
    other = _job(str(theirs.id), tmp_path / "scope-theirs", title="other-job")
    return mine, theirs, own, other


def test_the_proof_run_poll_and_diff_routes_hold_a_client_to_its_projects(tmp_path):
    mine, _theirs, own, other = _two_projects(tmp_path)
    client = _client(mine.slug)
    for suffix in ("proof", "run", "diff"):
        status, body, _headers = public_api.answer_public_api_get(
            f"/api/v1/jobs/{other}/{suffix}", client=client)
        assert (status, body["error"]) == (403, "api_client_policy_refused"), suffix
        assert other in body["message"]
        status, body, _headers = public_api.answer_public_api_get(
            f"/api/v1/jobs/{own}/{suffix}", client=client)
        assert status != 403, (suffix, body)


def _order(order_id: str, project_slug: str) -> None:
    from packages.orchestration.serve_paths import serve_paths

    folder = serve_paths().orders_dir / order_id
    folder.mkdir(parents=True)
    order_file = folder / "order.md"
    order_file.write_text(f"---\nproject: {project_slug}\nmax-total-tokens: 1000\n---\nHello\n")
    (folder / "order.json").write_text(json.dumps({
        "order_id": order_id, "pid": 1, "started_at": "2026-01-01T00:00:00Z",
        "order_file": str(order_file), "out_log": str(folder / "out.log"),
        "err_log": str(folder / "err.log"), "exit_code": 0,
        "ended_at": "2026-01-01T00:00:05Z"}))


def test_the_order_poll_route_holds_a_client_to_its_projects(tmp_path):
    mine, theirs, _own, _other = _two_projects(tmp_path)
    _order("aaaa000000000001", mine.slug)
    _order("aaaa000000000002", theirs.slug)
    client = _client(str(mine.id))
    status, body, _headers = public_api.answer_public_api_get(
        "/api/v1/orders/aaaa000000000002", client=client)
    assert (status, body["error"]) == (403, "api_client_policy_refused")
    status, body, _headers = public_api.answer_public_api_get(
        "/api/v1/orders/aaaa000000000001", client=client)
    assert status == 200 and body["order_id"] == "aaaa000000000001"
    status, body, _headers = public_api.answer_public_api_get(
        "/api/v1/orders/aaaa000000000002")
    assert status == 200, body
    # An order no record names stays the route's own 404, for a client too.
    status, body, _headers = public_api.answer_public_api_get(
        "/api/v1/orders/aaaa000000000003", client=client)
    assert (status, body["error"]) == (404, "order_not_found")


def test_the_digest_lists_only_the_clients_projects_and_their_jobs(tmp_path):
    mine, theirs, own, other = _two_projects(tmp_path)
    status, body, _headers = public_api.answer_public_api_get(
        "/api/v1/digest", client=_client(mine.slug))
    assert status == 200, body
    assert [p["slug"] for p in body["projects"]] == [mine.slug]
    assert [j["job_id"] for j in body["jobs"]] == [own]
    assert other not in json.dumps(body) and str(theirs.id) not in json.dumps(body)
    # The server's own token still reads every project.
    status, body, _headers = public_api.answer_public_api_get("/api/v1/digest")
    assert {j["job_id"] for j in body["jobs"]} == {own, other}


def test_what_changed_lists_only_the_clients_jobs(tmp_path):
    mine, _theirs, own, other = _two_projects(tmp_path)
    query = "since=2000-01-01T00:00:00Z"
    status, body, _headers = public_api.answer_public_api_get(
        "/api/v1/changes", query, client=_client(mine.slug))
    assert status == 200, body
    assert [j["job_id"] for j in body["jobs"]] == [own]
    assert other not in json.dumps(body)
    status, body, _headers = public_api.answer_public_api_get("/api/v1/changes", query)
    assert {j["job_id"] for j in body["jobs"]} == {own, other}


def test_a_client_of_no_registered_project_sees_no_job(tmp_path):
    _mine, _theirs, _own, _other = _two_projects(tmp_path)
    client = _client(str(uuid4()))
    status, body, _headers = public_api.answer_public_api_get("/api/v1/digest", client=client)
    assert status == 200 and body["jobs"] == [] and body["projects"] == []


def test_the_now_route_lists_only_the_clients_projects_jobs(tmp_path):
    """F311 D6: `client.now` joined `_CLIENT_FILTERED_TWINS`, as the digest is filtered."""
    from packages.orchestration.pingpong_job import JOB_RUNNING, JobPlan, TaskEntry, save_job_plan

    mine, theirs, _own, _other = _two_projects(tmp_path)

    def _running(project_id: str, title: str) -> str:
        job = JobPlan(job_title=title, tasks=[TaskEntry(title="t")], state=JOB_RUNNING,
                     project_id=project_id)
        save_job_plan(job)
        return str(job.job_id)

    own = _running(str(mine.id), "own-running")
    other = _running(str(theirs.id), "other-running")

    status, body, _headers = public_api.answer_public_api_get(
        "/api/v1/now", client=_client(mine.slug))
    assert status == 200, body
    assert [j["job"] for j in body["jobs"]] == [own]
    assert other not in json.dumps(body)
    status, body, _headers = public_api.answer_public_api_get("/api/v1/now")
    assert {j["job"] for j in body["jobs"]} == {own, other}


def test_the_insight_route_holds_a_client_to_its_projects(tmp_path):
    """F311 D6: `client.insight` joined `_CLIENT_SCOPED_TWINS`."""
    mine, _theirs, own, other = _two_projects(tmp_path)
    status, body, _headers = public_api.answer_public_api_get(
        f"/api/v1/jobs/{other}/insight", client=_client(mine.slug))
    assert (status, body["error"]) == (403, "api_client_policy_refused")
    assert other in body["message"]
    status, body, _headers = public_api.answer_public_api_get(
        f"/api/v1/jobs/{own}/insight", client=_client(mine.slug))
    assert status != 403, body


def test_the_cancel_routes_hold_a_client_to_its_projects(tmp_path):
    """exec-1017c: a client cancels only its own projects' jobs and orders; nothing runs otherwise."""
    mine, theirs, own, other = _two_projects(tmp_path)
    _order("aaaa000000000001", mine.slug)
    _order("aaaa000000000002", theirs.slug)
    client = _client(str(mine.id))
    calls: list[tuple[str, list[str]]] = []

    def run(lock: str, argv: list[str]) -> dict:
        calls.append((lock, argv))
        return {"ok": True}

    for path in (f"/api/v1/jobs/{other}/abandon", "/api/v1/orders/aaaa000000000002/cancel"):
        status, body, _headers = public_api.answer_public_api_post(path, b"{}", run, client=client)
        assert (status, body["error"]) == (403, "api_client_policy_refused"), path
        assert body["message"].endswith("nothing was run")
    assert calls == []
    for path in (f"/api/v1/jobs/{own}/abandon", "/api/v1/orders/aaaa000000000001/cancel"):
        status, body, _headers = public_api.answer_public_api_post(path, b"{}", run, client=client)
        assert status == 200, (path, body)
    assert [lock for lock, _argv in calls] == [own, "order:aaaa000000000001"]
