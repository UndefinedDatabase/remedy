"""Persistent development-server supervisor (F007 final round).

The problem this exists to solve: `remedy runtime serve` is a SHORT-LIVED process.
If it owns the dev server and the log pump directly, then the moment the CLI exits
the pump thread dies, the stdout pipe loses its reader, bounded logging stops and a
chatty application dies on a broken pipe. The reviewed implementation did exactly
that — the server was dead ~300 ms after the CLI returned.

So `serve` no longer owns the runtime. It starts a SUPERVISOR:

    remedy runtime serve (short-lived)
      └── supervisor  (own session, survives the CLI)
            ├── bounded LogPump (owns the app's stdout pipe for its whole life)
            └── application (child of the supervisor)

The supervisor: opens the log, launches the app, records both identities, persists
``starting``, waits for HTTP readiness, persists ``running``, reports the outcome
back over a private filesystem handshake, and then STAYS ALIVE — pumping logs,
watching the app, and polling for a stop request — until the runtime is stopped or
the app exits on its own.

No shell, no Docker, no network control port, no provider call. This is not F011's
job stop mechanism: the stop request here is a local file for this one runtime.

Invoked as a module::

    python -m packages.runtimes.runtime_supervisor --repo <project> --spec <json>
        --handshake <path>
"""
from __future__ import annotations

import argparse
import contextlib
import json
import os
import signal
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.runtimes.dev_server import (
    GRACE_SECONDS,
    LOG_TAIL_BYTES,
    READY_STATUS_MAX,
    READY_STATUS_MIN,
    STATUS_EXITED,
    STATUS_LOG_CLEANUP_FAILED,
    STATUS_LOG_FAILED,
    STATUS_RUNNING,
    STATUS_START_CLEANUP_FAILED,
    STATUS_STARTING,
    STATUS_STOP_FAILED,
    LogPump,
    RuntimeSpec,
    RuntimeState,
    _process_create_time,
    atomic_write_text,
    clear_state,
    ensure_runtime_dir,
    handshake_path,
    http_probe,
    load_state,
    log_failure_note_path,
    log_path,
    project_digest,
    read_log_tail,
    resolved_fingerprint,
    save_state,
    spec_file_path,
    stop_process_tree,
    stop_request_path,
    validate_spec,
)

#: How often the supervisor checks the app and the stop request.
POLL_SECONDS = 0.25

#: How long `serve` waits for the supervisor's handshake before giving up.
HANDSHAKE_TIMEOUT_S = 90.0


def write_handshake(path: Path, payload: dict[str, Any]) -> None:
    """Atomic PRIVATE handshake write: the reader never sees a half-written result,
    and no other user ever sees the result at all."""
    atomic_write_text(path, json.dumps(payload, indent=2) + "\n")


def read_handshake(path: Path) -> dict[str, Any] | None:
    """Read the handshake, or None while it is absent/incomplete/corrupt."""
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None                      # not written yet, or corrupt: keep waiting
    return data if isinstance(data, dict) else None


@dataclass
class Supervisor:
    """Owns one application process for the whole life of a served runtime."""

    spec: RuntimeSpec
    project_root: str
    handshake: Path
    instance_id: str = ""

    proc: Any = None
    pump: LogPump | None = None
    state: RuntimeState | None = None
    port: int = 0

    # -- helpers -----------------------------------------------------------

    @property
    def url(self) -> str:
        return f"http://{self.spec.host}:{self.port}{self.spec.health_path}"

    def _report_failure(self, error: str, error_class: str,
                        survivors: list[int]) -> None:
        with contextlib.suppress(Exception):
            write_handshake(self.handshake, {
                "ok": False, "error": error, "error_class": error_class,
                "survivors": survivors, "instance_id": self.instance_id,
                "supervisor_pid": os.getpid(),
                "log_tail": read_log_tail(log_path(self.project_root),
                                          LOG_TAIL_BYTES),
            })

    def _finalize_failure(self, error: str, error_class: str) -> int:
        """The ONE way this supervisor fails, whatever went wrong.

        Every failure after the application was launched — pump start, `starting`
        persistence, readiness, `running` persistence, the success handshake, or an
        unexpected exception — ends here: stop the app family, join the pump, look at
        who survived, and only THEN decide what the state says. No path may delete the
        state unconditionally while a managed process is still alive.
        """
        cleanup = self._stop_app()
        survivors = list(cleanup.get("survivors") or [])

        if survivors:
            self._persist_start_cleanup_failed(cleanup, error)
        else:
            with contextlib.suppress(Exception):
                clear_state(self.project_root)

        payload = {
            "ok": False,
            "error": error,
            "error_class": error_class,
            "log_tail": read_log_tail(log_path(self.project_root), LOG_TAIL_BYTES),
            "cleanup": cleanup,
            "survivors": survivors,
            "supervisor_pid": os.getpid(),
            "instance_id": self.instance_id,
        }
        with contextlib.suppress(Exception):        # best effort: never mask the error
            write_handshake(self.handshake, payload)

        if survivors:
            return 5
        return 3 if error_class == "start" else (5 if error_class == "state" else 4)

    def _persist_start_cleanup_failed(self, cleanup: dict[str, Any],
                                      error: str) -> None:
        state = self.state or load_state(self.project_root)
        if state is None:
            return
        state.status = STATUS_START_CLEANUP_FAILED
        state.survivors = list(cleanup.get("survivors") or [])
        state.stop_error = (
            f"{error}; processes survived the supervisor cleanup: {state.survivors}")
        with contextlib.suppress(Exception):
            save_state(state)

    def _stop_app(self) -> dict[str, Any]:
        """Stop the application tree we own, and reap it."""
        if self.proc is None:
            return {"survivors": [], "error": ""}
        result = stop_process_tree(self.proc.pid, session_id=self._app_pgid())
        with contextlib.suppress(Exception):
            self.proc.wait(timeout=GRACE_SECONDS)
        if self.pump is not None:
            self.pump.join(timeout=GRACE_SECONDS)
        return result

    def _remove_control_files(self, *, keep_handshake: bool = False) -> None:
        """A stopped runtime leaves no stop request, handshake or spec behind.

        ``keep_handshake``: the SUCCESS handshake belongs to the serve CLI that is still
        waiting for it. A pump that fails microseconds after the handshake was written
        must not delete it underneath that CLI — the start really did succeed, and serve
        must be able to say so; the failure that follows is then reported by the durable
        state, which is exactly what a later probe reads.
        """
        stop_file = stop_request_path(self.project_root)
        targets = [stop_file,
                   stop_file.with_name(stop_file.name + ".invalid"),
                   spec_file_path(self.project_root)]
        if not keep_handshake:
            targets.append(self.handshake)
        for path in targets:
            with contextlib.suppress(OSError):
                Path(path).unlink()

    def _app_pgid(self) -> int:
        if self.proc is None:
            return 0
        with contextlib.suppress(OSError, ProcessLookupError):
            return os.getpgid(self.proc.pid)
        return 0

    # -- lifecycle ---------------------------------------------------------

    def run(self) -> int:
        import subprocess

        self.port = int(os.environ["REMEDY_RUNTIME_PORT"])
        argv = self.spec.resolved_cmd(self.port)
        env = self.spec.resolved_env(self.port)
        log_file = log_path(self.project_root)

        # 1. the log, synchronously, before any process exists
        try:
            handle = LogPump.open_log(log_file)
        except OSError as exc:
            # Nothing has been launched yet, so there is nothing to finalize.
            self._report_failure(f"runtime log could not be opened: {exc}", "start", [])
            return 3

        # 2. the application, as OUR child
        try:
            self.proc = subprocess.Popen(      # noqa: S603 - argv, never a shell
                argv, cwd=self.spec.cwd, env=env,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                # The application gets its OWN session, so its group can be killed
                # whole WITHOUT the supervisor signalling itself — the supervisor has
                # to stay alive long enough to record what the cleanup actually did.
                start_new_session=True,
            )
        except (OSError, ValueError) as exc:
            with contextlib.suppress(Exception):
                handle.close()
            self._report_failure(f"could not start the application: {exc}",
                                 "start", [])
            return 3

        # 3. the pump, whose thread lives as long as WE do
        try:
            # An operator (or a test) may cap the log lower than the default.
            cap = os.environ.get("REMEDY_RUNTIME_LOG_MAX")
            self.pump = LogPump(
                self.proc.stdout, handle, log_file,
                max_bytes=int(cap) if cap else None,
                keep_bytes=int(cap) // 2 if cap else None,
            )
            self.pump.start()
        except Exception as exc:
            cleanup = self._stop_app()
            return self._finalize_failure(f"log pump failed to start: {exc}", "start")

        # 4. identities, then the `starting` record
        try:
            app_create = _process_create_time(self.proc.pid)
            sup_pid = os.getpid()
            sup_cmd = list(sys.argv)
            sup_cwd = os.getcwd()
            digest = project_digest(self.project_root)
            self.state = RuntimeState(
                pid=self.proc.pid,
                create_time=app_create,
                pgid=os.getpgid(self.proc.pid),
                sid=os.getsid(self.proc.pid),
                session_id=os.getpgid(self.proc.pid),
                port=self.port,
                url=self.url,
                project_root=self.project_root,
                project_id=digest,
                cwd=str(Path(self.spec.cwd).resolve()),
                cmd=argv,
                cmd_fingerprint=resolved_fingerprint(argv, self.spec.cwd, digest),
                spec_fingerprint=self.spec.fingerprint(),
                started_at=time.time(),
                log_path=str(log_file),
                status=STATUS_STARTING,
                supervisor_pid=sup_pid,
                supervisor_create_time=_process_create_time(sup_pid),
                supervisor_cmd=[sys.executable, "-m",
                                "packages.runtimes.runtime_supervisor"] + sup_cmd[1:],
                supervisor_cwd=sup_cwd,
                supervisor_fingerprint=resolved_fingerprint(
                    [sys.executable, "-m", "packages.runtimes.runtime_supervisor"]
                    + sup_cmd[1:], sup_cwd, digest),
                supervisor_pgid=os.getpgrp(),
                supervisor_sid=os.getsid(0),
                instance_id=self.instance_id,
            )
            save_state(self.state)
        except Exception as exc:
            return self._finalize_failure(
                f"starting state could not be persisted: {exc}", "state")

        # 5. readiness
        ready = self._wait_ready()
        if not ready["ok"]:
            return self._finalize_failure(ready["error"], ready["error_class"])

        # 6. `running` — transactional: if it cannot be persisted, the app must NOT
        #    be left alive behind an abandoned record.
        try:
            self.state.status = STATUS_RUNNING
            self.state.log_error = self.pump.error if self.pump else ""
            save_state(self.state)
        except Exception as exc:
            return self._finalize_failure(
                f"running state could not be persisted: {exc}", "state")

        # 7. tell the CLI, then STAY ALIVE
        try:
            write_handshake(self.handshake, {
                "ok": True,
                "supervisor_pid": os.getpid(),
                "app_pid": self.proc.pid,
                "port": self.port,
                "url": self.state.url,
                "status_code": ready["status_code"],
                "instance_id": self.instance_id,
            })
        except Exception as exc:
            return self._finalize_failure(
                f"handshake could not be written: {exc}", "state")

        return self._supervise()

    def _persist_stop_failed(self, cleanup: dict[str, Any]) -> None:
        if self.state is None:
            return
        self.state.status = STATUS_STOP_FAILED
        self.state.survivors = list(cleanup.get("survivors") or [])
        self.state.stop_error = cleanup.get("error") or (
            f"processes survived the supervisor cleanup: {self.state.survivors}")
        with contextlib.suppress(Exception):
            save_state(self.state)

    def _wait_ready(self) -> dict[str, Any]:
        deadline = time.monotonic() + self.spec.ready_timeout_s
        last = ""
        while time.monotonic() < deadline:
            if self.proc.poll() is not None:
                return {"ok": False, "error_class": "start",
                        "error": (f"application exited before readiness "
                                  f"(exit code {self.proc.returncode})")}
            status, err = http_probe(self.url, timeout=2.0)
            if READY_STATUS_MIN <= status <= READY_STATUS_MAX:
                return {"ok": True, "status_code": status}
            last = err or f"health status {status}"
            time.sleep(0.15)
        return {"ok": False, "error_class": "ready",
                "error": f"not ready after {self.spec.ready_timeout_s}s: {last}"}

    def _stop_request_is_ours(self, stop_file: Path) -> bool:
        """A stop request is obeyed ONLY when it carries this runtime's exact id.

        Anything else — an empty or whitespace-only file, a truncated id, an id with
        extra text after it, a foreign id, an unreadable or undecodable file — is not a
        stop request for this runtime. The reviewed build treated an EMPTY file as a
        valid stop, so a zero-byte `runtime.stop` shut a live runtime down. Now the id
        must match exactly; an invalid request is quarantined and supervision
        continues, with the running state untouched.
        """
        try:
            requested = stop_file.read_text(encoding="utf-8").strip()
        except (OSError, ValueError, UnicodeDecodeError) as exc:
            self._quarantine(stop_file, f"unreadable stop request: {exc}")
            return False

        if self.instance_id and requested == self.instance_id:
            return True

        self._quarantine(
            stop_file,
            "stop request does not carry this runtime's instance id "
            f"({len(requested)} characters); the runtime keeps running")
        return False

    def _quarantine(self, stop_file: Path, reason: str) -> None:
        """Set an invalid stop request aside; never act on it, never loop on it."""
        with contextlib.suppress(OSError):
            atomic_write_text(stop_file.with_name(stop_file.name + ".invalid"),
                              f"{reason}\n")
        with contextlib.suppress(OSError):
            stop_file.unlink()

    def _log_failure(self) -> str:
        """Why the bounded log is no longer being drained — or "" while it is.

        The pump is checked for the WHOLE life of the runtime, not only at startup. A
        pump that raised, and a pump whose thread simply ended while the application is
        still running, are the same fact: nothing is draining the child's stdout any
        more. The pipe fills, the application blocks on its own output, and no line of it
        is being captured. That is a runtime failure even when no exception was recorded.
        """
        if self.pump is None:
            return "the log pump is gone"
        if self.pump.error:
            return self.pump.error
        if not self.pump.alive:
            return "log pump exited unexpectedly while the application was running"
        return ""

    def _finalize_log_failure(self, error: str) -> int:
        """A post-start pump failure ends the runtime — honestly, and with no orphan.

        The application family is stopped through the identity this supervisor OWNS (its
        own child and the group it observed at launch), the pump is joined, survivors are
        inspected, and only then is the durable record written. The state never stays
        ``running``, and the diagnostic is never cleared here: a later `runtime probe`
        must still be able to say what went wrong, and `runtime stop` clears it once the
        processes are proven gone.

        The write itself can fail. What happens then depends entirely on whether anything
        SURVIVED: runtime.json is the only record of a survivor's pid, creation time,
        process group, session and instance id, and without it no later command can ever
        prove ownership of that process again. So a survivor's record is never deleted
        because a nicer diagnostic could not be written — the previous record stays as
        the minimum safe fallback. Only when nothing survived is clearing a now-false
        `running` record the safe thing to do.
        """
        cleanup = self._stop_app()
        survivors = list(cleanup.get("survivors") or [])
        self._remove_control_files(keep_handshake=True)

        state = load_state(self.project_root) or self.state
        if state is None or state.supervisor_pid not in (0, os.getpid()):
            return 5

        status = STATUS_LOG_CLEANUP_FAILED if survivors else STATUS_LOG_FAILED
        detail = (f"the runtime log pump failed: {error}"
                  + (f"; processes survived the cleanup: {survivors}" if survivors
                     else "; the application family was stopped"))
        updated = RuntimeState.from_json(state.to_json())
        updated.status = status
        updated.log_error = error
        updated.survivors = survivors
        updated.stop_error = detail
        try:
            save_state(updated)
        except Exception as exc:
            if survivors:
                # NEVER clear here. The pre-existing record — pid, creation time, pgid,
                # sid, instance id — is the only thing that lets a later probe or stop
                # identify these live processes at all. Keep it, and leave the write
                # failure where an operator will find it.
                self._emergency_note(status, detail, survivors, exc)
            else:
                # Nothing survived: a record still claiming `running` would be a lie
                # about processes that no longer exist.
                with contextlib.suppress(Exception):
                    clear_state(self.project_root)
        return 5

    def _emergency_note(self, status: str, detail: str, survivors: list[int],
                        exc: Exception) -> None:
        """A private owner-only sidecar describing a diagnostic that could not be saved.

        It is a NOTE, never authorization: nothing reads it to decide what to signal. The
        durable runtime.json — untouched — remains the only identity a command may act on.
        """
        with contextlib.suppress(Exception):
            atomic_write_text(
                log_failure_note_path(self.project_root),
                json.dumps({
                    "status": status,
                    "detail": detail,
                    "survivors": survivors,
                    "state_write_error": f"{type(exc).__name__}: {exc}",
                    "supervisor_pid": os.getpid(),
                    "instance_id": self.instance_id,
                }, indent=2) + "\n",
            )

    def _supervise(self) -> int:
        """Stay alive: pump logs, watch the app, watch the PUMP, poll for a stop."""
        stop_file = stop_request_path(self.project_root)
        while True:
            if stop_file.exists():
                if not self._stop_request_is_ours(stop_file):
                    time.sleep(POLL_SECONDS)
                    continue
                cleanup = self._stop_app()
                self._remove_control_files()
                if cleanup.get("survivors"):
                    self._persist_stop_failed(cleanup)
                    return 5
                clear_state(self.project_root)
                return 0

            code = self.proc.poll()
            if code is not None:
                # The application died on its own: say so, honestly, and leave. Checked
                # BEFORE the pump, because a pump reaching EOF is the normal consequence
                # of the application closing its stdout on the way out.
                if self.pump is not None:
                    self.pump.join(timeout=GRACE_SECONDS)
                current = load_state(self.project_root)
                if current is not None and current.supervisor_pid == os.getpid():
                    current.status = STATUS_EXITED
                    current.app_exit_code = code
                    current.stop_error = f"application exited with code {code}"
                    current.log_error = self.pump.error if self.pump else ""
                    with contextlib.suppress(Exception):
                        save_state(current)
                return 0

            failure = self._log_failure()
            if failure:
                return self._finalize_log_failure(failure)

            time.sleep(POLL_SECONDS)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="remedy-runtime-supervisor")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--spec", required=True, help="path to a spec JSON file")
    parser.add_argument("--handshake", required=True)
    parser.add_argument("--instance", required=True,
                        help="the runtime instance id (also written to runtime.json)")
    args = parser.parse_args(argv)

    project_root = str(Path(args.repo).resolve())
    ensure_runtime_dir(project_root)     # 0700, and repair any file from an old build

    # The spec file carries the configured runtime ENVIRONMENT — it may contain
    # secrets. It is ingested exactly once and then deleted, whether or not it turns
    # out to be usable: nothing that failed to start is worth leaving an environment
    # on disk for.
    spec_file = Path(args.spec)
    try:
        raw = spec_file.read_text(encoding="utf-8")
    finally:
        with contextlib.suppress(OSError):
            spec_file.unlink()
    data = json.loads(raw)
    spec = validate_spec(
        RuntimeSpec(
            cmd=list(data["cmd"]), cwd=data["cwd"], port=int(data["port"]),
            health_path=data["health_path"],
            ready_timeout_s=float(data["ready_timeout_s"]),
            host=data.get("host", "127.0.0.1"),
            env=dict(data.get("env") or {}),
            source=data.get("source", "config"),
        ),
        project_root,
    )

    # Ignore the terminal's signals: the supervisor is nobody's foreground job.
    with contextlib.suppress(Exception):
        signal.signal(signal.SIGHUP, signal.SIG_IGN)

    sup = Supervisor(spec=spec, project_root=project_root,
                     handshake=Path(args.handshake), instance_id=args.instance)
    try:
        return sup.run()
    except Exception as exc:                      # never a raw traceback on disk
        return sup._finalize_failure(
            f"supervisor failed: {type(exc).__name__}: {exc}", "state")


if __name__ == "__main__":
    raise SystemExit(main())
