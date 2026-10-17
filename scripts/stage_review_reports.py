#!/usr/bin/env python3
"""Stage the latest review reports for `make_review_zip.sh` (operator order exec-1017, D5).

    stage_review_reports.py --dest DIR [--limit 10]

Copies the newest LIMIT reports of `<data root>/review_reports/` (the ones `remedy do
--capture-review` leaves) into DIR, newest first by start time and then report id, failed and
cancelled runs included, and writes DIR/index.json and DIR/INDEX.md naming each with its outcome.
Every copy is redacted again on the way (the reports are redacted when written; this is the second
fence). With no report, the index says so and lists none: nothing is ever made up. Prints the
number of reports staged. The data root is the one Remedy resolves (`REMEDY_DATA_DIR`, the
configured `data_dir`, else this checkout's `.data`).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from packages.orchestration.review_reports import (  # noqa: E402
    REVIEW_REPORTS_CLASS,
    redact_review_report,
    review_reports_dir,
)

#: How many reports a review package carries.
REVIEW_ZIP_REPORT_LIMIT = 10


def latest_review_reports(folder: Path, limit: int) -> tuple[list[dict], list[str]]:
    """The newest *limit* readable reports, newest first, and a sentence per file that was not readable."""
    reports, unreadable = [], []
    for path in sorted(folder.glob("rr-*.json")) if folder.is_dir() else []:
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            unreadable.append(f"{path.name}: {type(exc).__name__}")
            continue
        if isinstance(report, dict) and report.get("report_id") == path.stem:
            reports.append(report)
        else:
            unreadable.append(f"{path.name}: not a review report of its own name")
    reports.sort(key=lambda r: (str(r.get("started_at") or ""), str(r["report_id"])), reverse=True)
    return reports[:limit], unreadable


def _entry(report: dict) -> dict:
    outcome = report.get("outcome") or {}
    configuration = report.get("configuration") or {}
    return {"report_id": report["report_id"], "file": f"{report['report_id']}.json",
            "started_at": report.get("started_at"), "ended_at": report.get("ended_at"),
            "duration_s": report.get("duration_s"), "status": outcome.get("status"),
            "reason": str(outcome.get("reason") or "")[:200], "lane": configuration.get("lane"),
            "job_ids": report.get("job_ids") or [],
            "order": " ".join(str((report.get("order") or {}).get("text") or "").split())[:160]}


def stage(dest: Path, limit: int = REVIEW_ZIP_REPORT_LIMIT, root: Path | None = None) -> int:
    folder = review_reports_dir(root)
    reports, unreadable = latest_review_reports(folder, limit)
    reports = [redact_review_report(report) for report in reports]      # before any byte is written
    dest.mkdir(parents=True, exist_ok=True)
    for report in reports:
        (dest / f"{report['report_id']}.json").write_text(
            json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8")
    entries = [_entry(report) for report in reports]
    note = (f"the {len(entries)} newest review reports, newest first" if entries else
            f"no review report exists under the data root's {REVIEW_REPORTS_CLASS}/; run `remedy do "
            f"--capture-review` (or POST /api/v1/orders with capture_review) to leave one")
    index = {"schema": "remedy_review_report_index_v1", "limit": limit, "count": len(entries),
             "note": note, "unreadable": unreadable, "reports": entries}
    (dest / "index.json").write_text(json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                                     encoding="utf-8")
    lines = ["# Review reports", "", f"{note[0].upper()}{note[1:]}.", ""]
    if entries:
        lines += ["| report | started | status | lane | jobs | order |", "|---|---|---|---|---|---|"]
        lines += [f"| {e['file']} | {e['started_at']} | {e['status']} | {e['lane']} | "
                  f"{', '.join(e['job_ids']) or '-'} | {e['order'].replace('|', '/')} |" for e in entries]
    lines += [f"- unreadable: {item}" for item in unreadable]
    (dest / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(entries)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dest", required=True)
    parser.add_argument("--limit", type=int, default=REVIEW_ZIP_REPORT_LIMIT)
    args = parser.parse_args()
    print(stage(Path(args.dest), args.limit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
