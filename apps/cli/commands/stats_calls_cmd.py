"""`remedy stats calls` — tokens by kind per provider call and per landed change (F302 T004).

Read-only: it reads the run records and the job apply records and writes nothing. The figures come
from `packages/orchestration/call_tokens.py`; an unmeasured figure prints the word `unmeasured` and
is `null` in the JSON, never 0. DECISION F302 D4.
"""
from __future__ import annotations

from typing import Any

from apps.cli.commands.failure_stats_cmd import _validate_since
from apps.cli.json_envelope import emit_ok

#: The version of this command's own JSON payload.
CALLS_OUTPUT_VERSION = 1
UNMEASURED = "unmeasured"
_HEADERS = ("role", "provider", "calls", "measured", "input", "output", "cache creation",
            "cache read", "per call")


def _cell(value: Any) -> str:
    return f"{value:,}" if isinstance(value, int) else UNMEASURED


def _row(label_role: str, label_provider: str, figures: dict[str, Any]) -> list[str]:
    per = figures["per_call"]
    kinds = [_cell(per[k]) if per else UNMEASURED
             for k in ("input", "output", "cache_creation", "cache_read")]
    return [label_role, label_provider, str(figures["calls"]), str(figures["measured_calls"]), *kinds,
            _cell(figures["per_call_total"])]


def _jobs(count: int) -> str:
    return f"{count} landed job" if count == 1 else f"{count} landed jobs"


def render_calls_text(summary: dict[str, Any]) -> str:
    """The figures as a table of tokens per call by role and provider, then the landed changes."""
    rows = [_row(g["role"], g["provider"], g) for g in summary["groups"]]
    rows.append(_row("all", "", summary["all"]))
    widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(_HEADERS)]
    lines = ["Tokens by kind per provider call, read from each task's run record",
             "  ".join(h.ljust(widths[i]) for i, h in enumerate(_HEADERS)).rstrip()]
    lines += ["  ".join(c.ljust(widths[i]) for i, c in enumerate(r)).rstrip() for r in rows]
    if summary["per_landed_change"] is None:
        lines.append(f"Per landed change: {UNMEASURED} — {_jobs(summary['landed_changes'])} among "
                     "these calls.")
    else:
        per = summary["per_landed_change"]
        lines.append(
            f"Per landed change: {summary['per_landed_change_total']:,} tokens over "
            f"{_jobs(summary['landed_changes'])} — input {per['input']:,}, output "
            f"{per['output']:,}, cache creation {per['cache_creation']:,}, cache read "
            f"{per['cache_read']:,}.")
    return "\n".join(lines)


def _cmd_stats_calls(*, since: str = "", job: str = "", json_output: bool = False) -> None:
    from packages.orchestration.call_tokens import recorded_calls, summarize_call_tokens
    from packages.orchestration.job_apply import job_apply_landed

    since = _validate_since(since, json_output=json_output)
    summary = summarize_call_tokens(recorded_calls(since=since, job_id=job), landed=job_apply_landed)
    if json_output:
        emit_ok(version=CALLS_OUTPUT_VERSION, source="run records",
                filters={"since": since, "job": job}, **summary)
    else:
        print(render_calls_text(summary))


COMMAND_HANDLERS = {
    "stats.calls": lambda args: _cmd_stats_calls(
        since=getattr(args, "since", "") or "",
        job=getattr(args, "job", "") or "",
        json_output=getattr(args, "json", False),
    ),
}
