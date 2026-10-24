"""The versioned price catalog of each worker adapter (F158 T002, DECISION F158 D4).

One TOML file per adapter under `price_catalog_files/`, named after the adapter's `adapter_ref`
(`packages/orchestration/worker_adapters.py`): a `[catalog]` table with the adapter and its
`pricing_version`, and one `[models."<id>"]` table per priced model with four prices per million
tokens, the currency, the date the prices are valid from and the source they were read from.

Remedy deliberately ships no price it cannot cite: a price enters a catalog only with a source a
reviewer can open, so a model a catalog does not list stays unpriced and its cost unknown, never a
plausible invention. A catalog file is refused whole on any malformed entry — a half-read price
list would price some calls and silently skip others. Advisory doubts that do not make a catalog
wrong (a model id Remedy does not ship, a price in a currency other than the configured one) are
`price_catalog_warnings`, never refusals.
"""

from __future__ import annotations

import datetime
import math
import re
from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10: the declared backport (amend1015c D1)
    import tomli as tomllib

from packages.orchestration.cost_currency import COST_CURRENCY_USD
from packages.orchestration.model_aliases import builtin_model_ids
from packages.orchestration.worker_adapters import list_worker_specs

#: Where the shipped catalogs live, one `<adapter_ref>.toml` each.
PRICE_CATALOG_DIR = Path(__file__).resolve().parent / "price_catalog_files"

#: The four prices of a model, each in its currency per million tokens.
PRICE_CATALOG_PRICE_FIELDS = (
    "input_per_million",
    "output_per_million",
    "cache_read_per_million",
    "cache_write_per_million",
)

#: Every key a model's table must carry, and no other.
PRICE_CATALOG_MODEL_FIELDS = (*PRICE_CATALOG_PRICE_FIELDS, "currency", "valid_from", "source")

_CURRENCY_CODE_RE = re.compile(r"[a-z]{3}")


class PriceCatalogError(ValueError):
    """A price catalog file Remedy refuses to read."""


@dataclass(frozen=True)
class ModelPrice:
    """One model's prices in one catalog, per million tokens in `currency`."""

    model: str
    input_per_million: float
    output_per_million: float
    cache_read_per_million: float
    cache_write_per_million: float
    currency: str
    valid_from: datetime.date
    source: str


@dataclass(frozen=True)
class PriceCatalog:
    """An adapter's catalog: its pricing version and its model prices, sorted by model id."""

    adapter: str
    pricing_version: int
    prices: tuple[ModelPrice, ...]

    def price_for(self, model: str) -> ModelPrice | None:
        """The price of `model`, or None when this catalog does not list it."""
        for price in self.prices:
            if price.model == model:
                return price
        return None


def registered_adapter_refs() -> frozenset[str]:
    """Every non-empty `adapter_ref` the worker registry names: the adapters a catalog may price."""
    return frozenset(spec.adapter_ref for spec in list_worker_specs() if spec.adapter_ref)


def _refuse(adapter: str, reason: str) -> PriceCatalogError:
    return PriceCatalogError(f"{adapter} price catalog: {reason}")


def _keys_exactly(adapter: str, where: str, table: object, expected: tuple[str, ...]) -> dict:
    if not isinstance(table, dict):
        raise _refuse(adapter, f"{where} must be a table")
    missing = [k for k in expected if k not in table]
    extra = sorted(k for k in table if k not in expected)
    if missing or extra:
        raise _refuse(adapter, f"{where} must hold exactly {', '.join(expected)}; "
                               f"missing {missing}, unexpected {extra}")
    return table


def _price_value(adapter: str, model: str, field: str, value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise _refuse(adapter, f"model {model!r} {field} must be a finite number")
    # A model may have no cache, so a cache price may be zero; a call is never free to send.
    floor_ok = value >= 0 if field.startswith("cache_") else value > 0
    if not floor_ok:
        bound = "zero or more" if field.startswith("cache_") else "greater than zero"
        raise _refuse(adapter, f"model {model!r} {field} must be {bound}")
    return float(value)


def _model_price(adapter: str, model: object, table: object) -> ModelPrice:
    if not isinstance(model, str) or not model or model != model.strip() or " " in model:
        raise _refuse(adapter, f"model id {model!r} must be non-empty text without spaces")
    entry = _keys_exactly(adapter, f"model {model!r}", table, PRICE_CATALOG_MODEL_FIELDS)
    prices = {f: _price_value(adapter, model, f, entry[f]) for f in PRICE_CATALOG_PRICE_FIELDS}
    currency = entry["currency"]
    if not isinstance(currency, str) or not _CURRENCY_CODE_RE.fullmatch(currency):
        raise _refuse(adapter, f"model {model!r} currency must be a lower-case ISO 4217 code")
    valid_from = entry["valid_from"]
    if isinstance(valid_from, datetime.datetime) or not isinstance(valid_from, datetime.date):
        raise _refuse(adapter, f"model {model!r} valid_from must be a TOML date such as 2026-10-01")
    source = entry["source"]
    if not isinstance(source, str) or not source.strip():
        raise _refuse(adapter, f"model {model!r} source must name where its prices were read")
    return ModelPrice(model=model, currency=currency, valid_from=valid_from, source=source, **prices)


def parse_price_catalog(text: str, *, adapter: str) -> PriceCatalog:
    """Parse one catalog file's text for `adapter`, refusing it whole on any malformed entry."""
    try:
        parsed = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise _refuse(adapter, f"not valid TOML: {exc}") from exc
    top = _keys_exactly(adapter, "the file", parsed, ("catalog", "models"))
    header = _keys_exactly(adapter, "[catalog]", top["catalog"], ("adapter", "pricing_version"))
    if header["adapter"] != adapter:
        raise _refuse(adapter, f"[catalog] adapter {header['adapter']!r} must equal the file's "
                               f"adapter {adapter!r}")
    if adapter not in registered_adapter_refs():
        raise _refuse(adapter, f"{adapter!r} is not an adapter_ref the worker registry names; "
                               f"registered: {', '.join(sorted(registered_adapter_refs()))}")
    version = header["pricing_version"]
    if isinstance(version, bool) or not isinstance(version, int) or version < 1:
        raise _refuse(adapter, "[catalog] pricing_version must be a whole number of 1 or more")
    models = top["models"]
    if not isinstance(models, dict):
        raise _refuse(adapter, "[models] must be a table")
    prices = tuple(sorted((_model_price(adapter, m, t) for m, t in models.items()),
                          key=lambda p: p.model))
    return PriceCatalog(adapter=adapter, pricing_version=version, prices=prices)


def load_price_catalog(adapter: str, directory: Path | None = None) -> PriceCatalog | None:
    """The catalog of `adapter` from `directory` (the shipped one by default), or None if absent."""
    path = (directory or PRICE_CATALOG_DIR) / f"{adapter}.toml"
    if not path.is_file():
        return None
    return parse_price_catalog(path.read_text(encoding="utf-8"), adapter=adapter)


def load_price_catalogs(directory: Path | None = None) -> dict[str, PriceCatalog]:
    """Every catalog in `directory` (the shipped one by default), keyed by adapter."""
    base = directory or PRICE_CATALOG_DIR
    return {path.stem: parse_price_catalog(path.read_text(encoding="utf-8"), adapter=path.stem)
            for path in sorted(base.glob("*.toml"))}


def price_catalog_warnings(catalog: PriceCatalog, *, currency: str = COST_CURRENCY_USD) -> list[str]:
    """Advisory doubts about a valid catalog: unknown model ids and prices in another currency."""
    known = set(builtin_model_ids())
    warnings: list[str] = []
    for price in catalog.prices:
        if price.model not in known:
            warnings.append(f"{catalog.adapter} price catalog: model {price.model!r} is not one of "
                            f"Remedy's built-in model ids; check its spelling")
        if price.currency != currency:
            warnings.append(f"{catalog.adapter} price catalog: model {price.model!r} is priced in "
                            f"{price.currency}, not {currency}; with no exchange rate configured, "
                            f"and none invented, its cost stays unnormalized")
    return warnings
