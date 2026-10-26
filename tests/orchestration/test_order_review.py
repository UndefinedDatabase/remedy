"""An order's review report as Markdown (operator amendment amend1026-go-live-and-ask, Part D3):
`order_review.order_review_answer`, which `GET /api/v1/orders/{order}/review` and `remedy client
order-review --json` share."""
from __future__ import annotations

import json

import pytest

from packages.orchestration.order_review import order_review_answer, render_review_report_markdown

ORDER_ID = "0123456789abcdef"
REPORT_ID = "rr-20261026T100000Z-0a1b2c3d"


@pytest.fixture()
def order_with_log(tmp_path, monkeypatch):
    """An ended order whose out.log holds the walk's answer; the test writes the answer and the report."""
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import OrderRecord

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    paths = serve_paths()
    folder = paths.orders_dir / ORDER_ID
    folder.mkdir(parents=True)
    record = OrderRecord(order_id=ORDER_ID, pid=1, started_at="2026-10-26T10:00:00Z",
                         order_file=str(folder / "order.md"), out_log=str(folder / "out.log"),
                         err_log=str(folder / "err.log"), exit_code=0, ended_at="2026-10-26T10:05:00Z")
    (folder / "order.json").write_text(json.dumps(record.to_json()), encoding="utf-8")
    return folder, tmp_path / "data" / "review_reports"


def _report(report_id: str = REPORT_ID, order_id: str = ORDER_ID) -> dict:
    return {"schema": "remedy_review_report_v1", "report_id": report_id,
            "started_at": "2026-10-26T10:00:00+00:00", "ended_at": "2026-10-26T10:05:00+00:00", "duration_s": 300.0,
            "outcome": {"status": "completed", "reason": "every step ran"},
            "order": {"text": "Mach den Gruß freundlicher.", "supervisor_order_id": order_id},
            "configuration": {"lane": "full", "providers": {"planner": "claude-cli", "builder": "claude-cli"}},
            "jobs": [{"job_id": "24270f620da248bc", "title": "Gruß", "state": "completed",
                      "verification": {"status": "passed"},
                      "tasks": [{"task_id": "T001", "title": "core", "final_status": "completed",
                                 "reviewer_verdict": "pass", "test_passed": True, "changed_files": ["greet/core.py"],
                                 "runs": [{"rounds": [{"round": 1, "reviewer_verdict": "pass",
                                                       "reviewer_summary": "sauber"}]}]}]}],
            "usage_by_role": {"builder": {"tokens": 10}}, "landed": [], "next": ["remedy job apply"],
            "not_measured": ["queue time"]}


def test_the_report_the_walks_answer_names_is_rendered_as_markdown(order_with_log):
    folder, reports = order_with_log
    reports.mkdir(parents=True)
    (reports / f"{REPORT_ID}.json").write_text(json.dumps(_report()), encoding="utf-8")
    (folder / "out.log").write_text(json.dumps({"ok": True, "review_report": {"report_id": REPORT_ID}}) + "\n",
                                    encoding="utf-8")

    answer = order_review_answer(order=ORDER_ID)

    assert (answer["ok"], answer["order_id"], answer["report_id"], answer["status"]) == (
        True, ORDER_ID, REPORT_ID, "completed")
    markdown = answer["markdown"]
    assert markdown.startswith(f"# Review report {REPORT_ID}\n")
    for fragment in ("**completed**", "Mach den Gruß freundlicher.", "### Job 24270f620da248bc: Gruß",
                     "changed `greet/core.py`", "verdict pass — sauber", "## Not measured"):
        assert fragment in markdown


def test_without_an_answer_the_report_recording_the_orders_id_is_found(order_with_log):
    _folder, reports = order_with_log
    reports.mkdir(parents=True)
    (reports / "rr-20261026T090000Z-ffffffff.json").write_text(
        json.dumps(_report("rr-20261026T090000Z-ffffffff", "fedcba9876543210")), encoding="utf-8")
    (reports / f"{REPORT_ID}.json").write_text(json.dumps(_report()), encoding="utf-8")

    assert order_review_answer(order=ORDER_ID)["report_id"] == REPORT_ID


def test_an_order_without_a_report_and_an_unknown_order_are_refused(order_with_log):
    folder, _reports = order_with_log
    (folder / "out.log").write_text(json.dumps({"ok": True, "review_report": {"report_id": REPORT_ID}}) + "\n",
                                    encoding="utf-8")

    assert order_review_answer(order=ORDER_ID)["error"] == "review_report_not_found"
    assert order_review_answer(order="ffffffffffffffff")["error"] == "order_not_found"


def test_a_figure_the_report_does_not_hold_reads_a_dash():
    markdown = render_review_report_markdown({"report_id": "rr-x", "outcome": {"status": "running"}})
    assert "- Outcome: **running** — —" in markdown and "No job is recorded yet." in markdown
