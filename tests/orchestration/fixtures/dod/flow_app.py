"""A tiny harness-startable application, for proving runtime_flow checks (F061 T003).

Stdlib only, loopback only, no dependency of its own. It binds the port the
runtime harness hands it in ``PORT`` and answers three paths:

    /health   200, body "ok"          — the readiness path
    //status  200, body "ready: yes"  — something with text worth asserting on
    /broken   500, body "boom"        — a deliberate red for flow tests

``REMEDY_FLOW_APP_BREAK_HEALTH=1`` makes /health answer 500 instead, so a test
can prove the "never became ready" path without a second fixture app.
"""
from __future__ import annotations

import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"

_ROUTES: dict[str, tuple[int, bytes]] = {
    "/health": (200, b"ok"),
    "/status": (200, b"ready: yes"),
    "/broken": (500, b"boom"),
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler's spelling
        path = self.path.split("?", 1)[0]
        if path == "/health" and os.environ.get("REMEDY_FLOW_APP_BREAK_HEALTH"):
            status, body = 500, b"health is broken on purpose"
        else:
            status, body = _ROUTES.get(path, (404, b"no such path"))
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        """Requests go to stdout, which the flow runner captures as the app log."""
        sys.stdout.write("flow-app: " + (fmt % args) + "\n")
        sys.stdout.flush()


def main() -> int:
    port = int(os.environ.get("PORT", "0"))
    server = HTTPServer((HOST, port), Handler)
    sys.stdout.write(f"flow-app: listening on {HOST}:{server.server_port}\n")
    sys.stdout.flush()
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
