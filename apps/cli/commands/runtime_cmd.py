"""`remedy runtime` — start, probe and stop the project's dev server (F007).

Exit-code contract (stable):

    0  success
    2  configuration error   (no/ambiguous/unsafe/mismatched runtime spec)
    3  startup error         (the process could not start, or died before readiness)
    4  readiness error       (the health URL never answered in time)
    5  lifecycle/state error (stop failure, surviving startup rollback, corrupt or
                              unprovable runtime state, lifecycle lock busy)

Every lifecycle transition — read state, verify identity, start/stop, commit — runs
under the project's lifecycle lock, so serve/probe/stop can never create a duplicate
runtime or orphan one. `serve` reports a runtime as running only AFTER HTTP readiness.

No provider call, no shell, no Docker, no SSE (F008), no project registry (F146).
"""
from __future__ import annotations

import contextlib
import json as _json
import os
import sys
from pathlib import Path
from typing import Any

EXIT_CONFIG = 2
EXIT_START = 3
EXIT_READY = 4
EXIT_STATE = 5          # lifecycle/state failure: stop failed, survivors, bad state
EXIT_STOP = EXIT_STATE  # kept for readers of the previous contract


def _fail(message: str, code: int, *, json_output: bool,
          payload: dict | None = None) -> None:
    if json_output:
        print(_json.dumps({"ok": False, "error": message, **(payload or {})}, indent=2))
    else:
        print(f"Error: {message}", file=sys.stderr)
    sys.exit(code)


def _resolve(repo: str, json_output: bool):
    from packages.runtimes.dev_server import RuntimeConfigError
    from packages.runtimes.runtime_config import resolve_spec

    root = Path(repo or ".").resolve()
    try:
        return root, resolve_spec(root)
    except RuntimeConfigError as exc:
        _fail(str(exc), EXIT_CONFIG, json_output=json_output,
              payload={"error_class": "config"})
    return None, None       # unreachable


def _state_guard(root, json_output: bool):
    """Read runtime.json WITH its type. A corrupt/unreadable state is a hard stop.

    "I cannot read the state" must never be treated as "there is no runtime": that is
    exactly how a second server gets started beside a live one.
    """
    from packages.runtimes.dev_server import (
        STATE_CORRUPT,
        STATE_UNREADABLE,
        load_state_result,
    )

    load = load_state_result(root)
    if load.kind in (STATE_CORRUPT, STATE_UNREADABLE):
        _fail(
            f"runtime state is {load.kind}: {load.error}. Refusing to start or stop "
            f"anything; inspect {load.path} manually.",
            EXIT_STATE, json_output=json_output,
            payload={"error_class": "state", "state": load.to_json()},
        )
    return load


def _serve_supervisor(root, spec, json_output: bool):
    """Start the PERSISTENT supervisor and wait for its bounded handshake.

    `serve` is short-lived; the supervisor is not. It owns the application and the
    bounded log pump for the whole life of the served runtime, so the server keeps
    running (and logging) after this CLI process exits — which is exactly what the
    old in-CLI ownership could not do.
    """
    import json
    import subprocess
    import sys as _sys
    import time

    from packages.runtimes import runtime_supervisor as SUP
    from packages.runtimes.dev_server import (
        STATUS_RUNNING,
        choose_port,
        classify_state,
        classify_supervisor,
        handshake_path,
        load_state,
        runtime_dir,
        stop_process_tree,
        stop_request_path,
    )

    rdir = runtime_dir(root)
    rdir.mkdir(parents=True, exist_ok=True)
    hs = handshake_path(root)
    for stale in (hs, stop_request_path(root)):
        with contextlib.suppress(OSError):
            stale.unlink()

    port = choose_port(spec.port, spec.host)
    spec_file = rdir / "runtime.spec.json"
    spec_file.write_text(json.dumps({**spec.to_json(), "env": dict(spec.env)},
                                    indent=2), encoding="utf-8")

    env = dict(os.environ)
    env["REMEDY_RUNTIME_PORT"] = str(port)
    source_root = Path(__file__).resolve().parents[3]      # the Remedy checkout

    proc = subprocess.Popen(              # noqa: S603 - argv, never a shell
        [_sys.executable, "-m", "packages.runtimes.runtime_supervisor",
         "--repo", str(root), "--spec", str(spec_file), "--handshake", str(hs)],
        cwd=str(source_root), env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        start_new_session=True,           # its OWN session: not our process group
    )

    deadline = time.monotonic() + min(SUP.HANDSHAKE_TIMEOUT_S,
                                      spec.ready_timeout_s + 30.0)
    payload = None
    while time.monotonic() < deadline:
        payload = SUP.read_handshake(hs)
        if payload is not None:
            break
        if proc.poll() is not None and SUP.read_handshake(hs) is None:
            payload = {"ok": False, "error_class": "start",
                       "error": (f"supervisor exited with code {proc.returncode} "
                                 f"before reporting")}
            break
        time.sleep(0.05)

    if payload is None:
        # Handshake timeout: the supervisor is not to be left running blind.
        cleanup = stop_process_tree(proc.pid)
        _fail(f"supervisor handshake timed out after "
              f"{int(deadline - time.monotonic() + spec.ready_timeout_s)}s",
              EXIT_STATE if cleanup["survivors"] else EXIT_READY,
              json_output=json_output,
              payload={"error_class": "handshake",
                       "survivors": cleanup["survivors"]})
        return None

    with contextlib.suppress(OSError):
        hs.unlink()

    if not payload.get("ok"):
        cls = payload.get("error_class", "start")
        survivors = payload.get("survivors") or []
        code = (EXIT_STATE if survivors or cls == "state"
                else EXIT_START if cls == "start" else EXIT_READY)
        _fail(str(payload.get("error", "supervisor failed")), code,
              json_output=json_output,
              payload={"error_class": cls, "survivors": survivors,
                       "log_tail": payload.get("log_tail", ""),
                       "cleanup": payload.get("cleanup", {})})
        return None

    # The CLI only reports success once a DURABLE `running` state exists whose
    # supervisor and application identities are both verified.
    state = load_state(root)
    app = classify_state(state, root)
    sup = classify_supervisor(state, root)
    if (state is None or state.status != STATUS_RUNNING or not app.verified
            or not sup.verified
            or state.supervisor_pid != payload.get("supervisor_pid")
            or state.pid != payload.get("app_pid")):
        _fail("supervisor reported success but no verified running state exists",
              EXIT_STATE, json_output=json_output,
              payload={"error_class": "state",
                       "app_identity": app.to_json(),
                       "supervisor_identity": sup.to_json()})
        return None
    return state, payload


def _cmd_runtime_serve(repo: str = ".", *, json_output: bool = False) -> None:
    """Start a PERSISTENT dev server and return; the supervisor keeps it alive.

    The transition — read state, verify identity, start the supervisor, wait for its
    handshake, confirm a durable `running` record — happens under the project
    lifecycle lock, so a second serve can never duplicate a runtime, attach to a
    temporary probe runtime, or report `already_running` for a runtime that has not
    become ready.
    """
    from packages.runtimes.dev_server import (
        DEFINITELY_GONE,
        PID_REUSED,
        STATUS_PROBING,
        STATUS_RUNNING,
        STATUS_STARTING,
        RuntimeLockError,
        classify_state,
        classify_supervisor,
        lifecycle_lock,
    )

    root, spec = _resolve(repo, json_output)

    try:
        with lifecycle_lock(root):
            load = _state_guard(root, json_output)
            existing = load.state
            check = classify_state(existing, root)

            if existing is not None and check.verified:
                status = existing.status

                if status == STATUS_RUNNING:
                    if (existing.spec_fingerprint
                            and existing.spec_fingerprint != spec.fingerprint()):
                        _fail(
                            "runtime_spec_mismatch: a different runtime is already "
                            f"running for this project (pid {existing.pid}, port "
                            f"{existing.port}). Run `remedy runtime stop` first.",
                            EXIT_CONFIG, json_output=json_output,
                            payload={"error_class": "config",
                                     "running": existing.to_json()},
                        )
                        return
                    payload = {"ok": True, "already_running": True,
                               **existing.to_json()}
                    if json_output:
                        print(_json.dumps(payload, indent=2))
                    else:
                        print(f"Runtime already running (pid {existing.pid}) on "
                              f"{existing.url}\n  Log: {existing.log_path}")
                    return

                if status == STATUS_STARTING:
                    # A bare `starting` state is NOT success. Who owns it?
                    sup = classify_supervisor(existing, root)
                    if sup.verified:
                        _fail(
                            "runtime_start_in_progress: a supervisor (pid "
                            f"{existing.supervisor_pid}) is still starting this "
                            f"runtime. Wait, or run `remedy runtime stop`.",
                            EXIT_STATE, json_output=json_output,
                            payload={"error_class": "state",
                                     "runtime_status": STATUS_STARTING,
                                     "starting": existing.to_json()},
                        )
                        return
                    _fail(
                        "interrupted_start: a `starting` runtime has no live "
                        "supervisor. Nothing was started; run `remedy runtime stop` "
                        "to clean it up.",
                        EXIT_STATE, json_output=json_output,
                        payload={"error_class": "state",
                                 "runtime_status": "interrupted_start",
                                 "interrupted": existing.to_json()},
                    )
                    return

                if status == STATUS_PROBING:
                    _fail(
                        "a one-shot probe currently owns this runtime; a permanent "
                        "serve will not attach to it. Try again shortly.",
                        EXIT_STATE, json_output=json_output,
                        payload={"error_class": "state",
                                 "runtime_status": STATUS_PROBING},
                    )
                    return

                _fail(
                    f"runtime state is {status!r}: {existing.stop_error or ''} "
                    f"Run `remedy runtime stop` to clean it up.",
                    EXIT_STATE, json_output=json_output,
                    payload={"error_class": "state", "runtime_status": status,
                             "state": existing.to_json()},
                )
                return

            if (existing is not None
                    and check.classification not in (DEFINITELY_GONE, PID_REUSED)):
                _fail(
                    f"runtime state cannot be trusted ({check.classification}): "
                    f"{check.reason}. Nothing was started; run `remedy runtime stop` "
                    f"or clean up manually.",
                    EXIT_STATE, json_output=json_output,
                    payload={"error_class": "state", "identity": check.to_json()},
                )
                return

            started = _serve_supervisor(root, spec, json_output)
            if started is None:
                return
            state, handshake = started
    except RuntimeLockError as exc:
        _fail(str(exc), EXIT_STATE, json_output=json_output,
              payload={"error_class": "lock"})
        return

    payload = {
        "ok": True, "already_running": False, **state.to_json(),
        "status_code": handshake.get("status_code", 0),
    }
    if json_output:
        print(_json.dumps(payload, indent=2))
    else:
        print(f"Runtime started (app pid {state.pid}, "
              f"supervisor pid {state.supervisor_pid})")
        print(f"  Port: {state.port}")
        print(f"  URL:  {state.url}")
        print(f"  Log:  {state.log_path}")
        print(f"  Spec: {spec.source}")


def _cmd_runtime_probe(repo: str = ".", *, json_output: bool = False) -> None:
    """One-shot probe.

    A probe that has to CREATE a server owns its whole bounded lifecycle — start,
    readiness, probe, stop, cleanup — under the lifecycle lock, so two concurrent
    probes can never leave two servers running. A probe of an already-served runtime
    takes its decision under the lock and then performs the short HTTP request
    without owning that server's lifetime.
    """
    from packages.runtimes.dev_server import (
        DevServer,
        RuntimeLockError,
        RuntimeProbeResult,
        RuntimeStartError,
        classify_state,
        http_probe,
        lifecycle_lock,
    )

    root, spec = _resolve(repo, json_output)
    served = None

    try:
        with lifecycle_lock(root):
            load = _state_guard(root, json_output)
            existing = load.state
            check = classify_state(existing, root)

            if check.verified and existing is not None:
                served = existing
            elif existing is not None and not check.may_auto_clear:
                _fail(
                    f"runtime state cannot be trusted ({check.classification}): "
                    f"{check.reason}. Nothing was started or stopped.",
                    EXIT_STATE, json_output=json_output,
                    payload={"error_class": "state", "identity": check.to_json()},
                )
                return

            if served is None:
                # This probe owns the server it creates, from start to cleanup.
                server = DevServer(spec, root)
                try:
                    server.start()
                except RuntimeStartError as exc:
                    rollback = getattr(exc, "rollback", {}) or {}
                    code = EXIT_STATE if rollback.get("survivors") else EXIT_START
                    _fail(str(exc), code, json_output=json_output,
                          payload={"error_class": "start", "rollback": rollback})
                    return

                result = server.wait_ready()
                if result.ok:
                    result = server.probe()
                stop = server.stop()
                survivors = stop.get("survivors", [])

                payload = {**result.to_json(), "managed_by_serve": False,
                           "stopped": not survivors, "survivors": survivors}
                if survivors:
                    payload["ok"] = False
                    payload["error"] = (
                        f"managed processes survived the probe cleanup: {survivors}")
                    payload["error_class"] = "stop"
                    if json_output:
                        print(_json.dumps(payload, indent=2))
                    else:
                        print(f"Probe cleanup FAILED: survivors {survivors}",
                              file=sys.stderr)
                    sys.exit(EXIT_STATE)

                if json_output:
                    print(_json.dumps(payload, indent=2))
                else:
                    if result.ok:
                        print(f"Probe OK: {result.url} (status {result.status_code}, "
                              f"{result.elapsed_s:.2f}s); server stopped again")
                    else:
                        print(f"Probe FAILED: {result.error}", file=sys.stderr)
                        if result.log_tail:
                            print(result.log_tail[-2000:], file=sys.stderr)
                if not result.ok:
                    sys.exit(EXIT_START if result.error_class == "start"
                             else EXIT_READY)
                return
    except RuntimeLockError as exc:
        _fail(str(exc), EXIT_STATE, json_output=json_output,
              payload={"error_class": "lock"})
        return

    # An already-served runtime: a short HTTP request, no lifecycle ownership.
    status, err = http_probe(served.url, timeout=3.0)
    good = 200 <= status <= 399
    result = RuntimeProbeResult(
        ok=good, status_code=status, url=served.url, port=served.port,
        error="" if good else (err or f"health status {status}"),
        error_class="" if good else "ready", pid=served.pid,
        log_error=served.log_error,
    )
    payload = {**result.to_json(), "managed_by_serve": True, "stopped": False}
    if json_output:
        print(_json.dumps(payload, indent=2))
    else:
        print(f"Probe {'OK' if good else 'FAILED'}: {served.url} "
              f"(pid {served.pid}, still running)")
    if not good:
        sys.exit(EXIT_READY)


def _cmd_runtime_stop(repo: str = ".", *, json_output: bool = False) -> None:
    """Stop the managed server's whole process tree. Idempotent, and honest.

    Nothing is killed unless the recorded runtime's identity — including its LIVE
    process group and session — is fully verified. A survivor keeps a retryable
    `stop_failed` state and exits 5; so does a corrupt, unreadable or unprovable
    state, which is never silently deleted.
    """
    from packages.runtimes.dev_server import RuntimeLockError, stop_recorded_runtime

    root = Path(repo or ".").resolve()
    try:
        result = stop_recorded_runtime(root)
    except RuntimeLockError as exc:
        _fail(str(exc), EXIT_STATE, json_output=json_output,
              payload={"error_class": "lock"})
        return

    ok = bool(result.get("ok"))
    survivors = result.get("survivors") or []

    if json_output:
        print(_json.dumps(result, indent=2))
    elif survivors:
        print(f"Runtime stop FAILED: {result.get('stop_error')}", file=sys.stderr)
        print(f"  Survivors: {survivors}", file=sys.stderr)
        print("  State kept as stop_failed; run `remedy runtime stop` again.",
              file=sys.stderr)
    elif not ok:
        print(f"Runtime NOT stopped: {result.get('reason')}", file=sys.stderr)
        print("  Nothing was killed and the runtime state was kept.", file=sys.stderr)
        print("  Resolve the identity/state problem, then stop again.",
              file=sys.stderr)
    elif result.get("stopped"):
        print(f"Runtime stopped (pid {result.get('pid')}).")
    else:
        print(f"No runtime running ({result.get('reason', 'nothing recorded')}).")

    if not ok:
        sys.exit(EXIT_STATE)


COMMAND_HANDLERS = {
    "runtime.serve": lambda args: _cmd_runtime_serve(
        getattr(args, "repo", None) or ".",
        json_output=getattr(args, "json", False),
    ),
    "runtime.probe": lambda args: _cmd_runtime_probe(
        getattr(args, "repo", None) or ".",
        json_output=getattr(args, "json", False),
    ),
    "runtime.stop": lambda args: _cmd_runtime_stop(
        getattr(args, "repo", None) or ".",
        json_output=getattr(args, "json", False),
    ),
}
