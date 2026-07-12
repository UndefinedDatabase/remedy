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
    STATUS_RUNNING,
    STATUS_STARTING,
    STATUS_STOP_FAILED,
    LogPump,
    RuntimeSpec,
    RuntimeState,
    _process_create_time,
    clear_state,
    handshake_path,
    http_probe,
    load_state,
    log_path,
    project_digest,
    read_log_tail,
    resolved_fingerprint,
    save_state,
    stop_process_tree,
    stop_request_path,
    validate_spec,
)

#: How often the supervisor checks the app and the stop request.
POLL_SECONDS = 0.25

#: How long `serve` waits for the supervisor's handshake before giving up.
HANDSHAKE_TIMEOUT_S = 90.0


def write_handshake(path: Path, payload: dict[str, Any]) -> None:
    """Atomic handshake write: the reader never sees a half-written result."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, path)
    except Exception:
        with contextlib.suppress(OSError):
            tmp.unlink()
        raise


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

    proc: Any = None
    pump: LogPump | None = None
    state: RuntimeState | None = None
    port: int = 0

    # -- helpers -----------------------------------------------------------

    @property
    def url(self) -> str:
        return f"http://{self.spec.host}:{self.port}{self.spec.health_path}"

    def _fail(self, error: str, error_class: str, cleanup: dict[str, Any]) -> int:
        payload = {
            "ok": False,
            "error": error,
            "error_class": error_class,
            "log_tail": read_log_tail(log_path(self.project_root), LOG_TAIL_BYTES),
            "cleanup": cleanup,
            "survivors": cleanup.get("survivors", []),
            "supervisor_pid": os.getpid(),
        }
        with contextlib.suppress(Exception):
            write_handshake(self.handshake, payload)
        return 3 if error_class == "start" else (5 if cleanup.get("survivors") else 4)

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
            return self._fail(f"runtime log could not be opened: {exc}",
                              "start", {"survivors": []})

        # 2. the application, as OUR child
        try:
            self.proc = subprocess.Popen(      # noqa: S603 - argv, never a shell
                argv, cwd=self.spec.cwd, env=env,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
            )
        except (OSError, ValueError) as exc:
            with contextlib.suppress(Exception):
                handle.close()
            return self._fail(f"could not start the application: {exc}",
                              "start", {"survivors": []})

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
            return self._fail(f"log pump failed to start: {exc}", "start", cleanup)

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
            )
            save_state(self.state)
        except Exception as exc:
            cleanup = self._stop_app()
            return self._fail(f"starting state could not be persisted: {exc}",
                              "state", cleanup)

        # 5. readiness
        ready = self._wait_ready()
        if not ready["ok"]:
            cleanup = self._stop_app()
            if not cleanup.get("survivors"):
                clear_state(self.project_root)
            else:
                self._persist_stop_failed(cleanup)
            return self._fail(ready["error"], ready["error_class"], cleanup)

        # 6. `running` — transactional: if it cannot be persisted, the app must NOT
        #    be left alive behind an abandoned record.
        try:
            self.state.status = STATUS_RUNNING
            self.state.log_error = self.pump.error if self.pump else ""
            save_state(self.state)
        except Exception as exc:
            cleanup = self._stop_app()
            if cleanup.get("survivors"):
                self._persist_stop_failed(cleanup)
            else:
                clear_state(self.project_root)
            return self._fail(
                f"running state could not be persisted: {exc}", "state", cleanup)

        # 7. tell the CLI, then STAY ALIVE
        try:
            write_handshake(self.handshake, {
                "ok": True,
                "supervisor_pid": os.getpid(),
                "app_pid": self.proc.pid,
                "port": self.port,
                "url": self.state.url,
                "status_code": ready["status_code"],
            })
        except Exception as exc:
            cleanup = self._stop_app()
            clear_state(self.project_root)
            return self._fail(f"handshake could not be written: {exc}",
                              "state", cleanup)

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

    def _supervise(self) -> int:
        """Stay alive: pump logs, watch the app, poll for a stop request."""
        stop_file = stop_request_path(self.project_root)
        while True:
            if stop_file.exists():
                cleanup = self._stop_app()
                with contextlib.suppress(OSError):
                    stop_file.unlink()
                if cleanup.get("survivors"):
                    self._persist_stop_failed(cleanup)
                    return 5
                clear_state(self.project_root)
                return 0

            code = self.proc.poll()
            if code is not None:
                # The application died on its own: say so, honestly, and leave.
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

            time.sleep(POLL_SECONDS)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="remedy-runtime-supervisor")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--spec", required=True, help="path to a spec JSON file")
    parser.add_argument("--handshake", required=True)
    args = parser.parse_args(argv)

    project_root = str(Path(args.repo).resolve())
    data = json.loads(Path(args.spec).read_text(encoding="utf-8"))
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
                     handshake=Path(args.handshake))
    try:
        return sup.run()
    except Exception as exc:                      # never a raw traceback on disk
        cleanup = sup._stop_app()
        return sup._fail(f"supervisor failed: {type(exc).__name__}: {exc}",
                         "start", cleanup)


if __name__ == "__main__":
    raise SystemExit(main())
