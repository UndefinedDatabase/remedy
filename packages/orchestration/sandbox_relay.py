"""The first process inside a Pi sandbox: the provider port, then Pi (DECISION amend1016sb D3).

The sandbox has its own network namespace, so nothing on the host is reachable from it. Pi still
needs its model endpoint. This script listens on 127.0.0.1:<port> INSIDE the sandbox and carries
every connection, byte for byte, to one Unix socket that Remedy's trusted host side bound into the
sandbox; that host side (`tool_sandbox.ProviderRelay`) admits only the model requests and talks
to the configured endpoint. Then it runs the given command (Pi) and exits with its status.

It runs as `python -I -S <this file> <port> <socket> -- <argv...>` with the standard library
alone, because no Remedy package is mounted inside the sandbox; it imports nothing from Remedy.
Remedy deliberately keeps no filter here: everything inside the sandbox is untrusted, so the
filter lives on the host side, where a model-controlled command cannot change it.
"""
from __future__ import annotations

import socket
import subprocess
import sys
import threading

_CHUNK = 65536


def _pump(source: socket.socket, sink: socket.socket) -> None:
    """Copy one direction until end-of-file, then pass the end-of-file on."""
    try:
        while True:
            data = source.recv(_CHUNK)
            if not data:
                break
            sink.sendall(data)
    except OSError:
        pass    # the other side went away; the connection ends either way
    finally:
        try:
            sink.shutdown(socket.SHUT_WR)
        except OSError:
            pass    # already closed


def _carry(client: socket.socket, socket_path: str) -> None:
    """One client connection, carried to the provider socket."""
    with client:
        try:
            upstream = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            upstream.connect(socket_path)
        except OSError:
            return
        with upstream:
            back = threading.Thread(target=_pump, args=(upstream, client), daemon=True)
            back.start()
            _pump(client, upstream)
            back.join()


def _serve(listener: socket.socket, socket_path: str) -> None:
    while True:
        client, _ = listener.accept()
        threading.Thread(target=_carry, args=(client, socket_path), daemon=True).start()


def main(argv: list[str]) -> int:
    if len(argv) < 4 or argv[2] != "--":
        sys.stderr.write("usage: sandbox_relay.py <port> <socket> -- <command...>\n")
        return 2
    port, socket_path, command = int(argv[0]), argv[1], argv[3:]
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", port))
    listener.listen(16)
    threading.Thread(target=_serve, args=(listener, socket_path), daemon=True).start()
    child = subprocess.Popen(command)
    code = child.wait()
    return 128 - code if code < 0 else code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
