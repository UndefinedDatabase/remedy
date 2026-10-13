"""What the cockpit's UI server binds, advertises and opens when it starts (finding R-1264).

Moved unchanged out of `packages/orchestration/ui_server.py`, which imports these names back, so
every import path keeps working; `_ui_session_info` and `_print_ui_urls` hold what
`start_ui_server` wrote and printed in place, so that function stays under the limit of
`docs/system/structure-ledger-v1.md`.
"""

from __future__ import annotations

import os
import socket
from datetime import datetime, timezone

_UI_LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})
_ANY_IPV4_HOST = ".".join(("0", "0", "0", "0"))
_UI_WILDCARD_HOSTS = frozenset({"", _ANY_IPV4_HOST, "*"})


def _outer_ui_ip_candidates(requested_host: str) -> list[str]:
    """LAN-facing IPv4 hosts worth advertising for one UI server."""
    candidates: list[str] = []
    if requested_host and requested_host not in _UI_WILDCARD_HOSTS:
        candidates.append(requested_host)
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            candidates.append(str(info[4][0]))
    except OSError:
        pass
    seen: set[str] = set()
    result: list[str] = []
    for host in candidates:
        if host in seen or host in _UI_LOOPBACK_HOSTS or host.startswith("127."):
            continue
        seen.add(host)
        result.append(host)
    return result


def _ui_bind_and_urls(host: str, actual_port: int, job_id: str, token: str) -> tuple[str, list[str], list[str]]:
    """Return `(bind_host, urls, external_urls)` for a requested UI host."""
    requested = (host or "127.0.0.1").strip()
    external = requested not in _UI_LOOPBACK_HOSTS
    bind_host = "" if external else "127.0.0.1"
    local_url = f"http://127.0.0.1:{actual_port}/?job={job_id}&token={token}"
    external_urls = [
        f"http://{candidate}:{actual_port}/?job={job_id}&token={token}"
        for candidate in _outer_ui_ip_candidates(requested)
    ] if external else []
    return bind_host, [local_url, *external_urls], external_urls


# The info file a started server writes, key for key in the order `start_ui_server` wrote it.
def _ui_session_info(
    *, url: str, host: str, bind_host: str, port: int, urls: list[str],
    external_urls: list[str], token: str, job_id: str,
) -> dict[str, object]:
    """The JSON object a started UI server writes to its info file."""
    return {
        "version": 1,
        "url": url,
        "host": host,
        "bind_host": bind_host,
        "port": port,
        "urls": urls,
        "external_urls": external_urls,
        "token": token,
        "job_id": job_id,
        "pid": os.getpid(),
        "started_at": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def _print_ui_urls(url: str, external_urls: list[str]) -> None:
    """Print a started server's loopback URL, each LAN URL, and how to stop it."""
    print(f"\nRemedy UI: {url}")
    for external_url in external_urls:
        print(f"LAN URL: {external_url}")
    print("\nPress Ctrl-C to stop.\n")


def _try_open_browser(url: str) -> None:
    """Best-effort platform opener. Failure does not raise."""
    import platform
    import subprocess

    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", url])
        elif system == "Linux":
            subprocess.Popen(["xdg-open", url])
        elif system == "Windows":
            os.startfile(url)  # type: ignore[attr-defined]
    except (OSError, FileNotFoundError):
        pass
