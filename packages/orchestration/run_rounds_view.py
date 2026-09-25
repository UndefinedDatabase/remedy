"""F023 T002 — the per-round facts of one task's latest run, for the graph's L2 run detail.

The brain graph draws its run nodes from the event stream, whose envelope carries no round
number, no duration and no token count (DECISION F023 D3). The run report that
`pingpong_loop.export_pingpong_json` persists at `data_paths.run_dir(run_id)/"result.json"`
holds all three for every round, and the job's task record keeps that run's id in
`TaskEntry.run_id`. This module reads that one report for one task and returns only
numbers, short vocabulary words and timestamps — never a summary, a finding text, a file
name or a path — so the envelope is safe to serve exactly as built.

It never raises. An unknown task, a task with no run yet, and a report that is missing or
unreadable are each a named `reason` in an envelope with `available` false, because an
absence the reader can name is data, as it is for the diff route beside it.

`TaskEntry.run_id` names the task's LATEST run only: a task that ran twice has the second
run's rounds here and the first run's nowhere a job points at.
"""
from __future__ import annotations

import json
import re
from collections.abc import Callable
from datetime import datetime
from typing import Any

#: The envelope's shape version; a reader refuses any other.
TASK_RUN_ROUNDS_VERSION = 1

REASON_UNKNOWN_TASK = "unknown_task"
REASON_NO_RUN = "no_run_recorded"
REASON_REPORT_MISSING = "run_report_missing"
REASON_REPORT_UNREADABLE = "run_report_unreadable"

# A run id is minted as sixteen lowercase hex digits (`data_paths.mint_run_id`); anything
# else in a task record is refused before it can become a path segment.
_RUN_ID_RE = re.compile(r"[0-9a-f]{8,32}")
# A vocabulary word the report may carry (a round kind, a reviewer verdict).
_WORD_RE = re.compile(r"[a-z_]{1,32}")


def _read_run_report(run_id: str) -> tuple[dict[str, Any] | None, str | None]:
    """The persisted run report, or None with the reason it could not be had."""
    from packages.orchestration.data_paths import run_dir

    path = run_dir(run_id) / "result.json"
    if not path.is_file():
        return None, REASON_REPORT_MISSING
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, REASON_REPORT_UNREADABLE
    if not isinstance(data, dict):
        return None, REASON_REPORT_UNREADABLE
    return data, None


def _count(value: Any) -> int | None:
    """A non-negative whole number, or None; a bool is not a count."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _word(value: Any) -> str | None:
    return value if isinstance(value, str) and _WORD_RE.fullmatch(value) else None


def _instant(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _span_ms(started: datetime | None, finished: datetime | None) -> int | None:
    """Milliseconds from start to finish, or None when either end is missing or the two
    cannot be compared, or when the finish comes first."""
    if started is None or finished is None:
        return None
    try:
        delta = (finished - started).total_seconds()
    except TypeError:
        return None
    return int(round(delta * 1000)) if delta >= 0 else None


def _round_facts(raw: dict[str, Any]) -> dict[str, Any]:
    started, finished = _instant(raw.get("started_at")), _instant(raw.get("finished_at"))
    test_passed = raw.get("test_passed")
    facts: dict[str, Any] = {
        "round": _count(raw.get("round")),
        "kind": _word(raw.get("kind")),
        "started_at": started.isoformat() if started else None,
        "finished_at": finished.isoformat() if finished else None,
        "duration_ms": _span_ms(started, finished),
        "test_passed": test_passed if isinstance(test_passed, bool) else None,
        "builder": None,
        "reviewer": None,
    }
    builder = raw.get("builder")
    if isinstance(builder, dict):
        facts["builder"] = {
            "duration_ms": _count(builder.get("duration_ms")),
            "tokens_used": _count(builder.get("tokens_used")),
        }
    reviewer = raw.get("reviewer")
    if isinstance(reviewer, dict):
        facts["reviewer"] = {
            "verdict": _word(reviewer.get("verdict")),
            "duration_ms": _count(reviewer.get("duration_ms")),
            "parse_retried": reviewer.get("parse_retried") is True,
        }
    return facts


def build_task_run_rounds(
    job: Any,
    task_id: str,
    *,
    read_report: Callable[[str], tuple[dict[str, Any] | None, str | None]] = _read_run_report,
) -> dict[str, Any]:
    """The rounds envelope for one task of one job. Never raises."""
    envelope: dict[str, Any] = {
        "version": TASK_RUN_ROUNDS_VERSION,
        "job_id": str(getattr(job, "job_id", "")),
        "task_id": task_id,
        "available": False,
        "reason": None,
        "run_id": None,
        "retries_used": None,
        "rounds": [],
    }
    task = next((t for t in getattr(job, "tasks", None) or [] if getattr(t, "task_id", None) == task_id), None)
    if task is None:
        envelope["reason"] = REASON_UNKNOWN_TASK
        return envelope
    run_id = getattr(task, "run_id", "")
    if not isinstance(run_id, str) or not _RUN_ID_RE.fullmatch(run_id):
        envelope["reason"] = REASON_NO_RUN
        return envelope
    envelope["run_id"] = run_id
    report, reason = read_report(run_id)
    if report is None:
        envelope["reason"] = reason or REASON_REPORT_UNREADABLE
        return envelope
    rounds = report.get("rounds")
    envelope["rounds"] = [_round_facts(r) for r in rounds if isinstance(r, dict)] if isinstance(rounds, list) else []
    envelope["retries_used"] = _count(report.get("retries_used"))
    envelope["available"] = True
    return envelope
