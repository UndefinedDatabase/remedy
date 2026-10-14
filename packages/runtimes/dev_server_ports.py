"""The ports and the readiness probe, moved out of `packages/runtimes/dev_server.py`.

Holds the port helpers `port_is_free`, `pick_free_port` and `choose_port`, the
readiness-probe result shape `RuntimeProbeResult`, and the one HTTP GET `http_probe`
polls a project's dev server with. Every consumer imports these names from here
(operator amendment amend1014-luna-mission-fixes D.2).
"""
from __future__ import annotations

import os
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

DEFAULT_HOST = "127.0.0.1"


def port_is_free(port: int, host: str = DEFAULT_HOST) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, int(port)))
        except OSError:
            return False
    return True


def pick_free_port(host: str = DEFAULT_HOST) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1])


def choose_port(requested: int, host: str = DEFAULT_HOST) -> int:
    """Prefer the requested port; fall back to a free one. Never kill the squatter."""
    if port_is_free(requested, host):
        return int(requested)
    return pick_free_port(host)


@dataclass
class RuntimeProbeResult:
    ok: bool = False
    status_code: int = 0
    url: str = ""
    port: int = 0
    elapsed_s: float = 0.0
    error: str = ""
    error_class: str = ""       # "" | "config" | "start" | "ready" | "stop"
    log_tail: str = ""
    pid: int = 0
    survivors: list[int] = field(default_factory=list)
    log_error: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "log_error": self.log_error,
            "status_code": self.status_code,
            "url": self.url,
            "port": self.port,
            "elapsed_s": round(self.elapsed_s, 3),
            "error": self.error,
            "error_class": self.error_class,
            "log_tail": self.log_tail,
            "pid": self.pid,
            "survivors": list(self.survivors),
        }


# WHY: a health answer can come from another check's app squatting the same port;
# only a process THIS run's own session started answering LISTEN proves it is ours.
def port_listener_in_session(port: int, session_id: int) -> bool | None:
    """Does a process in process group ``session_id`` hold a LISTEN socket on ``port``?

    True as soon as a live member of ``session_id`` holds a LISTEN socket on
    ``port``. A process whose own group id cannot be read is skipped outright — it
    vanished, or it is not ours to read. Among the processes confirmed to be IN the
    session, one that vanished before its connections could be read
    (``psutil.NoSuchProcess``) is also skipped; any OTHER failure to read them
    (access denied, a zombie) leaves this port's true owner unproven, so a denied
    read never reads as proof the port is foreign. False only when every session
    member was read cleanly and none listens on ``port``; None when some member
    was unreadable that way, or when the process table itself could not be read
    at all.
    """
    import psutil

    try:
        procs = list(psutil.process_iter(["pid"]))
    except (psutil.Error, OSError):
        return None

    unreadable = False
    for proc in procs:
        try:
            if os.getpgid(proc.pid) != session_id:
                continue
        except (OSError, ProcessLookupError):
            continue  # vanished, or not ours to read

        try:
            reader = getattr(proc, "net_connections", None) or proc.connections
            conns = reader(kind="inet")
        except psutil.NoSuchProcess:
            continue
        except (psutil.Error, OSError):
            unreadable = True
            continue

        for conn in conns:
            if conn.status == psutil.CONN_LISTEN and conn.laddr and conn.laddr.port == port:
                return True

    return None if unreadable else False


def http_probe(url: str, timeout: float = 3.0) -> tuple[int, str]:
    """One HTTP GET. Returns (status, error). Never raises."""
    req = urllib.request.Request(url, method="GET")  # noqa: S310 - loopback only
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            return int(resp.status), ""
    except urllib.error.HTTPError as exc:
        return int(exc.code), ""
    except urllib.error.URLError as exc:
        return 0, str(exc.reason)
    except (TimeoutError, OSError) as exc:
        return 0, str(exc)
