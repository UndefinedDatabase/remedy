"""amend1015 P5.2, amend1024 Part E: `remedy do` shows dollars only when `cost.show_usd` is true."""
from __future__ import annotations

from packages.orchestration.config import reset_config
from packages.orchestration.do_context import DoContext
from packages.orchestration.do_summary import do_cost_summary_lines, do_json_document

_SUMMARY = {"roles": [{"role": "builder", "harness_invocations": 2, "model_turns": None,
                       "tokens_in": 1200, "tokens_out": 300, "cache_read": None, "cost_usd": 0.0018}],
            "cost_usd": 0.0018, "job_ids": ["j"], "mirror_failed_job_ids": [], "mirror_errors": {}}


def test_the_default_prints_no_dollar_figure():
    text = "\n".join(do_cost_summary_lines(_SUMMARY))
    assert "$" not in text
    assert "Cost: not shown — tokens only" in text
    # amend1024 Part E: the line names the remedy.toml key that replaced `[cockpit] show_cost_usd`.
    assert "set cost.show_usd = true in remedy.toml" in text
    assert "[cockpit]" not in text


def test_the_opt_in_prints_the_measured_dollars():
    text = "\n".join(do_cost_summary_lines(_SUMMARY, show_cost_usd=True))
    assert "Cost: $0.001800 (measured, from the ledger)" in text


def test_an_unreported_cost_reads_the_same_either_way():
    summary = {**_SUMMARY, "cost_usd": None}
    assert "Cost: not reported by the provider" in do_cost_summary_lines(summary)


def test_the_json_document_nulls_every_dollar_field_unless_the_key_is_true(monkeypatch):
    """amend1024 Part E: the `--json` answer keeps its keys; a dollar field reads null by default."""
    cost = {**_SUMMARY, "show_cost_usd": False}
    hidden = do_json_document(DoContext(order="o"), jobs=[], cost=cost, contract=None)["cost"]
    assert set(hidden) == set(cost)
    assert hidden["cost_usd"] is None
    assert [role["cost_usd"] for role in hidden["roles"]] == [None]
    assert hidden["roles"][0]["tokens_in"] == 1200
    assert hidden["show_cost_usd"] is False

    monkeypatch.setenv("REMEDY_COST_SHOW_USD", "true")
    reset_config()
    shown = do_json_document(DoContext(order="o"), jobs=[], cost=cost, contract=None)["cost"]
    assert shown == cost
