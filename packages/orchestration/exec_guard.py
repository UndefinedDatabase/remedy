"""POSIX execution guard for spawned commands — F085 stage 1, T001.

`run_guarded` runs one argv list under kernel resource limits, under this
guard's OWN wall-clock deadline and under per-stream output caps, and returns a
classified `ExecGuardResult`.

Deliberate absences, written here because text search cannot find code that does
not exist:

- PARTIAL COVERAGE, and the gap is the point. Since F085 T002a the managed
  builder seam and the claude CLI provider run through `run_guarded`, and a
  supervisor that must own its own parent half may take the CHILD half alone
  through `plan_child_spawn`; since T002b the test class is PARTIALLY migrated
  through `run_guarded_test_command`; and since T002c the DoD's bounded process
  checks run through `run_guarded_dod_process_command`, while the DoD app
  harness and the runtime, git and packaging classes still spawn unsupervised.
  No count is written here on purpose: it changes with every migration round,
  and the caller grep is the honest answer.
- No environment scrubbing UNLESS the policy asks for it: with
  `env_allowlist=None` the policy's `env` reaches the child UNCHANGED, which every
  T001 test relies on. Callers CHOOSE the allowlist per command class — the
  builder policy pins one, the CLI-provider policy deliberately does not — so what
  a child inherits is that caller's decision, never this module's default.
- No network posture and no filesystem fence; both are T003.

Why `address_space_bytes` is ENFORCED and deliberately NOT classified: a child
that exceeds RLIMIT_AS has its mapping refused, raises `MemoryError` and exits 1
with no signal, and its `ru_maxrss` stays BELOW the limit because the refused
mapping never became resident. Nothing `wait4` reports therefore distinguishes
that death from any other exit-1 failure, so this module enforces the limit and
declines to name it in `tripped_limit`. Claiming `address_space` from that
evidence would be an overclaim.

What an allowlist does NOT bound, stated where a reader will look for it: it
bounds what the PARENT hands over, never what the child's own runtime then adds
to itself. A CPython child spawned with a restricted environment sets `LC_CTYPE`
during PEP 538 locale coercion, so the child's environment is a SUPERSET of the
scrubbed one. Nothing here can prevent that, and stage 1 does not pretend to.

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
from collections.abc import Callable, Mapping, Sequence
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

#: Never inherited by a guarded child, whatever an allowlist says. Same spelling and
#: members as `managed_builder_execution._FORBIDDEN_ENV_KEYS`, kept here so the guard
#: denies them even when a caller's allowlist is wrong.
FORBIDDEN_ENV_KEYS = frozenset({
    "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "CLAUDE_API_KEY",
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
    "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN",
    "GITHUB_TOKEN", "GH_TOKEN", "GITLAB_TOKEN",
    "DATABASE_URL", "REDIS_URL",
})

#: WHY: the one environment a `test`-class command may inherit — locale, interpreter
#: behaviour, the toolchain PATH and the temp dirs a test suite legitimately needs.
#: Sorted, so a reader can see at a glance whether a key is a member.
#: `REMEDY_UI_NO_AUTO_BUILD` is a member for carried finding R-0202: the mid-run UI
#: rebuild class exists BECAUSE that variable stopped reaching a child, so an
#: allowlist that dropped it would re-create the very bug this feature must close.
TEST_COMMAND_ENV_ALLOWLIST: tuple[str, ...] = (
    "CI", "HOME", "LANG", "LC_ALL", "LC_CTYPE", "LOGNAME", "PATH", "PWD",
    "PYTHONDONTWRITEBYTECODE", "PYTHONHASHSEED", "PYTHONPATH", "PYTHONUNBUFFERED",
    "REMEDY_UI_NO_AUTO_BUILD", "SHELL", "TEMP", "TERM", "TMP", "TMPDIR", "TZ",
    "USER", "VIRTUAL_ENV",
)

#: Default per-stream output cap for a `test`-class command, 16 MiB. It MUST stay
#: strictly ABOVE `test_runner.MAX_TEST_OUTPUT_BYTES` (1 MiB): the caller does its own
#: truncation and publishes `output_truncated` from it, so a guard cap at or below the
#: caller's would truncate FIRST and that flag would stop describing what the caller
#: measured. The relationship is stated in words rather than imported, because the
#: dependency runs the other way — `test_runner` imports this module, never the reverse.
TEST_COMMAND_OUTPUT_CAP_BYTES: int = 16 * 1024 * 1024


def scrub_child_env(source: Mapping[str, str], allowlist: Sequence[str]) -> dict[str, str]:
    """Build a child environment from `source`, keeping ONLY allowlisted keys.

    A `FORBIDDEN_ENV_KEYS` member is dropped even when the allowlist names it: the
    allowlist is a caller's policy, this set is the guard's floor. An undefined key
    is ABSENT, not empty — a build tool reads empty as "set to nothing".
    """
    keep = set(allowlist) - FORBIDDEN_ENV_KEYS
    return {key: source[key] for key in sorted(keep) if key in source}


@dataclass(frozen=True)
class ExecGuardPolicy:
    """What a guarded run is allowed to consume. `None` means "do not set".

    `cpu_seconds` is the RLIMIT_CPU SOFT limit; the hard limit is
    `cpu_seconds + cpu_grace_seconds` so the kernel delivers SIGXCPU before
    SIGKILL and the trip stays attributable. `wall_timeout_seconds` is this
    guard's own deadline, and `None` — no wall timeout — is a real policy for
    the runtime command class. `output_cap_bytes` is PER STREAM, not combined.
    `env` reaches the child unchanged while `env_allowlist` is None. When
    `env_allowlist` names keys, the child's environment is built by
    `scrub_child_env` from `env` — or from `os.environ` when `env` is None —
    keeping only those keys and never one in `FORBIDDEN_ENV_KEYS`.
    `stream_drain_grace_seconds` is the TOTAL extra time the guard will wait for
    both stream pumps after the child is reaped, so a descendant that escaped the
    process group and still holds the pipe cannot extend the call without bound.
    """

    cpu_seconds: int | None = None
    cpu_grace_seconds: int = 2
    address_space_bytes: int | None = None
    open_files: int | None = None
    core_file_bytes: int = 0
    wall_timeout_seconds: float | None = None
    stream_drain_grace_seconds: float = 5.0
    output_cap_bytes: int | None = None
    cwd: str | None = None
    env: dict[str, str] | None = None
    env_allowlist: tuple[str, ...] | None = None


# WHY: the CHILD-side half of a policy — everything a `Popen` must pass to obey it — so a supervisor that owns its own PARENT half can still be limited.
@dataclass(frozen=True)
class ChildSpawnPlan:
    """What any `subprocess.Popen` must be given to spawn a child under a policy.

    The PARENT half — the wall deadline, the output cap, reaping the child and
    killing its group — stays with whichever supervisor spawns, because
    `run_guarded` buffers both streams to bytes while a streaming supervisor
    consumes stdout line by line, and only this half is common to both.

    `limits_enforced` therefore names ONLY the rlimits that were really applied.
    `wall_timeout` and `output_bytes` are parent-side, and each supervisor
    appends them to its own result when it enforces them.
    """

    cwd: str | None
    env: dict[str, str] | None
    preexec_fn: Callable[[], None]
    limits_enforced: tuple[str, ...]
    limits_unsupported: tuple[str, ...]


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

    `streams_complete` is False when a stream pump was still blocked when the
    drain grace ran out — an escaped descendant holding the inherited pipe. Its
    meaning is exactly that and nothing more: some pump did not reach EOF. ITS
    `stdout`/`stderr` field then carries whatever that pump had already read when
    the grace ran out, which is a PARTIAL buffer and is claimed as nothing else,
    and `stdout_bytes_seen`/`stderr_bytes_seen` are the byte totals counted so
    far — above the stored length whenever the cap trimmed the storage. A guard
    that returns on time with the bytes in hand, and says the stream is
    incomplete, is better than one that blocks for the escapee's whole life.
    """

    returncode: int | None
    term_signal: str | None
    stdout: bytes
    stderr: bytes
    stdout_truncated: bool
    stderr_truncated: bool
    stdout_bytes_seen: int
    stderr_bytes_seen: int
    streams_complete: bool
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

    Every field lives behind `_lock` and is read only through `snapshot()`, so a
    caller that gives up on a pump still blocked at the drain deadline gets the
    bytes it HAD read rather than nothing, and never observes a half-applied
    update of the three values against each other.
    """

    def __init__(self, stream, cap: int | None) -> None:
        super().__init__(daemon=True)
        self._stream = stream
        self._cap = cap
        self._lock = threading.Lock()
        self._stored = bytearray()
        self._bytes_seen = 0
        self._truncated = False

    def snapshot(self) -> tuple[bytes, int, bool]:
        """The bytes stored so far, the bytes seen so far and the truncated flag.

        Safe to call at any time, including while `run()` is still reading: all
        three are taken under the writer's own lock, so they describe one single
        point in the stream. After EOF they are the pump's final values.
        """
        with self._lock:
            return bytes(self._stored), self._bytes_seen, self._truncated

    def run(self) -> None:
        while True:
            chunk = self._stream.read1(_READ_CHUNK_BYTES)
            if not chunk:
                break
            with self._lock:
                self._bytes_seen += len(chunk)
                if self._cap is None:
                    self._stored += chunk
                    continue
                room = max(self._cap - len(self._stored), 0)
                if room:
                    self._stored += chunk[:room]
                if len(chunk) > room:
                    self._truncated = True


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


def plan_child_spawn(policy: ExecGuardPolicy) -> ChildSpawnPlan:
    """Resolve `policy` into the cwd, environment and `preexec_fn` a child needs.

    Support for each rlimit is decided HERE, in the parent, so an unsupported
    limit is reported rather than dropped in silence. The returned `preexec_fn`
    runs between fork and exec and applies those limits and nothing else.

    The environment follows the module's rule exactly: `policy.env` reaches the
    child UNCHANGED — including `None`, which means "inherit" — while
    `env_allowlist` is None, and is rebuilt by `scrub_child_env` when it is not.
    """
    rlimit_calls, enforced, unsupported = _plan_rlimits(policy)

    def _apply_rlimits() -> None:
        # Runs in the forked child between fork and exec: rlimits, nothing else.
        for const, soft, hard in rlimit_calls:
            resource.setrlimit(const, (soft, hard))

    child_env = policy.env
    if policy.env_allowlist is not None:
        child_env = scrub_child_env(
            os.environ if policy.env is None else policy.env, policy.env_allowlist
        )

    return ChildSpawnPlan(
        cwd=policy.cwd,
        env=child_env,
        preexec_fn=_apply_rlimits,
        limits_enforced=tuple(enforced),
        limits_unsupported=tuple(unsupported),
    )


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
    path, so no descendant of THAT GROUP outlives this call.

    A descendant that calls `setsid` leaves the group and the kill cannot reach
    it (R-0495). It still holds the inherited pipe write ends, so the guard drains
    the streams under `stream_drain_grace_seconds` and returns with
    `streams_complete=False` rather than waiting for EOF that may never come:
    `wall_timeout_seconds` bounds the CHILD, and the two together bound THIS CALL.
    """
    argv = list(cmd)
    if not argv:
        raise ValueError("run_guarded requires a non-empty argv list")

    plan = plan_child_spawn(policy)
    # The parent half is this guard's own, so it appends its own limit names.
    enforced = list(plan.limits_enforced)
    if policy.wall_timeout_seconds is not None:
        enforced.append("wall_timeout")
    if policy.output_cap_bytes is not None:
        enforced.append("output_bytes")

    started = time.monotonic()
    proc = subprocess.Popen(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=plan.cwd,
        env=plan.env,
        start_new_session=True,
        preexec_fn=plan.preexec_fn,
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
        # ONE deadline for BOTH pumps, so the grace is a total cost and not a
        # per-stream one that a second blocked pump could double.
        drain_deadline = time.monotonic() + policy.stream_drain_grace_seconds
        for pump in (out_pump, err_pump):
            pump.join(max(drain_deadline - time.monotonic(), 0.0))
        streams_complete = not (out_pump.is_alive() or err_pump.is_alive())
        # Read through snapshot() rather than off a pump that may still be
        # blocked: a pump the grace ran out on has bytes in hand, and throwing
        # them away buys nothing. `streams_complete` above already says the
        # stream is partial, so the two together stay honest.
        stdout_data, stdout_seen, stdout_truncated = out_pump.snapshot()
        stderr_data, stderr_seen, stderr_truncated = err_pump.snapshot()
        if streams_complete:
            # Closed ONLY when no pump is still reading: closing a descriptor under
            # a blocked reader risks that thread reading a recycled fd after a later
            # open(). The pumps are daemons, so a leaked pair is the cheaper wrong.
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
    elif stdout_truncated or stderr_truncated:
        classification, tripped_limit = "resource_limit", "output_bytes"
    elif returncode == 0:
        classification, tripped_limit = "ok", None
    else:
        classification, tripped_limit = "failed", None

    return ExecGuardResult(
        returncode=returncode,
        term_signal=term_signal,
        stdout=stdout_data,
        stderr=stderr_data,
        stdout_truncated=stdout_truncated,
        stderr_truncated=stderr_truncated,
        stdout_bytes_seen=stdout_seen,
        stderr_bytes_seen=stderr_seen,
        streams_complete=streams_complete,
        wall_seconds=wall_seconds,
        cpu_seconds_used=rusage.ru_utime + rusage.ru_stime,
        classification=classification,
        tripped_limit=tripped_limit,
        limits_enforced=tuple(enforced),
        limits_unsupported=plan.limits_unsupported,
    )


# ---------------------------------------------------------------------------
# The shared `test`-class seam (F085 T002b) — ONE policy and ONE runner for the
# whole command class, so ten modules cannot each grow a private answer.
# ---------------------------------------------------------------------------


def test_command_exec_policy(
    timeout_sec: float,
    cwd: str | None,
    *,
    output_cap_bytes: int = TEST_COMMAND_OUTPUT_CAP_BYTES,
    extra_env_keys: Sequence[str] = (),
    extra_env: Mapping[str, str] | None = None,
) -> ExecGuardPolicy:
    """The stage-1 policy every `test`-class command runs under.

    `cpu_seconds`, `address_space_bytes` and `open_files` are deliberately None,
    for the reasons `managed_builder_execution._builder_exec_policy` already
    settled for the builder class — not restated here, so the two cannot drift
    apart. What IS enforced is real: this guard's own wall deadline, a per-stream
    output cap applied WHILE reading, the cwd pin, a zero core dump and an
    explicit environment allowlist.

    `env=None` is deliberate: it makes `plan_child_spawn` build the child
    environment from `os.environ`, which is where a test command's toolchain
    actually lives. `extra_env_keys` is the per-project override knob T2_F085's
    edge-case section promises — a project whose suite needs one more variable
    names it there instead of widening the shared allowlist for everyone.

    `extra_env` SETS variables the parent need not have, which `extra_env_keys`
    cannot do: that knob names keys to pass THROUGH, so a key absent from
    `os.environ` arrives absent. Both `test`-class call sites still on a bare
    spawn overlay one variable onto a copy of `os.environ` and would lose that
    value silently on this seam without this knob. The overlay becomes the scrub
    SOURCE and its keys join the allowlist, so `scrub_child_env` still applies
    `FORBIDDEN_ENV_KEYS` as the floor: an `extra_env` naming a forbidden key does
    not reach the child.
    """
    overlay = dict(extra_env or {})
    return ExecGuardPolicy(
        wall_timeout_seconds=float(timeout_sec),
        output_cap_bytes=output_cap_bytes,
        cwd=cwd,
        core_file_bytes=0,
        env={**os.environ, **overlay} if overlay else None,
        env_allowlist=(
            TEST_COMMAND_ENV_ALLOWLIST + tuple(extra_env_keys) + tuple(sorted(overlay))
        ),
    )


def run_guarded_test_command(
    cmd: Sequence[str],
    *,
    timeout_sec: float,
    cwd: str | None,
    extra_env_keys: Sequence[str] = (),
    extra_env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    """Run one `test`-class command under the guard, shaped like `subprocess.run`.

    The return value is a `CompletedProcess` with BYTES streams and a wall trip is
    raised as `subprocess.TimeoutExpired`, so a call site migrated onto this seam
    keeps the exception and result shapes it already handled: the mechanism
    changes, the observable outcome does not.

    The `TimeoutExpired` carries the PARTIAL streams the guard is already holding.
    Callers of the sites this seam replaces read `exc.stdout` and `exc.stderr` to
    persist what a timed-out suite managed to print, and dropping that output would
    lose evidence the guard has in hand.

    A signal death comes back as a NEGATIVE returncode in the -SIGNUM form — the
    same translation `managed_builder_execution._guarded_exit_code` performs — since
    that is what `subprocess.run` reported before the migration.

    `FileNotFoundError` is deliberately NOT caught here: `Popen` raises it inside
    `run_guarded` before any supervision starts, it means the executable does not
    exist rather than that a run misbehaved, and every caller already handles it.
    """
    guarded = run_guarded(cmd, test_command_exec_policy(
        timeout_sec, cwd, extra_env_keys=extra_env_keys, extra_env=extra_env))
    if guarded.tripped_limit == "wall_timeout":
        raise subprocess.TimeoutExpired(
            list(cmd), timeout_sec, output=guarded.stdout, stderr=guarded.stderr
        )
    returncode = guarded.returncode
    if returncode is None:
        try:
            returncode = -int(signal.Signals[guarded.term_signal].value)
        except (KeyError, ValueError, TypeError):
            returncode = -1
    return subprocess.CompletedProcess(list(cmd), returncode, guarded.stdout, guarded.stderr)


# ---------------------------------------------------------------------------
# The `dod-process` seam (F085 T002c) — the DoD's own bounded checks, which
# KEEP their wall timeout: a DoD check is a check, never a service.
# ---------------------------------------------------------------------------


#: WHY: the environment a `dod-process` command may inherit, and its per-stream cap.
#: The MEMBERS are the `test`-class values and the NAMES are deliberately separate:
#: T2_F085's policy table rules `test` and `dod-process` as two rows, so widening one
#: row stays a one-line edit here instead of silently widening the other. The cap MUST
#: stay strictly ABOVE `dod_runners.MAX_OUTPUT_TAIL_CHARS` for the reason
#: `TEST_COMMAND_OUTPUT_CAP_BYTES` states about `test_runner`: the caller tails the
#: output itself and publishes `output_truncated` from that measurement.
DOD_PROCESS_ENV_ALLOWLIST: tuple[str, ...] = TEST_COMMAND_ENV_ALLOWLIST
DOD_PROCESS_OUTPUT_CAP_BYTES: int = TEST_COMMAND_OUTPUT_CAP_BYTES


def dod_process_exec_policy(timeout_sec: float, cwd: str | None) -> ExecGuardPolicy:
    """The stage-1 policy every `dod-process` check runs under.

    A DoD check is BOUNDED — pytest, a linter, a build, a project's own command —
    so it KEEPS a wall timeout, which is what separates this class from `dod-app`
    in T2_F085's policy table. `cpu_seconds`, `address_space_bytes` and
    `open_files` are None for the reasons
    `managed_builder_execution._builder_exec_policy` already settled for the
    builder class, not restated here so the two cannot drift apart.

    `env=None` is deliberate and is the gap this seam closes: the call site it
    replaces passed `os.environ.copy()`, which handed a project-authored command
    the WHOLE parent environment. With `env=None` and an allowlist,
    `plan_child_spawn` builds the child environment from `os.environ` keeping only
    allowlisted keys, and `FORBIDDEN_ENV_KEYS` remains the floor beneath it.
    """
    return ExecGuardPolicy(
        wall_timeout_seconds=float(timeout_sec),
        output_cap_bytes=DOD_PROCESS_OUTPUT_CAP_BYTES,
        cwd=cwd,
        core_file_bytes=0,
        env=None,
        env_allowlist=DOD_PROCESS_ENV_ALLOWLIST,
    )


def run_guarded_dod_process_command(
    cmd: Sequence[str],
    *,
    timeout_sec: float,
    cwd: str | None,
) -> subprocess.CompletedProcess[bytes]:
    """Run one `dod-process` check under the guard, shaped like `subprocess.run`.

    The same three translations `run_guarded_test_command` performs, and for the
    same reason — a migrated call site keeps the result and exception shapes it
    already handled: a wall trip is raised as `subprocess.TimeoutExpired` CARRYING
    the partial streams the guard is holding, a signal death comes back as a
    NEGATIVE returncode, and `FileNotFoundError` is left to propagate, because it
    means the executable does not exist rather than that a run misbehaved.

    WHY the translation is duplicated here rather than shared: two callers are not
    yet a pattern, and the third is known — `runtime-build` at T002d, whose sites
    are `subprocess.run` calls carrying a `timeout=` of their own. That round
    extracts this, with three uses to show which parts are really common.
    """
    guarded = run_guarded(cmd, dod_process_exec_policy(timeout_sec, cwd))
    if guarded.tripped_limit == "wall_timeout":
        raise subprocess.TimeoutExpired(
            list(cmd), timeout_sec, output=guarded.stdout, stderr=guarded.stderr
        )
    returncode = guarded.returncode
    if returncode is None:
        try:
            returncode = -int(signal.Signals[guarded.term_signal].value)
        except (KeyError, ValueError, TypeError):
            returncode = -1
    return subprocess.CompletedProcess(list(cmd), returncode, guarded.stdout, guarded.stderr)
