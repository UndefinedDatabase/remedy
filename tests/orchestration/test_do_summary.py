"""amend1015 P5.2: the `Cost:` line of `remedy do` shows dollars only when the project asks."""
from __future__ import annotations

from packages.orchestration.do_summary import do_cost_summary_lines

_SUMMARY = {"roles": [{"role": "builder", "harness_invocations": 2, "model_turns": None,
                       "tokens_in": 1200, "tokens_out": 300, "cache_read": None, "cost_usd": 0.0018}],
            "cost_usd": 0.0018, "job_ids": ["j"], "mirror_failed_job_ids": [], "mirror_errors": {}}


def test_the_default_prints_no_dollar_figure():
    text = "\n".join(do_cost_summary_lines(_SUMMARY))
    assert "$" not in text
    assert "Cost: not shown — tokens only" in text


def test_the_opt_in_prints_the_measured_dollars():
    text = "\n".join(do_cost_summary_lines(_SUMMARY, show_cost_usd=True))
    assert "Cost: $0.001800 (measured, from the ledger)" in text


def test_an_unreported_cost_reads_the_same_either_way():
    summary = {**_SUMMARY, "cost_usd": None}
    assert "Cost: not reported by the provider" in do_cost_summary_lines(summary)
