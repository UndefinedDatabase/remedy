"""Tokens by kind for every recorded provider call, per call and per landed change (F302 T004).

DECISION F302 D4. Each task run's record, `<data root>/runs/<run>/result.json`, lists one entry
per provider call under `provider_evidence.provider_attempts`, with its role, its provider and the
four figures the provider reported: input, output, cache creation and cache read. The token ledger
holds only the calls of a job with a project, so this reader reads the run records. A call whose
record carries no four whole figures is UNMEASURED: it is counted, and it adds nothing to a sum, so
an absent figure never reads as a zero. A landed change is a job whose change reached its target
repository, which `job_apply_landed` answers from its `remedy job apply` records.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration import data_paths

#: The four kinds of token a call reports, in the order every view prints them.
TOKEN_KINDS = ("input", "output", "cache_creation", "cache_read")
_USAGE_KEYS = {
    "input": "input_tokens",
    "output": "output_tokens",
    "cache_creation": "cache_creation_input_tokens",
    "cache_read": "cache_read_input_tokens",
}


@dataclass(frozen=True)
class RecordedCall:
    """One provider call as its run record holds it; `tokens` is None for an unmeasured call."""

    run_id: str
    job_id: str
    role: str
    provider: str
    tokens: dict[str, int] | None


def _instant(text: str) -> datetime | None:
    """An ISO-8601 timestamp as an aware instant, a date or a naive time read as UTC."""
    try:
        moment = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def _tokens(usage: Any) -> dict[str, int] | None:
    if not isinstance(usage, dict):
        return None
    figures = {kind: usage.get(key) for kind, key in _USAGE_KEYS.items()}
    if any(not isinstance(v, int) or isinstance(v, bool) or v < 0 for v in figures.values()):
        return None
    return figures


def recorded_calls(*, since: str = "", job_id: str = "", root: Path | None = None) -> list[RecordedCall]:
    """Every provider call of the run records, oldest run directory first.

    `since` keeps the runs that finished at or after it; a run whose finish time cannot be read is
    left out when `since` is given. `job_id` keeps the runs of that job. A record that cannot be
    read or parsed is skipped, so one torn file hides no other.
    """
    runs = data_paths.runs_dir(root)
    if not runs.is_dir():
        return []
    floor = _instant(since) if since else None
    calls: list[RecordedCall] = []
    for run in sorted(p for p in runs.iterdir() if p.is_dir()):
        try:
            data = json.loads((run / "result.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict):
            continue
        if job_id and data.get("job_id") != job_id:
            continue
        if floor is not None:
            finished = _instant(str(data.get("finished_at") or ""))
            if finished is None or finished < floor:
                continue
        evidence = data.get("provider_evidence")
        attempts = evidence.get("provider_attempts") if isinstance(evidence, dict) else None
        for attempt in attempts if isinstance(attempts, list) else []:
            if not isinstance(attempt, dict):
                continue
            calls.append(RecordedCall(
                run_id=str(data.get("run_id") or run.name),
                job_id=str(data.get("job_id") or ""),
                role=str(attempt.get("role") or "unknown"),
                provider=str(attempt.get("provider") or "unknown"),
                tokens=_tokens(attempt.get("usage")),
            ))
    return calls


def _figures(calls: list[RecordedCall]) -> dict[str, Any]:
    measured = [c.tokens for c in calls if c.tokens is not None]
    sums = {kind: sum(t[kind] for t in measured) for kind in TOKEN_KINDS} if measured else None
    total = sum(sums.values()) if sums else None
    per_call = ({kind: round(sums[kind] / len(measured)) for kind in TOKEN_KINDS}
                if sums else None)
    return {
        "calls": len(calls),
        "measured_calls": len(measured),
        "tokens": sums,
        "total_tokens": total,
        "per_call": per_call,
        "per_call_total": round(total / len(measured)) if total is not None else None,
    }


def summarize_call_tokens(calls: list[RecordedCall], *,
                          landed: Callable[[str], bool]) -> dict[str, Any]:
    """The figures by role and provider, over all calls, and per landed change.

    `per_landed_change` divides the tokens of EVERY measured call in `calls` — those of the jobs
    that did not land as well — by the number of distinct jobs among them that landed, so it is
    what one landed change cost; it is None when none landed or nothing was measured.
    """
    groups = []
    for role, provider in sorted({(c.role, c.provider) for c in calls}):
        member = [c for c in calls if (c.role, c.provider) == (role, provider)]
        groups.append({"role": role, "provider": provider, **_figures(member)})
    overall = _figures(calls)
    landed_jobs = sorted({c.job_id for c in calls if c.job_id and landed(c.job_id)})
    sums = overall["tokens"]
    per_landed = ({kind: round(sums[kind] / len(landed_jobs)) for kind in TOKEN_KINDS}
                  if sums and landed_jobs else None)
    return {
        "groups": groups,
        "all": overall,
        "landed_changes": len(landed_jobs),
        "landed_jobs": landed_jobs,
        "per_landed_change": per_landed,
        "per_landed_change_total": (round(overall["total_tokens"] / len(landed_jobs))
                                    if per_landed else None),
    }
