"""F082 T002 — the append-only bench history, the trend read off it, and the
regression rules that turn that trend into a warning.

One file, one job. This module appends bench rows to a JSON-lines history under
the data root's project area, reads them back in file order, and compares the
latest run of a series against the runs before it. It runs no order, starts no
runner and evaluates nothing — every row it stores was built elsewhere.

A NEW module rather than a function inside
:mod:`packages.orchestration.capability_bench`, for the reason that module's own
docstring gives: it promises "no disk read, no network, no clock", and
everything below reads and writes a file. The promise stays true by keeping the
reading out of it — the same split
:mod:`packages.orchestration.bench_dry_run` made.

ADDITIVE by construction (F082 inventory Q11): :class:`BenchRecord` and
:func:`projects_dir` are IMPORTED. No symbol moves out of a bench or gauntlet
module and none is edited.

Remedy deliberately does NOT put a clock in the history. Runs are grouped by an
integer ``run_seq`` derived from the file itself — one more than the highest the
file already holds — and never by a timestamp. That is what makes a golden
fixture comparable byte for byte and a computed trend independent of when the
computation happened to run; a wall-clock field would make both depend on the
minute.

**Unmeasured is ``None``, and ``None`` never warns.** A row whose ``cost`` or
``wall_s`` is absent is not a regression, it is a field nobody measured
(R-0178, and R-0407 for what a false zero costs). Absent values are excluded
from BOTH sides of every comparison rather than read as zero, which is the same
discipline :mod:`packages.orchestration.capability_bench` applies to the row,
applied here to the comparison.
"""
from __future__ import annotations

import json
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import UUID

from packages.orchestration.capability_bench import BenchRecord
from packages.orchestration.data_paths import projects_dir

#: The history file's name inside a project's data directory.
BENCH_HISTORY_FILENAME = "bench_history.jsonl"

#: Envelope version stamped on every line, so a later shape change is readable.
BENCH_HISTORY_VERSION = 1

#: How much worse than the trailing median counts as a regression. 1.5x is the
#: F082 default; every caller may pass its own.
REGRESSION_MULTIPLIER_DEFAULT = 1.5

#: An order that used to pass and does not any more.
REGRESSION_PASS_DROP = "pass_drop"

#: An order whose token total blew past its own trailing median.
REGRESSION_COST = "cost_regression"

#: An order whose wall time blew past its own trailing median.
REGRESSION_WALL = "wall_regression"


def bench_history_path_for(project_id: UUID | str, root: Path | None = None) -> Path:
    """Return ``<data_root>/projects/<project_id>/bench_history.jsonl``.

    ``project_id`` is ``project_registry.RemyProject.id`` — the registry UUID,
    the canonical project identity. It is NOT the sha256 repo-path hash that
    ``worktrees.py`` uses for lock directories; those two must never be swapped.

    The data root is resolved through ``data_paths.projects_dir``, the single
    authoritative reader of the data-root configuration. This module never reads
    that environment variable itself.
    """
    return projects_dir(root) / str(project_id) / BENCH_HISTORY_FILENAME


@dataclass(frozen=True)
class BenchHistoryEntry:
    """One stored bench row, plus the run it belonged to."""

    #: Which run of the history this row came from. Integer, not a timestamp —
    #: see the module docstring for why there is no clock here.
    run_seq: int
    record: BenchRecord

    def to_json(self) -> dict[str, Any]:
        """The line shape the history file stores, one JSON object per row.

        The row is NESTED under its own key rather than flattened into the
        envelope, so no future :class:`BenchRecord` field can ever collide with
        an envelope field.
        """
        return {
            "bench_history_version": BENCH_HISTORY_VERSION,
            "run_seq": self.run_seq,
            "row": self.record.to_json(),
        }


def _record_from_row(row: dict[str, Any]) -> BenchRecord | None:
    """Rebuild a :class:`BenchRecord` from a stored ``row`` object, or ``None``.

    ``None`` means the line is not usable as a row and the caller skips it.
    Absent optional fields stay absent: a missing ``cost`` reads back as
    ``None``, never as an empty dict or a zero.
    """
    order_id = row.get("order_id")
    series = row.get("series")
    if not isinstance(order_id, str) or not isinstance(series, str):
        return None
    passed = row.get("passed")
    cost = row.get("cost")
    wall_s = row.get("wall_s")
    repair_rounds = row.get("repair_rounds")
    classes = row.get("postmortem_classes")
    return BenchRecord(
        order_id=order_id,
        series=series,
        passed=None if passed is None else bool(passed),
        cost={str(k): int(v) for k, v in cost.items()} if isinstance(cost, dict) else None,
        wall_s=float(wall_s) if isinstance(wall_s, (int, float)) and not isinstance(wall_s, bool) else None,
        repair_rounds=int(repair_rounds) if isinstance(repair_rounds, int) and not isinstance(repair_rounds, bool) else None,
        postmortem_classes=tuple(str(c) for c in classes) if isinstance(classes, list) else (),
    )


def load_bench_history(path: Path | str) -> tuple[BenchHistoryEntry, ...]:
    """Every stored entry, in FILE order.

    Reading NEVER raises — the promise :mod:`packages.orchestration.bench_dry_run`
    makes, for the same reason. A missing file is ``()``; a line that is not
    JSON, is not an object, carries no integer ``run_seq`` or carries no usable
    ``row`` is SKIPPED. One corrupt line therefore costs one row instead of the
    whole history, and a half-written final line cannot erase a year of trend.
    """
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError:
        return ()
    entries: list[BenchHistoryEntry] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            body = json.loads(line)
        except ValueError:
            continue
        if not isinstance(body, dict):
            continue
        run_seq = body.get("run_seq")
        row = body.get("row")
        if not isinstance(run_seq, int) or isinstance(run_seq, bool) or not isinstance(row, dict):
            continue
        record = _record_from_row(row)
        if record is None:
            continue
        entries.append(BenchHistoryEntry(run_seq=run_seq, record=record))
    return tuple(entries)


def next_run_seq(path: Path | str) -> int:
    """One more than the highest ``run_seq`` the file holds; ``1`` when empty."""
    entries = load_bench_history(path)
    if not entries:
        return 1
    return max(entry.run_seq for entry in entries) + 1


def append_bench_run(records: Iterable[BenchRecord], *, path: Path | str) -> int:
    """Append one whole bench run and return the ``run_seq`` it was given.

    ONE sequence number covers the whole batch: a run is the unit the trend
    compares, so every row of it shares its number. The file is opened for
    APPEND and never for write — a rerun ADDS rows and never rewrites one, which
    is the F082 acceptance criterion "History is append-only (rerun never
    rewrites old rows)". Parent directories are created.

    An empty ``records`` writes nothing at all and returns ``0``: there was no
    run, so no sequence number is spent on it.
    """
    rows = tuple(records)
    if not rows:
        return 0
    target = Path(path)
    seq = next_run_seq(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        for record in rows:
            entry = BenchHistoryEntry(run_seq=seq, record=record)
            handle.write(json.dumps(entry.to_json()) + "\n")
    return seq


@dataclass(frozen=True)
class BenchRegression:
    """One warning about one order, on one series.

    ``latest`` and ``baseline`` are always both carried because the F082
    acceptance criterion is "warns with order and numbers" — a warning that
    names only the order does not meet it.
    """

    kind: str
    order_id: str
    series: str
    latest: float
    baseline: float
    #: The threshold multiplier the comparison used, or ``None`` for a pass
    #: drop, which is not a threshold comparison and has no multiplier.
    multiplier: float | None

    def describe(self) -> str:
        """A one-line warning naming the ORDER and BOTH numbers."""
        if self.multiplier is None:
            return (f"{self.kind}: order {self.order_id} in series {self.series} "
                    f"— latest {self.latest} against a trailing pass rate of {self.baseline}")
        return (f"{self.kind}: order {self.order_id} in series {self.series} "
                f"— latest {self.latest} against a trailing median of {self.baseline} "
                f"(over {self.multiplier}x)")


def _median(values: Sequence[float]) -> float:
    """The median of a NON-EMPTY sequence; mean of the middle two when even.

    The median and not the mean, deliberately: one catastrophic run must not
    raise the bar every later run is compared against, and an average lets it.
    """
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return float(ordered[middle])
    return (float(ordered[middle - 1]) + float(ordered[middle])) / 2.0


def _cost_total(record: BenchRecord) -> float | None:
    """The row's token total, or ``None`` when the run measured no tokens."""
    if record.cost is None:
        return None
    return float(sum(record.cost.values()))


def _wall_total(record: BenchRecord) -> float | None:
    """The row's wall time, or ``None`` when nobody measured it."""
    return None if record.wall_s is None else float(record.wall_s)


def _threshold_regression(kind: str, order_id: str, series: str,
                          latest: float | None, trailing: Sequence[float],
                          multiplier: float) -> BenchRegression | None:
    """A regression when ``latest`` exceeds ``multiplier`` times the trailing median.

    ``None`` on either side means unmeasured, and unmeasured never warns: an
    absent latest value or an empty trailing series produces no warning at all.
    """
    if latest is None or not trailing:
        return None
    baseline = _median(trailing)
    if latest <= baseline * multiplier:
        return None
    return BenchRegression(kind=kind, order_id=order_id, series=series,
                           latest=latest, baseline=baseline, multiplier=multiplier)


def bench_regressions(entries: Iterable[BenchHistoryEntry], *, series: str,
                      multiplier: float = REGRESSION_MULTIPLIER_DEFAULT
                      ) -> tuple[BenchRegression, ...]:
    """Warnings for the LATEST run of ``series``, against the runs before it.

    Entries of every other series are ignored entirely — two series in one file
    are two independent trends. Fewer than two runs of this series returns
    ``()``: a first run has nothing to regress against, and warning about it
    would be warning about the baseline itself.

    Per order id present in the latest run, in THAT run's row order, at most one
    warning of each kind is emitted, in the fixed order pass, cost, wall.
    """
    mine = [entry for entry in entries if entry.record.series == series]
    seqs = {entry.run_seq for entry in mine}
    if len(seqs) < 2:
        return ()
    latest_seq = max(seqs)
    latest_rows = [entry.record for entry in mine if entry.run_seq == latest_seq]
    trailing_rows = [entry.record for entry in mine if entry.run_seq < latest_seq]

    warnings: list[BenchRegression] = []
    for row in latest_rows:
        earlier = [r for r in trailing_rows if r.order_id == row.order_id]

        judged = [r.passed for r in earlier if r.passed is not None]
        if row.passed is False and judged:
            rate = sum(1 for p in judged if p) / len(judged)
            if rate > 0:
                warnings.append(BenchRegression(
                    kind=REGRESSION_PASS_DROP, order_id=row.order_id, series=series,
                    latest=0.0, baseline=rate, multiplier=None,
                ))

        for kind, reader in ((REGRESSION_COST, _cost_total), (REGRESSION_WALL, _wall_total)):
            trailing = [value for value in (reader(r) for r in earlier) if value is not None]
            found = _threshold_regression(kind, row.order_id, series,
                                          reader(row), trailing, multiplier)
            if found is not None:
                warnings.append(found)
    return tuple(warnings)
