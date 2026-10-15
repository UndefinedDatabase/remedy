"""Hosting the one write door for a test, now that the cockpit's own server is gone
(DECISION amend1015f D27).

`POST /api/jobs/<id>/commands` is answered by `serve_daemon.socket_handler_class`, the handler
the `remedy serve start` supervisor binds to its unix socket. Two hosts are offered:

- `start_door_for_job` binds that very handler class to a loopback TCP port in a daemon thread,
  so a test keeps posting with `http.client.HTTPConnection("127.0.0.1", port)` exactly as it did
  against the cockpit. Every check of the door (token, CSRF header, nonce replay, rate limit,
  audit line) is the socket's own; the effect is recorded with the socket's source.
- `SupervisorThread` runs the real supervisor (`serve_daemon.run_supervisor`) on its real unix
  socket in a thread of the test process, for a test that drives a command line which finds the
  supervisor by itself. Its data root must be short (`serve_paths.socket_path_problem`).
"""
from __future__ import annotations

import secrets
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

from packages.orchestration import serve_daemon as SD


def start_door_for_job(job_id: str, tmp_path: Path | None = None) -> tuple[int, str]:
    """Serve the write door on 127.0.0.1 at a free port; (port, token).

    JOB_ID and TMP_PATH are accepted so the callers written for the cockpit's start keep their
    shape; the socket's handler serves every job of the data root, as the supervisor does.
    """
    del job_id, tmp_path
    token = secrets.token_urlsafe(16)
    server = ThreadingHTTPServer(("127.0.0.1", 0), SD.socket_handler_class(token))
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return int(server.server_address[1]), token


class SupervisorThread:
    """A real `remedy serve start` supervisor for ROOT, running until `close`."""

    def __init__(self, root: Path) -> None:
        self.stop = threading.Event()
        self.ready = threading.Event()
        self.errors: list[Exception] = []

        def run() -> None:
            try:
                SD.run_supervisor(root, stop=self.stop, on_ready=lambda _s: self.ready.set(),
                                  api_port=None)
            except (SD.ServeError, OSError) as exc:
                self.errors.append(exc)
                self.ready.set()

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
        assert self.ready.wait(10), "the supervisor never became ready"
        assert not self.errors, self.errors

    def close(self) -> None:
        """End the supervisor; a second call finds it ended and does nothing more."""
        self.stop.set()
        self.thread.join(10)
        assert not self.thread.is_alive(), "the supervisor did not end"


def run_log_frames(job_id: str, data_dir: Path) -> list[dict]:
    """The job's run-log events in the order a reader of the log sees them, each as
    `{"seq", "event", "task_id", "metadata"}`.

    The live tests read these where they read the cockpit's `events-since` route before it went
    (DECISION amend1015f D27): `seq` is the event's position in the log, as the route's was, and
    `task_id` is the top-level field or else the one nested in `metadata`, as the route read it.
    """
    from packages.orchestration.timeline import load_run_events

    frames: list[dict] = []
    for seq, event in enumerate(load_run_events(data_dir, job_id)):
        metadata = event.get("metadata") if isinstance(event.get("metadata"), dict) else {}
        linkage = event.get("task_id") or metadata.get("task_id", "")
        frames.append({"seq": seq, "event": event.get("event", ""),
                       "task_id": linkage if isinstance(linkage, str) else "",
                       "metadata": metadata})
    return frames
