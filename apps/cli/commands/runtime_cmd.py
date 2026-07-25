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
        LOG_FAILURE_STATUSES,
        OWNER_SUPERVISED,
        STATUS_EXITED,
        STATUS_RUNNING,
        _pid_alive,
        atomic_write_text,
        choose_port,
        classify_runtime,
        clear_state,
        ensure_runtime_dir,
        handshake_path,
        load_state,
        log_failure_note_path,
        new_instance_id,
        project_digest,
        read_log_tail,
        spec_file_path,
        stop_process_tree,
        stop_request_path,
    )

    ensure_runtime_dir(root)              # 0700 directory, owner-only artifacts
    hs = handshake_path(root)
    # A new instance inherits nothing: no stale handshake, no stale stop request, and no
    # emergency note from a runtime that is already gone. (A note whose survivor still
    # matters cannot be reached here — such a state blocks `serve` before this point.)
    for stale in (hs, stop_request_path(root), log_failure_note_path(root)):
        with contextlib.suppress(OSError):
            stale.unlink()

    instance_id = new_instance_id()      # binds state, argv, handshake, stop request
    port = choose_port(spec.port, spec.host)
    # The spec carries the runtime ENV, so it is written 0600 and the supervisor
    # deletes it the moment it has read it.
    spec_file = spec_file_path(root)
    atomic_write_text(spec_file,
                      json.dumps({**spec.to_json(), "env": dict(spec.env)}, indent=2))

    env = dict(os.environ)
    env["REMEDY_RUNTIME_PORT"] = str(port)
    source_root = Path(__file__).resolve().parents[3]      # the Remedy checkout

    try:
        proc = subprocess.Popen(          # noqa: S603 - argv, never a shell
            [_sys.executable, "-m", "packages.runtimes.runtime_supervisor",
             "--repo", str(root), "--spec", str(spec_file), "--handshake", str(hs),
             "--instance", instance_id],
            cwd=str(source_root), env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,       # its OWN session: not our process group
        )
    except (OSError, ValueError) as exc:
        with contextlib.suppress(OSError):
            spec_file.unlink()            # no supervisor will ever ingest it
        _fail(f"the supervisor could not be started: {type(exc).__name__}: {exc}",
              EXIT_START, json_output=json_output,
              payload={"error_class": "start"})
        return None

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
        # Handshake timeout. The only pid this CLI may act on is the one its OWN Popen
        # returned — never a number read out of a file.
        cleanup = stop_process_tree(proc.pid)
        _cleanup_control_files(root)
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
        _cleanup_control_files(root)
        _fail(str(payload.get("error", "supervisor failed")), code,
              json_output=json_output,
              payload={"error_class": cls, "survivors": survivors,
                       "log_tail": payload.get("log_tail", ""),
                       "cleanup": payload.get("cleanup", {})})
        return None

    # --- the handshake itself must prove WHO wrote it -------------------------
    # A success payload is only believed when it carries the instance id this CLI
    # generated and the supervisor pid its own Popen returned. Anything else is a
    # stale or forged file, and no pid inside it is ever used as a kill target.
    if (payload.get("instance_id") != instance_id
            or payload.get("supervisor_pid") != proc.pid):
        cleanup = _retire_own_supervisor(root, proc, instance_id)
        _fail(
            "the runtime handshake does not belong to this serve "
            f"(instance {payload.get('instance_id')!r}, supervisor pid "
            f"{payload.get('supervisor_pid')!r}); nothing outside this command's own "
            "supervisor was touched"
            + ("" if not cleanup["survivors"]
               else f". Cleanup left survivors {cleanup['survivors']}: "
                    "stop them manually"),
            EXIT_STATE, json_output=json_output,
            payload={"error_class": "state", "survivors": cleanup["survivors"],
                     "manual_cleanup": cleanup["manual_cleanup"]})
        return None

    # The CLI only reports success once a DURABLE `running` state exists that the ONE
    # identity contract calls supervised — and if that check fails, the CLI owns the
    # cleanup of the supervisor it just created.
    state = load_state(root)

    # ...but first: is this OUR runtime, and did it already reach a KNOWN terminal
    # state? The supervisor can write its success handshake and then, microseconds
    # later, discover that its log pump is dead — or watch the application exit. It
    # records exactly what happened. Throwing that away and reporting "no verified
    # running state exists" would replace a precise diagnosis with a shrug, and would
    # delete the record a later probe/stop needs. A known terminal state of OUR OWN
    # instance is therefore reported as it is, and kept.
    ours = (state is not None
            and state.instance_id == instance_id
            and state.supervisor_pid == proc.pid
            and state.project_id == project_digest(root))
    if ours and state.status in (*LOG_FAILURE_STATUSES, STATUS_EXITED):
        _cleanup_control_files(root)
        survivors = [p for p in state.survivors if _pid_alive(p)]
        _fail(
            f"{state.status}: "
            + (state.stop_error or state.log_error
               or f"the runtime reached {state.status!r} right after it started")
            + ("" if not survivors
               else f"; processes survived: {survivors} — stop them manually"),
            EXIT_STATE, json_output=json_output,
            payload={
                "error_class": "state",
                "runtime_status": state.status,
                "log_error": state.log_error,
                "stop_error": state.stop_error,
                "app_exit_code": state.app_exit_code,
                "survivors": survivors,
                "manual_cleanup": survivors,
                "log_tail": read_log_tail(state.log_path) if state.log_path else "",
            })
        return None

    ident = classify_runtime(state, root)
    bad = (state is None or state.status != STATUS_RUNNING
           or ident.ownership != OWNER_SUPERVISED
           or state.instance_id != instance_id
           or state.supervisor_pid != proc.pid)
    if bad:
        cleanup = _retire_own_supervisor(root, proc, instance_id)
        if not cleanup["survivors"]:
            clear_state(root)
        _fail(
            "supervisor reported success but no verified running state exists; "
            + ("the runtime it created was stopped"
               if not cleanup["survivors"] else
               f"cleanup left survivors {cleanup['survivors']} — stop them manually"),
            EXIT_STATE, json_output=json_output,
            payload={"error_class": "state", "survivors": cleanup["survivors"],
                     "manual_cleanup": cleanup["manual_cleanup"],
                     "identity": ident.to_json()})
        return None
    return state, payload


def _cleanup_control_files(root) -> None:
    """Leave no handshake, stop request or spec (which carries the env) behind."""
    from packages.runtimes.dev_server import (
        handshake_path,
        spec_file_path,
        stop_request_path,
    )

    for path in (handshake_path(root), stop_request_path(root), spec_file_path(root)):
        with contextlib.suppress(OSError):
            path.unlink()


def _retire_own_supervisor(root, proc, instance_id: str) -> dict:
    """Stop the supervisor THIS command created — and let IT stop its application.

    The only process identities this CLI may act on directly are the supervisor pid its
    own ``Popen`` returned and the instance id it generated itself. An application pid
    that merely appeared in a handshake payload has been proven to be nothing, so it is
    never a kill target: instead the supervisor is asked (by a private stop request
    bound to the instance id) to shut its own application down, and only a FULLY
    verified durable state may afterwards be used to finish the job. If neither is
    possible, the survivors are reported for manual cleanup rather than guessed at.
    """
    import time

    from packages.runtimes.dev_server import (
        _pid_alive,
        atomic_write_text,
        load_state,
        stop_process_tree,
        stop_request_path,
    )

    survivors: list[int] = []

    # 1. ask our own supervisor to stop its runtime, bound to our instance id
    req = stop_request_path(root)
    with contextlib.suppress(OSError):
        atomic_write_text(req, f"{instance_id}\n")

    # 2. wait for it to go
    deadline = time.monotonic() + 15.0
    while time.monotonic() < deadline and _pid_alive(proc.pid):
        time.sleep(0.1)

    # 3. it is our own child: if it will not leave, its own process TREE may be
    #    signalled — the application is a descendant of it, so ownership is a fact of
    #    the live process table here, not a claim read out of a file.
    if _pid_alive(proc.pid):
        result = stop_process_tree(proc.pid)
        survivors.extend(result.get("survivors") or [])
    with contextlib.suppress(Exception):
        proc.wait(timeout=1.0)

    # 4. whatever is left: report it. With the supervisor gone, no live relationship can
    #    prove that a recorded pid is still ours, and guessing one is exactly how an
    #    unrelated process gets killed.
    manual: list[int] = []
    state = load_state(root)
    if state is not None and state.pid and _pid_alive(state.pid):
        manual.append(state.pid)

    _cleanup_control_files(root)
    return {"survivors": sorted({p for p in survivors if _pid_alive(p)}),
            "manual_cleanup": sorted(set(manual))}


def _cmd_runtime_serve(repo: str = ".", *, json_output: bool = False) -> None:
    """Start a PERSISTENT dev server and return; the supervisor keeps it alive.

    The transition — read state, verify identity, start the supervisor, wait for its
    handshake, confirm a durable `running` record — happens under the project
    lifecycle lock, so a second serve can never duplicate a runtime, attach to a
    temporary probe runtime, or report `already_running` for a runtime that has not
    become ready.
    """
    from packages.runtimes.dev_server import (
        LOG_FAILURE_STATUSES,
        OWNER_GONE,
        OWNER_SUPERVISOR_MISSING,
        STATUS_PROBING,
        STATUS_RUNNING,
        STATUS_STARTING,
        STATUS_SUPERVISOR_MISSING,
        RuntimeLockError,
        classify_runtime,
        lifecycle_lock,
    )

    root, spec = _resolve(repo, json_output)

    try:
        with lifecycle_lock(root):
            load = _state_guard(root, json_output)
            existing = load.state

            if existing is not None and existing.status in LOG_FAILURE_STATUSES:
                # A recorded logging failure is a diagnostic, not a free slot: starting a
                # new runtime here would overwrite the only account of what went wrong.
                _fail(
                    f"{existing.status}: {existing.stop_error or existing.log_error}. "
                    f"Nothing was started; run `remedy runtime stop` to clear it.",
                    EXIT_STATE, json_output=json_output,
                    payload={"error_class": "state",
                             "runtime_status": existing.status,
                             "log_error": existing.log_error,
                             "survivors": list(existing.survivors)},
                )
                return

            # The SAME contract probe and stop use: the supervisor is classified first
            # and, once it is verified, owns the application — so this CLI never has to
            # read the detached app's live cwd, which the kernel may well deny it.
            ident = classify_runtime(existing, root)
            check = ident.app

            if existing is not None and ident.usable:
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
                    if existing.supervisor_pid and not existing.instance_id:
                        # A supervised runtime with nothing binding its supervisor to
                        # this record cannot be re-attached to safely.
                        _fail(
                            "the running runtime has no instance id binding it to its "
                            "supervisor. Run `remedy runtime stop` first.",
                            EXIT_STATE, json_output=json_output,
                            payload={"error_class": "state",
                                     "identity": ident.to_json()},
                        )
                        return
                    payload = {"ok": True, "already_running": True,
                               "ownership": ident.ownership, **existing.to_json()}
                    if json_output:
                        print(_json.dumps(payload, indent=2))
                    else:
                        print(f"Runtime already running (pid {existing.pid}) on "
                              f"{existing.url}\n  Log: {existing.log_path}")
                    return

                if status == STATUS_STARTING:
                    # A bare `starting` state is NOT success. Who owns it?
                    if ident.supervisor.verified:
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

            if existing is not None and ident.ownership == OWNER_SUPERVISOR_MISSING:
                _fail(
                    f"supervisor_missing: {ident.reason}. Nothing was started; run "
                    f"`remedy runtime stop` or clean up pid {existing.pid} manually.",
                    EXIT_STATE, json_output=json_output,
                    payload={"error_class": "state",
                             "runtime_status": STATUS_SUPERVISOR_MISSING,
                             "identity": ident.to_json()},
                )
                return

            if existing is not None and ident.ownership != OWNER_GONE:
                _fail(
                    f"runtime state cannot be trusted ({ident.ownership}: "
                    f"{ident.reason or check.reason}). Nothing was started; run "
                    f"`remedy runtime stop` or clean up manually.",
                    EXIT_STATE, json_output=json_output,
                    payload={"error_class": "state", "identity": ident.to_json()},
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
        LOG_FAILURE_STATUSES,
        OWNER_SUPERVISOR_MISSING,
        STATUS_SUPERVISOR_MISSING,
        DevServer,
        RuntimeLockError,
        RuntimeProbeResult,
        RuntimeStartError,
        _pid_alive,
        classify_runtime,
        clear_state,
        http_probe,
        lifecycle_lock,
        save_state,
    )

    root, spec = _resolve(repo, json_output)
    served = None

    try:
        with lifecycle_lock(root):
            load = _state_guard(root, json_output)
            existing = load.state

            if existing is not None and existing.status in LOG_FAILURE_STATUSES:
                # The supervisor recorded that the bounded log pump died under a live
                # application. The runtime is not usable and the record is a diagnostic:
                # report it, do not start anything beside it, and let `runtime stop`
                # clear it once the processes are proven gone.
                _fail(
                    f"{existing.status}: {existing.stop_error or existing.log_error}",
                    EXIT_STATE, json_output=json_output,
                    payload={"error_class": "state",
                             "runtime_status": existing.status,
                             "log_error": existing.log_error,
                             "survivors": list(existing.survivors),
                             "state": existing.to_json()},
                )
                return

            ident = classify_runtime(existing, root)
            sup, check = ident.supervisor, ident.app

            if ident.ownership == OWNER_SUPERVISOR_MISSING:
                # The supervisor is gone: nobody owns the log pump or the lifecycle any
                # more, so this is never a healthy runtime, whatever the health URL
                # would answer. And nobody can prove any longer that the recorded pid is
                # still OUR application — it has been reparented, and every field in
                # runtime.json is mutable. So NOTHING is killed: supervisor_missing is
                # persisted with the survivor and identity data, and the operator is
                # told exactly what to look at.
                survivors = [existing.pid] if _pid_alive(existing.pid) else []
                if survivors:
                    existing.status = STATUS_SUPERVISOR_MISSING
                    existing.identity_reason = ident.reason
                    existing.survivors = survivors
                    existing.stop_error = ident.reason
                    with contextlib.suppress(Exception):
                        save_state(existing)
                else:
                    clear_state(root)
                _fail(
                    f"supervisor_missing: {ident.reason}. Nothing was killed"
                    + ("; the recorded application is gone too"
                       if not survivors else
                       f"; inspect pid {existing.pid} and clean it up manually"),
                    EXIT_STATE, json_output=json_output,
                    payload={"error_class": "state",
                             "runtime_status": STATUS_SUPERVISOR_MISSING,
                             "survivors": survivors,
                             "manual_cleanup": survivors,
                             "supervisor_identity": sup.to_json(),
                             "identity": ident.to_json()},
                )
                return

            if existing is not None and ident.usable:
                served = existing
            elif existing is not None and not ident.may_auto_clear:
                _fail(
                    f"runtime state cannot be trusted ({ident.ownership}: "
                    f"{ident.reason or check.reason}). Nothing was started or stopped.",
                    EXIT_STATE, json_output=json_output,
                    payload={"error_class": "state", "identity": ident.to_json()},
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

    # ...and then the runtime is classified AGAIN. The first classification is only a
    # statement about the past: a supervisor can die while the health URL is being
    # fetched, and the application would happily keep answering 200 with nobody owning
    # its log pump or its lifecycle. A supervisorless application is never a healthy
    # managed runtime, however cheerful its HTTP response.
    try:
        with lifecycle_lock(root):
            fresh = _revalidate_served(root, served)
    except RuntimeLockError as exc:
        _fail(str(exc), EXIT_STATE, json_output=json_output,
              payload={"error_class": "lock"})
        return

    if fresh["changed"]:
        _fail(
            f"the served runtime changed while it was being probed: {fresh['reason']}. "
            f"The HTTP status ({status or 'none'}) says nothing about a runtime nobody "
            f"owns any more.",
            EXIT_STATE, json_output=json_output,
            payload={"error_class": "state",
                     "runtime_status": fresh["runtime_status"],
                     "managed_by_serve": True, "stopped": False,
                     "status_code": status,
                     "log_error": fresh["log_error"],
                     "survivors": fresh["survivors"],
                     "identity": fresh["identity"]},
        )
        return

    # Everything reported now comes from the state RELOADED after the request — the
    # pre-request record is a snapshot of the past, and a log pump that died during the
    # probe is exactly the kind of failure it cannot know about.
    result = RuntimeProbeResult(
        ok=good, status_code=status, url=served.url, port=served.port,
        error="" if good else (err or f"health status {status}"),
        error_class="" if good else "ready", pid=served.pid,
        log_error=fresh["log_error"],
    )
    payload = {**result.to_json(), "managed_by_serve": True, "stopped": False,
               "runtime_status": fresh["runtime_status"],
               "survivors": fresh["survivors"]}
    if json_output:
        print(_json.dumps(payload, indent=2))
    else:
        print(f"Probe {'OK' if good else 'FAILED'}: {served.url} "
              f"(pid {served.pid}, still running)")
    if not good:
        sys.exit(EXIT_READY)


def _revalidate_served(root, before) -> dict:
    """Is the runtime we probed still the same, still running, still supervised?

    Called under the lifecycle lock AFTER the HTTP request. Everything that made the
    runtime trustworthy before the request has to hold again — and it has to be the SAME
    runtime: same instance id, same supervisor pid and creation time, same application
    pid and creation time. A state that was replaced underneath us is not "still fine
    because the port answered".
    """
    from packages.runtimes.dev_server import (
        LOG_FAILURE_STATUSES,
        OWNER_SUPERVISED,
        OWNER_SUPERVISOR_MISSING,
        STATUS_RUNNING,
        STATUS_SUPERVISOR_MISSING,
        classify_runtime,
        load_state_result,
    )

    def result(*, changed: bool, reason: str, status: str, state=None, ident=None) -> dict:
        return {
            "changed": changed, "reason": reason, "runtime_status": status,
            "log_error": (state.log_error if state is not None else ""),
            "survivors": (list(state.survivors) if state is not None else []),
            "identity": ident.to_json() if ident is not None else {},
        }

    load = load_state_result(root)
    after = load.state
    if after is None:
        return result(
            changed=True, status=load.kind,
            reason=(f"its durable state is {load.kind} "
                    f"({load.error or 'no record left'})"))

    same = (after.instance_id == before.instance_id
            and after.pid == before.pid
            and after.create_time == before.create_time
            and after.supervisor_pid == before.supervisor_pid
            and after.supervisor_create_time == before.supervisor_create_time)
    if not same:
        return result(
            changed=True, status=after.status, state=after,
            reason="the durable record now describes a different runtime instance")

    ident = classify_runtime(after, root)
    if after.status in LOG_FAILURE_STATUSES:
        # The pump died while we were fetching the health URL. A 200 from a runtime
        # whose logs nobody drains any more is not health.
        return result(
            changed=True, status=after.status, state=after, ident=ident,
            reason=f"its log pump failed ({after.log_error or 'no error recorded'})")
    if after.status != STATUS_RUNNING:
        return result(changed=True, status=after.status, state=after, ident=ident,
                      reason=f"its status is now {after.status!r}")
    if ident.ownership != OWNER_SUPERVISED:
        status = (STATUS_SUPERVISOR_MISSING
                  if ident.ownership == OWNER_SUPERVISOR_MISSING else after.status)
        return result(
            changed=True, status=status, state=after, ident=ident,
            reason=(f"it is no longer supervised ({ident.ownership}: "
                    f"{ident.reason or ident.supervisor.reason})"))
    return result(changed=False, reason="", status=after.status, state=after,
                  ident=ident)


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
