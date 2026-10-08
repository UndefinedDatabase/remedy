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
        assert route.method == "GET"
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
