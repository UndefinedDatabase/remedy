"""The one currency every cost figure in Remedy is stated in (F158 T001, DECISION F158 D3).

Remedy speaks one money language. Every budget field it ships is a USD field — `budget.max_cost_usd`,
the two profile cost limits, `cost_preview.confirm_above_usd`, `budget.price_basis_usd_per_1k_tokens`,
the ledger's `cost_usd` column — so the `cost.currency` key that budgets, previews, the ledger and
the price catalog share accepts exactly `usd` today. Another value is refused by name rather than
silently read as dollars, because a budget written in one currency and compared against costs in
another is a wrong answer that looks right.

Remedy deliberately does not convert between currencies here: a foreign-currency price is converted
only through an explicitly configured rate, or left unnormalized with a note (T002), and no exchange
rate is ever invented.

Remedy deliberately does not show a dollar figure unless `cost.show_usd` is true (operator
amendment amend1024-one-real-order Part E): the operator judges a run by its tokens and provider
calls. `show_cost_usd` reads the key; `visible_cost_usd` is the one rule every JSON answer of
`remedy stats`, `remedy job show`, `remedy do` and the HTTP API applies — with the key false every
field named `*_usd` keeps its key and reads null, except a limit the operator set (`max_*_usd`,
`cap_usd`, `confirm_above_usd`) and the `show_cost_usd` flag itself — and a text output prints
`COST_USD_HIDDEN_LABEL` or `COST_USD_HIDDEN_NOTE` where a dollar figure would stand.

`foreign_currency_markers` is the mixed-currency guard's scanner: it reads a Python source's string
literals and names every currency symbol or code other than the dollar, so a display that prints a
second currency is caught by `tests/orchestration/test_cost_currency.py` before it ships.
"""

from __future__ import annotations

import ast
import re
from collections.abc import Mapping
from typing import Any

#: The registry key every cost-stating surface reads its currency from.
COST_CURRENCY_KEY = "cost.currency"

#: The default, and today the only accepted value: every budget field is a USD field.
COST_CURRENCY_USD = "usd"

#: The closed set of accepted currencies, lower-case ISO 4217 codes.
COST_CURRENCIES = frozenset({COST_CURRENCY_USD})

#: Currency symbols and upper-case ISO 4217 codes a display must not print beside dollar figures.
FOREIGN_CURRENCY_SYMBOLS = ("€", "£", "¥", "₹", "₩", "₽", "₣")
FOREIGN_CURRENCY_CODES = ("AUD", "CAD", "CHF", "CNY", "EUR", "GBP", "INR", "JPY", "KRW", "SEK")

_FOREIGN_CODE_RE = re.compile(r"\b(" + "|".join(FOREIGN_CURRENCY_CODES) + r")\b")


#: The registry key that shows dollar figures; false by default (amend1024 Part E).
COST_SHOW_USD_KEY = "cost.show_usd"

#: What a text cell prints where a dollar figure would stand while `cost.show_usd` is false.
COST_USD_HIDDEN_LABEL = "not-shown"

#: The sentence a text output adds when it left its dollar figures out.
COST_USD_HIDDEN_NOTE = ("Dollar figures are not shown: tokens and provider calls only (set "
                        "cost.show_usd = true in remedy.toml to show them).")

#: Field-name prefixes of a `*_usd` field that is a limit or a flag, never a measured cost.
_COST_USD_KEPT_PREFIXES = ("max_", "cap_", "confirm_above_", "show_")


class CostCurrencyError(ValueError):
    """A `cost.currency` value Remedy does not accept."""


def resolve_cost_currency(value: object) -> str:
    """The accepted currency `value` names; unset or blank means `usd`.

    Raises `CostCurrencyError` for a value outside `COST_CURRENCIES`, naming the key, the accepted
    set and the reason, so the refusal tells an operator what to write instead.
    """
    if value is None:
        return COST_CURRENCY_USD
    if not isinstance(value, str):
        raise CostCurrencyError(
            f"{COST_CURRENCY_KEY} must be text naming a currency, got {type(value).__name__}")
    text = value.strip().lower()
    if not text:
        return COST_CURRENCY_USD
    if text not in COST_CURRENCIES:
        accepted = ", ".join(sorted(COST_CURRENCIES))
        raise CostCurrencyError(
            f"{COST_CURRENCY_KEY} {value!r} is not accepted: Remedy states every cost in usd, "
            f"because every budget field (max_cost_usd, the profile cost limits and "
            f"confirm_above_usd) is a USD field; accepted: {accepted}")
    return text


def cost_currency_problems(config: Mapping[str, object] | object) -> list[str]:
    """The `cost.currency` refusal for `config` as warning lines; empty when it resolves.

    `config` is anything with a `get(key)` method, such as a `RemedyConfig`.
    """
    try:
        resolve_cost_currency(config.get(COST_CURRENCY_KEY))  # type: ignore[union-attr]
    except CostCurrencyError as exc:
        return [str(exc)]
    return []


# The one reader of `cost.show_usd`: every surface that could print dollars asks it.
def show_cost_usd() -> bool:
    """True only when `cost.show_usd` resolves to true; a config that cannot be read hides them."""
    from packages.orchestration.config import get_config

    try:
        return get_config().get(COST_SHOW_USD_KEY) is True
    except (OSError, ValueError):
        # A remedy.toml that cannot be read fails the command that needs it; here it hides money.
        return False


def is_cost_usd_field(name: str) -> bool:
    """True for a field holding a measured or derived dollar figure: `*_usd` and not a limit."""
    return name.endswith("_usd") and not name.startswith(_COST_USD_KEPT_PREFIXES)


def hide_cost_usd_fields(value: Any) -> Any:
    """A copy of the JSON value `value` in which every `is_cost_usd_field` reads None."""
    if isinstance(value, dict):
        return {key: None if isinstance(key, str) and is_cost_usd_field(key)
                else hide_cost_usd_fields(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [hide_cost_usd_fields(item) for item in value]
    return value


def visible_cost_usd(document: Any) -> Any:
    """`document` itself when `show_cost_usd()`, else `hide_cost_usd_fields(document)`."""
    return document if show_cost_usd() else hide_cost_usd_fields(document)


def foreign_currency_markers(source: str) -> list[tuple[int, str]]:
    """Every foreign currency symbol or code in `source`'s string literals, as (line, marker).

    Only string literals are read, f-string parts included, so a comment or an identifier that
    happens to spell a code is not a display. A code counts as a whole upper-case word.
    """
    found: list[tuple[int, str]] = []
    for node in ast.walk(ast.parse(source)):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for symbol in FOREIGN_CURRENCY_SYMBOLS:
            if symbol in node.value:
                found.append((node.lineno, symbol))
        found.extend((node.lineno, match) for match in _FOREIGN_CODE_RE.findall(node.value))
    return sorted(found)
