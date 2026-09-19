"""R-0411 / DECISION F082 D3 — the bench's own sample project, and the premises
b04 and b05 are written on, checked by BEHAVIOUR against the frozen fixture.

The gauntlet pins "the template holds what the orders name" the same way
(``test_gauntlet_orders.py::test_the_template_holds_what_the_orders_name``). An
order whose premise is false asks a mission to do what is already done, so a
fixture edit that breaks a premise must turn a test red, not only the digest.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from io import BytesIO
from types import ModuleType
from wsgiref.util import setup_testing_defaults

from packages.orchestration.bench_orders import default_bench_template_dir


def _api() -> ModuleType:
    """The fixture's service module, loaded by path so nothing joins sys.path."""
    path = default_bench_template_dir() / "benchproj" / "api.py"
    spec = importlib.util.spec_from_file_location("bench_fixture_api", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _request(app, method: str, path: str, body: bytes = b"") -> tuple[str, dict, bytes]:
    environ: dict = {"REQUEST_METHOD": method, "PATH_INFO": path,
                     "CONTENT_LENGTH": str(len(body)), "wsgi.input": BytesIO(body)}
    setup_testing_defaults(environ)
    seen: dict = {}

    def start_response(status, headers):
        seen["status"], seen["headers"] = status, dict(headers)

    data = b"".join(app(environ, start_response))
    return seen["status"], seen["headers"], data


def test_the_fixture_suite_is_green_and_self_sufficient() -> None:
    """A world whose own suite is red would make every DoD meaningless."""
    proc = subprocess.run([sys.executable, "-B", "-m", "pytest", "tests", "-q",
                           "-p", "no:cacheprovider"],
                          cwd=str(default_bench_template_dir()), capture_output=True,
                          text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                          timeout=120)
    assert proc.returncode == 0, proc.stdout[-2000:]


def test_b04_premise_the_service_has_no_create_endpoint_today() -> None:
    app = _api().make_app([{"id": 1, "name": "first"}])
    status, _, _ = _request(app, "POST", "/items", b'{"name": "third"}')
    assert status == "405 Method Not Allowed", (
        f"POST /items answered {status}: b04 asks for an endpoint that already exists")
    assert _request(app, "GET", "/items")[0] == "200 OK"


def test_b05_premise_the_widget_is_served_without_a_count_badge() -> None:
    app = _api().make_app()
    page_status, page_headers, page = _request(app, "GET", "/widget")
    script_status, _, script = _request(app, "GET", "/static/widget.js")
    assert (page_status, script_status) == ("200 OK", "200 OK"), (
        "b05's HTTP-level smoke has nothing to fetch")
    assert page_headers["Content-Type"].startswith("text/html")
    assert b'src="/static/widget.js"' in page and b"function renderItems" in script
    for served in (page, script):
        assert b"item-count" not in served and b"countLabel" not in served, (
            "b05 asks for a count badge the widget already has")
