"""F114 T002 — tests for the shared cost-preview confirmation helper.

Covers `render_estimate_line` / `confirm_cost_preview` in
`apps.cli.cost_preview_confirm`, reusing the tty-mocking shape
`tests/cli/test_loop_cmd.py` already established for
`loop_cmd._stdin_is_a_tty` / `builtins.input`.
"""
from __future__ import annotations

import pytest

from apps.cli import cost_preview_confirm as cpc
from packages.orchestration.cost_preview import CostBandEstimate

AVAILABLE = CostBandEstimate(0.16, 2.40, "class defaults (low/high) x price=0.02", {})
UNAVAILABLE = CostBandEstimate(None, None, "estimate_unavailable", {})


class TestRenderEstimateLine:
    def test_available_estimate_shows_the_band_and_basis(self):
        line = cpc.render_estimate_line(AVAILABLE)
        assert "$0.1600" in line
        assert "$2.4000" in line
        assert "class defaults (low/high) x price=0.02" in line

    def test_unavailable_estimate_says_so_and_still_carries_a_basis(self):
        line = cpc.render_estimate_line(UNAVAILABLE)
        assert "unavailable" in line
        assert "estimate_unavailable" in line


class TestUnderThreshold:
    def test_under_threshold_proceeds_without_any_prompt(self, capsys):
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=10.0, yes=False, command_name="do")
        assert result is True
        assert "estimated" in capsys.readouterr().out

    def test_under_threshold_never_touches_stdin(self, monkeypatch, capsys):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: (_ for _ in ()).throw(
            AssertionError("must not be called when under threshold")))
        cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=10.0, yes=False, command_name="do")


class TestOverThresholdWithYes:
    def test_yes_skips_the_prompt_and_proceeds(self, capsys):
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=True, command_name="do")
        assert result is True
        out = capsys.readouterr().out
        assert "--yes" in out

    def test_yes_never_touches_stdin(self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: (_ for _ in ()).throw(
            AssertionError("must not be called when --yes")))
        cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=True, command_name="do")


class TestOverThresholdNonTty:
    def test_non_tty_exits_with_usage_code_never_hangs(self, monkeypatch, capsys):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: False)
        with pytest.raises(SystemExit) as exc:
            cpc.confirm_cost_preview(
                AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do")
        assert exc.value.code == cpc.EXIT_USAGE
        assert exc.value.code != 0
        err = capsys.readouterr().err
        assert "--yes" in err
        assert "do" in err

    def test_non_tty_never_calls_input(self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: False)
        monkeypatch.setattr("builtins.input", lambda prompt="": (_ for _ in ()).throw(
            AssertionError("must not prompt on non-tty")))
        with pytest.raises(SystemExit):
            cpc.confirm_cost_preview(
                AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do")


class TestOverThresholdTty:
    def test_tty_answering_yes_proceeds(self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda prompt="": "y")
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do")
        assert result is True

    def test_tty_declining_returns_false_without_raising(self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda prompt="": "n")
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do")
        assert result is False


class TestUnavailableIsTreatedAsExpensive:
    def test_unavailable_estimate_requires_confirmation_even_at_a_huge_threshold(
            self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: False)
        with pytest.raises(SystemExit) as exc:
            cpc.confirm_cost_preview(
                UNAVAILABLE, confirm_above_usd=999999.0, yes=False, command_name="do")
        assert exc.value.code == cpc.EXIT_USAGE

    def test_unavailable_estimate_with_yes_still_proceeds(self):
        result = cpc.confirm_cost_preview(
            UNAVAILABLE, confirm_above_usd=999999.0, yes=True, command_name="do")
        assert result is True
