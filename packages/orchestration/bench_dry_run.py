"""F082 T001, last item — the bench dry run: a frozen order file to bench rows,
over evidence that was ALREADY recorded.

Nothing here executes an order, starts a runner, or touches a clock. It reads a
directory of recorded gauntlet runs, joins each run to the order id that asked
for it, and produces one :class:`BenchRecord` per requested id. That is the
whole of it: the dry run proves the bench's join is wired end to end without
paying for a real campaign, which is what "a dry-run against recorded fixture
evidence" buys.

A NEW module rather than a function inside
:mod:`packages.orchestration.capability_bench`, and the reason is that module's
own docstring: it promises "no disk read, no network, no clock", and everything
below reads directories. A promise that is true is worth its own file, so the
pure record builder stays pure and the reading lives here.

ADDITIVE by construction (F082 inventory Q11): every gauntlet and bench symbol
this module needs is IMPORTED. Nothing is moved out of a gauntlet module and
nothing in one is edited — the gauntlet's own test files stay green unmodified.

Passing is NOT re-decided here. Each row's ``passed`` is whatever verdict
:func:`packages.orchestration.gauntlet_evaluator.evaluate_evidence_dir` already
reached for that run directory; the definition of a pass is
:data:`packages.orchestration.gauntlet_evaluator.PASS_CRITERIA`, which is on
F082's do-not-touch list.

Reading NEVER raises. A run directory whose ``run.json`` is unreadable or is
not a JSON object contributes no entry to the id map, so the order that asked
for it takes the missing row instead. That mirrors
:func:`packages.orchestration.gauntlet_evidence.load_run`, which documents the
same promise for the same reason: a harness that threw on unreadable evidence
would LOSE the run instead of failing it, and a lost run is invisible in a
history while a failed one is not.

Remedy deliberately does NOT record foreign runs as bench rows. A recorded run
whose ``order_id`` matches no id in ``order_ids`` produces no row at all,
because a row asserts membership in this series and a run from some other order
set is not a member of it. The reverse case — a requested id with no recorded
run — is a row, a failed one carrying
:data:`EVIDENCE_MISSING_CLASS`, because the F082 feature file's A9 rule says a
partial run is "recorded as failed rows with the class, series continues". An
absent order is a failure, never an omission.
"""
from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from packages.orchestration.bench_orders import load_bench_order_set
from packages.orchestration.capability_bench import BenchRecord, build_bench_record
from packages.orchestration.gauntlet_evaluator import evaluate_evidence_dir
from packages.orchestration.gauntlet_evidence import RUN_FILENAME, run_dirs

#: The postmortem class a row carries when the order it names has no recorded
#: run in the evidence directory. Defined once, so nothing invents a second
#: spelling for the same absence.
EVIDENCE_MISSING_CLASS = "evidence_missing"


def _recorded_bodies(evidence_dir: Path) -> dict[str, tuple[dict[str, Any], str]]:
    """Map each recorded run's OWN ``order_id`` to its body and directory name.

    Keyed on what the evidence says about itself rather than on the directory
    name, because the fixture directories are named for what they demonstrate
    (``run-04-injection-provider-api-error``) and the order id inside them is
    not derivable from that. First seen wins if two runs claim one id, and
    ``run_dirs`` sorts, so which one that is stays deterministic.
    """
    bodies: dict[str, tuple[dict[str, Any], str]] = {}
    for run_dir in run_dirs(evidence_dir):
        try:
            body = json.loads((run_dir / RUN_FILENAME).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(body, dict):
            continue
        order_id = str(body.get("order_id", ""))
        if order_id and order_id not in bodies:
            bodies[order_id] = (body, run_dir.name)
    return bodies


def _missing_row(order_id: str, series: str) -> BenchRecord:
    """The row an order gets when the evidence directory recorded no run for it."""
    return BenchRecord(
        order_id=order_id,
        series=series,
        passed=False,
        cost=None,
        wall_s=None,
        repair_rounds=None,
        postmortem_classes=(EVIDENCE_MISSING_CLASS,),
    )


def dry_run_rows(*, order_ids: Iterable[str], evidence_dir: Path,
                 series: str) -> tuple[BenchRecord, ...]:
    """One bench row per requested order id, IN THE ORDER THE IDS WERE GIVEN.

    Never in directory order: the caller's sequence is the bench's sequence, and
    a history whose columns silently re-sorted itself would not be comparable
    across runs.
    """
    bodies = _recorded_bodies(evidence_dir)
    verdicts = {run.run_dir: run for run in evaluate_evidence_dir(evidence_dir).runs}
    rows: list[BenchRecord] = []
    for order_id in order_ids:
        found = bodies.get(order_id)
        if found is None:
            rows.append(_missing_row(order_id, series))
            continue
        body, run_dir_name = found
        rows.append(build_bench_record(
            evidence_body=body,
            series=series,
            verdict=verdicts.get(run_dir_name),
        ))
    return tuple(rows)


def dry_run_from_order_set(*, evidence_dir: Path, series: str,
                           orders_dir: Path | None = None) -> tuple[BenchRecord, ...]:
    """The order-file-to-row path: load the FROZEN set, then join it to evidence.

    The freeze runs first and raises
    :class:`packages.orchestration.bench_orders.BenchOrderSetError` on a set
    that does not match its manifest, so a tampered set refuses before a single
    row exists rather than producing rows nobody can compare.
    """
    orders = load_bench_order_set(orders_dir)
    return dry_run_rows(
        order_ids=tuple(order.id for order in orders),
        evidence_dir=evidence_dir,
        series=series,
    )
