"""R-0950 probe plugin, loaded with `-p r0950_probe`; the mode comes from R0950_MODE.

FOREIGN  -- every app port is a fallback from the machine's shared pool, and the moment the
            harness has stopped the app, an unrelated listener binds that same number.
LEAK     -- the harness's stop does nothing and reports no survivor: a real zombie that lies.
REPORTED -- the harness stops the app but its sweep reports a survivor.
"""
import os
import signal
import socket

from packages.orchestration import dod_runners
from packages.runtimes.dev_server import pick_free_port

MODE = os.environ.get("R0950_MODE", "")
_listeners: list[socket.socket] = []
_leaked: list[int] = []
_last_port: list[int] = []


def pytest_configure(config):
    if MODE == "FOREIGN":
        real_stop = dod_runners._stop_app

        def fallback_port(requested, host="127.0.0.1"):
            port = pick_free_port(host)
            _last_port.append(port)
            return port

        def stop_then_foreign_bind(proc, log):
            reason = real_stop(proc, log)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("127.0.0.1", _last_port[-1]))
            sock.listen(1)
            _listeners.append(sock)
            return reason

        dod_runners.choose_port = fallback_port
        dod_runners._stop_app = stop_then_foreign_bind
    elif MODE == "LEAK":
        def stop_nothing(pid, session_id=0, **_kw):
            _leaked.append(session_id or pid)
            return {"survivors": []}

        dod_runners.stop_process_tree = stop_nothing
    elif MODE == "REPORTED":
        real_tree = dod_runners.stop_process_tree

        def stop_and_report(pid, **kw):
            result = dict(real_tree(pid, **kw))
            result["survivors"] = [424242]
            return result

        dod_runners.stop_process_tree = stop_and_report


def pytest_unconfigure(config):
    for sock in _listeners:
        sock.close()
    for group in _leaked:
        try:
            os.killpg(group, signal.SIGKILL)
        except OSError:
            pass
