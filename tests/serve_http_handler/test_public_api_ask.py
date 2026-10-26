"""The read-only ask over HTTP (operator amendment amend1026-go-live-and-ask, Part C2): what
`POST /api/v1/projects/{project}/ask` refuses before anything runs, the command line its twin runs
with, the runner's own timeout and the call ledger's host-tools mark. The ask itself is
`tests/orchestration/test_project_ask.py`'s."""
from __future__ import annotations

import json
import subprocess

import pytest

from packages.orchestration import public_api


@pytest.fixture()
def project(tmp_path, monkeypatch):
    from packages.orchestration.project_registry import register_project_repo

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    repo = tmp_path / "ask-repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    register_project_repo("ask-repo", repo)
    return repo


def _client(*, host_tools: bool, projects=("ask-repo",), ceiling=200000):
    from packages.orchestration.api_clients import ApiClient

    return ApiClient(name="asker", token="ask-route-test-token-0123456789abcdef", projects=tuple(projects),
                     max_total_tokens=ceiling, max_provider_calls=None, may_apply=False, host_tools=host_tools)


@pytest.mark.parametrize("client, body, status, error", [
    (_client(host_tools=False), {"question": "Was?", "max_total_tokens": 1000}, 400, "api_provider_not_offered"),
    (_client(host_tools=True, projects=("other",)), {"question": "Was?", "max_total_tokens": 1000}, 403,
     "api_client_policy_refused"),
    (_client(host_tools=True, ceiling=500), {"question": "Was?", "max_total_tokens": 1000}, 403,
     "api_client_policy_refused"),
    (_client(host_tools=True), {"question": "Was?"}, 400, "api_body_invalid"),
    (_client(host_tools=True), {"question": "Was?", "max_total_tokens": True}, 400, "api_body_invalid"),
    (_client(host_tools=True), {"question": "Was?", "max_total_tokens": 1000, "attachments": ["a"]}, 400,
     "api_body_invalid"),
])
def test_the_route_refuses_before_anything_runs(project, client, body, status, error):
    ran = []
    answered = public_api.answer_public_api_post(
        "/api/v1/projects/ask-repo/ask", json.dumps(body).encode(), lambda *a, **k: ran.append(a), client=client)
    assert (answered[0], answered[1]["error"]) == (status, error) and ran == []


def test_the_route_runs_the_twin_with_its_own_timeout_and_the_ledger_marks_it(project):
    calls = []

    def run_command(lock, argv, **keys):
        calls.append((lock, argv, keys))
        return {"ok": True, "answer": "x"}

    status, body, _headers = public_api.answer_public_api_post(
        "/api/v1/projects/ask-repo/ask", json.dumps({"question": "Was?", "max_total_tokens": 1000}).encode(),
        run_command, client=_client(host_tools=True))
    assert status == 200 and body["answer"] == "x"
    [(lock, argv, keys)] = calls
    assert lock == "project:ask-repo" and keys == {"timeout": 960}
    assert argv == ["client", "ask", "--max-total-tokens=1000", "--asked-by=asker", "--json", "--", "ask-repo", "Was?"]
    assert public_api.public_api_call_host_tools(b"{}", "/api/v1/projects/ask-repo/ask") is True
    assert public_api.public_api_call_host_tools(b"{}", "/api/v1/jobs/x/stop") is False
