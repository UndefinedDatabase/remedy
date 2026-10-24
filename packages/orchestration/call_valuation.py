"""Each ledger call valued in the one configured currency, with its basis (F158 T002, DECISION F158 D5).

The token ledger's `calls` row is the raw truth of a call — its four token counters and the cost the
provider reported — and nothing here ever writes to it. Beside it, in the same `ledger.sqlite`, this
module keeps one `call_valuations` row per call: the normalized cost, the basis it rests on, the
catalog's pricing version when a catalog priced it, and the cross-check of a provider-reported cost
against the catalog. The table is this module's, with its own schema key in the ledger's `meta`
table, because `packages/orchestration/token_ledger.py` is held at its row of the structure ledger.

The basis rules: a cost the provider reported wins (`provider_reported`); when a catalog also
prices the call, the two are compared and a difference beyond `cost.cross_check_threshold_percent`
is flagged and logged as a warning, never acted on. Without a provider cost, a catalog price computes
the cost (`price_table`). Otherwise the cost is unknown and the row says why. Remedy deliberately
never prices a call whose token counts the provider did not report, never prices a model two
catalogs disagree about, and never converts a foreign-currency price: each of those stays unknown.
"""

from __future__ import annotations

import logging
import sqlite3
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any

from packages.orchestration.cost_currency import COST_CURRENCY_USD
from packages.orchestration.price_catalog import ModelPrice, PriceCatalog
from packages.orchestration.token_ledger import (
    COST_BASIS_PRICE_TABLE,
    COST_BASIS_PROVIDER_REPORTED,
    COST_BASIS_UNKNOWN,
    CallRecord,
)

logger = logging.getLogger(__name__)

#: The ledger table and the `meta` key carrying its schema generation.
CALL_VALUATIONS_TABLE = "call_valuations"
CALL_VALUATIONS_SCHEMA_KEY = "call_valuations_schema_version"
CALL_VALUATIONS_SCHEMA_VERSION = 1

#: The default of `cost.cross_check_threshold_percent`, for a configuration that leaves it unset.
DEFAULT_CROSS_CHECK_THRESHOLD_PERCENT = 5.0

#: Why a call's cost is unknown, or how a provider-reported cost was checked.
VALUATION_NOTE_PROVIDER = "the provider reported this cost"
VALUATION_NOTE_CROSS_CHECKED = "the provider reported this cost; the catalog priced it too"
VALUATION_NOTE_PRICE_TABLE = "computed from the catalog's prices"
VALUATION_NOTE_NO_MODEL = "the call names no model"
VALUATION_NOTE_NO_PRICE = "no price catalog lists this model"
VALUATION_NOTE_AMBIGUOUS = "more than one price catalog lists this model"
VALUATION_NOTE_UNMEASURED = "the provider reported no token counts for this call"
VALUATION_NOTE_FOREIGN = "the catalog prices this model in {price}, not {target}; no exchange rate is configured"

_CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {CALL_VALUATIONS_TABLE} (
    call_id              TEXT PRIMARY KEY,
    model                TEXT,
    adapter              TEXT,
    currency             TEXT NOT NULL,
    normalized_cost      REAL,
    basis                TEXT NOT NULL CHECK (basis IN ('{COST_BASIS_PROVIDER_REPORTED}',
                                                         '{COST_BASIS_PRICE_TABLE}',
                                                         '{COST_BASIS_UNKNOWN}')),
    pricing_version      INTEGER,
    catalog_cost         REAL,
    deviation_percent    REAL,
    cross_check_exceeded INTEGER NOT NULL CHECK (cross_check_exceeded IN (0, 1)),
    price_valid_from     TEXT,
    note                 TEXT NOT NULL
)
"""

_COLUMNS = ("call_id", "model", "adapter", "currency", "normalized_cost", "basis", "pricing_version",
            "catalog_cost", "deviation_percent", "cross_check_exceeded", "price_valid_from", "note")


@dataclass(frozen=True)
class CallValuation:
    """One call's value in `currency`: None where unknown, with the basis and the reason."""

    call_id: str
    model: str | None
    adapter: str | None
    currency: str
    normalized_cost: float | None
    basis: str
    pricing_version: int | None
    catalog_cost: float | None
    deviation_percent: float | None
    cross_check_exceeded: bool
    price_valid_from: str | None
    note: str


def catalog_price_for_model(catalogs: Mapping[str, PriceCatalog],
                            model: str) -> tuple[PriceCatalog, ModelPrice] | None | str:
    """The one catalog listing `model` and its price; None when none does, the ambiguity note when several do."""
    found = [(catalog, price) for _, catalog in sorted(catalogs.items())
             if (price := catalog.price_for(model)) is not None]
    if not found:
        return None
    if len(found) > 1:
        return VALUATION_NOTE_AMBIGUOUS
    return found[0]


def catalog_cost_of(record: CallRecord, price: ModelPrice) -> float | None:
    """The cost of `record`'s token counts at `price`, or None when a count is unreported."""
    counts = (record.tokens_in, record.tokens_out, record.cache_read, record.cache_write)
    if any(count is None for count in counts):
        return None
    rates = (price.input_per_million, price.output_per_million, price.cache_read_per_million,
             price.cache_write_per_million)
    return round(sum(count * rate for count, rate in zip(counts, rates)) / 1_000_000, 10)


def value_ledger_call(record: CallRecord, catalogs: Mapping[str, PriceCatalog], *,
                      currency: str = COST_CURRENCY_USD,
                      threshold_percent: float = DEFAULT_CROSS_CHECK_THRESHOLD_PERCENT) -> CallValuation:
    """Value one ledger call by the basis rules of DECISION F158 D5."""
    # Every provider cost in the ledger is USD (`calls.cost_usd`), and `cost.currency` accepts only usd.
    provider_cost = record.cost_usd if record.cost_basis == COST_BASIS_PROVIDER_REPORTED else None
    adapter = version = catalog_cost = valid_from = None
    note = VALUATION_NOTE_NO_MODEL
    if record.model:
        match = catalog_price_for_model(catalogs, record.model)
        if match is None:
            note = VALUATION_NOTE_NO_PRICE
        elif isinstance(match, str):
            note = match
        else:
            catalog, price = match
            adapter, valid_from = catalog.adapter, price.valid_from.isoformat()
            if price.currency != currency:
                note = VALUATION_NOTE_FOREIGN.format(price=price.currency, target=currency)
            else:
                catalog_cost = catalog_cost_of(record, price)
                note = VALUATION_NOTE_UNMEASURED if catalog_cost is None else VALUATION_NOTE_PRICE_TABLE
                version = None if catalog_cost is None else catalog.pricing_version
    deviation = None
    exceeded = False
    if provider_cost is not None:
        if catalog_cost is not None:
            if provider_cost > 0:
                deviation = round(abs(catalog_cost - provider_cost) / provider_cost * 100, 6)
                exceeded = deviation > threshold_percent
            else:
                exceeded = catalog_cost > 0
        return CallValuation(
            call_id=record.call_id, model=record.model, adapter=adapter, currency=currency,
            normalized_cost=provider_cost, basis=COST_BASIS_PROVIDER_REPORTED,
            pricing_version=version, catalog_cost=catalog_cost, deviation_percent=deviation,
            cross_check_exceeded=exceeded, price_valid_from=valid_from,
            note=VALUATION_NOTE_CROSS_CHECKED if catalog_cost is not None else VALUATION_NOTE_PROVIDER)
    if catalog_cost is not None:
        return CallValuation(
            call_id=record.call_id, model=record.model, adapter=adapter, currency=currency,
            normalized_cost=catalog_cost, basis=COST_BASIS_PRICE_TABLE, pricing_version=version,
            catalog_cost=catalog_cost, deviation_percent=None, cross_check_exceeded=False,
            price_valid_from=valid_from, note=VALUATION_NOTE_PRICE_TABLE)
    return CallValuation(
        call_id=record.call_id, model=record.model, adapter=adapter, currency=currency,
        normalized_cost=None, basis=COST_BASIS_UNKNOWN, pricing_version=None, catalog_cost=None,
        deviation_percent=None, cross_check_exceeded=False, price_valid_from=valid_from, note=note)


def _open(project_id: str | None, path: Path | str | None) -> sqlite3.Connection:
    from packages.orchestration.token_ledger import open_ledger, token_ledger_path_for

    conn = open_ledger(path if path is not None else token_ledger_path_for(str(project_id)))
    with conn:
        conn.execute(_CREATE_TABLE)
        conn.execute("INSERT OR IGNORE INTO meta (key, value) VALUES (?, ?)",
                     (CALL_VALUATIONS_SCHEMA_KEY, str(CALL_VALUATIONS_SCHEMA_VERSION)))
    return conn


def record_call_valuations(valuations: Iterable[CallValuation], *, project_id: str | None = None,
                           path: Path | str | None = None) -> int:
    """Write `valuations` into the ledger's `call_valuations` table; a call valued again is replaced."""
    rows = [asdict(v) | {"cross_check_exceeded": int(v.cross_check_exceeded)} for v in valuations]
    conn = _open(project_id, path)
    try:
        with conn:
            conn.executemany(
                f"INSERT OR REPLACE INTO {CALL_VALUATIONS_TABLE} ({', '.join(_COLUMNS)}) VALUES "
                f"({', '.join(':' + c for c in _COLUMNS)})", rows)
    finally:
        conn.close()
    return len(rows)


def query_call_valuations(*, project_id: str | None = None,
                          path: Path | str | None = None) -> list[CallValuation]:
    """Every valuation the ledger holds, sorted by call id."""
    conn = _open(project_id, path)
    try:
        found = conn.execute(
            f"SELECT {', '.join(_COLUMNS)} FROM {CALL_VALUATIONS_TABLE} ORDER BY call_id").fetchall()
    finally:
        conn.close()
    return [CallValuation(**dict(zip(_COLUMNS, row)) | {"cross_check_exceeded": bool(row[9])})
            for row in found]


def configured_valuation_settings(config: Any = None) -> tuple[str, float]:
    """The configured currency and cross-check threshold, the defaults where unset."""
    from packages.orchestration.cost_currency import COST_CURRENCY_KEY, resolve_cost_currency

    if config is None:
        from packages.orchestration.config import get_config

        config = get_config()
    threshold = config.get("cost.cross_check_threshold_percent")
    return (resolve_cost_currency(config.get(COST_CURRENCY_KEY)),
            DEFAULT_CROSS_CHECK_THRESHOLD_PERCENT if threshold is None else float(threshold))


def value_and_record_calls(records: Iterable[CallRecord], *, project_id: str | None = None,
                           path: Path | str | None = None,
                           catalogs: Mapping[str, PriceCatalog] | None = None,
                           config: Any = None) -> list[CallValuation]:
    """Value `records` against the shipped catalogs and the configuration, record them, warn on a mismatch."""
    from packages.orchestration.price_catalog import load_price_catalogs

    currency, threshold = configured_valuation_settings(config)
    loaded = load_price_catalogs() if catalogs is None else catalogs
    valuations = [value_ledger_call(r, loaded, currency=currency, threshold_percent=threshold)
                  for r in records]
    for v in valuations:
        if v.cross_check_exceeded:
            logger.warning(
                "price cross-check: call %s on model %s cost %s %s as the provider reported it, "
                "and the %s catalog prices it at %s, a difference beyond %s percent",
                v.call_id, v.model, v.normalized_cost, v.currency, v.adapter, v.catalog_cost, threshold)
    record_call_valuations(valuations, project_id=project_id, path=path)
    return valuations


def ledger_call_records(*, project_id: str | None = None,
                        path: Path | str | None = None) -> list[CallRecord]:
    """Every `calls` row of the ledger as the record it was written from, sorted by call id; read only."""
    names = [f.name for f in fields(CallRecord)]
    conn = _open(project_id, path)
    try:
        rows = conn.execute(f"SELECT {', '.join(names)} FROM calls ORDER BY call_id").fetchall()
    finally:
        conn.close()
    return [CallRecord(**dict(zip(names, row))) for row in rows]


@dataclass(frozen=True)
class CallRecomputeResult:
    """What a recompute did: every call examined, the valuations it rewrote and those it left."""

    examined: int
    revalued: int
    unchanged: int


def recompute_call_valuations(*, project_id: str | None = None, path: Path | str | None = None,
                              catalogs: Mapping[str, PriceCatalog] | None = None,
                              config: Any = None) -> CallRecomputeResult:
    """Value every call in the ledger again and rewrite only the valuations that changed.

    The `calls` rows are only read, so the raw counters and the reported costs never change; a
    call valued for the first time counts as revalued, and a second run over the same catalogs
    rewrites nothing.
    """
    from packages.orchestration.price_catalog import load_price_catalogs

    currency, threshold = configured_valuation_settings(config)
    loaded = load_price_catalogs() if catalogs is None else catalogs
    current = {v.call_id: v for v in query_call_valuations(project_id=project_id, path=path)}
    fresh = [value_ledger_call(r, loaded, currency=currency, threshold_percent=threshold)
             for r in ledger_call_records(project_id=project_id, path=path)]
    changed = [v for v in fresh if current.get(v.call_id) != v]
    record_call_valuations(changed, project_id=project_id, path=path)
    return CallRecomputeResult(examined=len(fresh), revalued=len(changed),
                               unchanged=len(fresh) - len(changed))


#: The order a summary lists the bases in: the strongest evidence first.
VALUATION_BASIS_ORDER = (COST_BASIS_PROVIDER_REPORTED, COST_BASIS_PRICE_TABLE, COST_BASIS_UNKNOWN)


@dataclass(frozen=True)
class ValuationBasisTotal:
    """The calls of one basis and their summed normalized cost; None for the unknown basis."""

    basis: str
    calls: int
    normalized_cost: float | None


def summarize_call_valuations(valuations: Iterable[CallValuation]) -> list[ValuationBasisTotal]:
    """One total per basis present, never blending bases, in `VALUATION_BASIS_ORDER`."""
    groups: dict[str, list[CallValuation]] = {}
    for v in valuations:
        groups.setdefault(v.basis, []).append(v)
    return [ValuationBasisTotal(
        basis=basis, calls=len(groups[basis]),
        normalized_cost=None if basis == COST_BASIS_UNKNOWN else round(
            sum(v.normalized_cost or 0.0 for v in groups[basis]), 10))
        for basis in VALUATION_BASIS_ORDER if basis in groups]
