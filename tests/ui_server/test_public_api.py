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
import subprocess
import sys
import threading
from dataclasses import replace
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from packages.orchestration import public_api
from packages.orchestration.serve_daemon import UnixHTTPConnection, socket_handler_class
from packages.orchestration.ui_server import _RemedyHandler

REPO_ROOT = Path(__file__).resolve().parents[2]
SERVER_TOKEN = "f253-public-api-test-token"

#: `(method, path)` of every published route to the name of the test that pins it. A test that
#: the registry's own `(method, path)` set equals this dict's keys, and that every name here
#: exists in this module, makes an unpinned route fail the suite.
PINNED_ROUTES: dict[tuple[str, str], str] = {
    ("GET", "/api/v1/interface"): "test_interface_route_answers_the_command_envelope",
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
    from apps.cli.client_interface import CLIENT_OPERATION_IDS
    from apps.cli.command_catalog import get_command

    for route in public_api.PUBLIC_API_ROUTES:
        assert route.path.startswith(public_api.PUBLIC_API_PREFIX + "/")
        assert route.method == "GET"
        get_command(route.twin)  # raises KeyError if not a catalog command
        assert route.twin in CLIENT_OPERATION_IDS
        assert not public_api.command_is_excluded(route.twin)
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
