"""F074 T001 — estimate calibration: what tasks of each class really cost, from the cost ledger.

Remedy's estimates start from documented class defaults (`budget.class_default_tokens_*`, F104):
one token count per band, a stated assumption rather than a measurement. This module measures
instead. It reads a project's cost ledger, `ledger.sqlite`, adds up each task's calls per role, finds
the task's class in its job's own record (`jobs/<job_id>/job.json`, `tasks[].task_class`), and keeps,
for every task class and role, the distribution of the totals inside a rolling window: the number
of samples and their 20th, 50th and 80th percentiles, of tokens and of cost (DECISION F074 D1).

The role `all` is the whole task, every role's calls added up, and it is what an estimate reads: a
class with at least `budget.calibration_sample_floor` such samples is CALIBRATED, and the shared
estimator then prices its tasks from the class's P20 to P80 token range instead of the band's
default, with the basis label `calibrated(n)`. A class below the floor keeps the default and says
so, class by class.

Outlier damping: before the percentiles are taken, one sample in twenty, and at least one, is
trimmed from each end of a class's sorted values once it has three or more, so one runaway task
cannot drag a small class's P80 to itself.

The computation is read-only on the ledger: it opens it with `mode=rw` and `PRAGMA query_only=1`,
the reader `token_ledger` uses for every query, so a read can neither create nor migrate nor write
it. The table is cached as `calibration_snapshot.json` beside the ledger and rebuilt on the next
read once it is older than `budget.calibration_snapshot_max_age_seconds`, or was built with another
window or floor; nothing refreshes it in the background.

Remedy deliberately does not calibrate a task with no class on record (a job record that is gone or
names none), a task whose calls did not all report their tokens, or the teacher's calls, which belong
to no task: such a sample is counted as unclassified or unmeasured, never guessed.
"""

from __future__ import annotations

import json
import logging
import math
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

#: The role key of a whole task, every role's calls added up; the one an estimate reads.
TASK_TOTAL_ROLE = "all"

#: The snapshot file, beside the project's ledger, and the schema generation of its JSON.
CALIBRATION_SNAPSHOT_FILENAME = "calibration_snapshot.json"
CALIBRATION_SNAPSHOT_SCHEMA = 1

#: The defaults of `budget.calibration_sample_floor`, `budget.calibration_window_days` and
#: `budget.calibration_snapshot_max_age_seconds` (DECISION F074 D1 (3)).
DEFAULT_CALIBRATION_SAMPLE_FLOOR = 20
DEFAULT_CALIBRATION_WINDOW_DAYS = 90
DEFAULT_CALIBRATION_SNAPSHOT_MAX_AGE_SECONDS = 3600

#: The prefix every calibrated basis label opens with; `calibration_basis_label` writes the rest.
CALIBRATED_BASIS_PREFIX = "calibrated("

# A job id is a path segment of the job store; anything else in the ledger is not looked up.
_JOB_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")

# One sample per task and role: the task's calls added up, read in one grouped query.
_SAMPLE_QUERY = """
SELECT job_id, task_id, role,
       SUM(tokens_in), SUM(tokens_out),
       SUM(CASE WHEN tokens_in IS NULL OR tokens_out IS NULL THEN 1 ELSE 0 END),
       SUM(cost_usd),
       SUM(CASE WHEN cost_usd IS NULL OR cost_basis = 'unknown' THEN 1 ELSE 0 END),
       MAX(ts_utc)
FROM calls
WHERE job_id IS NOT NULL AND job_id != '' AND task_id IS NOT NULL AND task_id != ''
GROUP BY job_id, task_id, role
"""


@dataclass(frozen=True)
class CalibrationDistribution:
    """The damped distribution of one measure: the samples counted and three percentiles."""

    n: int
    p20: float
    p50: float
    p80: float

    def to_json(self) -> dict[str, Any]:
        return {"n": self.n, "p20": self.p20, "p50": self.p50, "p80": self.p80}


@dataclass(frozen=True)
class ClassCalibration:
    """One task class and role: its token distribution and, where every call was priced, its cost."""

    task_class: str
    role: str
    tokens: CalibrationDistribution
    cost_usd: CalibrationDistribution | None

    def to_json(self) -> dict[str, Any]:
        return {
            "task_class": self.task_class,
            "role": self.role,
            "tokens": self.tokens.to_json(),
            "cost_usd": None if self.cost_usd is None else self.cost_usd.to_json(),
        }


@dataclass(frozen=True)
class CalibrationTable:
    """A project's calibration: every class and role measured inside the window, and what was not.

    ``ledger_present`` is False when the project has no ledger yet; then ``entries`` is empty and
    every estimate stays on its class default.
    """

    project_id: str
    updated_at: str
    window_days: int
    sample_floor: int
    window_start: str
    ledger_present: bool
    entries: tuple[ClassCalibration, ...]
    unclassified_tasks: int
    unmeasured_tasks: int

    def lookup(self, task_class: str, role: str = TASK_TOTAL_ROLE) -> ClassCalibration | None:
        """The entry of ``task_class`` and ``role``, or None when no sample of it is in the window."""
        for entry in self.entries:
            if entry.task_class == task_class and entry.role == role:
                return entry
        return None

    def calibrated_tokens(self, task_class: str | None) -> CalibrationDistribution | None:
        """The whole-task token distribution of a CALIBRATED class, or None for a class below the floor."""
        if not task_class:
            return None
        entry = self.lookup(task_class)
        if entry is None or entry.tokens.n < self.sample_floor:
            return None
        return entry.tokens

    def to_json(self) -> dict[str, Any]:
        return {
            "schema": CALIBRATION_SNAPSHOT_SCHEMA,
            "project_id": self.project_id,
            "updated_at": self.updated_at,
            "window_days": self.window_days,
            "sample_floor": self.sample_floor,
            "window_start": self.window_start,
            "ledger_present": self.ledger_present,
            "entries": [entry.to_json() for entry in self.entries],
            "unclassified_tasks": self.unclassified_tasks,
            "unmeasured_tasks": self.unmeasured_tasks,
        }


def calibration_basis_label(n: int) -> str:
    """The basis label of an estimate read from a calibrated class of ``n`` samples."""
    return f"{CALIBRATED_BASIS_PREFIX}{n})"


def calibrated_class_tokens(calibration: Any, task_class: str | None) -> CalibrationDistribution | None:
    """The shared estimator's one question: is this task's class calibrated, and to what range?

    ``calibration`` is ``PredictiveBudgetConfig.calibration`` — a ``CalibrationTable`` or None. A
    missing table, a missing class and a class below the floor all answer None, which leaves the
    caller on its class default.
    """
    if not isinstance(calibration, CalibrationTable):
        return None
    return calibration.calibrated_tokens(task_class)


def _percentile(ordered: list[float], fraction: float) -> float:
    # Linear interpolation between the two nearest ranks, the inclusive method.
    if len(ordered) == 1:
        return ordered[0]
    position = fraction * (len(ordered) - 1)
    low = math.floor(position)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def damped_distribution(values: list[float]) -> CalibrationDistribution:
    """The 20th, 50th and 80th percentiles of ``values`` after the outlier trim; ``n`` counts them all.

    From three samples on, ``max(1, n // 20)`` values are trimmed from each end of the sorted list
    before the percentiles are taken, so a single runaway task never sets a class's P80.
    """
    if not values:
        raise ValueError("a distribution needs at least one sample")
    ordered = sorted(float(v) for v in values)
    if len(ordered) >= 3:
        trim = max(1, len(ordered) // 20)
        ordered = ordered[trim:len(ordered) - trim]
    return CalibrationDistribution(
        n=len(values),
        p20=round(_percentile(ordered, 0.2), 6),
        p50=round(_percentile(ordered, 0.5), 6),
        p80=round(_percentile(ordered, 0.8), 6),
    )


def _parse_utc(text: str) -> datetime | None:
    try:
        moment = datetime.fromisoformat(str(text).replace("Z", "+00:00"))
    except ValueError:
        return None
    return moment if moment.tzinfo is not None else moment.replace(tzinfo=timezone.utc)


def _job_task_classes(job_id: str, root: Path | None, cache: dict[str, dict[str, str]]) -> dict[str, str]:
    """``{task_id: task_class}`` from the job's own record; empty when the record is gone or unreadable."""
    if job_id in cache:
        return cache[job_id]
    from packages.orchestration.data_paths import job_record_path

    classes: dict[str, str] = {}
    if _JOB_ID_RE.match(job_id):
        try:
            record = json.loads(job_record_path(job_id, root).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            record = None
        tasks = record.get("tasks") if isinstance(record, dict) else None
        for task in tasks if isinstance(tasks, list) else ():
            if isinstance(task, dict) and task.get("task_id") and task.get("task_class"):
                classes[str(task["task_id"])] = str(task["task_class"])
    cache[job_id] = classes
    return classes


def _connect_ledger_readonly(path: Path) -> sqlite3.Connection:
    from packages.orchestration.token_ledger import _connect_readonly

    return _connect_readonly(path)


def build_calibration_table(
    project_id: str,
    *,
    now: datetime,
    window_days: int = DEFAULT_CALIBRATION_WINDOW_DAYS,
    sample_floor: int = DEFAULT_CALIBRATION_SAMPLE_FLOOR,
    root: Path | None = None,
) -> CalibrationTable:
    """Measure ``project_id``'s ledger: one distribution per task class and role inside the window.

    A task is in the window when its latest call is no older than ``window_days`` before ``now``.
    Read-only on the ledger; raises ``sqlite3.Error`` when the ledger cannot be read.
    """
    from packages.orchestration.token_ledger import token_ledger_path_for

    window_start = now - timedelta(days=window_days)
    table_args = {
        "project_id": str(project_id), "updated_at": now.isoformat(), "window_days": window_days,
        "sample_floor": sample_floor, "window_start": window_start.isoformat(),
    }
    ledger_path = token_ledger_path_for(project_id, root)
    if not ledger_path.is_file():
        return CalibrationTable(**table_args, ledger_present=False, entries=(), unclassified_tasks=0,
                                unmeasured_tasks=0)
    conn = _connect_ledger_readonly(ledger_path)
    try:
        rows = conn.execute(_SAMPLE_QUERY).fetchall()
    finally:
        conn.close()

    # Per task: its calls per role, and the latest call of any role, which places it in the window.
    tasks: dict[tuple[str, str], dict[str, Any]] = {}
    for job_id, task_id, role, tok_in, tok_out, unmeasured, cost, unpriced, latest in rows:
        task = tasks.setdefault((str(job_id), str(task_id)), {"roles": {}, "latest": None})
        task["roles"][str(role or "unknown")] = (
            None if unmeasured else int(tok_in) + int(tok_out),
            None if unpriced else float(cost),
        )
        moment = _parse_utc(latest)
        if moment is not None and (task["latest"] is None or moment > task["latest"]):
            task["latest"] = moment

    classes_by_job: dict[str, dict[str, str]] = {}
    samples: dict[tuple[str, str], tuple[list[float], list[float]]] = {}
    unclassified = unmeasured = 0
    for (job_id, task_id), task in sorted(tasks.items()):
        if task["latest"] is None or task["latest"] < window_start:
            continue
        task_class = _job_task_classes(job_id, root, classes_by_job).get(task_id)
        if task_class is None:
            unclassified += 1
            continue
        role_values = dict(task["roles"])
        if any(tokens is None for tokens, _cost in role_values.values()):
            unmeasured += 1
        else:
            costs = [cost for _tokens, cost in role_values.values()]
            role_values[TASK_TOTAL_ROLE] = (
                sum(tokens for tokens, _cost in role_values.values()),
                None if any(cost is None for cost in costs) else sum(costs),
            )
        for role, (tokens, cost) in role_values.items():
            if tokens is None:
                continue
            token_values, cost_values = samples.setdefault((task_class, role), ([], []))
            token_values.append(tokens)
            if cost is not None:
                cost_values.append(cost)

    entries = tuple(
        ClassCalibration(
            task_class=task_class, role=role, tokens=damped_distribution(token_values),
            cost_usd=damped_distribution(cost_values) if cost_values else None)
        for (task_class, role), (token_values, cost_values) in sorted(samples.items())
    )
    return CalibrationTable(**table_args, ledger_present=True, entries=entries,
                            unclassified_tasks=unclassified, unmeasured_tasks=unmeasured)


def _distribution_from_json(raw: Any) -> CalibrationDistribution:
    return CalibrationDistribution(n=int(raw["n"]), p20=float(raw["p20"]), p50=float(raw["p50"]),
                                   p80=float(raw["p80"]))


def calibration_table_from_json(raw: dict[str, Any]) -> CalibrationTable:
    """The table a snapshot holds; raises ``KeyError``, ``TypeError`` or ``ValueError`` on a bad one."""
    if raw.get("schema") != CALIBRATION_SNAPSHOT_SCHEMA:
        raise ValueError(f"calibration snapshot schema {raw.get('schema')!r} is not {CALIBRATION_SNAPSHOT_SCHEMA}")
    entries = tuple(
        ClassCalibration(
            task_class=str(item["task_class"]), role=str(item["role"]),
            tokens=_distribution_from_json(item["tokens"]),
            cost_usd=None if item["cost_usd"] is None else _distribution_from_json(item["cost_usd"]))
        for item in raw["entries"]
    )
    return CalibrationTable(
        project_id=str(raw["project_id"]), updated_at=str(raw["updated_at"]),
        window_days=int(raw["window_days"]), sample_floor=int(raw["sample_floor"]),
        window_start=str(raw["window_start"]), ledger_present=bool(raw["ledger_present"]),
        entries=entries, unclassified_tasks=int(raw["unclassified_tasks"]),
        unmeasured_tasks=int(raw["unmeasured_tasks"]),
    )


def calibration_snapshot_path(project_id: str, root: Path | None = None) -> Path:
    """``<data_root>/projects/<project_id>/calibration_snapshot.json``, beside the project's ledger."""
    from packages.orchestration.token_ledger import token_ledger_path_for

    return token_ledger_path_for(project_id, root).with_name(CALIBRATION_SNAPSHOT_FILENAME)


def load_calibration_table(
    project_id: str,
    *,
    now: datetime | None = None,
    window_days: int = DEFAULT_CALIBRATION_WINDOW_DAYS,
    sample_floor: int = DEFAULT_CALIBRATION_SAMPLE_FLOOR,
    max_age_seconds: int = DEFAULT_CALIBRATION_SNAPSHOT_MAX_AGE_SECONDS,
    root: Path | None = None,
) -> CalibrationTable:
    """The project's calibration: the snapshot while it is fresh, otherwise a new measurement.

    A snapshot is used only when it parses, was built with this window and floor, and is no older
    than ``max_age_seconds``; otherwise the ledger is measured again and, when a ledger exists, the
    new table replaces the snapshot. A snapshot that cannot be written leaves the measurement in use.
    """
    from packages.common.secure_fs import durable_write_json

    moment = now or datetime.now(timezone.utc)
    path = calibration_snapshot_path(project_id, root)
    try:
        cached = calibration_table_from_json(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError):
        cached = None
    if cached is not None and cached.window_days == window_days and cached.sample_floor == sample_floor:
        built = _parse_utc(cached.updated_at)
        if built is not None and timedelta(0) <= moment - built <= timedelta(seconds=max_age_seconds):
            return cached
    table = build_calibration_table(project_id, now=moment, window_days=window_days,
                                    sample_floor=sample_floor, root=root)
    if table.ledger_present:
        try:
            durable_write_json(path, table.to_json())
        except OSError:
            logger.warning("calibration snapshot %s could not be written; the measurement is used unsaved",
                           path, exc_info=True)
    return table


def resolve_calibration_for_root(
    project_root: str | Path,
    *,
    window_days: int,
    sample_floor: int,
    max_age_seconds: int,
) -> CalibrationTable | None:
    """The calibration of the registered project owning ``project_root``, or None.

    None when no registered project owns the path or its ledger cannot be read: an estimate then
    stays on its class defaults, and a broken calibration never stops a command or a job.
    """
    from packages.orchestration.project_registry import resolve_project
    from packages.orchestration.worktrees import WorktreeError

    try:
        project = resolve_project(project_root)
        if project is None:
            return None
        return load_calibration_table(str(project.id), window_days=window_days, sample_floor=sample_floor,
                                      max_age_seconds=max_age_seconds)
    except (OSError, ValueError, sqlite3.Error, WorktreeError):
        logger.warning("estimate calibration for %r could not be read; estimates stay on class defaults",
                       str(project_root), exc_info=True)
        return None
