#!/usr/bin/env python3
"""Select the evidence bundle for a review zip from the existing evidence index.

Never selects by raw filesystem modification time and never silently substitutes
a different job. Prints shell-friendly ``KEY=value`` lines:

    STATUS=selected|none
    JOB_ID=<id>
    EVIDENCE_DIR=<path>
    REASON=<machine reason>
    HISTORY=<job_id>:<path>[,<job_id>:<path>...]

Exit code is always 0; ``STATUS=none`` means the caller should build an honest
NO_EVIDENCE snapshot.
"""
from __future__ import annotations

import argparse
import os
import sys

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from packages.orchestration.evidence_index import select_evidence  # noqa: E402


def _path_of(record: dict) -> str:
    return str(record.get("evidence_export_path") or record.get("evidence_dir_local") or "")


def main() -> None:
    ap = argparse.ArgumentParser(description="Select review evidence from the index")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--job-id", default="")
    ap.add_argument("--include-recent", type=int, default=0)
    args = ap.parse_args()

    result = select_evidence(args.repo, job_id=args.job_id)
    selected = result["selected"]

    if selected is None:
        print("STATUS=none")
        print(f"REASON={result['reason']}")
        print("HISTORY=")
        return

    print("STATUS=selected")
    print(f"JOB_ID={selected.get('job_id', '')}")
    print(f"EVIDENCE_DIR={_path_of(selected)}")
    print(f"REASON={result['reason']}")

    history = []
    if args.include_recent > 0:
        for rec in result["history"][: args.include_recent]:
            jid, path = rec.get("job_id", ""), _path_of(rec)
            if jid and path and jid != selected.get("job_id"):
                history.append(f"{jid}:{path}")
    print("HISTORY=" + ",".join(history))


if __name__ == "__main__":
    main()
