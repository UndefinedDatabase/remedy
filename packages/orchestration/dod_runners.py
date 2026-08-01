"""F061 T002/T003 — execute DoD checks and record what actually happened.

One check in, one :class:`CheckEvidence` out: the command as argv, the working
directory, the exit code, how long it took, and a tail of the real output. A
check is green only when its process exited 0. Every other outcome — a missing
tool, a refused executable, a bad working directory, a timeout — is RED with a
named reason. Nothing here can produce a silent pass.

Subprocess discipline is the one already used by
``test_runner.run_tests_local``, reused rather than reinvented:

  * never ``shell=True``; ``subprocess.run`` receives an argv LIST;
  * ``cwd`` is the resolved worktree (or a validated subdirectory of it);
  * the environment is inherited as-is — no extra vars, no ``.env`` reading;
  * a timeout always applies;
  * output is captured, decoded leniently, and truncated to a tail.

Two guards are specific to this module, because a DoD check can originate from
an LLM rather than from repository discovery:

  * ``lint`` / ``build`` / ``custom_cmd`` name their own executable, so that
    executable must appear in an allowlist — by default the same closed list
    ``test_runner`` is willing to invoke. A refused executable is red with
    reason ``executable_not_allowed`` and NOTHING is run.
  * a check's ``cwd`` must resolve inside the worktree. The schema already
    refuses ``..`` and absolute paths at compile time; this is the second
    check, after symlink resolution, immediately before exec (F017).

``runtime_flow`` (T003) is the one kind that is not a single process. It drives
the F007 runtime harness instead: resolve the project's runtime spec, start the
application the way ``runtime serve`` would, wait for readiness, walk the
declarative steps (v1: open a path, assert on status and/or text), and stop the
application in a ``finally`` — always, on every path. Reused from
``dev_server``: the spec model and its validation, ``choose_port``,
``http_probe`` for readiness, and ``stop_process_tree`` for the terminate-then-
kill sweep. No browser automation and no new dependency: a flow is HTTP GETs
against a loopback port.

A kind with NO runner still fails loud: :func:`runner_for` raises
:class:`UnsupportedCheckKindError` rather than skipping the check or calling it
green. That guarantee is about the registry, not about any one round — it now
protects the next kind added to the schema.
"""
from __future__ import annotations

import contextlib
import os
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.dod_schema import DoD, DoDCheck
from packages.orchestration.test_runner import _EXECUTION_SAFE_EXECUTABLES
from packages.runtimes.dev_server import (
    GRACE_SECONDS,
    READY_STATUS_MAX,
    READY_STATUS_MIN,
    choose_port,
    http_probe,
    stop_process_tree,
)
from packages.runtimes.runtime_config import resolve_spec

#: Default per-check wall clock. A check that cannot finish in five minutes is
#: reported as a timeout, never left to hang a job.
CHECK_TIMEOUT_DEFAULT_SEC = 300

#: How much of the process output survives into the evidence record.
MAX_OUTPUT_TAIL_CHARS = 4000

#: Statuses a check can end in. There is no third, softer option.
STATUS_PASSED = "passed"
STATUS_FAILED = "failed"

#: Named reasons for a red check. Empty on a green one.
REASON_NONE = ""
REASON_NONZERO_EXIT = "nonzero_exit"
REASON_TOOL_UNAVAILABLE = "tool_unavailable"
REASON_TIMEOUT = "timeout"
REASON_EXECUTABLE_NOT_ALLOWED = "executable_not_allowed"
REASON_CWD_OUTSIDE_WORKTREE = "cwd_outside_worktree"
REASON_CWD_MISSING = "cwd_missing"
#: runtime_flow (T003).
REASON_RUNTIME_NOT_CONFIGURED = "runtime_not_configured"
REASON_APP_START_FAILED = "app_start_failed"
REASON_APP_NOT_READY = "app_not_ready"
REASON_APP_STOP_FAILED = "app_stop_failed"
REASON_FLOW_STEP_FAILED = "flow_step_failed"
REASON_UNKNOWN_FLOW_ACTION = "unknown_flow_action"
#: product_smoke (F062). ``not_applicable`` is the honest third answer for a
#: project with no runnable app: reported, and contributed non-blocking so it
#: gates nothing — it is never a pass.
REASON_SMOKE_NOT_APPLICABLE = "smoke_not_applicable"
REASON_SMOKE_START_FAILED = "smoke_start_failed"
REASON_SMOKE_PATH_FAILED = "smoke_path_failed"

#: The ONLY flow action v1 understands: open a path and assert on the answer.
#: A step naming anything else is red — the vocabulary grows deliberately, and
#: an unrecognised action is never treated as satisfied.
FLOW_ACTION_OPEN = "open"

#: Per-step HTTP timeout, and how often readiness is re-probed.
FLOW_STEP_TIMEOUT_S = 10.0
_READY_POLL_SECONDS = 0.15

#: The interpreter that runs ``pytest`` checks. Resolved rather than assumed:
#: inside a virtualenv the ``python3`` on PATH is not necessarily this one.
PYTEST_PYTHON = sys.executable or "python3"

#: Executables a check may name for itself. The closed list test_runner is
#: willing to invoke — deliberately shared, so widening it stays a single,
#: reviewable decision. Callers may pass a different set explicitly.
DEFAULT_ALLOWED_EXECUTABLES = _EXECUTION_SAFE_EXECUTABLES


class UnsupportedCheckKindError(Exception):
    """No runner is registered for this check kind."""


@dataclass(frozen=True)
class CheckEvidence:
    """What one check did, in enough detail to argue about it later."""

    check_id: str
    kind: str
    source: str
    blocking: bool
    status: str
    #: Empty when green; a named reason when red.
    reason: str
    #: The argv, joined for display. Empty when nothing was executed.
    command: str
    argv: tuple[str, ...]
    #: Working directory the process ran in, relative to the worktree.
    cwd: str
    #: None when no process ran (refused, missing tool) or on timeout.
    exit_code: int | None
    duration_ms: int
    output_tail: str
    output_truncated: bool = False

    @property
    def green(self) -> bool:
        return self.status == STATUS_PASSED


# ---------------------------------------------------------------------------
# Argv construction — one builder per runnable kind
# ---------------------------------------------------------------------------

def _pytest_argv(check: DoDCheck) -> list[str]:
    spec = check.spec
    return [PYTEST_PYTHON, "-m", "pytest", str(spec["selector"]),
            *[str(a) for a in spec.get("args", [])], "-q"]


def _tool_argv(check: DoDCheck) -> list[str]:
    """lint and build share a shape: a tool, its args, then its paths."""
    spec = check.spec
    return [str(spec["tool"]),
            *[str(a) for a in spec.get("args", [])],
            *[str(p) for p in spec.get("paths", [])]]


def _custom_argv(check: DoDCheck) -> list[str]:
    return [str(a) for a in check.spec["argv"]]


#: kind -> argv builder, for the kinds that ARE one process. ``runtime_flow``
#: has no argv form: it starts an application and speaks HTTP to it.
ARGV_BUILDERS: dict[str, Callable[[DoDCheck], list[str]]] = {
    "pytest": _pytest_argv,
    "lint": _tool_argv,
    "build": _tool_argv,
    "custom_cmd": _custom_argv,
}

#: Kinds whose executable comes from the check itself and is therefore
#: allowlisted. ``pytest`` is exempt: its argv is built from a fixed template
#: and only the pytest SELECTOR comes from the check.
_ALLOWLISTED_KINDS = frozenset({"lint", "build", "custom_cmd"})


def runner_for(kind: str) -> Callable[[DoDCheck, _RunContext], CheckEvidence]:
    """Return the executor for ``kind``, or fail loud.

    A kind with no runner raises rather than returning a no-op. A check that
    cannot run must never look like one that ran and passed. This guarantee
    outlives any particular round: `runtime_flow` gained its runner in T003,
    and the next kind added to the schema without one fails here.
    """
    runner = RUNNER_REGISTRY.get(kind)
    if runner is None:
        raise UnsupportedCheckKindError(
            f"no runner registered for check kind {kind!r} "
            f"(available: {', '.join(sorted(RUNNER_REGISTRY))})")
    return runner


def build_argv(check: DoDCheck) -> list[str]:
    """The exact argv a single-process check will be executed as."""
    builder = ARGV_BUILDERS.get(check.kind)
    if builder is None:
        raise UnsupportedCheckKindError(
            f"check kind {check.kind!r} is not a single-process check and has "
            f"no argv (argv kinds: {', '.join(sorted(ARGV_BUILDERS))})")
    return builder(check)


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class _RunContext:
    """What every executor needs, threaded in one object rather than five args."""

    root: Path
    timeout_sec: int
    allowed: frozenset[str]


def _resolve_cwd(check: DoDCheck, worktree_root: Path) -> tuple[Path | None, str]:
    """Resolve the check's working directory, or say why it is refused.

    Returns ``(path, "")`` when usable, ``(None, reason)`` otherwise. The
    worktree root itself is resolved first, so a symlinked worktree is compared
    against its real location rather than its alias.
    """
    root = worktree_root.resolve()
    relative = str(check.spec.get("cwd", "") or "").strip()
    candidate = (root / relative).resolve() if relative else root

    if candidate != root and root not in candidate.parents:
        return None, REASON_CWD_OUTSIDE_WORKTREE
    if not candidate.is_dir():
        return None, REASON_CWD_MISSING
    return candidate, ""


def _tail(raw: bytes) -> tuple[str, bool]:
    text = raw.decode("utf-8", errors="replace")
    if len(text) <= MAX_OUTPUT_TAIL_CHARS:
        return text, False
    return text[-MAX_OUTPUT_TAIL_CHARS:], True


def _refused(check: DoDCheck, reason: str, argv: list[str], cwd: str,
             detail: str) -> CheckEvidence:
    """A red result for a check that never reached exec."""
    return CheckEvidence(
        check_id=check.id,
        kind=check.kind,
        source=check.source,
        blocking=check.blocking,
        status=STATUS_FAILED,
        reason=reason,
        command=" ".join(argv),
        argv=tuple(argv),
        cwd=cwd,
        exit_code=None,
        duration_ms=0,
        output_tail=detail,
    )


def _run_process_check(check: DoDCheck, ctx: _RunContext) -> CheckEvidence:
    """Run a check that IS one process: pytest, lint, build, custom_cmd."""
    root = ctx.root
    argv = build_argv(check)
    allowed = ctx.allowed
    declared_cwd = str(check.spec.get("cwd", "") or "")

    if check.kind in _ALLOWLISTED_KINDS and argv[0] not in allowed:
        return _refused(
            check, REASON_EXECUTABLE_NOT_ALLOWED, argv, declared_cwd,
            f"executable {argv[0]!r} is not in the allowed set; nothing was run")

    cwd, cwd_reason = _resolve_cwd(check, root)
    if cwd is None:
        return _refused(
            check, cwd_reason, argv, declared_cwd,
            f"working directory {declared_cwd or '.'!r} is unusable "
            f"under {root}; nothing was run")

    start = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            cwd=str(cwd),
            capture_output=True,
            timeout=ctx.timeout_sec,
            env=os.environ.copy(),
        )
    except FileNotFoundError:
        # The tool is not installed. A missing linter is a RED check with a
        # named reason — never an absent one, and never a pass.
        return _refused(
            check, REASON_TOOL_UNAVAILABLE, argv, declared_cwd,
            f"{argv[0]!r} was not found on PATH")
    except subprocess.TimeoutExpired as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        raw = (exc.stdout or b"") + (exc.stderr or b"") + b"\n[timeout expired]\n"
        tail, truncated = _tail(raw)
        return CheckEvidence(
            check_id=check.id, kind=check.kind, source=check.source,
            blocking=check.blocking, status=STATUS_FAILED, reason=REASON_TIMEOUT,
            command=" ".join(argv), argv=tuple(argv), cwd=declared_cwd,
            exit_code=None, duration_ms=duration_ms, output_tail=tail,
            output_truncated=truncated,
        )

    duration_ms = int((time.monotonic() - start) * 1000)
    tail, truncated = _tail(proc.stdout + proc.stderr)
    passed = proc.returncode == 0
    return CheckEvidence(
        check_id=check.id,
        kind=check.kind,
        source=check.source,
        blocking=check.blocking,
        status=STATUS_PASSED if passed else STATUS_FAILED,
        reason=REASON_NONE if passed else REASON_NONZERO_EXIT,
        command=" ".join(argv),
        argv=tuple(argv),
        cwd=declared_cwd,
        exit_code=proc.returncode,
        duration_ms=duration_ms,
        output_tail=tail,
        output_truncated=truncated,
    )


# ---------------------------------------------------------------------------
# runtime_flow (T003) — start the app, walk the steps, ALWAYS stop it
# ---------------------------------------------------------------------------

def _http_get(url: str, timeout: float) -> tuple[int, str, str]:
    """One HTTP GET returning ``(status, body, error)``. Never raises.

    ``dev_server.http_probe`` answers readiness, where only the status matters.
    A flow step may also assert on TEXT, so this variant returns the body too;
    the error handling deliberately mirrors ``http_probe``.
    """
    import urllib.error
    import urllib.request

    req = urllib.request.Request(url, method="GET")  # noqa: S310 - loopback only
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            return int(resp.status), _decode(resp.read()), ""
    except urllib.error.HTTPError as exc:
        return int(exc.code), _decode(exc.read() if exc.fp else b""), ""
    except urllib.error.URLError as exc:
        return 0, "", str(exc.reason)
    except (TimeoutError, OSError, ValueError) as exc:
        return 0, "", str(exc)


def _decode(raw: bytes) -> str:
    return raw.decode("utf-8", errors="replace")


def _harness_evidence(check: DoDCheck, argv: list[str], reason: str,
                      log: list[str], started: float) -> CheckEvidence:
    """One harness-driven result — a runtime_flow or a product-smoke check.

    Neither is a single process with an exit code, so the run LOG is the
    evidence: it carries what was started, what answered, and what stopped.
    """
    tail, truncated = _tail("\n".join(log).encode("utf-8") + b"\n")
    passed = reason == REASON_NONE
    return CheckEvidence(
        check_id=check.id,
        kind=check.kind,
        source=check.source,
        blocking=check.blocking,
        status=STATUS_PASSED if passed else STATUS_FAILED,
        reason=reason,
        command=" ".join(argv),
        argv=tuple(argv),
        cwd=str(check.spec.get("cwd", "") or ""),
        exit_code=0 if passed else None,
        duration_ms=int((time.monotonic() - started) * 1000),
        output_tail=tail,
        output_truncated=truncated,
    )


def _wait_ready(proc: Any, url: str, deadline: float) -> str:
    """Poll until the app answers, it dies, or we run out of time.

    Returns "" when ready, else the reason. Mirrors the supervisor's readiness
    loop: the process is checked FIRST, so an app that exits during startup is
    reported as a dead app rather than as a timeout.
    """
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            return REASON_APP_START_FAILED
        status, _ = http_probe(url, timeout=2.0)
        if READY_STATUS_MIN <= status <= READY_STATUS_MAX:
            return ""
        time.sleep(_READY_POLL_SECONDS)
    return REASON_APP_NOT_READY


def _walk_steps(steps: list[Any], base_url: str, deadline: float,
                log: list[str]) -> str:
    """Execute the declarative steps in order. Returns "" or a red reason."""
    for i, step in enumerate(steps, 1):
        if time.monotonic() >= deadline:
            log.append(f"step {i}: not reached — the flow ran out of time")
            return REASON_TIMEOUT

        action = str(step.get("action", "")).strip()
        if action != FLOW_ACTION_OPEN:
            log.append(
                f"step {i}: action {action!r} is not supported "
                f"(v1 actions: {FLOW_ACTION_OPEN})")
            return REASON_UNKNOWN_FLOW_ACTION

        path = str(step.get("path", "") or "").strip()
        if not path.startswith("/"):
            log.append(
                f"step {i}: 'open' needs a 'path' starting with '/', "
                f"got {path!r}")
            return REASON_UNKNOWN_FLOW_ACTION

        remaining = max(0.1, min(FLOW_STEP_TIMEOUT_S, deadline - time.monotonic()))
        status, body, error = _http_get(base_url + path, timeout=remaining)
        if error or status == 0:
            log.append(f"step {i}: open {path} -> no response ({error})")
            return REASON_FLOW_STEP_FAILED

        expected_status = step.get("expect_status")
        if expected_status is not None and int(expected_status) != status:
            log.append(
                f"step {i}: open {path} -> {status}, expected {expected_status}")
            return REASON_FLOW_STEP_FAILED

        expected_text = step.get("expect_text")
        if expected_text is not None and str(expected_text) not in body:
            log.append(
                f"step {i}: open {path} -> {status}, but the body does not "
                f"contain {str(expected_text)!r}")
            return REASON_FLOW_STEP_FAILED

        log.append(f"step {i}: open {path} -> {status} OK")
    return ""


def _walk_smoke_paths(paths: list[Any], base_url: str, deadline: float,
                      log: list[str]) -> str:
    """Probe the smoke's core paths. Returns "" or a red reason.

    Stricter than a runtime_flow step by design: where a flow only asserts what
    it declares, a smoke path with NO declared expectation must still answer
    with an OK status. "It responded 500" is not a product that responds.
    """
    for i, entry in enumerate(paths, 1):
        if time.monotonic() >= deadline:
            log.append(f"path {i}: not reached — the smoke ran out of time")
            return REASON_TIMEOUT

        path = str(entry.get("path", "") or "")
        remaining = max(0.1, min(FLOW_STEP_TIMEOUT_S, deadline - time.monotonic()))
        status, body, error = _http_get(base_url + path, timeout=remaining)
        if error or status == 0:
            log.append(f"path {path} -> no response ({error})")
            return REASON_SMOKE_PATH_FAILED

        expected = entry.get("expect_status")
        if expected is not None:
            if int(expected) != status:
                log.append(f"path {path} -> {status}, expected {expected}")
                return REASON_SMOKE_PATH_FAILED
        elif not (READY_STATUS_MIN <= status <= READY_STATUS_MAX):
            log.append(f"path {path} -> {status}, expected an OK status")
            return REASON_SMOKE_PATH_FAILED

        marker = entry.get("expect_text")
        if marker is not None and str(marker) not in body:
            log.append(
                f"path {path} -> {status}, but the body does not contain "
                f"{str(marker)!r}")
            return REASON_SMOKE_PATH_FAILED

        log.append(f"path {path} -> {status} OK")
    return ""


def _stop_app(proc: Any, log: list[str]) -> str:
    """Stop the application family. Always called, also on failure.

    Delegates to ``dev_server.stop_process_tree`` — the same terminate-then-kill
    sweep the supervisor uses, including the second pass that catches a child
    spawned during shutdown. A survivor is a RED result even when the flow
    itself passed: a leaked process is not a clean run.
    """
    session_id = 0
    with contextlib.suppress(OSError, ProcessLookupError):
        session_id = os.getpgid(proc.pid)
    result = stop_process_tree(proc.pid, session_id=session_id)
    with contextlib.suppress(Exception):
        proc.wait(timeout=GRACE_SECONDS)

    survivors = list(result.get("survivors") or [])
    if survivors:
        log.append(f"stop: processes survived the cleanup: {survivors}")
        return REASON_APP_STOP_FAILED
    log.append("stop: the application family was stopped")
    return ""


@dataclass
class _AppRun:
    """One start-probe-stop cycle against the harness."""

    argv: list[str]
    reason: str
    #: The human sentence for ``reason`` — what a reader is actually told.
    detail: str = ""


def _run_app_once(spec: Any, deadline: float, log: list[str],
                  body: Callable[[str], str] | None) -> _AppRun:
    """Start the app, wait for readiness, run ``body``, and ALWAYS stop it.

    The single place that owns the harness process discipline for a DoD check:
    ``choose_port``, start in its own session, ``_wait_ready``, then
    ``stop_process_tree`` in a ``finally`` — on success, on failure, and on an
    exception alike. ``runtime_flow`` passes the step walker as ``body``; the
    product-smoke ``app_starts`` check passes ``None``, because for it the
    successful readiness probe IS the check.
    """
    port = choose_port(spec.port, spec.host)
    argv = spec.resolved_cmd(port)
    base_url = f"http://{spec.host}:{port}"
    log.append(f"$ {' '.join(argv)}  (cwd={spec.cwd}, port={port})")

    # The app's own output goes to a private temporary file, never a pipe: an
    # ephemeral run has no log-pump thread to drain a pipe, and a chatty app
    # would block on a full one. It is never written into the user's repo.
    with tempfile.TemporaryDirectory(prefix="remedy-dod-app-") as tmp:
        app_log = Path(tmp) / "app.log"
        try:
            handle = app_log.open("wb")
        except OSError as exc:
            detail = f"could not open the app log: {exc}"
            log.append(detail)
            return _AppRun(argv, REASON_APP_START_FAILED, detail)

        proc = None
        reason = REASON_NONE
        detail = ""
        try:
            try:
                proc = subprocess.Popen(  # noqa: S603 - argv list, never a shell
                    argv, cwd=spec.cwd, env=spec.resolved_env(port),
                    stdout=handle, stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    # Its own session, so the family can be killed whole without
                    # this process signalling itself — the supervisor's rule.
                    start_new_session=True,
                )
            except (OSError, ValueError) as exc:
                detail = f"the application could not be started: {exc}"
                log.append(detail)
                reason = REASON_APP_START_FAILED
            else:
                ready_deadline = min(
                    deadline, time.monotonic() + spec.ready_timeout_s)
                reason = _wait_ready(
                    proc, base_url + spec.health_path, ready_deadline)
                if reason == REASON_APP_START_FAILED:
                    detail = (f"the application exited before it answered "
                              f"{spec.health_path} (exit code {proc.returncode})")
                    log.append(detail)
                elif reason:
                    detail = (f"the application never became ready on "
                              f"{spec.health_path} within {spec.ready_timeout_s}s")
                    log.append(detail)
                else:
                    log.append(f"ready on {spec.health_path}")
                    if body is not None:
                        reason = body(base_url)
        finally:
            # ALWAYS stopped: success, red outcome, or an exception on the way
            # out. A stop failure only overrides a reason when the run itself
            # was green — a leaked process must never read as a clean run.
            if proc is not None:
                stop_reason = _stop_app(proc, log)
                if not reason and stop_reason:
                    reason, detail = stop_reason, "the application family survived cleanup"
            with contextlib.suppress(Exception):
                handle.close()
            with contextlib.suppress(OSError):
                app_tail, _ = _tail(app_log.read_bytes())
                if app_tail.strip():
                    log.append("--- application log ---")
                    log.append(app_tail)

    return _AppRun(argv, reason, detail)


def _run_runtime_flow(check: DoDCheck, ctx: _RunContext) -> CheckEvidence:
    """Drive the F007 runtime harness through one declarative flow.

    Start the app the way the project's runtime configuration says to start it,
    wait for readiness, walk the steps, and stop the app — in a ``finally``, so
    it is stopped on every path including an exception. No browser, no new
    dependency: a flow is HTTP GETs against a loopback port.
    """
    started = time.monotonic()
    deadline = started + ctx.timeout_sec
    log: list[str] = []

    try:
        spec = resolve_spec(ctx.root)
    except Exception as exc:
        return _refused(
            check, REASON_RUNTIME_NOT_CONFIGURED, [], "",
            f"the runtime harness cannot start this project: {exc}")

    run = _run_app_once(
        spec, deadline, log,
        lambda base_url: _walk_steps(check.spec["steps"], base_url, deadline, log))
    return _harness_evidence(check, run.argv, run.reason, log, started)


def _run_product_smoke(check: DoDCheck, ctx: _RunContext) -> CheckEvidence:
    """F062 — the product-smoke block's checks.

    v1 runs ``app_starts``: the app the project declares actually starts and
    answers its health path inside the configured readiness window. A flaky
    start gets ONE retry after a short backoff, and a pass that needed it says
    so (``passed on retry``) rather than reading like a clean first attempt.

    A project with no runnable app is NOT gated: the check reports
    ``smoke_not_applicable`` and, being contributed non-blocking, is reported
    without holding anything. Never silently green.
    """
    from packages.orchestration.product_smoke import (
        NOT_APPLICABLE_MESSAGE,
        PASSED_ON_RETRY,
        RETRY_BACKOFF_SECONDS,
        resolve_runtime,
    )

    started = time.monotonic()
    deadline = started + ctx.timeout_sec
    log: list[str] = []

    spec, why = resolve_runtime(ctx.root)
    if spec is None:
        return _refused(
            check, REASON_SMOKE_NOT_APPLICABLE, [], "",
            f"{NOT_APPLICABLE_MESSAGE}: {why}")

    # Each smoke check needs the app up; what it does once up is its own body.
    # `app_starts` has none — for it, the successful readiness probe IS the
    # check.
    smoke = str(check.spec.get("smoke", "")).strip()
    body = None
    if smoke == "core_paths_respond":
        def body(base_url: str) -> str:  # noqa: E306 - paired with the branch
            return _walk_smoke_paths(
                check.spec["paths"], base_url, deadline, log)

    attempts = 2 if bool(check.spec.get("retry", True)) else 1
    run = _AppRun([], REASON_NONE)
    for attempt in range(1, attempts + 1):
        if attempt > 1:
            log.append(
                f"attempt {attempt - 1} failed; retrying once after "
                f"{RETRY_BACKOFF_SECONDS}s backoff")
            time.sleep(RETRY_BACKOFF_SECONDS)
        run = _run_app_once(spec, deadline, log, body)
        if not run.reason:
            if attempt > 1:
                log.append(PASSED_ON_RETRY)
            return _harness_evidence(check, run.argv, REASON_NONE, log, started)
        if run.reason == REASON_SMOKE_PATH_FAILED:
            # The app came up; a path answered wrongly. Retrying the START
            # would not change that, and would hide a real product failure.
            break

    if run.reason == REASON_SMOKE_PATH_FAILED:
        return _harness_evidence(
            check, run.argv, REASON_SMOKE_PATH_FAILED, log, started)

    # Concrete, not vague: the finding names the probe reason the harness gave.
    log.append(f"start failed: {run.detail or run.reason}")
    return _harness_evidence(
        check, run.argv, REASON_SMOKE_START_FAILED, log, started)


#: kind -> executor. Every kind the schema accepts and this build can run.
RUNNER_REGISTRY: dict[str, Callable[[DoDCheck, _RunContext], CheckEvidence]] = {
    "pytest": _run_process_check,
    "lint": _run_process_check,
    "build": _run_process_check,
    "custom_cmd": _run_process_check,
    "runtime_flow": _run_runtime_flow,
    "product_smoke": _run_product_smoke,
}


def run_check(
    check: DoDCheck,
    worktree_root: Path | str,
    *,
    timeout_sec: int = CHECK_TIMEOUT_DEFAULT_SEC,
    allowed_executables: frozenset[str] | set[str] | None = None,
) -> CheckEvidence:
    """Run one check inside the worktree and return its evidence.

    Raises :class:`UnsupportedCheckKindError` for a kind with no runner — that
    is a wiring bug or an unimplemented round, and it is not something to paper
    over with a red result.
    """
    ctx = _RunContext(
        root=Path(worktree_root),
        timeout_sec=timeout_sec,
        allowed=(DEFAULT_ALLOWED_EXECUTABLES if allowed_executables is None
                 else frozenset(allowed_executables)),
    )
    return runner_for(check.kind)(check, ctx)


def run_checks(
    dod: DoD,
    worktree_root: Path | str,
    *,
    timeout_sec: int = CHECK_TIMEOUT_DEFAULT_SEC,
    allowed_executables: frozenset[str] | set[str] | None = None,
) -> list[CheckEvidence]:
    """Run every check in a DoD, in order, and return the evidence.

    Deliberately returns evidence and nothing else: deciding what a red
    blocking check MEANS for a job is the job-end gate's business (T004), not
    the runner's.
    """
    return [
        run_check(check, worktree_root, timeout_sec=timeout_sec,
                  allowed_executables=allowed_executables)
        for check in dod.checks
    ]
