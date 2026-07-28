"""Per-worker TCP ports for tests that start a real runtime.

The runtime default port is 5173 (``packages/runtimes/runtime_config.py``), and
the runtime tests wrote that literal into every generated ``.remedy/config.toml``.
Under ``pytest -n auto`` all workers then bound — and probed — the same port, so a
test asserting a readiness *failure* could reach a **different worker's** healthy
server: ``RuntimeProbeResult(ok=True, status_code=200, port=5173)`` where the test
required ``ok is False``, and a delayed-readiness assertion (``elapsed >= 1.4``)
returned in 0.15 s against the foreign listener.

``worker_port()`` gives each xdist worker its own port, so these tests can only
ever see the server they started themselves. The product default is untouched:
this is a test seam, not a behavior change.
"""

from __future__ import annotations

import os

#: Base of the per-worker range. Above the runtime default (5173) and below the
#: Linux ephemeral range (``net.ipv4.ip_local_port_range`` starts at 32768), so a
#: worker port can never collide with a kernel-assigned client port.
_BASE = 15173


def worker_index() -> int:
    """0 for a serial run, N for xdist worker ``gwN``."""
    name = os.environ.get("PYTEST_XDIST_WORKER", "")
    digits = name[2:] if name.startswith("gw") else ""
    return int(digits) if digits.isdigit() else 0


def worker_port(offset: int = 0) -> int:
    """A port owned by this worker alone.

    ``offset`` separates several servers started within one worker; keep it small
    and distinct per call site.
    """
    return _BASE + worker_index() * 16 + offset
