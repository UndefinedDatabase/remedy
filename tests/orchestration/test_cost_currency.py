"""The one currency (F158 T001, DECISION F158 D3): the key, its refusal, the audit page and the
mixed-currency guard over every production source."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.config import all_key_specs, get_key_spec
from packages.orchestration.cost_currency import (
    COST_CURRENCIES,
    COST_CURRENCY_KEY,
    COST_CURRENCY_USD,
    CostCurrencyError,
    cost_currency_problems,
    foreign_currency_markers,
    resolve_cost_currency,
)

REPO = Path(__file__).resolve().parents[2]
AUDIT_PAGE = REPO / "docs" / "system" / "cost-currency-v1.md"

#: The one production file allowed to spell foreign markers: the guard's own table of them.
GUARD_TABLE_FILE = "packages/orchestration/cost_currency.py"


class TestTheKeyAndItsRefusal:
    def test_the_key_is_registered_with_usd_as_its_default(self) -> None:
        spec = get_key_spec(COST_CURRENCY_KEY)
        assert spec is not None
        assert spec.env_var == "REMEDY_COST_CURRENCY"
        assert spec.value_type is str
        assert spec.default == COST_CURRENCY_USD == "usd"

    def test_usd_is_the_only_accepted_currency(self) -> None:
        assert COST_CURRENCIES == frozenset({"usd"})

    @pytest.mark.parametrize("value", [None, "", "  ", "usd", "USD", " Usd "])
    def test_unset_blank_and_any_spelling_of_usd_resolve_to_usd(self, value) -> None:
        assert resolve_cost_currency(value) == "usd"

    @pytest.mark.parametrize("value", ["eur", "EUR", "gbp", "dollars"])
    def test_another_currency_is_refused_naming_the_key_the_accepted_set_and_the_reason(
            self, value) -> None:
        with pytest.raises(CostCurrencyError) as caught:
            resolve_cost_currency(value)
        message = str(caught.value)
        assert message.startswith(f"cost.currency {value!r} is not accepted")
        assert "max_cost_usd" in message
        assert message.endswith("accepted: usd")

    def test_a_value_that_is_not_text_is_refused(self) -> None:
        with pytest.raises(CostCurrencyError, match="must be text naming a currency, got int"):
            resolve_cost_currency(3)

    def test_the_refusal_is_a_value_error(self) -> None:
        assert issubclass(CostCurrencyError, ValueError)

    def test_problems_are_empty_for_usd_and_name_the_refusal_otherwise(self) -> None:
        assert cost_currency_problems({COST_CURRENCY_KEY: "usd"}) == []
        assert cost_currency_problems({}) == []
        problems = cost_currency_problems({COST_CURRENCY_KEY: "eur"})
        assert len(problems) == 1 and problems[0].startswith("cost.currency 'eur' is not accepted")


@pytest.mark.subprocess
class TestConfigValidateReadsTheKey:
    """The user's path: `remedy config validate` names a refused currency and says invalid."""

    def _validate(self, tmp_path: Path, currency: str | None) -> dict:
        env = {k: v for k, v in os.environ.items() if k != "REMEDY_COST_CURRENCY"}
        env["PYTHONPATH"] = str(REPO)
        if currency is not None:
            env["REMEDY_COST_CURRENCY"] = currency
        r = subprocess.run([sys.executable, "-m", "apps.cli.grouped", "config", "validate", "--json"],
                           capture_output=True, text=True, timeout=60, cwd=tmp_path, env=env)
        assert r.returncode == 0, r.stderr
        return json.loads(r.stdout)

    def test_a_refused_currency_makes_the_config_invalid_and_is_named(self, tmp_path: Path) -> None:
        body = self._validate(tmp_path, "eur")
        assert body["valid"] is False
        assert [w for w in body["warnings"] if w.startswith("cost.currency 'eur' is not accepted")]

    def test_usd_adds_no_warning(self, tmp_path: Path) -> None:
        body = self._validate(tmp_path, "usd")
        assert not [w for w in body["warnings"] if w.startswith("cost.currency")]


class TestTheMixedCurrencyGuard:
    def test_the_scanner_finds_symbols_and_whole_codes_in_string_literals(self) -> None:
        source = 'a = "€3.00"\nb = f"{x} EUR"\nc = "£"\nd = "1 CHF and 2 JPY"\n'
        assert foreign_currency_markers(source) == [
            (1, "€"), (2, "EUR"), (3, "£"), (4, "CHF"), (4, "JPY")]

    def test_the_scanner_ignores_comments_identifiers_and_partial_words(self) -> None:
        source = '# priced in EUR\nEUR_RATE = 1\nx = "EUROPE eur Eur"\n'
        assert foreign_currency_markers(source) == []

    def test_no_production_source_prints_a_foreign_currency(self) -> None:
        offenders: list[str] = []
        for root in ("packages", "apps"):
            for path in sorted((REPO / root).rglob("*.py")):
                rel = path.relative_to(REPO).as_posix()
                if rel == GUARD_TABLE_FILE or "__pycache__" in path.parts:
                    continue
                for line, marker in foreign_currency_markers(path.read_text(encoding="utf-8")):
                    offenders.append(f"{rel}:{line} {marker}")
        assert offenders == []

    def test_the_only_exempt_file_is_the_guard_table_and_it_does_spell_markers(self) -> None:
        markers = foreign_currency_markers((REPO / GUARD_TABLE_FILE).read_text(encoding="utf-8"))
        assert {m for _, m in markers} >= {"€", "EUR"}


class TestTheAuditPage:
    def _table_keys(self) -> set[str]:
        """The first-column keys of the page's "Configuration keys" table, and of no other."""
        text = AUDIT_PAGE.read_text(encoding="utf-8")
        section = text.split("## Configuration keys\n", 1)[1].split("\n## ", 1)[0]
        return set(re.findall(r"^\| `([a-z0-9_.]+)` \|", section, re.M))

    def test_every_registered_usd_key_is_in_the_audit_table(self) -> None:
        usd_keys = {s.key for s in all_key_specs() if s.key.endswith("_usd")
                    or "_usd_" in s.key}
        assert usd_keys, "the registry holds USD keys"
        assert usd_keys <= self._table_keys()

    def test_the_currency_key_itself_is_in_the_audit_table(self) -> None:
        assert COST_CURRENCY_KEY in self._table_keys()

    def test_every_key_row_of_the_table_is_registered(self) -> None:
        registered = {s.key for s in all_key_specs()}
        assert self._table_keys() <= registered
