"""A real mini-app covering the three core-path outcomes (F062 T002 fixture).

Stdlib only, loopback only. One app, three honest cases the smoke must tell
apart:

    /health   200, "ok"                  — readiness, and an OK path
    /orders   200, "orders: 2 open"      — an OK path carrying a content marker
    /broken   500, "internal error"      — responds, but NOT with an OK status
    /empty    200, "" (no marker)        — OK status, marker absent

Deliberately a REAL app rather than a mock of the harness: the point of the
smoke is that something actually answered.
"""
from __future__ import annotations

import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"

_ROUTES: dict[str, tuple[int, bytes]] = {
    "/health": (200, b"ok"),
    "/orders": (200, b"orders: 2 open"),
    "/broken": (500, b"internal error"),
    "/empty": (200, b""),
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler's spelling
        status, body = _ROUTES.get(self.path.split("?", 1)[0], (404, b"no such path"))
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stdout.write("paths-app: " + (fmt % args) + "\n")
        sys.stdout.flush()


def main() -> int:
    server = HTTPServer((HOST, int(os.environ.get("PORT", "0"))), Handler)
    sys.stdout.write(f"paths-app: listening on {HOST}:{server.server_port}\n")
    sys.stdout.flush()
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
