"""F115 T002 — the cost report: where the tokens went, in two formats.

``query_cost`` answers "what did this period cost" and ``query_segment_shares``
answers "where did its prompt tokens go". This module is the PURE FUNCTION that
turns that PAIR into something a human or a UI can read: markdown for people,
json for the later UI section. It queries nothing, opens nothing, and computes
no price.

**The bytes are deterministic for a given pair of reports.** No clock, no
absolute path, no registry UUID, no dict-iteration order. That is why neither
``ledger_path`` nor ``project_id`` is rendered even though both reports carry
them: the first is a ``tmp_path`` under test and a data-root path in
production, the second is a UUID minted per machine, so either one would make
the same ledger render differently on two machines and a golden comparison
would decay into a re-blessing ritual. Provenance travels as ``label``, which
the caller states — the same choice ``gauntlet_matrix.py`` made for its
evidence directory, and for the same reason.

**Two absences, two words, and neither is a zero.** A figure nobody reported is
UNMEASURED — ``CostRow``'s nulls exist to carry it, and P6 forbids printing a 0
in its place. A call whose prompt was never traced is UNATTRIBUTED: it is
counted once, by name, and given no share of any segment kind.

Remedy deliberately does not compute a missing price here, and deliberately
does not fill an unattributed call's segments by re-splitting its prompt after
the fact: both would turn "we do not know" into a number a reader cannot tell
apart from a measurement.
"""
from __future__ import annotations

import json
from typing import Any

from packages.orchestration.token_ledger import (
    CostReport,
    CostRow,
    SegmentShareReport,
)

#: Report schema version. Bumped when the payload shape changes, so a reader
#: never has to guess which shape it is holding.
COST_REPORT_VERSION = 1

#: The report file names, written side by side when T003 puts them on disk.
COST_REPORT_MARKDOWN_FILENAME = "cost_report.md"
COST_REPORT_JSON_FILENAME = "cost_report.json"

#: What a figure nobody reported prints as. ``stats_ledger_cmd.UNMEASURED`` is
#: the same word for the same thing; T003 makes that module import this one so
#: the concept keeps ONE spelling (AGENTS.md, Code Discoverability).
COST_UNMEASURED_LABEL = "unmeasured"

#: What a bucket whose group column is NULL prints as — a call whose role the
#: evidence never named. The spelling the ledger CLI already prints.
COST_UNNAMED_BUCKET_LABEL = "(unnamed)"

#: What the header says when the caller named no scope.
COST_DEFAULT_LABEL = "(unlabelled)"

#: The cost table's figure columns, in render order.
COST_FIGURE_COLUMNS = (
    ("tokens_in", "tokens in"),
    ("tokens_out", "tokens out"),
    ("cache_read", "cache read"),
    ("cache_write", "cache write"),
    ("cost_usd", "cost usd"),
)

#: The share table's columns, in render order.
SHARE_TABLE_HEADER = ("segment", "calls", "segments", "chars", "tokens est.", "share")


def _figure(value: int | float | None) -> str:
    """One measurement, or the word — a 0 never stands in for nobody-reported."""
    if value is None:
        return COST_UNMEASURED_LABEL
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def _share_percent(part: int, whole: int) -> str:
    """A share of the attributed total, or a dash when there is no denominator."""
    if whole <= 0:
        return "-"
    return f"{100.0 * part / whole:.1f}%"


def _same_question(cost: CostReport, shares: SegmentShareReport) -> None:
    """Refuse a pair that answers two different questions.

    Both queries take the same ``since`` and ``job_id`` and run them through the
    same ``_cost_filters`` clause, so a MATCHED pair describes one set of calls
    by construction. An unmatched pair does not, and rendering it would publish
    the breakdown of one period beside the total of another — silently
    answering a different question than the one asked, which ``query_cost``
    already refuses to do for its own ``by`` argument.
    """
    if (cost.since, cost.job_id) != (shares.since, shares.job_id):
        raise ValueError(
            "a cost report needs one question, not two: "
            f"query_cost(since={cost.since!r}, job_id={cost.job_id!r}) does not "
            f"match query_segment_shares(since={shares.since!r}, "
            f"job_id={shares.job_id!r})"
        )


def _cost_row_payload(row: CostRow) -> dict[str, Any]:
    """One bucket as json: every figure as a number or null, never coerced."""
    return {
        "bucket": row.bucket,
        "calls": row.calls,
        "tokens_in": row.tokens_in,
        "tokens_out": row.tokens_out,
        "cache_read": row.cache_read,
        "cache_write": row.cache_write,
        "cost_usd": row.cost_usd,
        "measured_calls": row.measured_calls,
        "unmeasured_calls": row.unmeasured_calls,
        "fully_measured": row.fully_measured,
    }


def cost_report_json(
    cost: CostReport,
    shares: SegmentShareReport,
    *,
    label: str | None = None,
) -> dict[str, Any]:
    """The machine-readable report. Deterministic for a given pair of reports."""
    _same_question(cost, shares)
    return {
        "report_version": COST_REPORT_VERSION,
        "label": label if label is not None else COST_DEFAULT_LABEL,
        "filters": {
            "since": cost.since or "",
            "job": cost.job_id or "",
            "by": cost.by,
            "timezone": "UTC",
        },
        "ledger_exists": cost.ledger_exists,
        "unmeasured_notation": "null",
        "note": (
            "a null figure was never reported — it is not a zero; "
            "no price is ever computed"
        ),
        "total": _cost_row_payload(cost.total),
        "buckets": [_cost_row_payload(row) for row in cost.rows],
        "segments": {
            "attributed_calls": shares.attributed_calls,
            "unattributed_calls": shares.unattributed_calls,
            "total_segments": shares.total_segments,
            "total_chars": shares.total_chars,
            "total_tokens_estimated": shares.total_tokens_estimated,
            "rows": [
                {
                    "segment_name": row.segment_name,
                    "calls": row.calls,
                    "segments": row.segments,
                    "chars": row.chars,
                    "tokens_estimated": row.tokens_estimated,
                }
                for row in shares.rows
            ],
        },
    }


def cost_report_json_bytes(
    cost: CostReport,
    shares: SegmentShareReport,
    *,
    label: str | None = None,
) -> str:
    """The json report as the exact text a caller writes to disk."""
    return json.dumps(
        cost_report_json(cost, shares, label=label),
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    ) + "\n"


def _table(header: tuple[str, ...], rows: list[tuple[str, ...]]) -> list[str]:
    """A markdown table. The twin of ``gauntlet_matrix._table``, kept local so
    a report module never depends on the campaign gate."""
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return lines


def _cost_section(cost: CostReport) -> list[str]:
    total = cost.total
    header = ("bucket", "calls", *(label for _, label in COST_FIGURE_COLUMNS), "basis")
    rows = [
        (
            row.bucket if row.bucket is not None else COST_UNNAMED_BUCKET_LABEL,
            str(row.calls),
            *(_figure(getattr(row, name)) for name, _ in COST_FIGURE_COLUMNS),
            f"{row.measured_calls}/{row.calls} measured",
        )
        for row in cost.rows
    ]
    rows.append(
        (
            "TOTAL",
            str(total.calls),
            *(_figure(getattr(total, name)) for name, _ in COST_FIGURE_COLUMNS),
            f"{total.measured_calls}/{total.calls} measured",
        )
    )
    lines = ["## Cost", ""]
    lines += _table(header, rows)
    lines.append("")
    # In words, because a partial total that LOOKS complete is the exact mistake
    # this feature exists to prevent.
    if total.calls and total.measured_calls == 0:
        lines.append(
            f"FULLY UNMEASURED: not one of these {total.calls} call(s) reported "
            "usage or cost. Every figure above is unknown, not zero."
        )
    elif total.calls and not total.fully_measured:
        lines.append(
            f"PARTLY UNMEASURED: these figures cover only the "
            f"{total.measured_calls} call(s) whose provider reported them; the "
            f"{total.unmeasured_calls} unmeasured call(s) contribute nothing to "
            "any figure above."
        )
    lines.append(
        "No price is computed: a cost appears only where a provider reported one."
    )
    lines.append("")
    return lines


def _segment_section(shares: SegmentShareReport) -> list[str]:
    lines = ["## Where the tokens went", ""]
    if not shares.rows:
        lines.append(
            "No call in this period carries a segment manifest, so there is "
            "nothing to break down. That is an absence, not a set of zero shares."
        )
    else:
        whole = shares.total_tokens_estimated
        rows = [
            (
                row.segment_name,
                str(row.calls),
                str(row.segments),
                str(row.chars),
                str(row.tokens_estimated),
                _share_percent(row.tokens_estimated, whole),
            )
            for row in shares.rows
        ]
        # The TOTAL row's calls cell is a dash on purpose: one call can own
        # several segment kinds, so a column of per-kind call counts does not
        # add up to a number of calls and printing a sum would invent one.
        rows.append(
            (
                "TOTAL",
                "-",
                str(shares.total_segments),
                str(shares.total_chars),
                str(shares.total_tokens_estimated),
                _share_percent(whole, whole),
            )
        )
        lines += _table(SHARE_TABLE_HEADER, rows)
    lines.append("")
    lines.append(
        f"Attribution: {shares.attributed_calls} call(s) carry a segment "
        f"manifest, {shares.unattributed_calls} do not. An unattributed call is "
        "one whose prompt was never traced; it is counted here and given no "
        "share of any segment kind."
    )
    lines.append("")
    return lines


def render_cost_report_markdown(
    cost: CostReport,
    shares: SegmentShareReport,
    *,
    label: str | None = None,
) -> str:
    """The human-readable report. Same facts as the json, same bytes twice."""
    _same_question(cost, shares)
    name = label if label is not None else COST_DEFAULT_LABEL
    lines = [f"# Cost report — {name}", ""]
    filters = "  ".join(
        f"{key}={value}"
        for key, value in (
            ("since", cost.since or "-"),
            ("job", cost.job_id or "-"),
            ("by", cost.by or "-"),
        )
    )
    lines.append(f"Filters: {filters} · all timestamps UTC")
    lines.append("")
    # A ledger that was never READ is not a ledger that holds nothing, and a
    # table of zeros for it would be the P6 lie in another dress.
    if not cost.ledger_exists:
        lines.append(
            "No ledger on disk for this scope — nothing has been recorded yet. "
            "Run 'remedy stats backfill-ledger <evidence-dir>' to mirror "
            "existing evidence."
        )
        return "\n".join(lines).rstrip("\n") + "\n"
    lines += _cost_section(cost)
    lines += _segment_section(shares)
    return "\n".join(lines).rstrip("\n") + "\n"
