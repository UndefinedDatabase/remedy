"""F115 T002 — the cost report renderer: determinism is the property under test.

``cost_report.py`` is a PURE FUNCTION over the two report dataclasses, so every
pair below is built BY HAND from ``CostReport`` / ``CostRow`` /
``SegmentShareReport`` / ``SegmentShareRow``. This module reads no ledger, opens
no fixture tree and starts no clock: what it pins is that the same pair of
reports renders to the same bytes, twice and on any machine.

What it proves, one property per test:

  * markdown and json are byte-identical across two renders of one pair;
  * an UNMEASURED figure prints the word and never a 0, and stays ``null`` in
    the json — the P6 rule, carried through the renderer;
  * neither rendering leaks the ledger path or the registry UUID, the two
    machine-specific strings that would make a golden comparison decay into a
    re-blessing ritual;
  * a pair whose two halves answer different questions is REFUSED by both
    renderers rather than published side by side;
  * a ledger that does not exist renders as an absence, not as a table of
    zeros;
  * an unattributed call — one whose prompt was never traced — is counted once
    and given no share of any segment kind;
  * every share is a share of the attributed total, and an empty breakdown says
    so in words instead of printing 0.0%.
"""
from __future__ import annotations

import json

import pytest

from packages.orchestration.cost_report import (
    cost_report_json,
    cost_report_json_bytes,
    render_cost_report_markdown,
)
from packages.orchestration.token_ledger import (
    CostReport,
    CostRow,
    SegmentShareReport,
    SegmentShareRow,
)

LEDGER_PATH = "/tmp/machine-specific/ledger.sqlite"
PROJECT_ID = "11111111-2222-3333-4444-555555555555"


def _cost(*, rows=None, total=None, **kwargs) -> CostReport:
    """A cost report with the machine-specific fields always populated."""
    defaults = dict(
        by="model",
        since="2026-08-01",
        job_id="job-abc",
        project_id=PROJECT_ID,
        ledger_path=LEDGER_PATH,
        ledger_exists=True,
    )
    defaults.update(kwargs)
    return CostReport(
        rows=rows if rows is not None else _default_rows(),
        total=total if total is not None else _default_total(),
        **defaults,
    )


def _default_rows() -> list[CostRow]:
    return [
        CostRow(
            bucket="claude-opus",
            calls=2,
            tokens_in=1200,
            tokens_out=300,
            cache_read=None,
            cache_write=None,
            cost_usd=0.125,
            measured_calls=2,
            unmeasured_calls=0,
        ),
        CostRow(
            bucket=None,
            calls=1,
            tokens_in=None,
            tokens_out=None,
            cache_read=None,
            cache_write=None,
            cost_usd=None,
            measured_calls=0,
            unmeasured_calls=1,
        ),
    ]


def _default_total() -> CostRow:
    return CostRow(
        bucket=None,
        calls=3,
        tokens_in=1200,
        tokens_out=300,
        cache_read=None,
        cache_write=None,
        cost_usd=0.125,
        measured_calls=2,
        unmeasured_calls=1,
    )


def _shares(*, rows=None, **kwargs) -> SegmentShareReport:
    """A segment-share report over the same question as ``_cost``."""
    defaults = dict(
        attributed_calls=2,
        unattributed_calls=1,
        total_segments=4,
        total_chars=920,
        total_tokens_estimated=230,
        since="2026-08-01",
        job_id="job-abc",
        project_id=PROJECT_ID,
        ledger_path=LEDGER_PATH,
        ledger_exists=True,
    )
    defaults.update(kwargs)
    return SegmentShareReport(
        rows=rows if rows is not None else _default_share_rows(),
        **defaults,
    )


def _default_share_rows() -> list[SegmentShareRow]:
    return [
        SegmentShareRow("diff", calls=2, segments=2, chars=400, tokens_estimated=100),
        SegmentShareRow("task_brief", calls=1, segments=1, chars=460, tokens_estimated=100),
        SegmentShareRow("schema_tail", calls=1, segments=1, chars=60, tokens_estimated=30),
    ]


def test_markdown_bytes_are_identical_across_two_renders():
    cost, shares = _cost(), _shares()
    first = render_cost_report_markdown(cost, shares, label="F115 R11")
    second = render_cost_report_markdown(cost, shares, label="F115 R11")
    assert first == second
    # A second pair built from the same values, not the same objects, renders
    # the same bytes too — determinism over VALUES, not over identity.
    assert render_cost_report_markdown(_cost(), _shares(), label="F115 R11") == first


def test_json_bytes_are_identical_across_two_renders():
    cost, shares = _cost(), _shares()
    first = cost_report_json_bytes(cost, shares, label="F115 R11")
    second = cost_report_json_bytes(cost, shares, label="F115 R11")
    assert first == second
    assert cost_report_json_bytes(_cost(), _shares(), label="F115 R11") == first


def test_an_unmeasured_figure_prints_the_word_and_never_a_zero():
    # Every call reported its basis, so no "PARTLY UNMEASURED" sentence fires:
    # the word below can only have come from the figure cells themselves.
    total = CostRow(
        calls=2,
        tokens_in=1200,
        tokens_out=300,
        cache_read=None,
        cache_write=400,
        cost_usd=None,
        measured_calls=2,
        unmeasured_calls=0,
    )
    cost = _cost(rows=[], total=total)
    shares = _shares()

    markdown = render_cost_report_markdown(cost, shares, label="R11")
    assert "unmeasured" in markdown

    payload = cost_report_json(cost, shares, label="R11")
    assert payload["total"]["cost_usd"] is None
    assert payload["total"]["cache_read"] is None


def test_neither_rendering_carries_the_ledger_path_or_the_project_id():
    cost, shares = _cost(), _shares()
    markdown = render_cost_report_markdown(cost, shares, label="R11")
    payload = cost_report_json_bytes(cost, shares, label="R11")

    for machine_specific in (LEDGER_PATH, PROJECT_ID):
        assert machine_specific not in markdown
        assert machine_specific not in payload


def test_a_mismatched_pair_is_refused_by_both_renderers():
    cost = _cost(since="2026-08-01")
    shares = _shares(since="2026-08-05")

    with pytest.raises(ValueError):
        render_cost_report_markdown(cost, shares, label="R11")
    with pytest.raises(ValueError):
        cost_report_json_bytes(cost, shares, label="R11")


def test_a_missing_ledger_renders_the_absence_and_no_table():
    cost = _cost(ledger_exists=False)
    shares = _shares(ledger_exists=False)

    markdown = render_cost_report_markdown(cost, shares, label="R11")
    assert "No ledger on disk for this scope" in markdown
    assert not [line for line in markdown.splitlines() if line.startswith("|")]

    payload = cost_report_json(cost, shares, label="R11")
    assert payload["ledger_exists"] is False


def test_an_unattributed_call_is_counted_and_given_no_share():
    cost = _cost()
    shares = _shares(attributed_calls=2, unattributed_calls=1)

    markdown = render_cost_report_markdown(cost, shares, label="R11")
    assert "Attribution: 2 call(s) carry a segment manifest, 1 do not." in markdown

    payload = cost_report_json(cost, shares, label="R11")
    assert payload["segments"]["unattributed_calls"] == 1
    # The unattributed call owns no row: the rows account for attributed calls.
    assert [row["segment_name"] for row in payload["segments"]["rows"]] == [
        "diff",
        "task_brief",
        "schema_tail",
    ]


def test_the_share_column_uses_the_attributed_total_as_its_denominator():
    markdown = render_cost_report_markdown(_cost(), _shares(), label="R11")

    assert markdown.count("43.5%") == 2  # 100 of 230, twice
    assert markdown.count("13.0%") == 1  # 30 of 230
    total_row = [
        line for line in markdown.splitlines() if line.startswith("| TOTAL |")
    ][-1]
    assert total_row.endswith("| 100.0% |")


def test_an_empty_share_report_says_absence_rather_than_zero_percent():
    shares = _shares(
        rows=[],
        attributed_calls=0,
        unattributed_calls=3,
        total_segments=0,
        total_chars=0,
        total_tokens_estimated=0,
    )
    markdown = render_cost_report_markdown(_cost(), shares, label="R11")

    assert "nothing to break down" in markdown
    assert "0.0%" not in markdown


def test_the_json_and_the_markdown_agree_on_the_segment_total():
    cost, shares = _cost(), _shares()
    payload = json.loads(cost_report_json_bytes(cost, shares, label="R11"))
    assert payload["segments"]["total_tokens_estimated"] == 230

    markdown = render_cost_report_markdown(cost, shares, label="R11")
    total_row = [
        line for line in markdown.splitlines() if line.startswith("| TOTAL |")
    ][-1]
    assert "| 230 |" in total_row
