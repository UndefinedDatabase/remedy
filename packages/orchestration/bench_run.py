"""F082 — the on-demand bench run: a frozen order set through a campaign into a
history file.

The entry point the F082 inventory's Q6 found MISSING. Everything on either
side of it already existed — the frozen set
(:mod:`packages.orchestration.bench_orders`), the campaign
(:func:`packages.orchestration.gauntlet_runner.run_campaign`), the
evidence-to-row join (:mod:`packages.orchestration.bench_dry_run`) and the
append-only history (:mod:`packages.orchestration.bench_history`). Nothing
joined them, so a bench run was four calls a caller had to know how to order.
This module IS that join, and it is nothing else.

ADDITIVE by construction (F082 inventory Q11): every product symbol below is
IMPORTED. No gauntlet module is edited and no symbol moves out of one.

NO FAKE LIVES HERE. There is no double, no stub and no test-only branch in this
file. A run that touches no network is a run whose :class:`RunnerDeps` the
CALLER substituted — that dataclass is the seam, and every default it carries
stays the production one. A production module that knew tests existed would be
the thing F082 is supposed to measure rather than the thing measuring it.

NO CLOCK LIVES HERE EITHER, and yet the numbers are still clock-derived: a
row's ``wall_s`` comes from
:func:`packages.orchestration.gauntlet_runner.run_order`, which calls
``time.monotonic()`` around the mission it drives. That is ACKNOWLEDGED rather
than removed, because removing it would edit a gauntlet module. A reader
looking for the bench's clock finds the honest answer here: the bench keeps no
clock, and the wall time it records is the runner's.

BOTH ROOTS ARE REQUIRED ARGUMENTS, deliberately. ``run_campaign`` defaults
``real_data_root`` to ``data_paths.resolve_data_root()``, and
``bench_history.bench_history_path_for`` resolves through
``data_paths.projects_dir`` — either default lands in the OPERATOR's real data
root. Here both are keyword arguments with NO default, so a caller that forgets
one gets a :class:`TypeError` instead of a write into the operator's world.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.bench_dry_run import dry_run_from_order_set
from packages.orchestration.bench_history import append_bench_run
from packages.orchestration.bench_orders import load_bench_order_set
from packages.orchestration.gauntlet_runner import RunnerDeps, run_campaign


@dataclass(frozen=True)
class BenchRunResult:
    """Everything one bench run produced, so a caller need not re-read the disk."""

    #: One outcome per order, exactly as ``run_campaign`` returned them; each is
    #: a ``gauntlet_runner.OrderOutcome``.
    outcomes: tuple[Any, ...]
    #: One bench row per frozen order, in the order set's own order; each is a
    #: ``capability_bench.BenchRecord``.
    rows: tuple[Any, ...]
    #: The sequence number ``append_bench_run`` spent on this run, or ``0`` when
    #: there was nothing to append.
    run_seq: int


# WHY the freeze runs BEFORE the campaign: a tampered set refuses before any order executes.
def run_bench_campaign(*, campaign_root: Path, data_root: Path,
                       history_path: Path, series: str,
                       orders_dir: Path | None = None,
                       deps: RunnerDeps | None = None) -> BenchRunResult:
    """Run the frozen bench set once and append its rows to ``history_path``.

    ``campaign_root`` IS the evidence directory the join reads back:
    ``run_campaign`` writes one ``run.json`` per run beneath it, and
    ``bench_dry_run`` keys each recorded body on the ``order_id`` that body
    carries itself, so nothing has to agree about directory names.

    ``BenchOrder.order`` IS a real ``GauntletOrder``, so the set the freeze
    validated is handed to the runner unconverted and uncopied.
    """
    orders = load_bench_order_set(orders_dir)
    outcomes = run_campaign(tuple(bench.order for bench in orders), campaign_root,
                            deps=deps, real_data_root=data_root)
    rows = dry_run_from_order_set(evidence_dir=campaign_root, series=series,
                                  orders_dir=orders_dir)
    run_seq = append_bench_run(rows, path=history_path)
    return BenchRunResult(outcomes=tuple(outcomes), rows=tuple(rows),
                          run_seq=run_seq)
