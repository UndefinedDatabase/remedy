"""The item service: a stdlib WSGI app over an in-memory store.

``make_app`` builds an app with its OWN store, so every test starts clean.
Every method but GET is answered 405.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from wsgiref.simple_server import make_server

WEB_DIR = Path(__file__).resolve().parent / "web"
STATIC = {"/widget": ("widget.html", "text/html; charset=utf-8"),
          "/static/widget.js": ("widget.js", "text/javascript; charset=utf-8")}


def _send(start_response, status: str, data: bytes, content_type: str) -> list[bytes]:
    start_response(status, [("Content-Type", content_type), ("Content-Length", str(len(data)))])
    return [data]


def make_app(items: list[dict] | None = None):
    store = {item["id"]: dict(item) for item in (items or [])}

    def app(environ, start_response):
        method, path = environ.get("REQUEST_METHOD", "GET"), environ.get("PATH_INFO", "/")
        status, body = "404 Not Found", {"error": "not found"}
        if method != "GET":
            status, body = "405 Method Not Allowed", {"error": "method not allowed"}
        elif path in STATIC:
            name, content_type = STATIC[path]
            return _send(start_response, "200 OK", (WEB_DIR / name).read_bytes(), content_type)
        elif path == "/health":
            status, body = "200 OK", {"status": "ok"}
        elif path == "/items":
            status, body = "200 OK", [store[key] for key in sorted(store)]
        elif path.startswith("/items/") and path[7:].isdigit() and int(path[7:]) in store:
            status, body = "200 OK", store[int(path[7:])]
        return _send(start_response, status, json.dumps(body).encode("utf-8"), "application/json")

    return app


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    make_server("127.0.0.1", port, make_app([{"id": 1, "name": "first"}])).serve_forever()
