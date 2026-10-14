"""Operator amendment amend1014-do-golden-path-now D4 — what a human-facing `remedy do` says while it works.

Every step is announced on stderr, flushed, BEFORE it starts; a step that stays blocked repeats
one compact heartbeat line every `DO_HEARTBEAT_SECONDS`; every step announces its end with its
elapsed time at once, not when the whole walk returns. A line names the step, the provider of a
step that calls one, and the elapsed time; it never carries a prompt, a model's output or a secret.

`--json` builds no `DoProgress`: stdout stays one document and stderr stays silent.
The clock and the sink are injected, so a test drives the heartbeat without sleeping.
"""

from __future__ import annotations

import sys
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path

from packages.orchestration.do_context import DoContext
from packages.orchestration.do_lane import DO_TINY_REPO_MAX_FILES, settle_do_lane

#: The longest a blocked step stays silent.
DO_HEARTBEAT_SECONDS = 10.0

#: How often the heartbeat thread looks at the clock; the line itself waits for the interval.
_HEARTBEAT_POLL_SECONDS = 1.0

#: The prefix of every progress line, so a person can tell Remedy's own words from tool output.
DO_PROGRESS_PREFIX = "[remedy]"

#: How much of a stopped or failed step's detail its end line repeats.
_END_DETAIL_CHARS = 240


def write_progress_to_stderr(text: str) -> None:
    """The default sink: one line on the stderr of the moment, flushed at once."""
    print(text, file=sys.stderr, flush=True)  # noqa: T201 — the progress line the person watches


class DoProgress:
    """Progress lines for one walk: `step` brackets a step, `tick` is the heartbeat's one beat."""

    def __init__(
        self,
        write: Callable[[str], None] = write_progress_to_stderr,
        *,
        clock: Callable[[], float] = time.monotonic,
        interval: float = DO_HEARTBEAT_SECONDS,
        poll: float = _HEARTBEAT_POLL_SECONDS,
    ) -> None:
        self._write = write
        self._clock = clock
        self._interval = interval
        self._poll = poll
        self._active: tuple[str, float, Callable[[], str]] | None = None
        self._last_beat = 0.0
        self._lock = threading.Lock()

    def line(self, text: str) -> None:
        """Say one thing now."""
        self._write(f"{DO_PROGRESS_PREFIX} {text}")

    def tick(self) -> bool:
        """Say the heartbeat when the active step has been silent for the interval; True when it did."""
        with self._lock:
            if self._active is None:
                return False
            name, started, describe = self._active
            now = self._clock()
            if now - self._last_beat < self._interval:
                return False
            self._last_beat = now
        self.line(f"{name}: {describe()} — {now - started:.0f}s elapsed")
        return True

    @contextmanager
    def step(self, name: str, intro: str, describe: Callable[[], str] | None = None) -> Iterator[Callable[[str, str], None]]:
        """Announce *name* started, beat while it runs, and yield the function that announces its end.

        The end line is written by calling the yielded ``end(status, detail)``; a step that raises
        ends as ``failed`` before the exception goes on.
        """
        started = self._clock()
        self.line(f"{name} started — {intro}")
        with self._lock:
            self._active = (name, started, describe or (lambda: intro))
            self._last_beat = started
        stop = threading.Event()
        thread = threading.Thread(target=self._beat_until, args=(stop,), daemon=True)
        thread.start()
        ended: list[bool] = []

        def end(status: str, detail: str = "") -> None:
            if ended:
                return
            ended.append(True)
            elapsed = self._clock() - started
            tail = f": {detail[:_END_DETAIL_CHARS]}" if detail and status in ("stopped", "failed") else ""
            self.line(f"{name} {status} — {elapsed:.1f}s{tail}")

        try:
            yield end
        except BaseException:
            end("failed", "an exception ended the step")
            raise
        finally:
            stop.set()
            thread.join(timeout=2 * self._poll)
            with self._lock:
                self._active = None

    def _beat_until(self, stop: threading.Event) -> None:
        while not stop.wait(self._poll):
            self.tick()


def _role_provider(role: str, override: str | None) -> str:
    """The provider *role* resolves to, as the run resolves it; the word `default` when it cannot be told."""
    from packages.orchestration.role_config import resolve_role_config

    try:
        return str(resolve_role_config(role, cli_args={"provider": override} if override else None).provider)
    except Exception:  # noqa: BLE001 — a progress line never stops the walk it describes
        return "default"


def _latest_run_phase(job_id: str) -> str:
    """``role provider`` of the newest run-log event that names one, or "" when the log says none."""
    import json

    from packages.orchestration.data_paths import run_log_dir

    try:
        logs = sorted(Path(run_log_dir(job_id)).glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
        for raw in reversed(logs[-1].read_text(encoding="utf-8").splitlines()[-60:]):
            event = json.loads(raw)
            if event.get("role") and event.get("provider"):
                return f"{event['role']} {event['provider']}"
    except (OSError, ValueError, IndexError):
        return ""
    return ""


def do_step_intro(name: str, ctx: DoContext) -> str:
    """The sentence a step's start line carries: what it does, and which provider if it calls one."""
    if name == "init":
        return "registering the repository"
    if name == "study":
        deterministic = ctx.no_llm or settle_do_lane(ctx).bounded and ctx.tiny_repo
        if deterministic:
            return "deterministic scan, no provider call" + (
                f" (tiny repository, up to {DO_TINY_REPO_MAX_FILES} files)" if ctx.tiny_repo else "")
        return f"scan, narrated by provider {_role_provider('study', None)}"
    if name == "plan":
        lane = settle_do_lane(ctx)
        if lane.bounded or ctx.no_llm:
            return f"bounded one-deliverable lane ({lane.reason}), no provider call"
        return f"full lane ({lane.reason}), planner {_role_provider('planner', ctx.planner_provider)}"
    if name == "shape":
        return "shaping the jobs and their tasks"
    if name == "ui":
        return "opening the cockpit before the run"
    if name == "run":
        return (f"builder {_role_provider('builder', ctx.builder_provider)}, "
                f"reviewer {_role_provider('reviewer', ctx.reviewer_provider)}")
    return "checking what the run proposes" if name == "apply" else name


def do_step_describer(name: str, ctx: DoContext, intro: str) -> Callable[[], str]:
    """What a heartbeat of *name* says: the run names the role the job's own log last named."""
    if name != "run":
        return lambda: intro
    return lambda: (_latest_run_phase(ctx.job_ids[0]) if ctx.job_ids else "") or intro
