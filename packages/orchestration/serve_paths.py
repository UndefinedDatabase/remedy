"""Where the `remedy serve` supervisor keeps its state (F200, DECISION F200 D1).

One supervisor runs per data root, and everything it owns lives in the data-root
class `serve`: the unix socket the command line talks to, the file holding the
supervisor's process id, the file holding the token the socket requires, and the
run registry it resumes from after a restart. The supervisor and every client
compute these paths from the same data root, so a client finds the socket by
looking where its own data root says the socket is, and nothing else is read.

A unix socket path has a hard length limit: the kernel's `sun_path` holds 108
bytes on Linux and 104 on macOS, the terminating NUL included. A data root deep
enough to push the socket past the smaller limit is refused with a reason naming
the setting to change, rather than moved somewhere a client would not look.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.data_paths import data_class_dir

SOCKET_NAME = "serve.sock"
PID_NAME = "serve.pid"
TOKEN_NAME = "serve.token"
RUNS_NAME = "runs"

#: The longest socket path both Linux and macOS accept: 104 bytes less the NUL.
SOCKET_PATH_MAX_BYTES = 103


@dataclass(frozen=True)
class ServePaths:
    """The supervisor's files under one data root."""

    root: Path
    socket: Path
    pid_file: Path
    token_file: Path
    runs_dir: Path


def serve_paths(root: Path | None = None) -> ServePaths:
    """The `serve` class's paths under ROOT, or under the resolved data root."""
    base = data_class_dir("serve", root)
    return ServePaths(
        root=base,
        socket=base / SOCKET_NAME,
        pid_file=base / PID_NAME,
        token_file=base / TOKEN_NAME,
        runs_dir=base / RUNS_NAME,
    )


def socket_path_problem(path: Path) -> str:
    """Why PATH cannot be bound as a unix socket on every platform, or ``""``."""
    size = len(os.fsencode(path))
    if size <= SOCKET_PATH_MAX_BYTES:
        return ""
    return (f"the socket path {str(path)!r} is {size} bytes long and a unix socket "
            f"path may be at most {SOCKET_PATH_MAX_BYTES}; set REMEDY_DATA_DIR or the "
            f"data_dir setting to a shorter directory")
