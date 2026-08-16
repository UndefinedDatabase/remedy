"""POSIX execution guard for spawned commands — F085 stage 1, T001.

`run_guarded` runs one argv list under kernel resource limits, under this
guard's OWN wall-clock deadline and under per-stream output caps, and returns a
classified `ExecGuardResult`.

Deliberate absences, written here because text search cannot find code that does
not exist:

- NO CALLER. Nothing in this repository imports this module yet. Migrating the
  in-scope call sites is T002, so no subprocess in the running system is
  limited, supervised or sandboxed by anything written here.
- No environment scrubbing and no allowlist. `ExecGuardPolicy.env` is handed to
  the child UNCHANGED; scrubbing is T002.
- No network posture and no filesystem fence; both are T003.

Why `address_space_bytes` is ENFORCED and deliberately NOT classified: a child
that exceeds RLIMIT_AS has its mapping refused, raises `MemoryError` and exits 1
with no signal, and its `ru_maxrss` stays BELOW the limit because the refused
mapping never became resident. Nothing `wait4` reports therefore distinguishes
that death from any other exit-1 failure, so this module enforces the limit and
declines to name it in `tripped_limit`. Claiming `address_space` from that
evidence would be an overclaim.

Why the wall timeout is supervised here rather than forwarded as a `timeout=`
keyword: six of the seven timeout-less in-scope call sites are
`subprocess.Popen`, which takes no such keyword (amendment F085 D1).

Why `cpu_grace_seconds` exists: with RLIMIT_CPU soft == hard the kernel delivers
SIGKILL, which is byte-identical in `wait4` status to the SIGKILL this guard
itself sends on a wall-timeout, and the two causes stop being distinguishable.
With a grace band the kernel delivers SIGXCPU first and the trip is
attributable.

Why an output cap does not end the child: the cap bounds MEMORY, not runtime.
Past the cap the guard stops STORING and keeps COUNTING, so `stdout_bytes_seen`
and `stderr_bytes_seen` remain the totals the child really produced. Runtime is
bounded by `wall_timeout_seconds` and by `cpu_seconds`, which are separate
knobs.
"""

from __future__ import annotations

import os
import resource
import signal
import subprocess
import threading
import time
from collections.abc import Sequence
from dataclasses import dataclass

#: How often the supervisor re-checks a still-running child against its deadline.
_SUPERVISION_POLL_SECONDS = 0.01

#: Read size of one stream-pump iteration.
_READ_CHUNK_BYTES = 65536

#: Policy field name -> `resource` constant name, in the order they are applied.
_RLIMIT_ATTRS = {
    "cpu_seconds": "RLIMIT_CPU",
    "address_space_bytes": "RLIMIT_AS",
    "open_files": "RLIMIT_NOFILE",
    "core_file_bytes": "RLIMIT_CORE",
}


@dataclass(frozen=True)
class ExecGuardPolicy:
    """What a guarded run is allowed to consume. `None` means "do not set".

    `cpu_seconds` is the RLIMIT_CPU SOFT limit; the hard limit is
    `cpu_seconds + cpu_grace_seconds` so the kernel delivers SIGXCPU before
    SIGKILL and the trip stays attributable. `wall_timeout_seconds` is this
    guard's own deadline, and `None` — no wall timeout — is a real policy for
    the runtime command class. `output_cap_bytes` is PER STREAM, not combined.
    `env` is passed through unchanged: scrubbing is T002, not stage 1.
    """

    cpu_seconds: int | None = None
    cpu_grace_seconds: int = 2
    address_space_bytes: int | None = None
    open_files: int | None = None
    core_file_bytes: int = 0
    wall_timeout_seconds: float | None = None
    output_cap_bytes: int | None = None
    cwd: str | None = None
    env: dict[str, str] | None = None


@dataclass(frozen=True)
class ExecGuardResult:
    """The outcome of one guarded run, with the evidence the guard actually holds.

    `returncode` is the exit status when the child exited normally and `None`
    when it died on a signal, in which case `term_signal` carries the signal
    NAME. `stdout`/`stderr` hold at most `output_cap_bytes` per stream while
    `stdout_bytes_seen`/`stderr_bytes_seen` stay the true totals. `tripped_limit`
    is always a member of `limits_enforced`; `limits_unsupported` names every
    requested limit this platform has no `resource` constant for, so a dropped
    limit is never silent.
    """

    returncode: int | None
    term_signal: str | None
    stdout: bytes
    stderr: bytes
    stdout_truncated: bool
    stderr_truncated: bool
    stdout_bytes_seen: int
    stderr_bytes_seen: int
    wall_seconds: float
    cpu_seconds_used: float
    classification: str
    tripped_limit: str | None
    limits_enforced: tuple[str, ...]
    limits_unsupported: tuple[str, ...]


class _StreamPump(threading.Thread):
    """Drain one child stream, storing at most `cap` bytes and counting them all.

    The cap is applied WHILE reading. The buffer is never allowed to grow past
    the cap and then trimmed, because that would need the memory the cap exists
    to deny.
    """

    def __init__(self, stream, cap: int | None) -> None:
        super().__init__(daemon=True)
        self._stream = stream
        self._cap = cap
        self.data = b""
        self.bytes_seen = 0
        self.truncated = False

    def run(self) -> None:
        stored = bytearray()
        while True:
            chunk = self._stream.read1(_READ_CHUNK_BYTES)
            if not chunk:
                break
            self.bytes_seen += len(chunk)
            if self._cap is None:
                stored += chunk
                continue
            room = max(self._cap - len(stored), 0)
            if room:
                stored += chunk[:room]
            if len(chunk) > room:
                self.truncated = True
        self.data = bytes(stored)


def _plan_rlimits(policy: ExecGuardPolicy) -> tuple[list[tuple[int, int, int]], list[str], list[str]]:
    """Resolve the policy into (setrlimit calls, enforced names, unsupported names).

    Support is decided in the PARENT, where it can be reported: a limit whose
    `resource` constant is missing on this platform is recorded as unsupported
    instead of being dropped in silence. Requested limits are clamped down to the
    inherited hard limit, since an unprivileged process may lower a limit and
    never raise one.
    """
    requested: list[tuple[str, int, int]] = []
    if policy.cpu_seconds is not None:
        requested.append(("cpu_seconds", policy.cpu_seconds, policy.cpu_seconds + policy.cpu_grace_seconds))
    if policy.address_space_bytes is not None:
        requested.append(("address_space_bytes", policy.address_space_bytes, policy.address_space_bytes))
    if policy.open_files is not None:
        requested.append(("open_files", policy.open_files, policy.open_files))
    requested.append(("core_file_bytes", policy.core_file_bytes, policy.core_file_bytes))

    calls: list[tuple[int, int, int]] = []
    enforced: list[str] = []
    unsupported: list[str] = []
    for name, soft, hard in requested:
        const = getattr(resource, _RLIMIT_ATTRS[name], None)
        if const is None:
            unsupported.append(name)
            continue
        try:
            _, inherited_hard = resource.getrlimit(const)
        except (OSError, ValueError):
            unsupported.append(name)
            continue
        if inherited_hard != resource.RLIM_INFINITY:
            hard = min(hard, inherited_hard)
            soft = min(soft, hard)
        calls.append((const, soft, hard))
        enforced.append(name)
    return calls, enforced, unsupported


def _kill_process_group(pgid: int) -> None:
    """SIGKILL a whole process group; an already-gone group is success, not an error."""
    if pgid <= 1:
        return
    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        return


def _signal_name(signum: int) -> str:
    """Name of a termination signal, falling back to `SIG<n>` for an unknown number."""
    try:
        return signal.Signals(signum).name
    except ValueError:
        return f"SIG{signum}"


def run_guarded(cmd: Sequence[str], policy: ExecGuardPolicy) -> ExecGuardResult:
    """Run `cmd` under `policy` and classify how it ended.

    The child is spawned from an argv list — never `shell=True` — in its own
    session, so the wall-timeout kill reaches the whole process group rather than
    the leader alone. It is reaped with `os.wait4`, so the returned `rusage`
    belongs to that child and to no other, and the group is killed on every exit
    path, so no descendant outlives this call.
    """
    argv = list(cmd)
    if not argv:
        raise ValueError("run_guarded requires a non-empty argv list")

    rlimit_calls, enforced, unsupported = _plan_rlimits(policy)
    if policy.wall_timeout_seconds is not None:
        enforced.append("wall_timeout")
    if policy.output_cap_bytes is not None:
        enforced.append("output_bytes")

    def _apply_rlimits() -> None:
        # Runs in the forked child between fork and exec: rlimits, nothing else.
        for const, soft, hard in rlimit_calls:
            resource.setrlimit(const, (soft, hard))

    started = time.monotonic()
    proc = subprocess.Popen(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=policy.cwd,
        env=policy.env,
        start_new_session=True,
        preexec_fn=_apply_rlimits,
    )
    # start_new_session=True makes the child its own group leader, so its pid IS the pgid.
    pgid = proc.pid
    out_pump = _StreamPump(proc.stdout, policy.output_cap_bytes)
    err_pump = _StreamPump(proc.stderr, policy.output_cap_bytes)
    out_pump.start()
    err_pump.start()

    deadline = None
    if policy.wall_timeout_seconds is not None:
        deadline = started + policy.wall_timeout_seconds
    deadline_fired = False
    try:
        while True:
            # WNOWAIT observes the exit WITHOUT reaping, so the zombie keeps the pgid
            # allocated and the group kill below can never reach a recycled pid.
            exited = os.waitid(os.P_PID, proc.pid, os.WEXITED | os.WNOWAIT | os.WNOHANG)
            if exited is not None:
                break
            if deadline is not None and time.monotonic() >= deadline:
                deadline_fired = True
                break
            time.sleep(_SUPERVISION_POLL_SECONDS)
    finally:
        # Both exits run this: on a deadline it IS the kill, and on a normal exit it
        # sweeps any descendant the child left behind.
        _kill_process_group(pgid)
        _, status, rusage = os.wait4(proc.pid, 0)
        # The child is already reaped here, so hand Popen its result rather than
        # letting it wait on a pid this call no longer owns.
        proc.returncode = -os.WTERMSIG(status) if os.WIFSIGNALED(status) else os.WEXITSTATUS(status)
        out_pump.join()
        err_pump.join()
        proc.stdout.close()
        proc.stderr.close()
    wall_seconds = time.monotonic() - started

    if os.WIFSIGNALED(status):
        term_signal: str | None = _signal_name(os.WTERMSIG(status))
        returncode: int | None = None
    else:
        term_signal = None
        returncode = os.WEXITSTATUS(status)

    if deadline_fired:
        classification, tripped_limit = "resource_limit", "wall_timeout"
    elif term_signal == "SIGXCPU":
        classification, tripped_limit = "resource_limit", "cpu_seconds"
    elif out_pump.truncated or err_pump.truncated:
        classification, tripped_limit = "resource_limit", "output_bytes"
    elif returncode == 0:
        classification, tripped_limit = "ok", None
    else:
        classification, tripped_limit = "failed", None

    return ExecGuardResult(
        returncode=returncode,
        term_signal=term_signal,
        stdout=out_pump.data,
        stderr=err_pump.data,
        stdout_truncated=out_pump.truncated,
        stderr_truncated=err_pump.truncated,
        stdout_bytes_seen=out_pump.bytes_seen,
        stderr_bytes_seen=err_pump.bytes_seen,
        wall_seconds=wall_seconds,
        cpu_seconds_used=rusage.ru_utime + rusage.ru_stime,
        classification=classification,
        tripped_limit=tripped_limit,
        limits_enforced=tuple(enforced),
        limits_unsupported=tuple(unsupported),
    )
