"""The price catalog (F158 T002, DECISION F158 D4): the format, every refusal, the warnings and the
shipped catalogs."""

from __future__ import annotations

import datetime
from pathlib import Path

import pytest

from packages.orchestration.model_aliases import builtin_model_ids
from packages.orchestration.price_catalog import (
    PRICE_CATALOG_DIR,
    PRICE_CATALOG_MODEL_FIELDS,
    PriceCatalogError,
    load_price_catalog,
    load_price_catalogs,
    parse_price_catalog,
    price_catalog_warnings,
    registered_adapter_refs,
)

KNOWN_MODEL = builtin_model_ids()[0]

VALID = f"""
[catalog]
adapter = "claude-cli"
pricing_version = 3

[models."zz-model"]
input_per_million = 2
output_per_million = 10.5
cache_read_per_million = 0
cache_write_per_million = 2.5
currency = "usd"
valid_from = 2026-10-01
source = "docs/pricing-notes.md:12"

[models."{KNOWN_MODEL}"]
input_per_million = 3.0
output_per_million = 15.0
cache_read_per_million = 0.3
cache_write_per_million = 3.75
currency = "usd"
valid_from = 2026-09-01
source = "https://example.invalid/pricing"
"""


def _with(old: str, new: str) -> str:
    assert VALID.count(old) >= 1, old
    return VALID.replace(old, new, 1)


class TestTheFormat:
    def test_a_valid_catalog_parses_with_its_prices_sorted_by_model(self) -> None:
        catalog = parse_price_catalog(VALID, adapter="claude-cli")
        assert catalog.adapter == "claude-cli"
        assert catalog.pricing_version == 3
        assert [p.model for p in catalog.prices] == sorted([KNOWN_MODEL, "zz-model"])
        zz = catalog.price_for("zz-model")
        assert zz is not None
        assert (zz.input_per_million, zz.output_per_million, zz.cache_read_per_million,
                zz.cache_write_per_million) == (2.0, 10.5, 0.0, 2.5)
        assert isinstance(zz.input_per_million, float)
        assert zz.currency == "usd"
        assert zz.valid_from == datetime.date(2026, 10, 1)
        assert zz.source == "docs/pricing-notes.md:12"

    def test_an_unlisted_model_has_no_price(self) -> None:
        assert parse_price_catalog(VALID, adapter="claude-cli").price_for("other") is None

    def test_a_catalog_may_list_no_model(self) -> None:
        text = '[catalog]\nadapter = "claude-cli"\npricing_version = 1\n\n[models]\n'
        assert parse_price_catalog(text, adapter="claude-cli").prices == ()

    def test_the_model_fields_are_the_four_prices_the_currency_the_date_and_the_source(self) -> None:
        assert PRICE_CATALOG_MODEL_FIELDS == (
            "input_per_million", "output_per_million", "cache_read_per_million",
            "cache_write_per_million", "currency", "valid_from", "source")


REFUSALS = [
    ("not toml", "[catalog\n", "not valid TOML"),
    ("unknown top table", VALID + "\n[extra]\nx = 1\n", "the file must hold exactly catalog, models"),
    ("no models table", '[catalog]\nadapter = "claude-cli"\npricing_version = 1\n',
     "the file must hold exactly catalog, models"),
    ("adapter not the file's", _with('adapter = "claude-cli"', 'adapter = "other"'),
     "[catalog] adapter 'other' must equal the file's adapter 'claude-cli'"),
    ("extra catalog key", _with("pricing_version = 3", "pricing_version = 3\nnote = 1"),
     "[catalog] must hold exactly adapter, pricing_version"),
    ("version zero", _with("pricing_version = 3", "pricing_version = 0"),
     "pricing_version must be a whole number of 1 or more"),
    ("version boolean", _with("pricing_version = 3", "pricing_version = true"),
     "pricing_version must be a whole number of 1 or more"),
    ("version text", _with("pricing_version = 3", 'pricing_version = "3"'),
     "pricing_version must be a whole number of 1 or more"),
    ("missing price", _with("cache_write_per_million = 2.5\n", ""),
     "model 'zz-model' must hold exactly"),
    ("extra model key", _with('source = "docs/pricing-notes.md:12"',
                              'source = "docs/pricing-notes.md:12"\nnote = "x"'),
     "unexpected ['note']"),
    ("negative cache price", _with("cache_read_per_million = 0", "cache_read_per_million = -1"),
     "model 'zz-model' cache_read_per_million must be zero or more"),
    ("zero input price", _with("input_per_million = 2", "input_per_million = 0"),
     "model 'zz-model' input_per_million must be greater than zero"),
    ("zero output price", _with("output_per_million = 10.5", "output_per_million = 0"),
     "model 'zz-model' output_per_million must be greater than zero"),
    ("infinite price", _with("input_per_million = 2", "input_per_million = inf"),
     "model 'zz-model' input_per_million must be a finite number"),
    ("boolean price", _with("input_per_million = 2", "input_per_million = true"),
     "model 'zz-model' input_per_million must be a finite number"),
    ("text price", _with("input_per_million = 2", 'input_per_million = "2"'),
     "model 'zz-model' input_per_million must be a finite number"),
    ("upper-case currency", _with('currency = "usd"', 'currency = "USD"'),
     "model 'zz-model' currency must be a lower-case ISO 4217 code"),
    ("long currency", _with('currency = "usd"', 'currency = "dollar"'),
     "model 'zz-model' currency must be a lower-case ISO 4217 code"),
    ("date as text", _with("valid_from = 2026-10-01", 'valid_from = "2026-10-01"'),
     "model 'zz-model' valid_from must be a TOML date"),
    ("date and time", _with("valid_from = 2026-10-01", "valid_from = 2026-10-01T00:00:00"),
     "model 'zz-model' valid_from must be a TOML date"),
    ("blank source", _with('source = "docs/pricing-notes.md:12"', 'source = "  "'),
     "model 'zz-model' source must name where its prices were read"),
    ("model id with a space", _with('[models."zz-model"]', '[models."zz model"]'),
     "model id 'zz model' must be non-empty text without spaces"),
]


class TestEveryRefusal:
    @pytest.mark.parametrize("name,text,reason", REFUSALS, ids=[r[0] for r in REFUSALS])
    def test_a_malformed_catalog_is_refused_whole_naming_the_adapter_and_the_reason(
            self, name, text, reason) -> None:
        with pytest.raises(PriceCatalogError) as caught:
            parse_price_catalog(text, adapter="claude-cli")
        message = str(caught.value)
        assert message.startswith("claude-cli price catalog: ")
        assert reason in message

    def test_an_adapter_the_registry_does_not_name_is_refused(self) -> None:
        text = _with('adapter = "claude-cli"', 'adapter = "no-such-adapter"')
        with pytest.raises(PriceCatalogError, match="is not an adapter_ref the worker registry names"):
            parse_price_catalog(text, adapter="no-such-adapter")

    def test_the_refusal_is_a_value_error(self) -> None:
        assert issubclass(PriceCatalogError, ValueError)


class TestTheWarnings:
    def test_a_known_usd_model_draws_no_warning(self) -> None:
        catalog = parse_price_catalog(VALID, adapter="claude-cli")
        assert [w for w in price_catalog_warnings(catalog) if repr(KNOWN_MODEL) in w] == []

    def test_an_unknown_model_id_is_named(self) -> None:
        catalog = parse_price_catalog(VALID, adapter="claude-cli")
        assert price_catalog_warnings(catalog) == [
            "claude-cli price catalog: model 'zz-model' is not one of Remedy's built-in model ids; "
            "check its spelling"]

    def test_a_price_in_another_currency_stays_unnormalized_and_says_so(self) -> None:
        catalog = parse_price_catalog(_with('currency = "usd"\nvalid_from = 2026-09-01',
                                            'currency = "eur"\nvalid_from = 2026-09-01'),
                                      adapter="claude-cli")
        warnings = price_catalog_warnings(catalog)
        assert (f"claude-cli price catalog: model {KNOWN_MODEL!r} is priced in eur, not usd; with "
                "no exchange rate configured, and none invented, its cost stays unnormalized"
                ) in warnings


class TestTheShippedCatalogs:
    def test_every_shipped_catalog_is_named_after_a_registered_adapter_and_loads(self) -> None:
        catalogs = load_price_catalogs()
        assert set(catalogs) == {p.stem for p in PRICE_CATALOG_DIR.glob("*.toml")}
        assert set(catalogs) <= registered_adapter_refs()

    def test_the_claude_cli_catalog_lists_no_price_until_one_with_a_source_is_imported(self) -> None:
        catalog = load_price_catalog("claude-cli")
        assert catalog is not None
        assert catalog.pricing_version == 1
        assert catalog.prices == ()

    def test_an_adapter_without_a_catalog_file_has_none(self, tmp_path: Path) -> None:
        assert load_price_catalog("claude-cli", tmp_path) is None
        assert load_price_catalogs(tmp_path) == {}

    def test_a_catalog_directory_is_read_whole(self, tmp_path: Path) -> None:
        (tmp_path / "claude-cli.toml").write_text(VALID, encoding="utf-8")
        assert load_price_catalogs(tmp_path)["claude-cli"].pricing_version == 3
