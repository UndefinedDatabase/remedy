"""Each ledger call valued (F158 T002, DECISION F158 D5): the basis rules as goldens across mixed
bases, the cross-check at its threshold boundary, the table beside the untouched `calls` rows, the
configuration and the live hook."""

from __future__ import annotations

import datetime
import hashlib
import logging
import sqlite3

import pytest

from packages.orchestration.call_valuation import (
    CALL_VALUATIONS_SCHEMA_KEY,
    CALL_VALUATIONS_TABLE,
    VALUATION_NOTE_AMBIGUOUS,
    VALUATION_NOTE_CROSS_CHECKED,
    VALUATION_NOTE_NO_MODEL,
    VALUATION_NOTE_NO_PRICE,
    VALUATION_NOTE_PRICE_TABLE,
    VALUATION_NOTE_PROVIDER,
    VALUATION_NOTE_UNMEASURED,
    CallValuation,
    configured_valuation_settings,
    query_call_valuations,
    record_call_valuations,
    value_and_record_calls,
    value_ledger_call,
)
from packages.orchestration.cost_currency import CostCurrencyError
from packages.orchestration.price_catalog import ModelPrice, PriceCatalog, parse_price_catalog
from packages.orchestration.token_ledger import (
    COST_BASIS_PROVIDER_REPORTED,
    COST_BASIS_UNKNOWN,
    CallRecord,
    open_ledger,
    record_call,
)

CATALOG = parse_price_catalog("""
[catalog]
adapter = "claude-cli"
pricing_version = 3

[models."m-usd"]
input_per_million = 2
output_per_million = 10
cache_read_per_million = 0.5
cache_write_per_million = 2.5
currency = "usd"
valid_from = 2026-10-01
source = "fixture"

[models."m-eur"]
input_per_million = 2
output_per_million = 10
cache_read_per_million = 0.5
cache_write_per_million = 2.5
currency = "eur"
valid_from = 2026-10-01
source = "fixture"

[models."m-both"]
input_per_million = 1
output_per_million = 1
cache_read_per_million = 0
cache_write_per_million = 0
currency = "usd"
valid_from = 2026-10-01
source = "fixture"
""", adapter="claude-cli")
# A second catalog listing one of the same models, to make that model ambiguous.
OTHER = PriceCatalog(adapter="other", pricing_version=1, prices=(ModelPrice(
    model="m-both", input_per_million=9.0, output_per_million=9.0, cache_read_per_million=0.0,
    cache_write_per_million=0.0, currency="usd", valid_from=datetime.date(2026, 10, 1), source="x"),))
CATALOGS = {"claude-cli": CATALOG, "other": OTHER}
FOREIGN = "the catalog prices this model in eur, not usd; no exchange rate is configured"


def _call(call_id, model, *, cost=None, tokens=(0, 0, 0, 0)):
    tin, tout, cread, cwrite = tokens
    return CallRecord(call_id=call_id, model=model, ts_utc="2026-10-24T00:00:00+00:00",
                      tokens_in=tin, tokens_out=tout, cache_read=cread, cache_write=cwrite,
                      cost_usd=cost,
                      cost_basis=COST_BASIS_PROVIDER_REPORTED if cost is not None else COST_BASIS_UNKNOWN)


RECORDS = [
    _call("a-provider-only", "unlisted", cost=0.02),
    _call("b-agrees", "m-usd", cost=0.007, tokens=(1000, 500, 0, 0)),
    _call("c-within", "m-usd", cost=0.0068, tokens=(1000, 500, 0, 0)),
    _call("d-at-boundary", "m-usd", cost=0.01, tokens=(0, 1050, 0, 0)),
    _call("e-beyond", "m-usd", cost=0.01, tokens=(0, 1060, 0, 0)),
    _call("f-catalog-only", "m-usd", tokens=(1000, 500, 2000, 400)),
    _call("g-unmeasured", "m-usd", tokens=(1000, None, 0, 0)),
    _call("h-foreign", "m-eur", tokens=(1000, 500, 0, 0)),
    _call("i-ambiguous", "m-both", tokens=(1000, 500, 0, 0)),
    _call("j-no-model", None, tokens=(1000, 500, 0, 0)),
    _call("k-provider-zero", "m-usd", cost=0.0, tokens=(1000, 500, 0, 0)),
    _call("l-unlisted-unpriced", "unlisted", tokens=(1000, 500, 0, 0)),
    # A cost on a row whose basis is not provider_reported is not the provider's and does not win.
    CallRecord(call_id="m-cost-not-reported", model="m-usd", ts_utc="2026-10-24T00:00:00+00:00",
               tokens_in=1000, tokens_out=500, cache_read=0, cache_write=0, cost_usd=0.5,
               cost_basis="price_table"),
]

# (call_id, adapter, normalized_cost, basis, pricing_version, catalog_cost, deviation, exceeded, valid_from, note)
GOLDENS = [
    ("a-provider-only", None, 0.02, "provider_reported", None, None, None, False, None,
     VALUATION_NOTE_PROVIDER),
    ("b-agrees", "claude-cli", 0.007, "provider_reported", 3, 0.007, 0.0, False, "2026-10-01",
     VALUATION_NOTE_CROSS_CHECKED),
    ("c-within", "claude-cli", 0.0068, "provider_reported", 3, 0.007, 2.941176, False, "2026-10-01",
     VALUATION_NOTE_CROSS_CHECKED),
    ("d-at-boundary", "claude-cli", 0.01, "provider_reported", 3, 0.0105, 5.0, False, "2026-10-01",
     VALUATION_NOTE_CROSS_CHECKED),
    ("e-beyond", "claude-cli", 0.01, "provider_reported", 3, 0.0106, 6.0, True, "2026-10-01",
     VALUATION_NOTE_CROSS_CHECKED),
    ("f-catalog-only", "claude-cli", 0.009, "price_table", 3, 0.009, None, False, "2026-10-01",
     VALUATION_NOTE_PRICE_TABLE),
    ("g-unmeasured", "claude-cli", None, "unknown", None, None, None, False, "2026-10-01",
     VALUATION_NOTE_UNMEASURED),
    ("h-foreign", "claude-cli", None, "unknown", None, None, None, False, "2026-10-01", FOREIGN),
    ("i-ambiguous", None, None, "unknown", None, None, None, False, None, VALUATION_NOTE_AMBIGUOUS),
    ("j-no-model", None, None, "unknown", None, None, None, False, None, VALUATION_NOTE_NO_MODEL),
    ("k-provider-zero", "claude-cli", 0.0, "provider_reported", 3, 0.007, None, True, "2026-10-01",
     VALUATION_NOTE_CROSS_CHECKED),
    ("l-unlisted-unpriced", None, None, "unknown", None, None, None, False, None,
     VALUATION_NOTE_NO_PRICE),
    ("m-cost-not-reported", "claude-cli", 0.007, "price_table", 3, 0.007, None, False,
     "2026-10-01", VALUATION_NOTE_PRICE_TABLE),
]


def _golden(v: CallValuation) -> tuple:
    return (v.call_id, v.adapter, v.normalized_cost, v.basis, v.pricing_version, v.catalog_cost,
            v.deviation_percent, v.cross_check_exceeded, v.price_valid_from, v.note)


class TestTheBasisRules:
    def test_mixed_bases_match_their_goldens_exactly(self) -> None:
        got = [_golden(value_ledger_call(r, CATALOGS)) for r in RECORDS]
        assert got == GOLDENS

    def test_every_valuation_is_in_the_configured_currency(self) -> None:
        assert {value_ledger_call(r, CATALOGS).currency for r in RECORDS} == {"usd"}

    def test_the_threshold_is_configurable_and_strict(self) -> None:
        beyond = RECORDS[4]
        assert value_ledger_call(beyond, CATALOGS, threshold_percent=6.0).cross_check_exceeded is False
        assert value_ledger_call(beyond, CATALOGS, threshold_percent=5.999).cross_check_exceeded is True

    def test_the_cost_the_provider_reported_wins_even_far_from_the_catalog(self) -> None:
        v = value_ledger_call(_call("x", "m-usd", cost=1.0, tokens=(1000, 500, 0, 0)), CATALOGS)
        assert (v.normalized_cost, v.basis, v.cross_check_exceeded) == (1.0, "provider_reported", True)

    def test_no_catalog_at_all_leaves_an_unreported_cost_unknown(self) -> None:
        v = value_ledger_call(RECORDS[5], {})
        assert (v.normalized_cost, v.basis, v.note) == (None, "unknown", VALUATION_NOTE_NO_PRICE)


class TestTheTable:
    def test_valuations_round_trip_and_a_second_valuation_replaces_the_first(self, tmp_path) -> None:
        path = tmp_path / "ledger.sqlite"
        valuations = [value_ledger_call(r, CATALOGS) for r in RECORDS]
        assert record_call_valuations(valuations, path=path) == len(RECORDS)
        assert record_call_valuations(valuations[:2], path=path) == 2
        assert query_call_valuations(path=path) == sorted(valuations, key=lambda v: v.call_id)

    def test_the_table_carries_its_own_schema_key(self, tmp_path) -> None:
        path = tmp_path / "ledger.sqlite"
        record_call_valuations([], path=path)
        conn = open_ledger(path)
        try:
            row = conn.execute("SELECT value FROM meta WHERE key = ?",
                               (CALL_VALUATIONS_SCHEMA_KEY,)).fetchone()
        finally:
            conn.close()
        assert row[0] == "1"

    def test_the_table_refuses_a_basis_outside_the_ledgers_vocabulary(self, tmp_path) -> None:
        path = tmp_path / "ledger.sqlite"
        bad = value_ledger_call(RECORDS[0], CATALOGS)
        bad = CallValuation(**{**bad.__dict__, "basis": "catalog_computed"})
        with pytest.raises(sqlite3.IntegrityError):
            record_call_valuations([bad], path=path)

    def test_valuing_calls_never_touches_their_calls_rows(self, tmp_path) -> None:
        path = tmp_path / "ledger.sqlite"
        for record in RECORDS:
            assert record_call(record, path=path) is True

        def calls_digest() -> str:
            conn = open_ledger(path)
            try:
                rows = conn.execute("SELECT * FROM calls ORDER BY call_id").fetchall()
            finally:
                conn.close()
            return hashlib.sha256(repr(rows).encode()).hexdigest()

        before = calls_digest()
        value_and_record_calls(RECORDS, path=path, catalogs=CATALOGS, config={})
        assert calls_digest() == before
        assert len(query_call_valuations(path=path)) == len(RECORDS)


class TestTheConfiguration:
    def test_unset_keys_read_as_usd_and_five_percent(self) -> None:
        assert configured_valuation_settings({}) == ("usd", 5.0)

    def test_a_configured_threshold_is_used(self) -> None:
        assert configured_valuation_settings({"cost.cross_check_threshold_percent": 10}) == ("usd", 10.0)

    def test_a_refused_currency_refuses_the_valuation(self) -> None:
        with pytest.raises(CostCurrencyError):
            configured_valuation_settings({"cost.currency": "eur"})

    def test_a_mismatch_beyond_the_threshold_is_logged_as_a_warning(self, tmp_path, caplog) -> None:
        with caplog.at_level(logging.WARNING, logger="packages.orchestration.call_valuation"):
            value_and_record_calls([RECORDS[4]], path=tmp_path / "l.sqlite", catalogs=CATALOGS, config={})
        assert [r for r in caplog.records if r.getMessage().startswith("price cross-check: call e-beyond")]

    def test_a_mismatch_within_the_threshold_logs_nothing(self, tmp_path, caplog) -> None:
        with caplog.at_level(logging.WARNING, logger="packages.orchestration.call_valuation"):
            value_and_record_calls([RECORDS[2]], path=tmp_path / "l.sqlite", catalogs=CATALOGS, config={})
        assert not [r for r in caplog.records if "price cross-check" in r.getMessage()]


class TestTheLiveHook:
    """The evidence bundle's ledger hook values the call it mirrors, beside its row."""

    def test_the_hook_writes_a_valuation_for_the_mirrored_call(self, tmp_path) -> None:
        from packages.orchestration.pingpong_evidence import write_evidence_bundle

        job, task = "job-f158", "T001"
        ledger = tmp_path / "ledger.sqlite"
        bundle = {
            "manifest": {"run_id": "run-1"},
            "summary_md": "# run\n",
            "tests": "ok\n",
            "token_accounting": {"role": "builder"},
            "provider_evidence": {
                "schema_version": "1.0.0", "task_id": task, "execution_mode": "provider_backed",
                "provider_call_count": 1, "actual_call_count": 1, "cost_call_count": 1,
                "actual_prompt_tokens": 11, "actual_completion_tokens": 5, "actual_total_tokens": 16,
                "total_cost_usd": 0.02, "ts_utc": "2026-10-24T11:00:00+00:00",
            },
        }
        write_evidence_bundle(bundle, str(tmp_path / "evidence" / job / "task_runs" / task),
                              ledger_path=str(ledger), ledger_job_id=job, ledger_task_id=task)
        [valuation] = query_call_valuations(path=ledger)
        assert valuation.call_id == f"{job}:{task}"
        assert (valuation.normalized_cost, valuation.basis, valuation.currency) == (
            0.02, "provider_reported", "usd")
        conn = open_ledger(ledger)
        try:
            tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        finally:
            conn.close()
        assert CALL_VALUATIONS_TABLE in tables
