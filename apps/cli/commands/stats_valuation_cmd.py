"""`remedy stats valuations` and `remedy stats recompute-costs` (F158 T003, DECISION F158 D7).

`valuations` reads each call's valuation beside its ledger row: the calls and the normalized cost
per basis, never blended into one figure, the calls whose provider-reported cost the catalog prices
more than the threshold apart, and every catalog price older than the stale window — warned about,
never blocking. `recompute-costs` values every call of a project's ledger again after a catalog
changed and rewrites only the valuations that changed; it reads the `calls` rows and never writes
them, so the raw counters stay what the provider reported.
"""

from __future__ import annotations

import argparse
import datetime
from collections.abc import Callable
from pathlib import Path

# WHY: one project's ledger is resolved exactly as `stats backfill-ledger` resolves it.
from apps.cli.commands.stats_ledger_cmd import _one_project_ledger
from apps.cli.json_envelope import emit_ok, fail

EXIT_ERROR = 1


def _catalogs(catalog_dir: str | None, *, json_output: bool) -> dict:
    from packages.orchestration.price_catalog import PriceCatalogError, load_price_catalogs

    try:
        return load_price_catalogs(Path(catalog_dir) if catalog_dir else None)
    except PriceCatalogError as exc:
        fail("invalid_price_catalog", str(exc), json_output=json_output, exit_code=EXIT_ERROR)


def _stale_window_days() -> int:
    """`cost.catalog_stale_days`; the registry's default of 60 means it is always set."""
    from packages.orchestration.config import get_config

    return int(get_config().get("cost.catalog_stale_days"))


def _cmd_stats_recompute_costs(*, project: str | None, all_projects: bool, catalog_dir: str | None,
                               json_output: bool) -> None:
    from packages.orchestration.call_valuation import recompute_call_valuations

    ledger = _one_project_ledger(project, all_projects, action="recompute-costs",
                                 json_output=json_output)
    result = recompute_call_valuations(path=ledger,
                                       catalogs=_catalogs(catalog_dir, json_output=json_output))
    if json_output:
        emit_ok(ledger=str(ledger), examined=result.examined, revalued=result.revalued,
                unchanged=result.unchanged)
        return
    print(f"Recompute of the call valuations in {ledger}")
    print(f"  examined:  {result.examined} call(s)")
    print(f"  revalued:  {result.revalued} call(s) whose valuation changed")
    print(f"  unchanged: {result.unchanged} call(s)")
    print("The calls themselves were only read: their token counts and reported costs are unchanged.")


def _cmd_stats_valuations(*, project: str | None, all_projects: bool, catalog_dir: str | None,
                          json_output: bool) -> None:
    from packages.orchestration.call_valuation import (
        query_call_valuations,
        summarize_call_valuations,
    )
    from packages.orchestration.cost_currency import COST_CURRENCY_USD
    from packages.orchestration.price_catalog import stale_model_prices

    ledger = _one_project_ledger(project, all_projects, action="valuations", json_output=json_output)
    valuations = query_call_valuations(path=ledger)
    totals = summarize_call_valuations(valuations)
    currency = valuations[0].currency if valuations else COST_CURRENCY_USD
    flagged = [v for v in valuations if v.cross_check_exceeded]
    window = _stale_window_days()
    today = datetime.date.today()
    stale = [(catalog.adapter, price)
             for catalog in _catalogs(catalog_dir, json_output=json_output).values()
             for price in stale_model_prices(catalog, today=today, window_days=window)]

    if json_output:
        emit_ok(
            ledger=str(ledger), currency=currency,
            bases=[{"basis": t.basis, "calls": t.calls, "normalized_cost": t.normalized_cost}
                   for t in totals],
            flagged=[{"call_id": v.call_id, "model": v.model, "normalized_cost": v.normalized_cost,
                      "catalog_cost": v.catalog_cost, "deviation_percent": v.deviation_percent}
                     for v in flagged],
            stale_window_days=window,
            stale=[{"adapter": adapter, "model": p.model, "valid_from": p.valid_from.isoformat()}
                   for adapter, p in stale])
        return
    print(f"Call valuations in {ledger}, in {currency}")
    if not totals:
        print("  no call has been valued yet")
    for t in totals:
        cost = "unknown" if t.normalized_cost is None else f"{t.normalized_cost:.6f} {currency}"
        print(f"  {t.basis:<18} {t.calls:>5} call(s)  {cost}")
    for v in flagged:
        apart = ("" if v.deviation_percent is None
                 else f", {v.deviation_percent} percent apart")
        print(f"warning: cross-check: call {v.call_id} on model {v.model} cost {v.normalized_cost} "
              f"{currency} as the provider reported it, and the catalog prices it at "
              f"{v.catalog_cost}{apart}")
    for adapter, p in stale:
        print(f"warning: stale price: the {adapter} catalog's price for {p.model} is valid from "
              f"{p.valid_from.isoformat()}, more than {window} days ago; it is still used")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "stats.valuations": lambda args: _cmd_stats_valuations(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        catalog_dir=getattr(args, "catalog_dir", None),
        json_output=getattr(args, "json", False),
    ),
    "stats.recompute-costs": lambda args: _cmd_stats_recompute_costs(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        catalog_dir=getattr(args, "catalog_dir", None),
        json_output=getattr(args, "json", False),
    ),
}
