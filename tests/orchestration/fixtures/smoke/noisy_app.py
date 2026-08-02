"""A real mini-app that starts, answers, and SCREAMS (F062 T003 fixture).

Everything works — it binds, it serves ``/health`` with 200 — but on the way up
it prints a traceback and an ERROR line. That is the case ``clean_console``
exists for: a product that looks green to every other check while its console
says something is badly wrong.

``REMEDY_NOISY_APP_QUIET=1`` makes it start silently, so one fixture covers the
clean and dirty cases without a second app.
"""
from __future__ import annotations

import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler's spelling
        body = b"ok"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stdout.write("noisy-app: " + (fmt % args) + "\n")
        sys.stdout.flush()


def main() -> int:
    if not os.environ.get("REMEDY_NOISY_APP_QUIET"):
        sys.stdout.write(
            "Traceback (most recent call last):\n"
            '  File "cache.py", line 12, in warm\n'
            "    raise RuntimeError('cache warm failed')\n"
            "RuntimeError: cache warm failed\n"
            "ERROR could not warm the cache; serving cold\n")
        sys.stdout.flush()
    server = HTTPServer((HOST, int(os.environ.get("PORT", "0"))), Handler)
    sys.stdout.write(f"noisy-app: listening on {HOST}:{server.server_port}\n")
    sys.stdout.flush()
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
