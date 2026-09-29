"""F041 T002 — the UI server's own preview worker (DECISION F041 D4).

One worker per running server. It owns the only thread that ever acts on a preview
after the write door records a request: the door itself runs no verb (it only calls
:func:`packages.orchestration.preview_control.request_preview` and hands the job id to
this worker's :meth:`PreviewWorker.submit`), so a serve or a probe never blocks the
door's own request.

``step`` first runs every queued request with
:func:`packages.orchestration.preview_control.run_pending`, then, for every OTHER
preview it still keeps live, checks it for idleness with
:func:`packages.orchestration.preview_control.stop_if_idle` and, while it is still
live, probes it again with
:func:`packages.orchestration.preview_control.revalidate_live` — a live record on disk
says nothing about whether the app still answers. The thread this worker starts calls
``step`` at least every `PREVIEW_TICK_SECONDS`, and sooner whenever `submit` wakes it.
``adopt_live`` lets a freshly started server keep looking after a preview an earlier
server left live, and ``close`` stops every preview this worker still keeps live before
the server exits, so a server restart never leaves an orphaned runtime behind.

The runner looked up here is
:func:`packages.orchestration.preview_runner.run_runtime_verb`, resolved on the module
at each call so a test's monkeypatch of that name always reaches whichever call runs
next, exactly as the door's own effect (`preview_control.request_preview`) never runs
a verb itself.
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration import data_paths, pingpong_job, preview_control, preview_runner

#: The worker's own thread steps at least this often (DECISION F041 D4 (2)), so a
#: live preview nobody submits a request for is still revalidated and checked for
#: idleness on a bound.
PREVIEW_TICK_SECONDS = 15

#: The daemon thread's name, so a hang or a stack dump names this worker by it.
PREVIEW_WORKER_THREAD_NAME = "remedy-preview-worker"


class PreviewWorker:
    """Runs the harness's verbs for every job's preview, on its own thread.

    ``ttl_seconds`` is DECISION F041 D4 (3)'s idle limit, passed straight through to
    each `stop_if_idle` call. ``runner`` is the verb callable; ``None`` means
    :func:`packages.orchestration.preview_runner.run_runtime_verb`, looked up at each
    call rather than bound once. ``load_job`` is ``None`` means
    :func:`packages.orchestration.pingpong_job.load_job_plan`. ``clock`` is ``None``
    means the current UTC time. A lock guards the queue and the live set, since
    `submit` is called from the door's own request thread while `step` runs on this
    worker's own.
    """

    def __init__(
        self,
        *,
        ttl_seconds: int,
        runner: preview_control.RuntimeVerb | None = None,
        load_job: Any = None,
        clock: Any = None,
        data_root: Path | None = None,
    ) -> None:
        self._ttl_seconds = ttl_seconds
        self._runner = runner
        self._load_job = load_job if load_job is not None else pingpong_job.load_job_plan
        self._clock = clock if clock is not None else (lambda: datetime.now(timezone.utc))
        self._data_root = data_root

        self._lock = threading.Lock()
        self._pending: list[str] = []
        self._queued: set[str] = set()
        self._live: set[str] = set()

        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._wake_event = threading.Event()

    def _resolve_runner(self) -> preview_control.RuntimeVerb:
        """The verb callable this call uses: the given one, else the harness's own,
        looked up on `preview_runner` fresh each time (DECISION F041 D4 (2))."""
        if self._runner is not None:
            return self._runner
        return preview_runner.run_runtime_verb

    def _load(self, job_id: str) -> Any:
        """The job `load_job` answers, or ``None`` — which also drops ``job_id``
        from the live set, since a job that cannot be loaded cannot be looked after."""
        job = self._load_job(job_id)
        if job is None:
            with self._lock:
                self._live.discard(job_id)
        return job

    @property
    def live_jobs(self) -> frozenset[str]:
        """Every job id this worker currently keeps live."""
        with self._lock:
            return frozenset(self._live)

    def submit(self, job_id: str) -> None:
        """Queue ``job_id``'s pending request once and wake the thread. Runs
        nothing itself — `step` is what acts on the queue."""
        with self._lock:
            if job_id not in self._queued:
                self._queued.add(job_id)
                self._pending.append(job_id)
        self._wake_event.set()

    def adopt_live(self) -> None:
        """Take on every preview a record under `<jobs dir>/*/preview.json` already
        calls live, so a restarted server still looks after it (DECISION F041 D4 (2))."""
        jobs_root = data_paths.jobs_dir(self._data_root)
        if not jobs_root.is_dir():
            return
        for preview_file in sorted(jobs_root.glob(f"*/{preview_control.PREVIEW_FILENAME}")):
            job_id = preview_file.parent.name
            record = preview_control.load_preview(job_id, self._data_root)
            if record["state"] == preview_control.STATE_LIVE:
                with self._lock:
                    self._live.add(job_id)

    def step(self) -> None:
        """Run every queued request, then look after every other live preview
        (DECISION F041 D4 (2)): stop it if it has gone idle, and, while it is
        still live, revalidate it."""
        with self._lock:
            pending = list(self._pending)
            self._pending.clear()
            self._queued.clear()

        runner = self._resolve_runner()
        now = self._clock()
        processed: set[str] = set()

        for job_id in pending:
            processed.add(job_id)
            job = self._load(job_id)
            if job is None:
                continue
            record = preview_control.run_pending(
                job, runner, now=now, data_root=self._data_root)
            with self._lock:
                if record["state"] == preview_control.STATE_LIVE:
                    self._live.add(job_id)
                else:
                    self._live.discard(job_id)

        with self._lock:
            others = sorted(self._live - processed)

        for job_id in others:
            job = self._load(job_id)
            if job is None:
                continue
            record = preview_control.stop_if_idle(
                job, runner, now=now, ttl_seconds=self._ttl_seconds,
                data_root=self._data_root)
            if record["state"] != preview_control.STATE_LIVE:
                with self._lock:
                    self._live.discard(job_id)
                continue
            record = preview_control.revalidate_live(
                job, runner, now=now, data_root=self._data_root)
            if record["state"] != preview_control.STATE_LIVE:
                with self._lock:
                    self._live.discard(job_id)

    def stop_all(self) -> None:
        """Record a stop for every live preview and run it, sorted by job id so
        the order this worker stops them in is deterministic."""
        runner = self._resolve_runner()
        now = self._clock()
        with self._lock:
            job_ids = sorted(self._live)

        for job_id in job_ids:
            job = self._load(job_id)
            if job is None:
                continue
            preview_control.request_preview(
                job_id, preview_control.ACTION_STOP, now=now, data_root=self._data_root)
            preview_control.run_pending(job, runner, now=now, data_root=self._data_root)
            with self._lock:
                self._live.discard(job_id)

    def start(self, tick_seconds: float = PREVIEW_TICK_SECONDS) -> None:
        """Start the one daemon thread that steps, then waits on the wake event up
        to `tick_seconds`, until `close` stops it."""

        def _run() -> None:
            while not self._stop_event.is_set():
                self.step()
                self._wake_event.wait(tick_seconds)
                self._wake_event.clear()

        self._thread = threading.Thread(
            target=_run, name=PREVIEW_WORKER_THREAD_NAME, daemon=True)
        self._thread.start()

    def close(self, timeout: float = 5.0) -> None:
        """Stop and join the thread, then `stop_all` — every preview this worker
        still keeps live is stopped before the server that owns it exits."""
        self._stop_event.set()
        self._wake_event.set()
        if self._thread is not None:
            self._thread.join(timeout=timeout)
            self._thread = None
        self.stop_all()
