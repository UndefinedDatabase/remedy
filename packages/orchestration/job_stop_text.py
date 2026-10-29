"""F325 — every stop says why, in one sentence a person reads.

decodeux, 2026-10-29: "warum wurden sämtliche Verbesserungsläufe in remedy gebaut und alle
angehalten, teilweise ohne gründe". Every blocked job of the night of 2026-10-28 carried an empty
`stop.reason`: the reason sat in a task's `error` (`completion_gate_failed: final_status=
staged_blocked; reviewer_verdict=blocked`) and in the reviewer's findings of the task's run record,
and no answer a client reads said it.

`job_stop` is the one reading of why a job stopped: the job's own `stop_text` when a step wrote one
(F323's waiting jobs), else a sentence derived from its record, in this order: the task that ended
blocked or failed (the review's verdict with its findings by severity and the first finding, a
failed test run, the story's own closed reason for the run's error), the job's `stop_reason`, its pause reason, its
`error`. It feeds the story's `stop`, each order job's `stop_text` and `remedy job show --json`'s
`stop.text`, so the three always say the same sentence.

Remedy deliberately writes these sentences in English, like every other sentence of its answers
(`waiting_reason`); a client shows or translates them.
"""
from __future__ import annotations

import re
from typing import Any

#: The job states whose stop always carries a sentence; a paused job carries one when it has a reason.
JOB_STOP_STATES: tuple[str, ...] = ("blocked", "stopped", "cancelled", "failed")
#: The stop reason token of a task the review blocked, when the job recorded none of its own.
STOP_REASON_REVIEW_BLOCKED = "review_blocked"
#: The stop reason token of a task whose tests failed, when the job recorded none of its own.
STOP_REASON_TESTS_FAILED = "tests_failed"
#: The severities in the order the sentence names them.
_SEVERITY_ORDER = ("blocker", "high", "medium", "low")
#: How much of the first finding's summary the sentence quotes.
_FINDING_SUMMARY_CHARS = 240
_COUNT_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def _state_word(job: Any) -> str:
    return str(getattr(job.state, "value", job.state))


def _stopped_task(job: Any) -> Any:
    from packages.orchestration.pingpong_job import TASK_BLOCKED, TASK_FAILED

    return next((task for task in job.tasks if task.status in (TASK_BLOCKED, TASK_FAILED)), None)


def _task_findings(job: Any, task: Any) -> list[dict[str, Any]]:
    """The last round's findings of TASK's run record; [] when it has none or cannot be read."""
    from packages.orchestration.job_report import collect_blocked_task_findings

    for entry in collect_blocked_task_findings(job, full=True):
        if entry["task_id"] == task.task_id:
            return list(entry["findings"])
    return []


def _severity_counts(findings: list[dict[str, Any]]) -> str:
    """"one medium finding", "two high and one low finding"; "" for none."""
    counts: dict[str, int] = {}
    for finding in findings:
        severity = str(finding.get("severity") or "unrated").lower()
        counts[severity] = counts.get(severity, 0) + 1
    order = [s for s in _SEVERITY_ORDER if s in counts] + sorted(s for s in counts if s not in _SEVERITY_ORDER)
    parts = [f"{_COUNT_WORDS.get(counts[s], str(counts[s]))} {s}" for s in order]
    if not parts:
        return ""
    joined = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]
    return f"{joined} finding{'s' if len(findings) > 1 else ''}"


def _review_sentence(job: Any, task: Any) -> str:
    findings = _task_findings(job, task)
    verdict = task.reviewer_verdict or "blocked"
    text = f"The review ended task \"{task.title}\" with the verdict {verdict}"
    counted = _severity_counts(findings)
    if counted:
        first = findings[0]
        summary = " ".join(str(first.get("summary") or "").split())
        if len(summary) > _FINDING_SUMMARY_CHARS:
            summary = summary[:_FINDING_SUMMARY_CHARS - 1].rstrip() + "…"
        text += f" on {counted}"
        if summary:
            text += f"; the first ({first.get('severity') or 'unrated'}): {summary}"
    return text.rstrip(".") + "."


def _task_sentence(job: Any, task: Any) -> tuple[str, str]:
    """The reason token and the sentence of the task that stopped JOB."""
    ended = task.final_status or task.status
    if task.reviewer_verdict in ("blocked", "needs_repair") or task.final_status == "staged_blocked":
        return STOP_REASON_REVIEW_BLOCKED, _review_sentence(job, task)
    if task.test_passed is False:
        return STOP_REASON_TESTS_FAILED, f"The tests of task \"{task.title}\" failed, so it ended {ended}."
    # The story carries closed words, never a provider's own text (exec-1018, R-1347): the sentence
    # names the story's reason, else the error's leading token, and quotes nothing else of it.
    from packages.orchestration.client_story import story_failure_key

    key = story_failure_key(job)
    token = key if key and key != "unknown" else _error_token(task.final_status_detail or task.error)
    sentence = f"Task \"{task.title}\" ended {task.status}" + (f": {token.replace('_', ' ')}" if token else "")
    return token or str(ended), sentence + "."


def _error_token(error: str) -> str:
    """The leading closed token of a recorded error (`provider_unavailable: down` -> `provider_unavailable`)."""
    head = str(error or "").split(":", 1)[0].strip()
    return head if re.fullmatch(r"[a-z][a-z0-9_]*", head) else ""


def job_stop(job: Any) -> dict[str, str]:
    """Why JOB stopped: `reason`, a token or "", and `text`, one sentence or "" for a job that did not stop."""
    state = _state_word(job)
    reason = str(getattr(job, "stop_reason", "") or "")
    text = str(getattr(job, "stop_text", "") or "")
    pause = getattr(job, "pause", None) or {}
    if state == "paused" and not text and isinstance(pause, dict) and pause.get("reason"):
        return {"reason": reason or str(pause.get("source") or ""), "text": f"The job paused: {pause['reason']}."}
    if state not in JOB_STOP_STATES:
        return {"reason": reason, "text": text}
    task = _stopped_task(job)
    if task is not None and not text:
        token, text = _task_sentence(job, task)
        reason = reason or token
    if not text and reason:
        text = f"The job {state}: {reason.replace('_', ' ')}."
    error = _error_token(str(getattr(job, "error", None) or ""))
    if not text and error:
        text = f"The job {state}: {error.replace('_', ' ')}."
    if not text:
        text = (f"The job {state} and recorded no reason; `remedy job show {job.job_id} --full` "
                f"has its run's details.")
    return {"reason": reason, "text": text}


def job_stop_text(job: Any) -> str:
    """The sentence of `job_stop`; "" for a job that did not stop."""
    return job_stop(job)["text"]
