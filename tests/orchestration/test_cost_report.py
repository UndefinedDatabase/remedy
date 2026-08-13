"""F115 T002 — the cost report renderer: determinism is the property under test.

``cost_report.py`` is a PURE FUNCTION over the two report dataclasses, so every
PROPERTY pair below is built BY HAND from ``CostReport`` / ``CostRow`` /
``SegmentShareReport`` / ``SegmentShareRow``. Those tests read no ledger, open
no fixture tree and start no clock: what they pin is that the same pair of
reports renders to the same bytes, twice and on any machine.

The GOLDEN section at the bottom is the other half of that proof and works the
other way round: it builds a real evidence tree, runs the REAL
``backfill_ledger`` over it, asks the REAL queries for the pair, and compares
the rendered bytes against two files committed on disk. Nothing regenerates
those files — a golden a test re-blesses on mismatch checks nothing.

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
    so in words instead of printing 0.0%;
  * a prior period renders as SIGNED changes, a change across an unmeasured
    side is the word and never a number, and a prior window that was read and
    held nothing says exactly that instead of printing a table of zeros;
  * a prior that is not THIS period's prior — a stray window, or one from
    another ledger — is refused by both renderers;
  * the bytes of both reports over a real backfilled ledger are the bytes of
    the two golden files, and those files state the numbers that ledger holds.
"""
from __future__ import annotations

import json
from pathlib import Path

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
    backfill_ledger,
    prior_report_period,
    query_cost,
    query_segment_shares,
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


def _prior(*, total=None, **kwargs) -> CostReport:
    """The report of the window immediately BEFORE ``_cost``'s period.

    Its ``until`` is ``_cost``'s ``since`` and its ledger is the same one, which
    is exactly what ``_same_question``'s third guard demands of a comparison.
    """
    defaults = dict(
        by="model",
        since="2026-07-31",
        until="2026-08-01",
        job_id="job-abc",
        project_id=PROJECT_ID,
        ledger_path=LEDGER_PATH,
        ledger_exists=True,
    )
    defaults.update(kwargs)
    return CostReport(
        rows=[],
        total=total if total is not None else _prior_total(),
        **defaults,
    )


def _prior_total() -> CostRow:
    return CostRow(
        bucket=None,
        calls=2,
        tokens_in=1000,
        tokens_out=400,
        cache_read=None,
        cache_write=None,
        cost_usd=0.5,
        measured_calls=2,
        unmeasured_calls=0,
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


def test_a_pair_covering_two_different_periods_is_refused_by_both_renderers():
    """A period's END is a filter like any other, so two ends are two questions."""
    cost = _cost(until="2026-08-09")
    shares = _shares(until="2026-08-12")

    with pytest.raises(ValueError):
        render_cost_report_markdown(cost, shares, label="R15")
    with pytest.raises(ValueError):
        cost_report_json_bytes(cost, shares, label="R15")


def test_both_renderings_carry_the_until_the_report_holds():
    """The second end of the period is stated, not silently applied."""
    markdown = render_cost_report_markdown(
        _cost(until="2026-08-09"), _shares(until="2026-08-09"), label="R15"
    )
    assert "until=2026-08-09" in markdown

    payload = cost_report_json(
        _cost(until="2026-08-09"), _shares(until="2026-08-09"), label="R15"
    )
    assert payload["filters"]["until"] == "2026-08-09"

    # An OPEN-ENDED period says so in both formats rather than printing a date
    # nobody asked for: the dash in markdown, the empty string in json.
    assert "until=-" in render_cost_report_markdown(_cost(), _shares(), label="R15")
    assert cost_report_json(_cost(), _shares(), label="R15")["filters"]["until"] == ""


def test_a_pair_from_two_different_ledgers_is_refused_by_both_renderers():
    """Identical filters over two different ledgers are still two questions."""
    cost = _cost(ledger_path="/data/a/ledger.sqlite")
    shares = _shares(ledger_path="/data/b/ledger.sqlite")

    with pytest.raises(ValueError):
        render_cost_report_markdown(cost, shares, label="R12")
    with pytest.raises(ValueError):
        cost_report_json_bytes(cost, shares, label="R12")


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


def test_a_comparison_renders_in_both_formats():
    cost, shares, prior = _cost(), _shares(), _prior()

    markdown = render_cost_report_markdown(cost, shares, label="R16", prior=prior)
    assert "## Compared to the previous period" in markdown
    assert "| tokens in | 1200 | 1000 | +200 |" in markdown
    assert "| tokens out | 300 | 400 | -100 |" in markdown
    assert "| cost usd | 0.1250 | 0.5000 | -0.3750 |" in markdown
    assert "| calls | 3 | 2 | +1 |" in markdown
    assert (
        "Previous period: since=2026-07-31  until=2026-08-01 · 2 call(s)."
        in markdown
    )
    # The signed difference is the whole change: no percentage is printed.
    assert "%" not in markdown.split("## Compared to the previous period")[1]

    comparison = cost_report_json(cost, shares, label="R16", prior=prior)["comparison"]
    assert comparison["available"] is True
    assert comparison["reason"] == ""
    assert comparison["prior"]["since"] == "2026-07-31"
    assert comparison["prior"]["until"] == "2026-08-01"
    assert comparison["prior"]["total"]["calls"] == 2
    assert comparison["deltas"]["tokens_in"] == 200
    assert comparison["deltas"]["tokens_out"] == -100
    assert comparison["deltas"]["calls"] == 1
    assert comparison["deltas"]["cost_usd"] == pytest.approx(-0.375)


def test_a_change_cell_is_unmeasured_when_either_side_is_none():
    """No arithmetic across an absence: a missing side is never read as a zero."""
    prior = _prior(
        total=CostRow(calls=2, tokens_in=1000, tokens_out=None, cost_usd=None,
                      measured_calls=1, unmeasured_calls=1)
    )
    markdown = render_cost_report_markdown(_cost(), _shares(), label="R16", prior=prior)

    # This period measured 300; the previous one measured nothing there, so the
    # change is unknown rather than the whole of this period's figure.
    assert "| tokens out | 300 | unmeasured | unmeasured |" in markdown
    assert "| cache read | unmeasured | unmeasured | unmeasured |" in markdown
    assert "| cost usd | 0.1250 | unmeasured | unmeasured |" in markdown

    deltas = cost_report_json(
        _cost(), _shares(), label="R16", prior=prior
    )["comparison"]["deltas"]
    assert deltas["tokens_out"] is None
    assert deltas["cache_read"] is None
    assert deltas["cost_usd"] is None
    assert deltas["tokens_in"] == 200


def test_an_empty_prior_window_says_so_rather_than_printing_zeros():
    """The P6 split: "we looked and found nothing" is not "it cost nothing"."""
    empty = _prior(total=CostRow(calls=0))
    markdown = render_cost_report_markdown(_cost(), _shares(), label="R16", prior=empty)

    section = markdown.split("## Compared to the previous period")[1]
    assert "The previous period was read and holds no call at all" in section
    assert "|" not in section, "an empty window is not a table of zeros"
    assert " 0 " not in section

    comparison = cost_report_json(
        _cost(), _shares(), label="R16", prior=empty
    )["comparison"]
    assert comparison["available"] is False
    assert comparison["prior"] is None
    assert set(comparison["deltas"].values()) == {None}

    # Contrast: nobody looked at all, which is a different fact and says so.
    unread = render_cost_report_markdown(_cost(), _shares(), label="R16")
    assert "No previous period was read" in unread


def test_a_prior_that_is_not_this_periods_prior_is_refused_by_both_renderers():
    """A comparison's baseline must ABUT this period; any other window is a lie."""
    stray = _prior(since="2026-07-01", until="2026-07-08")

    with pytest.raises(ValueError):
        render_cost_report_markdown(_cost(), _shares(), label="R16", prior=stray)
    with pytest.raises(ValueError):
        cost_report_json_bytes(_cost(), _shares(), label="R16", prior=stray)


def test_a_prior_from_a_different_ledger_is_refused_by_both_renderers():
    """One ledger per question — a prior included."""
    other = _prior(ledger_path="/data/b/ledger.sqlite")

    with pytest.raises(ValueError):
        render_cost_report_markdown(_cost(), _shares(), label="R16", prior=other)
    with pytest.raises(ValueError):
        cost_report_json_bytes(_cost(), _shares(), label="R16", prior=other)


def test_the_json_and_the_markdown_agree_on_the_segment_total():
    cost, shares = _cost(), _shares()
    payload = json.loads(cost_report_json_bytes(cost, shares, label="R11"))
    assert payload["segments"]["total_tokens_estimated"] == 230

    markdown = render_cost_report_markdown(cost, shares, label="R11")
    total_row = [
        line for line in markdown.splitlines() if line.startswith("| TOTAL |")
    ][-1]
    assert "| 230 |" in total_row


# ── The golden pair, over a ledger the REAL backfill wrote ──────────────────
#
# The fixture is built HERE rather than imported from ``test_token_ledger.py``:
# a golden whose input a reader cannot see in the same file is a golden that
# gets re-blessed instead of argued with. Everything below writes real evidence
# files, hands them to the real ``backfill_ledger`` and asks the real queries —
# no row is hand-inserted with SQL, so a writer that stopped producing these
# rows would fail these tests rather than pass them.

GOLDEN_DIR = Path(__file__).parent / "fixtures" / "cost_report" / "golden"
GOLDEN_LABEL = "f115-golden"
GOLDEN_MARKDOWN_NAME = "cost_report.md"
GOLDEN_JSON_NAME = "cost_report.json"


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _manifest_entry(name, rank, sha256, chars, tokens_estimated):
    """One ``ComposedPrompt.manifest_as_dicts()`` row, key for key."""
    return {
        "name": name,
        "rank": rank,
        "sha256": sha256,
        "chars": chars,
        "tokens_estimated": tokens_estimated,
    }


def _trace_entry(job_id, task_id, manifest):
    """One prompt-trace object in the shape ``prompt_trace.py`` writes on disk."""
    return {
        "run_id": "run-golden",
        "job_id": job_id,
        "task_id": task_id,
        "round": 1,
        "role": "builder",
        "provider": "fake",
        "prompt_kind": "initial",
        "prompt_sha256": "0" * 64,
        "prompt_chars": 1234,
        "prompt_tokens_estimated": 308,
        "segment_manifest": list(manifest),
        "segment_manifest_chars": sum(m["chars"] for m in manifest),
        "created_at": "2026-08-08T09:00:00+00:00",
    }


def _evidence_tree(root, job_id, runs):
    """A job-evidence tree in the shape the exporter writes it.

    Each run is ``(task_id, ts_utc, manifest, extra)``: ``manifest`` None means
    the pre-F115 shape, a call whose prompt was never traced, and ``extra``
    carries whatever usage the provider reported beyond the base counters.
    """
    _write_json(
        root / "manifest.json", {"bundle_type": "job_evidence", "job_id": job_id}
    )
    for task_id, ts_utc, manifest, extra in runs:
        run = root / "task_runs" / task_id
        evidence = {
            "schema_version": "1.0.0",
            "task_id": task_id,
            "execution_mode": "provider_backed",
            "provider_call_count": 1,
            "actual_call_count": 1,
            "cost_call_count": 1,
            "actual_prompt_tokens": 1000,
            "actual_completion_tokens": 200,
            "ts_utc": ts_utc,
        }
        evidence.update(extra)
        _write_json(run / "provider_evidence.json", evidence)
        _write_json(run / "token_accounting.json", {"role": "builder"})
        if manifest is not None:
            (run / "prompt_trace.jsonl").write_text(
                json.dumps(_trace_entry(job_id, task_id, manifest)) + "\n",
                encoding="utf-8",
            )
    return root


@pytest.fixture
def golden_ledger(tmp_path):
    """Four calls over three days: two traced, two not, one of them measured.

    ``diff`` and ``schema_tail`` publish the SAME ``tokens_estimated`` on
    purpose, so the goldens pin the tie-break of the row order and not only its
    direction. Only the last call reports cost and cache figures, so the total
    is PARTLY measured and the report has to say so in words.
    """
    brief = _manifest_entry("task_brief", 10, "a" * 64, 120, 30)
    diff = _manifest_entry("diff", 20, "b" * 64, 400, 100)
    tail = _manifest_entry("schema_tail", 30, "c" * 64, 60, 100)

    traced = _evidence_tree(
        tmp_path / "evidence" / "job-traced",
        "job-traced",
        [
            ("T001", "2026-08-01T10:00:00+00:00", [brief, diff], {}),
            ("T002", "2026-08-05T10:00:00+00:00", [tail], {}),
        ],
    )
    bare = _evidence_tree(
        tmp_path / "evidence" / "job-bare",
        "job-bare",
        [
            ("T001", "2026-08-09T10:00:00+00:00", None, {}),
            (
                "T002",
                "2026-08-09T11:00:00+00:00",
                None,
                {
                    "total_cost_usd": 0.25,
                    "actual_cache_read_tokens": 64,
                    "actual_cache_creation_tokens": 32,
                    "actual_model_verified": True,
                    "builder_actual_model": "claude-opus-5",
                },
            ),
        ],
    )
    ledger = tmp_path / "ledger.sqlite"
    assert backfill_ledger(traced, path=ledger).recorded == 2
    assert backfill_ledger(bare, path=ledger).recorded == 2
    return ledger


def _golden_pair(ledger):
    """The pair the goldens were rendered from: the day buckets and the shares."""
    return query_cost(path=ledger, by="day"), query_segment_shares(path=ledger)


def _golden_no_comparison_reason(cost):
    """The REAL sentence for the golden's period, from the code that produces it.

    The golden pair covers an OPEN-ENDED period, so it exercises the first
    unavailable case of ``prior_report_period``. Asking that function for the
    sentence is what makes the golden pin the real text; a paraphrase typed in
    here would pin the paraphrase and let the real one drift away from it.
    """
    return prior_report_period(cost.since, cost.until).unavailable_reason


def test_the_golden_markdown_matches_the_fixture_ledger(golden_ledger):
    """A golden re-blessed on every change checks nothing, so this one never is."""
    cost, shares = _golden_pair(golden_ledger)
    rendered = render_cost_report_markdown(
        cost,
        shares,
        label=GOLDEN_LABEL,
        no_comparison_reason=_golden_no_comparison_reason(cost),
    )
    assert rendered == (GOLDEN_DIR / GOLDEN_MARKDOWN_NAME).read_text(encoding="utf-8")


def test_the_golden_json_matches_the_fixture_ledger(golden_ledger):
    """A golden re-blessed on every change checks nothing, so this one never is."""
    cost, shares = _golden_pair(golden_ledger)
    rendered = cost_report_json_bytes(
        cost,
        shares,
        label=GOLDEN_LABEL,
        no_comparison_reason=_golden_no_comparison_reason(cost),
    )
    assert rendered == (GOLDEN_DIR / GOLDEN_JSON_NAME).read_text(encoding="utf-8")


def test_the_golden_files_state_the_numbers_the_ledger_holds():
    """The FILES, not the renderer: this is what stops a golden being a snapshot."""
    payload = json.loads((GOLDEN_DIR / GOLDEN_JSON_NAME).read_text(encoding="utf-8"))
    total = payload["total"]
    assert total["calls"] == 4
    assert total["tokens_in"] == 4000
    assert total["tokens_out"] == 800
    assert total["cache_read"] == 64
    assert total["cache_write"] == 32
    assert total["cost_usd"] == 0.25
    assert total["measured_calls"] == 1
    assert total["unmeasured_calls"] == 3
    assert [row["bucket"] for row in payload["buckets"]] == [
        "2026-08-01",
        "2026-08-05",
        "2026-08-09",
    ]
    segments = payload["segments"]
    assert [row["segment_name"] for row in segments["rows"]] == [
        "diff",
        "schema_tail",
        "task_brief",
    ]
    assert segments["total_tokens_estimated"] == 230
    assert segments["attributed_calls"] == 2
    assert segments["unattributed_calls"] == 2

    markdown = (GOLDEN_DIR / GOLDEN_MARKDOWN_NAME).read_text(encoding="utf-8")
    for stated in ("PARTLY UNMEASURED", "unmeasured", "0.2500", "43.5%", "13.0%"):
        assert stated in markdown


def test_the_golden_json_agrees_with_the_golden_markdown():
    """Two files, one set of facts — a drift between them is a defect in both."""
    payload = json.loads((GOLDEN_DIR / GOLDEN_JSON_NAME).read_text(encoding="utf-8"))
    markdown = (GOLDEN_DIR / GOLDEN_MARKDOWN_NAME).read_text(encoding="utf-8")

    for row in payload["segments"]["rows"]:
        assert row["segment_name"] in markdown
    assert f"| {payload['segments']['total_tokens_estimated']} |" in markdown
