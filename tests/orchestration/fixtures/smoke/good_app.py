"""A real mini-app that starts cleanly (F062 T001 fixture).

Stdlib only, loopback only. It binds the port the runtime harness hands it in
``PORT`` and answers ``/health`` — the shape the smoke's ``app_starts`` check
probes. Deliberately a REAL app rather than a mock of the harness: the whole
point of the smoke is that something actually ran.
"""
from __future__ import annotations

import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"

#: The pure logic a unit test can assert without starting anything.
def greeting() -> str:
    return "remedy smoke fixture: ok"


_ROUTES: dict[str, tuple[int, bytes]] = {
    "/health": (200, b"ok"),
    "/": (200, greeting().encode()),
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
        sys.stdout.write("good-app: " + (fmt % args) + "\n")
        sys.stdout.flush()


def main() -> int:
    server = HTTPServer((HOST, int(os.environ.get("PORT", "0"))), Handler)
    sys.stdout.write(f"good-app: listening on {HOST}:{server.server_port}\n")
    sys.stdout.flush()
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
