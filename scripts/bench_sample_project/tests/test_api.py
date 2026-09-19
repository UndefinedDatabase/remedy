"""The service, driven through WSGI directly — no socket, no server."""
import json
from io import BytesIO
from wsgiref.util import setup_testing_defaults

from benchproj.api import make_app

SEED = [{"id": 1, "name": "first"}, {"id": 2, "name": "second"}]


def request(app, method: str, path: str, body: bytes = b""):
    environ = {"REQUEST_METHOD": method, "PATH_INFO": path, "wsgi.input": BytesIO(body)}
    setup_testing_defaults(environ)
    seen = {}
    data = b"".join(app(environ, lambda status, headers: seen.update(status=status, headers=dict(headers))))
    return seen["status"], seen["headers"], data


def test_health_list_fetch_and_missing():
    app = make_app(list(reversed(SEED)))
    assert json.loads(request(app, "GET", "/health")[2]) == {"status": "ok"}
    assert json.loads(request(app, "GET", "/items")[2]) == SEED
    assert json.loads(request(app, "GET", "/items/2")[2]) == SEED[1]
    assert request(app, "GET", "/items/9")[0] == "404 Not Found"


def test_a_write_is_refused():
    assert request(make_app(), "DELETE", "/items/1")[0] == "405 Method Not Allowed"


def test_the_widget_page_and_its_script_are_served():
    status, headers, page = request(make_app(), "GET", "/widget")
    assert status == "200 OK" and headers["Content-Type"].startswith("text/html")
    assert b'<ul id="items">' in page and b'src="/static/widget.js"' in page
    status, headers, script = request(make_app(), "GET", "/static/widget.js")
    assert status == "200 OK" and headers["Content-Type"].startswith("text/javascript")
    assert b"function renderItems" in script
