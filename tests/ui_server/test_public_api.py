"""Contract tests for the public HTTP API's route registry (F253, DECISION F253 D1).

Pins `GET /api/v1/interface`, the registry's shape rules and the version rule, over real HTTP
requests to the cockpit's handler on a TCP socket and to the supervisor's handler on a unix
socket. No job, no provider, no model: the one route this round publishes answers the same
thing regardless of which job, if any, a server was started for.

`PINNED_ROUTES` is the drift guard: a route the registry carries with no test named here fails
the suite, so a route added later cannot ship unpinned.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import threading
from dataclasses import replace
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from uuid import uuid4

import pytest

from packages.orchestration import public_api
from packages.orchestration.serve_daemon import UnixHTTPConnection, socket_handler_class
from packages.orchestration.ui_server import _RemedyHandler, token_fingerprint

REPO_ROOT = Path(__file__).resolve().parents[2]
SERVER_TOKEN = "f253-public-api-test-token"

#: `(method, path)` of every published route to the name of the test that pins it. A test that
#: the registry's own `(method, path)` set equals this dict's keys, and that every name here
#: exists in this module, makes an unpinned route fail the suite.
PINNED_ROUTES: dict[tuple[str, str], str] = {
    ("GET", "/api/v1/interface"): "test_interface_route_answers_the_command_envelope",
    ("GET", "/api/v1/digest"): "test_digest_route_answers_the_status_commands_client_object",
    ("GET", "/api/v1/jobs/{job}/proof"): "test_proof_route_answers_the_change_proof_command",
    ("GET", "/api/v1/changes"): "test_changes_route_answers_the_client_changes_command",
    ("POST", "/api/v1/jobs/{job}/decisions/{decision}"):
        "test_the_decision_route_is_pinned_with_its_body_and_its_statuses",
    ("POST", "/api/v1/jobs/{job}/decline"):
        "test_the_decline_route_is_pinned_with_its_body_and_its_statuses",
    ("POST", "/api/v1/jobs/{job}/apply"):
        "test_the_apply_route_is_pinned_with_its_body_and_its_statuses",
    ("GET", "/api/v1/orders/{order}"):
        "test_the_order_poll_route_is_pinned_with_its_statuses",
}


def _handler_class() -> type:
    """A `_RemedyHandler` subclass bound to a known token, no job, no preview worker."""
    return type("_PublicApiTestHandler", (_RemedyHandler,), {
        "server_token": SERVER_TOKEN,
        "target_job_id": "",
        "app_html": "",
    })


@pytest.fixture
def tcp_server():
    """The cockpit's own handler on a real TCP socket, 127.0.0.1, port 0."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), _handler_class())
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server.server_address[1]
    finally:
        server.shutdown()
        thread.join(10)
        server.server_close()


@pytest.fixture
def unix_server(tmp_path_factory):
    """The supervisor's own handler, `socket_handler_class`, on a real unix socket."""
    import socketserver

    base = tmp_path_factory.mktemp("pa")
    sock_path = base / "s.sock"

    class _Server(socketserver.ThreadingUnixStreamServer):
        daemon_threads = True

    server = _Server(str(sock_path), socket_handler_class(SERVER_TOKEN))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield sock_path
    finally:
        server.shutdown()
        thread.join(10)
        server.server_close()


def _tcp_request(port: int, method: str, path: str,
                  headers: dict[str, str] | None = None) -> tuple[int, dict, dict[str, str]]:
    conn = HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.request(method, path, headers=headers or {})
        resp = conn.getresponse()
        raw = resp.read()
        status = resp.status
        resp_headers = dict(resp.getheaders())
    finally:
        conn.close()
    body = json.loads(raw) if raw else {}
    return status, body, resp_headers


def _unix_request(sock_path: Path, method: str, path: str,
                   headers: dict[str, str] | None = None) -> tuple[int, dict, dict[str, str]]:
    conn = UnixHTTPConnection(sock_path, timeout=10)
    try:
        conn.request(method, path, headers=headers or {})
        resp = conn.getresponse()
        raw = resp.read()
        status = resp.status
        resp_headers = dict(resp.getheaders())
    finally:
        conn.close()
    body = json.loads(raw) if raw else {}
    return status, body, resp_headers


def _bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _command_line_interface_answer() -> dict:
    """`remedy client interface --json`'s real standard output, as a subprocess, parsed."""
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "client", "interface", "--json"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def _status_json_client(extra_args: tuple[str, ...] = ()) -> dict:
    """`remedy status --json [extra_args]`'s real `client` key, as a subprocess, parsed."""
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "status", "--json", *extra_args],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)["client"]


def _change_proof_command_answer(job_id: str, *, ok: bool = True) -> dict:
    """`remedy change proof <job_id> --json`'s real standard output, as a subprocess, parsed.

    A refusal exits nonzero but still prints the envelope to stdout
    (`apps.cli.json_envelope.fail`), so `ok` only selects which exit this call expects.
    """
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "change", "proof", job_id, "--json"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=30,
    )
    if ok:
        assert result.returncode == 0, result.stderr
    else:
        assert result.returncode != 0, result.stderr
    return json.loads(result.stdout)


def _client_changes_command_answer(since: str | None = None, *, exit_code: int = 0) -> dict:
    """`remedy client changes [--since <since>] --json`'s real standard output, as a subprocess,
    parsed. A refusal exits nonzero but still prints the envelope to stdout
    (`apps.cli.json_envelope.fail`), so `exit_code` only selects which exit this call expects.
    """
    args = [sys.executable, "-m", "apps.cli.main", "client", "changes", "--json"]
    if since is not None:
        args += ["--since", since]
    result = subprocess.run(args, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=30)
    assert result.returncode == exit_code, result.stdout + result.stderr
    return json.loads(result.stdout)


#: Git identity for the scratch repository the seed below commits into.
_SEED_GIT_IDENTITY = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                      "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
#: A deadline already in the past: the run's budget stops it before any task runs,
#: raising the one decision a fake run raises on its own (as
#: tests/cli/test_machine_client_contract.py uses it).
_SEED_PAST_DEADLINE = "2000-01-01T00:00:00+00:00"


def _seed_project_job_and_decision(tmp_path: Path) -> None:
    """Put one project, one job and one open decision on the current data root.

    The same path as tests/cli/test_machine_client_contract.py, with the fake providers: an
    order file whose deadline has already passed stops the run before any task runs and raises
    the budget decision, so `remedy do` exits 1 and leaves one job with one open decision behind.
    """
    repo = tmp_path / "seed-repo"
    repo.mkdir()
    env = {**os.environ, **_SEED_GIT_IDENTITY}
    subprocess.run(["git", "init", "-q", str(repo)], check=True, env=env)
    (repo / "README.md").write_text("# Scratch\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "README.md"], check=True, env=env)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "init"], check=True, env=env)
    order_file = tmp_path / "seed-order.md"
    order_file.write_text(
        "---\nmax-cost-usd: 1\n---\nAdd a line saying hello to README.md\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "do", str(order_file), "--json",
         "--no-ui", "--yes", "--no-llm", "--builder-provider", "fake",
         "--reviewer-provider", "fake", "--deadline", _SEED_PAST_DEADLINE],
        cwd=str(repo), capture_output=True, text=True, env=env, timeout=120)
    assert result.returncode == 1, result.stdout + result.stderr


def _without_generated_at(answer: dict) -> dict:
    """`answer` without its own `generated_at`, stamped fresh by each call to `build_proof_chain`."""
    return {k: v for k, v in answer.items() if k != "generated_at"}


def _without_volatile_digest_fields(digest: dict) -> dict:
    """`digest` without its own `read_at` and without any decision's `age_seconds`."""
    copy = {k: v for k, v in digest.items() if k != "read_at"}
    copy["decisions"] = [
        {k: v for k, v in decision.items() if k != "age_seconds"}
        for decision in copy.get("decisions", [])
    ]
    return copy


def _without_volatile_changes_fields(changes: dict) -> dict:
    """`changes` without its own `read_at` and `cursor`, and without any decision's
    `age_seconds` (both `decisions` and `closed_decisions` carry the key)."""
    copy = {k: v for k, v in changes.items() if k not in ("read_at", "cursor")}
    for key in ("decisions", "closed_decisions"):
        copy[key] = [{k: v for k, v in entry.items() if k != "age_seconds"}
                     for entry in copy.get(key, [])]
    return copy


# -- A: the one route, over both transports ---------------------------------


def test_interface_route_answers_the_command_envelope(tcp_server):
    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/interface", headers=_bearer(SERVER_TOKEN))
    assert status == 200, body
    assert body == _command_line_interface_answer()


def test_the_same_route_over_the_supervisors_socket_answers_the_same_body(unix_server):
    status, body, _headers = _unix_request(
        unix_server, "GET", "/api/v1/interface", headers=_bearer(SERVER_TOKEN))
    assert status == 200, body
    assert body == _command_line_interface_answer()


# -- B: refusals --------------------------------------------------------------


def test_no_authorization_header_is_401(tcp_server):
    status, body, _headers = _tcp_request(tcp_server, "GET", "/api/v1/interface")
    assert status == 401, body
    assert body["ok"] is False
    assert body["error"] == "api_token_invalid"
    assert body["schema_version"] == 1


def test_a_wrong_bearer_token_is_401(tcp_server):
    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/interface", headers=_bearer("not-the-token"))
    assert status == 401, body
    assert body["ok"] is False
    assert body["error"] == "api_token_invalid"
    assert body["schema_version"] == 1


def test_the_right_token_only_in_the_query_is_401(tcp_server):
    status, body, _headers = _tcp_request(
        tcp_server, "GET", f"/api/v1/interface?token={SERVER_TOKEN}")
    assert status == 401, body
    assert body["ok"] is False
    assert body["error"] == "api_token_invalid"
    assert body["schema_version"] == 1


def test_an_unknown_path_with_the_right_token_is_404(tcp_server):
    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/nothing", headers=_bearer(SERVER_TOKEN))
    assert status == 404, body
    assert body["error"] == "api_route_not_found"


def test_the_bare_prefix_with_the_right_token_is_404(tcp_server):
    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1", headers=_bearer(SERVER_TOKEN))
    assert status == 404, body
    assert body["error"] == "api_route_not_found"


def test_an_unknown_path_without_a_token_is_401_not_404(tcp_server):
    status, body, _headers = _tcp_request(tcp_server, "GET", "/api/v1/nothing")
    assert status == 401, body
    assert body["error"] == "api_token_invalid"


# -- C: the drift guard -------------------------------------------------------


def test_every_route_is_pinned_by_name():
    registry_keys = {(route.method, route.path) for route in public_api.PUBLIC_API_ROUTES}
    assert registry_keys == set(PINNED_ROUTES.keys()), {
        "unpinned": sorted(registry_keys - set(PINNED_ROUTES.keys())),
        "vanished": sorted(set(PINNED_ROUTES.keys()) - registry_keys),
    }
    module_globals = globals()
    for test_name in PINNED_ROUTES.values():
        assert test_name in module_globals, f"{test_name} is not defined in this module"


# -- D: every route's shape ---------------------------------------------------


def test_every_route_is_well_formed():
    import re

    from apps.cli.client_interface import (
        CLIENT_OPERATION_IDS,
        OPERATION_ANSWER_KEYS,
        OPERATION_REFUSAL_TOKENS,
    )
    from apps.cli.command_catalog import get_command

    segment_re = re.compile(r"^[A-Za-z0-9_-]+$")
    for route in public_api.PUBLIC_API_ROUTES:
        assert route.path.startswith(public_api.PUBLIC_API_PREFIX + "/")
        assert route.method in ("GET", "POST")
        assert bool(route.body) == (route.method == "POST")
        assert (route.refusal_default is not None) == (route.method == "POST")
        entry = get_command(route.twin)  # raises KeyError if not a catalog command
        assert route.twin in CLIENT_OPERATION_IDS
        assert not public_api.command_is_excluded(route.twin)
        if route.twin_key is not None:
            assert route.twin_key in OPERATION_ANSWER_KEYS[route.twin]
        for segment in route.path.split("/")[1:]:
            is_named = segment.startswith("{") and segment.endswith("}")
            assert is_named or segment_re.match(segment), segment
        for token, status in route.refusals:
            assert token in OPERATION_REFUSAL_TOKENS[route.twin], (route.twin, token)
            assert status in (400, 404, 409), (route.twin, token, status)
        option_flags = {arg.name for arg in entry.args if arg.is_option}
        value_options = {arg.name for arg in entry.args if arg.is_option and not arg.is_flag}
        for key in route.query:
            assert "--" + key.replace("_", "-") in option_flags
        for key in route.query_values:
            assert "--" + key.replace("_", "-") in value_options
        flag_options = {arg.name for arg in entry.args if arg.is_option and arg.is_flag}
        for key, kind in route.body:
            assert kind in ("string", "strings", "flag")
            if kind == "flag":
                assert "--" + key.replace("_", "-") in flag_options, (route.path, key)
            else:
                assert "--" + key in value_options, (route.path, key)
    major = public_api.PUBLIC_API_PREFIX.rsplit("/api/v", 1)[-1]
    assert public_api.PUBLIC_API_VERSION.split(".")[0] == major


# -- E: the exclusion list -----------------------------------------------------


def test_the_exclusion_list_holds_the_feature_files_initial_entries():
    assert public_api.PUBLIC_API_EXCLUDED_COMMANDS == (
        "patch.apply", "patch.revert", "rollback.*", "snapshot.create", "config.set",
        "config.init", "init.run", "self-repair.proposal-approve", "self-repair.proposal-deny",
        "worker.unload", "runtime.stop", "ui.stop", "queue.rm", "queue.reclaim",
    )


def test_command_is_excluded_matches_a_wildcard_entry():
    assert public_api.command_is_excluded("rollback.anything") is True


def test_command_is_excluded_does_not_match_a_published_command():
    assert public_api.command_is_excluded("client.interface") is False


# -- F: deprecation -------------------------------------------------------------


def test_a_deprecated_route_answers_the_deprecation_header(tcp_server, monkeypatch):
    deprecated_route = replace(public_api.PUBLIC_API_ROUTES[0], deprecated=True)
    monkeypatch.setattr(public_api, "PUBLIC_API_ROUTES", (deprecated_route,))
    status, _body, headers = _tcp_request(
        tcp_server, "GET", deprecated_route.path, headers=_bearer(SERVER_TOKEN))
    assert status == 200
    assert headers.get("Deprecation") == "true"


def test_an_undeprecated_route_sends_no_deprecation_header(tcp_server):
    status, _body, headers = _tcp_request(
        tcp_server, "GET", "/api/v1/interface", headers=_bearer(SERVER_TOKEN))
    assert status == 200
    assert "Deprecation" not in headers


# -- G: the published page -----------------------------------------------------


def test_the_pages_generated_section_equals_the_rendering():
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    start = page.index(public_api.PUBLIC_API_PAGE_BEGIN)
    end = page.index(public_api.PUBLIC_API_PAGE_END) + len(public_api.PUBLIC_API_PAGE_END) + 1
    assert page[start:end] == public_api.render_public_api_markdown()


def test_the_page_states_the_prefix_the_auth_scheme_and_the_refusal_tokens():
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    assert "/api/v1" in page
    assert "Authorization: Bearer" in page
    assert "api_token_invalid" in page
    assert "api_route_not_found" in page
    assert "Deprecation: true" in page


def test_the_page_states_the_ledger_file_and_the_query_refusal_token():
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    assert "api/calls.jsonl" in page
    assert "api_query_invalid" in page


def test_the_page_states_the_changes_route_and_the_value_query_key():
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    assert "/api/v1/changes" in page
    assert "since=<value>" in page


def test_the_page_states_the_supervisor_ports_setting():
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    assert "serve.api_port" in page
    assert "REMEDY_SERVE_API_PORT" in page


def test_every_remedy_command_the_pages_hand_written_part_names_is_in_the_catalog():
    """R-1187: a `remedy <group> <subcommand>` span above the generated marker is real.

    A group named alone (no second word, or a second word starting with `-`) passes only
    when the catalog holds that group's `run` command — the way `remedy status` and `remedy
    do` run without a subcommand, and `remedy ui` prints its help instead (recurrence, round
    3, DECISION F253 D3 (5)): a bare `remedy ui` must fail here, not pass because the group
    merely exists.

    Mutates nothing; this is the standing proof, not the mutation the reviewer runs.
    """
    import re

    from apps.cli.command_catalog import CATALOG, resolve_group

    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    hand_written = page[:page.index(public_api.PUBLIC_API_PAGE_BEGIN)]
    spans = [s for s in re.findall(r"`([^`]+)`", hand_written) if s.startswith("remedy ")]
    assert spans, "no `remedy ...` span found in the page's hand-written part"
    for span in spans:
        words = span.split()
        first = words[1] if len(words) > 1 else ""
        second = words[2] if len(words) > 2 else ""
        if second and not second.startswith("-"):
            group_id = resolve_group(first)
            assert any(cmd.group_id == group_id and cmd.subcommand == second
                       for cmd in CATALOG), span
        else:
            group_id = resolve_group(first)
            assert group_id is not None, span
            assert any(cmd.group_id == group_id and cmd.subcommand == "run"
                       for cmd in CATALOG), span


def test_the_page_states_the_method_refusal_token():
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    assert "api_method_not_allowed" in page


# -- H: the digest route, twinned with status.run's client object -------------


def test_digest_route_answers_the_status_commands_client_object(tcp_server, tmp_path):
    _seed_project_job_and_decision(tmp_path)

    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/digest", headers=_bearer(SERVER_TOKEN))
    assert status == 200, body
    digest = {k: v for k, v in body.items() if k not in ("schema_version", "ok")}
    reference = _status_json_client()
    assert digest["jobs"], "the digest holds no job"
    assert digest["decisions"], "the digest holds no decision"
    assert _without_volatile_digest_fields(digest) == _without_volatile_digest_fields(reference)

    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/digest?all_ended_jobs=true", headers=_bearer(SERVER_TOKEN))
    assert status == 200, body
    digest_all = {k: v for k, v in body.items() if k not in ("schema_version", "ok")}
    reference_all = _status_json_client(("--all-ended-jobs",))
    assert (_without_volatile_digest_fields(digest_all)
            == _without_volatile_digest_fields(reference_all))


# -- H2: the proof route, twinned with change.proof ----------------------------


def test_proof_route_answers_the_change_proof_command(tcp_server, tmp_path):
    _seed_project_job_and_decision(tmp_path)
    client = _status_json_client()
    job_id = client["jobs"][0]["job_id"]
    reference = _without_generated_at(_change_proof_command_answer(job_id))

    for candidate in (job_id, job_id[:8]):
        status, body, _headers = _tcp_request(
            tcp_server, "GET", f"/api/v1/jobs/{candidate}/proof", headers=_bearer(SERVER_TOKEN))
        assert status == 200, body
        assert _without_generated_at(body) == reference


def test_proof_route_refusals_match_the_change_proof_command(tcp_server, tmp_path):
    _seed_project_job_and_decision(tmp_path)
    client = _status_json_client()
    job_id = client["jobs"][0]["job_id"]

    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/jobs/not-a-job/proof", headers=_bearer(SERVER_TOKEN))
    assert status == 404, body
    assert body["error"] == "invalid_job_id"
    assert body == _change_proof_command_answer("not-a-job", ok=False)

    missing = str(uuid4())
    status, body, _headers = _tcp_request(
        tcp_server, "GET", f"/api/v1/jobs/{missing}/proof", headers=_bearer(SERVER_TOKEN))
    assert status == 404, body
    assert body["error"] == "job_not_found"
    assert body == _change_proof_command_answer(missing, ok=False)

    # An ambiguous prefix: a second job id that shares the first eight hex characters.
    data_root = Path(os.environ["REMEDY_DATA_DIR"])
    source = data_root / "jobs" / job_id
    last = job_id[-1]
    twin_id = job_id[:-1] + ("0" if last != "0" else "1")
    shutil.copytree(source, data_root / "jobs" / twin_id)
    prefix = job_id[:8]
    status, body, _headers = _tcp_request(
        tcp_server, "GET", f"/api/v1/jobs/{prefix}/proof", headers=_bearer(SERVER_TOKEN))
    assert status == 400, body
    assert body["error"] == "ambiguous_job_id"
    assert body == _change_proof_command_answer(prefix, ok=False)


def test_the_proof_route_has_no_route_beneath_or_above_it(tcp_server, tmp_path):
    _seed_project_job_and_decision(tmp_path)
    client = _status_json_client()
    job_id = client["jobs"][0]["job_id"]

    status, body, _headers = _tcp_request(
        tcp_server, "GET", f"/api/v1/jobs/{job_id}", headers=_bearer(SERVER_TOKEN))
    assert status == 404, body
    assert body["error"] == "api_route_not_found"

    status, body, _headers = _tcp_request(
        tcp_server, "GET", f"/api/v1/jobs/{job_id}/proof/extra", headers=_bearer(SERVER_TOKEN))
    assert status == 404, body
    assert body["error"] == "api_route_not_found"

    status, body, _headers = _tcp_request(
        tcp_server, "GET", f"/api/v1/jobs/{job_id}/proof?path=README.md",
        headers=_bearer(SERVER_TOKEN))
    assert status == 400, body
    assert body["error"] == "api_query_invalid"


# -- H3: the changes route, twinned with client.changes (S3b, DECISION F253 D5) -----


def test_changes_route_answers_the_client_changes_command(tcp_server, tmp_path):
    _seed_project_job_and_decision(tmp_path)

    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/changes", headers=_bearer(SERVER_TOKEN))
    assert status == 200, body
    reference = _client_changes_command_answer()
    assert _without_volatile_changes_fields(body) == _without_volatile_changes_fields(reference)

    since = "2000-01-01T00:00:00Z"
    status, body, _headers = _tcp_request(
        tcp_server, "GET", f"/api/v1/changes?since={since}", headers=_bearer(SERVER_TOKEN))
    assert status == 200, body
    reference = _client_changes_command_answer(since)
    assert body["jobs"], "the route lists no job"
    assert _without_volatile_changes_fields(body) == _without_volatile_changes_fields(reference)

    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/changes?since=yesterday", headers=_bearer(SERVER_TOKEN))
    assert status == 400, body
    reference = _client_changes_command_answer("yesterday", exit_code=2)
    assert body == reference

    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/changes?since=", headers=_bearer(SERVER_TOKEN))
    assert status == 400, body
    assert body["error"] == "api_query_invalid"

    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/changes?since=a&since=b", headers=_bearer(SERVER_TOKEN))
    assert status == 400, body
    assert body["error"] == "api_query_invalid"


# -- I: query refusals ----------------------------------------------------------


@pytest.mark.parametrize("path", [
    "/api/v1/digest?nope=true",
    "/api/v1/digest?all_ended_jobs=yes",
    "/api/v1/digest?all_ended_jobs=",
    "/api/v1/digest?all_ended_jobs=true&all_ended_jobs=false",
    f"/api/v1/interface?token={SERVER_TOKEN}",
])
def test_an_undeclared_key_a_repeated_key_or_a_bad_value_is_400(tcp_server, path):
    status, body, _headers = _tcp_request(
        tcp_server, "GET", path, headers=_bearer(SERVER_TOKEN))
    assert status == 400, body
    assert body["error"] == "api_query_invalid"


def test_a_declared_flag_set_to_false_is_200(tcp_server):
    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/digest?all_ended_jobs=false", headers=_bearer(SERVER_TOKEN))
    assert status == 200, body


def test_an_invalid_query_without_a_token_is_401_not_400(tcp_server):
    status, body, _headers = _tcp_request(tcp_server, "GET", "/api/v1/digest?nope=true")
    assert status == 401, body
    assert body["error"] == "api_token_invalid"


# -- J: the call ledger ----------------------------------------------------------


def test_the_ledger_holds_one_line_per_request_in_order(tcp_server):
    data_root = Path(os.environ["REMEDY_DATA_DIR"])
    ledger_path = data_root / "api" / "calls.jsonl"

    status, _body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/interface", headers=_bearer(SERVER_TOKEN))
    assert status == 200
    status, _body, _headers = _tcp_request(tcp_server, "GET", "/api/v1/interface")
    assert status == 401
    status, _body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/nothing", headers=_bearer(SERVER_TOKEN))
    assert status == 404
    status, _body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/digest?nope=true", headers=_bearer(SERVER_TOKEN))
    assert status == 400

    raw_lines = ledger_path.read_text(encoding="utf-8").splitlines()
    assert len(raw_lines) == 4
    records = [json.loads(line) for line in raw_lines]
    for record in records:
        assert list(record.keys()) == ["ts", "token_fp", "method", "path", "status", "error"]
        assert record["method"] == "GET"

    assert records[0]["status"] == 200
    assert records[0]["error"] == ""
    assert records[0]["path"] == "/api/v1/interface"
    assert records[0]["token_fp"] == token_fingerprint(SERVER_TOKEN)

    assert records[1]["status"] == 401
    assert records[1]["error"] == "api_token_invalid"
    assert records[1]["path"] == "/api/v1/interface"
    assert records[1]["token_fp"] == token_fingerprint("")

    assert records[2]["status"] == 404
    assert records[2]["error"] == "api_route_not_found"
    assert records[2]["path"] == "/api/v1/nothing"
    assert records[2]["token_fp"] == token_fingerprint(SERVER_TOKEN)

    assert records[3]["status"] == 400
    assert records[3]["error"] == "api_query_invalid"
    assert records[3]["path"] == "/api/v1/digest"
    assert records[3]["token_fp"] == token_fingerprint(SERVER_TOKEN)

    for raw_line in raw_lines:
        assert SERVER_TOKEN not in raw_line
        assert "?" not in raw_line
        assert "nope" not in raw_line

    assert (ledger_path.parent.stat().st_mode & 0o777) == 0o700
    assert (ledger_path.stat().st_mode & 0o777) == 0o600


# -- K: a failed ledger write never changes the answer ---------------------------


def test_a_failed_ledger_write_never_changes_the_answer(tcp_server, monkeypatch):
    def _raise_os_error(**_kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(public_api, "append_public_api_call", _raise_os_error)

    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/interface", headers=_bearer(SERVER_TOKEN))
    assert status == 200, body
    assert body == _command_line_interface_answer()

    status, body, _headers = _tcp_request(tcp_server, "GET", "/api/v1/interface")
    assert status == 401, body


# -- L: POST, PUT and DELETE under the namespace (R-1188) -----------------------


@pytest.mark.parametrize("method", ["POST", "PUT", "DELETE"])
def test_post_put_and_delete_answer_method_not_allowed_with_the_token(tcp_server, method):
    status, body, _headers = _tcp_request(
        tcp_server, method, "/api/v1/interface", headers=_bearer(SERVER_TOKEN))
    assert status == 405, body
    assert body["ok"] is False
    assert body["error"] == "api_method_not_allowed"
    assert body["schema_version"] == 1


@pytest.mark.parametrize("method", ["POST", "PUT", "DELETE"])
def test_post_put_and_delete_without_the_token_are_401(tcp_server, method):
    status, body, _headers = _tcp_request(tcp_server, method, "/api/v1/interface")
    assert status == 401, body
    assert body["error"] == "api_token_invalid"


def test_post_put_and_delete_each_write_their_own_ledger_line(tcp_server):
    data_root = Path(os.environ["REMEDY_DATA_DIR"])
    ledger_path = data_root / "api" / "calls.jsonl"

    for method in ("POST", "PUT", "DELETE"):
        status, _body, _headers = _tcp_request(
            tcp_server, method, "/api/v1/interface", headers=_bearer(SERVER_TOKEN))
        assert status == 405

    raw_lines = ledger_path.read_text(encoding="utf-8").splitlines()
    assert len(raw_lines) == 3
    records = [json.loads(line) for line in raw_lines]
    for method, record in zip(("POST", "PUT", "DELETE"), records):
        assert record["method"] == method
        assert record["status"] == 405
        assert record["error"] == "api_method_not_allowed"
        assert record["path"] == "/api/v1/interface"


# -- M: the write route that answers a decision (S4a, DECISION F253 D9) -----------

DECISION_PATH = "/api/v1/jobs/{job}/decisions/{decision}"
_OK_ENVELOPE = {"schema_version": 1, "ok": True, "outcome": "answered"}


def _decision_route() -> public_api.PublicApiRoute:
    return next(route for route in public_api.PUBLIC_API_ROUTES if route.path == DECISION_PATH)


def _recording_runner(envelope: dict | None = _OK_ENVELOPE):
    """A stand-in `run_command` that records its arguments and returns ENVELOPE."""
    calls: list[tuple[str, list[str]]] = []

    def run(job: str, argv: list[str]) -> dict | None:
        calls.append((job, argv))
        return envelope

    return calls, run


def _post(path: str, body: object, run) -> tuple[int, dict, dict[str, str]]:
    raw = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
    return public_api.answer_public_api_post(path, raw, run)


def test_the_decision_route_is_pinned_with_its_body_and_its_statuses():
    route = _decision_route()
    assert (route.method, route.path, route.twin) == ("POST", DECISION_PATH, "decision.resolve")
    assert route.body == (("reason", "string"), ("answer", "strings"))
    assert route.refusal_default == 409
    assert route.refusals == (
        ("invalid_job_id", 404), ("job_not_found", 404), ("decision_not_found", 404),
        ("stop_reason_not_found", 404), ("proposed_task_not_found", 404),
        ("ambiguous_job_id", 400), ("invalid_argument", 400), ("missing_argument", 400),
        ("option_not_applicable", 400), ("answer_parse_error", 400), ("invalid_budget", 400),
        ("decision_not_resolvable", 400),
    )
    assert "--as-mission" in route.description and "is not offered" in route.description
    assert public_api.PUBLIC_API_VERSION == "1.7"


def test_the_page_names_the_body_keys_and_the_default_status_of_the_decision_route():
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    assert "Query or body" in page
    assert "`reason` (string), `answer` (strings)" in page
    assert "`decision_not_resolvable` 400, any other 409" in page


def test_the_page_states_how_a_write_is_refused():
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    hand_written = page[:page.index(public_api.PUBLIC_API_PAGE_BEGIN)]
    assert "## Writes" in hand_written
    for token in ("api_body_invalid", "api_path_invalid", "api_command_failed"):
        assert token in hand_written, token


def test_a_post_builds_the_command_line_from_the_body_and_the_path():
    calls, run = _recording_runner()
    status, body, headers = _post("/api/v1/jobs/j1/decisions/d1",
                                  {"reason": "extend", "answer": ["a b", "--c"]}, run)
    assert (status, body, headers) == (200, _OK_ENVELOPE, {})
    assert calls == [("j1", ["decision", "resolve", "--reason=extend", "--answer=a b",
                             "--answer=--c", "--json", "--", "j1", "d1"])]


@pytest.mark.parametrize("raw", [b"", b"  \n", b"{}"])
def test_a_post_with_no_body_or_an_empty_object_takes_the_bare_command_line(raw):
    calls, run = _recording_runner()
    assert _post("/api/v1/jobs/j1/decisions/d1", raw, run)[0] == 200
    assert calls == [("j1", ["decision", "resolve", "--json", "--", "j1", "d1"])]


@pytest.mark.parametrize("body, key", [
    (b"not json", "valid JSON"),
    (b"\xff\xfe", "valid JSON"),
    (b'["reason"]', "JSON object"),
    (b'"reason"', "JSON object"),
    (b'{"as_mission": true}', "as_mission"),
    (b'{"reason": 3}', "reason"),
    (b'{"reason": null}', "reason"),
    (b'{"answer": "Postgres"}', "answer"),
    (b'{"answer": ["ok", ""]}', "answer"),
    (b'{"answer": ["ok", 2]}', "answer"),
])
def test_a_post_body_that_is_not_the_routes_own_is_400_and_runs_nothing(body, key):
    calls, run = _recording_runner()
    status, answer, _headers = _post("/api/v1/jobs/j1/decisions/d1", body, run)
    assert status == 400 and answer["error"] == "api_body_invalid"
    assert key in answer["message"]
    assert calls == []


@pytest.mark.parametrize("path", [
    "/api/v1/jobs/-h/decisions/d1", "/api/v1/jobs/j1/decisions/--help",
    "/api/v1/jobs/-/decisions/d1",
])
def test_a_path_value_that_begins_with_a_dash_is_400_and_runs_nothing(path):
    calls, run = _recording_runner()
    status, answer, _headers = _post(path, {}, run)
    assert status == 400 and answer["error"] == "api_path_invalid"
    assert calls == []


def test_a_command_that_prints_no_envelope_is_500():
    calls, run = _recording_runner(None)
    status, answer, _headers = _post("/api/v1/jobs/j1/decisions/d1", {}, run)
    assert (status, answer["error"]) == (500, "api_command_failed")
    assert len(calls) == 1


@pytest.mark.parametrize("token, expected", [
    ("decision_not_found", 404), ("ambiguous_job_id", 400), ("decision_already_answered", 409),
    ("a_token_nobody_listed", 409),
])
def test_a_refusal_keeps_the_commands_envelope_and_takes_its_routes_status(token, expected):
    refusal = {"schema_version": 1, "ok": False, "error": token, "message": "m"}
    _calls, run = _recording_runner(refusal)
    status, answer, _headers = _post("/api/v1/jobs/j1/decisions/d1", {}, run)
    assert (status, answer) == (expected, refusal)


def test_a_get_of_a_write_routes_path_is_404_and_a_post_of_a_get_routes_path_is_405():
    status, body, _headers = public_api.answer_public_api_get("/api/v1/jobs/j1/decisions/d1")
    assert (status, body["error"]) == (404, "api_route_not_found")
    _calls, run = _recording_runner()
    status, body, _headers = _post("/api/v1/interface", {}, run)
    assert (status, body["error"]) == (405, "api_method_not_allowed")
    status, body, _headers = _post("/api/v1/nothing", {}, run)
    assert (status, body["error"]) == (404, "api_route_not_found")


def test_the_cockpits_own_server_answers_a_decision_post_405_and_ledgers_it(tcp_server):
    ledger_path = Path(os.environ["REMEDY_DATA_DIR"]) / "api" / "calls.jsonl"
    path = "/api/v1/jobs/j1/decisions/d1"
    status, body, _headers = _tcp_request(tcp_server, "POST", path, headers=_bearer(SERVER_TOKEN))
    assert (status, body["error"]) == (405, "api_method_not_allowed")
    assert "remedy serve start" in body["message"]
    records = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines()]
    assert [(r["method"], r["path"], r["status"]) for r in records] == [("POST", path, 405)]


def test_a_percent_encoded_path_value_reaches_the_command_decoded():
    """R-1192: `encodeURIComponent` and `urllib.parse.quote` both send `:` as `%3A`."""
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    assert "percent-encoded" in page[:page.index(public_api.PUBLIC_API_PAGE_BEGIN)]
    calls, run = _recording_runner()
    status, _body, _headers = _post("/api/v1/jobs/j1/decisions/td%3Aabc%3A1", {}, run)
    assert status == 200
    assert calls == [("j1", ["decision", "resolve", "--json", "--", "j1", "td:abc:1"])]


def test_a_path_value_that_decodes_to_a_dash_is_400_and_runs_nothing():
    calls, run = _recording_runner()
    status, answer, _headers = _post("/api/v1/jobs/%2Dh/decisions/d1", {}, run)
    assert (status, answer["error"]) == (400, "api_path_invalid")
    assert calls == []


def test_a_job_prefix_and_its_full_id_lock_on_the_same_job():
    """R-1193: the runner's one-command-per-job lock is keyed by the job, not by its spelling."""
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

    job = JobPlan(job_title="lock-key-job", user_prompt="Lock key prompt",
                  tasks=[TaskEntry(title="Pick a database")])
    save_job_plan(job)
    full = str(job.job_id)
    calls, run = _recording_runner()
    for spelling in (full, full[:8]):
        assert _post(f"/api/v1/jobs/{spelling}/decisions/d1", {}, run)[0] == 200
    assert [key for key, _argv in calls] == [full, full]
    assert [argv[-2] for _key, argv in calls] == [full, full[:8]]


def test_a_path_value_that_decodes_to_a_slash_or_a_nul_is_400_and_runs_nothing():
    """R-1195: `decision resolve` builds a file name from its job value, and a child's arguments
    cannot hold a NUL, so a value holding either never reaches the command."""
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    hand_written = " ".join(page[:page.index(public_api.PUBLIC_API_PAGE_BEGIN)].split())
    assert "holds `/` or a NUL character once decoded" in hand_written
    calls, run = _recording_runner()
    for path in ("/api/v1/jobs/..%2F..%2Fescape/decisions/sr:abc",
                 "/api/v1/jobs/j1/decisions/td%2Fabc",
                 "/api/v1/jobs/j1/decisions/td%00abc"):
        status, answer, _headers = _post(path, {}, run)
        assert (status, answer["error"]) == (400, "api_path_invalid"), path
    assert calls == []


# -- the write route that declines a result (S4b, DECISION F253 D11) -------------

DECLINE_PATH = "/api/v1/jobs/{job}/decline"


def test_the_decline_route_is_pinned_with_its_body_and_its_statuses():
    route = next(r for r in public_api.PUBLIC_API_ROUTES if r.path == DECLINE_PATH)
    assert (route.method, route.twin) == ("POST", "job.decline")
    assert route.body == (("reason", "string"),)
    assert route.refusal_default == 409
    assert route.refusals == (
        ("invalid_job_id", 404), ("job_not_found", 404), ("ambiguous_job_id", 400),
        ("missing_argument", 400),
    )
    assert "`api`" in route.description


@pytest.mark.parametrize("body, reason", [({"reason": "not wanted"}, "not wanted"), ({}, "")])
def test_a_decline_post_runs_the_command_with_its_reason_and_the_api_door(body, reason):
    calls, run = _recording_runner()
    status, _answer, _headers = _post("/api/v1/jobs/j1/decline", body, run)
    assert status == 200
    assert calls == [("j1", ["job", "decline", f"--reason={reason}", "--source=api", "--json",
                             "--", "j1"])]


def test_a_decline_post_refuses_a_key_the_route_does_not_take():
    calls, run = _recording_runner()
    status, answer, _headers = _post("/api/v1/jobs/j1/decline", {"answer": ["x"]}, run)
    assert (status, answer["error"]) == (400, "api_body_invalid")
    assert calls == []


def test_every_route_declares_only_refusals_its_twin_answers():
    """A route's `refusals` are tokens its twin command really refuses with, as the machine
    client interface lists them (DECISION F298 D4), so no status is declared for a token that
    cannot arrive."""
    from apps.cli.client_interface import OPERATION_REFUSAL_TOKENS

    stray = {route.path: sorted({token for token, _status in route.refusals}
                                - set(OPERATION_REFUSAL_TOKENS[route.twin]))
             for route in public_api.PUBLIC_API_ROUTES}
    assert {path: tokens for path, tokens in stray.items() if tokens} == {}


# -- the write route that approves an apply (S4c, DECISION F253 D12) -------------

APPLY_PATH = "/api/v1/jobs/{job}/apply"


def _saved_job_in(repo_path: str) -> str:
    """The full id of a saved job whose record names REPO_PATH as its repository."""
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

    job = JobPlan(job_title="apply-route-job", user_prompt="Apply route prompt",
                  tasks=[TaskEntry(title="Write a page")], repo_path=repo_path)
    save_job_plan(job)
    return str(job.job_id)


def test_the_apply_route_is_pinned_with_its_body_and_its_statuses():
    route = next(r for r in public_api.PUBLIC_API_ROUTES if r.path == APPLY_PATH)
    assert (route.method, route.twin) == ("POST", "job.apply")
    assert route.body == (("commit", "string"), ("commit_auto", "flag"),
                          ("commit_with_history", "flag"), ("push", "flag"),
                          ("skip_blocked", "flag"))
    assert route.refusal_default == 409
    assert route.refusals == (("job_not_found", 404), ("invalid_argument", 400))
    assert "`--test-command`" in route.description and "not offered" in route.description


def test_an_apply_post_applies_to_the_jobs_own_repository_by_its_full_id(tmp_path):
    full = _saved_job_in(str(tmp_path))
    calls, run = _recording_runner()
    status, _answer, _headers = _post(
        f"/api/v1/jobs/{full[:8]}/apply", {"commit": "Land it", "push": True, "skip_blocked": False},
        run)
    assert status == 200
    assert calls == [(full, ["job", "apply", "--approve", f"--repo={tmp_path}", "--commit=Land it",
                             "--push", "--json", "--", full])]


@pytest.mark.parametrize("flag", ["commit_auto", "commit_with_history", "push", "skip_blocked"])
def test_each_apply_flag_set_true_passes_its_option(tmp_path, flag):
    full = _saved_job_in(str(tmp_path))
    calls, run = _recording_runner()
    assert _post(f"/api/v1/jobs/{full}/apply", {flag: True}, run)[0] == 200
    assert calls == [(full, ["job", "apply", "--approve", f"--repo={tmp_path}",
                             "--" + flag.replace("_", "-"), "--json", "--", full])]


def test_an_apply_post_for_no_known_job_runs_the_command_without_a_repository():
    """The command refuses the value `job_not_found` before it touches any repository."""
    calls, run = _recording_runner()
    assert _post("/api/v1/jobs/0123abcd/apply", {}, run)[0] == 200
    assert calls == [("0123abcd", ["job", "apply", "--approve", "--json", "--", "0123abcd"])]


def test_an_apply_post_for_a_job_without_a_repository_is_409_and_runs_nothing():
    """Without a repository on the record, `--repo` would mean the supervisor's own folder."""
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    assert "`api_job_repository_unknown`" in page[:page.index(public_api.PUBLIC_API_PAGE_BEGIN)]
    full = _saved_job_in("")
    calls, run = _recording_runner()
    status, answer, _headers = _post(f"/api/v1/jobs/{full}/apply", {"commit_auto": True}, run)
    assert (status, answer["error"]) == (409, "api_job_repository_unknown")
    assert full in answer["message"]
    assert calls == []


def test_an_apply_post_refuses_a_key_or_a_kind_the_route_does_not_take(tmp_path):
    full = _saved_job_in(str(tmp_path))
    calls, run = _recording_runner()
    for body in ({"push": "true"}, {"push": 1}, {"test_command": "true"}, {"repo": str(tmp_path)},
                 {"dry_run": True}):
        status, answer, _headers = _post(f"/api/v1/jobs/{full}/apply", body, run)
        assert (status, answer["error"]) == (400, "api_body_invalid"), body
    assert calls == []


# -- the route that polls an order (S5b, DECISION F253 D14) ---------------------

ORDER_POLL_PATH = "/api/v1/orders/{order}"


def _order_command_answer(order_id: str, *, ok: bool = True) -> dict:
    """`remedy client order <order_id> --json`'s real standard output, as a subprocess, parsed.

    A refusal exits nonzero but still prints the envelope to stdout
    (`apps.cli.json_envelope.fail`), so `ok` only selects which exit this call expects.
    """
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "client", "order", order_id, "--json"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=30,
    )
    if ok:
        assert result.returncode == 0, result.stderr
    else:
        assert result.returncode != 0, result.stderr
    return json.loads(result.stdout)


def test_the_order_poll_route_is_pinned_with_its_statuses():
    route = next(r for r in public_api.PUBLIC_API_ROUTES if r.path == ORDER_POLL_PATH)
    assert (route.method, route.twin) == ("GET", "client.order")
    assert route.refusals == (("order_not_found", 404),)
    assert public_api.PUBLIC_API_VERSION == "1.7"


def test_the_order_poll_route_answers_as_the_client_order_command_does(tcp_server):
    from tests.cli.test_client_order_cmd import _start_ended_order

    data_root = Path(os.environ["REMEDY_DATA_DIR"])
    order_id = _start_ended_order(data_root)

    status, body, _headers = _tcp_request(
        tcp_server, "GET", f"/api/v1/orders/{order_id}", headers=_bearer(SERVER_TOKEN))
    assert status == 200, body
    assert body == _order_command_answer(order_id)


def test_the_order_poll_route_refuses_an_unknown_well_formed_id(tcp_server):
    unknown = "0123456789abcdef"
    status, body, _headers = _tcp_request(
        tcp_server, "GET", f"/api/v1/orders/{unknown}", headers=_bearer(SERVER_TOKEN))
    assert status == 404, body
    assert body == _order_command_answer(unknown, ok=False)


def test_the_order_poll_route_rejects_a_path_shaped_id(tcp_server):
    """R-1198's own guard, read through the route: `../x` must never be read as a path."""
    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/orders/..%2Fx", headers=_bearer(SERVER_TOKEN))
    assert status == 404, body
    assert body["error"] == "order_not_found"
