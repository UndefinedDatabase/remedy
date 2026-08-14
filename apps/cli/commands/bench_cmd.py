"""`remedy stats bench` (F082 T003a) — the capability trend, read only.

ONE command over the append-only bench history: show the latest run of a series,
the runs before it, and the regression warnings that comparison produced. It
opens the history file for READING and nothing else — it never appends, never
creates the file, never migrates it. Running the bench is a different command in
a later round; a read view that could start a run would make `stats bench` unsafe
to type.

A NEW module rather than a fifth command inside
:mod:`apps.cli.commands.stats_ledger_cmd`, for the reason that module's own
docstring gives: it scopes itself to "the per-project SQLite ledger", and the
bench history is a JSON-lines file with no ledger, no schema and no mirror to
reconcile. The same split :mod:`packages.orchestration.bench_dry_run` made
against :mod:`packages.orchestration.capability_bench` — a promise that is true
is worth its own file.

NO PRICE IS COMPUTED AND NO ABSENCE PRINTS AS A ZERO. ``BenchRecord.cost`` is a
token dict or ``None`` and ``wall_s`` is a float or ``None``; an absent figure
prints the WORD :data:`UNMEASURED` in the table and carries that same word in a
``_basis`` key of the JSON, where the figure itself stays ``null``. The word is
IMPORTED from :mod:`apps.cli.commands.stats_ledger_cmd` rather than respelled
here, so the two views cannot come to print two different words for one absence
(AGENTS.md, Code Discoverability).

Remedy deliberately does NOT render a repair-rounds column.
``BenchRecord.repair_rounds`` is ``None`` at every row by construction — that
field's own comment traces ``repair_rounds_used`` to the ``JobExecution``
boundary where it is dropped — so the column would be identical placeholders on
every line. The limit is stated once, in a sentence, where a reader would search
for the column: see :data:`_REPAIR_ROUNDS_NOTE`.

THE REGRESSION RULE LIVES IN ONE PLACE AND IT IS NOT HERE.
:func:`packages.orchestration.bench_history.bench_regressions` decides what a
regression is, and :meth:`BenchRegression.describe` already names the order and
both numbers, which is F082's acceptance criterion. This module renders that
sentence; it re-derives no threshold, re-implements no median and re-decides no
pass.
"""
from __future__ import annotations

import json as _json
import sys
from pathlib import Path
from typing import Any

from apps.cli.commands.stats_ledger_cmd import UNMEASURED
from packages.orchestration.bench_history import (
    REGRESSION_MULTIPLIER_DEFAULT,
    BenchHistoryEntry,
    BenchRegression,
    bench_history_path_for,
    load_bench_history,
)

EXIT_USAGE = 2
EXIT_ERROR = 1

#: The payload version, so a consumer of `--json` can tell shapes apart.
BENCH_OUTPUT_VERSION = 1

#: What a measured figure's basis reads as, opposite :data:`UNMEASURED`.
MEASURED = "measured"

#: Why no repair-round figure appears anywhere in this view. A column of
#: identical placeholders is noise; the limit itself is the information.
_REPAIR_ROUNDS_NOTE = (
    "Repair rounds: no run records them yet. The gauntlet drops "
    "repair_rounds_used at the JobExecution boundary, so every stored row "
    "carries None and there is no repair-round series to regress on — which is "
    "why this view has no repair-round column instead of one full of placeholders."
)

#: Said in both output modes, for the same reason `stats cost` says it.
_NO_PRICE_NOTE = (
    "No price is computed: the bench records token counts, never money."
)

#: The measurement columns of a bench row, in render order, with their headers.
_FIGURE_COLUMNS = (
    ("passed", "Passed"),
    ("cost_tokens", "Cost tokens"),
    ("wall_s", "Wall s"),
)


def _validate_multiplier(raw: str | float | None) -> float:
    """`--multiplier` as a positive float, or a usage error naming the flag.

    Zero and negatives are refused rather than clamped: a multiplier of 0 makes
    every measured run a regression and a negative one makes none, and both
    would be reported as if a comparison had been made.
    """
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        return REGRESSION_MULTIPLIER_DEFAULT
    try:
        value = float(raw)
    except (TypeError, ValueError):
        print(f"Error: --multiplier {raw!r} is not a number", file=sys.stderr)
        raise SystemExit(EXIT_USAGE) from None
    if value <= 0:
        print(f"Error: --multiplier {raw!r} must be greater than 0", file=sys.stderr)
        raise SystemExit(EXIT_USAGE)
    return value


def _one_project_history(project: str | None) -> tuple[Path, str]:
    """The single project's history file, plus a human label for the scope.

    EXACTLY ONE PROJECT and no `--all-projects`: two projects' benches are two
    independent trends over two different order sets, and folding them would
    compare an order against a median it never ran in. The path is COMPUTED, not
    created — nothing here touches the disk.
    """
    from packages.orchestration.project_scope import resolve_scope

    scope = resolve_scope(project_flag=project, all_projects=False)
    if scope.project_id is None:
        print(
            "Error: no project resolved for stats bench. Run inside a registered "
            "project or pass --project <slug-or-uuid>.",
            file=sys.stderr,
        )
        raise SystemExit(EXIT_ERROR)
    return bench_history_path_for(scope.project_id), f"project {scope.project_id}"


def _series_present(entries: tuple[BenchHistoryEntry, ...]) -> tuple[str, ...]:
    """Every series the file holds, in first-seen order."""
    seen: list[str] = []
    for entry in entries:
        if entry.record.series not in seen:
            seen.append(entry.record.series)
    return tuple(seen)


def _latest_series(entries: tuple[BenchHistoryEntry, ...]) -> str:
    """The series of the highest ``run_seq`` in the file.

    File order breaks a tie, so two series sharing the highest sequence number
    resolve to the one written first rather than to whichever way a set happened
    to iterate. The caller NAMES the answer either way — see
    :func:`_render_bench_human`; never silently picking one of several is the
    point of returning the other names alongside it.
    """
    top = max(entry.run_seq for entry in entries)
    return next(entry.record.series for entry in entries if entry.run_seq == top)


def _cost_tokens(record) -> int | None:
    """The row's token total, or ``None`` when the run measured no tokens."""
    return None if record.cost is None else sum(record.cost.values())


def _figure(value: Any) -> str:
    """One measurement as a table cell — or the word standing in for its absence."""
    if value is None:
        return UNMEASURED
    if isinstance(value, bool):
        return "yes" if value else "NO"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _basis(value: Any) -> str:
    """The one word saying whether a figure was measured at all."""
    return UNMEASURED if value is None else MEASURED


def _row_payload(entry: BenchHistoryEntry) -> dict[str, Any]:
    """One stored row as JSON: every figure keeps its own basis word beside it.

    The figure stays ``null`` when nobody measured it — never 0, never "" — and
    the sibling ``*_basis`` key carries the same word the table prints, so a
    consumer reading only the figures cannot mistake an absence for a zero and
    one reading the basis never has to guess which absence it is looking at.
    """
    record = entry.record
    return {
        "run_seq": entry.run_seq,
        "order_id": record.order_id,
        "series": record.series,
        "passed": record.passed,
        "passed_basis": _basis(record.passed),
        "cost_tokens": _cost_tokens(record),
        "cost_basis": _basis(record.cost),
        "cost": dict(record.cost) if record.cost is not None else None,
        "wall_s": record.wall_s,
        "wall_basis": _basis(record.wall_s),
        "postmortem_classes": list(record.postmortem_classes),
    }


def _regression_payload(warning: BenchRegression) -> dict[str, Any]:
    """One warning as JSON, carrying the rendered sentence it also prints.

    ``describe`` is included rather than left to the consumer to rebuild: it is
    the text that names the order and both numbers, and two spellings of one
    warning is how they drift apart.
    """
    return {
        "kind": warning.kind,
        "order_id": warning.order_id,
        "series": warning.series,
        "latest": warning.latest,
        "baseline": warning.baseline,
        "multiplier": warning.multiplier,
        "describe": warning.describe(),
    }


def _bench_payload(*, path: Path, scope_label: str, series: str | None,
                   selected_by: str, available: tuple[str, ...],
                   rows: list[BenchHistoryEntry], run_seqs: list[int],
                   warnings: tuple[BenchRegression, ...],
                   multiplier: float) -> dict[str, Any]:
    """The `--json` document: what was read, which series, and what it compared."""
    compared = len(run_seqs) >= 2
    return {
        "version": BENCH_OUTPUT_VERSION,
        "scope": scope_label,
        "history_path": str(path),
        "history_exists": path.is_file(),
        "series": series,
        "series_selected_by": selected_by,
        "series_available": list(available),
        "series_not_read": [name for name in available if name != series],
        "multiplier": multiplier,
        "unmeasured_label": UNMEASURED,
        "runs": run_seqs,
        "latest_run": run_seqs[-1] if run_seqs else None,
        "rows": [_row_payload(entry) for entry in rows],
        "comparison": {
            "compared": compared,
            "runs_compared": len(run_seqs),
            "reason": (
                f"{len(run_seqs)} run(s) of this series are recorded; a "
                f"comparison needs at least two, so no warning was computed"
                if not compared else
                f"the latest run was compared against the {len(run_seqs) - 1} "
                f"run(s) before it"
            ),
        },
        "regressions": [_regression_payload(w) for w in warnings],
        "notes": {
            "repair_rounds": _REPAIR_ROUNDS_NOTE,
            "no_price": _NO_PRICE_NOTE,
            "unmeasured": (
                f"a null figure was never measured — it is not a zero; the "
                f"matching *_basis key spells it {UNMEASURED!r}"
            ),
        },
    }


def _render_rows(rows: list[BenchHistoryEntry]) -> list[str]:
    """The row table: one line per stored row, no aggregate and no invented cell."""
    headers = ["Run", "Order", *(label for _, label in _FIGURE_COLUMNS)]
    body = [
        [
            str(entry.run_seq),
            entry.record.order_id,
            _figure(entry.record.passed),
            _figure(_cost_tokens(entry.record)),
            _figure(entry.record.wall_s),
        ]
        for entry in rows
    ]
    widths = [max(len(headers[i]), *(len(r[i]) for r in body)) for i in range(len(headers))]
    # rstrip: the last column is padded like every other, and a table that
    # trails whitespace is a diff hazard wherever the output gets captured.
    lines = ["  ".join(h.ljust(w) for h, w in zip(headers, widths)).rstrip()]
    lines.extend("  ".join(c.ljust(w) for c, w in zip(row, widths)).rstrip() for row in body)
    return lines


def _render_bench_human(*, path: Path, scope_label: str, series: str,
                        selected_by: str, available: tuple[str, ...],
                        rows: list[BenchHistoryEntry], run_seqs: list[int],
                        warnings: tuple[BenchRegression, ...],
                        multiplier: float) -> str:
    """The readable trend: which series was read, its runs, and the warnings."""
    chosen = ("named by --series" if selected_by == "flag"
              else "chosen as the series of the latest run")
    lines = [
        f"Capability bench trend — {scope_label}",
        f"History: {path}",
        f"Series:  {series} ({chosen})",
    ]
    others = [name for name in available if name != series]
    if others:
        lines.append(f"Not read: {', '.join(others)} — "
                     f"{len(others)} other series in this file")
    lines.append(f"Runs:    {len(run_seqs)} of this series "
                 f"({', '.join(str(seq) for seq in run_seqs)}); "
                 f"latest is run {run_seqs[-1]}")

    lines.append("")
    lines.extend(_render_rows(rows))

    lines.append("")
    if len(run_seqs) < 2:
        lines.append(
            f"No comparison was made: only {len(run_seqs)} run of series "
            f"{series} is recorded, and a regression is a comparison against "
            f"the runs before it. This is not the same as 'no regressions'."
        )
    elif warnings:
        lines.append(f"REGRESSIONS ({len(warnings)}), against the trailing median "
                     f"at {multiplier}x:")
        lines.extend(f"  {warning.describe()}" for warning in warnings)
    else:
        lines.append(
            f"No regression: run {run_seqs[-1]} was compared against the "
            f"{len(run_seqs) - 1} run(s) before it at {multiplier}x the trailing "
            f"median, and no order dropped a pass, a token budget or a wall time."
        )

    lines.append("")
    lines.append(f"'{UNMEASURED}' means nobody measured that figure — it is not a zero.")
    lines.append(_REPAIR_ROUNDS_NOTE)
    lines.append(_NO_PRICE_NOTE)
    return "\n".join(lines)


def _cmd_stats_bench(*, series: str | None = None,
                     multiplier: str | float | None = None,
                     project: str | None = None,
                     json_output: bool = False) -> None:
    """Read the history, pick the series, and render its trend. Writes nothing."""
    from packages.orchestration.bench_history import bench_regressions

    factor = _validate_multiplier(multiplier)
    path, scope_label = _one_project_history(project)
    entries = load_bench_history(path)
    available = _series_present(entries)

    # A MISSING HISTORY IS NOT AN EMPTY ONE, and neither is an error: an unrun
    # bench has nothing to say and says so, in a sentence, exiting 0.
    if not entries:
        exists = path.is_file()
        reason = (
            "the file exists but holds no readable row"
            if exists else "nothing has been recorded yet — the bench has not run"
        )
        if json_output:
            print(_json.dumps(_bench_payload(
                path=path, scope_label=scope_label, series=None,
                selected_by="none", available=available, rows=[], run_seqs=[],
                warnings=(), multiplier=factor) | {"empty_reason": reason}, indent=2))
        else:
            print(f"Capability bench trend — {scope_label}")
            print(f"History: {path}")
            print(f"No trend to show: {reason}.")
            print("Nothing was created: 'stats bench' only ever reads this file.")
        return

    requested = (series or "").strip()
    chosen = requested or _latest_series(entries)
    selected_by = "flag" if requested else "latest_run"
    mine = [entry for entry in entries if entry.record.series == chosen]

    if not mine:
        # Naming what IS there beats an empty table that looks like a clean run.
        if json_output:
            print(_json.dumps(_bench_payload(
                path=path, scope_label=scope_label, series=chosen,
                selected_by=selected_by, available=available, rows=[],
                run_seqs=[], warnings=(), multiplier=factor)
                | {"empty_reason": "no row of this series is recorded"}, indent=2))
        else:
            print(f"Capability bench trend — {scope_label}")
            print(f"History: {path}")
            print(f"No row of series {chosen} is recorded. This file holds: "
                  f"{', '.join(available)}.")
        return

    run_seqs = sorted({entry.run_seq for entry in mine})
    warnings = bench_regressions(entries, series=chosen, multiplier=factor)

    if json_output:
        print(_json.dumps(_bench_payload(
            path=path, scope_label=scope_label, series=chosen,
            selected_by=selected_by, available=available, rows=mine,
            run_seqs=run_seqs, warnings=warnings, multiplier=factor), indent=2))
    else:
        print(_render_bench_human(
            path=path, scope_label=scope_label, series=chosen,
            selected_by=selected_by, available=available, rows=mine,
            run_seqs=run_seqs, warnings=warnings, multiplier=factor))


COMMAND_HANDLERS = {
    "stats.bench": lambda args: _cmd_stats_bench(
        series=getattr(args, "series", None),
        multiplier=getattr(args, "multiplier", None),
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
}
