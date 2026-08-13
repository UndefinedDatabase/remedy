"""`remedy stats cost` / `cache` / `report` / `backfill-ledger` / `verify-ledger` (F103, F115).

Five commands over the per-project SQLite ledger: query it three ways, mirror the
evidence into it, and check that the mirror still matches the files. `report`
(F115) is the widest of the three reads — the cost table, where the prompt tokens
went, and the equal-length period before this one — and it is deliberately the
only one WITHOUT `--all-projects`: cost folds across projects but the segment
breakdown does not, so an all-projects report would publish one project's
breakdown under a multi-project total.

EVERY COST FIGURE NAMES ITS BASIS. That is the feature's own acceptance
criterion (P6) and it is the reason this module is longer than a table printer
needs to be: a bucket in which no provider reported usage prints the word
``unmeasured`` and never the digit 0, the basis breakdown
(``provider_reported`` versus ``unknown``) is carried on every row in BOTH output
modes, and a total that is only partly measured says so in a sentence a reader
cannot skim past. A number without its provenance is the failure this feature
exists to prevent.

Remedy deliberately does NOT compute a price anywhere here. ``cost_usd`` is
printed only where a provider reported one; there is no price table, so an
unpriced call stays unpriced instead of being multiplied into a plausible
figure.

THE FILES REMAIN THE SOURCE OF TRUTH AND THE DATABASE IS A MIRROR. `cost` reads
the mirror; `verify-ledger` is how a disagreement between the two is found; and
`backfill-ledger` is the only one of the three that writes anything.
"""
from __future__ import annotations

import json as _json
import sys
from pathlib import Path

from packages.orchestration.cost_report import COST_UNMEASURED_LABEL

EXIT_USAGE = 2
EXIT_ERROR = 1

#: `verify-ledger` exits with this when the mirror disagrees with the files, so
#: the command is usable as a check in a script or a gate. A clean reconcile
#: exits 0.
EXIT_DRIFT = 1

#: The payload version, so a consumer of `--json` can tell shapes apart.
COST_OUTPUT_VERSION = 1

#: What an unmeasured figure prints as. Never `0`, never blank: a reader must be
#: able to tell "nobody reported this" from "it was zero", and only a WORD does
#: that in a column of numbers. THE SPELLING NOW LIVES IN ONE PLACE — the word is
#: defined by `cost_report.COST_UNMEASURED_LABEL` and imported here, so this
#: module's tables and the report renderer cannot come to print two different
#: words for the same absence (AGENTS.md, Code Discoverability).
UNMEASURED = COST_UNMEASURED_LABEL

#: The measurement columns of a cost row, in render order, with their headers.
_FIGURE_COLUMNS = (
    ("tokens_in", "Tokens in"),
    ("tokens_out", "Tokens out"),
    ("cache_read", "Cache read"),
    ("cache_write", "Cache write"),
    ("cost_usd", "Cost USD"),
)


def _validate_by(raw: str | None) -> str | None:
    """`--by` accepts exactly the ledger's own group keys, or nothing at all."""
    from packages.orchestration.token_ledger import COST_GROUP_KEYS

    text = (raw or "").strip()
    if not text:
        return None
    if text not in COST_GROUP_KEYS:
        print(
            f"Error: --by {raw!r} is not a grouping; use one of "
            f"{', '.join(COST_GROUP_KEYS)}",
            file=sys.stderr,
        )
        raise SystemExit(EXIT_USAGE)
    return text


# One end of a report period, validated under ITS OWN FLAG NAME.
def _validate_period_bound(raw: str | None, *, flag: str) -> str:
    """`--since` or `--until` as an ISO-8601 timestamp, or a usage error NAMING it.

    `flag` is a parameter rather than a hardcoded word because this validator
    runs twice per invocation: a message that always says `--since` would send a
    reader to the flag they typed correctly while the wrong one stays wrong. Only
    `stats report` uses this — `stats cost` and `stats cache` keep the
    single-bound `_validate_since` they already share with `stats failures`.
    """
    from datetime import datetime

    text = (raw or "").strip()
    if not text:
        return ""
    try:
        # `Z` for UTC is the same spelling `token_ledger._parse_period_bound`
        # accepts, so a bound this command takes is one the query can compare.
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        print(
            f"Error: {flag} {raw!r} is not an ISO-8601 timestamp "
            f"(e.g. 2026-07-13 or 2026-07-13T12:00:00+00:00)",
            file=sys.stderr,
        )
        raise SystemExit(EXIT_USAGE) from None
    return text


def _ledger_paths_for_scope(project: str | None, all_projects: bool) -> tuple[list[Path], str]:
    """Every ledger this invocation may READ, plus a human label for the scope.

    Under `--all-projects` the ledgers are discovered by globbing the projects
    area and keeping only files that ALREADY EXIST — reading across projects must
    never create or migrate another project's database, so a project without a
    ledger simply contributes nothing.
    """
    from packages.orchestration.data_paths import projects_dir
    from packages.orchestration.project_scope import resolve_scope
    from packages.orchestration.token_ledger import LEDGER_FILENAME, token_ledger_path_for

    scope = resolve_scope(project_flag=project, all_projects=all_projects)
    if scope.all_projects or scope.project_id is None:
        found = sorted(projects_dir().glob(f"*/{LEDGER_FILENAME}"))
        return [p for p in found if p.is_file()], "all projects"
    return [token_ledger_path_for(scope.project_id)], f"project {scope.project_id}"


def _one_project_ledger(project: str | None, all_projects: bool, *, action: str) -> Path:
    """The single ledger a per-project command acts on, or a usage error.

    `--all-projects` is refused here on purpose. Backfill WRITES, and a reconcile
    compares ONE evidence tree against ONE project's ledger; spreading either
    across every project would mean guessing which project the evidence belongs
    to. Read-only aggregation across projects is `stats cost`'s job alone.
    """
    from packages.orchestration.project_scope import resolve_scope
    from packages.orchestration.token_ledger import token_ledger_path_for

    if all_projects:
        print(
            f"Error: --all-projects is a read-only aggregation for 'stats cost'; "
            f"{action} needs exactly one project. Use --project <slug-or-uuid>.",
            file=sys.stderr,
        )
        raise SystemExit(EXIT_USAGE)
    scope = resolve_scope(project_flag=project, all_projects=False)
    if scope.project_id is None:
        print(
            f"Error: no project resolved for {action}. Run inside a registered "
            f"project or pass --project <slug-or-uuid>.",
            file=sys.stderr,
        )
        raise SystemExit(EXIT_ERROR)
    return token_ledger_path_for(scope.project_id)


def _require_evidence_dir(raw: str) -> Path:
    """The evidence directory must exist; scanning a typo would report a false zero."""
    text = (raw or "").strip()
    if not text:
        print("Error: an evidence directory is required", file=sys.stderr)
        raise SystemExit(EXIT_USAGE)
    path = Path(text)
    if not path.is_dir():
        print(f"Error: evidence directory not found: {text}", file=sys.stderr)
        raise SystemExit(EXIT_USAGE)
    return path


def _row_basis(row) -> str:
    """The one word that says how measured a bucket is: the row's own basis."""
    from packages.orchestration.token_ledger import (
        COST_BASIS_PROVIDER_REPORTED,
        COST_BASIS_UNKNOWN,
    )

    if row.calls == 0:
        return COST_BASIS_UNKNOWN
    if row.measured_calls == row.calls:
        return COST_BASIS_PROVIDER_REPORTED
    if row.measured_calls == 0:
        return COST_BASIS_UNKNOWN
    return "mixed"


def _row_payload(row) -> dict:
    """One cost row as JSON: unmeasured figures stay ``null``, never 0."""
    payload = {"bucket": row.bucket, "calls": row.calls}
    payload.update({name: getattr(row, name) for name, _ in _FIGURE_COLUMNS})
    payload.update({
        "measured_calls": row.measured_calls,
        "unmeasured_calls": row.unmeasured_calls,
        "basis": _row_basis(row),
    })
    return payload


def _cost_payload(report, *, ledgers_read: list[str], scope_label: str) -> dict:
    """The `--json` document: the figures, their basis, and where they came from."""
    return {
        "version": COST_OUTPUT_VERSION,
        "scope": scope_label,
        "ledgers_read": ledgers_read,
        "filters": {
            "since": report.since or "",
            "job": report.job_id or "",
            "by": report.by,
        },
        "basis": {
            "measured_calls": report.total.measured_calls,
            "unmeasured_calls": report.total.unmeasured_calls,
            "fully_measured": report.total.fully_measured,
            "unmeasured_notation": "null",
            "note": (
                "a null figure was never reported — it is not a zero; "
                "no price is ever computed"
            ),
        },
        "total": _row_payload(report.total),
        "rows": [_row_payload(row) for row in report.rows],
    }


def _figure(value) -> str:
    """Render one measurement — or the unmeasured word when nobody reported it."""
    if value is None:
        return UNMEASURED
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def _render_cost_human(report, *, ledgers_read: list[str], scope_label: str) -> str:
    """A readable table in which no unmeasured figure can be mistaken for a zero."""
    lines = [f"Cost from the token ledger — {scope_label}, "
             f"{len(ledgers_read)} ledger(s) read"]
    filters = [f"{name}={value}" for name, value in (
        ("since", report.since or "-"),
        ("job", report.job_id or "-"),
        ("by", report.by or "-"),
    )]
    lines.append("Filters: " + "  ".join(filters))

    # No ledger was READ — which is not the same as a ledger that holds nothing,
    # and printing a table of zeros for it would be the P6 lie in another dress.
    if not report.ledger_exists:
        lines.append("")
        lines.append("No ledger on disk for this scope — nothing has been recorded yet.")
        lines.append("Run 'remedy stats backfill-ledger <evidence-dir>' to mirror "
                     "existing evidence.")
        return "\n".join(lines)

    headers = ["Bucket", "Calls", *(label for _, label in _FIGURE_COLUMNS), "Basis"]
    body = [
        [
            row.bucket if row.bucket is not None else "(unnamed)",
            str(row.calls),
            *(_figure(getattr(row, name)) for name, _ in _FIGURE_COLUMNS),
            f"{_row_basis(row)} ({row.measured_calls}/{row.calls})",
        ]
        for row in report.rows
    ]
    total = report.total
    body.append([
        "TOTAL",
        str(total.calls),
        *(_figure(getattr(total, name)) for name, _ in _FIGURE_COLUMNS),
        f"{_row_basis(total)} ({total.measured_calls}/{total.calls})",
    ])
    widths = [max(len(headers[i]), *(len(r[i]) for r in body)) for i in range(len(headers))]
    lines.append("")
    # rstrip: the last column is padded like every other, and a table that
    # trails whitespace is a diff hazard wherever the output gets captured.
    lines.append("  ".join(h.ljust(w) for h, w in zip(headers, widths)).rstrip())
    for row in body:
        lines.append("  ".join(cell.ljust(w) for cell, w in zip(row, widths)).rstrip())

    lines.append("")
    lines.append(
        f"Basis: {total.measured_calls} of {total.calls} call(s) reported usage "
        f"(provider_reported); {total.unmeasured_calls} reported none (unknown)."
    )
    # In words, because a partial total that LOOKS complete is the exact mistake
    # this feature exists to prevent.
    if total.calls and total.measured_calls == 0:
        lines.append(
            f"FULLY UNMEASURED: not one of these {total.calls} call(s) reported "
            f"usage or cost. Every figure above is unknown, not zero."
        )
    elif total.calls and not total.fully_measured:
        lines.append(
            f"PARTLY UNMEASURED: these figures cover only the "
            f"{total.measured_calls} call(s) whose provider reported them. "
            f"The {total.unmeasured_calls} unmeasured call(s) contribute nothing "
            f"to any figure above — this is NOT a complete total."
        )
    lines.append("No price is computed: a cost appears only where a provider reported one.")
    return "\n".join(lines)


# Every read a ledger VIEW needs, in one place, so renderers stay renderers.
def _load_ledger_reports(*, since: str, job: str, by: str | None,
                         project: str | None, all_projects: bool,
                         json_output: bool):
    """Validate the filters, query every ledger in scope, and merge the answers.

    Views over this ledger ask it the SAME question and differ only in what they
    render from the answer, so the reading lives here once. Returns the merged
    report, the ledger paths actually READ, and the scope label, in that order.

    An unreadable ledger EXITS here instead of returning an empty report: a
    database error does not mean zero, and rendering it as zero would be the
    exact lie the basis labeling exists to prevent.
    """
    import sqlite3

    from apps.cli.commands.failure_stats_cmd import _validate_since
    from packages.orchestration.token_ledger import merge_cost_reports, query_cost

    # One spelling of "what is a valid --since", shared with `stats failures`.
    since = _validate_since(since)
    by = _validate_by(by)
    ledgers, scope_label = _ledger_paths_for_scope(project, all_projects)

    try:
        reports = [
            query_cost(path=path, since=since or None, job_id=job or None, by=by)
            for path in ledgers
        ]
    except sqlite3.Error as exc:
        if json_output:
            print(_json.dumps({"ok": False, "error": str(exc)}, indent=2))
        else:
            print(f"Error: cannot read the token ledger: {exc}", file=sys.stderr)
        raise SystemExit(EXIT_ERROR) from None

    report = reports[0] if len(reports) == 1 else merge_cost_reports(reports)
    # What was actually READ, not what was looked for: a project whose ledger does
    # not exist yet contributes no file and no figure.
    ledgers_read = [r.ledger_path for r in reports if r.ledger_exists and r.ledger_path]
    return report, ledgers_read, scope_label


def _cmd_stats_cost(*, since: str = "", job: str = "", by: str | None = None,
                    project: str | None = None,
                    all_projects: bool = False,
                    json_output: bool = False) -> None:
    report, ledgers_read, scope_label = _load_ledger_reports(
        since=since, job=job, by=by, project=project,
        all_projects=all_projects, json_output=json_output)
    if json_output:
        print(_json.dumps(_cost_payload(
            report, ledgers_read=ledgers_read, scope_label=scope_label), indent=2))
    else:
        print(_render_cost_human(
            report, ledgers_read=ledgers_read, scope_label=scope_label))


#: What a share prints when its inputs WERE reported and are both zero. That is
#: NOT "nobody reported it": it is a real bucket that read nothing at all, and a
#: share of nothing has no value. Calling that `unmeasured` would blame a
#: provider for a figure it did report, and `0.0%` would invent a measurement.
UNDEFINED_SHARE = "undefined"

#: What a role split cannot tell a reader yet, printed in the output instead of
#: buried in a docstring. Every ledger row a live run writes carries one
#: hardcoded role, so a role split of production data has exactly one bucket;
#: further buckets come from hand-written accounting files. Remedy names the
#: limit rather than presenting one bucket as a breakdown.
_ROLE_LIMIT_NOTE = (
    "Per-role limit: every row a live run writes carries one hardcoded role "
    "today, so a role split of production data shows a single bucket. Any "
    "further bucket here came from a hand-written accounting file, not from "
    "the orchestrator."
)


def _cache_read_share(row) -> float | str:
    """The bucket's cache-read share, or the word saying why it has none.

    The share is ``cache_read / (tokens_in + cache_read)``: of everything fed
    into the model, how much came from cache. BOTH inputs must be measured — an
    unmeasured input makes the share unmeasured too, because substituting a 0
    for a figure nobody reported is the same lie one layer up.
    """
    cache_read, tokens_in = row.cache_read, row.tokens_in
    if cache_read is None or tokens_in is None:
        return UNMEASURED
    total_input = tokens_in + cache_read
    if total_input == 0:
        return UNDEFINED_SHARE
    return cache_read / total_input


def _share_text(share) -> str:
    """One share as a table cell: a percentage, or the word standing in for it."""
    return share if isinstance(share, str) else f"{share * 100:.1f}%"


def _cache_row_payload(row) -> dict:
    """One cache row as JSON: the share is a number, or null carrying its reason.

    A consumer that only reads ``cache_read_share`` sees ``null`` and knows the
    figure is absent; one that needs to know WHY reads ``share_basis``, which
    carries the same word the table prints. The two absences never collapse
    into one, and neither ever becomes a 0.
    """
    share = _cache_read_share(row)
    return {
        "bucket": row.bucket,
        "calls": row.calls,
        "tokens_in": row.tokens_in,
        "cache_read": row.cache_read,
        "cache_read_share": None if isinstance(share, str) else round(share, 6),
        "share_basis": share if isinstance(share, str) else "measured",
        "measured_calls": row.measured_calls,
        "unmeasured_calls": row.unmeasured_calls,
        "basis": _row_basis(row),
    }


def _cache_payload(report, *, ledgers_read: list[str], scope_label: str) -> dict:
    """The `--json` document for the cache view, carrying its own limits."""
    return {
        "version": COST_OUTPUT_VERSION,
        "scope": scope_label,
        "ledgers_read": ledgers_read,
        "filters": {"since": report.since or "", "job": report.job_id or "",
                    "by": report.by},
        "share_formula": "cache_read / (tokens_in + cache_read)",
        "note": ("a null share was never measurable and is not a zero share; "
                 "share_basis names which of the two reasons applies"),
        "role_limit": _ROLE_LIMIT_NOTE,
        "total": _cache_row_payload(report.total),
        "rows": [_cache_row_payload(row) for row in report.rows],
    }


def _render_cache_human(report, *, ledgers_read: list[str], scope_label: str) -> str:
    """A share table in which no missing share can be mistaken for 0 %."""
    lines = [f"Cache-read share from the token ledger — {scope_label}, "
             f"{len(ledgers_read)} ledger(s) read"]
    lines.append("Filters: " + "  ".join(f"{name}={value}" for name, value in (
        ("since", report.since or "-"),
        ("job", report.job_id or "-"),
        ("by", report.by or "-"),
    )))

    if not report.ledger_exists:
        lines.append("")
        lines.append("No ledger on disk for this scope — nothing has been recorded yet.")
        lines.append("Run 'remedy stats backfill-ledger <evidence-dir>' to mirror "
                     "existing evidence.")
        return "\n".join(lines)

    headers = ["Bucket", "Calls", "Tokens in", "Cache read", "Cache share", "Basis"]
    labelled = [(row.bucket if row.bucket is not None else "(unnamed)", row)
                for row in report.rows] + [("TOTAL", report.total)]
    body = [
        [
            label,
            str(row.calls),
            _figure(row.tokens_in),
            _figure(row.cache_read),
            _share_text(_cache_read_share(row)),
            f"{_row_basis(row)} ({row.measured_calls}/{row.calls})",
        ]
        for label, row in labelled
    ]
    widths = [max(len(headers[i]), *(len(r[i]) for r in body)) for i in range(len(headers))]
    lines.append("")
    lines.append("  ".join(h.ljust(w) for h, w in zip(headers, widths)).rstrip())
    for row in body:
        lines.append("  ".join(cell.ljust(w) for cell, w in zip(row, widths)).rstrip())

    total = report.total
    lines.append("")
    lines.append("Share = cache_read / (tokens_in + cache_read).")
    lines.append(f"'{UNMEASURED}' means nobody reported the inputs; "
                 f"'{UNDEFINED_SHARE}' means they were reported and were zero.")
    lines.append(
        f"Basis: {total.measured_calls} of {total.calls} call(s) reported usage "
        f"(provider_reported); {total.unmeasured_calls} reported none (unknown)."
    )
    if report.by == "role":
        lines.append(_ROLE_LIMIT_NOTE)
    return "\n".join(lines)


def _cmd_stats_cache(*, since: str = "", job: str = "", by: str | None = None,
                     project: str | None = None,
                     all_projects: bool = False,
                     json_output: bool = False) -> None:
    report, ledgers_read, scope_label = _load_ledger_reports(
        since=since, job=job, by=by, project=project,
        all_projects=all_projects, json_output=json_output)
    if json_output:
        print(_json.dumps(_cache_payload(
            report, ledgers_read=ledgers_read, scope_label=scope_label), indent=2))
    else:
        print(_render_cache_human(
            report, ledgers_read=ledgers_read, scope_label=scope_label))


# The widest read: the cost table, the segment breakdown and the period before.
def _cmd_stats_report(*, since: str = "", until: str = "", job: str = "",
                      by: str | None = None, label: str | None = None,
                      project: str | None = None,
                      json_output: bool = False) -> None:
    """Render `cost_report` over ONE project's ledger, markdown or json.

    EXACTLY ONE PROJECT, and no `--all-projects`: `merge_cost_reports` folds cost
    across projects but nothing folds the segment breakdown, so an all-projects
    report would publish one project's breakdown under a multi-project total —
    the very mismatch `cost_report._same_question` exists to refuse.
    """
    import sqlite3

    from packages.orchestration.cost_report import (
        cost_report_json_bytes,
        render_cost_report_markdown,
    )
    from packages.orchestration.token_ledger import (
        prior_report_period,
        query_cost,
        query_segment_shares,
    )

    since = _validate_period_bound(since, flag="--since")
    until = _validate_period_bound(until, flag="--until")
    by = _validate_by(by)
    ledger = _one_project_ledger(project, False, action="stats report")

    period = prior_report_period(since or None, until or None)
    try:
        cost = query_cost(path=ledger, since=since or None, until=until or None,
                          job_id=job or None, by=by)
        shares = query_segment_shares(path=ledger, since=since or None,
                                      until=until or None, job_id=job or None)
        prior = None
        if period.available:
            # THE SAME `job` FILTER, deliberately. A period filtered to one job
            # compared against a previous window holding every job is two
            # questions, not one — the defect `_same_question` refuses a layer
            # up, and the CLI must not be the thing that constructs it.
            prior = query_cost(path=ledger, since=period.since, until=period.until,
                               job_id=job or None, by=None)
    except sqlite3.Error as exc:
        # A database error is not a zero, so this refuses to render rather than
        # publishing an empty report — the same choice `_load_ledger_reports`
        # makes, for the same reason.
        if json_output:
            print(_json.dumps({"ok": False, "error": str(exc)}, indent=2))
        else:
            print(f"Error: cannot read the token ledger: {exc}", file=sys.stderr)
        raise SystemExit(EXIT_ERROR) from None

    rendered = (cost_report_json_bytes if json_output else render_cost_report_markdown)(
        cost, shares, label=label, prior=prior,
        no_comparison_reason=None if period.available else period.unavailable_reason,
    )
    # Both renderers already end in exactly one newline; print must not add a second.
    print(rendered, end="")


def _cmd_stats_backfill_ledger(*, evidence_dir: str = "",
                               project: str | None = None,
                               all_projects: bool = False,
                               json_output: bool = False) -> None:
    from packages.orchestration.token_ledger import backfill_ledger

    base = _require_evidence_dir(evidence_dir)
    ledger = _one_project_ledger(project, all_projects, action="backfill-ledger")
    result = backfill_ledger(base, path=ledger)

    if json_output:
        print(_json.dumps({
            "version": COST_OUTPUT_VERSION,
            "evidence_dir": str(base),
            "ledger": str(ledger),
            "scanned": result.scanned,
            "recorded": result.recorded,
            "skipped": result.skipped,
            "failed": result.failed,
        }, indent=2))
        return

    print(f"Backfill of {base} into {ledger}")
    print(f"  scanned:  {result.scanned} task run(s)")
    print(f"  recorded: {result.recorded} row(s) durable (a re-run records the same rows)")
    print(f"  skipped:  {result.skipped} task run(s) with no provider evidence to mirror")
    print(f"  failed:   {result.failed} task run(s) unrecordable — no row was invented")
    print("Backfill is idempotent: the same evidence always yields the same rows.")


def _cmd_stats_verify_ledger(*, evidence_dir: str = "",
                             project: str | None = None,
                             all_projects: bool = False,
                             json_output: bool = False) -> None:
    from packages.orchestration.token_ledger import verify_ledger

    base = _require_evidence_dir(evidence_dir)
    ledger = _one_project_ledger(project, all_projects, action="verify-ledger")
    result = verify_ledger(base, path=ledger)

    if json_output:
        print(_json.dumps({
            "version": COST_OUTPUT_VERSION,
            "evidence_dir": str(base),
            "ledger": str(ledger),
            "checked": result.checked,
            "missing_rows": result.missing_rows,
            "orphan_rows": result.orphan_rows,
            "drifted_rows": result.drifted_rows,
            "unreadable": result.unreadable,
            "has_drift": result.has_drift,
        }, indent=2))
    else:
        print(f"Reconcile of {base} against {ledger}")
        print(f"  checked:  {result.checked} task run(s) carrying provider evidence")
        print(f"  missing:  {len(result.missing_rows)} row(s) on disk with no row in the ledger")
        print(f"  orphan:   {len(result.orphan_rows)} row(s) in the ledger with no evidence")
        print(f"  drifted:  {len(result.drifted_rows)} row(s) whose contents no longer match")
        print(f"  unreadable: {len(result.unreadable)} task run(s) nothing can be said about")
        for label, ids in (("missing", result.missing_rows),
                           ("orphan", result.orphan_rows),
                           ("drifted", result.drifted_rows)):
            for call_id in ids:
                print(f"    {label}: {call_id}")
        if result.has_drift:
            print("DRIFT: the files are the source of truth, so the ledger is wrong here. "
                  "Run 'remedy stats backfill-ledger' to re-record missing rows.")
        else:
            print("Clean: the ledger agrees with the evidence files.")

    if result.has_drift:
        raise SystemExit(EXIT_DRIFT)


COMMAND_HANDLERS = {
    "stats.cost": lambda args: _cmd_stats_cost(
        since=getattr(args, "since", "") or "",
        job=getattr(args, "job", "") or "",
        by=getattr(args, "by", None),
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=getattr(args, "json", False),
    ),
    "stats.cache": lambda args: _cmd_stats_cache(
        since=getattr(args, "since", "") or "",
        job=getattr(args, "job", "") or "",
        by=getattr(args, "by", None),
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=getattr(args, "json", False),
    ),
    "stats.report": lambda args: _cmd_stats_report(
        since=getattr(args, "since", "") or "",
        until=getattr(args, "until", "") or "",
        job=getattr(args, "job", "") or "",
        by=getattr(args, "by", None),
        label=getattr(args, "label", None),
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
    "stats.backfill-ledger": lambda args: _cmd_stats_backfill_ledger(
        evidence_dir=getattr(args, "evidence_dir", "") or "",
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=getattr(args, "json", False),
    ),
    "stats.verify-ledger": lambda args: _cmd_stats_verify_ledger(
        evidence_dir=getattr(args, "evidence_dir", "") or "",
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=getattr(args, "json", False),
    ),
}
