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
from packages.orchestration import serve_runs as SR
from packages.orchestration.serve_daemon import UnixHTTPConnection, socket_handler_class
from packages.orchestration.serve_paths import serve_paths
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
    ("POST", "/api/v1/orders"):
        "test_the_order_create_route_is_pinned_with_its_body_and_its_statuses",
    ("GET", "/api/v1/jobs/{job}/run"):
        "test_the_run_poll_route_is_pinned_with_its_statuses",
    ("POST", "/api/v1/jobs/{job}/run"):
        "test_the_run_route_is_pinned_with_its_body_and_its_statuses",
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
                   headers: dict[str, str] | None = None,
                   body: bytes | None = None) -> tuple[int, dict, dict[str, str]]:
    conn = UnixHTTPConnection(sock_path, timeout=10)
    try:
        conn.request(method, path, body=body, headers=headers or {})
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
        assert (route.refusal_default is not None) == (
            route.method == "POST" and not (route.starts_order or route.starts_run))
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
            # A `starts_order` route's body maps to `remedy do run`'s own flags, not its twin
            # `client.order`'s (which takes none): checked by its own dedicated test instead.
            if route.starts_order:
                continue
            if kind == "flag":
                assert "--" + key.replace("_", "-") in flag_options, (route.path, key)
            else:
                assert "--" + key.replace("_", "-") in value_options, (route.path, key)
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
        assert list(record.keys()) == ["ts", "token_fp", "client", "method", "path", "status",
                                       "error"]
        assert record["method"] == "GET"
        assert record["client"] == ""

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
    assert public_api.PUBLIC_API_VERSION == "1.10"


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
    assert public_api.PUBLIC_API_VERSION == "1.10"


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


# -- the write route that creates and starts an order (S5b, DECISION F253 D14) --

ORDER_CREATE_PATH = "/api/v1/orders"


def _registered_project_slug(tmp_path: Path) -> str:
    """The slug of a project registered on the active data root, backed by a fresh git repo."""
    from packages.orchestration.project_registry import register_project_repo

    repo = tmp_path / "order-route-repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    return register_project_repo("order-route-repo", repo).slug


@pytest.fixture
def registered_project_slug(tmp_path):
    return _registered_project_slug(tmp_path)


def _order_text(slug: str) -> str:
    return f"---\nproject: {slug}\nmax-cost-usd: 1\n---\nAdd a line saying hello to README.md\n"


def _fixture_order_record(**overrides) -> SR.OrderRecord:
    """An `OrderRecord` whose `ended_at` is already set, so `order_state` never touches `/proc`
    at all — the mocked tests below only need a deterministic answer, not a live process."""
    base = dict(
        order_id="abc0123456789def", pid=1, started_at="2026-01-01T00:00:00Z",
        order_file="/data/orders/abc0123456789def/order.md",
        out_log="/data/orders/abc0123456789def/out.log",
        err_log="/data/orders/abc0123456789def/err.log",
        exit_code=None, ended_at="2026-01-01T00:00:05Z")
    base.update(overrides)
    return SR.OrderRecord(**base)


def _recording_order_starter(record: SR.OrderRecord):
    """A stand-in order starter that records `(order_text, options)` and returns RECORD."""
    calls: list[tuple[str, list[str]]] = []

    def start(order_text: str, options: list[str]):
        calls.append((order_text, list(options)))
        return record

    return calls, start


def _post_order(body: object, start) -> tuple[int, dict, dict[str, str]]:
    raw = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
    _run_calls, run = _recording_runner()
    return public_api.answer_public_api_post(ORDER_CREATE_PATH, raw, run, start)


def test_the_order_create_route_is_pinned_with_its_body_and_its_statuses():
    route = next(r for r in public_api.PUBLIC_API_ROUTES if r.path == ORDER_CREATE_PATH)
    assert (route.method, route.twin) == ("POST", "client.order")
    assert route.body == (
        ("order", "string"), ("no_llm", "flag"), ("new_mission", "flag"),
        ("force_job", "flag"), ("force_mission", "flag"), ("builder_provider", "string"),
        ("reviewer_provider", "string"), ("deadline", "string"))
    assert route.refusals == ()
    assert route.refusal_default is None
    assert route.starts_order is True
    assert "`api_order_project_unknown`" in route.description


def test_the_order_create_routes_body_matches_do_runs_own_flags():
    """`route.body`'s twin is `client.order`, which takes none of these; its flags and strings
    are checked against `do.run`'s own instead (DECISION F253 D14 (1))."""
    from apps.cli.command_catalog import get_command

    do_run = get_command("do.run")
    flag_options = {a.name for a in do_run.args if a.is_option and a.is_flag}
    value_options = {a.name for a in do_run.args if a.is_option and not a.is_flag}
    route = next(r for r in public_api.PUBLIC_API_ROUTES if r.path == ORDER_CREATE_PATH)
    for key, kind in route.body:
        if key == "order":
            continue
        if kind == "flag":
            assert "--" + key.replace("_", "-") in flag_options, key
        else:
            assert "--" + key.replace("_", "-") in value_options, key


@pytest.mark.parametrize("flag", ["no_llm", "new_mission", "force_job", "force_mission"])
def test_each_order_create_flag_set_true_passes_its_option(registered_project_slug, flag):
    text = _order_text(registered_project_slug)
    calls, start = _recording_order_starter(_fixture_order_record())
    status, _body, _headers = _post_order({"order": text, flag: True}, start)
    assert status == 202
    assert calls == [(text, ["--" + flag.replace("_", "-")])]


@pytest.mark.parametrize("flag", ["no_llm", "new_mission", "force_job", "force_mission"])
def test_each_order_create_flag_set_false_passes_nothing(registered_project_slug, flag):
    text = _order_text(registered_project_slug)
    calls, start = _recording_order_starter(_fixture_order_record())
    status, _body, _headers = _post_order({"order": text, flag: False}, start)
    assert status == 202
    assert calls == [(text, [])]


@pytest.mark.parametrize("key, flag_name", [
    ("builder_provider", "--builder-provider"),
    ("reviewer_provider", "--reviewer-provider"),
    ("deadline", "--deadline"),
])
def test_each_order_create_string_passes_its_value(registered_project_slug, key, flag_name):
    text = _order_text(registered_project_slug)
    calls, start = _recording_order_starter(_fixture_order_record())
    status, _body, _headers = _post_order({"order": text, key: "value-x"}, start)
    assert status == 202
    assert calls == [(text, [f"{flag_name}=value-x"])]


def test_an_order_create_post_sends_the_order_text_to_the_starter_byte_for_byte(
        registered_project_slug):
    text = (f"---\nproject: {registered_project_slug}\nmax-cost-usd: 1\n---\n"
           "Unicode: café ☃, and a trailing blank line.\n\n")
    calls, start = _recording_order_starter(_fixture_order_record())
    status, _body, _headers = _post_order({"order": text}, start)
    assert status == 202
    assert calls == [(text, [])]


def test_an_order_create_post_answers_202_with_the_starters_record(
        tmp_path, registered_project_slug):
    out_log = tmp_path / "out.log"
    out_log.write_text('{"ok": true, "mission_id": "m-fixture"}\n', encoding="utf-8")
    record = _fixture_order_record(
        out_log=str(out_log), order_file=str(tmp_path / "order.md"), exit_code=0)
    calls, start = _recording_order_starter(record)
    text = _order_text(registered_project_slug)

    status, body, _headers = _post_order({"order": text}, start)

    assert status == 202, body
    assert body == {
        "schema_version": 1, "ok": True,
        "order_id": record.order_id, "state": "ended",
        "started_at": record.started_at, "ended_at": record.ended_at,
        "exit_code": record.exit_code, "order_file": record.order_file,
        "answer": {"ok": True, "mission_id": "m-fixture"},
    }
    assert calls == [(text, [])]


def test_an_order_create_post_without_the_order_key_is_400_and_starts_nothing():
    calls, start = _recording_order_starter(_fixture_order_record())
    status, answer, _headers = _post_order({}, start)
    assert (status, answer["error"]) == (400, "api_body_invalid")
    assert calls == []


def test_an_order_create_post_with_a_broken_header_is_400_and_starts_nothing():
    calls, start = _recording_order_starter(_fixture_order_record())
    body = {"order": "---\nnot a valid line\n---\nDo it\n"}
    status, answer, _headers = _post_order(body, start)
    assert (status, answer["error"]) == (400, "order_file_invalid_header")
    assert calls == []


def test_an_order_create_post_with_an_empty_order_is_400_and_starts_nothing():
    calls, start = _recording_order_starter(_fixture_order_record())
    status, answer, _headers = _post_order({"order": "---\n---\n   \n"}, start)
    assert (status, answer["error"]) == (400, "order_file_empty")
    assert calls == []


def test_an_order_create_post_whose_header_names_no_project_is_409_and_starts_nothing():
    calls, start = _recording_order_starter(_fixture_order_record())
    body = {"order": "---\nmax-cost-usd: 1\n---\nDo it\n"}
    status, answer, _headers = _post_order(body, start)
    assert (status, answer["error"]) == (409, "api_order_project_unknown")
    assert calls == []


def test_an_order_create_post_whose_project_is_not_registered_is_409_and_starts_nothing():
    calls, start = _recording_order_starter(_fixture_order_record())
    body = {"order": "---\nproject: no-such-project-xyz\n---\nDo it\n"}
    status, answer, _headers = _post_order(body, start)
    assert (status, answer["error"]) == (409, "api_order_project_unknown")
    assert calls == []


def test_an_order_create_post_whose_header_names_no_project_is_refused_with_remedy_project_set(
        monkeypatch, registered_project_slug):
    """R-1202: `_order_text_and_options` refuses an order whose header names no project before
    `select_project` is ever consulted. With `REMEDY_PROJECT` naming a registered project, a
    fall-through to `select_project`'s own environment fallback would otherwise accept such an
    order; this test fails if that fall-through replaces the explicit refusal."""
    monkeypatch.setenv("REMEDY_PROJECT", registered_project_slug)
    calls, start = _recording_order_starter(_fixture_order_record())
    body = {"order": "---\nmax-cost-usd: 1\n---\nDo it\n"}
    status, answer, _headers = _post_order(body, start)
    assert (status, answer["error"]) == (409, "api_order_project_unknown")
    assert calls == []


def test_an_order_create_post_whose_starter_raises_oserror_is_500_and_starts_nothing(
        registered_project_slug):
    """R-1201: an `OSError` from the order starter (the child could not be started) is answered
    500 `api_command_failed` rather than left to propagate unanswered and unledgered."""
    def start(order_text: str, options: list[str]):
        raise OSError("cannot start")

    text = _order_text(registered_project_slug)
    status, answer, _headers = _post_order({"order": text}, start)
    assert (status, answer["error"]) == (500, "api_command_failed")


def test_an_order_create_post_through_the_socket_handler_when_the_child_cannot_start(
        tmp_path, registered_project_slug):
    """R-1201: through a real handler made by `socket_handler_class` holding an `OrderLauncher`
    whose child cannot start, `POST /api/v1/orders` answers 500 `api_command_failed`, the call
    ledger holds one line for it with that status and token, and `orders_dir` is left holding
    no folder."""
    import socketserver

    from packages.orchestration.serve_paths import serve_paths

    paths = serve_paths()
    launcher = SR.OrderLauncher(paths, argv_prefix=[str(tmp_path / "no-such-program")])

    class _Server(socketserver.ThreadingUnixStreamServer):
        daemon_threads = True

    sock_path = tmp_path / "order-500.sock"
    server = _Server(str(sock_path), socket_handler_class(
        SERVER_TOKEN, runner=SR.CommandRunner(paths), orders=launcher))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        text = _order_text(registered_project_slug)
        status, body, _headers = _unix_request(
            sock_path, "POST", ORDER_CREATE_PATH, headers=_bearer(SERVER_TOKEN),
            body=json.dumps({"order": text}).encode("utf-8"))
    finally:
        server.shutdown()
        thread.join(10)
        server.server_close()

    assert (status, body["error"]) == (500, "api_command_failed")
    ledger_path = Path(os.environ["REMEDY_DATA_DIR"]) / "api" / "calls.jsonl"
    records = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines()]
    matches = [r for r in records if r["path"] == ORDER_CREATE_PATH]
    assert len(matches) == 1
    assert matches[0]["status"] == 500
    assert matches[0]["token_fp"] == token_fingerprint(SERVER_TOKEN)
    assert list(paths.orders_dir.glob("*")) == []


def test_an_order_create_post_with_no_starter_is_405():
    _calls, run = _recording_runner()
    status, answer, _headers = public_api.answer_public_api_post(ORDER_CREATE_PATH, b"{}", run)
    assert (status, answer["error"]) == (405, "api_method_not_allowed")


def test_the_page_states_the_order_create_refusal_tokens():
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    hand_written = page[:page.index(public_api.PUBLIC_API_PAGE_BEGIN)]
    for token in ("api_order_project_unknown", "order_file_invalid_header", "order_file_empty"):
        assert token in hand_written, token


# -- client tokens and their policy (S6b-1, DECISION F253 D16) -------------------

CLIENT_TOKEN = "client-token-of-the-nightly-bot-0123456789"


def _client_entry(**changes) -> dict:
    entry = {"name": "nightly-bot", "token": CLIENT_TOKEN, "projects": [],
             "max_total_tokens": None, "max_provider_calls": None, "may_apply": False}
    entry.update(changes)
    return entry


def _write_clients(entries: list[dict], mode: int = 0o600) -> Path:
    """Write the operator's clients file under the scratch data root, at MODE."""
    from packages.orchestration.api_clients import api_clients_path

    path = api_clients_path()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    path.write_text(json.dumps({"clients": entries}), encoding="utf-8")
    os.chmod(path, mode)
    return path


def _ledger_records() -> list[dict]:
    ledger_path = Path(os.environ["REMEDY_DATA_DIR"]) / "api" / "calls.jsonl"
    return [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines()]


def test_a_client_token_reads_a_route_like_the_servers_token_and_the_ledger_names_it(tcp_server):
    _write_clients([_client_entry()])
    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/interface", headers=_bearer(CLIENT_TOKEN))
    assert status == 200, body
    server_status, server_body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/interface", headers=_bearer(SERVER_TOKEN))
    assert server_status == 200
    assert body == server_body
    records = _ledger_records()
    assert [r["client"] for r in records] == ["nightly-bot", ""]
    assert records[0]["token_fp"] == token_fingerprint(CLIENT_TOKEN)
    assert CLIENT_TOKEN not in json.dumps(records)


def test_a_client_token_is_refused_by_the_cockpits_other_doors(tcp_server):
    from packages.orchestration.ui_server import COMMAND_CSRF_HEADER

    _write_clients([_client_entry()])
    status, _body, _headers = _tcp_request(tcp_server, "GET", f"/api/state?token={CLIENT_TOKEN}")
    assert status == 403
    status, _body, _headers = _tcp_request(
        tcp_server, "POST", "/api/jobs/any-job/commands",
        headers={**_bearer(CLIENT_TOKEN), COMMAND_CSRF_HEADER: CLIENT_TOKEN})
    assert status == 403


@pytest.mark.parametrize("change", ["mode", "removed"])
def test_a_client_token_stops_working_at_the_very_next_call(tcp_server, change):
    path = _write_clients([_client_entry()])
    assert _tcp_request(tcp_server, "GET", "/api/v1/interface",
                        headers=_bearer(CLIENT_TOKEN))[0] == 200
    if change == "mode":
        os.chmod(path, 0o644)
    else:
        _write_clients([_client_entry(name="other-bot", token="other-token-" + "x" * 30)])
    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/interface", headers=_bearer(CLIENT_TOKEN))
    assert (status, body["error"]) == (401, "api_token_invalid")
    assert _tcp_request(tcp_server, "GET", "/api/v1/interface",
                        headers=_bearer(SERVER_TOKEN))[0] == 200
    assert _ledger_records()[-2]["client"] == ""


def _registered_project(tmp_path: Path):
    from packages.orchestration.project_registry import register_project_repo

    repo = tmp_path / "client-route-repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    return register_project_repo("client-route-repo", repo)


def _client_order(project, **ceilings) -> str:
    header = "".join(f"{key}: {value}\n" for key, value in ceilings.items())
    return f"---\nproject: {project.slug}\n{header}---\nAdd a line saying hello to README.md\n"


def _client_policy(**changes):
    from packages.orchestration.api_clients import ApiClient

    fields = {"name": "nightly-bot", "token": CLIENT_TOKEN, "projects": (),
              "max_total_tokens": None, "max_provider_calls": None, "may_apply": False}
    fields.update(changes)
    return ApiClient(**fields)


def _saved_job_of_project(project_id: str, repo_path: str) -> str:
    """The full id of a saved job whose record names PROJECT_ID as its project."""
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

    job = JobPlan(job_title="client-policy-job", user_prompt="Client policy prompt",
                  tasks=[TaskEntry(title="Write a page")], repo_path=repo_path,
                  project_id=project_id)
    save_job_plan(job)
    return str(job.job_id)


def _post_order_as(client, text: str, start):
    _run_calls, run = _recording_runner()
    raw = json.dumps({"order": text}).encode("utf-8")
    return public_api.answer_public_api_post(ORDER_CREATE_PATH, raw, run, start, client=client)


def test_a_client_order_for_a_project_it_does_not_list_is_403_and_starts_nothing(tmp_path):
    project = _registered_project(tmp_path)
    calls, start = _recording_order_starter(_fixture_order_record())
    client = _client_policy(projects=("some-other-project",))
    status, answer, _headers = _post_order_as(client, _client_order(project), start)
    assert (status, answer["error"]) == (403, "api_client_policy_refused")
    assert "nightly-bot" in answer["message"] and answer["message"].endswith("; nothing was run")
    assert calls == []


def test_a_client_order_for_a_project_listed_by_slug_or_by_id_is_202(tmp_path):
    project = _registered_project(tmp_path)
    for listed in (project.slug, str(project.id)):
        calls, start = _recording_order_starter(_fixture_order_record())
        client = _client_policy(projects=(listed,))
        status, answer, _headers = _post_order_as(client, _client_order(project), start)
        assert status == 202, answer
        assert len(calls) == 1


@pytest.mark.parametrize("ceiling_key,header", [
    ("max_total_tokens", "max-total-tokens"), ("max_provider_calls", "max-provider-calls")])
def test_a_client_order_is_held_to_its_ceilings(tmp_path, ceiling_key, header):
    project = _registered_project(tmp_path)
    client = _client_policy(projects=(project.slug,), **{ceiling_key: 1000})
    for ceilings in ({}, {header: 1001}):
        calls, start = _recording_order_starter(_fixture_order_record())
        status, answer, _headers = _post_order_as(
            client, _client_order(project, **ceilings), start)
        assert (status, answer["error"]) == (403, "api_client_policy_refused"), ceilings
        assert header + ":" in answer["message"]
        assert calls == []
    calls, start = _recording_order_starter(_fixture_order_record())
    status, answer, _headers = _post_order_as(
        client, _client_order(project, **{header: 1000}), start)
    assert status == 202, answer
    assert len(calls) == 1


def test_a_client_apply_needs_its_may_apply(tmp_path):
    project = _registered_project(tmp_path)
    full = _saved_job_of_project(str(project.id), str(tmp_path))
    path = f"/api/v1/jobs/{full}/apply"
    calls, run = _recording_runner()
    status, answer, _headers = public_api.answer_public_api_post(
        path, b"{}", run, client=_client_policy(projects=(project.slug,), may_apply=False))
    assert (status, answer["error"]) == (403, "api_client_policy_refused")
    assert answer["message"].endswith("; nothing was run")
    assert calls == []
    status, _answer, _headers = public_api.answer_public_api_post(
        path, b"{}", run, client=_client_policy(projects=(project.slug,), may_apply=True))
    assert status == 200
    assert calls == [(full, ["job", "apply", "--approve", f"--repo={tmp_path}", "--json", "--",
                             full])]


def test_a_client_order_outside_its_projects_through_the_socket_handler_starts_nothing(
        tmp_path):
    """Through a real handler made by `socket_handler_class`: the client's order outside its
    projects is 403, the ledger holds one line for it naming the client, and no order starts."""
    import socketserver

    from packages.orchestration.serve_paths import serve_paths

    project = _registered_project(tmp_path)
    _write_clients([_client_entry(projects=["some-other-project"])])
    paths = serve_paths()
    launcher = SR.OrderLauncher(paths, argv_prefix=[str(tmp_path / "no-such-program")])

    class _Server(socketserver.ThreadingUnixStreamServer):
        daemon_threads = True

    sock_path = tmp_path / "client-403.sock"
    server = _Server(str(sock_path), socket_handler_class(
        SERVER_TOKEN, runner=SR.CommandRunner(paths), orders=launcher))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        status, body, _headers = _unix_request(
            sock_path, "POST", ORDER_CREATE_PATH, headers=_bearer(CLIENT_TOKEN),
            body=json.dumps({"order": _client_order(project)}).encode("utf-8"))
    finally:
        server.shutdown()
        thread.join(10)
        server.server_close()

    assert (status, body["error"]) == (403, "api_client_policy_refused")
    records = [r for r in _ledger_records() if r["path"] == ORDER_CREATE_PATH]
    assert len(records) == 1
    assert records[0]["status"] == 403
    assert records[0]["error"] == "api_client_policy_refused"
    assert records[0]["client"] == "nightly-bot"
    assert list(paths.orders_dir.glob("*")) == []


def test_the_page_states_the_clients_file_and_the_policy_refusal():
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    hand_written = page[:page.index(public_api.PUBLIC_API_PAGE_BEGIN)]
    token_section = hand_written[hand_written.index("## The token"):
                                 hand_written.index("## The envelope")]
    assert "clients.json" in token_section
    assert "api_client_policy_refused" in hand_written
    assert "Until the next slice" not in page
    assert "max_provider_calls" in hand_written


# -- a client token's jobs and budget answers (S6b-2, DECISION F253 D17) ---------

#: The three routes that act on one job: kind to path template and body.
_JOB_WRITES = {
    "decision": ("/api/v1/jobs/{job}/decisions/plan:x", {"reason": "approve"}),
    "decline": ("/api/v1/jobs/{job}/decline", {"reason": "not wanted"}),
    "apply": ("/api/v1/jobs/{job}/apply", {}),
}


def _client_job_write(kind: str, job: str, client):
    """Post the KIND write for JOB as CLIENT; the (status, answer) and the runner's calls."""
    template, body = _JOB_WRITES[kind]
    calls, run = _recording_runner()
    status, answer, _headers = public_api.answer_public_api_post(
        template.replace("{job}", job), json.dumps(body).encode("utf-8"), run, client=client)
    return status, answer, calls


@pytest.mark.parametrize("kind", sorted(_JOB_WRITES))
def test_a_client_write_for_a_job_of_another_project_is_403_and_runs_nothing(tmp_path, kind):
    project = _registered_project(tmp_path)
    full = _saved_job_of_project(str(project.id), str(tmp_path))
    client = _client_policy(projects=("some-other-project",), may_apply=True)
    status, answer, calls = _client_job_write(kind, full, client)
    assert (status, answer["error"]) == (403, "api_client_policy_refused")
    assert "nightly-bot" in answer["message"] and full in answer["message"]
    assert answer["message"].endswith("; nothing was run")
    assert calls == []


@pytest.mark.parametrize("kind", sorted(_JOB_WRITES))
def test_a_client_write_for_a_job_of_a_project_it_lists_by_slug_or_id_runs(tmp_path, kind):
    project = _registered_project(tmp_path)
    full = _saved_job_of_project(str(project.id), str(tmp_path))
    for listed in (project.slug, str(project.id)):
        client = _client_policy(projects=(listed,), may_apply=True)
        status, answer, calls = _client_job_write(kind, full, client)
        assert status == 200, answer
        assert len(calls) == 1


@pytest.mark.parametrize("kind", sorted(_JOB_WRITES))
def test_a_client_write_for_a_job_of_no_project_is_403_and_runs_nothing(tmp_path, kind):
    full = _saved_job_of_project("", str(tmp_path))
    client = _client_policy(projects=("demo",), may_apply=True)
    status, answer, calls = _client_job_write(kind, full, client)
    assert (status, answer["error"]) == (403, "api_client_policy_refused")
    assert calls == []


@pytest.mark.parametrize("kind", sorted(_JOB_WRITES))
def test_a_client_write_for_a_value_that_names_no_job_runs_the_command_as_before(kind):
    client = _client_policy(projects=("demo",), may_apply=True)
    status, _answer, calls = _client_job_write(kind, "0123abcd", client)
    assert status == 200
    assert len(calls) == 1


def _budget_answer_as(client, decision: str, job: str, answers: list[str]):
    calls, run = _recording_runner()
    raw = json.dumps({"reason": "extend", "answer": answers}).encode("utf-8")
    status, answer, _headers = public_api.answer_public_api_post(
        f"/api/v1/jobs/{job}/decisions/{decision}", raw, run, client=client)
    return status, answer, calls


@pytest.mark.parametrize("decision", ["budget:r1", "budget_exhausted"])
@pytest.mark.parametrize("limit,ceiling", [("max_total_tokens", 1000), ("max_provider_calls", 5)])
def test_a_client_budget_answer_above_its_ceiling_is_403_and_runs_nothing(
        tmp_path, decision, limit, ceiling):
    project = _registered_project(tmp_path)
    full = _saved_job_of_project(str(project.id), str(tmp_path))
    client = _client_policy(projects=(project.slug,), **{limit: ceiling})
    status, answer, calls = _budget_answer_as(client, decision, full, [f"{limit}={ceiling + 1}"])
    assert (status, answer["error"]) == (403, "api_client_policy_refused")
    assert limit in answer["message"] and answer["message"].endswith("; nothing was run")
    assert calls == []
    status, answer, calls = _budget_answer_as(client, decision, full, [f"{limit}={ceiling}"])
    assert status == 200, answer
    assert len(calls) == 1


def test_a_client_answer_of_a_decision_that_is_not_a_budget_decision_is_not_held_to_a_ceiling(
        tmp_path):
    project = _registered_project(tmp_path)
    full = _saved_job_of_project(str(project.id), str(tmp_path))
    client = _client_policy(projects=(project.slug,), max_total_tokens=1000)
    status, answer, calls = _budget_answer_as(client, "plan:x", full, ["max_total_tokens=5000"])
    assert status == 200, answer
    assert len(calls) == 1


def test_a_client_decline_of_a_job_of_another_project_through_the_socket_handler_runs_nothing(
        tmp_path):
    """Through a real handler made by `socket_handler_class`: the decline is 403, the ledger holds
    one line for it naming the client, and the runner never runs a command."""
    import socketserver

    project = _registered_project(tmp_path)
    full = _saved_job_of_project(str(project.id), str(tmp_path))
    _write_clients([_client_entry(projects=["some-other-project"])])
    ran: list[tuple[str, list[str]]] = []

    class _RecordingRunner:
        def run(self, job_id: str, argv: list[str]) -> dict | None:
            ran.append((job_id, argv))
            return _OK_ENVELOPE

    class _Server(socketserver.ThreadingUnixStreamServer):
        daemon_threads = True

    sock_path = tmp_path / "client-decline-403.sock"
    server = _Server(str(sock_path), socket_handler_class(
        SERVER_TOKEN, runner=_RecordingRunner()))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    path = f"/api/v1/jobs/{full}/decline"
    try:
        status, body, _headers = _unix_request(
            sock_path, "POST", path, headers=_bearer(CLIENT_TOKEN),
            body=json.dumps({"reason": "not wanted"}).encode("utf-8"))
    finally:
        server.shutdown()
        thread.join(10)
        server.server_close()

    assert (status, body["error"]) == (403, "api_client_policy_refused")
    records = [r for r in _ledger_records() if r["path"] == path]
    assert len(records) == 1
    assert records[0]["status"] == 403
    assert records[0]["error"] == "api_client_policy_refused"
    assert records[0]["client"] == "nightly-bot"
    assert ran == []


# -- a write on a job whose record cannot be read (R-1204) -----------------------


def _saved_job_with_unreadable_record(project_id: str, repo_path: str) -> str:
    """The full id of a saved job whose record's `tasks` was then rewritten to `5`, which parses
    as JSON into the wrong shape."""
    from packages.orchestration.data_paths import job_record_path

    full = _saved_job_of_project(project_id, repo_path)
    path = job_record_path(full)
    data = json.loads(path.read_text(encoding="utf-8"))
    data["tasks"] = 5
    path.write_text(json.dumps(data), encoding="utf-8")
    return full


def test_an_apply_post_for_a_job_whose_record_cannot_be_read_is_passed_on_as_sent(tmp_path):
    """R-1204: the record is passed on as a missing one is, with no `--repo`, and nothing raises."""
    full = _saved_job_with_unreadable_record("", str(tmp_path))
    calls, run = _recording_runner()
    status, _answer, _headers = _post(f"/api/v1/jobs/{full}/apply", {}, run)
    assert status == 200
    assert calls == [(full, ["job", "apply", "--approve", "--json", "--", full])]


@pytest.mark.parametrize("kind", sorted(_JOB_WRITES))
def test_a_client_write_for_a_job_whose_record_cannot_be_read_is_403_and_runs_nothing(
        tmp_path, kind):
    """R-1204: the unreadable record has no project keys, so no list of projects reaches it."""
    project = _registered_project(tmp_path)
    full = _saved_job_with_unreadable_record(str(project.id), str(tmp_path))
    client = _client_policy(
        projects=(project.slug, str(project.id), "demo", "some-other-project"), may_apply=True)
    status, answer, calls = _client_job_write(kind, full, client)
    assert (status, answer["error"]) == (403, "api_client_policy_refused")
    assert answer["message"].endswith("; nothing was run")
    assert calls == []


# -- the route that starts a job's run (S7a, DECISION F253 D18) ------------------

RUN_PATH = "/api/v1/jobs/{job}/run"


def _run_record(job_id: str) -> SR.RunRecord:
    return SR.RunRecord(job_id=job_id, pid=4242, started_at="2026-01-01T00:00:00Z",
                        out_log="/data/serve/runs/out", err_log="/data/serve/runs/err")


def _recording_run_starter(outcome: object = None):
    """A stand-in run starter that records `(job, options)`; it returns the job's `RunRecord`,
    or raises OUTCOME when that is an exception."""
    calls: list[tuple[str, list[str]]] = []

    def start(job: str, options: list[str]):
        calls.append((job, list(options)))
        if isinstance(outcome, Exception):
            raise outcome
        return _run_record(job)

    return calls, start


def _post_run(job: str, body: object, start, client=None) -> tuple[int, dict, dict[str, str]]:
    raw = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
    _run_calls, run = _recording_runner()
    return public_api.answer_public_api_post(
        RUN_PATH.replace("{job}", job), raw, run, client=client, start_run=start)


def test_the_run_route_is_pinned_with_its_body_and_its_statuses():
    route = next(r for r in public_api.PUBLIC_API_ROUTES
                 if r.path == RUN_PATH and r.method == "POST")
    assert (route.method, route.twin) == ("POST", "job.run")
    assert route.body == (("builder_provider", "string"), ("reviewer_provider", "string"))
    assert route.refusals == ()
    assert route.refusal_default is None
    assert route.starts_run is True
    assert "job_already_running" in route.description


def test_a_run_post_starts_the_run_by_the_full_id_and_answers_202_with_its_record():
    full = _saved_job_in("")
    calls, start = _recording_run_starter()
    status, body, headers = _post_run(full, {}, start)
    assert (status, headers) == (202, {})
    # The stand-in record names a process no run of this job owns and a log that does not exist,
    # so the poll's two added keys read `lost` and no answer (DECISION F253 D20 (4)).
    assert body == {"schema_version": 1, "ok": True, **_run_record(full).to_json(),
                    "state": "lost", "answer": None}
    assert sorted(body) == sorted(
        ["schema_version", "ok", "job_id", "pid", "started_at", "out_log", "err_log",
         "exit_code", "ended_at", "state", "answer"])
    assert calls == [(full, [])]


def test_a_run_post_passes_the_builder_then_the_reviewer_provider():
    full = _saved_job_in("")
    calls, start = _recording_run_starter()
    body = {"reviewer_provider": "fake", "builder_provider": "fake"}
    assert _post_run(full, body, start)[0] == 202
    assert calls == [(full, ["--builder-provider=fake", "--reviewer-provider=fake"])]
    calls.clear()
    assert _post_run(full, {"reviewer_provider": "ollama"}, start)[0] == 202
    assert calls == [(full, ["--reviewer-provider=ollama"])]


def test_a_run_post_by_a_job_prefix_starts_the_full_id():
    full = _saved_job_in("")
    calls, start = _recording_run_starter()
    assert _post_run(full[:8], {}, start)[0] == 202
    assert calls == [(full, [])]


@pytest.mark.parametrize("value, status, token", [
    ("not-a-job", 404, "invalid_job_id"),
    (str(uuid4()), 404, "job_not_found"),
    ("0123abcd", 404, "job_not_found"),
])
def test_a_run_post_for_no_job_is_refused_and_starts_nothing(value, status, token):
    calls, start = _recording_run_starter()
    got, answer, _headers = _post_run(value, {}, start)
    assert (got, answer["ok"], answer["error"]) == (status, False, token)
    assert calls == []


def test_a_run_post_for_a_job_whose_record_cannot_be_read_is_404_and_starts_nothing(tmp_path):
    full = _saved_job_with_unreadable_record("", str(tmp_path))
    calls, start = _recording_run_starter()
    status, answer, _headers = _post_run(full, {}, start)
    assert (status, answer["error"]) == (404, "job_not_found")
    assert calls == []


def test_a_run_post_by_a_prefix_two_jobs_share_is_400_and_starts_nothing():
    first = _saved_job_in("")
    data_root = Path(os.environ["REMEDY_DATA_DIR"])
    twin = first[:-1] + ("0" if first[-1] != "0" else "1")
    shutil.copytree(data_root / "jobs" / first, data_root / "jobs" / twin)
    calls, start = _recording_run_starter()
    status, answer, _headers = _post_run(first[:8], {}, start)
    assert (status, answer["error"]) == (400, "ambiguous_job_id")
    assert sorted(answer["matches"]) == sorted([first, twin])
    assert calls == []


def test_a_run_post_whose_starter_refuses_is_409_with_the_starters_own_token():
    full = _saved_job_in("")
    calls, start = _recording_run_starter(
        SR.RunRefused("job_already_running", f"the serve supervisor is already running job {full}"))
    status, answer, _headers = _post_run(full, {}, start)
    assert (status, answer["error"]) == (409, "job_already_running")
    assert full in answer["message"]
    assert len(calls) == 1


def test_a_run_post_whose_starter_raises_oserror_is_500_api_command_failed():
    full = _saved_job_in("")
    calls, start = _recording_run_starter(OSError("cannot start"))
    status, answer, _headers = _post_run(full, {}, start)
    assert (status, answer["error"]) == (500, "api_command_failed")
    assert len(calls) == 1


def test_a_run_post_with_no_run_starter_is_405():
    full = _saved_job_in("")
    status, answer, _headers = _post_run(full, {}, None)
    assert (status, answer["error"]) == (405, "api_method_not_allowed")


@pytest.mark.parametrize("body", [
    {"max_total_tokens": 5}, {"test_command": "true"}, {"builder_provider": 3},
    {"reviewer_provider": ["fake"]}, b"not json", b"[]",
])
def test_a_run_post_body_that_is_not_the_routes_own_is_400_and_starts_nothing(body):
    full = _saved_job_in("")
    calls, start = _recording_run_starter()
    status, answer, _headers = _post_run(full, body, start)
    assert (status, answer["error"]) == (400, "api_body_invalid")
    assert calls == []


def test_a_clients_run_of_a_job_of_another_project_is_403_and_starts_nothing(tmp_path):
    project = _registered_project(tmp_path)
    full = _saved_job_of_project(str(project.id), str(tmp_path))
    calls, start = _recording_run_starter()
    status, answer, _headers = _post_run(
        full, {}, start, client=_client_policy(projects=("some-other-project",)))
    assert (status, answer["error"]) == (403, "api_client_policy_refused")
    assert answer["message"].endswith("; nothing was run")
    assert calls == []
    status, _answer, _headers = _post_run(
        full, {}, start, client=_client_policy(projects=(project.slug,)))
    assert status == 202
    assert calls == [(full, [])]


def test_the_cockpits_own_server_answers_a_run_post_405(tcp_server):
    status, body, _headers = _tcp_request(
        tcp_server, "POST", "/api/v1/jobs/j1/run", headers=_bearer(SERVER_TOKEN))
    assert (status, body["error"]) == (405, "api_method_not_allowed")


def test_the_page_names_the_run_route_and_its_running_refusal():
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    hand_written = page[:page.index(public_api.PUBLIC_API_PAGE_BEGIN)]
    assert "## Runs" in hand_written
    assert "/api/v1/jobs/{job}/run" in hand_written
    assert "job_already_running" in hand_written


# -- a body string that holds a NUL character (R-1205) ---------------------------


def _refused_for_the_key(status: int, answer: dict, key: str) -> None:
    assert (status, answer["error"]) == (400, "api_body_invalid")
    assert f"'{key}' must not hold a NUL character" in answer["message"]


def test_a_decision_post_whose_reason_or_answer_holds_a_nul_is_400_and_runs_nothing():
    calls, run = _recording_runner()
    status, answer, _headers = _post("/api/v1/jobs/j1/decisions/d1", {"reason": "a\u0000b"}, run)
    _refused_for_the_key(status, answer, "reason")
    status, answer, _headers = _post(
        "/api/v1/jobs/j1/decisions/d1", {"answer": ["fine", "a\u0000b"]}, run)
    _refused_for_the_key(status, answer, "answer")
    assert calls == []


def test_a_decline_post_whose_reason_holds_a_nul_is_400_and_runs_nothing():
    calls, run = _recording_runner()
    status, answer, _headers = _post(
        DECLINE_PATH.replace("{job}", "j1"), {"reason": "a\u0000b"}, run)
    _refused_for_the_key(status, answer, "reason")
    assert calls == []


def test_an_order_post_whose_deadline_holds_a_nul_is_400_and_starts_nothing(tmp_path):
    slug = _registered_project_slug(tmp_path)
    calls, start = _recording_order_starter(_fixture_order_record())
    status, answer, _headers = _post_order(
        {"order": _order_text(slug), "deadline": "x\u0000y"}, start)
    _refused_for_the_key(status, answer, "deadline")
    assert calls == []


def test_a_run_post_whose_builder_provider_holds_a_nul_is_400_and_starts_nothing():
    full = _saved_job_in("")
    calls, start = _recording_run_starter()
    status, answer, _headers = _post_run(full, {"builder_provider": "fa\u0000ke"}, start)
    _refused_for_the_key(status, answer, "builder_provider")
    assert calls == []


def test_the_rendering_of_the_run_route_names_the_runs_record_not_the_twins_command():
    rows = [line for line in public_api.render_public_api_markdown().splitlines()
            if line.startswith(f"| `POST` | `{RUN_PATH}` |")]
    assert len(rows) == 1
    assert "the run's record, as the supervisor's `RunLauncher` writes it" in rows[0]
    assert "remedy job run --json" not in rows[0]


# -- the read route that polls a run (R-1208, DECISION F253 D20) --


def _run_command_answer(job: str, *, ok: bool = True) -> dict:
    """`remedy client run <job> --json`'s real standard output, as a subprocess, parsed.

    A refusal exits nonzero but still prints the envelope to stdout, so `ok` only selects which
    exit this call expects.
    """
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "client", "run", job, "--json"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=30,
    )
    if ok:
        assert result.returncode == 0, result.stderr
    else:
        assert result.returncode != 0, result.stderr
    return json.loads(result.stdout)


def test_the_run_poll_route_is_pinned_with_its_statuses():
    route = next(r for r in public_api.PUBLIC_API_ROUTES
                 if r.path == RUN_PATH and r.method == "GET")
    assert (route.method, route.twin) == ("GET", "client.run")
    assert route.refusals == (("run_not_found", 404),)
    assert public_api.PUBLIC_API_VERSION == "1.10"


def test_the_run_poll_route_answers_as_the_client_run_command_does(tcp_server):
    from tests.cli.test_client_run_cmd import _start_ended_run

    data_root = Path(os.environ["REMEDY_DATA_DIR"])
    full = _saved_job_in("")
    _start_ended_run(data_root, full)

    status, body, _headers = _tcp_request(
        tcp_server, "GET", f"/api/v1/jobs/{full}/run", headers=_bearer(SERVER_TOKEN))
    assert status == 200, body
    assert body["state"] == "ended" and body["exit_code"] == 0
    assert body["answer"] == {"ok": True, "job_id": full, "stand_in": True}
    assert body == _run_command_answer(full)
    prefix_status, prefix_body, _headers = _tcp_request(
        tcp_server, "GET", f"/api/v1/jobs/{full[:8]}/run", headers=_bearer(SERVER_TOKEN))
    assert prefix_status == 200, prefix_body
    assert prefix_body == body


def test_the_run_poll_route_refuses_a_job_with_no_run_record(tcp_server):
    full = _saved_job_in("")
    status, body, _headers = _tcp_request(
        tcp_server, "GET", f"/api/v1/jobs/{full}/run", headers=_bearer(SERVER_TOKEN))
    assert status == 404, body
    assert body == _run_command_answer(full, ok=False)
    assert body["error"] == "run_not_found"


def test_the_run_poll_route_refuses_a_value_that_is_no_id(tcp_server):
    status, body, _headers = _tcp_request(
        tcp_server, "GET", "/api/v1/jobs/..%2Fx/run", headers=_bearer(SERVER_TOKEN))
    assert status == 404, body
    assert body["error"] == "run_not_found"


# -- the 202 answers equal what the commands that read what they start print (R-1212) --

#: A stand-in for `remedy do run` and for `remedy job run`: prints one envelope and exits 0.
_PRINTS_ONE_ENVELOPE = 'import json; print(json.dumps({"ok": True, "stand_in": "r1212"}))'


def test_the_order_create_202_answer_equals_what_client_order_prints(
        registered_project_slug):
    """R-1212: the route's 202 body is the envelope `remedy client order <order> --json` prints."""
    paths = serve_paths(Path(os.environ["REMEDY_DATA_DIR"]))
    launcher = SR.OrderLauncher(paths, argv_prefix=[sys.executable, "-c", _PRINTS_ONE_ENVELOPE])
    started = launcher.start("do a thing", [])
    assert launcher.wait(started.order_id, timeout=30) == 0
    record = SR.read_order_record(paths, started.order_id)
    assert record is not None and record.ended_at is not None

    calls, start = _recording_order_starter(record)
    status, body, _headers = _post_order({"order": _order_text(registered_project_slug)}, start)

    assert status == 202, body
    assert len(calls) == 1
    assert body["answer"] == {"ok": True, "stand_in": "r1212"}
    assert body == _order_command_answer(record.order_id)


def test_the_run_202_answer_equals_what_client_run_prints():
    """R-1212: the route's 202 body is the envelope `remedy client run <job> --json` prints."""
    job = _saved_job_in("")
    paths = serve_paths(Path(os.environ["REMEDY_DATA_DIR"]))
    launcher = SR.RunLauncher(
        paths, argv_for=lambda job_id: [sys.executable, "-c", _PRINTS_ONE_ENVELOPE, job_id])
    launcher.start(job)
    assert launcher.wait(job, timeout=30) == 0
    record = SR.read_run_record(paths, job)
    assert record is not None and record.ended_at is not None

    def start(job_id: str, options: list[str]):
        return record

    status, body, _headers = _post_run(job, {}, start)

    assert status == 202, body
    assert body["state"] == "ended"
    assert body["answer"] == {"ok": True, "stand_in": "r1212"}
    assert body == _run_command_answer(job)


# -- the page's section "A client's test" names what the gate test's fixture uses (R-1215) --

GATE_TEST_PATH = "tests/orchestration/test_public_api_gate_paths.py"


def test_the_clients_test_section_names_what_the_gate_tests_fixture_uses():
    page = (REPO_ROOT / public_api.PUBLIC_API_PAGE_PATH).read_text(encoding="utf-8")
    heading = "## A client's test"
    assert page.count(heading) == 1
    after = page[page.index(heading) + len(heading):]
    next_heading = after.find("\n## ")
    section = after if next_heading < 0 else after[:next_heading]
    # A line break inside a code span is a space for a reader of the page.
    section = " ".join(section.split())
    for needle in ("REMEDY_DATA_DIR", "REMEDY_SERVE_API_PORT", "remedy serve start --json",
                   "api_port", "serve/serve.token", "remedy project register --repo",
                   "remedy serve stop --json", GATE_TEST_PATH):
        assert needle in section, needle
    gate_source = (REPO_ROOT / GATE_TEST_PATH).read_text(encoding="utf-8")
    for needle in ("REMEDY_SERVE_API_PORT", '"serve", "start", "--json"', '"api_port"',
                   '"serve.token"', '"project", "register", "--repo"',
                   '"serve", "stop", "--json"'):
        assert needle in gate_source, needle
