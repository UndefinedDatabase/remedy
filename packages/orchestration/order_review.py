"""An order's review report as Markdown (operator amendment amend1026-go-live-and-ask, Part D3).

`POST /api/v1/orders` with `capture_review: true` makes the walk leave a review report under the
data root's `review_reports` (`packages/orchestration/review_reports.py`). `GET
/api/v1/orders/{order}/review` and `remedy client order-review <order> --json` answer it rendered
as Markdown for a person: the outcome, the order, the configuration, each job with its tasks, runs
and verdicts, the usage and what the report cannot measure. The report is found by the id the
walk's answer names, or, while the walk runs, by the supervisor's order id the report records.

Remedy deliberately renders the report it kept and never a summary of its own: every figure here
is one the report holds, and a figure it does not hold reads `—`.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

#: The top-level keys of the answer beside the envelope's own.
ORDER_REVIEW_ANSWER_KEYS: tuple[str, ...] = ("markdown", "order_id", "report_id", "status")


def _figure(value: Any) -> str:
    return "—" if value is None or value == "" else str(value)


def _report_path(report_id: str, root: Path | None = None) -> Path | None:
    from packages.orchestration.review_reports import review_reports_dir

    if not report_id or "/" in report_id or "\x00" in report_id or report_id.startswith("."):
        return None
    path = review_reports_dir(root) / f"{report_id}.json"
    return path if path.is_file() else None


def find_order_review_report(paths: Any, record: Any, root: Path | None = None) -> dict[str, Any] | None:
    """The review report of the order RECORD names, or None when its walk kept none.

    The id the walk's answer names wins; without an answer (the walk runs, or printed none) the
    newest report whose `order.supervisor_order_id` is the order's id is read.
    """
    from packages.orchestration.review_reports import review_reports_dir
    from packages.orchestration.serve_runs import order_answer

    answer = order_answer(record) or {}
    named = answer.get("review_report") if isinstance(answer.get("review_report"), dict) else {}
    by_name = _report_path(str(named.get("report_id") or ""), root)
    folder = review_reports_dir(root)
    candidates = [by_name] if by_name is not None else (
        sorted(folder.glob("rr-*.json"), reverse=True) if folder.is_dir() else [])
    for path in candidates:
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(report, dict) and (
                by_name is not None or (report.get("order") or {}).get("supervisor_order_id") == record.order_id):
            return report
    return None


def _job_lines(job: dict[str, Any]) -> list[str]:
    lines = [f"### Job {_figure(job.get('job_id'))}: {_figure(job.get('title'))}", "",
             f"- State: {_figure(job.get('state'))}; duration {_figure(job.get('duration_s'))} s",
             f"- Verification: {_figure((job.get('verification') or {}).get('status'))}"]
    if job.get("error"):
        lines.append(f"- Error: {job['error']}")
    for task in job.get("tasks") or []:
        lines.append(f"- Task {_figure(task.get('task_id'))} {_figure(task.get('title'))}: "
                     f"{_figure(task.get('final_status'))}, reviewer {_figure(task.get('reviewer_verdict'))}, "
                     f"tests {_figure(task.get('test_passed'))}")
        for changed in task.get("changed_files") or []:
            lines.append(f"  - changed `{changed}`")
        for run in task.get("runs") or []:
            for round_ in run.get("rounds") or []:
                summary = str(round_.get("reviewer_summary") or "").strip()
                lines.append(f"  - round {_figure(round_.get('round'))}: verdict "
                             f"{_figure(round_.get('reviewer_verdict'))}" + (f" — {summary}" if summary else ""))
    for check in job.get("dod_checks") or []:
        lines.append(f"- Check {_figure(check.get('check_id'))} ({_figure(check.get('kind'))}): "
                     f"{_figure(check.get('status'))}")
    return [*lines, ""]


def render_review_report_markdown(report: dict[str, Any]) -> str:
    """REPORT, a `remedy_review_report_v1` object, as Markdown a person reads."""
    outcome = report.get("outcome") or {}
    order = report.get("order") or {}
    configuration = report.get("configuration") or {}
    providers = configuration.get("providers") or {}
    lines = [f"# Review report {_figure(report.get('report_id'))}", "",
             f"- Outcome: **{_figure(outcome.get('status'))}** — {_figure(outcome.get('reason'))}",
             f"- Started {_figure(report.get('started_at'))}, ended {_figure(report.get('ended_at'))}, "
             f"{_figure(report.get('duration_s'))} s",
             f"- Lane: {_figure(configuration.get('lane'))} ({_figure(configuration.get('lane_reason'))}); "
             f"shape {_figure(configuration.get('shape'))}",
             f"- Providers: planner {_figure(providers.get('planner'))}, builder {_figure(providers.get('builder'))}, "
             f"reviewer {_figure(providers.get('reviewer'))}", "",
             "## Order", "", "```", str(order.get("text") or "").strip(), "```", "", "## Jobs", ""]
    jobs = report.get("jobs") or []
    for job in jobs:
        lines += _job_lines(job if isinstance(job, dict) else {})
    if not jobs:
        lines += ["No job is recorded yet.", ""]
    lines += ["## Usage", ""]
    usage = report.get("usage_by_role")
    lines += (["```json", json.dumps(usage, indent=2, sort_keys=True, ensure_ascii=False), "```"]
              if usage else ["Not recorded."])
    for title, key in (("Landed", "landed"), ("Next", "next"), ("Not measured", "not_measured")):
        entries = report.get(key) or []
        if entries:
            lines += ["", f"## {title}", "", *(f"- {entry}" for entry in entries)]
    return "\n".join(lines).rstrip() + "\n"


def order_review_answer(*, order: str) -> dict[str, Any]:
    """The answer `GET /api/v1/orders/{order}/review` and `remedy client order-review --json` share:
    the order's review report as Markdown, `order_not_found` for an id no record names, or
    `review_report_not_found` when its walk kept no report."""
    from apps.cli.json_envelope import build_error, build_ok
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import order_not_found_message, read_order_record

    paths = serve_paths()
    record = read_order_record(paths, order)
    if record is None:
        return build_error("order_not_found", order_not_found_message(order))
    report = find_order_review_report(paths, record)
    if report is None:
        return build_error("review_report_not_found",
                           f"order {order!r} kept no review report; send it with capture_review true")
    return build_ok(order_id=record.order_id, report_id=str(report.get("report_id") or ""),
                    status=str((report.get("outcome") or {}).get("status") or ""),
                    markdown=render_review_report_markdown(report))
