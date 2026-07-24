"""Aggregate failure post-mortems from the filesystem (F010 T003).

Files, not a database: the post-mortems already exist as JSON inside the evidence exports,
and a second copy of the truth in a schema of its own is a second thing to keep honest. So
this scans, counts, and says exactly what it could not read.

Three scopes, never mixed:

* ``call`` — one finally-failed logical provider call;
* ``task`` — one terminally failed task;
* ``job``  — a job that failed before any task could own the failure (a worktree lock
  during workspace acquisition, say).

A task rollup POINTS AT the call post-mortems below it, and only the CANONICAL exported
copy under ``call_postmortems/`` is counted — the streamed source copy is the same record,
and counting both would double every streamed failure.

What this covers: the EVIDENCE EXPORTS. A job whose evidence was never exported is not in
the corpus at all — this does not scan the job registry and does not pretend to. Exported
tasks that predate F010 have no post-mortems and are not silently skipped: they show up in
``coverage`` as scanned-but-unexplained, because "we have no record" is a fact worth
printing.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.orchestration.data_paths import evidence_exports_dir
from packages.orchestration.failure_postmortem import (
    CALL_POSTMORTEM_SUBDIR,
    POSTMORTEM_FILENAME,
    POSTMORTEM_VERSION,
)

#: F011: the exported layout of one stop episode's record. Imported by name (not from
#: pingpong_job) so a read-only stats scan never drags the job runner into the process.
STOP_POSTMORTEM_SUBDIR = "stop_postmortems"

#: Result schema version. Consumers may pin it.
STATS_VERSION = 1

#: How many distinct reasons the report carries. Bounded, so a pathological corpus cannot
#: turn a summary into a dump of provider output.
TOP_REASONS_LIMIT = 10

#: How much of a reason is used as a histogram key.
REASON_KEY_CHARS = 120


class FailureStatsError(RuntimeError):
    """The evidence root itself could not be read. Never reported as "no failures"."""


@dataclass
class ScanCounters:
    jobs_scanned: int = 0
    tasks_scanned: int = 0
    tasks_without_postmortem: int = 0
    malformed: int = 0
    unsupported_version: int = 0
    warnings: list[str] = field(default_factory=list)


def _reason_key(record: dict[str, Any]) -> str:
    """A deterministic, bounded histogram key. Never free-text deduplication.

    Redacted again on the way OUT: records are redacted when they are written, but stats
    also reads corpora written by an older build (or by hand), and a secret must not reach
    a terminal just because it reached a file.
    """
    from packages.orchestration.failure_postmortem import safe_text

    reason = safe_text(str(record.get("raw_reason") or "")).strip().replace("\n", " ")
    if not reason:
        reason = str(record.get("terminal_status") or record.get("signal_source") or "")
    return reason[:REASON_KEY_CHARS]


def _load(path: Path, counters: ScanCounters, base: Path) -> dict[str, Any] | None:
    """Read one record. A bad file is counted and NAMED — it never kills the scan.

    Named by its path relative to the evidence root, not by the bare filename: every
    post-mortem in the corpus is called ``postmortem.json``, so "malformed:
    postmortem.json" told an operator nothing about which one to go and look at.
    """
    try:
        where = path.relative_to(base).as_posix()
    except ValueError:
        where = path.name

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        counters.malformed += 1
        counters.warnings.append(f"unreadable: {where} ({type(exc).__name__})")
        return None
    except ValueError:
        counters.malformed += 1
        counters.warnings.append(f"malformed JSON: {where}")
        return None
    if not isinstance(data, dict):
        counters.malformed += 1
        counters.warnings.append(f"not a JSON object: {where}")
        return None
    if data.get("postmortem_v") != POSTMORTEM_VERSION:
        counters.unsupported_version += 1
        counters.warnings.append(
            f"unsupported postmortem_v {data.get('postmortem_v')!r}: {where}")
        return None
    return data


def collect_failures(
    *,
    root: str | Path | None = None,
    job: str = "",
    since: str = "",
    job_ids: set[str] | None = None,
) -> dict[str, Any]:
    """Scan the evidence exports and return the stable aggregation result.

    ``since`` uses the repository's existing timestamp semantics (an ISO-8601 string,
    compared lexicographically — the same rule ``remedy event list --since`` already
    follows), so operators do not have to learn a second duration language.
    """
    base = Path(root) if root is not None else evidence_exports_dir()
    counters = ScanCounters()

    counts_by_class: dict[str, int] = {}
    counts_by_scope: dict[str, int] = {"call": 0, "job": 0, "task": 0}
    reasons: dict[str, int] = {}
    total = 0

    if base.exists() and not base.is_dir():
        raise FailureStatsError(f"evidence root is not a directory: {base}")

    job_dirs: list[Path] = []
    if base.is_dir():
        try:
            job_dirs = sorted(p for p in base.iterdir() if p.is_dir())
        except OSError as exc:
            raise FailureStatsError(
                f"evidence root is not readable: {base} ({type(exc).__name__}: {exc})"
            ) from exc

    def _count(record: dict[str, Any]) -> None:
        nonlocal total
        scope = str(record.get("scope") or "call")
        cls = str(record.get("failure_class") or "unknown")
        counts_by_scope[scope] = counts_by_scope.get(scope, 0) + 1
        counts_by_class[cls] = counts_by_class.get(cls, 0) + 1
        reasons[_reason_key(record)] = reasons.get(_reason_key(record), 0) + 1
        total += 1

    for job_dir in job_dirs:
        if job and job_dir.name != job:
            continue
        if job_ids is not None and job_dir.name not in job_ids:
            continue
        counters.jobs_scanned += 1

        # A JOB-scope record: the job failed before any task could own the failure (a
        # worktree lock during workspace acquisition, say). It is counted in its own scope.
        job_pm = job_dir / POSTMORTEM_FILENAME
        if job_pm.is_file():
            record = _load(job_pm, counters, base)
            if record is not None and (
                not since or str(record.get("created_at", "")) >= since):
                _count(record)

        # F011: each stop EPISODE is its own job-scope record, under its request id. One
        # per consumed request — a job stopped twice is two records, and a duplicated stop
        # command (one request) is still one.
        stop_root = job_dir / STOP_POSTMORTEM_SUBDIR
        if stop_root.is_dir():
            for stop_path in sorted(stop_root.rglob(POSTMORTEM_FILENAME)):
                record = _load(stop_path, counters, base)
                if record is not None and (
                    not since or str(record.get("created_at", "")) >= since):
                    _count(record)

        task_runs = job_dir / "task_runs"
        if not task_runs.is_dir():
            continue
        try:
            task_dirs = sorted(p for p in task_runs.iterdir() if p.is_dir())
        except OSError as exc:
            counters.warnings.append(
                f"unreadable task_runs in {job_dir.name}: {type(exc).__name__}")
            continue

        for task_dir in task_dirs:
            counters.tasks_scanned += 1
            found_any = False

            rollup_path = task_dir / POSTMORTEM_FILENAME
            if rollup_path.is_file():
                record = _load(rollup_path, counters, base)
                if record is not None:
                    found_any = True
                    if not since or str(record.get("created_at", "")) >= since:
                        _count(record)

            # ONLY the canonical exported location. The source copy under
            # ``task_runs/<task>/streams/...`` is the same record, and counting both would
            # double every streamed failure.
            call_root = task_dir / CALL_POSTMORTEM_SUBDIR
            if call_root.is_dir():
                for call_path in sorted(call_root.rglob(POSTMORTEM_FILENAME)):
                    record = _load(call_path, counters, base)
                    if record is None:
                        continue
                    found_any = True
                    if not since or str(record.get("created_at", "")) >= since:
                        _count(record)

            if not found_any:
                # A task that never failed has nothing to explain — and so does a task
                # from before F010 existed. Both are honestly "no post-mortem here".
                counters.tasks_without_postmortem += 1

    top_reasons = [
        {"reason": reason, "count": count}
        for reason, count in sorted(reasons.items(), key=lambda kv: (-kv[1], kv[0]))
    ][:TOP_REASONS_LIMIT]

    return {
        "version": STATS_VERSION,
        "filters": {"job": job or "", "since": since or ""},
        "total_postmortems": total,
        "counts_by_class": dict(sorted(counts_by_class.items())),
        "counts_by_scope": dict(sorted(counts_by_scope.items())),
        "top_reasons": top_reasons,
        "coverage": {
            "jobs_scanned": counters.jobs_scanned,
            "tasks_scanned": counters.tasks_scanned,
            "tasks_without_postmortem": counters.tasks_without_postmortem,
            "malformed_postmortems": counters.malformed,
            "unsupported_version_postmortems": counters.unsupported_version,
        },
        "warnings": sorted(counters.warnings),
        "evidence_root": base.name,
    }


def render_human(result: dict[str, Any]) -> str:
    """The same truth, for a person. Deterministic order; nothing invented."""
    lines: list[str] = []
    coverage = result["coverage"]

    if result["total_postmortems"] == 0:
        lines.append("No failures recorded.")
    else:
        lines.append(f"Failures: {result['total_postmortems']} post-mortems")
        lines.append("")
        lines.append("By class:")
        for cls, count in result["counts_by_class"].items():
            lines.append(f"  {cls:<24} {count}")
        lines.append("")
        lines.append("By scope:")
        for scope, count in result["counts_by_scope"].items():
            lines.append(f"  {scope:<24} {count}")
        if result["top_reasons"]:
            lines.append("")
            lines.append("Top reasons:")
            for entry in result["top_reasons"]:
                lines.append(f"  {entry['count']:>3}  {entry['reason']}")

    lines.append("")
    lines.append(
        f"Coverage: {coverage['tasks_scanned']} scanned, "
        f"{coverage['tasks_without_postmortem']} without postmortems"
    )
    if coverage["malformed_postmortems"] or coverage["unsupported_version_postmortems"]:
        lines.append(
            f"  unreadable: {coverage['malformed_postmortems']} malformed, "
            f"{coverage['unsupported_version_postmortems']} unsupported version"
        )
    return "\n".join(lines)
